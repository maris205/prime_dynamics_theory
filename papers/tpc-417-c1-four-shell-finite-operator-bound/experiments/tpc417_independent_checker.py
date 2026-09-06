#!/usr/bin/env python3
"""Independent aggregate replay for TPC-417; it does not import the producer."""
from __future__ import annotations
import hashlib,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3]; CERT=ROOT/'papers/tpc-417-c1-four-shell-finite-operator-bound/results/tpc417_certificate.json'
QS,COUNTS,HEIGHTS,B=(65536,131072,262144,524288),(5709,10749,20390,38635),(16,32,66,128),1_000_000
SCHEMA='TPC417_C1_FOUR_SHELL_FINITE_OPERATOR_BOUND_V1'; STATUS='PROVED_EXACT_FINITE_FULL_OPERATOR_BOUND'
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def nodup(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def noconst(v): raise ValueError('non-finite JSON constant')
def primes(limit):
    f=bytearray(b'\1')*(limit+1); f[:2]=b'\0\0'
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def txt(v): return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def shells():
    out=[]
    for q,n in zip(QS,COUNTS):
        s=[p for p in primes(2*q) if p>q]; need(len(s)==n,'shell census'); out += [(p,q) for p in s]
    return out
def replay(h,items):
    N=4*h; t=lambda d:Fraction(h*h,h*h+d*d); S=[]
    for r in range(N): S.append(sum((t(abs(s-r))**2 for s in range(N) if s!=r),Fraction(0)))
    vm=vp=pm=pp=Fraction(0); amin=None
    for i,(p,q) in enumerate(items):
        a=Fraction(p**3,q*q*(p-1)); amin=a if amin is None or a<amin else amin
        if i%2: vm+=a*a; pm+=a
        else: vp+=a*a; pp+=a
    A=pp-pm; D=[vm*S[0]]+[vm*S[r]+vp*(S[r]-t(r)**2) for r in range(1,N)]
    star=Fraction(4)*pm*pm/(vm*vm*h); kernel=sum((t(d) for d in range(N-1,0,-1)),Fraction(0))
    need(star<=Fraction(4)/(amin*amin*h),'star'); need(min(S)>=Fraction(h,4),'S lower'); need(min(D[1:])>=vm*Fraction(h,4),'D lower')
    need(kernel<=2*h and pm*pm<=(len(items)//2)*vm and vm>=(len(items)//2)*amin*amin,'proof prerequisites')
    return {'H':h,'N':N,'shell_count':len(items),'shell_counts':list(COUNTS),'Q_scales':list(QS),'m_minus':len(items)//2,'m_plus':(len(items)+1)//2,
      'a_min':txt(amin),'P_minus':txt(pm),'P_plus':txt(pp),'A_signed_bulk':txt(A),'V_minus':txt(vm),'V_plus':txt(vp),
      'S_min':txt(min(S)),'S_max':txt(max(S)),'D0':txt(D[0]),'D_min_interior':txt(min(D[1:])),
      'star_envelope_square':txt(star),'star_bound_square':txt(Fraction(4)/(amin*amin*h)),'kernel_one_sided_sum':txt(kernel),
      'bulk_bound':txt(Fraction(16)*abs(A)/vm),'operator_bound':'2/(a_min*sqrt(H))+16*abs(A_signed_bulk)/V_minus',
      'uniform_bound_exact':True,'crt_origin_contract':'o>B, o=0 mod p_i for even i, o=-N mod p_i for odd i'}
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    d=json.loads(CERT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst); p=d['payload']; items=shells()
    need(d['claim_status']==STATUS and d['payload_sha256']==hashlib.sha256(canonical(p)).hexdigest(),'certificate')
    need(p['schema']==SCHEMA and p['Q_scales']==list(QS) and p['shell_counts']==list(COUNTS) and p['heights']==list(HEIGHTS),'domain')
    need(canonical(p['cases'])==canonical([replay(h,items) for h in HEIGHTS]),'independent aggregate replay')
    need(p['claim_firewall']['FULL_FINITE_OPERATOR_BOUND']=='PROVED_EXACT_FINITE' and p['claim_firewall']['FULL_OPERATOR_GROWING_THEOREM']=='OPEN','firewall')
    print('TPC417_INDEPENDENT_CHECK=PASS cases=4 heights=4 shells=4 shell_count=75483 full_bound=PASS')
if __name__=='__main__': main()
