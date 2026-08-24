#!/usr/bin/env python3
from __future__ import annotations
import copy,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'code'))
from matched_mass_ceiling import MassFailure,validate_payload  # noqa:E402
def main()->int:
 b=json.loads((P/'results/certificate.json').read_text());edits=[(('schema',),'bad'),(('claim_level',),'PROVED_ARITHMETIC_L2'),(('theorem','literal_aligned_kappa_bound'),3),(('theorem','strict_1_over_400_edge_density_toll'),'FREE'),(('q25','edge_count'),2),(('boundary_scan','scales_checked'),1),(('checks','mass_ceiling_exact'),False)];n=0
 for path,val in edits:
  x=copy.deepcopy(b);y=x
  for k in path[:-1]:y=y[k]
  y[path[-1]]=val
  try:validate_payload(x)
  except MassFailure:n+=1
 if n!=len(edits):print(f'TPC230_MASS_ADVERSARY=FAIL: {n}/{len(edits)}',file=sys.stderr);return 1
 print('TPC230_MASS_ADVERSARY=PASS');print(f'mutations_rejected={n}');return 0
if __name__=='__main__':raise SystemExit(main())
