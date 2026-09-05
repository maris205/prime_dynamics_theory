#!/usr/bin/env python3
"""TPC-402: exact finite audit of the signed diagonal-deletion coefficient."""
from __future__ import annotations
import argparse, hashlib, json, math
from fractions import Fraction
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]; RESULT=PROJECT/'results/tpc402_certificate.json'
SCHEMA='TPC402_C1_SIGNED_DIAGONAL_TERM_AUDIT_V1'; STATUS='PROVED_EXACT_FINITE_SIGNED_DIAGONAL_TERM_AUDIT'
Q,N,H=8192,1024,66; ORIGINS=(7600001,7603209,7606417,7609625,7612833,7616041); POS=(0,1,512,1022,1023)
class Failure(ValueError): pass
def need(c,m):
    if type(c) is not bool or not c: raise Failure(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def primes(limit):
    f=bytearray(b'\1')*(limit+1); f[:2]=b'\0\0'
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def audit():
    ps=[p for p in primes(2*Q) if p>Q]; need(len(ps)==872,'shell')
    laws={'all_plus':lambda i:1,'alternating_index':lambda i:1 if i%2==0 else -1}
    counts={k:0 for k in laws}; total=0; comparisons=0; diagonal_zero=0
    for law,sgn in laws.items():
        aa=[Fraction(p**3,Q**2*(p-1))*sgn(i) for i,p in enumerate(ps)]; A=sum(aa,Fraction(0))
        for o in ORIGINS:
            for x in POS:
                u=o+x
                bu=sum((w for w,p in zip(aa,ps) if u%p==0),Fraction(0))
                for y in POS:
                    v=o+y
                    if u==v: diagonal_zero+=1; continue
                    bv=sum((w for w,p in zip(aa,ps) if v%p==0),Fraction(0))
                    k=Fraction(H*H,H*H+(u-v)*(u-v)); direct=Fraction(0)
                    for w,p in zip(aa,ps):
                        if u%p and v%p: direct-=w*k
                    reduced=k*(-A+bu+bv)
                    need(direct==reduced,'signed coefficient')
                    counts[law]+=1; total+=1; comparisons+=len(ps)
    return {'Q':Q,'N':N,'H':H,'origins':list(ORIGINS),'positions':list(POS),'shell_cardinality':len(ps),
      'laws':list(laws),'signed_component_rows':total,'signed_component_prime_comparisons':comparisons,'rows_by_law':counts,'diagonal_pairs_skipped':diagonal_zero,
      'all_signed_coefficients_exact':True}
def anchor(): return {'Q':8,'N':13,'p':11,'u':7600001,'v':7600012,'active_masks':True,'difference':-11,'divisibility_indicator':True,'production_condition_holds':False}
def build():
    payload={'schema':SCHEMA,'status':STATUS,'audit':audit(),'anchor_boundary':anchor(),
      'identity':'M_sigma(u,v)=T_uv[-A_sigma+b_sigma(u)+b_sigma(v)] for u != v and N<Q<p',
      'claim_firewall':{'TPC402_ANALYTIC_STRUCTURE':'PROVED_EXACT_FINITE','TPC402_ARITHMETIC_ADVANCE':'NO','TPC402_FIXED_POWER_CREDIT':0,'TPC402_SOURCE_UNIFORM_L2':'OPEN','TPC402_FULL_GATE_B':'OPEN','TPC402_TWIN_PRIME_RESULT':'NONE'},
      'round2_clue':'TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION'}
    doc={'certificate_version':1,'claim_status':STATUS,'payload':payload,'payload_sha256':hashlib.sha256(canonical(payload)).hexdigest()}; RESULT.write_bytes(canonical(doc))
def check(d):
    need(type(d['certificate_version']) is int and d['certificate_version']==1 and d['claim_status']==STATUS,'header')
    need(d['payload_sha256']==hashlib.sha256(canonical(d['payload'])).hexdigest(),'digest'); p=d['payload']; need(p['schema']==SCHEMA and p['status']==STATUS,'schema')
    a=p['audit']; need(a==audit(),'exact audit'); need(p['anchor_boundary']==anchor(),'anchor'); need(p['round2_clue']=='TEST_C1_SIGNED_DIAGONAL_TERM_GROWING_OBSTRUCTION','clue')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--write',action='store_true'); ap.add_argument('--check',action='store_true'); x=ap.parse_args()
    if x.write: build(); print('TPC402_CERTIFICATE=WRITTEN'); return
    if not x.check: raise SystemExit('explicit --check or --write required')
    check(json.loads(RESULT.read_bytes())); print('TPC402_CERTIFICATE=PASS signed_rows=240 prime_comparisons=209280 laws=2 anchor_boundary=PASS')
if __name__=='__main__': main()
