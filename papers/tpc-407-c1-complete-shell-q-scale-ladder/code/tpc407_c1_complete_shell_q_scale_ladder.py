#!/usr/bin/env python3
"""Exact Q-scale ladder for the TPC-406 complete-shell proxy entry."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
PROJECT=Path(__file__).resolve().parents[1]
RESULT=PROJECT/"results/tpc407_certificate.json"
SCHEMA="TPC407_C1_COMPLETE_SHELL_Q_SCALE_LADDER_V1"
STATUS="PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_LADDER"
Q_SCALES=(4096,8192,16384,32768); H=66; N=264; B=1_000_000
EXPECTED_COUNTS=(464,872,1612,3030)
class Failure(ValueError): pass
def need(c,m):
    if type(c) is not bool or not c: raise Failure(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))+"\n").encode()
def no_duplicates(pairs):
    out={}
    for k,v in pairs: need(k not in out,"duplicate key");out[k]=v
    return out
def no_constants(v): raise Failure("non-finite JSON constant")
def primes(limit):
    f=bytearray(b"\1")*(limit+1);f[:2]=b"\0\0"
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b"\0"*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def crt(residues,moduli):
    period=math.prod(moduli)
    return sum(r*(period//p)*pow(period//p,-1,p) for r,p in zip(residues,moduli))%period,period
def txt(x): return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def shell_for(Q):
    shell=[p for p in primes(2*Q) if p>Q]
    need(len(shell)%2==0,"even shell");return shell
def row(Q,shell):
    residues=[0 if i%2==0 else -N for i in range(len(shell))]
    residue,period=crt(residues,shell);origin=residue+((B-residue)//period+1)*period
    t=lambda d:Fraction(H*H,H*H+d*d)
    S0=sum((t(d)**2 for d in range(1,N)),Fraction(0));S1=sum((t(d)**2 for d in range(1,N-1)),Fraction(0))+t(1)**2
    aa=[Fraction(p**3,Q*Q*(p-1)) for p in shell]
    vm=sum((a*a for a in aa[1::2]),Fraction(0));vp=sum((a*a for a in aa[::2]),Fraction(0));pm=sum(aa[1::2],Fraction(0));amin=min(aa)
    g0=vm*S0;g1=vm*S1+vp*(S1-t(1)**2);direct=t(1)*pm;z2=direct*direct/(g0*g1);sharp2=t(1)**2/(amin*amin*S0*S1);coarse2=Fraction(16,H*H)
    need(origin>B and g0>0 and g1>0 and z2<=sharp2<=coarse2,"bound")
    return {"Q":Q,"H":H,"N":N,"m":len(shell)//2,"shell_count":len(shell),"origin_lower_bound":B,
            "selected_primes":shell,"residues":residues,"crt_residue":residue,"crt_period":period,"origin":origin,
            "S0":txt(S0),"S1":txt(S1),"a_min":txt(amin),"P_minus":txt(pm),"V_minus":txt(vm),"V_plus":txt(vp),"G0":txt(g0),"G1":txt(g1),"direct":txt(direct),"normalized_square":txt(z2),"sharp_bound_square":txt(sharp2),"coarse_bound_square_4_over_H":txt(coarse2),"uniform_bound_exact":True,"normalized_float64_observation":f"{math.sqrt(float(z2)):.15f}","H_times_normalized_float64_observation":f"{H*math.sqrt(float(z2)):.15f}"}
def payload():
    shells=[shell_for(Q) for Q in Q_SCALES]
    need(tuple(len(s) for s in shells)==EXPECTED_COUNTS,"shell census")
    return {"schema":SCHEMA,"status":STATUS,"Q_scales":list(Q_SCALES),"H":H,"N":N,"origin_lower_bound":B,"shell_rule":"all primes Q<p<=2Q with even shell cardinality","shell_counts":list(EXPECTED_COUNTS),"shell_sha256":{str(Q):hashlib.sha256(canonical(s)).hexdigest() for Q,s in zip(Q_SCALES,shells)},"window_rule":"N=264=4H","normalization":"complete-shell local diagonal","theorem_domain":{"H_and_N":"fixed integers H=66,N=264 with N=4H","Q_and_shell":"Q>N and an even complete prime shell Q<p<=2Q with 2m primes","profile":"all shell primes, indexed increasingly; even i residue 0, odd i residue -N","origin":"o is a CRT solution above the declared origin lower bound","proxy":"complete-shell masked local geometry from TPC-404"},"theorem":{"exact_sharp_bound":"0<=z<=t1/(a_min*sqrt(S0*S1))","coarse_uniform_bound":"z<=4/(a_min*H)<=4/H","proof_steps":["P_minus^2<=m*V_minus","G1>=V_minus*S1","V_minus>=m*a_min^2","S0>=H/4","S1>=H/4","a_min>=1"],"scope":"one adjacent normalized proxy entry across a finite Q scale ladder, not the full operator"},"cases":[row(Q,s) for Q,s in zip(Q_SCALES,shells)],"claim_firewall":{"COMPLETE_SHELL_Q_SCALE_LADDER":"PROVED_EXACT_FINITE","SCALE_LADDER_DECIMALS":"NUMERICAL_OBSERVATION","FULL_OPERATOR_NORM":"OPEN","NORMALIZED_GROWING_THEOREM":"OPEN","ARITHMETIC_SIGN_IDENTIFICATION":"OPEN","ARITHMETIC_ADVANCE":"NO","FIXED_POWER_CREDIT":0,"FULL_GATE_B":"OPEN","TWIN_PRIME_RESULT":"NONE"},"round2_clue":"TEST_C1_COMPLETE_SHELL_Q_SCALE_EXTENSION"}
def write():
    p=payload();RESULT.write_bytes(canonical({"certificate_version":1,"claim_status":STATUS,"payload":p,"payload_sha256":hashlib.sha256(canonical(p)).hexdigest()}))
def check_document(d):
    need(type(d) is dict and set(d)=={"certificate_version","claim_status","payload","payload_sha256"},"document");need(type(d["certificate_version"]) is int and d["certificate_version"]==1,"version");need(d["claim_status"]==STATUS,"claim status");need(d["payload_sha256"]==hashlib.sha256(canonical(d["payload"])).hexdigest(),"digest");need(canonical(d["payload"])==canonical(payload()),"exact Q ladder")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--write",action="store_true");ap.add_argument("--check",action="store_true");a=ap.parse_args()
    if a.write: write();print("TPC407_CERTIFICATE=WRITTEN")
    elif a.check: check_document(json.loads(RESULT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants));print("TPC407_CERTIFICATE=PASS cases=4 q_scales=4 complete_shell=PASS")
    else: raise SystemExit("explicit --check or --write required")
if __name__=="__main__":main()
