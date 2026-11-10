"""Exact binary CSS and subsystem gauge decomposition on 144 address-labelled qubits.

Parent: two-variable BB code (12,6), A=x^3+y+y^2, B=y^3+x+x^2.
This is the 144-qubit, 12-logical bivariate-bicycle parent used in published code examples.
Subsystem: choose 54 independent X and 54 independent Z checks;
restore omitted 12+12 as canonical pairs to expose 12 protected + 24 gauge qubits.
The Q72 address labelling is bijective; product uses commuting x/y translations.
"""
import json,sys,itertools
from pathlib import Path
import numpy as np

def rank_and_indices(a):
  ar=(a.copy()&1).astype(np.uint8);nrows,ncols=ar.shape;inds=np.arange(nrows)
  r=0
  for c in range(ncols):
    cand=np.flatnonzero(ar[r:,c]);
    if len(cand)==0:continue
    piv=cand[0]+r;ar[[r,piv]]=ar[[piv,r]];inds[[r,piv]]=inds[[piv,r]]
    rr=np.flatnonzero(ar[r+1:,c])+r+1
    ar[rr]^=ar[r]
    r+=1
    if r==nrows:break
  return r,inds[:r].tolist()

def gf2_inv(a):
  n=len(a);v=np.concatenate([a.copy()%2,np.eye(n,dtype=np.uint8)],axis=1)
  for j in range(n):
    piv=next((i for i in range(j,n) if v[i,j]),None)
    if piv is None:raise RuntimeError('matrix singular')
    if piv!=j:v[[j,piv]]=v[[piv,j]]
    ix=np.where(v[:,j]==1)[0];ix=ix[ix!=j];v[ix]^=v[j]
  return v[:,n:]

def right_inverse(A):
  rank,cols=rank_and_indices(A.T)
  assert rank==len(A)
  B=A[:,cols];Bi=gf2_inv(B)
  ret=np.zeros((A.shape[1],A.shape[0]),dtype=np.uint8)
  ret[cols,:]=Bi
  assert np.array_equal((A@ret)%2,np.eye(len(A),dtype=np.uint8))
  return ret

def bb_matrices():
  l,m=12,6;n=l*m
  def shift(dx,dy):
    M=np.zeros((n,n),dtype=np.uint8)
    for x in range(l):
      for y in range(m): M[x*m+y,((x+dx)%l)*m+(y+dy)%m]=1
    return M
  A=shift(3,0)^shift(0,1)^shift(0,2)
  B=shift(0,3)^shift(1,0)^shift(2,0)
  hx=np.concatenate([A,B],axis=1)
  hz=np.concatenate([B.T,A.T],axis=1)
  assert not np.any((hx@hz.T)%2)
  return hx,hz

def pivots(a):
  r,ix=rank_and_indices(a)
  return a[ix,:].copy(),a[[j for j in range(len(a)) if j not in ix],:].copy(),r

def list2mask(bits):
  return sum(int(v)<<i for i,v in enumerate(bits))

def basis_masks(a):
  b={}
  for row in a:
    x=list2mask(row)
    while x:
      p=x.bit_length()-1
      if p not in b:
        b[p]=x;break
      x^=b[p]
  return b

def in_span(x,b):
  x=int(x)
  while x:
    p=x.bit_length()-1
    if p not in b:return False
    x^=b[p]
  return True

def min_witness(Hcheck,GX,maxw=3):
  basis=basis_masks(GX)
  cols=[list2mask(Hcheck[:,i]) for i in range(Hcheck.shape[1])]
  n=len(cols)
  # X syndrome H_Z * error; skip vector if gauge subgroup.
  for w in range(1,maxw+1):
    for ii in itertools.combinations(range(n),w):
      syndrome=0;mask=0
      for i in ii:syndrome ^= cols[i];mask |= 1<<i
      if syndrome==0 and not in_span(mask,basis):return {'weight':w,'indices':list(ii),'type':'logical'}
  return None

def main():
  hx,hz=bb_matrices()
  rx,ix=rank_and_indices(hx);rz,iz=rank_and_indices(hz)
  hxf=hx[ix];hzf=hz[iz]
  assert rx==66 and rz==66
  hxr,hxo=hxf[:54],hxf[54:];hzr,hzo=hzf[:54],hzf[54:]
  assert rank_and_indices(hxr)[0]==54 and rank_and_indices(hzr)[0]==54
  # Symplectic gauge duals from right inverses of the complete parent check bases.
  Xright=right_inverse(hxf);Zright=right_inverse(hzf)
  ZA=Xright[:,54:66].T.copy() # conjugate to 12 X omitted checks
  XB=Zright[:,54:66].T.copy() # conjugate to 12 Z omitted checks
  XA=hxo.copy();ZB=hzo.copy()
  # Remove XA/Z_A cross-pairing from XB by XA shifts.
  c=(XB@ZA.T)%2
  XB^=(c@XA)%2
  # XGA=XA, ZGA=ZA ; XGB=XB, ZGB=ZB ; other mixed pairs vanish.
  assert np.array_equal((XA@ZA.T)%2,np.eye(12,dtype=np.uint8))
  assert np.array_equal((XB@ZB.T)%2,np.eye(12,dtype=np.uint8))
  assert not np.any((XA@ZB.T)%2) and not np.any((XB@ZA.T)%2)
  assert not np.any((hxr@ZA.T)%2) and not np.any((hxr@ZB.T)%2)
  assert not np.any((hzr@XA.T)%2) and not np.any((hzr@XB.T)%2)
  GX=np.concatenate([hxr,XA,XB],axis=0)
  GZ=np.concatenate([hzr,ZA,ZB],axis=0)
  assert rank_and_indices(GX)[0]==78 and rank_and_indices(GZ)[0]==78
  rank_sx=rank_and_indices(hxr)[0];rank_sz=rank_and_indices(hzr)[0]
  k_css=144-rank_sx-rank_sz;gauge_pairs=24;k_protected=k_css-gauge_pairs
  assert (k_css,gauge_pairs,k_protected)==(36,24,12)
  # Explore dressed logical low-weight states for the obtained subsystem.
  wx=min_witness(hzr,GX,maxw=3)
  wz=min_witness(hxr,GZ,maxw=3)
  # Output dense binary matrices and full canonical gauge generator sets.
  dest=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results');dest.mkdir(parents=True,exist_ok=True)
  np.savez_compressed(dest/'Q72_144_qubit_subsystem_matrices.npz',HX_parent=hx,HZ_parent=hz,HX_center=hxr,HZ_center=hzr,GA_X=XA,GA_Z=ZA,GB_X=XB,GB_Z=ZB,GX_full=GX,GZ_full=GZ,addr=np.array([[z,a,b] for z in range(3) for a in range(12) for b in range(2)],dtype=np.uint8))
  report={'n':144,'parent_hx_rank':rx,'parent_hz_rank':rz,'parent_k':144-rx-rz,'center_hx_rank':rank_sx,'center_hz_rank':rank_sz,'center_k':k_css,'gauge_qubits':gauge_pairs,'protected_qubits':k_protected,'gauge_symplectic_pairs':24,'checks_commute':True,'low_weight_dressed_X_witness_up_to3':wx,'low_weight_dressed_Z_witness_up_to3':wz,'address_label':'Z3 x Dic6 (z,a,b) bijection; X/Y actions are commuting translation coordinatization, distinct from Dic6 group multiplication','parent_polynomials':'A=x^3+y+y^2; B=y^3+x+x^2 on Z12 x Z6','parent_distance_reference':12}
  (dest/'qec_144_subsystem.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
