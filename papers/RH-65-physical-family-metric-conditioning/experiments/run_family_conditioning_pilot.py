"""Audit Lyapunov conditioning across near-peripheral Jordan families."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import mpmath as mp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from metric_conditioning import (  # noqa: E402
    contraction_horizon,
    metric_ledger,
    theoretical_exponents,
)


FULL_OUTPUT = ROOT / "results" / "family_conditioning_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "family_conditioning_smoke.json"
GAPS = tuple(10.0 ** (-power) for power in range(2, 9))
CASES = (
    (2, 0.0),
    (3, 0.0),
    (4, 0.0),
    (4, 0.5),
    (4, 0.75),
    (4, 1.0),
)
COUPLING_COEFFICIENT = 0.2
TAIL_TOLERANCE = 1.0e-6


def scientific(value: mp.mpf, digits: int = 24) -> str:
    return mp.nstr(value, digits, min_fixed=0, max_fixed=0)


def fit_exponent(gaps: list[float], values: list[float], sign: float) -> float:
    selected_gaps = np.asarray(gaps[-4:], dtype=float)
    selected_values = np.asarray(values[-4:], dtype=float)
    slope = np.polyfit(
        np.log(selected_gaps),
        np.log(selected_values),
        1,
    )[0]
    return float(sign * slope)


def case_record(
    dimension: int,
    coupling_power: float,
    gaps: tuple[float, ...],
    dps: int,
) -> dict[str, object]:
    rows = []
    conditions = []
    metric_gaps = []
    for gap in gaps:
        with mp.workdps(dps):
            s = mp.mpf(str(gap))
            coupling = mp.mpf(str(COUPLING_COEFFICIENT)) * (
                s ** mp.mpf(str(coupling_power))
            )
            ledger = metric_ledger(
                dimension,
                s,
                coupling,
                dps=dps,
            )
            horizon = contraction_horizon(
                ledger.contraction,
                TAIL_TOLERANCE,
            )
            conditions.append(float(ledger.condition_number))
            metric_gaps.append(float(ledger.contraction_gap))
            rows.append(
                {
                    "gap": float(s),
                    "coupling": float(coupling),
                    "lambda_min": scientific(ledger.lambda_min),
                    "lambda_max": scientific(ledger.lambda_max),
                    "condition_number": float(ledger.condition_number),
                    "condition_number_text": scientific(
                        ledger.condition_number
                    ),
                    "transfer_factor": float(ledger.transfer_factor),
                    "metric_contraction_gap": float(
                        ledger.contraction_gap
                    ),
                    "metric_contraction_gap_text": scientific(
                        ledger.contraction_gap
                    ),
                    "generic_horizon_1e_minus_6": horizon,
                }
            )
    predicted_condition, predicted_gap = theoretical_exponents(
        dimension,
        coupling_power,
    )
    fitted_condition = fit_exponent(
        list(gaps),
        conditions,
        -1.0,
    )
    fitted_gap = fit_exponent(
        list(gaps),
        metric_gaps,
        1.0,
    )
    return {
        "dimension": dimension,
        "coupling_power": coupling_power,
        "coupling_law": (
            f"{COUPLING_COEFFICIENT} * gap^{coupling_power:g}"
        ),
        "predicted_condition_exponent": predicted_condition,
        "fitted_condition_exponent": fitted_condition,
        "predicted_metric_gap_exponent": predicted_gap,
        "fitted_metric_gap_exponent": fitted_gap,
        "endpoint": rows[-1],
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        cases = CASES[:2]
        gaps = GAPS[:2]
        dps = 80
    else:
        cases = CASES
        gaps = GAPS
        dps = 140
    payload = {
        "status": "rh65_physical_family_metric_conditioning_pilot",
        "evidence_level": (
            "deterministic high-precision Jordan-family audit; the "
            "production folded-Gaussian family was not recomputed"
        ),
        "precision_decimal_digits": dps,
        "gaps": list(gaps),
        "tail_tolerance": TAIL_TOLERANCE,
        "cases": [
            case_record(dimension, power, gaps, dps)
            for dimension, power in cases
        ],
        "theorem_boundary": {
            "exact_lyapunov_contraction_identity": True,
            "matched_coupling_uniform_conditioning": True,
            "unmatched_jordan_lower_obstruction": True,
            "production_family_uniformity": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "A full-space Lyapunov metric is viable only after the "
            "residual coupling is localized to the peripheral gap scale; "
            "global weighting is not a polylogarithmic substitute for "
            "Krylov or block deflation."
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
                "case_count": len(payload["cases"]),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
