#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"tpc192_mvp9_pointwise_frontier_route_decision.json"
AUDIT=HERE/"tpc192_mvp9_pointwise_frontier_route_decision_audit.json"
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def validate(p,a):
    assert p["paper"]==192
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

def validate_upstreams(p):
    locks={x["source_id"]:x for x in p["source_locks"]}
    expected={
      183:("PROVED_L1_INTERFACE_ONE_WAY_IMPLICATION","O161.bad_endpoint_pointwise_fixed_atom"),
      184:("TARGET_WELL_TYPED_OPEN","O161.bad_endpoint_pointwise_fixed_atom"),
      185:("EXACT_FACTOR_TWO_EQUIVALENCE","O161.bad_endpoint_pointwise_fixed_atom"),
      186:("LOCAL_OSCILLATION_IS_EXACT_GAP","O161.bad_endpoint_pointwise_fixed_atom"),
      187:("STOP_SCOPED","O161.bad_endpoint_pointwise_fixed_atom"),
      188:("SWITCH_TO_DIRECT_TWIST","O161.direct_additive_twist_fixed_atom"),
      189:("TARGET_WELL_TYPED_OPEN","O161.direct_additive_twist_fixed_atom"),
      190:("STOP_SCOPED","O161.direct_additive_twist_fixed_atom"),
      191:("BOTH_POINTWISE_ROUTES_OPEN_METHODS_SCOPED","BOTH_O161_POINTWISE_PARENTS"),
    }
    imported=[]
    for n in range(183,192):
        lock=locks[f"TPC{n}.payload"]
        u=json.loads((REPO/lock["path"]).read_text(encoding="utf-8"))
        assert u["paper"]==n
        assert u["progress"]["L2"] is False
        assert u["fixed_atom_decay_obtained"] is False
        assert u["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
        assert (u["verdict"],u["selected_route"])==expected[n]
        assert u["required_quantifier_signature"]==p["required_quantifier_signature"]
        assert all(v is False for v in u["claim_boundary"].values())
        if u["stop_scoped"] is not None:
            assert u["stop_scoped"]["global_pointwise_route_stopped"] is False
            assert u["stop_scoped"]["architecture_stopped"] is False
        imported.append(u)
    stops={u["stop_scoped"]["cell"] for u in imported if u["stop_scoped"] is not None}
    assert stops=={"SIZE_ONLY_LOCAL_OSCILLATION_METHOD","PARSEVAL_CHEBYSHEV_TO_PRESCRIBED_ATOM"}
    selector=json.loads((REPO/locks["TPC181.selector_gate"]["path"]).read_text(encoding="utf-8"))
    assert selector["scoped_obstruction"]["stopped_method"]=="phase_metric_uncontrolled_atomic"
    assert selector["scoped_obstruction"]["scope"]=="UNCONTROLLED_ATOMIC_PROMOTION_ONLY"
    assert selector["scoped_obstruction"]["does_not_stop_architecture"] is True
    assert selector["scoped_obstruction"]["does_not_stop_pointwise_theorems"] is True
    assert [x["source_paper"] for x in p["scoped_method_cells"]]==[181,187,190]
    assert p["global_first_missing"]=="H1.source_backed_local_occurrence_edge_family"
    assert p["selected_pointwise_first_missing"]=="LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION"

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"))
    a=json.loads(AUDIT.read_text(encoding="utf-8"))
    validate(p,a)
    validate_upstreams(p)
    if ns.check:
        assert PAYLOAD.read_text(encoding="utf-8")==canonical(p)
        assert AUDIT.read_text(encoding="utf-8")==canonical(a)
    print(json.dumps({"paper":192,"verdict":p["verdict"],"check":ns.check,"mutations":8},sort_keys=True))
if __name__=="__main__": main()
