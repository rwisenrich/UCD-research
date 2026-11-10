"""Canonical seven-positive-direction Kelvin/BCC complex in doubled integer coordinates."""
from fractions import Fraction
from itertools import product
import numpy as np

V=np.array([[2,0,0],[0,2,0],[0,0,2],[1,1,1],[1,1,-1],[1,-1,1],[-1,1,1]],dtype=np.int32)
W=[Fraction(1,6)]*3+[Fraction(1,3)]*4
DISP=np.vstack([np.array([[1,0,0,0]],dtype=np.int32),np.column_stack([np.zeros(7,dtype=np.int32),V])])
WV=np.array([1.0]+[float(x) for x in W])
WEIGHTS={(r,s): (W[s-1] if r==0 else 2*W[r-1]*W[s-1]) for r in range(8) for s in range(r+1,8)}

def geometry(L=3,Nt=8):
    assert L>=3 and Nt>=4
    site_list=[(t,x,y,z) for t in range(Nt) for x,y,z in product(range(2*L),repeat=3) if x%2==y%2==z%2]
    sites=np.array(site_list,dtype=np.int32); idx={tuple(v):i for i,v in enumerate(site_list)}
    period=np.array([Nt,2*L,2*L,2*L],dtype=np.int32)
    plus=np.array([[idx[tuple((x+v)%period)] for v in DISP] for x in sites],dtype=np.int32)
    neg=np.empty_like(plus)
    for x in range(len(sites)):
        for r in range(8):neg[plus[x,r],r]=x
    pla=[]; weights=[]; times=[]; normals=[]; types=[]
    for x in range(len(sites)):
        for r in range(8):
            for s in range(r+1,8):
                # Four ordered edges: U(x,r) U(x+r,s) U(x+s,r)^dagger U(x,s)^dagger
                pla.append([8*x+r,8*plus[x,r]+s,8*plus[x,s]+r,8*x+s])
                weights.append(float(WEIGHTS[(r,s)]));times.append(int(sites[x,0]));types.append(int(r==0))
                if r>0:
                    vi=V[r-1]/2.;vj=V[s-1]/2.;n=np.cross(vi,vj);normals.append(n/np.linalg.norm(n))
                else:normals.append(np.array([0.,0.,0.]))
    plaq=np.array(pla,dtype=np.int32);pw=np.array(weights,dtype=np.float64)
    adj_idx=[[] for _ in range(8*len(sites))]
    for p,row in enumerate(plaq):
        for e in row:adj_idx[e].append(p)
    assert max(map(len,adj_idx)) <= 24
    maxd=max(map(len,adj_idx));adj=np.full((len(adj_idx),maxd),-1,dtype=np.int32)
    for i,rr in enumerate(adj_idx):adj[i,:len(rr)]=rr
    return {"sites":sites,"plus":plus,"minus":neg,"pla":plaq,"pw":pw,
            "times":np.array(times,dtype=np.int32),"spatial":np.array(types,dtype=np.int32)==0,
            "normal":np.array(normals),"adj":adj,"Nt":Nt,"L":L,
            "n_sites":len(sites),"n_links":8*len(sites),"n_plaquettes":len(pla)}

if __name__=='__main__':
    g=geometry();print({k:g[k] for k in ['Nt','L','n_sites','n_links','n_plaquettes']})
