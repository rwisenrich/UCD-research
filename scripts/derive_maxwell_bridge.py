from pathlib import Path
import csv, json, math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
charges=[(-1.0,36),(0.0,36),(-1/3,216),(2/3,216)]
tr2=sum(n*q*q for q,n in charges); tr4=sum(n*q**4 for q,n in charges)
assert abs(tr2-156)<1e-12; assert abs(tr4-244/3)<1e-12
rows=[]
for th in [0.2,0.1,0.05,0.025,0.0125,0.00625]:
    exact=sum(n*(1-math.cos(q*th)) for q,n in charges); quad=0.5*tr2*th**2; quart=quad-(tr4/24)*th**4
    rows.append({'Theta':th,'exact_ReTr_I_minus_Up':exact,'quadratic':quad,'quartic':quart,'quadratic_relative_error':abs(exact-quad)/exact,'quartic_relative_error':abs(exact-quart)/exact,'normalized_action':exact/tr2})
with (RES/'32_maxwell_bridge_convergence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
x=np.log([r['Theta'] for r in rows]); y=np.log([r['quadratic_relative_error'] for r in rows]); p=np.polyfit(x,y,1)[0]
out={'charge_multiplicities':[{'q':q,'multiplicity':n} for q,n in charges],'TrQ2':tr2,'TrQ4':tr4,'exact_plaquette_action':'S_p=(1/156) Re Tr(I-exp(i Q Theta_p))','equivalent_HS_action':'S_p=(1/312)||I-exp(i Q Theta_p)||_HS^2','small_phase_expansion':'S_p=Theta_p^2/2-(61/2808)Theta_p^4+O(Theta_p^6)','edge_identification':'theta_e=g a A_mu+O(a^2)','plaquette_identification':'Theta_p=g a^2 F_munu+O(a^3)','quadratic_relative_error_power_fit':float(p)}
(RES/'33_maxwell_bridge_theorem.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
