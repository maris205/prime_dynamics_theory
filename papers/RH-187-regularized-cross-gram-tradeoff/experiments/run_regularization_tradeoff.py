"""Regularization sweep for every RH-185 physical bi-Krylov window."""

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

from cross_gram_regularization import clipped_cross_gram_budget, clipped_gate_infimum  # noqa: E402


MULTIPLIERS = (0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0, 128.0, 256.0, 512.0, 1024.0)


def run(smoke: bool) -> dict[str, object]:
    source_name = "bi_krylov_smoke.json" if smoke else "bi_krylov_audit.json"
    source = json.loads((RH185 / "results" / source_name).read_text(encoding="utf-8"))
    windows = []
    sweep_records = []
    for item in source["records"]:
        sigma = float(item["minimum_cross_singular_value"])
        epsilon = max(float(item["right_relative_residual"]), float(item["left_relative_residual"]))
        exact = clipped_gate_infimum(sigma, epsilon)
        sweeps = []
        for multiplier in MULTIPLIERS:
            budget = clipped_cross_gram_budget(sigma, epsilon, multiplier * sigma)
            sweeps.append(budget)
            sweep_records.append({
                "sigma": item["sigma"],
                "side": item["side"],
                "candidate_length": item["candidate_length"],
                "start": item["start"],
                "threshold_multiplier": multiplier,
                **budget,
            })
        best = min(sweeps, key=lambda record: float(record["combined_regularized_gate"]))
        windows.append({
            "sigma": item["sigma"],
            "side": item["side"],
            "candidate_length": item["candidate_length"],
            "start": item["start"],
            "minimum_cross_singular_value": sigma,
            "residual_level": epsilon,
            **exact,
            "best_grid_gate": best["combined_regularized_gate"],
            "best_grid_threshold": best["clipping_threshold"],
        })
    ratios = np.asarray([float(item["residual_to_cross_angle_ratio"]) for item in windows])
    return {
        "status": "rh187_regularized_cross_gram_tradeoff_audit",
        "window_count": len(windows),
        "threshold_multiplier_count": len(MULTIPLIERS),
        "sweep_case_count": len(sweep_records),
        "strict_regularized_contraction_count": sum(bool(item["strict_contraction_exists"]) for item in windows),
        "minimum_residual_to_cross_angle_ratio": float(ratios.min()),
        "median_residual_to_cross_angle_ratio": float(np.median(ratios)),
        "maximum_residual_to_cross_angle_ratio": float(ratios.max()),
        "minimum_grid_gate": min(float(item["combined_regularized_gate"]) for item in sweep_records),
        "windows": windows,
        "sweep_records": sweep_records,
        "theorem_boundary": {
            "clipped_cross_gram_formula": True,
            "exact_pareto_identity": True,
            "strict_gate_iff_residual_below_cross_angle": True,
            "finite_physical_sweep": not smoke,
            "regularization_closes_current_gate": any(bool(item["strict_contraction_exists"]) for item in windows),
            "all_regularizers_excluded": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "regularization_smoke.json" if args.smoke else "regularization_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "sweeps": payload["sweep_case_count"],
        "strict_contractions": payload["strict_regularized_contraction_count"],
        "minimum_ratio": payload["minimum_residual_to_cross_angle_ratio"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
