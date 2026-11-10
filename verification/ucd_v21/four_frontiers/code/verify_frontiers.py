"""Independent deterministic multi-frontier verification and source-to-output checks."""
from pathlib import Path
import sys,json,itertools
from fractions import Fraction
import numpy as np
from kelvin import geometry,V,W,WEIGHTS
from glueball_nt8 import trace_plaq
from qec_144_subsystem import rank_and_indices,basis_masks,in_span,list2mask
from gravity_spin2_bounce import run as gravity_run

ROOT=Path(__file__).resolve().parents[1];RESULTS=ROOT/'results'
passed=[]
def check(name,truth):
    assert truth,name
    passed.append(name)

def su3(rng):
    x=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));q,r=np.linalg.qr(x)
    q=q@np.diag(np.diag(r)/np.abs(np.diag(r)));q[:,0]/=np.linalg.det(q)
    return q

def main():
    g=geometry(3,8);N=g['n_sites'];check('432 actual BCC spacetime sites',N==432)
    check('3456 SU3 link variables',g['n_links']==3456)
    check('12096 weighted 4-link plaquettes',g['n_plaquettes']==12096)
    check('exact 28 faces per vertex',g['n_plaquettes']==28*N)
    check('exact per-cell weight 14/3',sum(WEIGHTS.values())==Fraction(14,3))
    # Gauge transformation on arbitrary SU(3) links, complete 12096-plaquette test.
    rng=np.random.default_rng(20261110);links=np.array([su3(rng) for _ in range(g['n_links'])]);G=np.array([su3(rng) for _ in range(N)])
    tr=np.empty_like(links)
    for x in range(N):
        for d in range(8):tr[8*x+d]=G[x]@links[8*x+d]@G[g['plus'][x,d]].conj().T
    maxerr=0.
    for f in g['pla']:
        maxerr=max(maxerr,abs(trace_plaq(links,f)-trace_plaq(tr,f)))
    check('full non-Abelian gauge invariance across all plaquettes',maxerr<2e-12)
    # Local DeltaS recomputation versus direct full action difference.
    e=387;link2=links.copy();link2[e]=su3(rng)@link2[e]
    all_old=sum(w*trace_plaq(links,f) for w,f in zip(g['pw'],g['pla']))
    all_new=sum(w*trace_plaq(link2,f) for w,f in zip(g['pw'],g['pla']))
    adj=g['adj'][e];adj=adj[adj>=0];local=sum(g['pw'][j]*(trace_plaq(link2,g['pla'][j])-trace_plaq(links,g['pla'][j])) for j in adj)
    check('Metropolis local action change equals full Wilson action change',abs((all_new-all_old)-local)<1e-10)
    # Full E/M BCC bivector isotropy.
    d=np.vstack([np.array([[1,0,0,0.]]),np.column_stack([np.zeros(7),V/2.])]);pairs=list(itertools.combinations(range(4),2));M=np.zeros((6,6))
    for (r,s),w in WEIGHTS.items():
        f=np.array([d[r,i]*d[s,j]-d[r,j]*d[s,i] for i,j in pairs]);M+=float(w)*np.outer(f,f)
    check('exact SO4 quadratic bivector identity',np.max(np.abs(M-0.5*np.eye(6)))<1e-14)
    ev=json.loads((RESULTS/'electroweak_chiral.json').read_text())
    check('SU2 doublet Wilson covariance',ev['sectors']['left_weak_doublet']['wilson_gauge_covariance_fro']<1e-10)
    check('SU2 doublet overlap covariance',ev['sectors']['left_weak_doublet']['overlap_gauge_covariance_fro']<1e-8)
    check('weak-doublet GW identity',ev['sectors']['left_weak_doublet']['gw_fro']<1e-8)
    check('U1 singlet overlap covariance',ev['sectors']['right_charged_singlet']['overlap_gauge_covariance_fro']<1e-8)
    check('U1 singlet GW identity',ev['sectors']['right_charged_singlet']['gw_fro']<1e-8)
    check('all four chiral anomalies cancel',all(v=='0' for k,v in ev['anomalies'].items() if k!='left_SU2_doublets_three_generations'))
    check('even number of SU2 doublets',ev['anomalies']['left_SU2_doublets_three_generations']%2==0)
    gr=gravity_run();check('rank-two TT projector',gr['spin2']['TT_dimension']==2)
    check('TT projector idempotence',gr['spin2']['TT_projector_max_residual']<1e-12)
    check('fourth-order improvement factor',abs(gr['spin2']['ratio_fourth'][-2]-16)<.1)
    check('regular-core bounce first integral',max(abs(x['first_integral_residual']) for x in gr['regular_core']['trajectory'])<1e-12)
    q=json.loads((RESULTS/'qec_distance12_concatenated.json').read_text());n=q['concatenated']['n']
    check('native Q72 CSS exact rank54+54',q['outer']['HX_rank']==q['outer']['HZ_rank']==54)
    check('native Q72 CSS d4 exact enumeration',q['outer']['d']==4 and q['outer']['complete_search_X_weight_lt4']==497784)
    check('Shor inner d3',q['inner']['n']==9 and q['inner']['d']==3)
    check('CSS concatenation 1296,36,12',n==1296 and q['concatenated']['k']==36 and q['concatenated']['d_lower_from_product']==q['concatenated']['d_upper_from_witness']==12)
    check('concatenated rank342+918',q['concatenated']['HX_rank']==342 and q['concatenated']['HZ_rank']==918)
    check('concatenated stabilizer commutation',q['concatenated']['orthogonal'])
    # Test raw MC block shape, Wilson scalar order of magnitude, Nt=8 sample number.
    sims={}
    for beta in [160,190]:
        name=f'glueball_beta{beta}_L3_Nt8'
        raw=np.load(RESULTS/'hot_runs'/f'{name}_raw.npz')['operator_timelines']
        sim=json.loads((RESULTS/'hot_runs'/f'{name}.json').read_text())
        check(f'Nt8 SU3 beta{beta//10} independent raw trajectory',raw.shape==(80,8,3) and np.all(np.isfinite(raw)))
        multi=np.load(RESULTS/f'multi_beta{beta}_L3_Nt8_raw.npz')['operator_timelines']
        check(f'Nt8 beta{beta//10} four-representation raw channels',multi.shape==(80,8,12) and np.all(np.isfinite(multi)))
        sims[name]={'scalar_mean':float(np.mean(raw[:,:,0])),'scalar_first_half':float(np.mean(raw[:40,:,0])),'scalar_last_half':float(np.mean(raw[40:,:,0])),'tensor_E2a_C1':sim['channels']['E2a']['C'][1], 'effective_scalar_tau1':sim['channels']['0++']['effective_mass_tau1'],'effective_tensor_tau1':sim['channels']['E2a']['effective_mass_tau1']}
    spect=np.load(RESULTS/'h504_W_eigenvalues.npy')
    check('all H504 Schur eigenvalues positive',len(spect)==84 and float(np.min(spect))>0)
    check('H504 Schur trace matches exact workbench',abs(float(np.sum(spect))-11.04707592532283)<1e-9)
    check('H504 quadratic trace matches workbench',abs(float(np.sum(spect*spect))-1.519011346657387)<1e-9)
    out={'passed':len(passed),'failed':0,'checks':passed,'max_su3_plaquette_gauge_error':maxerr,'Metropolis_exact_action_difference_residual':float(abs((all_new-all_old)-local)),'bivector_6x6_error':float(np.max(np.abs(M-.5*np.eye(6)))),'simulations':sims}
    (RESULTS/'frontier_verification_summary.json').write_text(json.dumps(out,indent=2));print(json.dumps({'passed':len(passed),'max_gauge_err':maxerr,'simulations':sims},indent=2))
if __name__=='__main__':main()
