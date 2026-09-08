from pathlib import Path
import json,csv
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
S=np.array([[0,0,1],[1,0,0],[0,1,0]],complex);X=S+S.conj().T;J=(S-S.conj().T)/(1j*np.sqrt(3));D=np.diag([1,0,-1]).astype(complex);I=np.eye(3,dtype=complex)
def orth_basis(mats,tol=1e-10):
    vecs=[];basis=[]
    for M in mats:
        v=M.reshape(-1).astype(complex)
        for q in vecs:v-=np.vdot(q,v)*q
        n=np.linalg.norm(v)
        if n>tol:q=v/n;vecs.append(q);basis.append(M)
    return basis
def alg_generate(gens):
    basis=orth_basis([I]+gens);changed=True
    while changed:
        changed=False;old=list(basis)
        for A in old:
            for B in old:
                before=len(basis);basis=orth_basis(basis+[A@B]);changed|=len(basis)>before
        if len(basis)>=9:break
    return basis
basis=alg_generate([X,J,D]);algdim=len(basis);rows=[]
for G in [X,J,D]:
    cols=[]
    for p in range(3):
      for q in range(3):
        E=np.zeros((3,3),complex);E[p,q]=1;cols.append((E@G-G@E).reshape(-1))
    rows.append(np.stack(cols,axis=1))
A=np.vstack(rows);s=np.linalg.svd(A,compute_uv=False);commdim=9-int(np.sum(s>1e-10));even_res=float(np.linalg.norm(X.conj()-X));odd_res=float(np.linalg.norm(J.conj()+J))
Y={'L':-1.0,'eR':-2.0,'nuR':0.0,'Q':1/3,'dR':-2/3,'uR':4/3,'H':1.0,'Ht':-1.0}
terms=[('lepton_charged','bar L H eR',-Y['L']+Y['H']+Y['eR']),('lepton_neutral','bar L Htilde nuR',-Y['L']+Y['Ht']+Y['nuR']),('quark_down','bar Q H dR',-Y['Q']+Y['H']+Y['dR']),('quark_up','bar Q Htilde uR',-Y['Q']+Y['Ht']+Y['uR'])]
with (RES/'25_yukawa_hypercharge_invariance.csv').open('w',newline='') as f:wr=csv.writer(f);wr.writerow(['term','operator','hypercharge_sum']);[wr.writerow(row) for row in terms]
rng=np.random.default_rng(720504)
def haar(n):
    Z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));Q,R=np.linalg.qr(Z);ph=np.diag(R);ph=np.where(np.abs(ph)>0,ph/np.abs(ph),1);return Q@np.diag(ph.conj())
V=haar(3);su=np.array([0.002,1.27,172.0]);sd=np.array([0.0047,0.096,4.18]);Yu=np.diag(su);Yd=V@np.diag(sd);wu,Uu=np.linalg.eigh(Yu@Yu.conj().T);wd,Ud=np.linalg.eigh(Yd@Yd.conj().T);Vrec=Uu.conj().T@Ud;ckm_abs_res=float(np.linalg.norm(np.abs(Vrec)-np.abs(V)));Bmat=np.stack([B.reshape(-1) for B in basis],axis=1);coef_u=np.linalg.lstsq(Bmat,Yu.reshape(-1),rcond=None)[0];coef_d=np.linalg.lstsq(Bmat,Yd.reshape(-1),rcond=None)[0];span_u=float(np.linalg.norm(Bmat@coef_u-Yu.reshape(-1)));span_d=float(np.linalg.norm(Bmat@coef_d-Yd.reshape(-1)))
summary={'family_associative_algebra_dimension':algdim,'family_commutant_dimension':commdim,'orientation_even_X_residual':even_res,'orientation_odd_J_residual':odd_res,'all_four_yukawa_hypercharge_residual_max':float(max(abs(r[2]) for r in terms)),'arbitrary_Yu_span_residual':span_u,'arbitrary_Yd_span_residual':span_d,'prescribed_CKM_absolute_matrix_reconstruction_residual':ckm_abs_res,'minimal_orientation_odd_degree_one_direction':'J_Z=(S-S^dagger)/(i sqrt(3))','gauge_invariant_yukawa_action':'-bar L Y_e H e_R - bar L Y_nu Htilde nu_R - bar Q Y_d H d_R - bar Q Y_u Htilde u_R + h.c.','theorem_statement':'The native family operators X_Z,J_Z,D generate M3(C), with scalar commutant. Hence every complex 3x3 Yukawa matrix belongs to the generated family algebra.'}
(RES/'26_native_flavor_completion_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
