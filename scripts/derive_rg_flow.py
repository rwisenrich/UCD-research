from pathlib import Path
import csv,json,math
from fractions import Fraction
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
b={'g1':Fraction(41,10),'g2':Fraction(-19,6),'g3':Fraction(-7,1)}
rows=[]
for name,bi in b.items():
    rows.append({'coupling':name,'b_i':str(bi),'d_alpha_inverse_d_ln_mu':float(-bi/(2*math.pi)),'delta_inverse_g2_per_refinement_ln2':float(-bi*math.log(2)/(8*math.pi**2))})
with (RES/'36_one_loop_rg_refinement.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
out={'beta_convention':'d g_i/d ln(mu)=b_i g_i^3/(16 pi^2)','b_gut_normalized':{k:str(v) for k,v in b.items()},'integrated_solution':'1/g_i(mu)^2=1/g_i(mu_B)^2-b_i/(8 pi^2) ln(mu/mu_B)','native_boundary_trace_relation':'g3(mu_B)=g2(mu_B)=g1(mu_B), where g1=sqrt(5/3) gY','refinement_scale':'a_r=L_*/2^r, mu_r=xi/a_r, so ln(mu_{r+1}/mu_r)=ln 2','discrete_refinement_step':'1/g_i(r+1)^2-1/g_i(r)^2= -b_i ln2/(8 pi^2)'}
(RES/'37_rg_flow_theorem.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
