#!/usr/bin/env python3
"""Fresh sieve and literal mask replay for TPC-412's four pooled heights."""
from __future__ import annotations
import hashlib,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3]; CERT=ROOT/'papers/tpc-412-c1-pooled-complete-shell-extension/results/tpc412_certificate.json'
SCHEMA='TPC412_C1_POOLED_COMPLETE_SHELL_EXTENSION_V1'; STATUS='PROVED_EXACT_FINITE_POOLED_COMPLETE_SHELL_EXTENSION'; QS,COUNTS,HEIGHTS,B=(65536,131072),(5709,10749),(16,32,66,128),1_000_000
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def no_duplicates(pairs):
    d={}
    for k,v in pairs: need(k not in d,'duplicate key'); d[k]=v
    return d
def no_constants(v): raise ValueError('non-finite constant')
def primes(limit):
    f=bytearray(b'\1')*(limit+1); f[:2]=b'\0\0'
    for p in range(2,math.isqrt(limit)+1):
        if f[p]: f[p*p:limit+1:p]=b'\0'*(((limit-p*p)//p)+1)
    return [p for p in range(2,limit+1) if f[p]]
def txt(v): return str(v.numerator) if v.denominator==1 else f'{v.numerator}/{v.denominator}'
def replay(h):
    items=[]
    for q,n in zip(QS,COUNTS):
        s=[p for p in primes(2*q) if p>q]; need(len(s)==n,'shell census'); items.extend((p,q) for p in s)
    ps,qs=[p for p,_ in items],[q for _,q in items]; N=4*h; rs=[0 if i%2==0 else -N for i in range(len(ps))]; period=math.prod(ps); residue=sum(r*(period//p)*pow(period//p,-1,p) for r,p in zip(rs,ps))%period; origin=residue+((B-residue)//period+1)*period; om=[origin%p for p in ps]
    t=lambda d: Fraction(h*h,h*h+d*d); s0=sum((t(d)**2 for d in range(1,N)),Fraction(0)); s1=sum((t(d)**2 for d in range(1,N-1)),Fraction(0))+t(1)**2; aa=[Fraction(p**3,q*q*(p-1)) for p,q in items]; minus,plus=aa[1::2],aa[::2]; vm=sum((a*a for a in minus),Fraction(0)); vp=sum((a*a for a in plus),Fraction(0)); pm=sum(minus,Fraction(0)); amin=min(aa); g0=vm*s0; g1=vm*s1+vp*(s1-t(1)**2); direct=t(1)*pm; z2=direct*direct/(g0*g1); sharp=t(1)**2/(amin*amin*s0*s1); coarse=Fraction(16,h*h)
    weights=[t(d)**2 for d in range(N)]; literal=[]
    for offset in (0,1):
        energy=Fraction(0)
        for p,a,r in zip(ps,aa,om):
            if (r+offset)%p==0: continue
            inner=Fraction(0)
            for j in range(N):
                if j==offset or (r+j)%p==0: continue
                inner+=weights[abs(offset-j)]
            energy+=a*a*inner
        literal.append(energy)
    signed=sum((-(-1)**i*a*t(1) for i,a in enumerate(aa) if om[i] and (om[i]+1)%ps[i]),Fraction(0))
    need(literal==[g0,g1] and signed==direct,'literal pooled masks'); need(z2<=sharp<=coarse,'bound')
    return {'H':h,'N':N,'m_minus':len(minus),'m_plus':len(plus),'shell_count':len(ps),'shell_counts':list(COUNTS),'Q_scales':list(QS),'origin_lower_bound':B,'selected_primes':ps,'prime_shell_Q':qs,'residues':rs,'crt_residue':residue,'crt_period':period,'origin':origin,'S0':txt(s0),'S1':txt(s1),'a_min':txt(amin),'P_minus':txt(pm),'V_minus':txt(vm),'V_plus':txt(vp),'G0':txt(g0),'G1':txt(g1),'direct':txt(direct),'normalized_square':txt(z2),'sharp_bound_square':txt(sharp),'coarse_bound_square_4_over_H':txt(coarse),'uniform_bound_exact':True,'normalized_float64_observation':f'{math.sqrt(float(z2)):.15f}','H_times_normalized_float64_observation':f'{h*math.sqrt(float(z2)):.15f}'}
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    d=json.loads(CERT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants); need(d['claim_status']==STATUS,'status'); need(d['payload_sha256']==hashlib.sha256(canonical(d['payload'])).hexdigest(),'digest'); p=d['payload']; need(p['schema']==SCHEMA and p['cases']==[replay(h) for h in HEIGHTS],'independent replay'); need(p['heights']==list(HEIGHTS) and p['shell_counts']==list(COUNTS),'domain'); need(p['claim_firewall']['POOLED_COMPLETE_SHELL_EXTENSION']=='PROVED_EXACT_FINITE','firewall'); print('TPC412_INDEPENDENT_CHECK=PASS cases=4 heights=4 pooled_shells=2 literal_crt_masks=PASS')
if __name__=='__main__': main()
