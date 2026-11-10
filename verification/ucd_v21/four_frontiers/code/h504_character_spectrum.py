"""Reproduce H504 bright-sector Schur spectrum from frozen v17 original workbench source."""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'source/v17_h504'))
import original_h504_master_hamiltonian as m

def main():
  P24=sum(m.left_regular((2*j,0)) for j in range(6))/6
  Q24=np.eye(24)-P24
  M24=np.zeros((24,24),complex)
  for g in [(0,0),(1,0),(0,1),(1,1)]:M24[m.IDX[g],m.IDX[g]]=1
  B24=6/np.sqrt(5)*Q24@M24@P24
  E24=B24@B24.conj().T
  evals,vec=np.linalg.eigh((E24+E24.conj().T)/2)
  Ub=np.kron(np.eye(21),vec[:,np.argsort(evals)[-4:]])
  H7=m.build_H504();K=np.kron(np.eye(21),B24+B24.conj().T)
  H0=H7+8*np.eye(504)+0.1*K
  assert np.linalg.eigvalsh(H0)[0]>0
  W=Ub.conj().T@np.linalg.solve(H0,Ub);W=(W+W.conj().T)/2
  eig=np.linalg.eigvalsh(W).real
  assert eig.min()>0
  out={'source':'v17 original_h504_master_hamiltonian.py; 8I shift, 0.1 Dic6 mixing','bright_dim':84,'W_min':float(eig.min()),'W_max':float(eig.max()),'trace_W':float(eig.sum()),'trace_W2':float(np.dot(eig,eig)),'trace_W3':float(np.sum(eig**3)),'eta':.0001}
  (ROOT/'results/h504_character_spectrum.json').write_text(json.dumps(out,indent=2));np.save(ROOT/'results/h504_W_eigenvalues.npy',eig)
  print(json.dumps(out,indent=2))
if __name__=='__main__':main()
