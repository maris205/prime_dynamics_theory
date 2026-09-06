#!/usr/bin/env python3
"""Strict fail-closed mutation tests for the TPC-412 certificate."""
from __future__ import annotations
import copy,hashlib,json,sys
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3]; CERT=ROOT/'papers/tpc-412-c1-pooled-complete-shell-extension/results/tpc412_certificate.json'; SCHEMA='TPC412_C1_POOLED_COMPLETE_SHELL_EXTENSION_V1'; STATUS='PROVED_EXACT_FINITE_POOLED_COMPLETE_SHELL_EXTENSION'
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def canonical(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def no_duplicates(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def no_constants(v): raise ValueError('non-finite constant')
def validate(d):
    need(type(d)is dict and set(d)=={'certificate_version','claim_status','payload','payload_sha256'},'document'); need(d['certificate_version']==1 and d['claim_status']==STATUS,'header'); p=d['payload']; need(d['payload_sha256']==hashlib.sha256(canonical(p)).hexdigest(),'digest'); need(p.get('schema')==SCHEMA and p.get('status')==STATUS,'status'); need(p.get('Q_scales')==[65536,131072] and p.get('shell_counts')==[5709,10749],'scales'); need(p.get('heights')==[16,32,66,128] and p.get('window_rule')=='N=4H','domain'); need(p.get('theorem',{}).get('coarse_uniform_bound')=='z<=4/(a_min*H)<=4/H','bound'); need(p.get('claim_firewall',{}).get('FULL_OPERATOR_NORM')=='OPEN','firewall'); cs=p.get('cases'); need(type(cs)is list and len(cs)==4,'case census'); need([c.get('H') for c in cs]==[16,32,66,128],'height rows'); need(all(c.get('shell_count')==16458 and c.get('m_minus')==8229 and c.get('m_plus')==8229 and c.get('uniform_bound_exact')is True for c in cs),'cases'); need(cs[0].get('prime_shell_Q')==[65536]*5709+[131072]*10749,'shell labels')
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    original=json.loads(CERT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants); validate(original); muts=('q_scales','shell_counts','heights','window','bound','prime_q','operator','case_count','shell_count','height_label','exact_flag'); rejected=0
    for m in muts:
        d=copy.deepcopy(original); p=d['payload']
        if m=='q_scales': p['Q_scales']=[65536]
        elif m=='shell_counts': p['shell_counts'][1]=10748
        elif m=='heights': p['heights']=[16,32,66]
        elif m=='window': p['window_rule']='N=H'
        elif m=='bound': p['theorem']['coarse_uniform_bound']='z<=8/H'
        elif m=='prime_q': p['cases'][0]['prime_shell_Q'][0]=131072
        elif m=='operator': p['claim_firewall']['FULL_OPERATOR_NORM']='PROVED'
        elif m=='case_count': p['cases']=[]
        elif m=='shell_count': p['cases'][0]['shell_count']=16457
        elif m=='height_label': p['cases'][0]['H']=15
        else: p['cases'][0]['uniform_bound_exact']=False
        d['payload_sha256']=hashlib.sha256(canonical(p)).hexdigest()
        try: validate(d)
        except ValueError: rejected+=1
    need(rejected==len(muts),'mutation escaped'); print(f'TPC412_STRESS=PASS mutations={len(muts)} strict_contract=PASS')
if __name__=='__main__': main()
