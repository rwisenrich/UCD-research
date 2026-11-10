"""Select sparse rank-54 CSS center checks from a 144-qubit BB parent.
Exact meet-in-the-middle all dressed Pauli X/Z errors up to weight 6.
"""
import itertools,sys,json,time
from pathlib import Path
import numpy as np
from qec_144_subsystem import bb_matrices,rank_and_indices,right_inverse,basis_masks,in_span,list2mask

def canonical_gauge(hx,hz,seed):
    rng=np.random.default_rng(seed)
    ix=rng.permutation(len(hx));iz=rng.permutation(len(hz))
    _,qx=rank_and_indices(hx[ix]);_,qz=rank_and_indices(hz[iz]);HX=hx[ix[qx]];HZ=hz[iz[qz]]
    assert len(HX)==66 and len(HZ)==66
    sx,sa=HX[:54],HX[54:];sz,sb=HZ[:54],HZ[54:]
    ZA=right_inverse(HX)[:,54:66].T.copy();XB=right_inverse(HZ)[:,54:66].T.copy()
    XB^=((XB@ZA.T)%2@sa)%2
    GX=np.concatenate([sx,sa,XB]);GZ=np.concatenate([sz,ZA,sb])
    assert np.array_equal((sa@ZA.T)%2,np.eye(12,dtype=np.uint8))
    assert np.array_equal((XB@sb.T)%2,np.eye(12,dtype=np.uint8))
    assert not np.any((XB@ZA.T)%2)
    assert not np.any((sx@GZ.T)%2) and not np.any((sz@GX.T)%2)
    assert rank_and_indices(GX)[0]==78 and rank_and_indices(GZ)[0]==78
    return sx,sz,sa,ZA,XB,sb,GX,GZ

def min_dressed_to6(H,G):
    # H is opposite-type center stabilizers; a dressed X or Z error has H*e=0.
    cols=[list2mask(H[:,i]) for i in range(144)]
    gauge=basis_masks(G)
    seen={0:0};count=0;degenerate=0
    for w in (1,2,3):
        for idx in itertools.combinations(range(144),w):
            synd=0;mask=0
            for i in idx:synd^=cols[i];mask^=1<<i
            old=seen.get(synd)
            if old is not None:
                e=mask^old
                if e!=0:
                    ew=e.bit_count()
                    if not in_span(e,gauge):
                        return {'found':True,'weight':ew,'positions':[i for i in range(144) if (e>>i)&1],'examined_subsets':count,'syndrome_classes':len(seen)}
                    degenerate+=1
            else:seen[synd]=mask
            count+=1
    return {'found':False,'certified_lower_bound':7,'examined_subsets':count,'syndrome_classes':len(seen),'degenerate_collisions':degenerate}

def main():
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results';out.mkdir(parents=True,exist_ok=True)
    hx,hz=bb_matrices();log=[];best=None
    for seed in range(101,131):
        sx,sz,sa,ZA,XB,sb,GX,GZ=canonical_gauge(hx,hz,seed)
        zx=min_dressed_to6(sz,GX)
        zz=min_dressed_to6(sx,GZ)
        entry={'seed':seed,'X':zx,'Z':zz};log.append(entry)
        print('seed',seed,'X',zx.get('weight','>=7'),'Z',zz.get('weight','>=7'),flush=True)
        if not zx['found'] and not zz['found']:
            best=(seed,sx,sz,sa,ZA,XB,sb,GX,GZ)
            break
    if best:
        seed,sx,sz,sa,ZA,XB,sb,GX,GZ=best
        np.savez_compressed(out/'Q72_144_sparse_center_certified6.npz',HX_center=sx,HZ_center=sz,GA_X=sa,GA_Z=ZA,GB_X=XB,GB_Z=sb,GX_full=GX,GZ_full=GZ,HX_parent=hx,HZ_parent=hz)
    result={'search_attempts':len(log),'best_seed':best[0] if best else None,'complete_weight_6_dressed_error_search':bool(best),'log':log}
    (out/'qec_sparse_center_search.json').write_text(json.dumps(result,indent=2));print(json.dumps({'chosen_seed':result['best_seed'],'attempts':len(log)},indent=2))
if __name__=='__main__':main()
