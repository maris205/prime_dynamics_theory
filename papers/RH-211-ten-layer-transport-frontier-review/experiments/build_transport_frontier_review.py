"""Build the RH-202--RH-210 aggregate transport-frontier ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from transport_review import review_coordinate, strict_gate_vector  # noqa: E402


SOURCES = {
    202: ("RH-202-adjacent-edge-quartet-transport", "adjacent_transport_audit.json"),
    203: ("RH-203-riesz-intertwining-transport-budget", "riesz_transport_identity_audit.json"),
    204: ("RH-204-conjugate-branch-correspondence", "branch_correspondence_audit.json"),
    205: ("RH-205-endpoint-procrustes-shell-map", "procrustes_shell_audit.json"),
    206: ("RH-206-residue-cocycle-renormalization-obstruction", "residue_cocycle_audit.json"),
    207: ("RH-207-dual-channel-quartic-divisor-flow", "quartic_divisor_flow.json"),
    208: ("RH-208-endpoint-isolation-transport-certification", "transport_certification_feasibility.json"),
    209: ("RH-209-expanding-edge-cloud-transport-obstruction", "expanding_cloud_audit.json"),
    210: ("RH-210-divisor-first-gate-a-pivot", "divisor_first_route_audit.json"),
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads((PAPERS / directory / "results" / filename).read_text(encoding="utf-8"))
        for number, (directory, filename) in SOURCES.items()
    }


def run() -> dict[str, object]:
    source = load_sources()
    statuses = {
        "naive_haar_transport_rejected": float(source[202]["maximum_oblique_projector_defect"]) > 1.0,
        "resolvent_transport_identity_proved": int(source[203]["identity_failure_count"]) == 0,
        "branch_correspondence_supported": int(source[204]["unique_assignment_case_count"]) == 4,
        "endpoint_partial_isometry_exists": int(source[205]["identity_failure_count"]) == 0,
        "scalar_residue_renormalization_rejected": float(source[206]["maximum_common_scalar_relative_residual"]) > 0.9,
        "dual_channel_divisor_supported": float(source[207]["maximum_left_right_coefficient_relative_error"]) < 0.01,
        "endpoint_isolation_feasible": int(source[208]["endpoint_case_below_one_count"]) == 6,
        "naive_transport_certification_rejected": int(source[208]["transport_case_below_one_count"]) == 0,
        "expanded_cloud_rejected": int(source[209]["expanded_two_sided_green_count"]) == 0,
        "divisor_first_pivot_recorded": source[210]["route_coordinate"] == "finite_dual_channel_divisor_flow_open_renormalization",
        "all_level_divisor_limit": False,
    }
    coordinate = review_coordinate(statuses)
    finite_item_counts = {
        "rh202_endpoint_case_and_mode_records": int(source[202]["adjacent_case_count"]) + int(source[202]["mode_transport_count"]) + len(source[202]["endpoint_rows"]),
        "rh203_identity_and_physical_records": int(source[203]["resolvent_identity_case_count"]) + int(source[203]["channel_decomposition_case_count"]) + len(source[203]["inherited_transport_rows"]),
        "rh204_correspondence_records": int(source[204]["adjacent_case_count"]) + int(source[204]["synchronization_case_count"]),
        "rh205_identity_and_physical_records": int(source[205]["identity_case_count"]) + int(source[205]["physical_case_count"]),
        "rh206_cocycle_records": len(source[206]["rows"]) + len(source[206]["channel_rows"]) + len(source[206]["telescoping_rows"]),
        "rh207_newton_and_flow_records": int(source[207]["newton_identity_case_count"]) + int(source[207]["channel_case_count"]) + int(source[207]["scale_transition_count"]),
        "rh208_endpoint_and_transport_modes": sum(len(row["modes"]) for row in source[208]["endpoint_rows"]) + sum(len(row["modes"]) for row in source[208]["transport_rows"]),
        "rh209_rank_records": int(source[209]["rank_case_count"]),
        "rh210_counterexample_records": len(source[210]["counterexample_rows"]),
    }
    identity_failures = (
        int(source[203]["identity_failure_count"])
        + int(source[205]["identity_failure_count"])
        + int(source[207]["newton_identity_failure_count"])
    )
    return {
        "status": "rh211_ten_layer_transport_frontier_review",
        "route_coordinate": coordinate,
        "statuses": statuses,
        "macro_gates": strict_gate_vector(),
        "aggregate_finite_item_count": sum(finite_item_counts.values()),
        "finite_item_counts": finite_item_counts,
        "aggregate_identity_failure_count": identity_failures,
        "headline_metrics": {
            "maximum_haar_subspace_sine": max(source[202]["maximum_right_subspace_sine"], source[202]["maximum_left_subspace_sine"]),
            "maximum_oblique_projector_defect": source[202]["maximum_oblique_projector_defect"],
            "maximum_left_right_branch_mismatch": source[204]["maximum_left_right_branch_mismatch"],
            "maximum_common_scalar_residue_residual": source[206]["maximum_common_scalar_relative_residual"],
            "maximum_left_right_quartic_error": source[207]["maximum_left_right_coefficient_relative_error"],
            "maximum_adjacent_quartic_flow": source[207]["maximum_adjacent_scale_coefficient_relative_error"],
            "maximum_endpoint_isolation_ratio": source[208]["maximum_endpoint_isolation_ratio"],
            "minimum_transport_ratio": source[208]["minimum_transport_ratio"],
            "expanded_cloud_green_count": source[209]["expanded_two_sided_green_count"],
        },
        "next_target": {
            "paper": "RH-212",
            "objective": "densify the small-noise branch/divisor flow and test intrinsic coefficient renormalizations before returning to state transport",
        },
        "theorem_boundary": {
            "finite_transport_frontier_classified": True,
            "naive_haar_shell_map_rejected_finitely": True,
            "divisor_first_route_selected": True,
            "all_level_divisor_limit": False,
            "fredholm_determinant": False,
            "gate_A": False,
            "gates_B_to_E": False,
            "hilbert_polya_or_rh_conclusion": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/transport_frontier_review.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "items": payload["aggregate_finite_item_count"],
        "failures": payload["aggregate_identity_failure_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
