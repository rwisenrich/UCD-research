from pathlib import Path
import csv,json,math
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
rows=[]
for r in range(4,13):
    a=2**(-r); n=math.ceil(1/a)
    rows.append({'r':r,'a_r':a,'n_r':n,'lemm_threshold_1_over_n_plus_2_over_n2':1/n+2/n**2,'mass_term_a_m0_over_J':a,'sufficient_block_gap':1/n+2/n**2+a})
with (RES/'42_regulator_scaled_gap_schedule.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
out={'physical_hamiltonian_scaling':'a_r H_phys = J_r K_r','physical_gap':'m_r=J_r gamma_r/a_r','fixed_physical_block':'n_r a_r -> ell0','nearest_neighbor_ff_finite_size_criterion':'for the stated frustration-free projector class in D>2, gamma_N >= gamma_Bn - 1/n - 2/n^2','sufficient_scaled_certificate':'gamma_block(r,n_r) >= 1/n_r + 2/n_r^2 + a_r m0/J_r implies m_global(r) >= m0 within that theorem class','continuum_spectral_transfer':'if connected Euclidean correlators converge and obey a uniform bound |C_r(t)|<=A exp(-m0 t), the limiting spectral measures have no support in (0,m0)'}
(RES/'43_regulator_scaled_gap_theorem.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
