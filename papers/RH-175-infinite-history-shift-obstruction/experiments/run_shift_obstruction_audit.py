"""Finite-section witnesses for the infinite-history spectral-disk wall."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from history_shift import (  # noqa: E402
    finite_history_completion,
    shift_resolvent_vector_lower_bound,
    unilateral_shift_truncation,
)


def run(smoke: bool) -> dict[str, object]:
    weight = 1.0 / math.sqrt(512.0)
    lengths = (4, 8) if smoke else (4, 8, 16, 32, 64)
    fractions = (0.5,) if smoke else (0.25, 0.5, 0.75)
    records = []
    for length in lengths:
        shift = unilateral_shift_truncation(length)
        for fraction in fractions:
            point = fraction * weight
            matrix = point * np.eye(length) - weight * shift
            vector = np.zeros(length)
            vector[0] = 1.0
            observed = float(np.linalg.norm(np.linalg.solve(matrix, vector)))
            exact = shift_resolvent_vector_lower_bound(length, weight, point)
            records.append({
                "length": length,
                "spectral_fraction_of_shift_radius": fraction,
                "finite_spectrum_radius": float(max(abs(np.linalg.eigvals(weight * shift)), default=0.0)),
                "resolvent_vector_norm": observed,
                "exact_lower_bound": exact,
                "relative_formula_error": abs(observed - exact) / exact,
                "log10_resolvent_lower_bound": math.log10(exact),
            })

    operator = np.diag([0.25, -0.40])
    singular_records = []
    for length in lengths:
        completion = finite_history_completion(operator, length, 0.8)
        singular = np.linalg.svd(completion, compute_uv=False)
        singular_records.append({
            "length": length,
            "dimension": int(completion.shape[0]),
            "singular_values_at_least_shift_weight": int(np.sum(singular >= weight * (1.0 - 1e-12))),
            "expected_shift_floor_count": 2 * (length - 1),
            "minimum_nonzero_singular_value": float(singular[-1]),
        })
    return {
        "status": "rh175_infinite_history_shift_obstruction_audit",
        "shift_radius": weight,
        "resolvent_case_count": len(records),
        "maximum_relative_formula_error": max(record["relative_formula_error"] for record in records),
        "maximum_log10_resolvent_lower_bound": max(record["log10_resolvent_lower_bound"] for record in records),
        "all_finite_shift_spectra_zero": all(record["finite_spectrum_radius"] == 0.0 for record in records),
        "all_singular_floor_counts_match": all(record["singular_values_at_least_shift_weight"] == record["expected_shift_floor_count"] for record in singular_records),
        "resolvent_records": records,
        "singular_records": singular_records,
        "theorem_boundary": {
            "infinite_history_spectrum_contains_shift_disk": True,
            "infinite_history_not_compact_or_schatten": True,
            "finite_nilpotent_spectra_detect_disk": False,
            "direct_fredholm_determinant_route": False,
            "all_possible_history_completions_rejected": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "shift_obstruction_smoke.json" if args.smoke else "shift_obstruction_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "case_count": payload["resolvent_case_count"], "max_log10_lower": payload["maximum_log10_resolvent_lower_bound"]}, sort_keys=True))


if __name__ == "__main__":
    main()
