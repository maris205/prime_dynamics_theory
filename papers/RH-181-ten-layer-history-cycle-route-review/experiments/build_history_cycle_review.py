"""Aggregate the RH-172--180 theorem and audit ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from history_cycle_frontier import current_frontiers, route_status  # noqa: E402


RESULTS = {
    172: "polar_identity_audit.json",
    173: "cocycle_identity_audit.json",
    174: "physical_history_audit.json",
    175: "shift_obstruction_audit.json",
    176: "cyclic_closure_audit.json",
    177: "double_cycle_audit.json",
    178: "orientation_mark_audit.json",
    179: "clock_cycle_audit.json",
    180: "cycle_riesz_audit.json",
}


def directory(number: int) -> Path:
    matches = tuple(PAPERS.glob(f"RH-{number}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one RH-{number} directory, found {len(matches)}")
    return matches[0]


def main() -> None:
    payloads = {
        number: json.loads((directory(number) / "results" / filename).read_text(encoding="utf-8"))
        for number, filename in RESULTS.items()
    }
    statuses = {
        "memory_to_history": "proved",
        "history_to_transfer": "open",
        "cycle_algebra": "proved",
        "cycle_calibration": "open",
        "cycle_to_transfer": "open",
        "physical_data": "open",
        "uniform_margins": "open",
        "shell_transport": "open",
    }
    finite_case_count = (
        payloads[172]["case_count"]
        + payloads[173]["case_count"]
        + payloads[174]["snapshot_count"]
        + payloads[175]["resolvent_case_count"]
        + payloads[176]["determinant_case_count"]
        + payloads[177]["determinant_case_count"]
        + payloads[177]["trace_case_count"]
        + payloads[178]["stability_case_count"]
        + payloads[179]["row_count"]
        + payloads[180]["matrix_case_count"]
        + payloads[180]["shell_case_count"]
    )
    frontiers = current_frontiers(statuses)
    output_payload = {
        "status": "rh181_ten_layer_history_cycle_route_review",
        "paper_numbers": list(range(172, 181)),
        "aggregate_finite_case_count": finite_case_count,
        "formula_or_rank_failure_count": (
            payloads[178]["stability_failure_count"]
            + payloads[179]["translation_identity_failure_count"]
            + payloads[180]["rank_failure_count"]
            + payloads[180]["certificate_failure_count"]
        ),
        "history_snapshot_count": payloads[174]["snapshot_count"],
        "history_update_count": payloads[174]["update_count"],
        "history_two_sided_threshold_success_count": payloads[174]["threshold_counts"]["two_sided_residuals_at_most_0_25"],
        "cycle_shell_case_count": payloads[180]["shell_case_count"],
        "current_statuses": statuses,
        "current_route_status": route_status(statuses),
        "current_frontiers": {name: sorted(missing) for name, missing in frontiers},
        "branch_decisions": {
            "finite_memory_to_history_realization": "proved at every finite snapshot",
            "consecutive_reset_packet_two_sided_invariance": "not supported by the 130-snapshot float audit",
            "direct_infinite_history_determinant": "rejected for the canonical weighted-shift completion",
            "finite_cyclic_geometric_cloud": "proved as an exact algebraic model",
            "physical_cycle_identification": "open",
        },
        "macro_boundary": {
            "physical_interface_R": False,
            "cloud_ledger_Q": False,
            "complement_limit_U": False,
            "canonicity_Z": False,
            "directed_limit_T": False,
            "gate_A": False,
            "gates_B_to_E": False,
            "riemann_hypothesis": False,
        },
    }
    output = ROOT / "results/history_cycle_review.json"
    output.write_text(json.dumps(output_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "aggregate_cases": finite_case_count, "route_status": output_payload["current_route_status"], "frontiers": output_payload["current_frontiers"]}, sort_keys=True))


if __name__ == "__main__":
    main()
