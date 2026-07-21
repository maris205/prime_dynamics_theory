"""Nested residual pilot for RH-63."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from nested_krylov import nested_krylov_certificate  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "nested_krylov_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "nested_krylov_smoke.json"
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


def schedule_key(schedule: tuple[int, ...]) -> str:
    return "x".join(str(value) for value in schedule)


def model_record(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"])
    source = np.asarray(model["source"])
    records = {}
    for horizon in HORIZONS:
        horizon_records = {}
        for schedule in schedules(operator.shape[0]):
            certificate = nested_krylov_certificate(
                operator, source, horizon, schedule
            )
            horizon_records[schedule_key(schedule)] = {
                "schedule": list(certificate.dimensions),
                "exact_norm": certificate.exact_norm,
                "approximation_norm": certificate.approximation_norm,
                "remainder_bound": certificate.remainder_bound,
                "upper_bound": certificate.upper_bound,
                "upper_over_exact": certificate.upper_bound
                / max(certificate.exact_norm, 1.0e-300),
                "level_residual_norms": list(
                    certificate.level_residual_norms
                ),
                "terminal_breakdown": certificate.terminal_breakdown,
            }
        records[str(horizon)] = horizon_records
    endpoint = records["32"]
    return {
        "name": model["name"],
        "dimension": int(operator.shape[0]),
        "operator_norm": float(np.linalg.norm(operator, 2)),
        "horizons": records,
        "one_level_endpoint_gain": endpoint["1"]["upper_over_exact"],
        "fully_nested_endpoint_gain": endpoint[
            schedule_key((1,) * operator.shape[0])
        ]["upper_over_exact"],
        "full_primary_endpoint_gain": endpoint[str(operator.shape[0])][
            "upper_over_exact"
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    selected = models()[:2] if args.smoke else models()
    payload = {
        "status": "rh63_nested_krylov_residual_closure_pilot",
        "evidence_level": (
            "deterministic finite-dimensional recursive Arnoldi audit; "
            "no production physical-family interval calculation"
        ),
        "horizons": list(HORIZONS),
        "models": [model_record(model) for model in selected],
        "theorem_boundary": {
            "coherent_nested_identity": True,
            "terminal_positive_remainder": True,
            "physical_family_uniformity": False,
            "stage_A1_closed": False,
        },
        "limitations": [
            "Nested depth is finite-model dependent and is not uniformly bounded in the physical family.",
            "The final unexpanded remainder still uses an ordinary operator norm.",
            "The pilot sources are vectors; block cross-column fusion remains open.",
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
