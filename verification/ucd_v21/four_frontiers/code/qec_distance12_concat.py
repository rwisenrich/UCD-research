"""Exact Dic6/Z3 group-CSS distance-four to distance-twelve concatenation.

Outer: native [[144,36,4]] CSS, A=1+L(a^3), B=A*(R(g1)+R(g2)+R(g3));
Inner: [[9,1,3]] Shor CSS. Result: [[1296,36,12]] CSS.
"""
import itertools,json,sys
from pathlib import Path
import numpy as np
from qec_144_subsystem import list2mask,basis_masks,in_span,rank_and_indices

def rank_bitrows(a):
    b={}
    for row in a:
        x=list2mask(row)
        while x:
            p=x.bit_length()-1
            if p not in b:b[p]=x;break
            x^=b[p]
    return len(b)

def check_distance4(H,G,witness):
    # Complete enumeration of weights 1,2,3, no Monte Carlo search.
    cols=[list2mask(H[:,j]) for j in range(144)];b=basis_masks(G)
    tested=0
    for w in (1,2,3):
        for idx in itertools.combinations(range(144),w):
            tested+=1;synd=0
            for i in idx:synd^=cols[i]
            if synd==0:
                m=sum(1<<i for i in idx)
                assert in_span(m,b),('logical below 4',idx)
    assert len(witness)==4
    mask=sum(1<<i for i in witness);synd=0
    for i in witness:synd^=cols[i]
    assert synd==0 and not in_span(mask,b)
    return tested

def inner_code():
    Hx=np.zeros((2,9),np.uint8);Hz=np.zeros((6,9),np.uint8)
    Hx[0,0:6]=1;Hx[1,3:9]=1
    for block in range(3):Hz[2*block,3*block:3*block+2]=1;Hz[2*block+1,3*block+1:3*block+3]=1
    LxZ=np.zeros(9,np.uint8);LxZ[[0,3,6]]=1
    LzX=np.zeros(9,np.uint8);LzX[[0,1,2]]=1
    assert (Hx@Hz.T%2==0).all()
    assert (Hx@LxZ%2==0).all() and (Hz@LzX%2==0).all()
    assert int(LxZ@LzX)%2==1
    assert (rank_bitrows(Hx),rank_bitrows(Hz))==(2,6)
    return Hx,Hz,LxZ,LzX

def concat(outerHx,outerHz):
    # Use linearly independent outer stabilizer rows.
    _,ix=rank_and_indices(outerHx);_,iz=rank_and_indices(outerHz)
    HXo=outerHx[ix];HZo=outerHz[iz]
    assert len(HXo)==len(HZo)==54
    ix,iz,LxZ,LzX=inner_code()
    N=144*9
    # X stabilizers: 2 inner X per block and 54 outer Z represented by inner logical Z (physical X).
    Hx=np.zeros((144*2+54,N),np.uint8)
    Hz=np.zeros((144*6+54,N),np.uint8)
    for block in range(144):
        Hx[2*block:2*block+2,9*block:9*(block+1)]=ix
        Hz[6*block:6*block+6,9*block:9*(block+1)]=iz
    for i in range(54):
        for j in np.flatnonzero(HZo[i]):Hx[144*2+i,9*j:9*j+9]=LzX
        for j in np.flatnonzero(HXo[i]):Hz[144*6+i,9*j:9*j+9]=LxZ
    return Hx,Hz,LxZ,LzX

def main():
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[1]/'results';dest.mkdir(parents=True,exist_ok=True)
    outer=np.load(dest/'Q72_native_CSS_144_optimized.npz');ox=outer['HX'];oz=outer['HZ'];assert not np.any(ox@oz.T%2)
    Xw=[0,6,12,18];Zw=[0,5,62,114]
    nx=check_distance4(oz,ox,Xw);nz=check_distance4(ox,oz,Zw)
    HX,HZ,XLZ,ZLX=concat(ox,oz)
    n=HX.shape[1]
    # Full exact CSS orthogonality, calculated as packed integer dot parities.
    zrows=[list2mask(row) for row in HZ]; xrows=[list2mask(row) for row in HX]
    assert all(((x&z).bit_count()%2)==0 for x in xrows for z in zrows)
    rX=rank_bitrows(HX);rZ=rank_bitrows(HZ)
    assert (rX,rZ,n-rX-rZ)==(342,918,36)
    # Lift outer X witness to physical Z, and outer Z witness to physical X.
    physZ=np.zeros(n,np.uint8);physX=np.zeros(n,np.uint8)
    for j in Xw:physZ[9*j:9*j+9]=XLZ
    for j in Zw:physX[9*j:9*j+9]=ZLX
    assert np.count_nonzero(physZ)==np.count_nonzero(physX)==12
    assert all((x&list2mask(physZ)).bit_count()%2==0 for x in xrows)
    assert all((z&list2mask(physX)).bit_count()%2==0 for z in zrows)
    assert not in_span(list2mask(physZ),basis_masks(HZ))
    assert not in_span(list2mask(physX),basis_masks(HX))
    # Standard concatenation theorem: d >= d_outer*d_inner = 4*3; witnesses show d <=12.
    # Full check matrices retained as portable compressed arrays.
    np.savez_compressed(dest/'Q72_Dic6_CSS_1296_36_12.npz',HX=HX,HZ=HZ,outer_HX=ox,outer_HZ=oz,X_logical_witness=physX,Z_logical_witness=physZ,inner_Xchecks=inner_code()[0],inner_Zchecks=inner_code()[1])
    result={'construction':'native Z3 x Dic6 CSS [[144,36,4]] concatenated with 9-qubit Shor CSS [[9,1,3]]',
            'outer':{'n':144,'k':36,'d':4,'HX_rank':54,'HZ_rank':54,'complete_search_X_weight_lt4':nx,'complete_search_Z_weight_lt4':nz,'X_witness':Xw,'Z_witness':Zw},
            'inner':{'n':9,'k':1,'d':3},
            'concatenated':{'n':n,'k':n-rX-rZ,'d_lower_from_product':12,'d_upper_from_witness':12,'HX_rank':rX,'HZ_rank':rZ,'HX_rows':len(HX),'HZ_rows':len(HZ),'orthogonal':True,'logical_witness_X_weight':int(np.sum(physX)),'logical_witness_Z_weight':int(np.sum(physZ)),'logical_witness_X_indices':np.flatnonzero(physX).tolist(),'logical_witness_Z_indices':np.flatnonzero(physZ).tolist()}}
    (dest/'qec_distance12_concatenated.json').write_text(json.dumps(result,indent=2));print(json.dumps({'outer':result['outer'],'inner':result['inner'],'concatenated':{k:v for k,v in result['concatenated'].items() if 'indices' not in k}},indent=2))
if __name__=='__main__':main()
