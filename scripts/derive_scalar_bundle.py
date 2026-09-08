from pathlib import Path
import csv,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
S=np.roll(np.eye(3),1,axis=1).astype(complex);X=S+S.conj().T;J=(S-S.conj().T)/(1j*math.sqrt(3));res_X=np.linalg.norm(X.conj()-X);res_J=np.linalg.norm(J.conj()+J);eigs=np.linalg.eigvalsh(J)
Y={'L':-1,'eR':-2,'nuR':0,'Q':1/3,'dR':-2/3,'uR':4/3};YH=1.0
checks={'LeH_eR':-Y['L']+YH+Y['eR'],'LtildeH_nuR':-Y['L']-YH+Y['nuR'],'QH_dR':-Y['Q']+YH+Y['dR'],'QtildeH_uR':-Y['Q']-YH+Y['uR']}
with (RES/'38_scalar_yukawa_hypercharge_checks.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['term','residual']);[w.writerow([k,v]) for k,v in checks.items()]
out={'family_shift_eigenvalues_JZ':[float(x) for x in eigs],'orientation_reversal_X_even_residual':float(res_X),'orientation_reversal_J_odd_residual':float(res_J),'minimal_Hermitian_degree_one_family_space':'span_R{I,X_Z,J_Z}','orientation_odd_subspace':'R J_Z (dimension 1)','scalar_generation_seed':'Phi_gen=sigma J_Z','higgs_representation':'H:(1,2)_{+1}; tilde H:(1,2)_{-1}','yukawa_hypercharge_residuals':checks,'renormalizable_single_doublet_potential':'V(H)=V0+m^2 H^dag H+lambda(H^dag H)^2','bounded_broken_phase':'lambda>0 and m^2<0 gives H^dag H=-m^2/(2lambda); in unitary gauge H=(0,(v+h)/sqrt2)^T, v^2=-m^2/lambda and m_h^2=2 lambda v^2=-2m^2','family_matrix_completion':'Alg_C(I,X_Z,J_Z,D)=M_3(C), so each Yukawa matrix is a native family-algebra element; parent projection fixes its coefficients.'}
(RES/'39_scalar_bundle_theorem.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
