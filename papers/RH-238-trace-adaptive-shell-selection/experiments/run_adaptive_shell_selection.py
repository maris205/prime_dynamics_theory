"""Select the first shell prefix whose order-12 log jet is at most sigma."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from adaptive_cloud import complex_payload, first_admissible_prefix  # noqa: E402
from resonance_cloud import conjugate_shells  # noqa: E402


MINIMUM_RANK = 4
RADIUS = 1.0


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    traces = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    trace_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in traces["endpoint_rows"]
    }
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        key = (float(endpoint["sigma"]), str(endpoint["side"]))
        trace_row = trace_rows[key]
        full = values(trace_row["full_trace_powers"])
        shells = conjugate_shells(values(endpoint["candidate_roots"]))
        result = first_admissible_prefix(
            shells,
            full,
            scalar(endpoint["perron_scaled"]),
            scalar(endpoint["parity_scaled"]),
            tolerance=float(endpoint["sigma"]),
            minimum_rank=MINIMUM_RANK,
            radius=RADIUS,
        )
        selected = result["selected"]
        if selected is None:
            rows.append({
                "sigma": endpoint["sigma"],
                "side": endpoint["side"],
                "selection_pass": False,
                "evaluated_prefix_count": len(result["rows"]),
                "admissible_prefix_count": 0,
            })
            continue
        cloud = selected["cloud"]
        moments = selected["moments"]
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "dimension": endpoint["dimension"],
            "tolerance_equals_sigma": endpoint["sigma"],
            "selection_pass": True,
            "current_atlas_rank": endpoint["actual_rank"],
            "adaptive_rank": int(cloud.size),
            "adaptive_minus_current_rank": int(cloud.size - int(endpoint["actual_rank"])),
            "adaptive_jet_norm": selected["jet_norm"],
            "tolerance_slack": float(endpoint["sigma"] - selected["jet_norm"]),
            "adaptive_roots": complex_payload(cloud),
            "adaptive_trace_powers": complex_payload(moments),
            "evaluated_prefix_count": len(result["rows"]),
            "admissible_prefix_count": len(result["admissible_rows"]),
            "best_available_jet_norm": min(row["jet_norm"] for row in result["rows"]),
            "complete_candidate_rank": int(sum(np.asarray(shell).size for shell in shells)),
        })
    passing = [row for row in rows if row["selection_pass"]]
    endpoint_map = {(float(row["sigma"]), row["side"]): row for row in passing}
    sigmas = [float(value) for value in atlas["sigmas"]]
    channel_rank_differences = [
        abs(endpoint_map[(sigma, "left")]["adaptive_rank"] - endpoint_map[(sigma, "right")]["adaptive_rank"])
        for sigma in sigmas
    ] if len(passing) == len(rows) else []
    return {
        "status": "rh238_trace_adaptive_shell_selection",
        "maximum_order": traces["maximum_order"],
        "minimum_rank": MINIMUM_RANK,
        "radius": RADIUS,
        "tolerance_rule": "epsilon_sigma=sigma",
        "endpoint_count": len(rows),
        "selection_pass_count": len(passing),
        "all_endpoints_pass": len(passing) == len(rows),
        "minimum_adaptive_rank": min(row["adaptive_rank"] for row in passing),
        "maximum_adaptive_rank": max(row["adaptive_rank"] for row in passing),
        "maximum_adaptive_jet_norm": max(row["adaptive_jet_norm"] for row in passing),
        "minimum_tolerance_slack": min(row["tolerance_slack"] for row in passing),
        "maximum_channel_rank_difference": max(channel_rank_differences, default=-1),
        "total_evaluated_prefix_count": sum(row["evaluated_prefix_count"] for row in rows),
        "minimum_admissible_prefix_count": min(row["admissible_prefix_count"] for row in passing),
        "maximum_admissible_prefix_count": max(row["admissible_prefix_count"] for row in passing),
        "endpoint_rows": rows,
        "theorem_boundary": {
            "minimal_shell_complete_finite_jet_selector_defined": True,
            "all_archived_endpoints_meet_epsilon_sigma_equals_sigma": len(passing) == len(rows),
            "asymptotic_candidate_availability": False,
            "all_order_trace_control": False,
            "deterministic_numerator_identification": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/adaptive_shell_selection.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload["selection_pass_count"],
        "rank_range": [payload["minimum_adaptive_rank"], payload["maximum_adaptive_rank"]],
        "maximum_jet_norm": payload["maximum_adaptive_jet_norm"],
        "maximum_channel_rank_difference": payload["maximum_channel_rank_difference"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
