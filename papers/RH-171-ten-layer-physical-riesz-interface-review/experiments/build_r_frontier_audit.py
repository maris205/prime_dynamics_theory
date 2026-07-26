"""Aggregate RH-162--170 audits and build the physical-R frontier."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from r_interface_frontier import physical_r_frontier, physical_r_status  # noqa: E402


SOURCES = (
    (162, "RH-162-ambient-realization-reset-riesz-gate/results/realization_audit.json", "sample_count", "failure_count"),
    (163, "RH-163-two-sided-schur-packet-riesz-certificate/results/schur_audit.json", "sample_count", "failure_count"),
    (164, "RH-164-balanced-similarity-packet-coupling/results/balance_audit.json", "sample_count", "norm_identity_failure_count"),
    (165, "RH-165-midgap-normal-block-contour/results/midgap_audit.json", "sample_count", "rank_count_failure_count"),
    (166, "RH-166-bi-ritz-directional-riesz-graph/results/bi_ritz_audit.json", "sample_count", "identity_failure_count"),
    (167, "RH-167-finite-mesh-resolvent-envelope/results/mesh_audit.json", "trial_count", "failure_count"),
    (168, "RH-168-operator-ball-mesh-schur-transfer/results/operator_ball_audit.json", "trial_count", "failure_count"),
    (169, "RH-169-common-coordinate-riesz-transport/results/transport_audit.json", "sample_count", "failure_count"),
)


def main() -> None:
    records = []
    total_cases = 0
    total_failures = 0
    for number, relative, count_key, failure_key in SOURCES:
        path = PAPERS / relative
        payload = json.loads(path.read_text(encoding="utf-8"))
        count = int(payload[count_key])
        failures = int(payload[failure_key])
        # RH-164 and RH-165 have a second independent failure count.
        if number == 164:
            failures += int(payload["local_optimum_failure_count"])
        if number == 165:
            failures += int(payload["resolvent_bound_failure_count"])
        total_cases += count
        total_failures += failures
        records.append({"paper": f"RH-{number}", "case_count": count, "failure_count": failures, "source": relative})
    shell = json.loads((PAPERS / "RH-170-rank-growing-riesz-shell-atlas/results/shell_audit.json").read_text(encoding="utf-8"))
    shell_witnesses = int(shell["rank_change_count"])
    shell_failures = int(shell["rank_floor_failure_count"])
    total_failures += shell_failures
    statuses = {"X_phys": "open", "D_phys": "open", "K_phys": "open", "H_phys": "open"}
    frontier = physical_r_frontier(statuses)
    payload = {
        "status": "rh171_ten_layer_physical_riesz_interface_review",
        "audit_records": records,
        "finite_matrix_case_count": total_cases,
        "rank_change_witness_count": shell_witnesses,
        "aggregate_failure_count": total_failures,
        "physical_leaf_statuses": statuses,
        "physical_R_status": physical_r_status(statuses),
        "minimal_completion_bundles": [sorted(bundle) for bundle in frontier],
        "current_first_missing_interface": "X_phys",
        "theorem_boundary": {
            "conditional_physical_R_closure_theorem": True,
            "architecture_relative_minimal_frontier": True,
            "all_abstract_R_implications_proved": True,
            "any_physical_leaf_proved": False,
            "physical_R_interface": False,
            "macro_gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "riemann_hypothesis": False,
        },
    }
    output = ROOT / "results" / "r_frontier_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "finite_cases": total_cases,
        "rank_witnesses": shell_witnesses,
        "failures": total_failures,
        "first_missing": "X_phys",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
