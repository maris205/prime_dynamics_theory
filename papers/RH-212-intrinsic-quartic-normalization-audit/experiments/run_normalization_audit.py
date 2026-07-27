"""Build the frozen dense-scale quartet and normalization ledger."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from quartic_normalization import (  # noqa: E402
    centered_rms_normalize,
    coefficient_distance,
    conjugacy_error,
    determinant_radius_normalize,
    haar_coarse_embedding,
    monic_coefficients,
    outer_bulk_quartet,
)


AUDIT_SIGMAS = (0.04, 0.032, 0.025, 0.02, 0.016, 0.0125, 0.01, 0.008)
EXTENDED_SIGMAS = AUDIT_SIGMAS + (0.00625, 0.005, 0.004, 0.0032, 0.0025, 0.002, 0.0016, 0.00125)
FINE_RESOLUTION = 5.12


def complex_payload(values: np.ndarray) -> dict[str, list[float]]:
    array = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in array],
        "imag": [float(value.imag) for value in array],
    }


def extract_sigma(sigma: float) -> list[dict[str, object]]:
    dimension = max(32, 2 * int(round(FINE_RESOLUTION / float(sigma) / 2.0)))
    fine = sparse_folded_gaussian_matrix(dimension, float(sigma)).tocsr()
    embedding = haar_coarse_embedding(dimension)
    coarse = (embedding.T @ fine @ embedding).tocsr()
    rows = []
    for side, matrix in (("left", fine), ("right", coarse)):
        started = time.perf_counter()
        roots = outer_bulk_quartet(matrix)
        raw = monic_coefficients(roots)
        radial = determinant_radius_normalize(roots)
        centered = centered_rms_normalize(roots)
        rows.append({
            "sigma": float(sigma),
            "side": side,
            "dimension": int(matrix.shape[0]),
            "roots": complex_payload(roots),
            "raw_coefficients": complex_payload(raw),
            "determinant_radius": radial.scale,
            "determinant_radius_coefficients": complex_payload(monic_coefficients(radial.roots)),
            "center": {"real": centered.center.real, "imag": centered.center.imag},
            "centered_rms_radius": centered.scale,
            "centered_rms_roots": complex_payload(centered.roots),
            "centered_rms_coefficients": complex_payload(monic_coefficients(centered.roots)),
            "conjugacy_error": conjugacy_error(roots),
            "elapsed_seconds": time.perf_counter() - started,
        })
    return rows


def roots(row: dict[str, object], field: str) -> np.ndarray:
    payload = row[field]
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def coefficients(row: dict[str, object], field: str) -> np.ndarray:
    payload = row[field]
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in rows}
    available_sigmas = tuple(sigma for sigma in AUDIT_SIGMAS if (sigma, "left") in endpoint and (sigma, "right") in endpoint)
    modes = {
        "raw": ("roots", "raw_coefficients"),
        "determinant_radius": (None, "determinant_radius_coefficients"),
        "centered_rms": ("centered_rms_roots", "centered_rms_coefficients"),
    }
    adjacent_rows = []
    channel_rows = []
    for name, (root_field, coefficient_field) in modes.items():
        errors = []
        for coarse, fine in zip(available_sigmas[:-1], available_sigmas[1:]):
            for side in ("left", "right"):
                first = coefficients(endpoint[(coarse, side)], coefficient_field)
                second = coefficients(endpoint[(fine, side)], coefficient_field)
                difference = second - first
                error = {
                    "maximum_absolute_error": float(np.max(np.abs(second - first))),
                    "coarse_relative_l2_error": float(
                        np.linalg.norm(difference) / max(np.linalg.norm(first), np.finfo(float).tiny)
                    ),
                    "fine_relative_l2_error": float(
                        np.linalg.norm(difference) / max(np.linalg.norm(second), np.finfo(float).tiny)
                    ),
                }
                row = {"normalization": name, "coarse_sigma": coarse, "fine_sigma": fine, "side": side, **error}
                adjacent_rows.append(row)
                errors.append(error["fine_relative_l2_error"])
        channel_errors = []
        for sigma in available_sigmas:
            left = coefficients(endpoint[(sigma, "left")], coefficient_field)
            right = coefficients(endpoint[(sigma, "right")], coefficient_field)
            absolute_error = float(np.max(np.abs(left - right)))
            relative_error = float(
                np.linalg.norm(left - right) / max(np.linalg.norm(left), np.finfo(float).tiny)
            )
            channel_errors.append(relative_error)
            channel_rows.append({
                "normalization": name,
                "sigma": sigma,
                "maximum_absolute_error": absolute_error,
                "left_relative_l2_error": relative_error,
            })
        modes[name] = {
            "adjacent_fine_relative_error_minimum": min(errors) if errors else None,
            "adjacent_fine_relative_error_maximum": max(errors) if errors else None,
            "adjacent_fine_relative_error_mean": float(np.mean(errors)) if errors else None,
            "left_right_relative_error_maximum": max(channel_errors),
        }
    return {
        "normalization_summary": modes,
        "adjacent_rows": adjacent_rows,
        "channel_rows": channel_rows,
    }


def legacy_anchor_comparison(rows: list[dict[str, object]]) -> dict[str, float]:
    source = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    current = {(float(row["sigma"]), str(row["side"])): roots(row, "roots") for row in rows}
    root_errors = []
    coefficient_errors = []
    for row in source["endpoint_rows"]:
        sigma = float(row["sigma"])
        side = str(row["side"])
        legacy = np.asarray(row["quartet_values_real"]) + 1j * np.asarray(row["quartet_values_imag"])
        candidate = current[(sigma, side)]
        root_errors.append(min(
            max(abs(candidate[index] - legacy[target]) for index, target in enumerate(order))
            for order in itertools.permutations(range(4))
        ))
        coefficient_errors.append(float(np.max(np.abs(np.poly(candidate) - np.poly(legacy)))))
    return {
        "legacy_anchor_maximum_root_matching_error": float(max(root_errors)),
        "legacy_anchor_maximum_coefficient_error": float(max(coefficient_errors)),
    }


def run(sigmas: tuple[float, ...]) -> dict[str, object]:
    started = time.perf_counter()
    rows = []
    for sigma in sigmas:
        current = extract_sigma(sigma)
        rows.extend(current)
        print(json.dumps({
            "sigma": sigma,
            "left_dimension": current[0]["dimension"],
            "right_dimension": current[1]["dimension"],
            "left_conjugacy_error": current[0]["conjugacy_error"],
            "right_conjugacy_error": current[1]["conjugacy_error"],
        }, sort_keys=True), flush=True)
    payload = {
        "status": "rh212_intrinsic_quartic_normalization_audit",
        "audit_sigmas": list(AUDIT_SIGMAS),
        "extended_sigmas": list(sigmas),
        "endpoint_rows": rows,
        **summarize(rows),
        **legacy_anchor_comparison(rows),
        "maximum_conjugacy_error": max(float(row["conjugacy_error"]) for row in rows),
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "normalizations_defined_exactly": True,
            "finite_eight_scale_audit": True,
            "natural_normalization_contraction": False,
            "all_level_coefficient_limit": False,
            "growing_divisor_family": False,
            "gate_A": False,
        },
    }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="extract only sigma=0.04")
    args = parser.parse_args()
    sigmas = (AUDIT_SIGMAS[0],) if args.smoke else EXTENDED_SIGMAS
    payload = run(sigmas)
    output = ROOT / ("results/normalization_smoke.json" if args.smoke else "results/intrinsic_normalization_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "elapsed_seconds": payload["elapsed_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
