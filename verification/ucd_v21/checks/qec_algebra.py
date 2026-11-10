#!/usr/bin/env python3
"""Exact characteristic-two regular-representation test of Section 12.4 polynomials."""
import numpy as np
import json
from pathlib import Path

def mul(g,h):
    i,b,c=g; j,d,e=h
    return ((i+(-j if b else j)+6*b*d)%12,(b+d)%2,(c+e)%3)

G=[(a,b,c) for a in range(12) for b in range(2) for c in range(3)]
ix={g:i for i,g in enumerate(G)}
identity=(0,0,0); x=(0,1,0); y=(0,0,1)
def power(g,n):
    h=identity
    for _ in range(n):h=mul(h,g)
    return h

def poly(*terms):
    d={}
    for gg in terms:d[gg]=d.get(gg,0)^1
    return {g for g,b in d.items() if b}
A=poly(identity,power(x,2),mul(power(x,4),y),mul(power(x,8),power(y,2)))
B=poly(y,power(x,3),mul(power(x,5),power(y,2)),power(x,7))
def mat(terms):
    R=np.zeros((72,72),dtype=np.uint8)
    for c,g in enumerate(G):
        for h in terms:R[ix[mul(h,g)],c]^=1
    return R
MA=mat(A); MB=mat(B)
HX=np.hstack((MA,MB)); HZ=np.hstack((MB.T,MA.T))

def row_ints(m):
    return [sum((int(v)<<k) for k,v in enumerate(row) if v) for row in m]
def rank(m):
    piv={}
    for v in row_ints(m):
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return len(piv)

assert len(G)==72
assert not np.any((MA@MB+MB@MA)%2)
assert not np.any((HX@HZ.T)%2)
rX=rank(HX);rZ=rank(HZ);k=144-rX-rZ
result={"group_order":72,"simplified_A_terms":[str(g) for g in sorted(A)],"simplified_B_terms":[str(g) for g in sorted(B)],"row_weight_A":int(MA[0].sum()),"row_weight_B":int(MB[0].sum()),"rank_A":rank(MA),"rank_B":rank(MB),"rank_HX":rX,"rank_HZ":rZ,"logical_qubits":k,"commutator_zero":True,"css_commuting":True,"n":144,"claimed_ranks":66,"claimed_k":12}
print(json.dumps(result,indent=2))
Path(__file__).resolve().parents[1].joinpath('results/qec_poly_algebra.json').write_text(json.dumps(result,indent=2))

# Small-weight logical search in the exact stabilizer quotient.
from itertools import combinations
piv={}
for v in row_ints(HZ):
    while v:
        p=v.bit_length()-1
        if p in piv:v^=piv[p]
        else:piv[p]=v;break

def in_stab(v):
    while v:
        p=v.bit_length()-1
        if p in piv:v^=piv[p]
        else:return False
    return True
cols=[sum((int(v)<<r) for r,v in enumerate(HX[:,c]) if v) for c in range(144)]
zero=[]
for i,c in enumerate(cols):
    if not c and not in_stab(1<<i):zero.append((i,))
seen={}
for i,j in combinations(range(144),2):
    s=cols[i]^cols[j]
    if s==0 and not in_stab((1<<i)|(1<<j)):zero.append((i,j))
    if s in seen:
        p,q=seen[s]
        candidate=(1<<i)|(1<<j)|(1<<p)|(1<<q)
        if candidate.bit_count()==4 and not in_stab(candidate):
            zero.append((p,q,i,j)); break
    else:seen[s]=(i,j)
print('logical_weight_at_most_4=',zero[:3])
result['explicit_logical_weight_le4']=zero[:3]
Path(__file__).resolve().parents[1].joinpath('results/qec_poly_algebra.json').write_text(json.dumps(result,indent=2))
from collections import defaultdict
pairs=defaultdict(list)
for i,j in combinations(range(144),2):
    pairs[cols[i]^cols[j]].append((i,j))
triple_syndromes={}
witness=None
counter={'searched_triples':0,'collisions':0}
for i,j,kidx in combinations(range(144),3):
    cnt=cols[i]^cols[j]^cols[kidx]
    counter['searched_triples']+=1
    if cnt in pairs:
        for p,q in pairs[cnt]:
            v=(1<<i)|(1<<j)|(1<<kidx)|(1<<p)|(1<<q)
            if v.bit_count()==5 and not in_stab(v):
                witness=sorted({i,j,kidx,p,q});break
        if witness:break
    if cnt in triple_syndromes:
        p,q,r=triple_syndromes[cnt]
        v=(1<<i)|(1<<j)|(1<<kidx)|(1<<p)|(1<<q)|(1<<r)
        counter['collisions']+=1
        if v.bit_count()==6 and not in_stab(v):
            witness=sorted({i,j,kidx,p,q,r});break
    else: triple_syndromes[cnt]=(i,j,kidx)
print('logical_weight_le6_witness',witness,'counter',counter)
result['weight_le6_witness']=witness
result['weight_le6_test_stats']=counter
Path(__file__).resolve().parents[1].joinpath('results/qec_poly_algebra.json').write_text(json.dumps(result,indent=2))
# A separating dual functional gives a finite certificate of nontriviality.
rref={p:v for p,v in piv.items()}
for p in sorted(rref):
    for q in sorted(rref):
        if q < p and ((rref[p] >> q)&1):rref[p]^=rref[q]
free=sorted(set(range(144))-set(rref))
v=sum(1<<i for i in [0,1,36,74,75])
sep=[]
for f in free:
    zz=1<<f
    for p,rr in rref.items():
        if (rr >> f)&1:zz |=1<<p
    if (v&zz).bit_count()%2:
        if all((zz & r).bit_count()%2==0 for r in row_ints(HZ)):
            sep.append(zz)
sep.sort(key=int.bit_count)
if sep:
    z=sep[0]
    print('dual_separation_weight',z.bit_count(),'support',[i for i in range(144) if (z>>i)&1],'dot', (z&v).bit_count()%2)
    result['dual_witness_support']=[i for i in range(144) if (z>>i)&1]
    result['logical_witness_weight5']=[0,1,36,74,75]
    Path(__file__).resolve().parents[1].joinpath('results/qec_poly_algebra.json').write_text(json.dumps(result,indent=2))
np.savez_compressed(Path(__file__).resolve().parents[1]/'results/Dic6_C3_144_12_5_matrices.npz', Hx=HX, Hz=HZ, labels=np.array(G,dtype=np.int16))
