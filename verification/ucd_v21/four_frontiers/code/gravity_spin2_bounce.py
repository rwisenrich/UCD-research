"""Exact Kelvin 2nd/4th moments, Richardson spin-2 TT kernel, core bounce."""
import json,sys,math
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from kelvin import V,W

def moments():
  vec=[tuple(Q(int(x),2) for x in v) for v in V]
  second=[[sum(w*v[i]*v[j] for w,v in zip(W,vec)) for j in range(3)] for i in range(3)]
  fourth=[[[[sum(w*v[i]*v[j]*v[k]*v[l] for w,v in zip(W,vec)) for l in range(3)] for k in range(3)] for j in range(3)] for i in range(3)]
  assert second==[[Q(1,2) if i==j else Q(0) for j in range(3)] for i in range(3)]
  assert all(fourth[i][j][k][l]==Q(1,12)*(int(i==j)*int(k==l)+int(i==k)*int(j==l)+int(i==l)*int(j==k)) for i in range(3) for j in range(3) for k in range(3) for l in range(3))
  return {'second':[[str(x) for x in row] for row in second], 'fourth_all':True,'fourth_spatial_isotropic_coefficient':'1/12'}

def L(k,a):
  vec=V/2.
  return sum(4*float(w)*(1-math.cos(float(a*np.dot(k,v))))/(a*a) for w,v in zip(W,vec))

def improved(k,a):return (4*L(k,a)-L(k,2*a))/3

def tt_projector(k):
    kh=k/np.linalg.norm(k);P=np.eye(3)-np.outer(kh,kh)
    Q=np.empty((9,9))
    for i in range(3):
      for j in range(3):
        for l in range(3):
          for m in range(3):Q[3*i+j,3*l+m]=.5*(P[i,l]*P[j,m]+P[i,m]*P[j,l])-.5*P[i,j]*P[l,m]
    return Q

def run():
  v=moments(); q=np.array([.7,.4,.2]);q2=float(q@q)
  refinement=[]
  for a in [.8,.4,.2,.1,.05]:
    err2=abs(L(q,a)/q2-1);err4=abs(improved(q,a)/q2-1)
    refinement.append({'a':a,'relative_unimproved_error':float(err2),'relative_improved_error':float(err4)})
  ratios2=[refinement[i]['relative_unimproved_error']/refinement[i+1]['relative_unimproved_error'] for i in range(4)]
  ratios4=[refinement[i]['relative_improved_error']/refinement[i+1]['relative_improved_error'] for i in range(4)]
  assert abs(ratios2[0]-4)<.2 and abs(ratios4[0]-16)<2
  rng=np.random.default_rng(778)
  residuals=[]
  for _ in range(40):
    k=rng.normal(size=3);P=tt_projector(k)
    ev=np.linalg.eigvalsh(P);residuals.append([float(np.linalg.norm(P@P-P)),float(np.linalg.norm(P-P.T)),float(np.linalg.norm(np.sort(ev)-np.array([0]*7+[1]*2)))])
  assert np.max(np.array(residuals))<1e-12
  # Homogeneous effective-core first integral, in units G=M=1, length ell0 arbitrary.
  G=M=1.;ell0=.2;Rb=(6*G*M*ell0**2)**(1./3.)
  rows=[]
  for tau in np.linspace(-4,4,41):
    R=(Rb**3+4.5*G*M*tau*tau)**(1./3.)
    dR=3*G*M*tau/R**2
    energy=(dR*dR-(2*G*M/R)*(1-(Rb/R)**3))
    d2R=(-G*M/R**2+4*G*M*Rb**3/R**5)
    rows.append({'tau':float(tau),'radius':float(R),'velocity':float(dR),'acceleration':float(d2R),'first_integral_residual':float(energy)})
  assert max(abs(r['first_integral_residual']) for r in rows)<1e-12
  v.update({'spin2':{'TT_dimension':2,'TT_projector_max_residual':float(np.max(np.array(residuals))), 'unimproved_refinement':refinement,'ratio_second':ratios2,'ratio_fourth':ratios4},'regular_core':{'G':G,'M':M,'ell0':ell0,'Rb':Rb,'bounce_acceleration':3*G*M/Rb**2,'trajectory':rows}})
  return v
if __name__=='__main__':
  res=run();p=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results');p.mkdir(parents=True,exist_ok=True)
  (p/'gravity_spin2_bounce.json').write_text(json.dumps(res,indent=2));print(json.dumps({'TT_dim':res['spin2']['TT_dimension'],'max_projector_err':res['spin2']['TT_projector_max_residual'],'ratios4':res['spin2']['ratio_fourth'],'Rb':res['regular_core']['Rb'],'first_integral_max':max(abs(x['first_integral_residual']) for x in res['regular_core']['trajectory'])},indent=2))
