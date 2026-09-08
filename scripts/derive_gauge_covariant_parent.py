#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, sys, csv, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'; RES.mkdir(parents=True, exist_ok=True)
spec=importlib.util.spec_from_file_location('h504', str(Path(__file__).with_name('ucd_504_master_hamiltonian.py'))); h=importlib.util.module_from_spec(spec); sys.modules['h504']=h; spec.loader.exec_module(h)
def fro(A): return float(np.linalg.norm(A,'fro'))
def writecsv(name, rows):
    with open(RES/name,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
def dump(name,obj): (RES/name).write_text(json.dumps(obj,indent=2,default=str))
v=h.V7_ops(); I7=np.eye(7,dtype=complex); I3=np.eye(3,dtype=complex); I24=np.eye(24,dtype=complex); I504=np.eye(504,dtype=complex); A7=I7-2*v['Pc']; A=np.kron(np.kron(A7,I3),I24); B24=h.left_regular((6,0)); B=np.kron(np.kron(I7,I3),B24); Gamma24=np.diag([1 if e==0 else -1 for (k,e) in h.ELEMS]).astype(complex); Gamma=np.kron(np.kron(I7,I3),Gamma24); PL=(I504-Gamma)/2; PR=I504-PL; Q=A/3+B/2-I504/6; T3w=PL@B/2; Y=2*(Q-T3w)
Zc24=np.diag([1 if k<6 else -1 for (k,e) in h.ELEMS]).astype(complex); tau1=Zc24; tau3=B24; tau2=-1j*B24@Zc24; PL24=(I24-Gamma24)/2; Weak24=[PL24@t/2 for t in (tau1,tau2,tau3)]; Weak=[np.kron(np.kron(I7,I3),w) for w in Weak24]
Tp=v['Tp']; leaf_cols=[]
for c in range(3):
    for o in range(2):
        n=next(n for n in range(6) if n%3==c and n%2==o); e=np.zeros(7,complex); e[n+1]=1; leaf_cols.append(e)
Bleaf=np.column_stack(leaf_cols); s3=math.sqrt(3); lam=[np.array([[0,1,0],[1,0,0],[0,0,0]],complex),np.array([[0,-1j,0],[1j,0,0],[0,0,0]],complex),np.diag([1,-1,0]).astype(complex),np.array([[0,0,1],[0,0,0],[1,0,0]],complex),np.array([[0,0,-1j],[0,0,0],[1j,0,0]],complex),np.array([[0,0,0],[0,0,1],[0,1,0]],complex),np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex),np.diag([1,1,-2]).astype(complex)/s3]; color7=[Bleaf@np.kron(L/2,np.eye(2))@Bleaf.conj().T for L in lam]; Color=[np.kron(np.kron(c,I3),I24) for c in color7]
species={}; meta={}
for aval,label,colorrep in [(-1,'l','1'),(1,'q','3')]:
    PA=(I504+aval*A)/2
    for bval,name in [(-1,'lower'),(1,'upper')]:
        PB=(I504+bval*B)/2; pname=('e' if aval==-1 and bval==-1 else 'nu' if aval==-1 else 'd' if bval==-1 else 'u')
        for chir,Pchi in [('L',PL),('R',PR)]:
            key=pname+'_'+chir; P=PA@PB@Pchi; species[key]=P; rank=int(round(np.trace(P).real)); meta[key]={'rank':rank,'color':colorrep,'weak':'2' if chir=='L' else '1','Y':float(np.trace(P@Y).real/rank),'Q':float(np.trace(P@Q).real/rank),'chir':chir,'B':bval,'A':aval}
