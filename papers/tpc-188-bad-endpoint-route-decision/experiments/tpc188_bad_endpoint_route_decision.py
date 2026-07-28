#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"tpc188_bad_endpoint_route_decision.json"
AUDIT=HERE/"tpc188_bad_endpoint_route_decision_audit.json"
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def validate(p,a):
    assert p["paper"]==188
    assert p["required_quantifier_signature"]["phase_axis"]=="NAMED_FIXED_ATOM"
    assert p["fixed_atom_decay_obtained"] is False
    assert p["progress"]["L2"] is False
    assert p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
    assert p["endpoint_ledger"]["state"]=="UNPAID"
    assert all(v is False for v in p["claim_boundary"].values())
    for lock in p["source_locks"]:
        source=REPO/lock["path"]
        assert source.is_file()
        assert hashlib.sha256(source.read_bytes()).hexdigest()==lock["sha256"]
        assert lock["hash_is_theorem_evidence"] is False
    if p["stop_scoped"] is not None:
        assert p["stop_scoped"]["global_pointwise_route_stopped"] is False
        assert p["stop_scoped"]["architecture_stopped"] is False
    assert a["payload_sha256"]==hashlib.sha256(canonical(p).encode()).hexdigest()
    assert a["all_checks_pass"] is True
    assert len(a["mutation_registry"])==8
    assert all(x["rejected"] is True for x in a["mutation_registry"])
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"))
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(p,a)
    if ns.check:
        assert PAYLOAD.read_text(encoding="utf-8")==canonical(p)
        assert AUDIT.read_text(encoding="utf-8")==canonical(a)
    print(json.dumps({"paper":188,"verdict":p["verdict"],"check":ns.check,"mutations":8},sort_keys=True))
if __name__=="__main__": main()
