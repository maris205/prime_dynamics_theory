#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(PROJECT/'code'))
from resonance_matching import MatchingFailure,build_certificate  # noqa:E402
OUTPUT=PROJECT/'results/certificate.json'
def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('--check',action='store_true'); args=p.parse_args()
 try:
  text=json.dumps(build_certificate(),indent=2,sort_keys=True)+'\n'
  if args.check:
   if not OUTPUT.exists() or OUTPUT.read_text()!=text: raise MatchingFailure('certificate rebuild mismatch')
  else: OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(text)
 except (OSError,ValueError,MatchingFailure) as e: print(f'TPC229_CERTIFICATE=FAIL: {e}',file=sys.stderr); return 1
 print('TPC229_CERTIFICATE=PASS'); print('matching_scan_scales=4089'); print('spectral_fixtures=4'); return 0
if __name__=='__main__': raise SystemExit(main())
