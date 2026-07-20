"""Small 256-bit Arb audit of the RH-54 factor-composition formulas."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, arb_mat, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_factor_transfer_audit.json"


def matrix(rows) -> arb_mat:
    return arb_mat([[arb(str(value)) for value in row] for row in rows])


def frobenius_upper(value: arb_mat) -> arb:
    return sum((entry * entry for entry in value.entries()), arb(0)).sqrt()


def upper(value: arb) -> float:
    return float(value.upper())


def main() -> None:
    ctx.prec = 256
    reference = matrix(
        [
            ["0.18 +/- 1e-35", "0.31 +/- 1e-35"],
            ["-0.22 +/- 1e-35", "0.43 +/- 1e-35"],
            ["0.37 +/- 1e-35", "-0.11 +/- 1e-35"],
        ]
    )
    perturbation = matrix(
        [
            ["2e-9 +/- 1e-40", "-1e-9 +/- 1e-40"],
            ["-3e-9 +/- 1e-40", "1e-9 +/- 1e-40"],
            ["1e-9 +/- 1e-40", "2e-9 +/- 1e-40"],
        ]
    )
    perturbed = reference + perturbation
    reference_norm = frobenius_upper(reference)
    defect = frobenius_upper(perturbation)
    perturbed_norm = frobenius_upper(perturbed)
    normalized_reference = reference / reference_norm
    normalized_perturbed = perturbed / perturbed_norm
    actual_normalized_defect = frobenius_upper(
        normalized_reference - normalized_perturbed
    )
    normalized_upper = 2 * defect / reference_norm
    if upper(defect) >= float(reference_norm.lower()):
        raise RuntimeError("normalization premise was not certified")
    if upper(actual_normalized_defect) > float(normalized_upper.lower()):
        raise RuntimeError("normalization inequality was not certified")

    hardy_radius = arb("0.85")
    markov_defect = arb("6.7e-8 +/- 1e-30")
    weighted_defect = arb("3.8e-8 +/- 1e-30")
    projector_defect = arb("4.0e-8 +/- 1e-30")
    complement_norm = arb("2.1 +/- 1e-30")
    operator_defect = (markov_defect + weighted_defect) / hardy_radius
    source_defect = projector_defect + complement_norm * normalized_upper

    reference_ledger = [
        arb(value)
        for value in ("1", "1.8", "1.1", "0.70", "0.42", "0.25")
    ]
    perturbed_ledger = [
        arb(value)
        for value in ("1", "1.81", "1.11", "0.71", "0.43", "0.26")
    ]
    horizon = 6
    power_defect = operator_defect * sum(
        (
            reference_ledger[horizon - 1 - index]
            * perturbed_ledger[index]
            for index in range(horizon)
        ),
        arb(0),
    )
    reference_block = arb("0.025 +/- 1e-30")
    transferred_block = reference_block + power_defect
    if upper(transferred_block) >= 1.0:
        raise RuntimeError("transferred block contraction was not certified")

    payload = {
        "status": "arb_outward_rounded_factor_composition_audit",
        "evidence_level": "256-bit Arb interval execution on an abstract factor ledger",
        "precision_bits": 256,
        "coupling_shape": [3, 2],
        "reference_norm_ball": str(reference_norm),
        "coupling_defect_ball": str(defect),
        "actual_normalized_defect_ball": str(actual_normalized_defect),
        "normalized_defect_upper_ball": str(normalized_upper),
        "normalization_premise_certified": (
            upper(defect) < float(reference_norm.lower())
        ),
        "normalization_bound_certified": (
            upper(actual_normalized_defect) <= float(normalized_upper.lower())
        ),
        "factor_aware_operator_defect_ball": str(operator_defect),
        "factor_aware_source_defect_ball": str(source_defect),
        "horizon": horizon,
        "semigroup_power_defect_ball": str(power_defect),
        "transferred_block_norm_ball": str(transferred_block),
        "transferred_block_contraction_certified": upper(transferred_block) < 1.0,
        "arithmetic_scope": (
            "abstract interval coupling and semigroup ledger; this validates the "
            "outward arithmetic of the RH-54 formulas but is not a production-scale "
            "folded-Gaussian Riesz enclosure"
        ),
        "production_intrinsic_riesz_interval_executed": False,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
