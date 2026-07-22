"""Audit block cross-column Krylov Gram certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from block_krylov_gram import (  # noqa: E402
    block_gram_certificate,
    directional_certificate,
    lyapunov_metric,
)


FULL_OUTPUT = ROOT / "results" / "block_gram_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "block_gram_smoke.json"


def models() -> list[dict[str, object]]:
    return [
        {
            "name": "cancelling_slow_pair",
            "operator": np.diag([0.995, 0.55, 0.2]).astype(
                np.complex128
            ),
            "sources": np.asarray(
                [[1.0, -1.0], [1.0, 1.0], [0.2, -0.2]],
                dtype=np.complex128,
            ),
            "coefficients": np.ones(2, dtype=np.complex128),
            "horizon": 32,
            "depths": (1,),
        },
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
            "depths": (1, 2),
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
            "depths": (1, 2),
        },
    ]


def positive_gain(upper: float, exact: float) -> float:
    return upper / max(exact, 1.0e-300)


def independent_column_upper(
    operator: np.ndarray,
    sources: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    depth: int,
    coefficients: np.ndarray,
) -> float:
    root_upper = 0.0
    for column in range(sources.shape[1]):
        certificate = directional_certificate(
            operator,
            sources[:, column : column + 1],
            metric,
            horizon,
            depth,
            np.ones(1),
        )
        root_upper += abs(coefficients[column]) * np.sqrt(
            certificate.upper_energy
        )
    return float(root_upper**2)


def depth_record(
    operator: np.ndarray,
    sources: np.ndarray,
    metric: np.ndarray,
    horizon: int,
    depth: int,
    coefficients: np.ndarray,
) -> dict[str, object]:
    block = block_gram_certificate(
        operator,
        sources,
        metric,
        horizon,
        depth,
    )
    directional = directional_certificate(
        operator,
        sources,
        metric,
        horizon,
        depth,
        coefficients,
    )
    gram_upper = max(
        0.0,
        float(
            np.real(
                np.vdot(
                    coefficients,
                    block.gram_envelope @ coefficients,
                )
            )
        ),
    )
    independent_upper = independent_column_upper(
        operator,
        sources,
        metric,
        horizon,
        depth,
        coefficients,
    )
    fused = directional_certificate(
        operator,
        (sources @ coefficients).reshape(-1, 1),
        metric,
        horizon,
        max(1, block.krylov_rank),
        np.ones(1),
    )
    envelope_slack = np.min(
        np.linalg.eigvalsh(
            0.5
            * (
                block.gram_envelope
                - block.exact_gram
                + (block.gram_envelope - block.exact_gram).conjugate().T
            )
        )
    )
    exact = directional.exact_energy
    return {
        "depth": depth,
        "krylov_rank": block.krylov_rank,
        "metric_contraction": block.metric_contraction,
        "source_reconstruction_norm": block.source_reconstruction_norm,
        "residual_relation_norm": block.residual_relation_norm,
        "exact_directional_energy": exact,
        "center_directional_energy": directional.center_energy,
        "directional_residual_radius": directional.residual_radius,
        "directional_upper": directional.upper_energy,
        "directional_gain": positive_gain(directional.upper_energy, exact),
        "uniform_gram_upper": gram_upper,
        "uniform_gram_gain": positive_gain(gram_upper, exact),
        "independent_column_upper": independent_upper,
        "independent_column_gain": positive_gain(independent_upper, exact),
        "rank_matched_fused_upper": fused.upper_energy,
        "rank_matched_fused_gain": positive_gain(fused.upper_energy, exact),
        "gram_envelope_minimum_slack_eigenvalue": float(envelope_slack),
        "trace_eta": block.trace_eta,
    }


def model_record(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"])
    sources = np.asarray(model["sources"])
    coefficients = np.asarray(model["coefficients"])
    metric = lyapunov_metric(operator)
    horizon = int(model["horizon"])
    return {
        "name": model["name"],
        "dimension": int(operator.shape[0]),
        "source_columns": int(sources.shape[1]),
        "horizon": horizon,
        "metric_condition_number": float(np.linalg.cond(metric)),
        "coefficient_norm": float(np.linalg.norm(coefficients)),
        "depths": [
            depth_record(
                operator,
                sources,
                metric,
                horizon,
                int(depth),
                coefficients,
            )
            for depth in model["depths"]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    selected = models()[:1] if args.smoke else models()
    payload = {
        "status": "rh66_block_cross_column_krylov_gram_pilot",
        "evidence_level": (
            "deterministic binary64 block-Krylov model audit; no production "
            "folded-Gaussian packet computation"
        ),
        "models": [model_record(model) for model in selected],
        "theorem_boundary": {
            "block_power_identity": True,
            "directional_center_radius_certificate": True,
            "uniform_psd_gram_envelope": True,
            "production_block_family_uniformity": False,
            "stage_A1_closed": False,
        },
        "limitations": [
            "The trace-optimal PSD envelope can remain conservative in a special cancelling coefficient direction.",
            "The pilot uses canonical finite-dimensional Lyapunov metrics rather than production observation-weighted block metrics.",
            "Uniform block depth and interval-certified physical packet transfer remain open.",
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
                "model_count": len(payload["models"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
