#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, sys, csv, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'; RES.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('h504', str(Path(__file__).with_name('ucd_504_master_hamiltonian.py')))
h=importlib.util.module_from_spec(spec); sys.modules['h504']=h; spec.loader.exec_module(h)
ht=h.build_terms('reflection'); T=ht.terms; names=ht.names
n=504
G=np.array([[np.trace(A.conj().T@B).real/n for B in T] for A in T])
rows=[]
for i,name in enumerate(names):
    rows.append({'term':name,'G_diag':G[i,i],**{f'G_{j+1}':G[i,j] for j in range(7)}})
with open(RES/'11_parent_gram_matrix.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader();w.writerows(rows)
K=(T[0]@T[1]+T[1]@T[0])/2 + 0.37*T[2]@T[2] + 0.11j*(T[4]@T[5]-T[5]@T[4])
K=(K+K.conj().T)/2
J=np.array([np.trace(A.conj().T@K).real/n for A in T])
c=np.linalg.solve(G,J)
P=sum(c[i]*T[i] for i in range(7))
R=K-P
orth=np.array([np.trace(A.conj().T@R)/n for A in T])
s=np.array([2.0,0.5,3.0,1.25,0.8,4.0,1.7]); S=np.diag(s)
Tp=[s[i]*T[i] for i in range(7)]
Gp=np.array([[np.trace(A.conj().T@B).real/n for B in Tp] for A in Tp])
Jp=np.array([np.trace(A.conj().T@K).real/n for A in Tp])
cp=np.linalg.solve(Gp,Jp)
Pp=sum(cp[i]*Tp[i] for i in range(7))
I7=np.eye(7,dtype=complex); I3=np.eye(3,dtype=complex); I24=np.eye(24,dtype=complex)
Sx=sum(h.right_regular((k,1)) for k in range(12))/12
Sx504=np.kron(np.kron(I7,I3),Sx)
JZ=h.F3_ops()['JZ']; JZ504=np.kron(np.kron(I7,JZ),I24)
new_ov={'Sx':[float(abs(np.trace(A.conj().T@Sx504)/n)) for A in T], 'JZ_seed':[float(abs(np.trace(A.conj().T@JZ504)/n)) for A in T]}
summary={
 'Gram_matrix':G.tolist(),'rank':int(np.linalg.matrix_rank(G)),'condition_number':float(np.linalg.cond(G)),
 'expected_diagonal':['12/7','2','12/7','12/7','1','1/3','4/7'],
 'max_offdiag':float(np.max(np.abs(G-np.diag(np.diag(G))))),
 'projection_test':{'max_normal_equation_residual':float(np.max(np.abs(G@c-J))),'max_orthogonality_residual':float(np.max(np.abs(orth))),'reconstruction_norm_difference_under_basis_rescaling':float(np.linalg.norm(P-Pp,'fro')),'max_cprime_minus_Sinv_c':float(np.max(np.abs(cp-np.linalg.solve(S,c)))),'max_Gprime_minus_SGS':float(np.max(np.abs(Gp-S@G@S))),'max_Jprime_minus_SJ':float(np.max(np.abs(Jp-S@J)))},
 'new_direction_overlaps':new_ov,
 'theorem':'For any parent generator K, the unique Hilbert-Schmidt projection coefficients on the seven-term addressed subspace satisfy Gc=J with J_a=Tr(T_a^dagger K)/504. Under T->ST, c->S^{-1}c, G->SGS, J->SJ, so the physical projected operator is normalization invariant.'
}
(RES/'12_parent_projection_theorem.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
