#!/usr/bin/env python3
import importlib.util,sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
spec=importlib.util.spec_from_file_location('h',str(Path(__file__).with_name('ucd_504_master_hamiltonian.py')))
h=importlib.util.module_from_spec(spec);sys.modules['h']=h;spec.loader.exec_module(h)
def f(A): return float(np.linalg.norm(A,'fro'))
I24=np.eye(24,dtype=complex); B=h.left_regular((6,0)); Z=np.diag([1 if k<6 else -1 for k,e in h.ELEMS]).astype(complex); G=np.diag([1 if e==0 else -1 for k,e in h.ELEMS]).astype(complex); X=B; Y=-1j*B@Z; PL=(I24-G)/2; PR=I24-PL; W=[PL@Z/2,PL@Y/2,PL@X/2]
checks={'B2':f(B@B-I24),'XZ_anticomm':f(B@Z+Z@B),'weak_su2_12':f(W[0]@W[1]-W[1]@W[0]-1j*W[2]),'weak_su2_23':f(W[1]@W[2]-W[2]@W[1]-1j*W[0]),'weak_su2_31':f(W[2]@W[0]-W[0]@W[2]-1j*W[1]),'right_singlet':max(f(PR@x) for x in W)}
expected={(-1,-1,1):(-1,-.5,-1),(-1,1,1):(0,.5,-1),(1,-1,1):(-1/3,-.5,1/3),(1,1,1):(2/3,.5,1/3),(-1,-1,0):(-1,0,-2),(-1,1,0):(0,0,0),(1,-1,0):(-1/3,0,-2/3),(1,1,0):(2/3,0,4/3)}
for (A,b,L),(q0,t0,y0) in expected.items():
    q=b/2+A/3-1/6; t=L*b/2; y=2*(q-t); checks[f'table_{A}_{b}_{L}']=max(abs(q-q0),abs(t-t0),abs(y-y0))
passed=all(v<1e-10 for v in checks.values()); out={'passed':passed,'n_checks':len(checks),'max_residual':max(checks.values()),'checks':checks}; (RES/'05_independent_native_sm_verifier.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
