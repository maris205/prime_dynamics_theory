#!/usr/bin/env python3
from __future__ import annotations
import copy,json,sys
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(PROJECT/'code'))
from resonance_matching import MatchingFailure,validate_payload  # noqa:E402
def main()->int:
 base=json.loads((PROJECT/'results/certificate.json').read_text()); muts=[]
 edits=[(('schema',),'bad'),(('claim_level',),'PROVED_ARITHMETIC_L2'),(('theorem','edge_operator_spectrum'),[-2,2]),(('boundary_scan','maximum_degree'),2),(('symmetric_fixtures','aligned','AP_over_diagonal'),'1'),(('symmetric_fixtures','anti_aligned','AP_over_diagonal'),'1'),(('checks','matching_degree_at_most_one'),False)]
 for path,val in edits:
  x=copy.deepcopy(base); y=x
  for k in path[:-1]: y=y[k]
  y[path[-1]]=val; muts.append(x)
 rejected=0
 for x in muts:
  try: validate_payload(x)
  except MatchingFailure: rejected+=1
 if rejected!=len(muts): print(f'TPC229_MATCHING_ADVERSARY=FAIL: {rejected}/{len(muts)}',file=sys.stderr); return 1
 print('TPC229_MATCHING_ADVERSARY=PASS'); print(f'mutations_rejected={rejected}'); return 0
if __name__=='__main__': raise SystemExit(main())
