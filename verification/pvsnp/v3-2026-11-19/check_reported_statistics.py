#!/usr/bin/env python3
"""Audit arithmetic of reported UCD v3 summary only; no solver replay."""
import json
rows = [
 (75,320,10,9,10,436,88,6.5,14.1,0.8),
 (100,427,9,3,10,1035,1890,153.2,132.7,1.4),
 (150,640,10,0,9,18706,11192,251.3,301.1,2.8),
 (200,853,10,3,10,4760,4367,126.4,184.8,2.8),
]
assert [sum(r[i] for r in rows) for i in [2,3,4]] == [39,15,39]
assert all(abs(m/n-4.267)<0.005 for n,m,*_ in rows)
out=[]
for n,m,w,f,h,wflip,hflip,wms,hms,rem in rows:
 out.append({'n':n,'flips_change_percent':round(100*(hflip/wflip-1),1),
             'time_change_percent':round(100*(hms/wms-1),1),
             'mean_clause_satisfaction_percent':round(100*(1-rem/m),3)})
assert [x['flips_change_percent'] for x in out] == [-79.8,82.6,-40.2,-8.3]
assert [x['time_change_percent'] for x in out] == [116.9,-13.4,19.8,46.2]
assert out[2]['mean_clause_satisfaction_percent']<99.6
print(json.dumps({'status':'PASS reported arithmetic only','cases':40,
 'walksat_solved':39,'flow_solved':15,'hybrid_solved':39,'details':out,
 'does_not_check':['the original solver','source CNFs','P versus NP']},indent=2))
