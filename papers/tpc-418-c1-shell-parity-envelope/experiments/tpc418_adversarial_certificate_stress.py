#!/usr/bin/env python3
"""Fail-closed certificate mutations for TPC-418."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CERT=ROOT/'papers/tpc-418-c1-shell-parity-envelope/results/tpc418_certificate.json'
SCHEMA='TPC418_C1_SHELL_PARITY_ENVELOPE_V1'; STATUS='PROVED_EXACT_FINITE_FAMILY_SHELL_PARITY_ENVELOPE'
def need(c,m):
    if type(c) is not bool or not c: raise ValueError(m)
def canon(v): return (json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(',',':'))+'\n').encode()
def nodup(ps):
    d={}
    for k,v in ps: need(k not in d,'duplicate key'); d[k]=v
    return d
def noconst(v): raise ValueError('non-finite constant')
def validate(d):
    need(type(d) is dict and set(d)=={'certificate_version','claim_status','payload','payload_sha256'},'document')
    need(type(d['certificate_version']) is int and d['certificate_version']==1,'version')
    need(d['claim_status']==STATUS and d['payload_sha256']==hashlib.sha256(canon(d['payload'])).hexdigest(),'header')
    p=d['payload']; need(p.get('schema')==SCHEMA and p.get('status')==STATUS,'status')
    th=p.get('theorem',{}); need('sigma_j=epsilon_j' in th.get('sigma','') and '(-1)^(n_j+1)' in th.get('sigma',''),'sigma theorem')
    need('B_sigma=sum_{j:sigma_j=sigma}' in th.get('envelope',''),'sigma grouping')
    fw=p.get('claim_firewall',{}); need(fw.get('GROWING_UNIFORM_THEOREM')=='OPEN_UNASSUMED' and fw.get('FIXED_POWER_CREDIT')==0,'firewall')
    fs=p.get('fixtures'); need(type(fs) is list and len(fs)==3,'fixtures')
    mixed=next((f for f in fs if f.get('name')=='mixed_parity_regression'),None); need(mixed is not None,'mixed fixture')
    need(mixed.get('old_start_sign_envelope_holds') is False,'old grouping regression')
    for f in fs:
        for row in f.get('shell_parity_ledger',[]):
            need(row.get('sigma_j') in (-1,1),'typed sigma')
            need(row.get('sigma_j') == (row['epsilon_j'] if row['n_j']%2 else -row['epsilon_j']),'sigma recurrence')
    return True
def main():
    if sys.argv[1:]!=['--check']: raise SystemExit('explicit --check required')
    d=json.loads(CERT.read_bytes(),object_pairs_hook=nodup,parse_constant=noconst); validate(d)
    muts=('sigma_flip','epsilon_flip','old_grouping','theorem_sigma','firewall','digest','fixture_count','mixed_flag','version_type')
    rejected=0
    for m in muts:
        x=copy.deepcopy(d); p=x['payload']
        if m=='sigma_flip': p['fixtures'][0]['shell_parity_ledger'][0]['sigma_j']*=-1
        elif m=='epsilon_flip': p['fixtures'][0]['shell_parity_ledger'][0]['epsilon_j']*=-1
        elif m=='old_grouping': p['fixtures'][2]['old_start_sign_envelope_holds']=True
        elif m=='theorem_sigma': p['theorem']['sigma']='sigma_j=epsilon_j'
        elif m=='firewall': p['claim_firewall']['GROWING_UNIFORM_THEOREM']='PROVED'
        elif m=='digest': x['payload_sha256']='0'*64
        elif m=='fixture_count': p['fixtures']=p['fixtures'][:2]
        elif m=='mixed_flag': p['fixtures'][2]['name']='small_multishell'
        else: x['certificate_version']=True
        if m != 'digest':
            x['payload_sha256']=hashlib.sha256(canon(p)).hexdigest()
        try: validate(x)
        except ValueError: rejected+=1
    need(rejected==len(muts),'mutation escaped')
    parse_rejections=0
    for raw in ('{"a":1,"a":2}','{"a":NaN}'):
        try: json.loads(raw,object_pairs_hook=nodup,parse_constant=noconst)
        except ValueError: parse_rejections+=1
    need(parse_rejections==2,'parser mutation escaped')
    print(f'TPC418_STRESS=PASS mutations={len(muts)} parsing_rejections={parse_rejections} sigma_contract=PASS')
if __name__=='__main__': main()