ht=h.build_terms('reflection'); rows=[]
for name,T in zip(ht.names,ht.terms):
    transitions=[]
    for out,Po in species.items():
        for inn,Pi in species.items():
            nrm=fro(Po@T@Pi)
            if nrm>1e-9:transitions.append((out,inn,nrm))
    rows.append({'term':name,'fro_norm':fro(T),'comm_Q':fro(Q@T-T@Q),'comm_Y':fro(Y@T-T@Y),'comm_chirality':fro(Gamma@T-T@Gamma),'max_comm_SU3':max(fro(G@T-T@G) for G in Color),'max_comm_SU2':max(fro(G@T-T@G) for G in Weak),'nonzero_species_blocks':len(transitions),'transition_list':'; '.join(f'{i}->{o}:{n:.6g}' for o,i,n in transitions)})
writecsv('06_h504_term_gauge_commutators.csv',rows)
medrows=[]
for name,T in zip(ht.names,ht.terms):
    for out,Po in species.items():
        for inn,Pi in species.items():
            nrm=fro(Po@T@Pi)
            if nrm<=1e-9 or out==inn:continue
            mo,mi=meta[out],meta[inn]; medrows.append({'term':name,'input':inn,'output':out,'block_norm':nrm,'input_rep':f"({mi['color']},{mi['weak']})_Y={mi['Y']:.12g}",'output_rep':f"({mo['color']},{mo['weak']})_Y={mo['Y']:.12g}",'delta_Y_output_minus_input':mo['Y']-mi['Y'],'interpretation':'mediator transforms as R_out tensor R_in*; sign reversed for Hermitian-conjugate block'})
writecsv('07_cross_species_mediator_requirements.csv',medrows)
Tp6=Bleaf.conj().T@v['Tp']@Bleaf; Tm6=Bleaf.conj().T@v['Tm']@Bleaf; R6=Tp6+Tm6; X3=np.array([[0,0,1],[1,0,0],[0,1,0]],complex); X2=np.array([[0,1],[1,0]],complex); ring_product_res=fro(R6-np.kron(X3+X3.conj().T,X2)); color_trace=float(np.trace(X3+X3.conj().T).real)
cols=[]
for k0 in range(6):
    for e in (0,1):
        for z in (0,1):
            idx=h.IDX[((k0+6*z)%12,e)]; vec=np.zeros(24,complex); vec[idx]=1; cols.append(vec)
F=np.column_stack(cols); La=h.left_regular((1,0)); rho_orient=(La+La.conj().T)/2; O=F.conj().T@rho_orient@F; O4=O.reshape(12,2,12,2); paulis=[np.eye(2),np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]; parts=[]
for P in paulis:
    Cc=np.zeros((12,12),complex)
    for q in range(12):
        for qp in range(12):Cc[q,qp]=0.5*np.trace(P@O4[q,:,qp,:])
    parts.append(Cc)
weak_component_norms=[fro(Cc) for Cc in parts]; recon=sum(np.kron(parts[mu],paulis[mu]) for mu in range(4)); weak_decomp_res=fro(O-recon)
T6=ht.terms[5]; t6_present={(o,i) for o,Po in species.items() for i,Pi in species.items() if fro(Po@T6@Pi)>1e-9}; singlets=[]
for name,T in zip(ht.names,ht.terms):
    test=max(fro(Q@T-T@Q),max(fro(G@T-T@G) for G in Color),max(fro(G@T-T@G) for G in Weak))
    if test<1e-9:singlets.append(name)
Lx=h.left_regular((0,1)); rho_plus=(Lx+Lx.conj().T)/2; rho_minus=(Lx-Lx.conj().T)/(2j); Pplus24=(I24+B24)/2; Pminus24=(I24-B24)/2; current_identities={'Lx_dagger_minus_B_Lx':fro(Lx.conj().T-B24@Lx),'rho_plus_minus_Lx_Pplus':fro(rho_plus-Lx@Pplus24),'rho_minus_plus_i_Lx_Pminus':fro(rho_minus+1j*Lx@Pminus24),'rho_plus_Pminus':fro(rho_plus@Pminus24),'rho_minus_Pplus':fro(rho_minus@Pplus24),'rho_plus_chirality_anticomm':fro(rho_plus@Gamma24+Gamma24@rho_plus),'rho_minus_chirality_anticomm':fro(rho_minus@Gamma24+Gamma24@rho_minus)}
f=h.F3_ops(); JZ=f['JZ']; T6minus=np.kron(np.kron(I7,JZ),rho_minus); minus_trans=[]
for out,Po in species.items():
    for inn,Pi in species.items():
        nrm=fro(Po@T6minus@Pi)
        if nrm>1e-9:minus_trans.append((out,inn,nrm))
