#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, sys, json, csv, math
from pathlib import Path
from fractions import Fraction
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'results'
RES.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location('h504', str(Path(__file__).with_name('ucd_504_master_hamiltonian.py')))
h = importlib.util.module_from_spec(spec); sys.modules['h504']=h; spec.loader.exec_module(h)

def fro(A): return float(np.linalg.norm(A, 'fro'))
def dump(name,obj): (RES/name).write_text(json.dumps(obj,indent=2,default=str))
def writecsv(name, rows):
    if not rows: return
    with open(RES/name,'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

v=h.V7_ops(); I7=np.eye(7,dtype=complex)
Tp=v['Tp']; P_leaf=v['R7']; P_center=v['Pc']
leaf_cols=[]; crt_rows=[]
for c in range(3):
    for o in range(2):
        n=next(n for n in range(6) if n%3==c and n%2==o)
        vec=np.zeros((7,),complex); vec[n+1]=1
        leaf_cols.append(vec)
        crt_rows.append({'color_index':c,'orientation_index':o,'leaf_number_1_to_6':n+1})
Bleaf=np.column_stack(leaf_cols)
Tp6=Bleaf.conj().T@Tp@Bleaf
X3=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
X2=np.array([[0,1],[1,0]],complex)
shift_res=min(fro(Tp6-np.kron(X3,X2)),fro(Tp6-np.kron(X3.conj().T,X2)))
sqrt3=math.sqrt(3)
lam=[]
lam.append(np.array([[0,1,0],[1,0,0],[0,0,0]],complex))
lam.append(np.array([[0,-1j,0],[1j,0,0],[0,0,0]],complex))
lam.append(np.diag([1,-1,0]).astype(complex))
lam.append(np.array([[0,0,1],[0,0,0],[1,0,0]],complex))
lam.append(np.array([[0,0,-1j],[0,0,0],[1j,0,0]],complex))
lam.append(np.array([[0,0,0],[0,0,1],[0,1,0]],complex))
lam.append(np.array([[0,0,0],[0,0,-1j],[0,1j,0]],complex))
lam.append(np.diag([1,1,-2]).astype(complex)/sqrt3)
t3=[L/2 for L in lam]
color7=[]
for t in t3:
    Tleaf=np.kron(t,np.eye(2))
    color7.append(Bleaf@Tleaf@Bleaf.conj().T)
Gram=np.array([[np.trace(a.conj().T@b).real for b in color7] for a in color7])
max_su3_closure=0.0; structure=[]
for a in range(8):
    for b in range(8):
        C=(color7[a]@color7[b]-color7[b]@color7[a])/1j
        coeff=np.linalg.solve(Gram, np.array([np.trace(g.conj().T@C).real for g in color7]))
        Cres=C-sum(coeff[k]*color7[k] for k in range(8))
        max_su3_closure=max(max_su3_closure,fro(Cres))
        if np.linalg.norm(coeff)>1e-10:
            structure.append({'a':a+1,'b':b+1,'coefficients':';'.join(f'{x:.12g}' for x in coeff)})
Cas=sum(T@T for T in color7)
color_casimir_res=fro(Cas-(4/3)*P_leaf)
color_center_res=max(fro(T@P_center) for T in color7)
writecsv('01_leaf_crt_factorization.csv',crt_rows); writecsv('01_su3_structure_nonzero.csv',structure)

I24=np.eye(24,dtype=complex); B=h.left_regular((6,0))
Zc=np.zeros((24,24),complex); Gamma_chi=np.zeros((24,24),complex)
for idx,(k,e) in enumerate(h.ELEMS):
    Zc[idx,idx]=1 if k<6 else -1
    Gamma_chi[idx,idx]=1 if e==0 else -1
tau3=B; tau1=Zc; tau2=-1j*B@Zc
pauli_res={'tau1_sq':fro(tau1@tau1-I24),'tau2_sq':fro(tau2@tau2-I24),'tau3_sq':fro(tau3@tau3-I24),'12':fro(tau1@tau2-tau2@tau1-2j*tau3),'23':fro(tau2@tau3-tau3@tau2-2j*tau1),'31':fro(tau3@tau1-tau1@tau3-2j*tau2),'gamma_sq':fro(Gamma_chi@Gamma_chi-I24),'gamma_tau_comm_max':max(fro(Gamma_chi@T-T@Gamma_chi) for T in (tau1,tau2,tau3))}
sigma=1; PL24=(I24-sigma*Gamma_chi)/2; PR24=I24-PL24
weak24=[PL24@T/2 for T in (tau1,tau2,tau3)]
weak_res={'12':fro(weak24[0]@weak24[1]-weak24[1]@weak24[0]-1j*weak24[2]),'23':fro(weak24[1]@weak24[2]-weak24[2]@weak24[1]-1j*weak24[0]),'31':fro(weak24[2]@weak24[0]-weak24[0]@weak24[2]-1j*weak24[1]),'right_singlet_max':max(fro(PR24@T) for T in weak24)}

I3=np.eye(3,dtype=complex); I504=np.eye(504,dtype=complex)
A7=v['I7']-2*v['Pc']; A=np.kron(np.kron(A7,I3),I24); B504=np.kron(np.kron(I7,I3),B); Gamma504=np.kron(np.kron(I7,I3),Gamma_chi)
PL=np.kron(np.kron(I7,I3),PL24); PR=I504-PL; C=2*A+B504
Qpoly=(C@C@C-4*C-3*I504)/18; Qlin=A/3+B504/2-I504/6; q_formula_res=fro(Qpoly-Qlin); T3w=PL@B504/2; Y=2*(Qlin-T3w); Yclosed=(2*A-I504)/3 + PR@B504; y_formula_res=fro(Y-Yclosed)
Weak=[np.kron(np.kron(I7,I3),W) for W in weak24]
weak_full_res=max(fro(Weak[0]@Weak[1]-Weak[1]@Weak[0]-1j*Weak[2]),fro(Weak[1]@Weak[2]-Weak[2]@Weak[1]-1j*Weak[0]),fro(Weak[2]@Weak[0]-Weak[0]@Weak[2]-1j*Weak[1]))
y_weak_comm=max(fro(Y@W-W@Y) for W in Weak)
Color=[np.kron(np.kron(T,I3),I24) for T in color7]
color_weak_comm=max(fro(T@W-W@T) for T in Color for W in Weak); y_color_comm=max(fro(Y@T-T@Y) for T in Color)
rows=[]
for aval,atype in [(-1,'lepton'),(1,'quark')]:
    PA=(I504+aval*A)/2
    for bval,btype,qname in [(-1,'lower','e' if aval==-1 else 'd'),(1,'upper','nu' if aval==-1 else 'u')]:
        PB=(I504+bval*B504)/2
        for chir,Pchi in [('L',PL),('R',PR)]:
            P=PA@PB@Pchi; rank=int(round(np.trace(P).real)); y=float(np.trace(P@Y).real/rank); t3v=float(np.trace(P@T3w).real/rank); q=float(np.trace(P@Qlin).real/rank)
            rows.append({'particle':qname+'_'+chir,'A_geometry':aval,'B_isospin':bval,'chirality':chir,'rank_in_H504':rank,'rank_per_Z3_family':rank//3,'Q':q,'T3':t3v,'Y':y,'color_rep':'1' if aval==-1 else '3','weak_rep':'2' if chir=='L' else '1'})
writecsv('02_native_species_table.csv',rows)
trace_SU3=Fraction(2,1); trace_SU2=Fraction(2,1); trace_U1=Fraction(10,3); Ngen=3; sumT3_weyl=Fraction(2*Ngen,1); sumT2_weyl=Fraction(2*Ngen,1); sumy2_weyl=Fraction(10*Ngen,3); sumT2_scalar=Fraction(1,2); sumy2_scalar=Fraction(1,2)
b3=-Fraction(11,3)*3 + Fraction(2,3)*sumT3_weyl; b2=-Fraction(11,3)*2 + Fraction(2,3)*sumT2_weyl + Fraction(1,3)*sumT2_scalar; bY=Fraction(2,3)*sumy2_weyl + Fraction(1,3)*sumy2_scalar; b1=Fraction(3,5)*bY
beta_rows=[{'coupling':'g3','b_exact':str(b3),'b_float':float(b3),'beta_convention':'dg/dlnmu = b g^3/(16 pi^2)'},{'coupling':'g2','b_exact':str(b2),'b_float':float(b2),'beta_convention':'dg/dlnmu = b g^3/(16 pi^2)'},{'coupling':'gY','b_exact':str(bY),'b_float':float(bY),'beta_convention':'dg/dlnmu = b g^3/(16 pi^2)'},{'coupling':'g1=sqrt(5/3)gY','b_exact':str(b1),'b_float':float(b1),'beta_convention':'dg/dlnmu = b g^3/(16 pi^2)'}]
writecsv('03_one_loop_beta_coefficients.csv',beta_rows)
fields=[('Q_L',3,2,Fraction(1,3),'3','2'),('u_R^c',3,1,Fraction(-4,3),'3bar','1'),('d_R^c',3,1,Fraction(2,3),'3bar','1'),('L_L',1,2,Fraction(-1,1),'1','2'),('e_R^c',1,1,Fraction(2,1),'1','1'),('nu_R^c',1,1,Fraction(0,1),'1','1')]
Agrav=sum(Fraction(nc*nw)*yy for _,nc,nw,yy,_,_ in fields); Au1=sum(Fraction(nc*nw)*yy**3 for _,nc,nw,yy,_,_ in fields); Asu2=sum(Fraction(nc,2)*yy for _,nc,nw,yy,_,wr in fields if wr=='2'); Asu3=sum(Fraction(nw,2)*yy for _,nc,nw,yy,cr,_ in fields if cr in ('3','3bar')); Asu3cub=sum(Fraction(nw)*(1 if cr=='3' else -1 if cr=='3bar' else 0) for _,nc,nw,yy,cr,_ in fields); witten_doublets=4
anoms={'gravitational_U1':str(Agrav),'U1_cubic':str(Au1),'SU2^2_U1':str(Asu2),'SU3^2_U1':str(Asu3),'SU3_cubic_relative':str(Asu3cub),'Witten_SU2_doublets_mod2':witten_doublets%2}
summary={'charge_identity':'Q = B/2 + A/3 - I/6, derived algebraically from C=2A+B and A^2=B^2=I.','chirality_operator':'Gamma_chi |a^k x^e> = (-1)^e |a^k x^e>; P_L=(I-sigma Gamma_chi)/2.','weak_generators':'On C[Dic6], tau3=B=L(a^6), tau1=Z_centralbit, tau2=-i B Z_centralbit; T_i=P_L tau_i/2.','hypercharge_identity':'Y = 2(Q-T3) = (2A-I)/3 + P_R B.','color_construction':'Leaf C6 factor is C3_color tensor C2_orientation by CRT; Gell-Mann/2 on C3 and identity on C2 gives su(3), extended by zero on the center.','family':'The separate C[Z3] factor supplies exactly three family labels.','gauge_algebra_checks':{'leaf_shift_CRT_residual':shift_res,'su3_closure_residual':max_su3_closure,'color_Casimir_residual':color_casimir_res,'color_annihilates_center_residual':color_center_res,'weak_pauli':pauli_res,'weak_su2_residual':weak_full_res,'Y_commutes_weak_residual':y_weak_comm,'color_commutes_weak_residual':color_weak_comm,'Y_commutes_color_residual':y_color_comm,'Q_polynomial_to_linear_residual':q_formula_res,'Y_closed_form_residual':y_formula_res},'matter_trace_metric_one_generation':{'Tr_fixed_SU3_generator_squared':str(trace_SU3),'Tr_fixed_SU2_generator_squared':str(trace_SU2),'Tr_(Y/2)^2':str(trace_U1),'ratios':'G3:G2:GY = 1:1:5/3; hence equal parent kinetic normalization gives g3^2=g2^2 and gY^2/g2^2=3/5.'},'one_loop_beta_coefficients':{x['coupling']:x['b_exact'] for x in beta_rows},'anomalies_one_generation':anoms,'species_table_file':'02_native_species_table.csv'}
dump('04_native_gauge_matter_theorem.json',summary); print(json.dumps(summary,indent=2))
