"""Audit Lyapunov-weighted terminal residuals on finite models."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weighted_residual import (  # noqa: E402
    lyapunov_metric,
    weighted_nested_certificate,
)


FULL_OUTPUT = ROOT / "results" / "weighted_residual_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "weighted_residual_smoke.json"
HORIZONS = (1, 4, 8, 16, 32, 64)


def models() -> list[dict[str, object]]:
    return [
        {
            "name": "rh61_left_calibrated_slow_fast",
            "operator": np.diag([0.993861320134583, 0.2]).astype(
                np.complex128
            ),
            "source": np.asarray([5.0e-4, 1.0], dtype=np.complex128),
        },
        {
            "name": "rh60_two_block",
            "operator": np.asarray(
                [[0.2, 0.3], [0.0, 0.7]], dtype=np.complex128
            ),
            "source": np.asarray([0.0, 0.4], dtype=np.complex128),
        },
        {
            "name": "nonnormal_four_step_chain",
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
        },
    ]


def schedules(dimension: int) -> list[tuple[int, ...]]:
    result = [(1,) * depth for depth in range(1, dimension + 1)]
    if (dimension,) not in result:
        result.append((dimension,))
    return result


def key(schedule: tuple[int, ...]) -> str:
    return "x".join(str(value) for value in schedule)


def model_record(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"])
    source = np.asarray(model["source"])
    metric = lyapunov_metric(operator)
    records = {}
    for horizon in HORIZONS:
        horizon_records = {}
        for schedule in schedules(operator.shape[0]):
            certificate = weighted_nested_certificate(
                operator, source, metric, horizon, schedule
            )
            horizon_records[key(schedule)] = {
                "schedule": list(certificate.dimensions),
                "metric_exact_norm": certificate.exact_metric_norm,
                "metric_upper": certificate.upper_bound,
                "metric_upper_over_exact": certificate.upper_bound
                / max(certificate.exact_metric_norm, 1.0e-300),
                "terminal_remainder_bound": certificate.terminal_remainder_bound,
                "metric_contraction": certificate.metric_contraction,
                "euclidean_operator_norm": certificate.euclidean_operator_norm,
                "terminal_breakdown": certificate.terminal_breakdown,
            }
        records[str(horizon)] = horizon_records
    endpoint = records["32"]
    return {
        "name": model["name"],
        "dimension": int(operator.shape[0]),
        "euclidean_operator_norm": float(np.linalg.norm(operator, 2)),
        "metric_condition_number": float(np.linalg.cond(metric)),
        "metric_contraction": float(
            endpoint["1"]["metric_contraction"]
        ),
        "horizons": records,
        "one_level_endpoint_gain": endpoint["1"][
            "metric_upper_over_exact"
        ],
        "fully_nested_endpoint_gain": endpoint[
            key((1,) * operator.shape[0])
        ]["metric_upper_over_exact"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    selected = models()[:2] if args.smoke else models()
    payload = {
        "status": "rh64_weighted_terminal_residual_pilot",
        "evidence_level": (
            "deterministic finite-dimensional Lyapunov-weighted audit; "
            "no production physical-family theorem"
        ),
        "horizons": list(HORIZONS),
        "models": [model_record(model) for model in selected],
        "theorem_boundary": {
            "positive_lyapunov_metric": True,
            "weighted_terminal_certificate": True,
            "physical_family_uniformity": False,
            "stage_A1_closed": False,
        },
        "limitations": [
            "The Lyapunov metric is recomputed separately for each finite model.",
            "Metric condition numbers can grow and are not uniformly controlled.",
            "The pilot is vector-valued; block cross-column fusion remains open.",
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
