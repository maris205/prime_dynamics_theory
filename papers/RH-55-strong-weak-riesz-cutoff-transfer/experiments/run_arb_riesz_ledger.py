"""Run a 256-bit Arb audit of the RH-55 cutoff and sandwich ledgers."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_riesz_cutoff_ledger.json"


def main() -> None:
    ctx.prec = 256

    dimension = 512
    h = arb(1) / dimension
    sigma = arb("0.01")
    effective = arb("5.46875")
    exponential = (-(effective * effective) / 2).exp()
    q = (
        2
        * arb(1).exp().sqrt()
        * exponential
        * (h + sigma / effective)
        / (sigma - h)
    )
    weak = 2 * q
    generic_strong = weak + 4 * q / h
    weak_l2 = weak / h.sqrt()
    gaussian_strong = 8 * exponential / sigma

    reference_resolvent = arb("4.2 +/- 1e-60")
    perturbed_resolvent = arb("4.3 +/- 1e-60")
    reference_smoothing = arb("10 +/- 1e-60")
    perturbed_smoothing = arb("10.1 +/- 1e-60")
    rho = weak_l2
    tau = gaussian_strong
    outer_left = rho * reference_resolvent * reference_smoothing
    resolvent = (
        perturbed_smoothing
        * reference_resolvent
        * perturbed_resolvent
        * tau
        * reference_smoothing
    )
    outer_right = perturbed_smoothing * perturbed_resolvent * tau
    sandwich = outer_left + resolvent + outer_right

    contour_length = 2 * arb.pi() * arb("0.1")
    minimum_modulus = arb("0.75")
    projector = contour_length * sandwich / (
        2 * arb.pi() * minimum_modulus * minimum_modulus
    )
    weighted = contour_length * sandwich / (
        2 * arb.pi() * minimum_modulus
    )

    h_schedule = arb("1e-12")
    sigma_schedule = arb("1e-5")
    kappa = arb(2)
    shape_schedule = h_schedule**kappa / sigma_schedule ** arb("2.5")
    shape_over_sqrt_sigma = shape_schedule / sigma_schedule.sqrt()

    payload = {
        "status": "arb_outward_rounded_strong_weak_riesz_ledger",
        "evidence_level": (
            "256-bit Arb evaluation of the RH-39 row-tail formula and an "
            "abstract strong--weak sandwich composition"
        ),
        "precision_bits": 256,
        "dimension": dimension,
        "sigma": str(sigma),
        "effective_multiple_ball": str(effective),
        "omitted_mass_upper_ball": str(q),
        "weak_l1_ball": str(weak),
        "generic_bv_ball": str(generic_strong),
        "weak_l2_ball": str(weak_l2),
        "gaussian_shape_bv_ball": str(gaussian_strong),
        "sandwich_terms": {
            "outer_left_ball": str(outer_left),
            "resolvent_ball": str(resolvent),
            "outer_right_ball": str(outer_right),
            "total_ball": str(sandwich),
        },
        "projector_defect_upper_ball": str(projector),
        "weighted_riesz_defect_upper_ball": str(weighted),
        "adaptive_schedule_audit": {
            "mesh": str(h_schedule),
            "sigma": str(sigma_schedule),
            "kappa": str(kappa),
            "shape_envelope_ball": str(shape_schedule),
            "shape_over_sqrt_sigma_ball": str(shape_over_sqrt_sigma),
            "below_sqrt_sigma_certified": float(
                shape_over_sqrt_sigma.upper()
            )
            < 1.0,
        },
        "production_intrinsic_riesz_interval_eigensolver_executed": False,
        "arithmetic_scope": (
            "The audit certifies formula evaluation only. Strong-space "
            "resolvent constants are illustrative interval inputs, not a "
            "production folded-Gaussian enclosure."
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
