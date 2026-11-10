"""Direct N_t=8 SU(3) Metropolis simulation on the 28-face Kelvin/BCC torus.

Exact 4-link Wilson plaquette geometry and the v11 anisotropic plaquette weights;
raw time-slice operators and bootstrap diagnostic correlators are exported.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from numba import njit
from kelvin import geometry

@njit

def trace_plaq(U,face):
    a,b,c,d=face
    # U_a U_b U_c^dagger U_d^dagger
    v=U[a]@U[b]@U[c].conj().T@U[d].conj().T
    return (v[0,0].real+v[1,1].real+v[2,2].real)/3.0

@njit

def apply_su2_left(U,e,i,j,x,y,z,w):
    # SU(2) block [[a,b],[-b*,a*]], where a=w+i*x, b=y+i*z.
    ui=U[e,i].copy();uj=U[e,j].copy()
    a=w+1j*x; b=y+1j*z
    U[e,i]=a*ui+b*uj
    U[e,j]=-np.conj(b)*ui+np.conj(a)*uj

@njit

def metropolis(U,faces,pw,adj,angle,seed):
    np.random.seed(seed)
    accepted=0;total=0
    for e in range(U.shape[0]):
        i=np.random.randint(0,3);j=(i+1+np.random.randint(0,2))%3
        p=np.array([np.random.normal(),np.random.normal(),np.random.normal()])
        mag=np.sqrt(p[0]**2+p[1]**2+p[2]**2)
        x,y,z=np.sin(angle)/mag*p
        w=np.cos(angle)
        old=0.0
        for a in range(adj.shape[1]):
            idx=adj[e,a]
            if idx<0:break
            old+=pw[idx]*trace_plaq(U,faces[idx])
        apply_su2_left(U,e,i,j,x,y,z,w)
        new=0.0
        for a in range(adj.shape[1]):
            idx=adj[e,a]
            if idx<0:break
            new+=pw[idx]*trace_plaq(U,faces[idx])
        if np.log(max(1e-300,np.random.random())) < (new-old):
            accepted+=1
        else:
            apply_su2_left(U,e,i,j,-x,-y,-z,w)
        total+=1
    return accepted/total

@njit

def sweep_beta(U,faces,pw,adj,angle,beta,seed):
    return metropolis(U,faces,pw*beta,adj,angle,seed)

@njit

def observe(U,faces,spatial,times,normal,Nt):
    scalar=np.zeros(Nt);E0=np.zeros(Nt);E1=np.zeros(Nt);cnt=np.zeros(Nt)
    for i in range(faces.shape[0]):
        if not spatial[i]:continue
        p=trace_plaq(U,faces[i]);t=times[i];n=normal[i]
        scalar[t]+=p
        E0[t]+=p*(n[2]**2-0.5*(n[0]**2+n[1]**2))
        E1[t]+=p*(n[0]**2-n[1]**2)
        cnt[t]+=1
    return scalar/cnt,E0/cnt,E1/cnt

def corr(data):
    # Correlation relative to ensemble average, over all periodic source times.
    c=np.array(data,dtype=float);c-=c.mean(axis=(0,1),keepdims=True)
    return np.array([np.mean(c*np.roll(c,-dt,axis=1),axis=(0,1)) for dt in range(c.shape[1]//2+1)])

def block_bootstrap(a,nboot,seed=20261110):
    rng=np.random.default_rng(seed);n=len(a)
    if n<10:return None
    # Block bootstrap of measurement history, 4 sweeps per block. Preserve sector correlations.
    blocks=np.array_split(np.arange(n),max(2,n//4))
    out=[]
    for _ in range(nboot):
        ids=rng.integers(0,len(blocks),size=len(blocks))
        arr=np.concatenate([a[blocks[j]] for j in ids],axis=0)[:n]
        out.append([corr(arr[:,:,j]) for j in range(a.shape[2])])
    return np.array(out)

def analyze(raw,boot):
    vals={}
    for j,name in enumerate(['0++','E2a','E2b']):
        c=corr(raw[:,:,j]);d={'C':c.tolist()}
        def meff(C,dt=1):
            if len(C)>dt+1 and C[dt]>0 and C[dt-1]+C[dt+1]>=2*C[dt]:
                return float(np.arccosh((C[dt-1]+C[dt+1])/(2*C[dt])))
            return None
        d['effective_mass_tau1']=meff(c)
        if boot is not None:
            bs=np.array([meff(cj) for cj in boot[:,j]],dtype=object)
            ok=np.array([x for x in bs if x is not None],dtype=float)
            d['bootstrap_valid_fraction']=float(len(ok)/len(bs))
            d['bootstrap_16_84']=np.quantile(ok,[.16,.84]).tolist() if len(ok)>10 else None
        vals[name]=d
    return vals

def main():
    p=argparse.ArgumentParser();p.add_argument('--beta',type=float,default=16.);p.add_argument('--L',type=int,default=3);p.add_argument('--nt',type=int,default=8);p.add_argument('--warm',type=int,default=30);p.add_argument('--measure',type=int,default=96);p.add_argument('--stride',type=int,default=3);p.add_argument('--angle',type=float,default=.18);p.add_argument('--seed',type=int,default=264816);p.add_argument('--hot',action='store_true');p.add_argument('--out',type=Path,default=Path('results'));args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    geom=geometry(args.L,args.nt)
    n=geom['n_links'];U=np.repeat(np.eye(3,dtype=np.complex128)[None,:,:],n,axis=0)
    if args.hot:
        rg=np.random.default_rng(args.seed)
        for e in range(n):
            z=rg.normal(size=(3,3))+1j*rg.normal(size=(3,3))
            q,rv=np.linalg.qr(z);q=q@np.diag(np.diag(rv)/np.abs(np.diag(rv)))
            q[:,0]/=np.linalg.det(q)
            U[e]=q
    kw={x:geom[x] for x in ('pla','pw','adj')}
    tr=time.time();a=[];acc=[];s=args.seed
    for step in range(args.warm+args.measure*args.stride):
        acceptance=sweep_beta(U,kw['pla'],kw['pw'],kw['adj'],args.angle,args.beta,s+step)
        if step>=args.warm and (step-args.warm)%args.stride==0:
            acc.append(acceptance);a.append(observe(U,geom['pla'],geom['spatial'],geom['times'],geom['normal'],args.nt))
    raw=np.array(a).transpose(0,2,1);boot=block_bootstrap(raw,150)
    results=analyze(raw,boot)
    data={'setup':{k:getattr(args,k) for k in ('beta','L','nt','warm','measure','stride','angle','seed','hot')},'geometry':{k:geom[k] for k in ('n_sites','n_links','n_plaquettes')},'acceptance':float(np.mean(acc)),'time_seconds':time.time()-tr,'channels':results}
    tag=f'beta{int(args.beta*10):03d}_L{args.L}_Nt{args.nt}'
    np.savez_compressed(args.out/f'glueball_{tag}_raw.npz',operator_timelines=raw,seed=args.seed)
    (args.out/f'glueball_{tag}.json').write_text(json.dumps(data,indent=2))
    print(json.dumps({'tag':tag,'acceptance':data['acceptance'],'secs':data['time_seconds'],'masses':{k:v['effective_mass_tau1'] for k,v in results.items()},'raw_records':len(raw)},indent=2))
if __name__=='__main__': main()
