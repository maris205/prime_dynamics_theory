"""Audit predeclared finite temporal clocks on the physical frozen models."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src")]

from finite_clock import clock_window_metrics, normalized_orbit  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from run_effective_rank_audit import HORIZONS, build_models  # noqa: E402


FULL_SIGMAS = (0.04, 0.02, 0.01)
GATE = 0.25


def candidate_lengths(sigma: float) -> tuple[int, ...]:
    rank = clock_rank(sigma, offset=2)
    return tuple(sorted({length for length in (rank - 3, rank - 4) if length >= 3}))


def cloud_rows() -> dict[float, dict[str, str]]:
    with (RH15 / "results/cloud_summary.csv").open(newline="", encoding="utf-8") as stream:
        return {float(row["sigma"]): row for row in csv.DictReader(stream)}


def metric_summary(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = np.asarray([float(record[key]) for record in records], dtype=float)
    return {
        "minimum": float(np.min(values)),
        "median": float(np.median(values)),
        "maximum": float(np.max(values)),
    }


def run(smoke: bool) -> dict[str, object]:
    started = time.perf_counter()
    sigmas = FULL_SIGMAS[:1] if smoke else FULL_SIGMAS
    clouds = cloud_rows()
    records: list[dict[str, object]] = []
    group_summaries = []
    for sigma in sigmas:
        dimension, models = build_models(sigma)
        rank = clock_rank(sigma, offset=2)
        lengths = candidate_lengths(sigma)
        endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
        for model in models:
            operator = np.asarray(model["operator"], dtype=float)
            source = np.asarray(model["source"], dtype=float)
            _, norms, units = normalized_orbit(operator, source, endpoint)
            for length in lengths:
                selected = []
                for start in range(endpoint - length + 1):
                    record = {
                        "sigma": sigma,
                        "side": str(model["side"]),
                        "fine_dimension": dimension,
                        "operator_dimension": int(operator.shape[0]),
                        "source_columns": int(source.shape[1]),
                        "clock_rank": rank,
                        "candidate_offset": rank - length,
                        "refresh_endpoint": endpoint,
                        **clock_window_metrics(operator, norms, units, start, length),
                    }
                    cloud = clouds.get(sigma)
                    if cloud is not None:
                        target_radius = float(cloud["cloud_radial_mean"])
                        threshold_radius = float(cloud["threshold_radius"])
                        record.update({
                            "archived_cloud_degree": int(cloud["effective_cloud_degree"]),
                            "archived_cloud_cycle_length": int(cloud["effective_cloud_degree"]) + 1,
                            "archived_cloud_radial_mean": target_radius,
                            "archived_threshold_radius": threshold_radius,
                            "cycle_to_cloud_radial_mean_error": float(record["cycle_radius"]) - target_radius,
                            "cycle_to_threshold_radius_error": float(record["cycle_radius"]) - threshold_radius,
                        })
                    selected.append(record)
                    records.append(record)
                group_summaries.append({
                    "sigma": sigma,
                    "side": str(model["side"]),
                    "clock_rank": rank,
                    "candidate_length": length,
                    "candidate_offset": rank - length,
                    "window_count": len(selected),
                    "negative_orientation_count": sum(float(item["orientation_mark_real"]) < 0.0 for item in selected),
                    "projective_wrap": metric_summary(selected, "projective_wrap_distance"),
                    "primal_residual": metric_summary(selected, "primal_relative_residual"),
                    "adjoint_residual": metric_summary(selected, "adjoint_relative_residual"),
                    "cycle_radius": metric_summary(selected, "cycle_radius"),
                    "three_gate_success_count": sum(
                        float(item["projective_wrap_distance"]) <= GATE
                        and float(item["primal_relative_residual"]) <= GATE
                        and float(item["adjoint_relative_residual"]) <= GATE
                        for item in selected
                    ),
                })
            print(json.dumps({
                "sigma": sigma,
                "side": model["side"],
                "clock_rank": rank,
                "candidate_lengths": lengths,
                "completed_windows": len(records),
            }, sort_keys=True), flush=True)

    formula_failure_count = sum(
        float(record["cycle_radius_formula_residual"]) > 1e-10
        or float(record["cycle_radial_rms_error"]) > 1e-10
        or float(record["cycle_phase_rms_error"]) > 1e-10
        or float(record["frame_isometry_defect"]) > 1e-10
        for record in records
    )
    three_gate = sum(
        float(record["projective_wrap_distance"]) <= GATE
        and float(record["primal_relative_residual"]) <= GATE
        and float(record["adjoint_relative_residual"]) <= GATE
        for record in records
    )
    return {
        "status": "rh182_finite_temporal_clock_physical_audit",
        "gate_threshold": GATE,
        "scale_count": len(sigmas),
        "channel_count": 2 * len(sigmas),
        "group_count": len(group_summaries),
        "window_count": len(records),
        "formula_failure_count": formula_failure_count,
        "three_gate_success_count": three_gate,
        "minimum_projective_wrap_distance": min(float(item["projective_wrap_distance"]) for item in records),
        "minimum_primal_relative_residual": min(float(item["primal_relative_residual"]) for item in records),
        "minimum_adjoint_relative_residual": min(float(item["adjoint_relative_residual"]) for item in records),
        "negative_orientation_count": sum(float(item["orientation_mark_real"]) < 0.0 for item in records),
        "group_summaries": group_summaries,
        "records": records,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "exact_weighted_cycle_spectrum": True,
            "exact_time_domain_length_selection": True,
            "finite_floating_physical_audit": not smoke,
            "orthogonal_clock_three_gate_survives": three_gate > 0,
            "all_level_cycle_rejection": False,
            "biorthogonal_clock_tested": False,
            "physical_interface_R": False,
            "gate_A": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "temporal_clock_smoke.json" if args.smoke else "temporal_clock_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "formula_failures": payload["formula_failure_count"],
        "three_gate_successes": payload["three_gate_success_count"],
        "minimum_adjoint_residual": payload["minimum_adjoint_relative_residual"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
