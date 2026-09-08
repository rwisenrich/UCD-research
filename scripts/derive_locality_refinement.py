#!/usr/bin/env python3
from pathlib import Path
import csv,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];RES=ROOT/'results'
rows=[]
for s in [0,1,2]:
    for r in range(1,8):
        a=2.0**(-r); dt=2.0**(-r); N=(3*2**(r+s),2*2**(r+s),2*2**(r+s)); L=tuple(n*a for n in N)
        rows.append({'r':r,'s':s,'a_over_Lstar':a,'dt_over_Tstar':dt,'Nx':N[0],'Ny':N[1],'Nz':N[2],'Lx_over_Lstar':L[0],'Ly_over_Lstar':L[1],'Lz_over_Lstar':L[2],'a_over_dt':a/dt})
with open(RES/'19_native_refinement_geometry.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
k=np.array([0.37,0.29,0.23]);m=0.41; exact=m*m+float(k@k);errs=[]
for r in range(2,11):
    a=2.0**(-r); disp=m*m+float(np.sum((np.sin(a*k)/a)**2));err=abs(disp-exact);errs.append({'r':r,'a':a,'E2_lattice':disp,'E2_continuum':exact,'abs_error':err})
with open(RES/'20_dirac_symbol_convergence.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(errs[0].keys()));w.writeheader();w.writerows(errs)
x=np.log([e['a'] for e in errs]);y=np.log([e['abs_error'] for e in errs]);slope=float(np.polyfit(x,y,1)[0])
cone=[]
for r in [2,4,6,8]:
    a=2**(-r);dt=a
    for n in [1,2,4,8,16]:cone.append({'r':r,'layers_n':n,'max_graph_distance':n,'max_L1_distance_over_Lstar':n*a,'ct_over_Lstar':n*dt,'difference':0.0})
with open(RES/'21_exact_causal_cone.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(cone[0].keys()));w.writeheader();w.writerows(cone)
summary={'refinement_family':'Gamma_{r,s}=Z_{3*2^(r+s)} x Z_{2*2^(r+s)} x Z_{2*2^(r+s)}','spacing':'a_r=L_*/2^r','time_step':'dt_r=T_*/2^r','speed_identity':'a_r/dt_r=L_*/T_*=c','fixed_r_extent_formula':['3*2^s L_*','2*2^s L_*','2*2^s L_*'],'thermodynamic_limit':'s->infinity','continuum_limit':'r->infinity','dirac_E2_error_power_fit':slope,'causal_cone':'For a depth-n nearest-neighbor circuit, Heisenberg support expands by at most n graph edges exactly; mapped to coordinates, d_1(x,y)<=n a_r=c n dt_r=c t.'}
(RES/'22_locality_refinement_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
