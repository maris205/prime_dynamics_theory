"""Stress-test physical-covariance block residual envelopes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from covariance_envelope import (  # noqa: E402
    block_components,
    covariance_certificate,
    diagonal_cancellation_ledger,
    lyapunov_metric,
)


FULL_OUTPUT = ROOT / "results" / "covariance_envelope_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "covariance_envelope_smoke.json"
CANCELLATION_EPSILONS = (
    1.0,
    1.0e-4,
    1.0e-8,
    1.0e-12,
    1.0e-16,
    1.0e-20,
    1.0e-24,
    1.0e-28,
)
GENERIC_EPSILONS = (1.0, 1.0e-2, 1.0e-4, 1.0e-6, 1.0e-8, 1.0e-10)


def generic_models() -> list[dict[str, object]]:
    return [
        {
            "name": "nonnormal_three_packet_chain",
            "operator": np.asarray(
                [
                    [0.95, 0.42, 0.0, 0.0],
                    [0.0, 0.70, 0.38, 0.0],
                    [0.0, 0.0, 0.50, 0.31],
                    [0.0, 0.0, 0.0, 0.30],
                ],
                dtype=np.complex128,
            ),
            "sources": np.asarray(
                [
                    [0.0, 0.0, 0.0],
                    [0.05, -0.04, 0.02],
                    [0.20, 0.15, -0.10],
                    [1.00, -0.80, 0.60],
                ],
                dtype=np.complex128,
            ),
            "coefficients": np.ones(3, dtype=np.complex128),
            "horizon": 24,
            "depth": 1,
        },
        {
            "name": "six_mode_complex_phase_packets",
            "operator": np.diag(
                [0.99, 0.92, 0.75, 0.55, 0.35, 0.15]
            ).astype(np.complex128),
            "sources": np.asarray(
                [
                    [1.0, -0.8, 0.2],
                    [0.5, 0.4, -0.9],
                    [0.3, -0.1, 0.7],
                    [1.0, 0.8, 0.6],
                    [0.2, -0.3, 0.1],
                    [0.4, 0.2, -0.5],
                ],
                dtype=np.complex128,
            ),
            "coefficients": np.asarray(
                [1.0, np.exp(2.0j), np.exp(-1.2j)],
                dtype=np.complex128,
            ),
            "horizon": 20,
            "depth": 1,
        },
    ]


def cancellation_record(epsilons: tuple[float, ...]) -> dict[str, object]:
    rows = []
    for epsilon in epsilons:
        ledger = diagonal_cancellation_ledger(epsilon)
        rows.append(
            {
                "epsilon": ledger.epsilon,
                "physical_gain": ledger.physical_gain,
                "global_spectral_gain": ledger.global_spectral_gain,
                "weighted_trace_gain": ledger.weighted_trace_gain,
                "young_parameter": ledger.young_parameter,
            }
        )
    endpoint = diagonal_cancellation_ledger(epsilons[-1])
    return {
        "name": "exact_diagonal_cancellation",
        "dimension": 3,
        "source_columns": 2,
        "horizon": 32,
        "exact_scalar_reduction": True,
        "target_exact_energy": endpoint.target_exact_energy,
        "complement_exact_energy": endpoint.complement_exact_energy,
        "complement_center_energy": endpoint.complement_center_energy,
        "complement_residual_upper": endpoint.complement_residual_upper,
        "directional_optimal_gain": 1.0,
        "rows": rows,
    }


def generic_record(
    model: dict[str, object],
    epsilons: tuple[float, ...],
) -> dict[str, object]:
    operator = np.asarray(model["operator"])
    sources = np.asarray(model["sources"])
    coefficients = np.asarray(model["coefficients"])
    metric = lyapunov_metric(operator)
    components = block_components(
        operator,
        sources,
        metric,
        int(model["horizon"]),
        int(model["depth"]),
        coefficients,
    )
    rows = []
    for epsilon in epsilons:
        certificate = covariance_certificate(components, epsilon)
        rows.append(
            {
                "epsilon": epsilon,
                "physical_gain": certificate.physical_gain,
                "weighted_trace_gain": certificate.weighted_trace_gain,
                "global_spectral_gain": certificate.global_spectral_gain,
                "directional_optimal_gain": certificate.directional_optimal_gain,
                "young_parameter": certificate.young_parameter,
                "minimum_residual_weight": min(
                    certificate.residual_weights, default=1.0
                ),
                "minimum_slack_eigenvalue": certificate.minimum_slack_eigenvalue,
            }
        )
    return {
        "name": model["name"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(sources.shape[1]),
        "horizon": int(model["horizon"]),
        "depth": int(model["depth"]),
        "krylov_rank": components.krylov_rank,
        "exact_scalar_reduction": False,
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        cancellation_eps = CANCELLATION_EPSILONS[:2]
        generic_eps = GENERIC_EPSILONS[:2]
        generic = generic_models()[:1]
    else:
        cancellation_eps = CANCELLATION_EPSILONS
        generic_eps = GENERIC_EPSILONS
        generic = generic_models()
    models = [cancellation_record(cancellation_eps)]
    models.extend(generic_record(model, generic_eps) for model in generic)
    payload = {
        "status": "rh67_physical_covariance_block_envelope_pilot",
        "evidence_level": (
            "exact scalar cancellation reduction plus deterministic binary64 "
            "generic block models; no production packet computation"
        ),
        "models": models,
        "theorem_boundary": {
            "covariance_optimal_residual_weights": True,
            "covariance_optimal_young_parameter": True,
            "rank_one_directional_limit": True,
            "sharpness_global_size_tradeoff": True,
            "production_covariance_uniformity": False,
            "stage_A1_closed": False,
        },
        "limitations": [
            "A nearly rank-one physical covariance can make the globally valid PSD envelope large off the physical ray.",
            "The physically admissible coefficient covariance has not been derived from the production packet family.",
            "Uniform block depth and interval transfer remain open.",
        ],
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
                "model_count": len(models),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
