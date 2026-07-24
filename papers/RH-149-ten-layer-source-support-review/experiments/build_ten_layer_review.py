from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from route_review import composition_closed, missing_interfaces, priority_score  # noqa: E402


UPSTREAM = {
    number: next(PAPERS.glob(f"RH-{number}-*/results/summary.json"))
    for number in range(140, 149)
}
RH139 = PAPERS / "RH-139-ten-layer-controlled-viability-review/results/summary.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def claim_violation(boundary: dict[str, object]) -> bool:
    return any(bool(boundary.get(key, False)) for key in (
        "riemann_hypothesis", "hilbert_polya_operator", "stage_A", "uniform_stage_A_closed"
    ))


def layer_records() -> tuple[list[dict[str, object]], dict[int, dict[str, object]]]:
    summaries = {number: json.loads(path.read_text()) for number, path in UPSTREAM.items()}
    kinds = {
        140: "constructive", 141: "mixed", 142: "constructive", 143: "constructive",
        144: "mixed", 145: "mixed", 146: "mixed", 147: "constructive", 148: "synthesis",
    }
    contributions = {
        140: "sharp normalized snapshot enclosure",
        141: "gap-stable packet theorem and universal-radius wall",
        142: "10/10 factorized Arb packet closure",
        143: "sharp clipped-threshold branch radius",
        144: "exact backward controlled kernels and two genuine finite obstructions",
        145: "delayed-start theorem and isolation of the coarse bad births",
        146: "sharp projective base recurrence; direct product route is lossy",
        147: "correlated support tube and signed cocycle",
        148: "conditional source-to-support composition and three open interfaces",
    }
    rows = []
    for number in range(140, 149):
        archive = UPSTREAM[number].with_name("archive_verification.json")
        boundary = summaries[number]["program_boundary"]
        rows.append({
            "paper": number,
            "kind": kinds[number],
            "contribution": contributions[number],
            "summary_path": str(UPSTREAM[number].relative_to(PAPERS.parent)),
            "summary_sha256": sha(UPSTREAM[number]),
            "archive_verified": archive.exists() and json.loads(archive.read_text())["status"].startswith(f"all_rh{number}_"),
            "claim_boundary_violation": claim_violation(boundary),
        })
    return rows, summaries


def truth_table() -> list[dict[str, object]]:
    names = ("E-source", "E-update", "E-cocycle")
    rows = []
    for values in itertools.product((False, True), repeat=3):
        state = dict(zip(names, values))
        rows.append({
            **state,
            "composition_closed": composition_closed(state),
            "missing": list(missing_interfaces(state)),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    layers, summaries = layer_records()
    previous = json.loads(RH139.read_text())
    table = truth_table()
    priorities = [
        {"interface": "E-update", "tractability": 5, "falsification_value": 5, "dependency_leverage": 5},
        {"interface": "E-cocycle", "tractability": 3, "falsification_value": 5, "dependency_leverage": 5},
        {"interface": "E-source", "tractability": 2, "falsification_value": 4, "dependency_leverage": 5},
    ]
    for item in priorities:
        item["priority_score"] = priority_score(item["tractability"], item["falsification_value"], item["dependency_leverage"])
    priorities.sort(key=lambda item: item["priority_score"], reverse=True)
    review_148 = json.loads(UPSTREAM[148].read_text())
    summary = {
        "upstream_paper_count": len(layers),
        "upstream_archive_verification_count": sum(row["archive_verified"] for row in layers),
        "claim_boundary_violation_count": sum(row["claim_boundary_violation"] for row in layers),
        "constructive_layer_count": sum(row["kind"] == "constructive" for row in layers),
        "mixed_layer_count": sum(row["kind"] == "mixed" for row in layers),
        "synthesis_layer_count": sum(row["kind"] == "synthesis" for row in layers),
        "previous_frontier_packet_count": 4,
        "minimal_open_interface_count": 3,
        "truth_table_case_count": len(table),
        "truth_table_closed_case_count": sum(row["composition_closed"] for row in table),
        "factorized_packet_certified_count": summaries[142]["audit"]["packet_certified_count"],
        "strict_threshold_branch_count": summaries[143]["audit"]["strict_branch_count"],
        "outward_transition_count": review_148["audit"]["outward_residual_transition_count"],
        "positive_tube_chain_count": summaries[147]["audit"]["positive_tube_chain_count"],
        "clean_suffix_chain_count": summaries[145]["audit"]["first_clean_suffix_chain_count"],
        "projective_summability_finite_trend_supported": summaries[146]["audit"]["finite_trend_supports_projective_summability"],
        "median_correlated_reanchoring_gain_orders": math.log10(summaries[147]["audit"]["median_reanchoring_gain_over_projective"]),
        "minimum_correlated_reanchoring_gain_orders": math.log10(summaries[147]["audit"]["minimum_reanchoring_gain_over_projective"]),
        "maximum_correlated_reanchoring_gain_orders": math.log10(summaries[147]["audit"]["maximum_reanchoring_gain_over_projective"]),
        "top_priority_interface": priorities[0]["interface"],
        "top_priority_score": priorities[0]["priority_score"],
    }
    payload = {
        "status": "rh149_ten_layer_source_support_review",
        "previous_rh139_summary_path": str(RH139.relative_to(PAPERS.parent)),
        "previous_rh139_summary_sha256": sha(RH139),
        "layers": layers,
        "truth_table": table,
        "priority_ranking": priorities,
        "frontier_mapping": {
            "RH-139 P_E source enclosure": ["E-source", "E-update"],
            "RH-139 P_O outward radii": ["E-update"],
            "RH-139 P_V controlled viability": ["E-cocycle"],
            "RH-139 P_B positive base liminf": ["E-cocycle"],
        },
        "route_decisions": {
            "primary": "correlated support cocycle with interval reanchoring",
            "fallback": "summable projective Gram variation",
            "next_experiment": "propagate RH-142 packet balls through RH-143 recursive updates",
            "stop_condition": "any branch-radius exhaustion or outward interval blow-up is recorded as an obstruction",
        },
        "audit_summary": summary,
        "theorem_boundary": {
            "three_interface_sufficiency": True,
            "inclusion_minimal_three_interface_frontier": True,
            "correlated_cocycle_is_primary_route": True,
            "projective_summability_is_fallback_route": True,
            "nine_layer_archive_review_complete": not args.smoke,
            "finite_end_to_end_interval_bridge_closed": False,
            "all_level_directional_support_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "RH-140--RH-149 reduces the directional program to an inclusion-minimal three-interface frontier. The next highest-value task is E-update: interval transport from certified source packets through thresholded recursion into the outward assembly. The correlated support cocycle is primary; unsigned projective summability remains a rigorous but empirically unsupported fallback.",
    }
    output = ROOT / "results" / ("ten_layer_source_support_smoke.json" if args.smoke else "ten_layer_source_support_review.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

