"""Physical source/observation bi-Krylov clock calibration."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH182 = PAPERS / "RH-182-finite-temporal-clock-physical-audit"
RH184 = PAPERS / "RH-184-balanced-biorthogonal-temporal-realization"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH182 / "src"),
    str(RH184 / "src"),
]

from bi_krylov_calibration import bi_krylov_window_metrics  # noqa: E402
from biorthogonal_clock import balanced_biorthogonal_frames  # noqa: E402
from finite_clock import normalized_orbit, projective_phase, temporal_synthesis  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from run_effective_rank_audit import HORIZONS, build_models  # noqa: E402


FULL_SIGMAS = (0.04, 0.02, 0.01)
RESIDUAL_GATE = 0.10


def candidate_lengths(sigma: float) -> tuple[int, ...]:
    rank = clock_rank(sigma, offset=2)
    return tuple(sorted({length for length in (rank - 3, rank - 4) if length >= 3}))


def summary(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = np.asarray([float(record[key]) for record in records])
    return {"minimum": float(values.min()), "median": float(np.median(values)), "maximum": float(values.max())}


def run(smoke: bool) -> dict[str, object]:
    started = time.perf_counter()
    sigmas = FULL_SIGMAS[:1] if smoke else FULL_SIGMAS
    records: list[dict[str, object]] = []
    groups = []
    for sigma in sigmas:
        dimension, models = build_models(sigma)
        rank = clock_rank(sigma, offset=2)
        endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
        for model in models:
            operator = np.asarray(model["operator"], dtype=float)
            source = np.asarray(model["source"], dtype=float)
            observation_seed = np.asarray(model["observation"], dtype=float).T
            _, right_norms, right_units = normalized_orbit(operator, source, endpoint)
            _, _, left_units = normalized_orbit(operator.T, observation_seed, endpoint)
            operator_norm = float(np.linalg.norm(operator, 2))
            for length in candidate_lengths(sigma):
                selected = []
                for start in range(endpoint - length + 1):
                    right_synthesis = temporal_synthesis(right_units, start, length)
                    left_synthesis = temporal_synthesis(left_units, start, length)
                    endpoint_index = start + length
                    phase = projective_phase(right_units[start], right_units[endpoint_index])
                    radius = float((right_norms[endpoint_index] / right_norms[start]) ** (1.0 / length))
                    metrics = bi_krylov_window_metrics(
                        operator,
                        right_synthesis,
                        left_synthesis,
                        source.shape,
                        target_radius=radius,
                        wrap_phase=phase,
                        balanced_builder=balanced_biorthogonal_frames,
                    )
                    record = {
                        "sigma": sigma,
                        "side": str(model["side"]),
                        "fine_dimension": dimension,
                        "operator_dimension": int(operator.shape[0]),
                        "source_columns": int(source.shape[1]),
                        "operator_norm": operator_norm,
                        "clock_rank": rank,
                        "candidate_length": length,
                        "candidate_offset": rank - length,
                        "start": start,
                        "endpoint": endpoint,
                        "source_cycle_radius": radius,
                        "orientation_mark_real": float(phase.real),
                        "orientation_mark_imag": float(phase.imag),
                        **metrics,
                    }
                    record["two_sided_0_10_gate"] = (
                        float(record["right_relative_residual"]) <= RESIDUAL_GATE
                        and float(record["left_relative_residual"]) <= RESIDUAL_GATE
                    )
                    selected.append(record)
                    records.append(record)
                groups.append({
                    "sigma": sigma,
                    "side": str(model["side"]),
                    "clock_rank": rank,
                    "candidate_length": length,
                    "candidate_offset": rank - length,
                    "window_count": len(selected),
                    "two_sided_0_10_gate_count": sum(bool(item["two_sided_0_10_gate"]) for item in selected),
                    "right_relative_residual": summary(selected, "right_relative_residual"),
                    "left_relative_residual": summary(selected, "left_relative_residual"),
                    "minimum_cross_singular_value": summary(selected, "minimum_cross_singular_value"),
                    "oblique_condition_number": summary(selected, "oblique_condition_number"),
                    "phase_grid_error": summary(selected, "compressed_cycle_phase_rms_error"),
                    "radial_grid_error": summary(selected, "compressed_cycle_radial_rms_error"),
                })
            print(json.dumps({
                "sigma": sigma,
                "side": model["side"],
                "candidate_lengths": candidate_lengths(sigma),
                "completed_windows": len(records),
            }, sort_keys=True), flush=True)

    local = [item for item in records if float(item["sigma"]) == 0.01 and int(item["candidate_length"]) == 4]
    alternatives = [item for item in records if int(item["candidate_length"]) == 3]
    return {
        "status": "rh185_physical_bi_krylov_cycle_calibration",
        "residual_gate": RESIDUAL_GATE,
        "scale_count": len(sigmas),
        "channel_count": 2 * len(sigmas),
        "window_count": len(records),
        "group_count": len(groups),
        "biorthogonality_failure_count": sum(float(item["biorthogonality_defect"]) > 1e-9 for item in records),
        "local_sigma_0_01_length_4_window_count": len(local),
        "local_sigma_0_01_length_4_two_sided_gate_count": sum(bool(item["two_sided_0_10_gate"]) for item in local),
        "length_3_two_sided_gate_count": sum(bool(item["two_sided_0_10_gate"]) for item in alternatives),
        "minimum_right_relative_residual": min(float(item["right_relative_residual"]) for item in records),
        "minimum_left_relative_residual": min(float(item["left_relative_residual"]) for item in records),
        "minimum_oblique_condition_number": min(float(item["oblique_condition_number"]) for item in records),
        "maximum_oblique_condition_number": max(float(item["oblique_condition_number"]) for item in records),
        "group_summaries": groups,
        "records": records,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "balanced_biorthogonal_formula": True,
            "finite_physical_bi_krylov_audit": not smoke,
            "local_sigma_0_01_length_4_candidate": sum(bool(item["two_sided_0_10_gate"]) for item in local) > 0,
            "unique_all_scale_calibration": False,
            "uniform_cross_angle": False,
            "outward_resolvent_certificate": False,
            "physical_interface_R": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "bi_krylov_smoke.json" if args.smoke else "bi_krylov_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "local_l4_gate_count": payload["local_sigma_0_01_length_4_two_sided_gate_count"],
        "length_3_gate_count": payload["length_3_two_sided_gate_count"],
        "conditioning_range": [payload["minimum_oblique_condition_number"], payload["maximum_oblique_condition_number"]],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