writecsv('09_complementary_current_channels.csv',[{'input':i,'output':o,'block_norm':n,'delta_Y':meta[o]['Y']-meta[i]['Y']} for o,i,n in minus_trans])
XZ=f['XZ']; D=f['P0_minus_P2']; gens=[np.eye(3,dtype=complex),XZ,JZ,D]; basis=[]
def add_if_independent(M,basis,tol=1e-10):
    v=M.reshape(-1)
    if not basis:basis.append(M);return True
    AA=np.column_stack([BB.reshape(-1) for BB in basis]); r0=np.linalg.matrix_rank(AA,tol); r1=np.linalg.matrix_rank(np.column_stack([AA,v]),tol)
    if r1>r0:basis.append(M);return True
    return False
for G0 in gens:add_if_independent(G0,basis)
changed=True
while changed:
    changed=False; old=list(basis)
    for A0 in old:
        for B0 in old:
            if add_if_independent(A0@B0,basis):changed=True
            if len(basis)==9:break
        if len(basis)==9:break
constraints=[np.kron(np.eye(3),G0)-np.kron(G0.T,np.eye(3)) for G0 in (XZ,JZ,D)]; Cmat=np.vstack(constraints); svals=np.linalg.svd(Cmat,compute_uv=False); commutant_dim=9-int(np.sum(svals>1e-10))
summary={'historical_gauge_singlets':singlets,'T1_completion':{'representation':'Xi_1 in (3,1)_{Y=4/3} plus conjugate','proof':'T1 maps L_L<->Q_L and each right-handed lepton<->quark partner with identity in weak space; Hom(2,2) component is the weak scalar.'},'T4_completion':{'right_handed':'Xi_R in (3,1)_{Y=4/3} plus conjugate','left_handed':'Xi_L in (3,3)_{Y=4/3} plus conjugate','proof':'T4 carries B. On P_L, B=2 T3 is traceless in Hom(2,2), hence the weak-adjoint 3; on P_R both endpoints are weak singlets.'},'T3_completion':{'representation':'SU(3) adjoint connection (8,1)_0 on the quark leaf sector','identity':'Rring=(X3+X3^dagger) tensor X2_orientation','product_residual':ring_product_res,'color_trace':color_trace},'T5_completion':{'decomposition':'rho_orient = K0 tensor I_2 + K3 tensor tau3 in the central-Z2 factorization','component_norms_I_sigmaX_sigmaY_sigmaZ':weak_component_norms,'reconstruction_residual':weak_decomp_res},'T6_upper_yukawa':{'identity_checks':current_identities,'channels':sorted([f'{i}->{o}' for o,i in t6_present]),'mediator':'tilde H in (1,2)_{Y=-1} for R->L upper channels and Hermitian conjugate for L->R'},'complementary_lower_yukawa':{'operator':'rho_-=(Lx-Lx^dagger)/(2i)=-i Lx P_{B=-1}','channels':sorted([f'{i}->{o}' for o,i,n in minus_trans]),'mediator':'H in (1,2)_{Y=+1} for R->L lower channels and Hermitian conjugate for L->R'},'family_algebra':{'generators':['I','X_Z','J_Z','D=P0-P2'],'generated_complex_matrix_algebra_dimension':len(basis),'commutant_dimension':commutant_dim,'conclusion':'The native family operators generate M3(C).'}}
dump('10_gauge_covariant_parent_completion.json',summary); print(json.dumps(summary,indent=2))
