#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]
class Failure(RuntimeError): pass
def req(c:bool,m:str)->None:
 if type(c) is not bool or not c: raise Failure(m)
def nodup(pairs):
 d={}
 for k,v in pairs:
  if k in d: raise Failure('duplicate key')
  d[k]=v
 return d
def main()->int:
 d=json.loads((PROJECT/'results/certificate.json').read_text(),object_pairs_hook=nodup)
 req(d['schema']=='tpc229-primitive-resonance-matching-spectrum-v1','schema')
 req(d['theorem']['edge_operator_spectrum']==[-1,-1,1,1],'spectrum')
 q25=d['q25']; req(q25['pairs']==[[37,47]] and q25['maximum_degree']==1,'Q25')
 expected={'aligned':Fraction(2),'anti_aligned':Fraction(0),'orthogonal':Fraction(1),'partial_negative':Fraction(2,3)}
 for k,v in expected.items(): req(Fraction(d['symmetric_fixtures'][k]['AP_over_diagonal'])==v,k)
 req(d['sharp_bilinear_fixture']['ratio_to_bound']=='1','sharp bound')
 req(d['firewall']['arithmetic_advance']=='NO' and d['firewall']['fixed_atom_credit']==0,'firewall')
 print('TPC229_INDEPENDENT_CHECK=PASS'); print('graph=PRIMITIVE_3_7_MATCHING'); print('block_spectrum=-1,-1,1,1'); return 0
if __name__=='__main__': raise SystemExit(main())
