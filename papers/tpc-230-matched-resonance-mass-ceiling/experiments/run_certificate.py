#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1];sys.path.insert(0,str(P/'code'))
from matched_mass_ceiling import MassFailure,build_certificate  # noqa:E402
O=P/'results/certificate.json'
def main()->int:
 a=argparse.ArgumentParser();a.add_argument('--check',action='store_true');x=a.parse_args()
 try:
  t=json.dumps(build_certificate(),indent=2,sort_keys=True)+'\n'
  if x.check:
   if not O.exists() or O.read_text()!=t:raise MassFailure('certificate mismatch')
  else:O.parent.mkdir(parents=True,exist_ok=True);O.write_text(t)
 except (OSError,ValueError,MassFailure) as e:print(f'TPC230_CERTIFICATE=FAIL: {e}',file=sys.stderr);return 1
 print('TPC230_CERTIFICATE=PASS');print('mass_scan_scales=4089');print('ceiling_fixtures=2');return 0
if __name__=='__main__':raise SystemExit(main())
