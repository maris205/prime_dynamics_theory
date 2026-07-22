"""Audit exact, perturbed, and clustered phase-depth families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from depth_barrier import (  # noqa: E402
    arc_phases,
    jittered_ring_phases,
    projection_audit,
    required_depth,
    uniform_ring_phases,
)


FULL_OUTPUT = ROOT / "results" / "depth_barrier_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "depth_barrier_smoke.json"
CONTRACTION = 0.995


def audit_dict(record) -> dict[str, object]:
    return {
        "depth": record.depth,
        "numerical_rank": record.numerical_rank,
        "projection_error": record.projection_error,
        "minimum_gram_eigenvalue": record.minimum_gram_eigenvalue,
        "target_correlation_norm": record.target_correlation_norm,
        "spectral_lower_bound": record.spectral_lower_bound,
        "mutual_coherence": record.mutual_coherence,
        "coherence_lower_bound": record.coherence_lower_bound,
    }


def exact_ring_records(dimensions: tuple[int, ...]) -> list[dict[str, object]]:
    rows = []
    for dimension in dimensions:
        horizon = dimension // 2
        candidate_depths = sorted(
            {
                1,
                2,
                4,
                8,
                16,
                horizon,
                horizon + 1,
            }
        )
        candidate_depths = [
            depth for depth in candidate_depths if depth <= horizon + 1
        ]
        phases = uniform_ring_phases(dimension)
        rows.append(
            {
                "dimension": dimension,
                "horizon": horizon,
                "contraction": CONTRACTION,
                "canonical_metric_condition_number": 1.0,
                "residual_contraction_before_full_closure": CONTRACTION,
                "required_depth_for_10_percent_error": required_depth(
                    phases, horizon, 0.1
                ),
                "depths": [
                    audit_dict(projection_audit(phases, horizon, depth))
                    for depth in candidate_depths
                ],
            }
        )
    return rows


def jitter_records(jitters: tuple[float, ...]) -> list[dict[str, object]]:
    dimension = 64
    horizon = 32
    rows = []
    for jitter in jitters:
        phases = jittered_ring_phases(dimension, jitter)
        rows.append(
            {
                "jitter_in_phase_cells": jitter,
                "dimension": dimension,
                "horizon": horizon,
                "required_depth_for_10_percent_error": required_depth(
                    phases, horizon, 0.1
                ),
                "depths": [
                    audit_dict(projection_audit(phases, horizon, depth))
                    for depth in (8, 16, 32, 33)
                ],
            }
        )
    return rows


def arc_records(widths: tuple[float, ...]) -> list[dict[str, object]]:
    dimension = 64
    horizon = 32
    rows = []
    for width in widths:
        phases = arc_phases(dimension, width)
        rows.append(
            {
                "arc_width_radians": width,
                "dimension": dimension,
                "horizon": horizon,
                "required_depth_for_10_percent_error": required_depth(
                    phases, horizon, 0.1
                ),
                "depth_4_error": projection_audit(
                    phases, horizon, 4
                ).projection_error,
                "depth_8_error": projection_audit(
                    phases, horizon, 8
                ).projection_error,
                "depth_16_error": projection_audit(
                    phases, horizon, 16
                ).projection_error,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        dimensions = (16,)
        jitters = (0.0, 0.05)
        widths = (0.0, 2.0 * np.pi)
    else:
        dimensions = (16, 32, 64, 128)
        jitters = (0.0, 0.05, 0.2, 0.5)
        widths = (0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 2.0 * np.pi)
    payload = {
        "status": "rh68_phase_coherence_block_depth_barrier_pilot",
        "evidence_level": (
            "deterministic binary64 phase-family audit; exact ring theorem "
            "and finite Arb DFT audit are separate"
        ),
        "exact_rings": exact_ring_records(dimensions),
        "jittered_rings": jitter_records(jitters),
        "phase_arcs": arc_records(widths),
        "theorem_boundary": {
            "exact_fourier_ring_orthogonality": True,
            "spectral_projection_lower_bound": True,
            "mutual_coherence_lower_bound": True,
            "universal_fixed_block_depth_ruled_out": True,
            "production_phase_compression": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "A fixed block depth cannot be justified from stability or "
            "spectral radius alone; the physical family must supply phase "
            "compression, effective-rank decay, or an admissible growing "
            "depth budget."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "ring_count": len(payload["exact_rings"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
