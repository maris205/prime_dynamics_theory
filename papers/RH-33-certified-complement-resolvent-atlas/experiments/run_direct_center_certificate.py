"""Run one rigorous direct complement inverse certificate at an RH-28 arc."""

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
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH30 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402
from resolvent_atlas import (  # noqa: E402
    build_direct_grushin_system,
    certify_arc_coverage,
    certify_direct_inverse,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--arc", type=int, required=True)
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    arcs = [
        row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    ]
    selected = next(row for row in arcs if int(row["arc"]) == int(arguments.arc))
    point = complex(float(selected["center_real"]), float(selected["center_imag"]))
    environment = rh25_global.build_environment(
        sigma, rh24.physical_settings()[sigma]
    )
    spectrum = environment["spectrum"]
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )
    system = build_direct_grushin_system(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
        point,
    )
    certificate = certify_direct_inverse(
        system, graph, point, chunk_size=int(arguments.chunk_size)
    )
    coverage = [
        certify_arc_coverage(point, certificate.center_inverse_two_norm_upper, row)
        for row in arcs
    ]
    closed = [row.arc for row in coverage if row.closed]
    payload = {
        "status": (
            "rigorous_direct_center_certificate"
            if certificate.admissible
            else "failed_direct_center_certificate"
        ),
        "sigma": sigma,
        "source_arc": int(arguments.arc),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "physical_dimension": int(system.physical_dimension),
        "border_rank": int(system.border_rank),
        "bordered_dimension": int(system.bordered_dimension),
        "matrix_nnz": int(system.matrix.nnz),
        "factor_nnz": certificate.factor_nnz,
        "factor_seconds": certificate.factor_seconds,
        "certificate_seconds": certificate.certificate_seconds,
        "approximate_inverse_frobenius_upper": certificate.approximate_inverse_frobenius_upper,
        "residual_frobenius_upper": certificate.residual_frobenius_upper,
        "residual_center_frobenius_upper": certificate.residual_center_frobenius_upper,
        "residual_radius_frobenius_upper": certificate.residual_radius_frobenius_upper,
        "center_inverse_two_norm_upper": certificate.center_inverse_two_norm_upper,
        "inverse_sha256": certificate.inverse_sha256,
        "residual_center_sha256": certificate.residual_center_sha256,
        "residual_radius_sha256": certificate.residual_radius_sha256,
        "closed_arc_count": len(closed),
        "closed_arcs": closed,
        "closed_arc_minimum": min(closed) if closed else None,
        "closed_arc_maximum": max(closed) if closed else None,
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "pilots" / f"direct_sigma_{sigma:.0e}_arc_{arguments.arc}.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
