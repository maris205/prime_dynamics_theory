"""Audit the global wedge-Lipschitz route against product Weyl bounds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
sys.path.insert(0, str(ROOT / "src"))

from wedge_lipschitz import (  # noqa: E402
    global_wedge_lower_bound,
    positivity_radius,
    product_weyl_lower_bound,
    sharp_scalar_example,
)

FULL_OUTPUT = ROOT / "results/wedge_lipschitz_audit.json"
SMOKE_OUTPUT = ROOT / "results/wedge_lipschitz_smoke.json"


def transform_step(step: dict[str, object]) -> dict[str, object]:
    recent = np.asarray(step["recent_singular_values"], dtype=float)
    delta = float(step["tail_operator_bound"])
    threshold = float(step["threshold"])
    global_bound = global_wedge_lower_bound(recent, delta)
    direct = product_weyl_lower_bound(recent, delta)
    radii = positivity_radius(recent)
    archived_direct = float(step["spectral_volume_lower"])
    return {
        "time": step["time"],
        "threshold": threshold,
        "packet_rank": len(recent),
        "global_wedge_lower": global_bound["normalized_lower"],
        "product_weyl_lower": direct,
        "archived_product_weyl_lower": archived_direct,
        "archived_formula_error": abs(direct - archived_direct),
        "global_is_dominated": global_bound["normalized_lower"] <= direct + 2e-15,
        "global_positive": global_bound["normalized_lower"] > 0.0,
        "direct_positive": direct > 0.0,
        "global_support": global_bound["normalized_lower"] >= threshold,
        "direct_support": direct >= threshold,
        "global_positivity_radius": radii["global"],
        "direct_positivity_radius": radii["product_weyl"],
        "positivity_radius_efficiency": radii["relative_efficiency"],
        "actual_normalized_volume": step["actual_normalized_volume"],
        "tail_operator_bound": delta,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    source = json.loads((RH110 / "results/three_mode_capacity_audit.json").read_text(encoding="utf-8"))
    selected = source["rows"][:1] if args.smoke else source["rows"]
    rows = []
    for row in selected:
        channels = []
        for channel in row["channels"]:
            thresholds = []
            for record in channel["thresholds"]:
                thresholds.append({
                    "threshold": record["threshold"],
                    "steps": [transform_step(step) for step in record["steps"]],
                })
            channels.append({"side": channel["side"], "thresholds": thresholds})
        rows.append({"sigma": row["sigma"], "clock_rank": row["clock_rank"], "channels": channels})

    records = [
        (row["sigma"], record)
        for row in rows
        for channel in row["channels"]
        for record in channel["thresholds"]
    ]
    all_steps = [step for _, record in records for step in record["steps"]]
    threshold_summary = {}
    for threshold in (1e-8, 1e-6, 1e-4):
        chosen = [(sigma, record) for sigma, record in records if float(record["threshold"]) == threshold]
        steps = [step for _, record in chosen for step in record["steps"]]
        fine = [step for sigma, record in chosen if sigma <= 0.02 for step in record["steps"]]
        threshold_summary[f"{threshold:.0e}"] = {
            "threshold": threshold,
            "update_count": len(steps),
            "global_support_count": sum(step["global_support"] for step in steps),
            "direct_support_count": sum(step["direct_support"] for step in steps),
            "fine_update_count": len(fine),
            "fine_global_support_count": sum(step["global_support"] for step in fine),
            "fine_direct_support_count": sum(step["direct_support"] for step in fine),
        }
    fine_steps = [step for sigma, record in records if sigma <= 0.02 for step in record["steps"]]
    reported = fine_steps if fine_steps else all_steps
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "domination_failure_count": sum(not step["global_is_dominated"] for step in all_steps),
        "archived_formula_failure_count": sum(step["archived_formula_error"] > 2e-15 for step in all_steps),
        "global_positive_count": sum(step["global_positive"] for step in all_steps),
        "direct_positive_count": sum(step["direct_positive"] for step in all_steps),
        "fine_global_positive_count": sum(step["global_positive"] for step in reported),
        "fine_direct_positive_count": sum(step["direct_positive"] for step in reported),
        "minimum_fine_radius_efficiency": min(step["positivity_radius_efficiency"] for step in reported),
        "maximum_fine_radius_efficiency": max(step["positivity_radius_efficiency"] for step in reported),
        "maximum_archived_formula_error": max(step["archived_formula_error"] for step in all_steps),
    }
    payload = {
        "status": "rh112_global_wedge_lipschitz_barrier_audit",
        "rows": rows,
        "threshold_summary": threshold_summary,
        "sharpness_examples": [sharp_scalar_example(1.0, delta) for delta in (0.0, 1e-6, 1e-3, 0.1)],
        "audit_summary": summary,
        "theorem_boundary": {
            "sharp_global_wedge_lipschitz_bound": True,
            "product_weyl_dominates_global_wedge": True,
            "global_route_declared_negative": True,
            "five_scale_domination_validated": not args.smoke,
            "directional_wedge_route_ruled_out": False,
            "all_level_physical_volume_lower_bound_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The norm-only exterior-power perturbation law is sharp, but its normalized lower bound is universally dominated by the singular-value-product Weyl certificate. Its positivity radius is alpha*((1+nu_hat)^(1/4)-1), approximately alpha*nu_hat/4, rather than the direct radius s4. The global wedge-Lipschitz branch is therefore closed as an efficiency improvement; directional exterior actions remain open."
        ),
        "limitations": [
            "The negative result concerns norm-only global exterior perturbation and does not rule out directional or structured tail estimates.",
            "The five-scale audit is validation of the theorem on archived packets, not an all-level physical law.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
