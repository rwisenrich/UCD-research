from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1];p=root/'results';out=root/'figures';out.mkdir(exist_ok=True)
G=json.loads((p/'gravity_spin2_bounce.json').read_text());z=G['spin2']['unimproved_refinement']
a=np.array([x['a'] for x in z]);e2=np.array([x['relative_unimproved_error'] for x in z]);e4=np.array([x['relative_improved_error'] for x in z])
plt.figure(figsize=(7,4.3));plt.loglog(a,e2,'o-',label='Kelvin second-order symbol');plt.loglog(a,e4,'s-',label='Richardson fourth-order symbol');plt.xlabel('Lattice spacing a');plt.ylabel('Relative symbol error');plt.title('Kelvin spatial spin-2 dispersion refinement');plt.legend();plt.grid(True,which='both',alpha=.2);plt.tight_layout();plt.savefig(out/'spin2_refinement.png',dpi=175);plt.close()
rows=G['regular_core']['trajectory'];t=np.array([v['tau'] for v in rows]);r=np.array([v['radius'] for v in rows]);Rb=G['regular_core']['Rb']
plt.figure(figsize=(7,4.3));plt.plot(t,r,label='Exact effective-core trajectory');plt.axhline(Rb,ls='--',label='Positive bounce radius');plt.xlabel('Proper-time coordinate');plt.ylabel('Core radius');plt.title('Regular-core bounce dynamics');plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(out/'core_bounce.png',dpi=175);plt.close()
plt.figure(figsize=(7,4.6));
for beta in [160,190]:
 z=np.load(p/'hot_runs'/f'glueball_beta{beta}_L3_Nt8_raw.npz')['operator_timelines'];series=z[:,:,0].mean(axis=1)
 plt.plot(np.arange(len(series))*3+300,series,label=f'beta={beta/10:g} (hot start)',alpha=.9)
plt.xlabel('Monte Carlo sweep');plt.ylabel('Mean fundamental spatial plaquette');plt.title('Kelvin Nt=8 raw Monte Carlo histories');plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(out/'glueball_nt8_histories.png',dpi=175);plt.close()
for beta in [160,190]:
 d=json.loads((p/'hot_runs'/f'glueball_beta{beta}_L3_Nt8.json').read_text());plt.figure(figsize=(7,4.3));
 for label,chan in [('0++','0++'),('E2a','E2a'),('E2b','E2b')]:
  C=d['channels'][chan]['C'];plt.plot(range(len(C)),C,'o-',label=label)
 plt.axhline(0,lw=.8);plt.xlabel('Time separation (steps)');plt.ylabel('Connected correlator');plt.title(f'Nt=8 single-plaquette correlators, beta={beta/10:g}');plt.legend();plt.grid(alpha=.2);plt.tight_layout();plt.savefig(out/f'glueball_correlators_beta{beta}.png',dpi=175);plt.close()
print('Figures:',[x.name for x in out.glob('*.png')])
