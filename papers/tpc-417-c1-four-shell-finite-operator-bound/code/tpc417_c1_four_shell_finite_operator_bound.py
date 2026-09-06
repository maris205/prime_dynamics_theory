#!/usr/bin/env python3
"""Exact finite full-matrix bound for the four-shell C1 proxy."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / 'results/tpc417_certificate.json'
SCHEMA = 'TPC417_C1_FOUR_SHELL_FINITE_OPERATOR_BOUND_V1'
STATUS = 'PROVED_EXACT_FINITE_FULL_OPERATOR_BOUND'
QS, COUNTS, HEIGHTS, B = (65536,131072,262144,524288), (5709,10749,20390,38635), (16,32,66,128), 1_000_000

class Failure(ValueError): pass
def need(c, m):
    if type(c) is not bool or not c: raise Failure(m)
def canonical(v): return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(',',':'))+'\n').encode()
def nodup(ps):
    d = {}
    for k,v in ps: need(k not in d, 'duplicate key'); d[k] = v
    return d
def noconst(v): raise Failure('non-finite JSON constant')
def primes(limit):
    f = bytearray(b'\1')*(limit+1); f[:2] = b'\0\0'
    for p in range(2, math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p] = b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2, limit+1) if f[p]]
def txt(v): return str(v.numerator) if v.denominator == 1 else f'{v.numerator}/{v.denominator}'
def shells():
    out=[]
    for q,n in zip(QS, COUNTS):
        s=[p for p in primes(2*q) if p>q]; need(len(s)==n, 'shell census')
        out.extend((p,q) for p in s)
    return out
def row(h, items):
    ps=[p for p,_ in items]; qs=[q for _,q in items]; N=4*h
    need(min(ps)>N and len(ps)%2==1, 'domain')
    t=lambda d: Fraction(h*h, h*h+d*d)
    prefix=[Fraction(0)]
    for d in range(1,N): prefix.append(prefix[-1]+t(d)**2)
    S=[prefix[r]+prefix[N-1-r] for r in range(N)]
    aa=[Fraction(p**3, q*q*(p-1)) for p,q in items]
    minus,plus=aa[1::2],aa[::2]
    vm=sum((a*a for a in minus), Fraction(0)); vp=sum((a*a for a in plus), Fraction(0))
    pm=sum(minus, Fraction(0)); pp=sum(plus, Fraction(0)); A=pp-pm; amin=min(aa)
    D=[vm*S[0]] + [vm*S[r]+vp*(S[r]-t(r)**2) for r in range(1,N)]
    need(all(d>0 for d in D), 'positive diagonal')
    star_envelope=Fraction(4)*pm*pm/(vm*vm*h)
    star_bound=Fraction(4,1)/(amin*amin*h)
    bulk_bound=Fraction(16)*abs(A)/vm
    kernel_sum=sum((t(d) for d in range(1,N)),Fraction(0))
    need(pm*pm<=len(minus)*vm and vm>=len(minus)*amin*amin, 'Cauchy and amplitude')
    need(star_envelope<=star_bound and all(x>=Fraction(h,4) for x in S), 'star bound')
    need(kernel_sum<=2*h, 'kernel sum')
    need(all(d>=vm*Fraction(h,4) for d in D[1:]), 'diagonal lower bound')
    return {'H':h,'N':N,'shell_count':len(ps),'shell_counts':list(COUNTS),'Q_scales':list(QS),
            'm_minus':len(minus),'m_plus':len(plus),'a_min':txt(amin),'P_minus':txt(pm),
            'P_plus':txt(pp),'A_signed_bulk':txt(A),'V_minus':txt(vm),'V_plus':txt(vp),
            'S_min':txt(min(S)),'S_max':txt(max(S)),'D0':txt(D[0]),'D_min_interior':txt(min(D[1:])),
            'star_envelope_square':txt(star_envelope),'star_bound_square':txt(star_bound),'kernel_one_sided_sum':txt(kernel_sum),
            'bulk_bound':txt(bulk_bound),'operator_bound':'2/(a_min*sqrt(H))+16*abs(A_signed_bulk)/V_minus',
            'uniform_bound_exact':True,'crt_origin_contract': 'o>B, o=0 mod p_i for even i, o=-N mod p_i for odd i'}
def payload():
    items=shells()
    return {'schema':SCHEMA,'status':STATUS,'Q_scales':list(QS),'heights':list(HEIGHTS),'origin_lower_bound':B,
      'shell_rule':'pooled full shells Q<p<=2Q','shell_counts':list(COUNTS),'shell_sha256':{str(q):hashlib.sha256(canonical([p for p,x in items if x==q])).hexdigest() for q in QS},
      'window_rule':'N=4H','normalization':'full finite matrix with exact local diagonal energies',
      'theorem_domain':{'H_and_N':'H in {16,32,66,128}, N=4H','Q_and_shell':'four complete shells pooled without deletion',
       'profile':'even i is positive and divides o; odd i is negative and divides o+N','amplitude':'a_i=p_i^3/[Q_i^2(p_i-1)]',
       'matrix':'M(u,v)=T_{u-v}[-A+b(u)+b(v)] off diagonal, M(u,u)=0','origin':'CRT solution above B'},
      'theorem':{'block_identity':'Z=[[0,q^T],[q,C]] after local diagonal normalization',
       'row_energy':'D_0=V_minus*S_0 and D_r=V_minus*S_r+V_plus*(S_r-t_r^2), r>=1',
       'star_bound':'||q||^2<=4/(a_min^2*H)','bulk_bound':'||C||_2<=16*abs(A_signed_bulk)/V_minus',
       'full_bound':'||Z||_2<=2/(a_min*sqrt(H))+16*abs(A_signed_bulk)/V_minus',
       'proof_steps':['CRT gives exactly the endpoint deletion masks','D_r>=V_minus*H/4','P_minus^2<=m_minus*V_minus',
                      'V_minus>=m_minus*a_min^2','sum_r t_r^2<=S_0','the one-sided kernel sum is at most 2H',
                      'symmetric row-sum bound controls C','triangle inequality for the two block matrices'],
       'scope':'full N by N normalized synthetic proxy matrix at four fixed finite heights'},
      'cases':[row(h,items) for h in HEIGHTS],
      'claim_firewall':{'FULL_FINITE_OPERATOR_BOUND':'PROVED_EXACT_FINITE','FULL_OPERATOR_GROWING_THEOREM':'OPEN',
       'PHYSICAL_H0':'OPEN','ARITHMETIC_SIGN_IDENTIFICATION':'OPEN','ARITHMETIC_ADVANCE':'NO','FIXED_POWER_CREDIT':0,
       'FULL_GATE_B':'OPEN','ROUTE_B':'OPEN','TWIN_PRIME_RESULT':'NONE'},'round2_clue':'TEST_C1_FOUR_SHELL_FINITE_OPERATOR_BOUND'}
def write():
    p=payload(); RESULT.write_bytes(canonical({'certificate_version':1,'claim_status':STATUS,'payload':p,'payload_sha256':hashlib.sha256(canonical(p)).hexdigest()}))
def main():
    a=argparse.ArgumentParser(); a.add_argument('--write',action='store_true'); a.add_argument('--check',action='store_true'); x=a.parse_args()
    if x.write: write(); print('TPC417_CERTIFICATE=WRITTEN')
    elif x.check:
        d=json.loads(RESULT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst)
        need(type(d)is dict and set(d)=={'certificate_version','claim_status','payload','payload_sha256'},'exact header fields')
        need(type(d['certificate_version'])is int and d['certificate_version']==1,'typed certificate version')
        need(d['claim_status']==STATUS and d['payload_sha256']==hashlib.sha256(canonical(d['payload'])).hexdigest(),'certificate')
        need(canonical(d['payload'])==canonical(payload()),'exact full-operator certificate')
        print('TPC417_CERTIFICATE=PASS cases=4 heights=4 shells=4 shell_count=75483 full_bound=PASS strict_firewall=PASS')
    else: raise SystemExit('explicit --check or --write required')
if __name__=='__main__': main()
