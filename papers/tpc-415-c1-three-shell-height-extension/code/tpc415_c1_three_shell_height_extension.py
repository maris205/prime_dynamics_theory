#!/usr/bin/env python3
"""Exact four-height replay for the three-shell pooled TPC proxy."""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
PROJECT=Path(__file__).resolve().parents[1]; RESULT=PROJECT/'results/tpc415_certificate.json'; SCHEMA='TPC415_C1_THREE_SHELL_HEIGHT_EXTENSION_V1'; STATUS='PROVED_EXACT_FINITE_THREE_SHELL_HEIGHT_EXTENSION'; QS,HEIGHTS,B=(65536,131072,262144),(16,32,66,128),1_000_000; COUNTS=(5709,10749,20390)
class Failure(ValueError): pass
def need(c,m):
    if type(c)is not bool or not c: raise Failure(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def nodup(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def noconst(v): raise Failure('non-finite JSON constant')
def primes(limit):
    f=bytearray(b'\1')*(limit+1); f[:2]=b'\0\0'
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def crt(rs,ms):
    period=math.prod(ms); return sum(r*(period//p)*pow(period//p,-1,p) for r,p in zip(rs,ms))%period,period
def txt(v): return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def shells():
    out=[]
    for q,n in zip(QS,COUNTS):
        s=[p for p in primes(2*q) if p>q]; need(len(s)==n,'shell census'); out.extend((p,q) for p in s)
    return out
def row(h,items):
    ps=[p for p,_ in items]; qs=[q for _,q in items]; N=4*h; need(min(ps)>N and len(ps)%2==0,'domain'); rs=[0 if i%2==0 else -N for i in range(len(ps))]; residue,period=crt(rs,ps); origin=residue+((B-residue)//period+1)*period; t=lambda d:Fraction(h*h,h*h+d*d); s0=sum((t(d)**2 for d in range(1,N)),Fraction(0)); s1=sum((t(d)**2 for d in range(1,N-1)),Fraction(0))+t(1)**2; aa=[Fraction(p**3,q*q*(p-1)) for p,q in items]; minus,plus=aa[1::2],aa[::2]; vm=sum((a*a for a in minus),Fraction(0)); vp=sum((a*a for a in plus),Fraction(0)); pm=sum(minus,Fraction(0)); amin=min(aa); g0=vm*s0; g1=vm*s1+vp*(s1-t(1)**2); direct=t(1)*pm; z2=direct*direct/(g0*g1); sharp=t(1)**2/(amin*amin*s0*s1); coarse=Fraction(16,h*h); need(origin>B and z2<=sharp<=coarse,'bound')
    return {'H':h,'N':N,'m_minus':len(minus),'m_plus':len(plus),'shell_count':len(ps),'shell_counts':list(COUNTS),'Q_scales':list(QS),'origin_lower_bound':B,'selected_primes':ps,'prime_shell_Q':qs,'residues':rs,'crt_residue':residue,'crt_period':period,'origin':origin,'S0':txt(s0),'S1':txt(s1),'a_min':txt(amin),'P_minus':txt(pm),'V_minus':txt(vm),'V_plus':txt(vp),'G0':txt(g0),'G1':txt(g1),'direct':txt(direct),'normalized_square':txt(z2),'sharp_bound_square':txt(sharp),'coarse_bound_square_4_over_H':txt(coarse),'uniform_bound_exact':True,'normalized_float64_observation':f'{math.sqrt(float(z2)):.15f}','H_times_normalized_float64_observation':f'{h*math.sqrt(float(z2)):.15f}'}
def payload():
    items=shells(); return {'schema':SCHEMA,'status':STATUS,'Q_scales':list(QS),'heights':list(HEIGHTS),'origin_lower_bound':B,'shell_rule':'pooled full shells Q<p<=2Q','shell_counts':list(COUNTS),'shell_sha256':{str(q):hashlib.sha256(canonical([p for p,x in items if x==q])).hexdigest() for q in QS},'window_rule':'N=4H','normalization':'pooled complete-shell local diagonal','theorem_domain':{'H_and_N':'fixed integer heights H in {16,32,66,128} with N=4H','Q_and_shell':'three full odd shells Q=65536,131072,262144 pooled without deletion','profile':'pooled primes ordered increasingly; even i residue 0, odd i residue -N','amplitude':'a_i=p_i^3/[Q_i^2(p_i-1)] using each prime declared shell Q_i','parity':'pooled cardinality r=36848 is even, with m_minus=m_plus=18424','origin':'o is a CRT solution above the declared origin lower bound','proxy':'complete-shell masked local geometry from TPC-404'},'theorem':{'exact_sharp_bound':'0<=z<=t1/(a_min*sqrt(S0*S1))','coarse_uniform_bound':'z<=4/(a_min*H)<=4/H','proof_steps':['P_minus^2<=m_minus*V_minus','G1>=V_minus*S1','V_minus>=m_minus*a_min^2','S0>=H/4','S1>=H/4','a_min>=1'],'scope':'one three-shell pooled adjacent normalized proxy entry across four heights, not the full operator'},'cases':[row(h,items) for h in HEIGHTS],'claim_firewall':{'THREE_SHELL_HEIGHT_EXTENSION':'PROVED_EXACT_FINITE','HEIGHT_LADDER_DECIMALS':'NUMERICAL_OBSERVATION','FULL_OPERATOR_NORM':'OPEN','NORMALIZED_GROWING_THEOREM':'OPEN','ARITHMETIC_SIGN_IDENTIFICATION':'OPEN','ARITHMETIC_ADVANCE':'NO','FIXED_POWER_CREDIT':0,'FULL_GATE_B':'OPEN','TWIN_PRIME_RESULT':'NONE'},'round2_clue':'TEST_C1_THREE_SHELL_HEIGHT_EXTENSION'}
def write():
    p=payload(); RESULT.write_bytes(canonical({'certificate_version':1,'claim_status':STATUS,'payload':p,'payload_sha256':hashlib.sha256(canonical(p)).hexdigest()}))
def main():
    a=argparse.ArgumentParser(); a.add_argument('--write',action='store_true'); a.add_argument('--check',action='store_true'); x=a.parse_args()
    if x.write: write(); print('TPC415_CERTIFICATE=WRITTEN')
    elif x.check:
        d=json.loads(RESULT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst); need(d['claim_status']==STATUS and d['payload_sha256']==hashlib.sha256(canonical(d['payload'])).hexdigest(),'certificate'); need(canonical(d['payload'])==canonical(payload()),'exact height certificate'); print('TPC415_CERTIFICATE=PASS cases=4 heights=4 shells=3 shell_count=36848 literal_domain=PASS')
    else: raise SystemExit('explicit --check or --write required')
if __name__=='__main__': main()
