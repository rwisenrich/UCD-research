from pathlib import Path
import json,numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
rng=np.random.default_rng(504);n=12;M=rng.normal(size=(n,n));C=M@M.T+np.eye(n);r=rng.normal(size=n);A=rng.normal(size=(n,n))
while abs(np.linalg.det(A))<1e-5:A=rng.normal(size=(n,n))
chi=float(r@np.linalg.solve(C,r));r2=A@r;C2=A@C@A.T;chi2=float(r2@np.linalg.solve(C2,r2))
out={'frozen_model_object':'M=(Omega0,S_parent,E_star,history,nuisance_policy)','prediction_vector':'mu(M)=(CMB,BAO,SNe,H(z),lensing,growth,JWST,...)','residual':'r=d-mu(M)','joint_gaussian_statistic':'chi2=r^T C^{-1} r','basis_invariance':'under r->A r and C->A C A^T for invertible A, chi2 is unchanged','numeric_invariance_residual':abs(chi-chi2),'severance_signature':'Delta_O=O(history_with_severance)-O(reference_history), computed from one common history map across all observable blocks','likelihood_ratio':'2 log Lambda = 2[log L_UCD - log L_reference] evaluated after model freeze','holdout_rule':'all structural/model parameters are fixed before holdout data are evaluated; nuisance parameters are handled only by the preregistered marginalization/profile rule'}
(RES/'41_frozen_cosmology_theorem.json').write_text(json.dumps(out,indent=2));print(json.dumps({'chi2':chi,'transformed':chi2,'residual':abs(chi-chi2)},indent=2))
