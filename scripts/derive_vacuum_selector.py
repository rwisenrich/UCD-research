#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,sys,csv,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]; RES=ROOT/'results'
spec=importlib.util.spec_from_file_location('h504',str(Path(__file__).with_name('ucd_504_master_hamiltonian.py')))
h=importlib.util.module_from_spec(spec);sys.modules['h504']=h;spec.loader.exec_module(h)
def fro(A): return float(np.linalg.norm(A,'fro'))
unused=set(h.ELEMS); classes=[]
while unused:
    g=next(iter(unused)); cl=set()
    for q in h.ELEMS:
        cl.add(h.dic6_mul(h.dic6_mul(q,g),h.dic6_inv(q)))
    classes.append(sorted(cl)); unused-=cl
classes.sort(key=lambda c:(len(c),c))
H=h.build_H504(); vals,vecs=np.linalg.eigh(H); E0=vals[0]; idx=np.where(np.abs(vals-E0)<1e-9)[0]; V=vecs[:,idx]
I7=np.eye(7);I3=np.eye(3)
rows=[]; restr=[]
for j,cl in enumerate(classes):
    Z=sum(h.right_regular(g) for g in cl)/len(cl)
    Z504=np.kron(np.kron(I7,I3),Z)
    M=V.conj().T@Z504@V; M=(M+M.conj().T)/2
    ev=np.linalg.eigvalsh(M)
    restr.append(M)
    rows.append({'class_id':j,'class_size':len(cl),'elements':str(cl),'ground_eig_1':float(ev[0]),'ground_eig_2':float(ev[-1]),'splitting':float(ev[-1]-ev[0])})
with open(RES/'13_vacuum_selector_conjugacy_classes.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
Mcols=[]
for M in restr:
    Mcols.append(np.concatenate([M.real.reshape(-1),M.imag.reshape(-1)]))
span_dim=int(np.linalg.matrix_rank(np.column_stack(Mcols),tol=1e-9))
Sx24=sum(h.right_regular((k,1)) for k in range(12))/12
Sx=np.kron(np.kron(I7,I3),Sx24)
Sg=(V.conj().T@Sx@V); Sg=(Sg+Sg.conj().T)/2
sgev=np.linalg.eigvalsh(Sg)
tau=1/72
sel=[]
for sigma in (1,-1):
    Hs=H-tau*sigma*Sx
    e,U=np.linalg.eigh(Hs); e0=e[0]; ids=np.where(np.abs(e-e0)<1e-9)[0]
    psi=U[:,0]
    sel.append({'sigma':sigma,'ground_energy':float(e0),'ground_multiplicity':len(ids),'gap_to_next':float(e[len(ids)]-e0),'Sx_expectation':float(np.vdot(psi,Sx@psi).real),'orientation_residual':float(abs(np.vdot(psi,Sx@psi).real-sigma))})
with open(RES/'14_vacuum_selector_ground_selection.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(sel[0].keys()));w.writeheader();w.writerows(sel)
summary={'default_ground_energy':float(E0),'default_ground_multiplicity':len(idx),'central_class_count':len(classes),'restricted_center_real_Hermitian_span_dimension':span_dim,'Sx_ground_eigenvalues':[float(x) for x in sgev],'Sx2_minus_I_on_ground':fro(Sg@Sg-np.eye(len(idx))),'selector_functional':'S_sel=(tau/2)<psi|(Sx-sigma I)^2|psi> = tau - tau sigma <Sx> on the ground doublet','effective_selector':'H_sel=-tau sigma Sx up to an additive constant','selected':sel}
(RES/'15_vacuum_selector_theorem.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
