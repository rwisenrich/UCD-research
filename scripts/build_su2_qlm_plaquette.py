#!/usr/bin/env python3
from pathlib import Path
import csv, json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'; D=5
def M(a,b):
    X=np.zeros((D,D),complex); X[a,b]=-1j; X[b,a]=1j; return X
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]],complex); sz=np.array([[1,0],[0,-1]],complex)
sig=[sx,sy,sz]; lam=[s/2 for s in sig]
A=[M(1,2),M(2,0),M(0,1)]; B=[M(0,3),M(1,3),M(2,3)]
L=[0.5*(A[i]+B[i]) for i in range(3)]; R=[0.5*(A[i]-B[i]) for i in range(3)]
q=[M(mu,4) for mu in range(4)]; U=[[None]*2 for _ in range(2)]
for a in range(2):
    for b in range(2):
        X=q[3]*(1 if a==b else 0)
        for i in range(3): X += 1j*q[i]*sig[i][a,b]
        U[a][b]=X
def fro(A): return float(np.linalg.norm(A,'fro'))
def comm(A,B): return A@B-B@A
algL=max(fro(comm(L[i],U[a][b]) + sum(lam[i][a,c]*U[c][b] for c in range(2))) for i in range(3) for a in range(2) for b in range(2))
algR=max(fro(comm(R[i],U[a][b]) - sum(U[a][c]*lam[i][c,b] for c in range(2))) for i in range(3) for a in range(2) for b in range(2))
I=np.eye(D,dtype=complex)
def kron4(ops): return np.kron(np.kron(np.kron(ops[0],ops[1]),ops[2]),ops[3])
def emb(op,e):
    ops=[I,I,I,I]; ops[e]=op; return kron4(ops)
Le=[[emb(L[a],e) for a in range(3)] for e in range(4)]; Re=[[emb(R[a],e) for a in range(3)] for e in range(4)]
G=[[] for _ in range(4)]
for a in range(3):
    G[0].append(Le[0][a]+Le[3][a]); G[1].append(Le[1][a]+Re[0][a]); G[2].append(Re[1][a]+Re[2][a]); G[3].append(Le[2][a]+Re[3][a])
Bp=np.zeros((D**4,D**4),complex)
for i in range(2):
 for j in range(2):
  for k in range(2):
   for l in range(2):
    Bp += kron4([U[i][j],U[j][k],U[l][k].conj().T,U[i][l].conj().T])
Bherm=Bp+Bp.conj().T
Eloc=sum(x@x for x in L)+sum(x@x for x in R); E=sum(emb(Eloc,e) for e in range(4))
gauge_B=max(fro(comm(Bherm,g)) for vv in G for g in vv); gauge_E=max(fro(comm(E,g)) for vv in G for g in vv)
G2=sum(g@g for vv in G for g in vv); gv,GV=np.linalg.eigh(G2); mask=gv<1e-9; P=GV[:,mask]
Er=P.conj().T@E@P; Br=P.conj().T@Bherm@P
scan=[]
for e in [0.4,0.5,0.75,1.0,1.25,1.5,2.0,3.0]:
    Hr=e*e*Er-(1/(4*e*e))*Br; he=np.linalg.eigvalsh(Hr)
    scan.append({'e':e,'ground_energy':float(he[0]),'first_excited':float(he[1]),'finite_plaquette_gap':float(he[1]-he[0]),'ground_multiplicity':int(np.sum(abs(he-he[0])<1e-10))})
with open(RES/'K_su2_qlm_one_plaquette_gap_scan.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(scan[0]));w.writeheader();w.writerows(scan)
summary={'construction':'SO(5) 5-vector SU(2) quantum-link scaffold, 4 links on one square plaquette','single_link_dimension':5,'four_link_dimension':625,'local_commutators':{'L_U_covariance_residual':algL,'R_U_covariance_residual':algR},'plaquette':{'magnetic_Gauss_commutator_max':gauge_B,'electric_Gauss_commutator_max':gauge_E},'gauss_law':{'physical_subspace_dimension':int(mask.sum())},'restricted_electric_eigenvalues':[float(x) for x in np.linalg.eigvalsh(Er)],'restricted_magnetic_matrix_frobenius_norm':fro(Br)}
(RES/'K_su2_qlm_one_plaquette.json').write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))
