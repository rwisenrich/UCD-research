from pathlib import Path
import json, csv, math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'; RES.mkdir(exist_ok=True)
sz=np.array([[1,0],[0,-1]],complex);sx=np.array([[0,1],[1,0]],complex);I=np.eye(2,dtype=complex);a=np.diag([np.exp(1j*np.pi/6),np.exp(-1j*np.pi/6)]);x=1j*sx;omega=np.exp(2j*np.pi/3)
def W(m,k,e):return (omega**m)*np.linalg.matrix_power(a,k)@np.linalg.matrix_power(x,e)
def inv(U):return U.conj().T
V=list(range(5));tree=[(0,1),(1,2),(1,3),(3,4)];chords=[(2,3),(0,4)];edges=tree+chords;labels=[(1,2,0),(2,5,1),(0,7,0),(1,9,1),(2,4,1),(1,1,0)];links={e:W(*lab) for e,lab in zip(edges,labels)}
g={0:I.copy()}
for u,v in tree:g[v]=g[u]@inv(links[(u,v)])
def transformed(e):
    u,v=e;return g[v]@links[e]@inv(g[u])
tree_res=max(np.linalg.norm(transformed(e)-I) for e in tree)
chord_rows=[]
for e in chords:
    H=transformed(e);chord_rows.append({'u':e[0],'v':e[1],'unitarity_residual':float(np.linalg.norm(H.conj().T@H-I)),'trace_real':float(np.real(np.trace(H))),'trace_imag':float(np.imag(np.trace(H))),'det_real':float(np.real(np.linalg.det(H))),'det_imag':float(np.imag(np.linalg.det(H)))})
with (RES/'23_omega_tree_gauge_holonomies.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=chord_rows[0].keys());w.writeheader();w.writerows(chord_rows)
d=12;rng=np.random.default_rng(50472);psi=rng.normal(size=d)+1j*rng.normal(size=d);psi/=np.linalg.norm(psi);rho=np.outer(psi,psi.conj());rho_rec=np.zeros((d,d),complex)
for j in range(d):rho_rec[j,j]=rho[j,j].real
for j in range(d):
    for k in range(j+1,d):
        S=np.zeros((d,d),complex);S[j,k]=1;S[k,j]=1;A=np.zeros((d,d),complex);A[j,k]=-1j;A[k,j]=1j;es=float(np.real(np.trace(rho@S)));ea=float(np.real(np.trace(rho@A)));z=es/2-1j*ea/2;rho_rec[j,k]=z;rho_rec[k,j]=z.conjugate()
res=np.linalg.norm(rho_rec-rho)
if res>1e-10:
    rho_rec=np.zeros((d,d),complex)
    for j in range(d):rho_rec[j,j]=rho[j,j].real
    for j in range(d):
        for k in range(j+1,d):
            S=np.zeros((d,d),complex);S[j,k]=1;S[k,j]=1;A=np.zeros((d,d),complex);A[j,k]=-1j;A[k,j]=1j;es=float(np.real(np.trace(rho@S)));ea=float(np.real(np.trace(rho@A)));z=es/2+1j*ea/2;rho_rec[j,k]=z;rho_rec[k,j]=z.conjugate()
res=float(np.linalg.norm(rho_rec-rho));herm=float(np.linalg.norm(rho_rec-rho_rec.conj().T));trace=float(abs(np.trace(rho_rec)-1));rank=np.linalg.matrix_rank(rho_rec,tol=1e-10);vals,vecs=np.linalg.eigh(rho_rec);psir=vecs[:,np.argmax(vals)];overlap=float(abs(np.vdot(psi,psir)))
def unitary_from_hermitian(H,t):
    ev,U=np.linalg.eigh(H);return U@np.diag(np.exp(-1j*t*ev))@U.conj().T
Us=[]
for n in range(4):M=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));H=(M+M.conj().T)/2;Us.append(unitary_from_hermitian(H,0.01*(n+1)))
Uhist=np.eye(d,dtype=complex)
for U in Us:Uhist=U@Uhist
psiN=Uhist@psi;psi0rec=Uhist.conj().T@psiN;reverse_res=float(np.linalg.norm(psi0rec-psi));unitarity_res=float(np.linalg.norm(Uhist.conj().T@Uhist-np.eye(d)))
summary={'graph_vertices':len(V),'graph_edges':len(edges),'tree_edges':len(tree),'independent_cycles':len(edges)-len(V)+1,'tree_gauge_identity_max_residual':float(tree_res),'tomography_dimension_tested':d,'tomography_density_matrix_residual':res,'tomography_hermiticity_residual':herm,'tomography_trace_residual':trace,'tomography_rank':int(rank),'pure_state_overlap_after_tomography':overlap,'history_unitarity_residual':unitarity_res,'history_reverse_reconstruction_residual':reverse_res,'theorem_statement':'For a connected finite addressed graph, a rooted spanning-tree gauge fixes all tree links to identity; the remaining chord matrices are the fundamental holonomies. Informationally complete Hermitian expectations uniquely determine rho; rank-one rho determines Psi up to global phase. Exact unitary history reconstructs Psi0 by U^dagger.'}
(RES/'24_omega_reconstruction_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
