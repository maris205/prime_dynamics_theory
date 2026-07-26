"""Audit the exact RH-80 cloud determinant and periodic trace ledger."""

from __future__ import annotations

import argparse
import cmath
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from double_cycle_cloud import (  # noqa: E402
    cloud_factor,
    double_cycle_determinant,
    double_cycle_eigenvalues,
    double_cycle_trace,
    scaled_geometric_profile,
)


def scattering_limit(value: complex) -> complex:
    coordinate = complex(value)
    return 1.0 if coordinate == 0.0 else (cmath.exp(coordinate) - 1.0) / coordinate


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(177)
    degrees = (2, 4) if smoke else (1, 2, 3, 4, 7, 12, 20, 32)
    trials = 4 if smoke else 24
    determinant_records = []
    trace_records = []
    for degree in degrees:
        eigenvalues = double_cycle_eigenvalues(degree)
        for trial in range(trials):
            parameter = 0.8 * 1.6785735104283224 * rng.random() ** 0.5 * np.exp(2j * np.pi * rng.random())
            expected = cloud_factor(degree, parameter)
            observed = double_cycle_determinant(degree, parameter)
            determinant_records.append({
                "degree": degree,
                "trial": trial,
                "relative_determinant_error": abs(observed - expected) / max(1.0, abs(expected)),
            })
        for power in range(1, min(2 * (degree + 1), 20) + 1):
            observed_trace = complex(np.sum(eigenvalues ** power))
            expected_trace = double_cycle_trace(degree, power)
            trace_records.append({
                "degree": degree,
                "power": power,
                "absolute_trace_error": abs(observed_trace - expected_trace),
            })
    coordinates = (-1.0, -0.5, 0.0, 0.5, 1.0)
    profile_records = []
    for degree in degrees:
        for coordinate in coordinates:
            profile_records.append({
                "degree": degree,
                "coordinate": coordinate,
                "profile_error": abs(scaled_geometric_profile(degree, coordinate) - scattering_limit(coordinate)),
            })
    return {
        "status": "rh177_double_cycle_geometric_cloud_audit",
        "determinant_case_count": len(determinant_records),
        "trace_case_count": len(trace_records),
        "maximum_relative_determinant_error": max(record["relative_determinant_error"] for record in determinant_records),
        "maximum_absolute_trace_error": max(record["absolute_trace_error"] for record in trace_records),
        "finest_profile_maximum_error": max(record["profile_error"] for record in profile_records if record["degree"] == degrees[-1]),
        "determinant_records": determinant_records,
        "trace_records": trace_records,
        "profile_records": profile_records,
        "theorem_boundary": {
            "exact_rh80_geometric_cloud_realization": True,
            "exact_periodic_trace_ledger": True,
            "actual_noisy_cloud_identification": False,
            "physical_riesz_projection": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "double_cycle_smoke.json" if args.smoke else "double_cycle_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "determinant_cases": payload["determinant_case_count"], "trace_cases": payload["trace_case_count"], "max_det_error": payload["maximum_relative_determinant_error"]}, sort_keys=True))


if __name__ == "__main__":
    main()
