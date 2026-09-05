#!/usr/bin/env python3
"""Independent exact complete-shell Q-scale replay for TPC-407."""
from __future__ import annotations
import hashlib,json,math,sys
from fractions import Fraction
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3];CERT=ROOT/"papers/tpc-407-c1-complete-shell-q-scale-ladder/results/tpc407_certificate.json"
SCHEMA="TPC407_C1_COMPLETE_SHELL_Q_SCALE_LADDER_V1";STATUS="PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_LADDER";QS=(4096,8192,16384,32768);H=66;N=264;B=1_000_000
def need(c,m):
    if type(c) is not bool or not c:raise ValueError(m)
def canonical(v):return(json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))+"\n").encode()
def no_duplicates(pairs):
    o={}
    for k,v in pairs:need(k not in o,"duplicate key");o[k]=v
    return o
def no_constants(v):raise ValueError("non-finite JSON constant")
def primes(limit):
    f=bytearray(b"\1")*(limit+1);f[:2]=b"\0\0"
    for p in range(2,math.isqrt(limit)+1):
        if f[p]:f[p*p:limit+1:p]=b"\0"*(((limit-p*p)//p)+1)
    return[p for p in range(2,limit+1)if f[p]]
def txt(x):return str(x.numerator)if x.denominator==1 else f"{x.numerator}/{x.denominator}"
def replay():
    out=[]
    for Q in QS:
        shell=[p for p in primes(2*Q)if p>Q];need(len(shell)%2==0,"even shell")
        residues=[0 if i%2==0 else -N for i in range(len(shell))];period=math.prod(shell);residue=sum(r*(period//p)*pow(period//p,-1,p)for r,p in zip(residues,shell))%period;origin=residue+((B-residue)//period+1)*period
        t=lambda d:Fraction(H*H,H*H+d*d);S0=sum((t(d)**2 for d in range(1,N)),Fraction(0));S1=sum((t(d)**2 for d in range(1,N-1)),Fraction(0))+t(1)**2
        aa=[Fraction(p**3,Q*Q*(p-1))for p in shell];vm=sum((a*a for a in aa[1::2]),Fraction(0));vp=sum((a*a for a in aa[::2]),Fraction(0));pm=sum(aa[1::2],Fraction(0));amin=min(aa);g0=vm*S0;g1=vm*S1+vp*(S1-t(1)**2);direct=t(1)*pm;z2=direct*direct/(g0*g1);sharp2=t(1)**2/(amin*amin*S0*S1);coarse2=Fraction(16,H*H)
        literal=[]
        for offset in(0,1):
            energy=Fraction(0)
            for p,a in zip(shell,aa):
                if(origin+offset)%p==0:continue
                inner=Fraction(0)
                for j in range(N):
                    if j==offset or(origin+j)%p==0:continue
                    inner+=t(offset-j)**2
                energy+=a*a*inner
            literal.append(energy)
        signed=sum((-(-1)**i*aa[i]*t(1)for i,p in enumerate(shell)if origin%p and(origin+1)%p),Fraction(0))
        need(literal==[g0,g1]and signed==direct,"literal masks");need(z2<=sharp2<=coarse2,"bound")
        out.append({"Q":Q,"H":H,"N":N,"m":len(shell)//2,"shell_count":len(shell),"origin_lower_bound":B,"selected_primes":shell,"residues":residues,"crt_residue":residue,"crt_period":period,"origin":origin,"S0":txt(S0),"S1":txt(S1),"a_min":txt(amin),"P_minus":txt(pm),"V_minus":txt(vm),"V_plus":txt(vp),"G0":txt(g0),"G1":txt(g1),"direct":txt(direct),"normalized_square":txt(z2),"sharp_bound_square":txt(sharp2),"coarse_bound_square_4_over_H":txt(coarse2),"uniform_bound_exact":True,"normalized_float64_observation":f"{math.sqrt(float(z2)):.15f}","H_times_normalized_float64_observation":f"{H*math.sqrt(float(z2)):.15f}"})
    return out
def main():
    if sys.argv[1:]!=['--check']:raise SystemExit("explicit --check required")
    d=json.loads(CERT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants);need(type(d)is dict and set(d)=={"certificate_version","claim_status","payload","payload_sha256"},"document");need(d["claim_status"]==STATUS,"status");need(d["payload_sha256"]==hashlib.sha256(canonical(d["payload"])).hexdigest(),"digest");p=d["payload"];need(p["schema"]==SCHEMA and p["cases"]==replay(),"independent replay");need(p["Q_scales"]==list(QS) and p["shell_counts"]==[464,872,1612,3030],"scale census");need(p["claim_firewall"]["COMPLETE_SHELL_Q_SCALE_LADDER"]=="PROVED_EXACT_FINITE","firewall");print("TPC407_INDEPENDENT_CHECK=PASS cases=4 q_scales=4 literal_crt_masks=PASS uniform_bound=PASS")
if __name__=="__main__":main()
