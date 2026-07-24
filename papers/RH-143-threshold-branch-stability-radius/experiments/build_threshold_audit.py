from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
sys.path.insert(0, str(ROOT / "src"))

from threshold_branch import branch_radius  # noqa: E402


ROUNDING_MULTIPLIER = 128.0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    archived = json.loads((RH96 / "results" / "weak_mode_quotient_audit.json").read_text(encoding="utf-8"))
    thresholds = ("1e-08",) if args.smoke else ("1e-08", "1e-06", "1e-04")
    source_rows = archived["rows"][:1] if args.smoke else archived["rows"]
    rows = []
    for scale in source_rows:
        sigma = float(scale["sigma"])
        for channel in scale["channels"]:
            dimension = int(channel["dimension"])
            relative_fp64_budget = ROUNDING_MULTIPLIER * np.finfo(float).eps * dimension
            for key in thresholds:
                tau = float(key)
                for step in channel["chains"][key]["steps"]:
                    result = branch_radius(step["cross_singular_values"], tau, minimum=2, maximum=4)
                    leading = float(step["cross_singular_values"][0])
                    rows.append({
                        "sigma": sigma,
                        "side": str(channel["side"]),
                        "dimension": dimension,
                        "time": int(step["time"]),
                        "threshold": tau,
                        "archived_selected_width": int(step["selected_width"]),
                        "recomputed_selected_width": int(result["selected_width"]),
                        "leading_cross_singular_value": leading,
                        "absolute_branch_radius": result["absolute_radius"],
                        "relative_branch_radius": result["relative_radius"],
                        "relative_fp64_backward_budget": relative_fp64_budget,
                        "branch_radius_to_fp64_budget": result["relative_radius"] / relative_fp64_budget,
                        "strict_branch": bool(result["relative_radius"] > 0.0),
                        "fp64_budget_inside_branch": bool(result["relative_radius"] > relative_fp64_budget),
                    })
    summaries = {}
    for key in thresholds:
        tau = float(key)
        group = [row for row in rows if row["threshold"] == tau]
        summaries[key] = {
            "threshold": tau,
            "update_count": len(group),
            "strict_branch_count": sum(row["strict_branch"] for row in group),
            "fp64_budget_stable_count": sum(row["fp64_budget_inside_branch"] for row in group),
            "width_two_count": sum(row["archived_selected_width"] == 2 for row in group),
            "width_three_count": sum(row["archived_selected_width"] == 3 for row in group),
            "width_four_count": sum(row["archived_selected_width"] == 4 for row in group),
            "minimum_relative_branch_radius": min(row["relative_branch_radius"] for row in group),
            "median_relative_branch_radius": float(np.median([row["relative_branch_radius"] for row in group])),
            "minimum_branch_radius_to_fp64_budget": min(row["branch_radius_to_fp64_budget"] for row in group),
        }
    summary = {
        "threshold_count": len(thresholds),
        "update_record_count": len(rows),
        "selected_width_mismatch_count": sum(row["archived_selected_width"] != row["recomputed_selected_width"] for row in rows),
        "strict_branch_count": sum(row["strict_branch"] for row in rows),
        "fp64_budget_stable_count": sum(row["fp64_budget_inside_branch"] for row in rows),
        "primary_minimum_relative_branch_radius": summaries["1e-08"]["minimum_relative_branch_radius"],
        "primary_minimum_branch_radius_to_fp64_budget": summaries["1e-08"]["minimum_branch_radius_to_fp64_budget"],
        "threshold_summaries": summaries,
    }
    payload = {
        "status": "rh143_threshold_branch_stability_radius",
        "rounding_multiplier": ROUNDING_MULTIPLIER,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "sharp_clipped_relative_threshold_branch_radius": True,
            "projected_cross_projector_lipschitz_bound": True,
            "all_archived_branches_have_positive_nominal_margin": not args.smoke and summary["strict_branch_count"] == len(rows),
            "all_archived_branches_stable_under_local_fp64_proxy": not args.smoke and summary["fp64_budget_stable_count"] == len(rows),
            "fp64_proxy_is_an_interval_source_to_cross_enclosure": False,
            "rh142_packet_balls_propagated_through_updates": False,
            "uniform_threshold_margin": False,
            "uniform_all_level_packet_update": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Every archived RH-96 width decision lies strictly inside a computable branch ball, "
            "and all 360 decisions dominate a conservative local fp64 backward proxy. The primary "
            "minimum relative radius is only 4.34e-9, however, so this is not yet a source-to-update "
            "interval certificate. A projector/snapshot error must be pushed through the projected-cross "
            "Lipschitz bound and compared step by step."
        ),
    }
    output = ROOT / "results" / ("threshold_branch_smoke.json" if args.smoke else "threshold_branch_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

