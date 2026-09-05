#!/usr/bin/env python3
"""Independent reverse-order checker for the TPC-401 finite certificate."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-401-c1-diagonal-deletion-decomposition/results/tpc401_certificate.json"
SCHEMA = "TPC401_C1_DIAGONAL_DELETION_DECOMPOSITION_V1"
STATUS = "PROVED_EXACT_FINITE_PRODUCTION_DOMAIN_DIAGONAL_DELETION_AUDIT"

def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))+"\n").encode()
class Failure(ValueError):
    pass

def need(condition, message):
    if type(condition) is not bool or not condition:
        raise Failure(message)

def parse(raw):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out: raise Failure('duplicate key')
            out[k]=v
        return out
    def bad_constant(x): raise Failure('nonfinite '+x)
    d=json.loads(raw,object_pairs_hook=pairs,parse_constant=bad_constant)
    need(raw == canonical(d), 'canonical document')
    return d

def check(d, recompute=True):
    need(type(d['certificate_version']) is int and d['certificate_version']==1 and d['claim_status']==STATUS, 'header')
    p=d['payload']; need(p['schema']==SCHEMA and p['status']==STATUS, 'schema')
    need(d['payload_sha256']==hashlib.sha256(canonical(p)).hexdigest(), 'digest')
    a=p['production_domain']['audit']
    expected={'H':66,'N':1024,'Q':8192,'origins':[7600001,7603209,7606417,7609625,7612833,7616041],
      'shell_cardinality':872,'sampled_offdiagonal_pairs':120,'component_rows':104640,
      'congruence_zero_rows':104640,'component_decomposition_equal_rows':104640,
      'expected_component_rows':104640,'all_sampled_components_equal':True,
      'all_sampled_divisibility_indicators_zero':True}
    need(canonical(a)==canonical(expected),'complete typed census')
    need(p['production_domain']['condition']=='N < Q < p','domain')
    firewall={'TPC401_ANALYTIC_STRUCTURE':'PROVED_EXACT_FINITE', 'TPC401_NUMERICAL_CERTIFICATION':'NONE_NEEDED',
      'TPC401_ARITHMETIC_ADVANCE':'NO','TPC401_FIXED_POWER_CREDIT':0,'TPC401_SOURCE_UNIFORM_L2':'OPEN',
      'TPC401_FULL_GATE_B':'OPEN','TPC401_TWIN_PRIME_RESULT':'NONE'}
    need(canonical(p['claim_firewall'])==canonical(firewall),'firewall')
    need(p['round2_clue']=='TEST_C1_DIAGONAL_DELETION_SIGNED_TERM_AUDIT','clue')
    e=p['exact_anchor_boundary']; u,v=7600001,7600012
    k=Fraction(66**2,66**2+121); scale=Fraction(11**3,8**2)
    direct=scale*k*Fraction(9,10); reduced=-scale*k/10
    boundary={'Q':8,'N':13,'prime':11,'difference':-11,'u':u,'v':v,'unit_masks_active':True,
      'direct':str(direct),'reduced':str(reduced),'nonzero_difference':str(direct-reduced),
      'offdiagonal':True,'divisibility_indicator':True,'decomposition_applicable':False}
    need(canonical(e)==canonical(boundary) and direct != reduced and u%11!=0 and v%11!=0,'active boundary')
    if not recompute: return
    ps=[p0 for p0 in range(16384,8192,-1) if all(p0%d for d in range(2,math.isqrt(p0)+1))]
    need(len(ps)==872,'trial-division shell')
    count=0
    for o in reversed(expected['origins']):
        for x in (1023,1022,512,1,0):
            for y in (1023,1022,512,1,0):
                if x==y: continue
                u,v=o+x,o+y; k=Fraction(4356,4356+(x-y)**2)
                for p0 in ps:
                    scale=Fraction(p0**3,8192**2)
                    active=int(u%p0!=0 and v%p0!=0)
                    literal=scale*k*(int((u-v)%p0==0)-Fraction(1,p0-1))*active
                    reduced=-scale*k*active/Fraction(p0-1)
                    need(literal==reduced and (u-v)%p0!=0,'reverse literal replay')
                    count+=1
    need(count==104640,'reverse census')

def main():
    import sys
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    check(parse(CERT.read_bytes())); print("TPC401_INDEPENDENT_CHECK=PASS component_rows=104640 reverse_trial_division_replay=PASS active_anchor_boundary=PASS")
if __name__ == "__main__": main()
