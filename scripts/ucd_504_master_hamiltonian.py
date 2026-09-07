#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,math,os
from dataclasses import dataclass
from typing import Callable,Dict,List,Tuple
import numpy as np
GroupElement=Tuple[int,int]
TAU=1.0/72.0; EXP=math.exp(-TAU)
DEFAULT_COEFFICIENTS={'c1':1.0,'eta':0.50,'kappa':0.10,'gamma':0.10,'mu':1.10,'nu':0.10,'delta':0.30}
def E(n,i,j):
    M=np.zeros((n,n),dtype=complex);M[i,j]=1;return M
def dic6_mul(g,h):
    k,e=g;l,f=h;return ((k+((-1)**e)*l+6*e*f)%12,(e+f)%2)
ELEMS=[(k,e) for k in range(12) for e in range(2)]; IDX={g:i for i,g in enumerate(ELEMS)}
def dic6_inv(g):
    for h in ELEMS:
        if dic6_mul(g,h)==(0,0) and dic6_mul(h,g)==(0,0):return h
    raise ValueError(g)
def left_regular(g):
    L=np.zeros((24,24),dtype=complex)
    for j,h in enumerate(ELEMS):L[IDX[dic6_mul(g,h)],j]=1
    return L
def right_regular(g):
    R=np.zeros((24,24),dtype=complex);ig=dic6_inv(g)
    for j,h in enumerate(ELEMS):R[IDX[dic6_mul(h,ig)],j]=1
    return R
def one_dim_character(eps_a,eps_b):
    return lambda g:(eps_a**g[0])*(eps_b**g[1])
def two_dim_character(j):
    return lambda g:0.0 if g[1] else 2.0*math.cos(math.pi*j*g[0]/6.0)
@dataclass
class Irrep:
    kind:str;name:str;dim:int;chi:Callable[[GroupElement],complex]
def irreps():
    out=[]
    for ea in [1,-1]:
        for eb in [1,-1]:out.append(Irrep('1d',f'eps_a={ea},eps_b={eb}',1,one_dim_character(ea,eb)))
    for j in range(1,6):out.append(Irrep('2d',f'j={j}',2,two_dim_character(j)))
    return out
def isotypic_projector(ir):
    P=np.zeros((24,24),complex)
    for g in ELEMS:P+=np.conj(ir.chi(g))*right_regular(g)
    return (ir.dim/len(ELEMS))*P
def V7_ops():
    I7=np.eye(7,dtype=complex);Pc=E(7,0,0);R7=I7-Pc;A7=np.zeros((7,7),complex)
    for i in range(1,7):A7[0,i]=A7[i,0]=1
    Tp=np.zeros((7,7),complex);Tm=np.zeros((7,7),complex)
    for i in range(1,7):Tp[1+(i%6),i]=1;Tm[1+((i-2)%6),i]=1
    return {'I7':I7,'Pc':Pc,'R7':R7,'A7':A7,'Rring':Tp+Tm,'Tp':Tp,'Tm':Tm}
def F3_ops():
    I3=np.eye(3,dtype=complex);R=np.array([[0,1,0],[0,0,1],[1,0,0]],complex);XZ=R+R.conj().T;JZ=(R-R.conj().T)/(1j*math.sqrt(3.0));H=np.diag([-1,0,1]).astype(complex);H2=np.diag([1,0,1]).astype(complex);P0_minus_P2=E(3,0,0)-E(3,2,2)
    return {'I3':I3,'R':R,'XZ':XZ,'JZ':JZ,'H':H,'H2':H2,'P0_minus_P2':P0_minus_P2}
def kron3(A,B,C):return np.kron(np.kron(A,B),C)
@dataclass
class HamiltonianTerms:
    names:List[str];terms:List[np.ndarray]
