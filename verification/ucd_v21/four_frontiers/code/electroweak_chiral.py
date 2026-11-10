"""Kelvin/BCC dynamic SU(2)_L x U(1)_Y Wilson-overlap finite-lattice experiment.

Constructs the 4D gamma matrices, explicit 8-direction BCC Wilson links,
charged doublet/singlet kernels, local gauge transformations, overlap operator,
and exact anomaly sums for three Standard Model generations.
"""
import json,sys
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from kelvin import V,DISP,W

I2=np.eye(2,dtype=complex); Z2=np.zeros((2,2),complex)
sigma=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.]).astype(complex)]
def blk(a,b,c,d):return np.block([[a,b],[c,d]])
gamma=[blk(Z2,I2,I2,Z2)]+[blk(Z2,-1j*s,1j*s,Z2) for s in sigma]
g5=gamma[0]@gamma[1]@gamma[2]@gamma[3]
assert np.max(np.abs(g5@g5-np.eye(4)))<1e-12
nvec=[np.array([1,0,0,0.])]+[np.array([0,*np.array(v,dtype=float)/np.linalg.norm(v)]) for v in V]
gam_n=[sum(float(a)*g for a,g in zip(n,gamma)) for n in nvec]
weights=np.array([1]+[float(w) for w in W]);

def small_geometry(L=2,Nt=2):
  coords=[(t,x,y,z) for t in range(Nt) for x in range(2*L) for y in range(2*L) for z in range(2*L) if x%2==y%2==z%2]; idx={p:i for i,p in enumerate(coords)}
  mod=np.array([Nt,2*L,2*L,2*L]);plus=np.array([[idx[tuple((np.array(c)+d)%mod)] for d in DISP] for c in coords]); return plus

def su2(rng,ang=.16):
  v=rng.normal(size=3);v/=np.linalg.norm(v)
  a=np.cos(ang)+1j*np.sin(ang)*v[0];b=np.sin(ang)*(v[1]+1j*v[2]);return np.array([[a,b],[-b.conjugate(),a.conjugate()]])

def fields(plus,iso,charge,seed=412):
  rng=np.random.default_rng(seed);ns=len(plus)
  U=np.empty((ns,8,iso,iso),complex);theta=rng.normal(scale=.22,size=(ns,8))
  for x in range(ns):
    for d in range(8):U[x,d]=su2(rng) if iso==2 else np.eye(1)
  F=U*np.exp(1j*charge*theta)[:,:,None,None]
  G=np.array([su2(rng,ang=.25) if iso==2 else np.eye(1) for x in range(ns)])
  phi=rng.normal(scale=.2,size=ns)
  loc=G*np.exp(1j*charge*phi)[:,None,None]
  # Covariant transformed links, including exact hypercharge phases.
  Utr=np.array([[G[x]@U[x,d]@G[plus[x,d]].conj().T for d in range(8)] for x in range(ns)])
  theta_tr=np.array([[theta[x,d]+phi[x]-phi[plus[x,d]] for d in range(8)] for x in range(ns)])
  Ftr=Utr*np.exp(1j*charge*theta_tr)[:,:,None,None]
  return F,Ftr,loc

def wilson(plus,F,rho=0.,r=1.):
  ns,n_dir,iso,_=F.shape;n=ns*4*iso
  D=np.zeros((n,n),complex)
  I4=np.eye(4);Iint=np.eye(iso)
  center=float(weights.sum())*r
  for x in range(ns):
    sl=slice(x*4*iso,(x+1)*4*iso)
    D[sl,sl]+=(center-rho)*np.eye(4*iso)
    for d in range(8):
      y=plus[x,d];sy=slice(y*4*iso,(y+1)*4*iso)
      D[sl,sy]+=-.5*weights[d]*np.kron(r*I4-gam_n[d],F[x,d])
      D[sy,sl]+=-.5*weights[d]*np.kron(r*I4+gam_n[d],F[x,d].conj().T)
  return D

def overlap(D):
  N=D.shape[0];iso=N//(4*ns_global)
  G5=np.kron(np.eye(ns_global),np.kron(g5,np.eye(iso)))
  H=G5@D
  herm=float(np.linalg.norm(H-H.conj().T,ord='fro'))
  evals, vec=eigh(H)
  S=(vec*np.sign(evals))@vec.conj().T
  O=np.eye(N,dtype=complex)+G5@S
  gw=np.linalg.norm(G5@O+O@G5-O@G5@O,ord='fro')
  return O,gw,herm,float(np.min(np.abs(evals)))

def anomalies():
  # All charges are L-handed; right-handed fermions contribute with conjugated Y.
  fields=[('Q_L',6,Q(1,3)),('u_R^c',3,Q(-4,3)),('d_R^c',3,Q(2,3)),('L_L',2,Q(-1)),('e_R^c',1,Q(2)),('nu_R^c',1,Q(0))]
  cubic=sum(mult*y**3 for _,mult,y in fields)
  grav=sum(mult*y for _,mult,y in fields)
  su2sq=3*Q(1,3)+Q(-1)
  su3sq=2*Q(1,3)+Q(-4,3)+Q(2,3)
  return {"U1_cubic":str(cubic),"gravitational_U1":str(grav),"SU2_squared_U1":str(su2sq),"SU3_squared_U1":str(su3sq),"left_SU2_doublets_three_generations":12}

def main():
  global ns_global
  plus=small_geometry();ns_global=len(plus);out={"sites":ns_global,"directions":8,"sectors":{},"anomalies":anomalies()}
  assert all(v=='0' for k,v in out['anomalies'].items() if k!='left_SU2_doublets_three_generations')
  for name,iso,y in [('left_weak_doublet',2,Q(1,3)),('right_charged_singlet',1,Q(-2))]:
    F,Ftr,loc=fields(plus,iso,float(y),seed=1445+iso)
    D=wilson(plus,F,rho=.5)
    Dt=wilson(plus,Ftr,rho=.5)
    G=np.kron(np.eye(1),np.block([[loc[i] if i==j else np.zeros((iso,iso)) for j in range(ns_global)] for i in range(ns_global)]))
    # Geometry ordering: site, spin, weak/color rep.
    G=np.kron(np.eye(ns_global),np.eye(4*iso)).astype(complex)
    for x in range(ns_global):G[x*4*iso:(x+1)*4*iso,x*4*iso:(x+1)*4*iso]=np.kron(np.eye(4),loc[x])
    residual=float(np.linalg.norm(Dt-G@D@G.conj().T,ord='fro'))
    O,gw,herm,mingap=overlap(D);Ot,gwtr,_,_=overlap(Dt)
    ovres=float(np.linalg.norm(Ot-G@O@G.conj().T,ord='fro'))
    out['sectors'][name]={"matrix_size":len(D),"Y":str(y),"wilson_gauge_covariance_fro":residual,"overlap_gauge_covariance_fro":ovres,"gw_fro":gw,"gw_transformed_fro":gwtr,"gamma5_hermitian_fro":herm,"min_abs_wilson_kernel_eig":mingap}
    assert residual<1e-10 and ovres<1e-8 and gw<1e-8
  dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results'
  dest.mkdir(parents=True,exist_ok=True);(dest/'electroweak_chiral.json').write_text(json.dumps(out,indent=2))
  print(json.dumps(out,indent=2))
if __name__=='__main__':main()
