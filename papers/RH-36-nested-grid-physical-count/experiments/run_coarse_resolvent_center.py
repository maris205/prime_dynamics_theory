"""Certify one physical coarse-grid resolvent center for RH-36."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
sys.path[:0] = [
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH30 / "src"),
    str(RH33 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402
from resolvent_atlas import (  # noqa: E402
    build_direct_grushin_system,
    certify_direct_inverse,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def contour(sigma: float) -> tuple[complex, float]:
    rows = read_csv(
        PAPERS
        / "RH-28-arcwise-rational-arnoldi-enclosure"
        / "results"
        / "arcwise_scale_summary.csv"
    )
    row = next(item for item in rows if float(item["sigma"]) == sigma)
    return (
        complex(
            float(row["contour_center_real"]),
            float(row["contour_center_imag"]),
        ),
        float(row["contour_radius"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--angle", type=float, default=0.445)
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    center, radius = contour(sigma)
    point = center + radius * np.exp(1j * float(arguments.angle))
    environment = rh25_global.build_environment(
        sigma, rh24.physical_settings()[sigma]
    )
    spectrum = environment["spectrum"]
    dimension = int(environment["matrix"].shape[0])
    empty_synthesis = np.empty((dimension, 0), dtype=np.float64)
    empty_analysis = np.empty((0, dimension), dtype=np.float64)
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        empty_synthesis,
        empty_analysis,
    )

    class PhysicalGraph:
        @staticmethod
        def action(source):
            return graph.two_step(source)

    system = build_direct_grushin_system(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        empty_synthesis,
        empty_analysis,
        point,
    )
    certificate = certify_direct_inverse(
        system,
        PhysicalGraph(),
        point,
        chunk_size=int(arguments.chunk_size),
    )
    payload = {
        "status": (
            "rigorous_physical_resolvent_center"
            if certificate.admissible
            else "failed_physical_resolvent_center"
        ),
        "sigma": sigma,
        "dimension": dimension,
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "angle": float(arguments.angle),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "border_rank": int(system.border_rank),
        "bordered_dimension": int(system.bordered_dimension),
        "matrix_nnz": int(system.matrix.nnz),
        "factor_nnz": certificate.factor_nnz,
        "factor_seconds": certificate.factor_seconds,
        "certificate_seconds": certificate.certificate_seconds,
        "approximate_inverse_frobenius_upper": (
            certificate.approximate_inverse_frobenius_upper
        ),
        "residual_frobenius_upper": certificate.residual_frobenius_upper,
        "residual_center_frobenius_upper": (
            certificate.residual_center_frobenius_upper
        ),
        "residual_radius_frobenius_upper": (
            certificate.residual_radius_frobenius_upper
        ),
        "center_inverse_two_norm_upper": (
            certificate.center_inverse_two_norm_upper
        ),
        "inverse_sha256": certificate.inverse_sha256,
        "residual_center_sha256": certificate.residual_center_sha256,
        "residual_radius_sha256": certificate.residual_radius_sha256,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "coarse_resolvent_center_pilot.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
