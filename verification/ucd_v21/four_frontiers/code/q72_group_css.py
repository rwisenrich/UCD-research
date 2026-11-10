"""A native non-Abelian Z3 x Dic6 group-addressed 144-qubit CSS construction.
The group action is represented exactly on 72 addresses; two-sided group algebra
ensures the A,B blocks commute, and GF(2) CSS orthogonality is automatic.
"""
import json,sys
from pathlib import Path
import numpy as np
from qec_144_subsystem import rank_and_indices
from qec_search_sparse_center import min_dressed_to6

GROUP=[(z,a,b) for z in range(3) for a in range(12) for b in range(2)]
IDX={e:i for i,e in enumerate(GROUP)}
def mul(g,h):
  z,a,b=g;w,c,d=h
  return ((z+w)%3,(a+(-1 if b else 1)*c+6*b*d)%12,(b+d)%2)
def perm(g,side):
  n=72;A=np.zeros((n,n),dtype=np.uint8)
  for i,h in enumerate(GROUP):
    j=IDX[mul(g,h) if side=='L' else mul(h,g)]
    A[j,i]=1
  return A

def main():
  I=np.eye(72,dtype=np.uint8);a3=perm((0,3,0),'L');xr=perm((0,0,1),'R')
  A=I^a3
  B=(A@(I^xr))%2
  HX=np.concatenate([A,B],axis=1); HZ=np.concatenate([B.T,A.T],axis=1)
  assert not np.any((HX@HZ.T)%2)
  rx=rank_and_indices(HX)[0];rz=rank_and_indices(HZ)[0]
  assert (rx,rz)==(54,54)
  X=min_dressed_to6(HZ,HX); Z=min_dressed_to6(HX,HZ)
  # Non-Abelian witness: a*x != x*a in Dic6; L(a)R(x) commute as actions.
  a=(0,1,0);x=(0,0,1);assert mul(a,x)!=mul(x,a)
  assert np.array_equal((perm(a,'L')@perm(x,'R'))%2,(perm(x,'R')@perm(a,'L'))%2)
  result={'group':'Z3 x Dic6','group_order':72,'nonabelian':True,'n_qubits':144,'generator_A':'I + L(a^3)','generator_B':'(I+L(a^3))(I+R(x))','HX_rank':rx,'HZ_rank':rz,'logical_qubits':144-rx-rz,'HX_row_weights':sorted(set(map(int,HX.sum(axis=1)))),'HZ_row_weights':sorted(set(map(int,HZ.sum(axis=1)))),'CSS_commutation':True,'low_weight_X':X,'low_weight_Z':Z}
  dest=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results');dest.mkdir(parents=True,exist_ok=True)
  np.savez_compressed(dest/'Q72_native_group_CSS_144.npz',HX=HX,HZ=HZ,A=A,B=B,group_elements=np.array(GROUP,dtype=np.uint8))
  (dest/'q72_native_group_css.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
