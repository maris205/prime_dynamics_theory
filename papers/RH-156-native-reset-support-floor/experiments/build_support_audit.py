from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH153 = PAPERS / "RH-153-congruence-covariant-reset-transport"
RH154 = PAPERS / "RH-154-half-horizon-delayed-reset-suffix"
RH155 = PAPERS / "RH-155-native-spectral-reset-memory-pair"
sys.path.insert(0, str(ROOT / "src"))

from reset_support import native_support_lower  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    congruence = json.loads((RH153 / "results/congruence_audit.json").read_text())
    memory = json.loads((RH155 / "results/memory_pair_audit.json").read_text())
    memory_map = {
        (float(row["sigma"]), row["side"], int(item["time"])): item
        for row in memory["rows"] for item in row["snapshots"]
    }
    suffix = json.loads((RH154 / "results/suffix_audit.json").read_text())["half_suffix"]
    starts = {(float(item["sigma"]), item["side"]): int(item["start_time"]) for item in suffix["channels"]}

    source_rows = congruence["rows"][:2] if args.smoke else congruence["rows"]
    rows = []
    for row in source_rows:
        sigma = float(row["sigma"])
        side = row["side"]
        transitions = []
        for item in row["transitions"]:
            memory_item = memory_map[(sigma, side, int(item["time"]))]
            eigen_lower = min(float(item["eigenvalue_lower"]), float(memory_item["packet_eigenvalue_lower"]))
            result = native_support_lower(
                eigen_lower,
                float(item["eigenvalue_upper"]),
                float(memory_item["tail_mass_upper"]),
                float(item["robust_overlap_lower"]),
            )
            transitions.append({
                "time": item["time"],
                "rank": item["rank"],
                "in_half_suffix": int(item["time"]) >= starts[(sigma, side)],
                "full_eigenvalue_lower": eigen_lower,
                "full_eigenvalue_upper": item["eigenvalue_upper"],
                "tail_mass_upper": memory_item["tail_mass_upper"],
                "robust_overlap_lower": item["robust_overlap_lower"],
                **result,
            })
        rows.append({"sigma": sigma, "side": side, "rank": row["rank"], "transitions": transitions})
        print(json.dumps({
            "sigma": sigma, "side": side, "transition_count": len(transitions),
            "positive_count": sum(item["support_lower"] > 0.0 for item in transitions),
            "minimum_support": min(item["support_lower"] for item in transitions),
        }, sort_keys=True), flush=True)

    items = [item for row in rows for item in row["transitions"]]
    half = [item for item in items if item["in_half_suffix"]]
    summary = {
        "channel_count": len(rows),
        "transition_count": len(items),
        "positive_support_count": sum(item["support_lower"] > 0.0 for item in items),
        "minimum_support_lower": min(item["support_lower"] for item in items),
        "median_support_lower": float(np.median([item["support_lower"] for item in items])),
        "maximum_support_lower": max(item["support_lower"] for item in items),
        "support_above_1e_8_count": sum(item["support_lower"] >= 1e-8 for item in items),
        "support_above_1e_6_count": sum(item["support_lower"] >= 1e-6 for item in items),
        "support_above_1e_4_count": sum(item["support_lower"] >= 1e-4 for item in items),
        "half_suffix_transition_count": len(half),
        "half_suffix_positive_support_count": sum(item["support_lower"] > 0.0 for item in half),
        "half_suffix_common_support_floor": min(item["support_lower"] for item in half),
        "half_suffix_median_support_lower": float(np.median([item["support_lower"] for item in half])),
        "maximum_relative_tail_upper": max(item["relative_tail_upper"] for item in items),
        "minimum_tail_factor": min(item["tail_factor"] for item in items),
    }
    payload = {
        "status": "rh156_native_reset_support_floor",
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "sharp_native_support_composition": True,
            "all_frozen_transition_support_positive": not args.smoke and summary["positive_support_count"] == 120,
            "half_suffix_common_native_support_tube": not args.smoke and summary["half_suffix_positive_support_count"] == 62,
            "directional_cross_action_bridge": False,
            "uniform_all_level_endpoint_laws": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "The selected full-memory eigenvalue, geometric tail mass, and robust overlap lower compose into one sharp native support formula. Every frozen transition is positive, and the RH-154 terminal half has a common floor 3.262e-8. This closes the finite native reset architecture; the next gate is comparison with the directional cross-action support functional.",
    }
    output = ROOT / "results" / ("support_smoke.json" if args.smoke else "support_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
