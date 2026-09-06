#!/usr/bin/env python3
"""Independent literal replay for the four-shell odd pooled row."""
from __future__ import annotations
import hashlib,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3]; CERT=ROOT/'papers/tpc-416-c1-four-shell-odd-pooled-extension/results/tpc416_certificate.json'; SCHEMA='TPC416_C1_FOUR_SHELL_ODD_POOLED_EXTENSION_V1'; STATUS='PROVED_EXACT_FINITE_FOUR_SHELL_ODD_POOLED_EXTENSION'; QS,COUNTS,H,N,B=(65536,131072,262144,524288),(5709,10749,20390,38635),66,264,1_000_000
def need(c,m):
    if type(c)is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def nodup(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def noconst(v): raise ValueError('non-finite constant')
def primes(limit):
    f=bytearray(b'\1')*(limit+1); f[:2]=b'\0\0'
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def txt(v): return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def replay():
    items=[]
    for q,n in zip(QS,COUNTS):
        s=[p for p in primes(2*q) if p>q]; need(len(s)==n,'shell census'); items.extend((p,q) for p in s)
    ps,qs=[p for p,_ in items],[q for _,q in items]; rs=[0 if i%2==0 else -N for i in range(len(ps))]; period=math.prod(ps); residue=sum(r*(period//p)*pow(period//p,-1,p) for r,p in zip(rs,ps))%period; origin=residue+((B-residue)//period+1)*period; om=[origin%p for p in ps]; t=lambda d:Fraction(H*H,H*H+d*d); s0=sum((t(d)**2 for d in range(1,N)),Fraction(0)); s1=sum((t(d)**2 for d in range(1,N-1)),Fraction(0))+t(1)**2; aa=[Fraction(p**3,q*q*(p-1)) for p,q in items]; minus,plus=aa[1::2],aa[::2]; vm=sum((a*a for a in minus),Fraction(0)); vp=sum((a*a for a in plus),Fraction(0)); pm=sum(minus,Fraction(0)); amin=min(aa); g0=vm*s0; g1=vm*s1+vp*(s1-t(1)**2); direct=t(1)*pm; z2=direct*direct/(g0*g1); sharp=t(1)**2/(amin*amin*s0*s1); coarse=Fraction(16,H*H); weights=[t(d)**2 for d in range(N)]; literal=[]
    for off in (0,1):
        energy=Fraction(0)
        for p,a,r in zip(ps,aa,om):
            if (r+off)%p==0: continue
            inner=Fraction(0)
            for j in range(N):
                if j==off or (r+j)%p==0: continue
                inner+=weights[abs(off-j)]
            energy+=a*a*inner
        literal.append(energy)
    signed=sum((-(-1)**i*a*t(1) for i,a in enumerate(aa) if om[i] and (om[i]+1)%ps[i]),Fraction(0)); need(literal==[g0,g1] and signed==direct,'literal masks'); need(z2<=sharp<=coarse,'bound')
    return {'H':H,'N':N,'m_minus':len(minus),'m_plus':len(plus),'shell_count':len(ps),'shell_counts':list(COUNTS),'Q_scales':list(QS),'origin_lower_bound':B,'selected_primes':ps,'prime_shell_Q':qs,'residues':rs,'crt_residue':residue,'crt_period':period,'origin':origin,'S0':txt(s0),'S1':txt(s1),'a_min':txt(amin),'P_minus':txt(pm),'V_minus':txt(vm),'V_plus':txt(vp),'G0':txt(g0),'G1':txt(g1),'direct':txt(direct),'normalized_square':txt(z2),'sharp_bound_square':txt(sharp),'coarse_bound_square_4_over_H':txt(coarse),'uniform_bound_exact':True,'normalized_float64_observation':f'{math.sqrt(float(z2)):.15f}','H_times_normalized_float64_observation':f'{H*math.sqrt(float(z2)):.15f}'}
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    d=json.loads(CERT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst); need(d['claim_status']==STATUS,'status'); need(d['payload_sha256']==hashlib.sha256(canonical(d['payload'])).hexdigest(),'digest'); p=d['payload']; need(p['schema']==SCHEMA and p['cases']==[replay()],'independent replay'); need(p['shell_counts']==list(COUNTS) and p['Q_scales']==list(QS),'domain'); need(p['claim_firewall']['FOUR_SHELL_ODD_POOLED_EXTENSION']=='PROVED_EXACT_FINITE','firewall'); print('TPC416_INDEPENDENT_CHECK=PASS cases=1 shells=4 shell_count=75483 odd_parity=37741/37742 literal_crt_masks=PASS')
if __name__=='__main__': main()
