#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,sys,csv,json,math
from pathlib import Path
import numpy as np
from scipy import sparse
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
spec=importlib.util.spec_from_file_location('h504',str(Path(__file__).with_name('ucd_504_master_hamiltonian.py')))
h=importlib.util.module_from_spec(spec);sys.modules['h504']=h;spec.loader.exec_module(h)
def fro(A): return float(np.linalg.norm(A,'fro'))
def wcsv(name,rows):
    with open(RES/name,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
v=h.V7_ops(); r0=np.zeros(7,complex);r0[1:]=1/math.sqrt(6)
P2=v['Pc']+np.outer(r0,r0.conj()); P144=np.kron(np.kron(P2,np.eye(3)),np.eye(24));P360=np.eye(504)-P144
P84_24=sum(h.right_regular((2*r,0)) for r in range(6))/6
P84=np.kron(np.kron(np.eye(7),np.eye(3)),P84_24);P420=np.eye(504)-P84
cross={'24':P144@P84,'120':P144@P420,'60':P360@P84,'300':P360@P420}
ht=h.build_terms('reflection')
ref={'rank144':int(round(np.trace(P144).real)),'rank360':int(round(np.trace(P360).real)),'rank84':int(round(np.trace(P84).real)),'rank420':int(round(np.trace(P420).real)),'projector_commutator':fro(P144@P84-P84@P144),'cross_ranks':{k:int(round(np.trace(P).real)) for k,P in cross.items()},'max_term_comm_P144':max(fro(T@P144-P144@T) for T in ht.terms),'max_term_comm_P84':max(fro(T@P84-P84@T) for T in ht.terms)}
q6=6;omega=np.exp(2j*np.pi/q6)
S6=np.zeros((q6,q6),complex)
for j in range(q6):S6[(j+1)%q6,j]=1
Z6=np.diag([omega**j for j in range(q6)])
F6=np.array([[omega**(j*k)/np.sqrt(q6) for k in range(q6)] for j in range(q6)],complex)
U5=F6[:,1:]; X5=U5.conj().T@S6@U5; Z5=U5.conj().T@Z6@U5
A=(X5+X5.conj().T)/2;B=(X5-X5.conj().T)/(2j);C=(Z5+Z5.conj().T)/2;D=(Z5-Z5.conj().T)/(2j);E=1j*(A@C-C@A);E=(E+E.conj().T)/2
ops=[A,B,C,D,E]
basis=[np.eye(5,dtype=complex)]
def add(M):
    v=M.reshape(-1);Q=np.column_stack([x.reshape(-1) for x in basis]);r=np.linalg.matrix_rank(Q,1e-10);r2=np.linalg.matrix_rank(np.column_stack([Q,v]),1e-10)
    if r2>r:basis.append(M);return True
    return False
for O in ops:add(O)
chg=True
while chg and len(basis)<25:
    chg=False
    old=list(basis)
    for P in old:
        for O in ops:
            if add(P@O):chg=True
            if len(basis)>=25:break
        if len(basis)>=25:break
Mcomm=np.vstack([np.kron(O.T,np.eye(5))-np.kron(np.eye(5),O) for O in ops]); s=np.linalg.svd(Mcomm,compute_uv=False); commdim=25-int(np.sum(s>1e-10))
I5=sparse.identity(5,format='csr',dtype=complex);ops_sp=[sparse.csr_matrix(o) for o in ops];tau=1/72
def emb1(op,i,N):
    out=None
    for k in range(N):
        f=op if k==i else I5; out=f if out is None else sparse.kron(out,f,format='csr')
    return out
def emb2(op1,i,op2,j,N):
    out=None
    for k in range(N):
        f=op1 if k==i else op2 if k==j else I5;out=f if out is None else sparse.kron(out,f,format='csr')
    return out
def HN(N):
    H=sparse.csr_matrix((5**N,5**N),dtype=complex);addrs=[]
    for i in range(N):
        qi=(7*i+3)%72;addrs.append(qi);th=2*np.pi*qi/72;cc=[np.cos(th),np.sin(th),np.cos(2*th),np.sin(2*th),np.cos(3*th)]
        for c,o in zip(cc,ops_sp):H+=c*emb1(o,i,N)
    for i in range(N-1):
        H+=emb2(ops_sp[0],i,ops_sp[0],i+1,N)+emb2(ops_sp[2],i,ops_sp[2],i+1,N)
        H+=tau*(emb2(ops_sp[1],i,ops_sp[3],i+1,N)+emb2(ops_sp[4],i,ops_sp[0],i+1,N))
    for i in range(N-2):H+=tau*tau*emb2(ops_sp[2],i,ops_sp[4],i+2,N)
    return (H+H.getH())*.5,addrs
def gapratio(vals):
    vals=np.sort(vals.real);g=np.diff(vals);g=g[int(.1*len(g)):int(.9*len(g))];den=np.maximum(g[:-1],g[1:]);m=den>1e-11;return float(np.mean(np.minimum(g[:-1],g[1:])[m]/den[m]))
rows=[]; cache={}
for N in [2,3,4]:
    Hs,ad=HN(N);Hd=Hs.toarray();vals,V=eigh(Hd,check_finite=False);cache[N]=(vals,V,Hd);d=len(vals);O=emb1(ops_sp[0],0,N).toarray();diag=np.real(np.diag(V.conj().T@O@V));cen=diag[d//4:3*d//4];probs=np.abs(V[:,d//4:3*d//4])**2;sh=-np.sum(np.where(probs>1e-300,probs*np.log(probs),0),axis=0)
    rows.append({'N_cells':N,'dim':d,'addresses':';'.join(map(str,ad)),'mean_gap_ratio':gapratio(vals),'ETH_central_diag_std':float(np.std(cen)),'Shannon_over_logdim':float(np.mean(sh)/np.log(d))})
wcsv('16_manybody_sector_mixing_stats.csv',rows)
vals,V,Hd=cache[3];d=len(vals);O0=emb1(ops_sp[0],0,3).toarray();O2=emb1(ops_sp[2],2,3).toarray();Oe=V.conj().T@O0@V;ot=[]
for t in np.linspace(0,8,17):
    ph=np.exp(1j*vals*t);Ot=V@(ph[:,None]*Oe*ph.conj()[None,:])@V.conj().T;K=Ot@O2-O2@Ot;ot.append({'t':float(t),'comm_fro_sq_per_dim':float(np.linalg.norm(K,'fro')**2/d)})
wcsv('17_otoc_N3.csv',ot)
summary={'common_refinement':ref,'local_detail_algebra_dimension':len(basis),'local_detail_commutant_dimension':commdim,'tensor_algebra_statement':'Because Alg{A,B,C,D,E}=M5(C), the independent local copies generate tensor_a M5(C)=M_{5^N}(C) on N detail fibers.','finite_stats':rows,'otoc_final':ot[-1]}
(RES/'18_manybody_hnet_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
