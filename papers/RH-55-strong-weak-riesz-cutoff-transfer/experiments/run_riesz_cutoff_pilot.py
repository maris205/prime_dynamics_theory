"""Build the RH-55 midpoint, cutoff, and intrinsic-factor diagnostics."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.special import ndtr


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from riesz_cutoff import (  # noqa: E402
    adaptive_tail_envelope,
    cutoff_norm_ledger,
    gaussian_shape_envelope,
    midpoint_ulam_ledger,
    rh39_omitted_mass_upper,
)


RH54_RESULT = (
    PAPERS
    / "RH-54-factor-aware-intrinsic-identification"
    / "results"
    / "factor_aware_transfer_pilot.json"
)
OUTPUT = ROOT / "results" / "riesz_cutoff_pilot.json"
SMOKE_OUTPUT = ROOT / "results" / "riesz_cutoff_pilot_smoke.json"
U_CRITICAL = 1.5436890126920764


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def full_midpoint_matrix(dimension: int, sigma: float) -> np.ndarray:
    nodes = (np.arange(dimension, dtype=np.float64) + 0.5) / dimension
    means = 1.0 - U_CRITICAL * nodes * nodes
    positive = -0.5 * ((nodes[None, :] - means[:, None]) / sigma) ** 2
    negative = -0.5 * ((-nodes[None, :] - means[:, None]) / sigma) ** 2
    logs = np.logaddexp(positive, negative)
    logs -= np.max(logs, axis=1, keepdims=True)
    weights = np.exp(logs)
    return weights / np.sum(weights, axis=1, keepdims=True)


def folded_cell_probabilities(
    source: np.ndarray, dimension: int, sigma: float
) -> np.ndarray:
    edges = np.arange(dimension + 1, dtype=np.float64) / dimension
    means = 1.0 - U_CRITICAL * source * source
    upper = edges[1:][None, :]
    lower = edges[:-1][None, :]
    mean = means[:, None]
    positive = ndtr((upper - mean) / sigma) - ndtr((lower - mean) / sigma)
    negative = ndtr((-lower - mean) / sigma) - ndtr((-upper - mean) / sigma)
    normalizer = ndtr((1.0 - means) / sigma) - ndtr(
        (-1.0 - means) / sigma
    )
    return (positive + negative) / normalizer[:, None]


def exact_ulam_matrix(
    dimension: int, sigma: float, quadrature_order: int
) -> np.ndarray:
    nodes, weights = leggauss(quadrature_order)
    h = 1.0 / dimension
    result = np.zeros((dimension, dimension), dtype=np.float64)
    for index in range(dimension):
        midpoint = (index + 0.5) * h
        source = midpoint + 0.5 * h * nodes
        probabilities = folded_cell_probabilities(source, dimension, sigma)
        result[index] = 0.5 * weights @ probabilities
    result /= np.sum(result, axis=1, keepdims=True)
    return result


def lifted_row_bv(row: np.ndarray, mesh: float) -> float:
    density = row / mesh
    return float(
        np.sum(np.abs(row))
        + np.sum(np.abs(np.diff(density)))
        + abs(density[0])
        + abs(density[-1])
    )


def midpoint_ulam_audit(
    sigma: float, dimensions: list[int], quadrature_order: int
) -> list[dict[str, float | int]]:
    rows = []
    for dimension in dimensions:
        mesh = 1.0 / dimension
        midpoint = full_midpoint_matrix(dimension, sigma)
        ulam = exact_ulam_matrix(dimension, sigma, quadrature_order)
        defect = midpoint - ulam
        row_l1 = np.sum(np.abs(defect), axis=1)
        row_l2 = np.linalg.norm(defect / math.sqrt(mesh), axis=1)
        row_bv = np.asarray([lifted_row_bv(row, mesh) for row in defect])
        scale = midpoint_ulam_ledger(mesh, sigma)
        rows.append(
            {
                "sigma": sigma,
                "dimension": dimension,
                "mesh": mesh,
                "quadrature_order": quadrature_order,
                "maximum_row_l1": float(np.max(row_l1)),
                "maximum_row_l2_density": float(np.max(row_l2)),
                "maximum_row_bv_density": float(np.max(row_bv)),
                "row_l1_over_h2_sigma_minus2": float(
                    np.max(row_l1) / scale.row_l1
                ),
                "row_bv_over_h_sigma_minus2": float(
                    np.max(row_bv) / scale.strong_bv
                ),
            }
        )
    return rows


def archived_factor_rows() -> list[dict[str, float | int]]:
    source = json.loads(RH54_RESULT.read_text(encoding="utf-8"))
    rows = []
    for level in source["rows"]:
        sigma = float(level["sigma"])
        dimension = int(level["fine_dimension"])
        mesh = 1.0 / dimension
        for comparison in level["comparisons"]:
            multiple = float(comparison["cutoff_multiple"])
            effective = float(comparison["effective_cutoff_multiple"])
            q_upper = rh39_omitted_mass_upper(mesh, sigma, multiple)
            generic = q_upper / (mesh * sigma**1.5)
            shape = math.exp(-0.5 * effective * effective) / sigma**2.5
            factor = comparison["intrinsic_factor_defects"]
            projector = float(factor["fine_projector_spectral"])
            weighted = float(factor["fine_weighted_riesz_spectral"])
            rows.append(
                {
                    "sigma": sigma,
                    "dimension": dimension,
                    "mesh": mesh,
                    "declared_multiple": multiple,
                    "effective_multiple": effective,
                    "omitted_mass_upper": q_upper,
                    "generic_mass_only_riesz_envelope_unit_constant": generic,
                    "gaussian_shape_riesz_envelope_unit_constant": shape,
                    "actual_fine_projector_defect": projector,
                    "actual_fine_weighted_riesz_defect": weighted,
                    "actual_sum": projector + weighted,
                    "actual_over_generic_envelope": (
                        (projector + weighted) / generic
                    ),
                    "actual_over_shape_envelope": (
                        (projector + weighted) / shape
                    ),
                }
            )
    return rows


def adaptive_rows() -> list[dict[str, float | str]]:
    rows = []
    sigmas = (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6, 1.0e-8)
    kappas = (1.0, 1.25, 1.5, 1.75, 2.0)
    for sigma in sigmas:
        mesh = sigma * sigma / math.log(1.0 / sigma)
        for kappa in kappas:
            generic = adaptive_tail_envelope(mesh, sigma, kappa)
            shape = gaussian_shape_envelope(mesh, sigma, kappa)
            rows.append(
                {
                    "sigma": sigma,
                    "mesh": mesh,
                    "schedule": "h=sigma^2/log(1/sigma)",
                    "kappa": kappa,
                    "generic_mass_only_riesz_envelope": generic.riesz_envelope,
                    "gaussian_shape_riesz_envelope": shape.riesz_envelope,
                    "shape_over_sqrt_sigma": (
                        shape.normalized_by_sqrt_sigma
                    ),
                }
            )
    return rows


def fixed_window_rows() -> list[dict[str, float]]:
    boundary = math.exp(-12.5)
    rows = []
    for sigma in (1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6):
        rows.append(
            {
                "sigma": sigma,
                "fixed_multiple": 5.0,
                "boundary_height": boundary,
                "strong_bv_route_proxy": boundary / sigma,
                "riesz_route_proxy": boundary / sigma**2.5,
            }
        )
    return rows


def build_payload(smoke: bool) -> dict[str, object]:
    midpoint_rows = midpoint_ulam_audit(
        sigma=0.08,
        dimensions=[32, 64] if smoke else [32, 64, 128, 256],
        quadrature_order=12,
    )
    factor_rows = archived_factor_rows()
    adaptive = adaptive_rows()
    fixed = fixed_window_rows()
    stress = [row for row in factor_rows if row["declared_multiple"] == 5.0]
    kappa_two = [row for row in adaptive if row["kappa"] == 2.0]
    return {
        "status": "strong_weak_riesz_cutoff_transfer_pilot",
        "evidence_level": (
            "binary64 midpoint/Ulam quadrature and reuse of the archived RH-54 "
            "dense intrinsic-factor pilot; diagnostic rather than interval validated"
        ),
        "smoke": smoke,
        "external_input": {
            "path": str(RH54_RESULT.relative_to(PAPERS.parent)),
            "sha256": sha256_file(RH54_RESULT),
        },
        "midpoint_ulam_audit": midpoint_rows,
        "archived_intrinsic_factor_audit": factor_rows,
        "adaptive_exponent_audit": adaptive,
        "fixed_window_route_no_go": fixed,
        "extrema": {
            "maximum_midpoint_row_scaled_ratio": max(
                row["row_l1_over_h2_sigma_minus2"] for row in midpoint_rows
            ),
            "maximum_midpoint_bv_scaled_ratio": max(
                row["row_bv_over_h_sigma_minus2"] for row in midpoint_rows
            ),
            "maximum_five_sigma_actual_riesz_sum": max(
                row["actual_sum"] for row in stress
            ),
            "maximum_five_sigma_actual_over_shape_envelope": max(
                row["actual_over_shape_envelope"] for row in stress
            ),
            "kappa_two_shape_ratio_strictly_decreases": all(
                kappa_two[index + 1]["shape_over_sqrt_sigma"]
                < kappa_two[index]["shape_over_sqrt_sigma"]
                for index in range(len(kappa_two) - 1)
            ),
            "fixed_window_strong_proxy_growth": (
                fixed[-1]["strong_bv_route_proxy"]
                / fixed[0]["strong_bv_route_proxy"]
            ),
        },
        "limitations": [
            "Unit-constant asymptotic envelopes display powers and are not explicit theorem constants.",
            "The midpoint/Ulam matrix is evaluated by high-order binary64 Gauss quadrature, not interval arithmetic.",
            "The intrinsic projector and weighted-Riesz defects are inherited binary64 eigensolver diagnostics from RH-54.",
            "Failure of the fixed-window strong-BV proxy does not prove that the actual Riesz projectors diverge.",
            "No uniform Hardy/Stein A1 trace budget or production intrinsic Riesz interval eigensolver is supplied.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    arguments = parser.parse_args()
    payload = build_payload(arguments.smoke)
    output = SMOKE_OUTPUT if arguments.smoke else OUTPUT
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {"output": str(output.relative_to(ROOT)), **payload["extrema"]},
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
