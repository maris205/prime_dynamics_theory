"""Deterministic audit of the canonical reset-memory polar identities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from history_realization import (  # noqa: E402
    memory_gram,
    normalized_history_factor,
    polar_realization,
    subspace_distance,
    top_packet,
)


def operator_norm(matrix: np.ndarray) -> float:
    return float(np.linalg.norm(matrix, 2))


def unitary(rng: np.random.Generator, dimension: int) -> np.ndarray:
    raw = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    frame, diagonal = np.linalg.qr(raw)
    phases = np.diag(diagonal)
    phases = phases / np.where(np.abs(phases) == 0.0, 1.0, np.abs(phases))
    return frame @ np.diag(phases.conj())


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(172)
    dimensions = (6,) if smoke else (6, 9, 12)
    horizons = (1, 3) if smoke else (1, 2, 4, 7)
    trials = 2 if smoke else 8
    records = []
    for dimension in dimensions:
        output_dimension = dimension + 3
        for horizon in horizons:
            for rank in (1, min(3, dimension // 2)):
                for trial in range(trials):
                    source = rng.normal(size=(output_dimension, dimension)) + 1j * rng.normal(size=(output_dimension, dimension))
                    operator = rng.normal(size=(output_dimension, output_dimension)) / np.sqrt(3.0 * output_dimension)
                    states = [source]
                    for _ in range(horizon - 1):
                        states.append(operator @ states[-1])
                    factor = normalized_history_factor(states)
                    gram = memory_gram(states)
                    values, packet = top_packet(gram, rank)
                    realized, positive = polar_realization(factor, packet)

                    source_gauge = unitary(rng, dimension)
                    gauged_states = [state @ source_gauge for state in states]
                    gauged_factor = normalized_history_factor(gauged_states)
                    gauged_packet = source_gauge.conj().T @ packet
                    gauged_realized, _ = polar_realization(gauged_factor, gauged_packet)

                    packet_gauge = unitary(rng, rank)
                    rotated_realized, _ = polar_realization(factor, packet @ packet_gauge)
                    image = factor @ packet
                    records.append({
                        "dimension": dimension,
                        "horizon": horizon,
                        "rank": rank,
                        "trial": trial,
                        "gram_factorization_residual": operator_norm(factor.conj().T @ factor - gram),
                        "isometry_defect": operator_norm(realized.conj().T @ realized - np.eye(rank)),
                        "polar_factorization_relative_residual": float(np.linalg.norm(image - realized @ positive, "fro") / np.linalg.norm(image, "fro")),
                        "source_gauge_frame_residual": operator_norm(realized - gauged_realized),
                        "packet_gauge_equivariance_residual": operator_norm(rotated_realized - realized @ packet_gauge),
                        "packet_gauge_projector_distance": subspace_distance(rotated_realized, realized),
                        "selected_condition_number": float(values[0] / values[-1]),
                    })
    metrics = (
        "gram_factorization_residual",
        "isometry_defect",
        "polar_factorization_relative_residual",
        "source_gauge_frame_residual",
        "packet_gauge_equivariance_residual",
        "packet_gauge_projector_distance",
    )
    return {
        "status": "rh172_canonical_polar_identity_audit",
        "case_count": len(records),
        "maximum_residuals": {metric: max(record[metric] for record in records) for metric in metrics},
        "maximum_selected_condition_number": max(record["selected_condition_number"] for record in records),
        "records": records,
        "theorem_boundary": {
            "finite_history_gram_factorization": True,
            "canonical_polar_packet_isometry": True,
            "source_coordinate_invariance": True,
            "physical_transfer_space_identification": False,
            "all_level_limit": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "polar_identity_smoke.json" if args.smoke else "polar_identity_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "case_count": payload["case_count"], **payload["maximum_residuals"]}, sort_keys=True))


if __name__ == "__main__":
    main()
