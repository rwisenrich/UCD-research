from pathlib import Path
import csv,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
def Klocal(k,c1=1.0,c2=0.2):return 2*c1*(1-math.cos(k))+2*c2*(1-math.cos(2*k))
rows=[]
for k in [2**(-j) for j in range(2,11)]:
    kl=Klocal(k);rows.append({'k':k,'K_local':kl,'K_over_k2':kl/k**2,'K_over_abs_k3':kl/abs(k)**3,'target_abs_k3':abs(k)**3})
with (RES/'34_dark_kernel_local_vs_nonanalytic.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
x=np.log([r['k'] for r in rows[-6:]]); y=np.log([r['K_local'] for r in rows[-6:]]);p=float(np.polyfit(x,y,1)[0]);log_coeff=-1/(2*math.pi**2)
out={'finite_range_theorem':'An inversion-symmetric finite-range translation-invariant kernel is real analytic and even at k=0, hence has a convergent Taylor series containing only even total degree. It cannot have leading nonzero behavior C|k|^3.','representative_local_power_fit':p,'required_flat_rotation_symbol':'K_eff(k) ~ C |k|^3 in d=3','critical_green_function':'G(r)-G(r0)=-(1/(2 pi^2 C)) log(r/r0) for Fourier convention integral d^3k/(2pi)^3, modulo contact/IR constants','log_coefficient_for_C1':log_coeff,'flat_curve_identity':'Phi=A log r implies v_c^2=r dPhi/dr=A','schur_form':'K_eff=L_bb-L_bi(L_ii-E)^(-1)L_ib','schur_analyticity_theorem':'If all blocks are analytic near k=0 and L_ii(k)-E is uniformly invertible there, K_eff is analytic. Therefore |k|^3 requires a singular/critical interior limit, an infinite-depth accumulation, or another nonanalytic thermodynamic mechanism.'}
(RES/'35_dark_kernel_theorem.json').write_text(json.dumps(out,indent=2));print(json.dumps({'local_power_fit':p,'log_coeff':log_coeff},indent=2))
