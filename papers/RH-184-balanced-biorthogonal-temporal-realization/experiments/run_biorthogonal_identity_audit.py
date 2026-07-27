"""Finite identity audit for the balanced biorthogonal construction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from biorthogonal_clock import (  # noqa: E402
    adjoint,
    balanced_biorthogonal_frames,
    biorthogonal_residuals,
    gauge_transform,
    oblique_projector,
    operator_norm,
)


def one_case(rng: np.random.Generator, ambient: int, rank: int, trial: int) -> dict[str, float | int | bool]:
    right_raw = rng.normal(size=(ambient, rank)) + 1j * rng.normal(size=(ambient, rank))
    left_raw = rng.normal(size=(ambient, rank)) + 1j * rng.normal(size=(ambient, rank))
    data = balanced_biorthogonal_frames(right_raw, left_raw)
    right = np.asarray(data["right_frame"])
    left = np.asarray(data["left_frame"])
    singular = np.asarray(data["cross_singular_values"])
    projector = oblique_projector(right, left)
    dynamics = rng.normal(size=(ambient, ambient)) + 1j * rng.normal(size=(ambient, ambient))
    residuals = biorthogonal_residuals(dynamics, right, left)
    gauge = rng.normal(size=(rank, rank)) + 1j * rng.normal(size=(rank, rank))
    gauge += 2.0 * np.eye(rank)
    transformed_right, transformed_left = gauge_transform(right, left, gauge)
    transformed = biorthogonal_residuals(dynamics, transformed_right, transformed_left)
    compressed = np.asarray(residuals["compressed"])
    expected_compressed = np.linalg.inv(gauge) @ compressed @ gauge
    minimum = float(singular[-1])
    norm_target = 1.0 / np.sqrt(minimum)
    product_target = 1.0 / minimum
    return {
        "ambient_dimension": ambient,
        "rank": rank,
        "trial": trial,
        "minimum_cross_singular_value": minimum,
        "biorthogonality_defect": operator_norm(adjoint(left) @ right - np.eye(rank)),
        "projector_idempotence_defect": operator_norm(projector @ projector - projector),
        "projector_norm_formula_error": abs(operator_norm(projector) - product_target),
        "right_frame_norm_formula_error": abs(operator_norm(right) - norm_target),
        "left_frame_norm_formula_error": abs(operator_norm(left) - norm_target),
        "compressed_gauge_covariance_error": operator_norm(np.asarray(transformed["compressed"]) - expected_compressed),
        "spectrum_gauge_error": float(np.max(np.abs(np.sort_complex(np.linalg.eigvals(compressed)) - np.sort_complex(np.linalg.eigvals(np.asarray(transformed["compressed"])))))),
        "right_residual_norm": float(residuals["right_residual_norm"]),
        "left_residual_norm": float(residuals["left_residual_norm"]),
    }


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(184)
    ambients = (8, 12) if smoke else (8, 12, 18, 24)
    trials = 3 if smoke else 10
    records = []
    for ambient in ambients:
        for rank in (2, 3, 4):
            if rank >= ambient:
                continue
            for trial in range(trials):
                records.append(one_case(rng, ambient, rank, trial))
    keys = (
        "biorthogonality_defect",
        "projector_idempotence_defect",
        "projector_norm_formula_error",
        "right_frame_norm_formula_error",
        "left_frame_norm_formula_error",
        "compressed_gauge_covariance_error",
        "spectrum_gauge_error",
    )
    maxima = {key: max(float(record[key]) for record in records) for key in keys}
    failures = sum(any(float(record[key]) > 1e-9 for key in keys) for record in records)
    return {
        "status": "rh184_balanced_biorthogonal_identity_audit",
        "case_count": len(records),
        "failure_count": failures,
        "maximum_errors": maxima,
        "records": records,
        "theorem_boundary": {
            "canonical_balanced_frames": True,
            "exact_biorthogonality": True,
            "optimal_norm_product_formula": True,
            "gauge_covariance": True,
            "finite_random_identity_audit": True,
            "physical_transversality": False,
            "physical_riesz_certificate": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "biorthogonal_identity_smoke.json" if args.smoke else "biorthogonal_identity_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "cases": payload["case_count"], "failures": payload["failure_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
