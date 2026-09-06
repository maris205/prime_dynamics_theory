#!/usr/bin/env python3
"""Fail-closed contract mutations for TPC-417."""
from __future__ import annotations
import copy,hashlib,json,sys
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3]; CERT=ROOT/'papers/tpc-417-c1-four-shell-finite-operator-bound/results/tpc417_certificate.json'
SCHEMA='TPC417_C1_FOUR_SHELL_FINITE_OPERATOR_BOUND_V1'; STATUS='PROVED_EXACT_FINITE_FULL_OPERATOR_BOUND'
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def nodup(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def noconst(v): raise ValueError('non-finite JSON constant')
def validate(d):
    need(type(d)is dict and set(d)=={'certificate_version','claim_status','payload','payload_sha256'},'document')
    need(type(d['certificate_version'])is int and d['certificate_version']==1 and d['claim_status']==STATUS,'header'); p=d['payload']
    need(d['payload_sha256']==hashlib.sha256(canonical(p)).hexdigest(),'digest')
    need(p.get('schema')==SCHEMA and p.get('status')==STATUS,'status')
    need(p.get('Q_scales')==[65536,131072,262144,524288] and p.get('shell_counts')==[5709,10749,20390,38635],'shell domain')
    need(p.get('heights')==[16,32,66,128] and p.get('window_rule')=='N=4H','height domain')
    th=p.get('theorem',{}); need(th.get('full_bound')=='||Z||_2<=2/(a_min*sqrt(H))+16*abs(A_signed_bulk)/V_minus','bound')
    fw=p.get('claim_firewall',{}); need(fw.get('FULL_FINITE_OPERATOR_BOUND')=='PROVED_EXACT_FINITE' and fw.get('FULL_OPERATOR_GROWING_THEOREM')=='OPEN','firewall')
    need(type(fw.get('FIXED_POWER_CREDIT'))is int and fw.get('FIXED_POWER_CREDIT')==0,'typed zero credit')
    need(p.get('theorem_domain',{}).get('origin')=='CRT solution above B','origin contract')
    cs=p.get('cases'); need(type(cs)is list and len(cs)==4 and [c.get('H') for c in cs]==[16,32,66,128],'cases')
    need(all(c.get('shell_count')==75483 and c.get('m_minus')==37741 and c.get('m_plus')==37742 and c.get('uniform_bound_exact')is True for c in cs),'case fields')
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    original=json.loads(CERT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst); validate(original)
    muts=('q_scales','counts','heights','window','bound','full_status','case_count','shell_count','height_label','exact_flag','growing_flag','crt_contract','version_bool','credit_bool')
    rejected=0
    for m in muts:
        d=copy.deepcopy(original); p=d['payload']
        if m=='q_scales': p['Q_scales']=[65536,131072]
        elif m=='counts': p['shell_counts'][3]=38634
        elif m=='heights': p['heights']=[16,32,66]
        elif m=='window': p['window_rule']='N=H'
        elif m=='bound': p['theorem']['full_bound']='||Z||_2<=1'
        elif m=='full_status': p['claim_firewall']['FULL_FINITE_OPERATOR_BOUND']='PROVED'
        elif m=='case_count': p['cases']=[]
        elif m=='shell_count': p['cases'][0]['shell_count']=75482
        elif m=='height_label': p['cases'][0]['H']=15
        elif m=='growing_flag': p['claim_firewall']['FULL_OPERATOR_GROWING_THEOREM']='PROVED'
        elif m=='crt_contract': p['theorem_domain']['origin']='arbitrary origin'
        elif m=='version_bool': d['certificate_version']=True
        elif m=='credit_bool': p['claim_firewall']['FIXED_POWER_CREDIT']=False
        else: p['cases'][0]['uniform_bound_exact']=False
        d['payload_sha256']=hashlib.sha256(canonical(p)).hexdigest()
        try: validate(d)
        except ValueError: rejected += 1
    need(rejected==len(muts),'mutation escaped')
    parsing=0
    for raw in ('{"a":1,"a":2}','{"a":NaN}'):
        try: json.loads(raw,object_pairs_hook=nodup,parse_constant=noconst)
        except ValueError: parsing+=1
    need(parsing==2,'malformed JSON escaped')
    print(f'TPC417_STRESS=PASS mutations={len(muts)} parsing_rejections={parsing} strict_contract=PASS')
if __name__=='__main__': main()
