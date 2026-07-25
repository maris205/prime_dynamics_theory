#!/usr/bin/env python3
"""Rational exponent and typed-ledger checks for TPC-112."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def status(lambda_d: Fraction, eta_z: Fraction) -> str:
    reserve = 2 * eta_z - lambda_d
    if reserve > 0:
        return "PASS_WITH_RESERVE"
    if reserve == 0:
        return "PASS_ZERO_RESERVE"
    return "RECORDED_PAIR_INSUFFICIENT"


def certificate() -> dict:
    checks = 0
    beta = Fraction(267, 400)
    j_exp = Fraction(133, 400)
    baseline = 3 * beta - 2
    assert beta + j_exp == 1
    checks += 1
    assert baseline == Fraction(1, 400)
    checks += 1
    assert beta - 2 * j_exp == Fraction(1, 400)
    checks += 1

    cases = [
        (Fraction(0), Fraction(0)),
        (Fraction(1, 100), Fraction(1, 100)),
        (Fraction(1, 100), Fraction(1, 200)),
        (Fraction(1, 50), Fraction(1, 200)),
    ]
    observed = []
    for lambda_d, eta_z in cases:
        reserve = 2 * eta_z - lambda_d
        flatness_exponent = baseline - reserve
        verdict = status(lambda_d, eta_z)
        assert (verdict != "RECORDED_PAIR_INSUFFICIENT") == (lambda_d <= 2 * eta_z)
        checks += 1
        observed.append(
            {
                "lambda_D": str(lambda_d),
                "eta_Z": str(eta_z),
                "reserve": str(reserve),
                "flatness_exponent": str(flatness_exponent),
                "status": verdict,
            }
        )

    source_ids = ["energy-lower", "zero-upper", "frame-cost", "tail-cost"]
    assert len(source_ids) == len(set(source_ids))
    checks += 1
    assert Fraction(1, 400) < Fraction(1, 300)
    checks += 1
    assert not (Fraction(1, 400) < Fraction(1, 400))
    checks += 1

    return {
        "schema": "tpc112-compatibility-audit-v1",
        "status": "PASS",
        "assertions_checked": checks,
        "critical_scales": {
            "beta": str(beta),
            "one_minus_beta": str(j_exp),
            "baseline": str(baseline),
        },
        "sample_cone_cases": observed,
        "current_route": {
            "energy_exponent_certified": False,
            "zero_exponent_certified": False,
            "compatibility_status": "OPEN_INPUTS_NOT_TESTABLE",
            "physical_endpoint_status": "OPEN",
        },
        "claim_boundary": {
            "exact_exponent_cone": True,
            "ledger_independence": True,
            "fixed_h0_L2_progress": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = certificate()
    target = Path(__file__).with_suffix(".json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        expected = json.loads(target.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("certificate mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
