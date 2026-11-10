"""N_t=8 Kelvin/BCC SU(3) scalar/tensor 3+8+6+H504 character spectroscopy.
Direct Monte Carlo, full non-Abelian link variables; H504 channel uses exact
v17 seven-term bright Schur eigenvalues and a numerically stable nonlinear remainder.
"""
from pathlib import Path
import argparse,json,time
import numpy as np
from numba import njit
from kelvin import geometry
from glueball_nt8 import sweep_beta,block_bootstrap,analyze

@njit

def observe_multi(U,faces,spatial,times,normal,nt,eig):
    ns=4*3
    out=np.zeros((nt,ns),dtype=np.float64);counts=np.zeros(nt)
    s2=np.dot(eig,eig);eta=.0001
    for p in range(faces.shape[0]):
        if not spatial[p]:continue
        a,b,c,d=faces[p]
        v=U[a]@U[b]@U[c].conj().T@U[d].conj().T
        tr=v[0,0]+v[1,1]+v[2,2]
        tr3=tr.real/3
        adj=(tr.real**2+tr.imag**2-1)/8
        six=((tr*tr-tr.conjugate()).real)/6
        fr=1-tr3
        r=0.0
        for wi in eig:
            u=eta*fr*wi
            r+=u-np.log1p(u)
        cell=r/(.5*eta*eta*s2)
        features=np.array([tr3,adj,six,cell])
        n=normal[p];eA=n[2]**2-.5*(n[0]**2+n[1]**2);eB=n[0]**2-n[1]**2
        t=times[p];counts[t]+=1.
        for j in range(4):
            out[t,j*3]+=features[j]
            out[t,j*3+1]+=features[j]*eA
            out[t,j*3+2]+=features[j]*eB
    for t in range(nt):out[t]/=counts[t]
    return out

def scalar_corr(data):
    # scalar/time average and cross spatial/time, centered over configurations and source times
    x=data-np.mean(data)
    return [float(np.mean(x*np.roll(x,-tau,axis=1))) for tau in range(x.shape[1]//2+1)]

def mass_estimate(c):
    if c[1]>0 and (c[0]+c[2])/(2*c[1])>=1:
        return float(np.arccosh((c[0]+c[2])/(2*c[1])))
    return None

def analyze_multi(arr,seed):
    names=['fundamental_3','adjoint_8','sextet_6','H504_nonlinear']
    rng=np.random.default_rng(seed);output={}
    for j,name in enumerate(names):
        rows={}
        for k,label in enumerate(['0pp','E2a','E2b']):
            x=arr[:,:,j*3+k];c=scalar_corr(x)
            # Four-measurement block bootstrap.
            blocks=np.array_split(np.arange(len(x)),max(2,len(x)//4));ms=[]
            for _ in range(200):
                inds=rng.integers(0,len(blocks),size=len(blocks))
                xs=np.concatenate([x[blocks[i]] for i in inds],axis=0)[:len(x)]
                mass=mass_estimate(scalar_corr(xs))
                if mass is not None:ms.append(mass)
            rows[label]={'C':c,'m_eff_tau1':mass_estimate(c),'bootstrap_valid_fraction':len(ms)/200,'bootstrap_16_84':np.quantile(ms,[.16,.84]).tolist() if len(ms)>20 else None}
        output[name]=rows
    return output

def su3_rand(rng):
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));q,r=np.linalg.qr(z)
    q=q@np.diag(np.diag(r)/abs(np.diag(r)));q[:,0]/=np.linalg.det(q)
    return q

def main():
    p=argparse.ArgumentParser();p.add_argument('--beta',type=float,default=16.);p.add_argument('--warm',type=int,default=300);p.add_argument('--measure',type=int,default=80);p.add_argument('--stride',type=int,default=3);p.add_argument('--angle',type=float,default=.35);p.add_argument('--seed',type=int,default=13016);p.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1]/'results');args=p.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    g=geometry(3,8);rg=np.random.default_rng(args.seed);U=np.array([su3_rand(rg) for _ in range(g['n_links'])]);eig=np.load(Path(__file__).resolve().parents[1]/'results/h504_W_eigenvalues.npy')
    raw=[];acc=[];t0=time.time()
    for step in range(args.warm+args.measure*args.stride):
        acceptance=sweep_beta(U,g['pla'],g['pw'],g['adj'],args.angle,args.beta,args.seed+step)
        if step>=args.warm and (step-args.warm)%args.stride==0:
            acc.append(acceptance);raw.append(observe_multi(U,g['pla'],g['spatial'],g['times'],g['normal'],g['Nt'],eig))
    arr=np.array(raw);results=analyze_multi(arr,args.seed)
    tag=f'multi_beta{int(args.beta*10)}_L3_Nt8'
    np.savez_compressed(args.out/f'{tag}_raw.npz',operator_timelines=arr)
    d={'setup':dict(vars(args)),'geometry':{k:g[k] for k in ['Nt','L','n_sites','n_links','n_plaquettes']},'H504_W_s1':float(eig.sum()),'H504_W_s2':float(eig@eig),'mean_acceptance':float(np.mean(acc)),'elapsed_seconds':time.time()-t0,'channels':results}
    d['setup']['out']=str(d['setup']['out'])
    (args.out/f'{tag}.json').write_text(json.dumps(d,indent=2))
    print(json.dumps({'tag':tag,'elapsed':d['elapsed_seconds'],'acceptance':d['mean_acceptance'],'scalar_masses':{name:c['0pp']['m_eff_tau1'] for name,c in results.items()}},indent=2))
if __name__=='__main__':main()
