"""Search sparse 144-qubit CSS on genuine Z3 x Dic6 two-sided group ring.
A=(1+L(a^3)), B=A * sum_{g in T} R(g), all commute and rank 54 exactly.
"""
import json,sys
from pathlib import Path
import numpy as np
from q72_group_css import GROUP,perm,IDX
from qec_144_subsystem import rank_and_indices
from qec_search_sparse_center import min_dressed_to6

def main():
  dest=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results');dest.mkdir(parents=True,exist_ok=True)
  I=np.eye(72,dtype=np.uint8);A=I^perm((0,3,0),'L');rg=np.random.default_rng(20261110)
  R=[perm(g,'R') for g in GROUP]; log=[]
  best=None
  for trial in range(100):
    inds=rg.choice(72,size=3,replace=False)
    B=(A@(R[inds[0]]^R[inds[1]]^R[inds[2]]))%2
    Hx=np.concatenate([A,B],axis=1);Hz=np.concatenate([B.T,A.T],axis=1)
    if np.any((Hx@Hz.T)%2):raise RuntimeError('commuting group ring construction failed')
    if rank_and_indices(Hx)[0]!=54 or rank_and_indices(Hz)[0]!=54:continue
    xx=min_dressed_to6(Hz,Hx);zz=min_dressed_to6(Hx,Hz)
    wx=xx.get('weight',7);wz=zz.get('weight',7)
    report={'trial':trial,'right_elements':[GROUP[int(x)] for x in inds],'row_weights_HX':sorted(set(map(int,Hx.sum(axis=1)))),'X_smallest_witness':xx,'Z_smallest_witness':zz}
    log.append(report)
    if best is None or min(wx,wz)>best[0]:best=(min(wx,wz),trial,Hx,Hz,B,report)
    print('trial',trial,'wX',wx,'wZ',wz,flush=True)
    if wx>=4 and wz>=4:break
  if best:
    _,trial,Hx,Hz,B,report=best
    np.savez_compressed(dest/'Q72_native_CSS_144_optimized.npz',HX=Hx,HZ=Hz,A=A,B=B,group_elements=np.array(GROUP,dtype=np.uint8))
  result={'attempts':len(log),'chosen_trial':best[1] if best else None,'chosen':best[-1] if best else None,'candidates':log}
  (dest/'q72_native_css_optimized.json').write_text(json.dumps(result,indent=2))
  print(json.dumps({'chosen':result['chosen'],'attempts':len(log)},indent=2)[:2400])
if __name__=='__main__':main()
