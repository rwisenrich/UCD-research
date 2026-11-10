#!/usr/bin/env python3
"""Exhaustive weight <= 4 and explicit weight 5 logical witnesses, both CSS sectors."""
import json
from pathlib import Path
from itertools import combinations
import numpy as np
from qec_algebra import HX,HZ,row_ints

def pivots_of(mat):
    piv={}
    for v in row_ints(mat):
        while v:
            p=v.bit_length()-1
            if p in piv:v^=piv[p]
            else:piv[p]=v;break
    return piv

def member(v,p):
    while v:
        j=v.bit_length()-1
        if j in p:v^=p[j]
        else:return False
    return True

def search(check,stabilizer):
    rows,dim=check.shape
    cols=[sum(int(check[i,j])<<i for i in range(rows) if check[i,j]) for j in range(dim)]
    piv=pivots_of(stabilizer)
    found={}; inspected={'w1':0,'w2':0,'w3':0,'w4_pairs':0,'w5':0}
    for i in range(dim):
        inspected['w1']+=1
        if not cols[i] and not member(1<<i,piv):found[1]=[i]
    pairs={}
    for i,j in combinations(range(dim),2):
        inspected['w2']+=1
        s=cols[i]^cols[j]
        if not s and not member((1<<i)|(1<<j),piv):found.setdefault(2,[i,j])
        if s in pairs:
            for p,q in pairs[s]:
                if len({i,j,p,q})<4:continue
                inspected['w4_pairs']+=1
                v=(1<<i)|(1<<j)|(1<<p)|(1<<q)
                if not member(v,piv):found.setdefault(4,[p,q,i,j])
        pairs.setdefault(s,[]).append((i,j))
    for i,j,k in combinations(range(dim),3):
        inspected['w3']+=1
        s=cols[i]^cols[j]^cols[k]
        if not s and not member((1<<i)|(1<<j)|(1<<k),piv):found.setdefault(3,[i,j,k])
        if s in [cols[i],cols[j],cols[k]]:continue
        if s in pairs and 5 not in found:
            for p,q in pairs[s]:
                if len({i,j,k,p,q})<5:continue
                inspected['w5']+=1
                v=sum(1<<a for a in (i,j,k,p,q))
                if not member(v,piv):found.setdefault(5,sorted([i,j,k,p,q]));break
    return {'min_logical_le5':min(found) if found else None,'examples':found,'inspected':inspected}

X=search(HX,HZ)
Z=search(HZ,HX)
r={'X':X,'Z':Z,'distance':min(X['min_logical_le5'],Z['min_logical_le5'])}
assert r['distance']==5
p=Path(__file__).resolve().parents[1]/'results'/'exact_Dic6_144_12_5_certificate.json'
p.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
