"""Floating full-spectrum pilot for the RH-34 complement pole count."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eigvals


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
sys.path[:0] = [
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    settings = rh24.physical_settings()[sigma]

    started = time.perf_counter()
    environment = rh25_global.build_environment(sigma, settings)
    environment_seconds = time.perf_counter() - started
    dimension = int(environment["matrix"].shape[0])

    started = time.perf_counter()
    identity = np.eye(dimension, dtype=np.float64)
    complement = np.asarray(environment["external_action"](identity))
    assembly_seconds = time.perf_counter() - started
    identity = None

    started = time.perf_counter()
    values = eigvals(
        complement,
        overwrite_a=True,
        check_finite=False,
    )
    eigensolve_seconds = time.perf_counter() - started

    scale = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == sigma
    )
    center = complex(
        float(scale["contour_center_real"]),
        float(scale["contour_center_imag"]),
    )
    radius = float(scale["contour_radius"])
    signed = np.abs(values - center) - radius
    inside = signed < 0.0
    order = np.argsort(np.abs(signed))
    nearest = [
        {
            "eigenvalue_real": float(values[index].real),
            "eigenvalue_imag": float(values[index].imag),
            "modulus": float(abs(values[index])),
            "signed_boundary_distance": float(signed[index]),
            "inside": bool(inside[index]),
        }
        for index in order[:20]
    ]
    payload = {
        "status": "floating_full_complement_spectrum_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": sigma,
        "dimension": dimension,
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "floating_inside_count": int(np.count_nonzero(inside)),
        "minimum_absolute_boundary_distance": float(np.min(np.abs(signed))),
        "minimum_outside_boundary_clearance": float(
            np.min(signed[~inside]) if np.any(~inside) else np.nan
        ),
        "maximum_inside_boundary_clearance": float(
            np.max(-signed[inside]) if np.any(inside) else np.nan
        ),
        "spectral_radius": float(np.max(np.abs(values))),
        "minimum_eigenvalue_modulus": float(np.min(np.abs(values))),
        "near_zero_count_1e-10": int(np.count_nonzero(np.abs(values) < 1.0e-10)),
        "nearest_boundary_eigenvalues": nearest,
        "environment_seconds": environment_seconds,
        "assembly_seconds": assembly_seconds,
        "eigensolve_seconds": eigensolve_seconds,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / f"floating_full_spectrum_sigma_{sigma:.0e}.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    np.savez_compressed(
        output.with_suffix(".npz"),
        eigenvalues=np.asarray(values, dtype=np.complex128),
        contour_center=np.asarray(center, dtype=np.complex128),
        contour_radius=np.asarray(radius, dtype=np.float64),
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
