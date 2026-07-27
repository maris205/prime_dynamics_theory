"""Replay the RH-185 windows through conditioning-aware gates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
sys.path.insert(0, str(ROOT / "src"))

from oblique_conditioning import conditioned_residual_budget, principal_angle_degrees  # noqa: E402


def summarize(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = np.asarray([float(item[key]) for item in records])
    return {"minimum": float(values.min()), "median": float(np.median(values)), "maximum": float(values.max())}


def run(smoke: bool) -> dict[str, object]:
    source_name = "bi_krylov_smoke.json" if smoke else "bi_krylov_audit.json"
    source = json.loads((RH185 / "results" / source_name).read_text(encoding="utf-8"))
    records = []
    for item in source["records"]:
        budget = conditioned_residual_budget(
            item["minimum_cross_singular_value"],
            item["right_relative_residual"],
            item["left_relative_residual"],
        )
        records.append({
            "sigma": item["sigma"],
            "side": item["side"],
            "candidate_length": item["candidate_length"],
            "start": item["start"],
            "principal_angle_degrees": principal_angle_degrees(item["minimum_cross_singular_value"]),
            **budget,
        })
    local = [item for item in records if float(item["sigma"]) == 0.01 and int(item["candidate_length"]) == 4]
    return {
        "status": "rh186_oblique_conditioning_riesz_budget_audit",
        "window_count": len(records),
        "raw_two_sided_0_10_count": source["local_sigma_0_01_length_4_two_sided_gate_count"],
        "conditioned_contraction_success_count": sum(bool(item["conditioned_contraction_gate"]) for item in records),
        "local_l4_conditioned_success_count": sum(bool(item["conditioned_contraction_gate"]) for item in local),
        "amplified_maximum_residual": summarize(records, "amplified_maximum_residual"),
        "principal_angle_degrees": summarize(records, "principal_angle_degrees"),
        "oblique_condition_number": summarize(records, "oblique_condition_number"),
        "relative_residual_product": summarize(records, "relative_residual_product"),
        "records": records,
        "theorem_boundary": {
            "optimal_oblique_projection_norm": True,
            "conditioning_aware_residual_gate": True,
            "finite_physical_replay": not smoke,
            "conditioned_gate_closed": any(bool(item["conditioned_contraction_gate"]) for item in records),
            "sharp_directional_schur_product_tested": False,
            "physical_riesz_shell": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "oblique_conditioning_smoke.json" if args.smoke else "oblique_conditioning_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "conditioned_successes": payload["conditioned_contraction_success_count"],
        "minimum_amplified_residual": payload["amplified_maximum_residual"]["minimum"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
