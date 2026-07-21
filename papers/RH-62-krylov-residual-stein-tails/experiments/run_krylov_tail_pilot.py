"""Krylov residual pilot on calibrated slow/fast finite-dimensional models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from krylov_tail import geometric_power_upper, krylov_power_certificate  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "krylov_tail_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "krylov_tail_smoke.json"
HORIZONS = (0, 1, 4, 8, 16, 32, 64)


def models() -> list[dict[str, object]]:
    return [
        {
            "name": "rh61_left_calibrated_slow_fast",
            "description": (
                "Two-mode surrogate using the RH-61 left endpoint gap; "
                "the source is mostly in the fast direction."
            ),
            "operator": np.diag([0.993861320134583, 0.2]).astype(
                np.complex128
            ),
            "source": np.asarray([5.0e-4, 1.0], dtype=np.complex128),
            "kappa": 1.0,
        },
        {
            "name": "rh60_two_block",
            "description": (
                "The two-scalar-block model used by the RH-60 Arb audit."
            ),
            "operator": np.asarray(
                [[0.2, 0.3], [0.0, 0.7]], dtype=np.complex128
            ),
            "source": np.asarray([0.0, 0.4], dtype=np.complex128),
            "kappa": 1.0,
        },
        {
            "name": "nonnormal_four_step_chain",
            "description": (
                "A four-dimensional upper-triangular stress model with "
                "feed-forward transient coupling."
            ),
            "operator": np.asarray(
                [
                    [0.95, 0.42, 0.0, 0.0],
                    [0.0, 0.70, 0.38, 0.0],
                    [0.0, 0.0, 0.50, 0.31],
                    [0.0, 0.0, 0.0, 0.30],
                ],
                dtype=np.complex128,
            ),
            "source": np.asarray([0.0, 0.0, 0.0, 1.0], dtype=np.complex128),
            "kappa": 1.0,
        },
    ]


def certificate_record(
    operator: np.ndarray,
    source: np.ndarray,
    horizon: int,
    dimension: int,
    kappa: float,
) -> dict[str, object]:
    certificate = krylov_power_certificate(
        operator,
        source,
        horizon,
        dimension,
    )
    geometric = geometric_power_upper(
        certificate.operator_norm,
        source,
        horizon,
    )
    return {
        "horizon": horizon,
        "krylov_dimension": certificate.krylov_dimension,
        "exact_norm": certificate.exact_norm,
        "geometric_upper": geometric,
        "krylov_projected_norm": certificate.projected_norm,
        "krylov_residual_bound": certificate.residual_bound,
        "krylov_upper": certificate.upper_bound,
        "stein_geometric_upper": float(np.sqrt(kappa) * geometric),
        "stein_krylov_upper": float(np.sqrt(kappa) * certificate.upper_bound),
        "krylov_over_exact": certificate.upper_bound
        / max(certificate.exact_norm, 1.0e-300),
        "geometric_over_exact": geometric
        / max(certificate.exact_norm, 1.0e-300),
        "arnoldi_residual_norm": certificate.arnoldi_residual_norm,
        "breakdown": certificate.breakdown,
    }


def model_record(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"])
    source = np.asarray(model["source"])
    kappa = float(model["kappa"])
    records = {
        str(horizon): {
            str(dimension): certificate_record(
                operator, source, horizon, dimension, kappa
            )
            for dimension in range(1, operator.shape[0] + 1)
        }
        for horizon in HORIZONS
    }
    endpoint = records["32"]
    return {
        "name": model["name"],
        "description": model["description"],
        "dimension": int(operator.shape[0]),
        "operator_norm": float(np.linalg.norm(operator, 2)),
        "source_norm": float(np.linalg.norm(source)),
        "kappa": kappa,
        "horizons": records,
        "endpoint_krylov_gain_k1": endpoint["1"]["krylov_over_exact"],
        "endpoint_geometric_gain": endpoint["1"]["geometric_over_exact"],
        "endpoint_full_krylov_gain": endpoint[str(operator.shape[0])][
            "krylov_over_exact"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    selected = models()[:2] if args.smoke else models()
    payload = {
        "status": "rh62_krylov_residual_directional_tail_pilot",
        "evidence_level": (
            "deterministic finite-dimensional model audit; the calibrated "
            "RH-61 model is a surrogate, not a production continuum matrix"
        ),
        "horizons": list(HORIZONS),
        "models": [model_record(model) for model in selected],
        "theorem_boundary": {
            "arnoldi_identity": True,
            "directional_power_upper": True,
            "production_physical_family": False,
            "stage_A1_closed": False,
        },
        "limitations": [
            "The RH-61-calibrated model matches a contraction gap only; it is not the stored folded-Gaussian operator.",
            "The residual bound still uses an ordinary operator norm for propagation after the Arnoldi defect.",
            "No block-Krylov or continuum uniformity theorem is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
