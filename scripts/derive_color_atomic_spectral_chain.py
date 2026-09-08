from pathlib import Path
import json,csv,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
lam=[];lam.append(np.array([[0,1,0],[1,0,0],[0,0,0]],complex));lam.append(np.array([[0,-1j,0],[1j,0,0],[0,0,0]],complex));lam.append(np.diag([1,-1,0]).astype(complex));lam.append(np.array([[0,0,1],[0,0,0],[1,0,0]],complex));lam.append(np.array([[0,0,-1j],[0,0,0],[1j,0,0]],complex));lam.append(np.array([[0,0,0],[0,0,1],[0,1,0]],complex));lam.append(np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex));lam.append(np.diag([1,1,-2]).astype(complex)/np.sqrt(3));t=[L/2 for L in lam];I3=np.eye(3,dtype=complex)
mes=np.zeros(9,complex)
for i in range(3):mes[i*3+i]=1/np.sqrt(3)
mes_res=[]
for T in t:mes_res.append(np.linalg.norm((np.kron(T,I3)+np.kron(I3,-T.conj()))@mes))
pair_mes=sum(np.vdot(mes,np.kron(T,-T.conj())@mes).real for T in t)
bar=np.zeros(27,complex)
def idx(i,j,k):return i*9+j*3+k
for perm in itertools.permutations(range(3)):
    inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));bar[idx(*perm)]=((-1)**inv)/np.sqrt(6)
bar_res=[]
for T in t:
    G=np.kron(np.kron(T,I3),I3)+np.kron(np.kron(I3,T),I3)+np.kron(np.kron(I3,I3),T);bar_res.append(np.linalg.norm(G@bar))
pair_vals=[]
for pair in [(0,1),(0,2),(1,2)]:
    op=np.zeros((27,27),complex)
    for T in t:
        O=np.kron(np.kron(T,T),I3) if pair==(0,1) else np.kron(np.kron(T,I3),T) if pair==(0,2) else np.kron(np.kron(I3,T),T);op+=O
    pair_vals.append(float(np.vdot(bar,op@bar).real))
CF=sum(T@T for T in t);CFres=float(np.linalg.norm(CF-(4/3)*I3));rows=[]
for n in range(1,8):
    for l in range(n):rows.append({'n':n,'l':l,'subshell_capacity':2*(2*l+1),'shell_capacity_formula':2*n*n})
with (RES/'29_atomic_shell_capacity.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=rows[0].keys());wr.writeheader();wr.writerows(rows)
letters='spdfghijk';subs=[]
for n in range(1,9):
  for l in range(n):subs.append((n+l,n,l,2*(2*l+1)))
subs.sort(key=lambda z:(z[0],z[1]));Z=0;auf=[]
for _,n,l,cap in subs:
    if Z>=118:break
    take=min(cap,118-Z);Z+=take;auf.append({'subshell':f'{n}{letters[l]}','capacity':cap,'electrons_through_subshell':Z,'fill_to_118':take})
with (RES/'30_aufbau_capacity_to_118.csv').open('w',newline='') as f:wr=csv.DictWriter(f,fieldnames=auf[0].keys());wr.writeheader();wr.writerows(auf)
summary={'fundamental_casimir_residual':CFres,'meson_singlet_generator_max_residual':float(max(mes_res)),'meson_pair_color_factor':float(pair_mes),'baryon_singlet_generator_max_residual':float(max(bar_res)),'baryon_pair_color_factors':pair_vals,'ideal_shell_capacity_identity':'sum_{l=0}^{n-1} 2(2l+1)=2n^2','spectral_mass_formula':'For a stable color-singlet interpolator O_H, C_H(t)=sum_n |<0|O_H|n>|^2 exp(-E_n t); m_H=lim_{t->infty}[-d/dt log C_H(t)] after the physical scale is fixed.','atomic_operator':'H_atom=sum_i[c alpha_i.p_i+beta_i m_e c^2-Z alpha hbar c/r_i]+sum_{i<j} alpha hbar c/r_ij + recoil + radiative + finite-nucleus terms.'}
(RES/'31_color_atomic_spectral_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
