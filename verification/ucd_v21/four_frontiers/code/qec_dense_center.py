"""Dense-center control for CSS 108-stabilizer/24-gauge family; exact low-weight search."""
import numpy as np,json,sys
from pathlib import Path
from qec_144_subsystem import bb_matrices,rank_and_indices
from qec_search_sparse_center import canonical_gauge,min_dressed_to6

def mix_full(a,rng):
  b=a[rank_and_indices(a)[1]]
  for _ in range(100):
    mix=rng.integers(0,2,size=(66,66),dtype=np.uint8)
    if rank_and_indices(mix)[0]==66:return (mix@b)%2
  raise RuntimeError('not found invertible')

def main():
  out=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results');out.mkdir(parents=True,exist_ok=True)
  hx,hz=bb_matrices();log=[]
  for seed in range(900,925):
    rng=np.random.default_rng(seed);Hx=mix_full(hx,rng);Hz=mix_full(hz,rng)
    sx,sz,sa,ZA,XB,sb,GX,GZ=canonical_gauge(Hx,Hz,seed)
    xx=min_dressed_to6(sz,GX);zz=min_dressed_to6(sx,GZ)
    print(seed,'X',xx.get('weight','>=7'),'Z',zz.get('weight','>=7'),flush=True)
    rowweight={'X':np.sum(sx,axis=1).tolist(),'Z':np.sum(sz,axis=1).tolist()}
    log.append({'seed':seed,'X':xx,'Z':zz,'rowweight_mean_X':float(np.mean(rowweight['X'])),'rowweight_mean_Z':float(np.mean(rowweight['Z']))})
    if not xx['found'] and not zz['found']:
      np.savez_compressed(out/'Q72_144_dense_center_certified6.npz',HX_center=sx,HZ_center=sz,GA_X=sa,GA_Z=ZA,GB_X=XB,GB_Z=sb,GX_full=GX,GZ_full=GZ,HX_parent=hx,HZ_parent=hz)
      break
  result={'best_seed':log[-1]['seed'] if not log[-1]['X']['found'] and not log[-1]['Z']['found'] else None,'attempts':len(log),'complete_weight_6_search':len(log)>0 and not log[-1]['X']['found'] and not log[-1]['Z']['found'],'log':log}
  (out/'qec_dense_center_search.json').write_text(json.dumps(result,indent=2));print(json.dumps({'best_seed':result['best_seed'],'attempts':result['attempts']},indent=2))
if __name__=='__main__':main()
