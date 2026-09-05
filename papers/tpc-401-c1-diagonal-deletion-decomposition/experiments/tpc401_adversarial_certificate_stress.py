#!/usr/bin/env python3
"""Small schema mutation firewall for TPC-401."""
import json, sys, hashlib, copy
from tpc401_independent_checker import check, parse, canonical, Failure
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
CERT=ROOT/"papers/tpc-401-c1-diagonal-deletion-decomposition/results/tpc401_certificate.json"
def main():
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    raw=CERT.read_bytes(); d=parse(raw); check(d,recompute=False); rejected=0
    mutations=[lambda m:m.__setitem__('certificate_version',True),
      lambda m:m.__setitem__('claim_status','BAD'),
      lambda m:m['payload'].__setitem__('schema','BAD'),
      lambda m:m['payload'].__setitem__('round2_clue','BAD'),
      lambda m:m['payload'].__setitem__('claim_firewall',{}),
      lambda m:m['payload'].__setitem__('production_domain',{}),
      lambda m:m['payload']['claim_firewall'].__setitem__('TPC401_FIXED_POWER_CREDIT',False),
      lambda m:m['payload']['production_domain']['audit'].__setitem__('component_rows',720),
      lambda m:m['payload']['production_domain']['audit'].__setitem__('all_sampled_components_equal',1),
      lambda m:m['payload']['exact_anchor_boundary'].__setitem__('u',0),
      lambda m:m['payload']['exact_anchor_boundary'].__setitem__('nonzero_difference','0')]
    for mutate in mutations:
        m=copy.deepcopy(d); mutate(m)
        m['payload_sha256']=hashlib.sha256(canonical(m['payload'])).hexdigest()
        try: check(m,recompute=False)
        except (Failure,KeyError,TypeError,ValueError): rejected+=1
        else: raise Failure('mutated document accepted')
    for bad in (b'{"x":1,"x":2}\n',b'{"x":NaN}\n',b'{"x":Infinity}\n'):
        try: parse(bad)
        except (Failure,ValueError): rejected+=1
        else: raise Failure('malformed JSON accepted')
    print(f'TPC401_STRESS=PASS mutations={rejected}')
if __name__ == "__main__": main()
