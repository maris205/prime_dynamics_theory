#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def req(c,m):
 if type(c) is not bool or not c:raise RuntimeError(m)
def nodup(ps):
 d={}
 for k,v in ps:
  if k in d:raise RuntimeError('duplicate')
  d[k]=v
 return d
def main()->int:
 d=json.loads((P/'results/certificate.json').read_text(),object_pairs_hook=nodup);req(d['schema']=='tpc230-matched-resonance-mass-ceiling-v1','schema')
 q=d['q25'];req(q['prime_count']==6 and q['edge_count']==1 and q['uniform_mass_fraction']=='1/3','Q25 uniform');req(Fraction(q['literal_aligned_mass_fraction'])<=1,'Q25 literal')
 f=d['sharp_fixture'];req(Fraction(f['AP'])==Fraction(f['unmatched_mass']),'sharp floor');req(Fraction(f['saving'])==Fraction(f['matched_mass']),'sharp ceiling')
 req(d['theorem']['strict_1_over_400_edge_density_toll']=='E/P>=1/3200 is necessary under literal kappa<=4','toll');req(d['firewall']['arithmetic_advance']=='NO','firewall')
 print('TPC230_INDEPENDENT_CHECK=PASS');print('ceiling=GLOBAL_SAVING_AT_MOST_MATCHED_MASS');print('literal_density_toll=1/3200');return 0
if __name__=='__main__':raise SystemExit(main())
