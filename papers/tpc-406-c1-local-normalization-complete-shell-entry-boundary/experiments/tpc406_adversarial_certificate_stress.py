#!/usr/bin/env python3
"""Strict contract mutation tests for TPC-406."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CERT=ROOT/"papers/tpc-406-c1-local-normalization-complete-shell-entry-boundary/results/tpc406_certificate.json"
SCHEMA="TPC406_C1_LOCAL_NORMALIZATION_COMPLETE_SHELL_ENTRY_BOUNDARY_V1"
STATUS="PROVED_EXACT_FINITE_COMPLETE_SHELL_LOCAL_ENTRY_BOUNDARY"
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))+"\n").encode()
def no_duplicates(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError("duplicate key")
        out[k]=v
    return out
def no_constants(v): raise ValueError("non-finite constant")
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def validate(d):
    need(type(d) is dict and set(d)=={"certificate_version","claim_status","payload","payload_sha256"},"document")
    need(type(d["certificate_version"]) is int and d["certificate_version"]==1 and d["claim_status"]==STATUS,"header")
    p=d["payload"]; need(d["payload_sha256"]==hashlib.sha256(canonical(p)).hexdigest(),"digest")
    need(p.get("schema")==SCHEMA and p.get("status")==STATUS,"status")
    need(p.get("shell_rule")=="all primes Q<p<=2Q" and p.get("shell_count")==872,"shell")
    need(p.get("window_rule")=="N=4H","window")
    need(p.get("theorem",{}).get("coarse_uniform_bound")=="z<=4/(a_min*H)<=4/H","bound")
    need(p.get("claim_firewall",{}).get("FULL_OPERATOR_NORM")=="OPEN","operator firewall")
    cases=p.get("cases"); need(type(cases) is list and len(cases)==5,"case census")
    need([c.get("H") for c in cases]==[16,32,66,128,256],"heights")
    need(all(c.get("m")==436 and c.get("shell_count")==872 and c.get("uniform_bound_exact") is True for c in cases),"case contract")
def main():
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    original=json.loads(CERT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants); validate(original)
    mutations=("shell_rule","shell_count","window_rule","bound","full_operator","case_count","magnitude","height")
    rejected=0
    for mutation in mutations:
        d=copy.deepcopy(original); p=d["payload"]
        if mutation=="shell_rule": p["shell_rule"]="first 8 shell primes"
        elif mutation=="shell_count": p["shell_count"]=8
        elif mutation=="window_rule": p["window_rule"]="N=H"
        elif mutation=="bound": p["theorem"]["coarse_uniform_bound"]="z<=8/H"
        elif mutation=="full_operator": p["claim_firewall"]["FULL_OPERATOR_NORM"]="PROVED"
        elif mutation=="case_count": p["cases"]=p["cases"][:-1]
        elif mutation=="magnitude": p["cases"][0]["m"]=4
        else: p["cases"][0]["H"]=15
        d["payload_sha256"]=hashlib.sha256(canonical(p)).hexdigest()
        try: validate(d)
        except ValueError: rejected+=1
    need(rejected==len(mutations),"mutation escaped")
    print(f"TPC406_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")
if __name__=="__main__": main()