def build_terms(rho_curr_mode='reflection'):
    v=V7_ops();f=F3_ops();I24=np.eye(24,complex) if False else np.eye(24,dtype=complex);La=left_regular((1,0));Lx=left_regular((0,1));La6=left_regular((6,0));rho_orient=.5*(La+La.conj().T)
    rho_curr=.5*(Lx+Lx.conj().T) if rho_curr_mode=='reflection' else (La-La.conj().T)/(2j)
    terms=[kron3(v['A7'],f['I3'],I24),kron3(v['I7'],f['XZ'],I24),kron3(v['Rring'],f['I3'],I24),kron3(v['A7'],f['I3'],La6),kron3(v['I7'],f['XZ'],rho_orient),kron3(v['I7'],f['JZ'],rho_curr),kron3(v['R7'],f['P0_minus_P2'],I24)]
    names=['T1_star','T2_family_XZ','T3_leaf_ring','T4_central_parity','T5_orientation_mix','T6_current','T7_leaf_family_selector'];return HamiltonianTerms(names,terms)
def build_H504(coeffs=None,rho_curr_mode='reflection'):
    c=DEFAULT_COEFFICIENTS.copy();c.update(coeffs or {});ht=build_terms(rho_curr_mode);sc=[c['c1'],c['eta'],c['kappa'],c['gamma'],c['mu'],c['nu'],c['delta']];H=np.zeros_like(ht.terms[0])
    for s,T in zip(sc,ht.terms):H+=s*T
    return EXP*H
def projector_basis(P,tol=1e-8):
    vals,vecs=np.linalg.eigh((P+P.conj().T)/2);return vecs[:,np.where(vals>1-tol)[0]]
def irrep_block(H,P24):
    U24=projector_basis(P24);B=np.kron(np.kron(np.eye(7),np.eye(3)),U24);return B.conj().T@H@B,B
def unique_clusters(evals,tol=1e-8):
    vals=sorted(float(x) for x in evals.real);clusters=[]
    for x in vals:
        if not clusters or abs(x-clusters[-1][0])>tol:clusters.append((x,1))
        else:
            old,n=clusters[-1];clusters[-1]=((old*n+x)/(n+1),n+1)
    return clusters
def closest_gap(clusters,target):
    gaps=[]
    for i in range(len(clusters)-1):
        gap=clusters[i+1][0]-clusters[i][0];gaps.append((i,gap,abs(gap-target),clusters[i][1],clusters[i+1][1],clusters[i][0],clusters[i+1][0]))
    return min(gaps,key=lambda row:row[2])
def direct_center_projection_blocks(H):
    e0=np.zeros((7,1),complex);e0[0,0]=1;I3=np.eye(3);blocks={}
    for ir in irreps():
        if ir.dim!=1:continue
        U24=projector_basis(isotypic_projector(ir));B=np.kron(np.kron(e0,I3),U24);blocks[ir.name]=B.conj().T@H@B
    return blocks
def schur_center_blocks(H,z=0.0):
    e0=np.zeros((7,1),complex);e0[0,0]=1;leaf=np.zeros((7,6),complex)
    for i in range(6):leaf[i+1,i]=1
    I3=np.eye(3);blocks={}
    for ir in irreps():
        if ir.dim!=1:continue
        U24=projector_basis(isotypic_projector(ir));Bc=np.kron(np.kron(e0,I3),U24);Bl=np.kron(np.kron(leaf,I3),U24);Hcc=Bc.conj().T@H@Bc;Hcl=Bc.conj().T@H@Bl;Hlc=Bl.conj().T@H@Bc;Hll=Bl.conj().T@H@Bl;blocks[ir.name]=Hcc-Hcl@np.linalg.pinv(Hll-z*np.eye(Hll.shape[0]))@Hlc
    return blocks
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='results/h504_master');p.add_argument('--rho-curr-mode',default='reflection',choices=['reflection','rotation_sine']);a=p.parse_args();os.makedirs(a.out,exist_ok=True);H=build_H504(rho_curr_mode=a.rho_curr_mode);summary={'dimension':504,'tau':TAU,'exp_minus_tau':EXP,'hermiticity_residual':float(np.linalg.norm(H-H.conj().T))};open(os.path.join(a.out,'h504_master_summary.json'),'w').write(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
