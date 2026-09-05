#!/usr/bin/env python3
"""Strict mutation tests for the TPC-407 complete-shell Q ladder."""
from __future__ import annotations
import copy,hashlib,json,sys
from pathlib import Path
sys.set_int_max_str_digits(1_000_000)
ROOT=Path(__file__).resolve().parents[3];CERT=ROOT/"papers/tpc-407-c1-complete-shell-q-scale-ladder/results/tpc407_certificate.json";SCHEMA="TPC407_C1_COMPLETE_SHELL_Q_SCALE_LADDER_V1";STATUS="PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_LADDER"
def canonical(v):return(json.dumps(v,sort_keys=True,ensure_ascii=True,separators=(",",":"))+"\n").encode()
def no_duplicates(pairs):
 o={}
 for k,v in pairs:
  if k in o:raise ValueError("duplicate key")
  o[k]=v
 return o
def no_constants(v):raise ValueError("non-finite constant")
def need(c,m):
 if type(c)is not bool or not c:raise ValueError(m)
def validate(d):
 need(type(d)is dict and set(d)=={"certificate_version","claim_status","payload","payload_sha256"},"document");need(type(d["certificate_version"])is int and d["certificate_version"]==1 and d["claim_status"]==STATUS,"header");p=d["payload"];need(d["payload_sha256"]==hashlib.sha256(canonical(p)).hexdigest(),"digest");need(p.get("schema")==SCHEMA and p.get("status")==STATUS,"status");need(p.get("Q_scales")==[4096,8192,16384,32768],"scales");need(p.get("shell_counts")==[464,872,1612,3030],"counts");need(p.get("window_rule")=="N=264=4H","window");need(p.get("theorem",{}).get("coarse_uniform_bound")=="z<=4/(a_min*H)<=4/H","bound");need(p.get("claim_firewall",{}).get("FULL_OPERATOR_NORM")=="OPEN","operator firewall");cs=p.get("cases");need(type(cs)is list and len(cs)==4,"case census");need([c.get("Q")for c in cs]==[4096,8192,16384,32768],"case order");need(all(c.get("uniform_bound_exact")is True and c.get("m")*2==c.get("shell_count")for c in cs),"cases")
def main():
 if sys.argv[1:]!=['--check']:raise SystemExit("explicit --check required")
 o=json.loads(CERT.read_bytes(),object_pairs_hook=no_duplicates,parse_constant=no_constants);validate(o);mutations=("q_scales","shell_counts","window","bound","operator","case_count","q_case","exact_flag");rej=0
 for m in mutations:
  d=copy.deepcopy(o);p=d["payload"]
  if m=="q_scales":p["Q_scales"]=[4096,8192]
  elif m=="shell_counts":p["shell_counts"][0]=75
  elif m=="window":p["window_rule"]="N=H"
  elif m=="bound":p["theorem"]["coarse_uniform_bound"]="z<=8/H"
  elif m=="operator":p["claim_firewall"]["FULL_OPERATOR_NORM"]="PROVED"
  elif m=="case_count":p["cases"]=p["cases"][:-1]
  elif m=="q_case":p["cases"][0]["Q"]=512
  else:p["cases"][0]["uniform_bound_exact"]=False
  d["payload_sha256"]=hashlib.sha256(canonical(p)).hexdigest()
  try:validate(d)
  except ValueError:rej+=1
 need(rej==len(mutations),"mutation escaped");print(f"TPC407_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")
if __name__=="__main__":main()
