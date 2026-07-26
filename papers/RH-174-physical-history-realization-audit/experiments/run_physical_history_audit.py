"""Audit canonical history packets on all 130 archived reset snapshots."""

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
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH172 = PAPERS / "RH-172-canonical-polar-reset-memory-realization"
RH173 = PAPERS / "RH-173-normalized-history-cocycle"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH172 / "src"),
    str(RH173 / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "experiments"),
]

from half_log_rank import clock_rank  # noqa: E402
from history_audit import metric_summary, threshold_count  # noqa: E402
from history_cocycle import apply_history_cocycle, normalization_ratio, packet_residuals  # noqa: E402
from history_realization import (  # noqa: E402
    memory_gram,
    normalized_history_factor,
    polar_realization,
    spectral_formula_realization,
    subspace_distance,
    top_packet,
)
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402


ETA = 1.0 / 512.0


def operator_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, 2))


def channel_records(model: dict[str, object], sigma: float) -> list[dict[str, object]]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    rank = clock_rank(sigma, offset=2)
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])

    factors: list[np.ndarray] = []
    packets: list[np.ndarray] = []
    records = []
    for time_index in range(endpoint + 1):
        active_states = states[:time_index + 1]
        factor = normalized_history_factor(active_states, eta=ETA)
        gram = memory_gram(active_states, eta=ETA)
        values, source_packet = top_packet(gram, rank)
        stable_packet, positive = polar_realization(factor, source_packet)
        formula_packet = spectral_formula_realization(factor, source_packet, values)
        image = factor @ source_packet
        record: dict[str, object] = {
            "sigma": sigma,
            "side": str(model["side"]),
            "time": time_index,
            "history_blocks": time_index + 1,
            "operator_dimension": int(operator.shape[0]),
            "source_columns": int(source.shape[1]),
            "clock_rank": rank,
            "smallest_selected_eigenvalue": float(values[-1]),
            "selected_packet_condition_number": float(values[0] / values[-1]),
            "gram_factorization_operator_residual": operator_norm(factor.T @ factor - gram),
            "stable_polar_isometry_defect": operator_norm(stable_packet.T @ stable_packet - np.eye(rank)),
            "direct_formula_isometry_defect": operator_norm(formula_packet.T @ formula_packet - np.eye(rank)),
            "stable_polar_factorization_relative_residual": float(np.linalg.norm(image - stable_packet @ positive, "fro") / np.linalg.norm(image, "fro")),
            "direct_formula_to_stable_frame_residual": operator_norm(formula_packet - stable_packet),
        }
        if time_index:
            ratio = normalization_ratio(states[time_index - 1], states[time_index])
            transported_factor = apply_history_cocycle(factors[-1], operator, ratio, eta=ETA)
            old_packet = packets[-1]
            transported_packet = apply_history_cocycle(old_packet, operator, ratio, eta=ETA)
            transported_polar, _ = polar_realization(transported_packet, np.eye(rank))
            residuals = packet_residuals(old_packet, stable_packet, operator, ratio, eta=ETA)
            record.update({
                "normalization_ratio": ratio,
                "history_cocycle_relative_frobenius_residual": float(np.linalg.norm(factor - transported_factor, "fro") / np.linalg.norm(factor, "fro")),
                "transported_packet_condition_number": float(np.linalg.cond(transported_packet)),
                "transported_reset_subspace_distance": subspace_distance(transported_polar, stable_packet),
                "primal_relative_residual": float(residuals["primal_relative"]),
                "adjoint_relative_residual": float(residuals["adjoint_relative"]),
            })
        factors.append(factor)
        packets.append(stable_packet)
        records.append(record)
    return records


def run(smoke: bool) -> dict[str, object]:
    started = time.perf_counter()
    sigmas = SIGMAS[:1] if smoke else SIGMAS
    records = []
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            records.extend(channel_records(model, sigma))
            print(json.dumps({"sigma": sigma, "side": model["side"], "completed_records": len(records)}, sort_keys=True), flush=True)

    metric_names = (
        "gram_factorization_operator_residual",
        "stable_polar_isometry_defect",
        "direct_formula_isometry_defect",
        "stable_polar_factorization_relative_residual",
        "direct_formula_to_stable_frame_residual",
        "history_cocycle_relative_frobenius_residual",
        "transported_reset_subspace_distance",
        "primal_relative_residual",
        "adjoint_relative_residual",
        "selected_packet_condition_number",
        "transported_packet_condition_number",
    )
    update_records = [record for record in records if int(record["time"]) > 0]
    scale_summaries = []
    for sigma in sigmas:
        selected = [record for record in update_records if float(record["sigma"]) == sigma]
        scale_summaries.append({
            "sigma": sigma,
            "update_count": len(selected),
            "maximum_transport_distance": max(float(record["transported_reset_subspace_distance"]) for record in selected),
            "median_transport_distance": float(np.median([record["transported_reset_subspace_distance"] for record in selected])),
            "maximum_primal_relative_residual": max(float(record["primal_relative_residual"]) for record in selected),
            "minimum_adjoint_relative_residual": min(float(record["adjoint_relative_residual"]) for record in selected),
            "maximum_adjoint_relative_residual": max(float(record["adjoint_relative_residual"]) for record in selected),
        })
    return {
        "status": "rh174_physical_history_realization_audit",
        "eta": ETA,
        "scale_count": len(sigmas),
        "channel_count": 2 * len(sigmas),
        "snapshot_count": len(records),
        "update_count": len(update_records),
        "metric_summaries": {name: metric_summary(records, name) for name in metric_names},
        "threshold_counts": {
            "stable_polar_isometry_at_most_1e_12": threshold_count(records, "stable_polar_isometry_defect", 1e-12),
            "direct_formula_isometry_at_most_1e_8": threshold_count(records, "direct_formula_isometry_defect", 1e-8),
            "transport_distance_at_most_0_25": threshold_count(update_records, "transported_reset_subspace_distance", 0.25),
            "primal_residual_at_most_0_10": threshold_count(update_records, "primal_relative_residual", 0.10),
            "adjoint_residual_at_most_0_25": threshold_count(update_records, "adjoint_relative_residual", 0.25),
            "two_sided_residuals_at_most_0_25": sum(
                float(record["primal_relative_residual"]) <= 0.25 and float(record["adjoint_relative_residual"]) <= 0.25
                for record in update_records
            ),
            "transport_distance_at_least_0_90": sum(float(record["transported_reset_subspace_distance"]) >= 0.90 for record in update_records),
        },
        "scale_summaries": scale_summaries,
        "records": records,
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "finite_history_realization_formula": True,
            "finite_history_cocycle_formula": True,
            "floating_130_snapshot_audit": not smoke,
            "outward_interval_residual_certificate": False,
            "two_sided_history_packet_invariance": False,
            "history_to_rh80_transfer_intertwiner": False,
            "all_level_asymptotic_theorem": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "physical_history_smoke.json" if args.smoke else "physical_history_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "snapshot_count": payload["snapshot_count"],
        "update_count": payload["update_count"],
        "threshold_counts": payload["threshold_counts"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
