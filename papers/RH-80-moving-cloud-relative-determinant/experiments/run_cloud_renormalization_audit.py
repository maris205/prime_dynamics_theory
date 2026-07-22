"""Arb audit of fixed-pole failure and archived moving-cloud geometry."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH15_CLOUD = PAPERS / "RH-15-parity-extracted-bulk-scattering" / "results" / "outer_resonance_cloud.csv"
RH46_SUMMARY = PAPERS / "RH-46-small-noise-mesh-double-pole" / "results" / "summary.json"
FULL_OUTPUT = ROOT / "results" / "cloud_renormalization_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "cloud_renormalization_smoke.json"
PRECISION_BITS = 256
LAMBDA_TEXT = "1.6785735104283224"
COORDINATES = ("-1", "-0.5", "0", "0.5", "1")
INTERIOR_RADII = ("0.5", "0.8", "0.95")
EXTERIOR_POINTS = ("1.02", "1.05", "1.1")
PROJECTED_DEGREES = (3, 4, 5, 6, 7, 8, 16, 32, 64)


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def lower(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def selected_clouds() -> dict[str, list[tuple[str, str, str]]]:
    groups: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    with RH15_CLOUD.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["positive_order"] == "selected":
                groups[row["sigma"]].append((row["real"], row["imag"], row["folded_dimension"]))
    return groups


def cloud_profile(rows: list[tuple[str, str, str]], sigma: str, lam: arb) -> dict[str, object]:
    values = [acb(arb(real), arb(imag)) for real, imag, _ in rows]
    degree = len(values) // 2
    radial_mean = sum((abs(value) for value in values), arb(0)) / len(values)
    edge_center = arb(1) / radial_mean**2
    base = acb(1)
    for value in values:
        base *= acb(1) - edge_center * value**2
    coordinate_rows = []
    errors: list[arb] = []
    for coordinate in COORDINATES:
        s = arb(coordinate)
        q = (s / (degree + 1)).exp()
        w = edge_center * q
        observed = acb(1)
        for value in values:
            observed *= acb(1) - w * value**2
        observed /= base
        if coordinate == "0":
            finite = arb(1)
        else:
            finite = ((s.exp() - 1) / ((degree + 1) * (q - 1))) ** 2
        error = abs(observed - finite)
        errors.append(error)
        coordinate_rows.append(
            {
                "coordinate": float(coordinate),
                "observed_ball": str(observed),
                "finite_geometric_ball": str(finite),
                "absolute_error_ball": str(error),
                "absolute_error_upper": upper(error),
            }
        )
    zero_radii = [arb(1) / abs(value) ** 2 for value in values]
    mean_error = sum(errors, arb(0)) / len(errors)
    max_error = max(errors, key=lambda value: float(value.upper()))
    mismatch = abs(edge_center / lam - 1)
    return {
        "sigma": float(sigma),
        "dimension": int(rows[0][2]),
        "effective_degree": degree,
        "one_step_cloud_size": len(values),
        "radial_mean_ball": str(radial_mean),
        "edge_center_ball": str(edge_center),
        "edge_center_upper": upper(edge_center),
        "relative_center_mismatch_ball": str(mismatch),
        "relative_center_mismatch_upper": upper(mismatch),
        "zero_radius_min_lower": lower(min(zero_radii, key=lambda value: float(value.lower()))),
        "zero_radius_max_upper": upper(max(zero_radii, key=lambda value: float(value.upper()))),
        "central_profile_mean_error_ball": str(mean_error),
        "central_profile_mean_error_upper": upper(mean_error),
        "central_profile_max_error_ball": str(max_error),
        "central_profile_max_error_upper": upper(max_error),
        "coordinates": coordinate_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads(RH46_SUMMARY.read_text(encoding="utf-8"))
    groups = selected_clouds()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    try:
        lam = arb(LAMBDA_TEXT)
        degrees = (3, 7) if args.smoke else PROJECTED_DEGREES
        interior_rows = []
        for degree in degrees:
            for radius_text in INTERIOR_RADII:
                radius = arb(radius_text)
                power = radius ** (degree + 1)
                error = arb(2) * power + power**2
                interior_rows.append(
                    {
                        "degree": degree,
                        "radius_ratio": float(radius_text),
                        "uniform_error_ball": str(error),
                        "uniform_error_upper": upper(error),
                    }
                )
        exterior_rows = []
        for degree in degrees:
            for point_text in EXTERIOR_POINTS:
                point = arb(point_text)
                value = (point ** (degree + 1) - 1) ** 2
                exterior_rows.append(
                    {
                        "degree": degree,
                        "point_ratio": float(point_text),
                        "fixed_cancellation_magnitude_ball": str(value),
                        "fixed_cancellation_magnitude_lower": lower(value),
                    }
                )
        sigma_keys = sorted(groups, key=float, reverse=True)
        if args.smoke:
            sigma_keys = sigma_keys[-1:]
        cloud_rows = [cloud_profile(groups[sigma], sigma, lam) for sigma in sigma_keys]
    finally:
        ctx.prec = previous_precision
    finest = cloud_rows[-1]
    payload = {
        "status": "rh80_moving_cloud_relative_determinant_audit",
        "precision_bits": PRECISION_BITS,
        "deterministic_double_pole": float(LAMBDA_TEXT),
        "inherited_double_pole_factor": inherited["double_pole_obstruction"]["two_step_factor"],
        "ideal_model": {
            "cloud_factor": "C_N(w)=Pi_N(w/lambda)^2",
            "fixed_cancellation_identity": "(1-w/lambda)^2 C_N(w)=(1-(w/lambda)^(N+1))^2",
            "interior_rows": interior_rows,
            "exterior_rows": exterior_rows,
            "fixed_cancellation_locally_bounded_across_circle": False,
        },
        "archived_cloud_rows": cloud_rows,
        "finest_cloud_gate": {
            "sigma": finest["sigma"],
            "degree": finest["effective_degree"],
            "relative_center_mismatch_upper": finest["relative_center_mismatch_upper"],
            "central_profile_mean_error_upper": finest["central_profile_mean_error_upper"],
            "central_profile_max_error_upper": finest["central_profile_max_error_upper"],
        },
        "theorem_boundary": {
            "fixed_pole_cancellation_failure_in_canonical_model": True,
            "exact_reducing_cloud_factorization": True,
            "uniform_complement_trace_norm_is_sufficient": True,
            "actual_cloud_riesz_projection_constructed": False,
            "uniform_complement_trace_norm_proved": False,
            "canonical_cloud_identification_proved": False,
            "stage_A5_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A fixed scalar double-pole factor cannot renormalize the canonical finite-cloud family on disks crossing |w|=lambda. "
            "The viable A5 object is the quotient by the actual moving spectral-cloud polynomial. Exact reducing factorization plus a uniform trace-class complement bound would make that quotient a normal family; trace-norm convergence would give a quantitative relative-determinant limit. The archived clouds support the geometry but do not prove the Riesz projection or complement bound."
        ),
        "limitations": [
            "Arb validates arithmetic propagated from archived decimal cloud coordinates; it does not upgrade the RH-15 floating eigensolver output into interval eigenvalue enclosures.",
            "The cloud-center and edge-profile audit is diagnostic and does not identify an actual moving Riesz projection.",
            "Uniform trace norm of the cloud complement is a sufficient gate, not a necessary condition.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "cloud_levels": len(cloud_rows),
                "finest_degree": finest["effective_degree"],
                "finest_profile_mean_error": finest["central_profile_mean_error_upper"],
                "fixed_cancellation_crosses_circle": False,
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()

