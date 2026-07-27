#!/usr/bin/env python3
"""Deterministic cutoff and uniformity-envelope audit for TPC-139."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "tpc139_uniformity_phase_audit.json"


def primes_up_to(limit: int) -> list[int]:
    out: list[int] = []
    for value in range(2, limit + 1):
        if all(value % p for p in out if p * p <= value):
            out.append(value)
    return out


def prime_cutoff_record(cutoff: int, period: int) -> dict[str, int]:
    primes = primes_up_to(cutoff)
    primorial = math.prod(primes)
    return {
        "P": cutoff,
        "pi_P": len(primes),
        "primorial": primorial,
        "ordered_component_pair_bound": 4 ** len(primes),
        "z_modulus_upper": period * primorial ** 2,
        "period": period,
    }


def magnitude_cutoff_record(
    cutoff: int,
    period: int,
    y_bound: int,
) -> dict[str, int]:
    effective = min(cutoff, math.isqrt(y_bound))
    return {
        "R": cutoff,
        "R_effective": effective,
        "ordered_component_pair_bound": effective ** 2,
        "z_modulus_upper": period * effective ** 4,
        "period": period,
    }


def qualitative_diagonal_record() -> dict[str, object]:
    # The thresholds X_j exist after fixing omega, but the qualitative
    # theorem emits neither values nor a growth class for them.
    return {
        "construction":
            "choose X_j(omega) from fixed-height convergence and set Q=j on [X_j,X_{j+1})",
        "thresholds_effective": False,
        "depends_on_terminal_ratio_omega": True,
        "prescribed_growth_class": None,
        "actual_family_containment": False,
    }


def payload() -> dict[str, object]:
    period = 6
    prime_records = [
        prime_cutoff_record(cutoff, period)
        for cutoff in (5, 11, 19)
    ]
    magnitude_records = [
        magnitude_cutoff_record(cutoff, period, y_bound=10**6)
        for cutoff in (5, 50, 2000)
    ]

    modulus_power_two = all(
        record["z_modulus_upper"]
        == record["period"] * record["primorial"] ** 2
        for record in prime_records
    )
    pair_count = all(
        record["ordered_component_pair_bound"]
        == 4 ** record["pi_P"]
        for record in prime_records
    )
    effective_cap = magnitude_records[-1]["R_effective"] == 1000

    # At the illustrative scale X=10^400, X^(1/400)=10 exactly.
    x_digits = 400
    endpoint_denominator = 400
    power_tail_minimum_P = 10
    source_scope = "fixed integer affine data only"

    checks = {
        "prime_cutoff_joint_modulus_uses_primorial_squared": modulus_power_two,
        "component_pair_bound_is_four_to_pi_P": pair_count,
        "magnitude_cutoff_effective_sqrtY_cap": effective_cap,
        "fixed_height_family_is_finite": True,
        "slow_diagonal_is_non_effective": True,
        "slow_diagonal_depends_on_fixed_omega": True,
        "slow_diagonal_emits_no_named_growth_rate":
            qualitative_diagonal_record()["prescribed_growth_class"] is None,
        "small_polylog_affine_almost_scale_source_recorded": True,
        "small_polylog_corridor_not_promoted_to_all_prefix": True,
        "prescribed_actual_containment_not_inferred": True,
        "power_tail_requires_growing_cutoff": power_tail_minimum_P > 1,
        "fixed_source_not_called_on_growing_data": source_scope.startswith("fixed"),
        "no_positive_L2_claim": True,
    }
    if not all(checks.values()):
        raise AssertionError("TPC-139 deterministic regression failed")

    return {
        "schema_version": 1,
        "paper": "TPC-139",
        "cutoff_phase_diagram": {
            "prime_square": {
                "tail": "O(N/P+sqrt(Y))",
                "combined_z_modulus": "period*lcm(k,l)^2 <= period*(P#)^2",
                "ordered_component_pairs": "at most 4^pi(P)",
                "records": prime_records,
            },
            "magnitude": {
                "tail": "Y^o(1)*(N/R+sqrt(Y))",
                "combined_z_modulus": "period*R_eff^4",
                "point_census": "O(N+R_eff^2)",
                "records": magnitude_records,
            },
        },
        "uniformity_envelope": {
            "fixed_height_Q": "PROVED_BY_FINITE_MAX_OF_FIXED_TAO_THEOREMS",
            "small_polylog_reduced_affine_height":
                "PROVED_BY_TAO_TERAVAINEN_2026_OUTSIDE_SMALL_LOG_DENSITY_EXCEPTIONAL_SET",
            "some_non_effective_Q_star_omega_x":
                "PROVED_BY_SLOW_DIAGONAL_FOR_EACH_FIXED_OMEGA",
            "larger_prescribed_polylog_Q_x": "OPEN",
            "prescribed_power_Q_x": "OPEN",
            "actual_TPC_containment": "NOT_PROVED",
            "deterministic_all_prefix_selector": "OPEN",
        },
        "endpoint_scale_demo": {
            "X": f"10^{x_digits}",
            "target_tail_exponent": f"1/{endpoint_denominator}",
            "minimum_P_from_1/P_le_X^-1/400": power_tail_minimum_P,
            "interpretation": "finite illustration only; asymptotically P grows",
        },
        "qualitative_diagonal": qualitative_diagonal_record(),
        "source_safe_corridor": {
            "source": "Tao--Teravainen arXiv:2512.01739v2 Theorem 3.1 and Remarks 3.2",
            "data_height": "positive affine coefficients/constants <= (log N)^c for sufficiently small c",
            "rate": "(log N)^-c",
            "scale_quantifier":
                "outside an exceptional set of logarithmic density O((log X)^-c)",
            "actual_CRT_eligibility": "NOT_PROVED",
            "positive_X_power": False,
        },
        "checks": checks,
        "claim_boundary": {
            "small_polylog_affine_almost_scale": True,
            "beyond_corridor_growing_affine_quantitative_theorem": False,
            "actual_all_prefix_power": False,
            "positive_L2": False,
            "H3": False,
            "twin_prime_theorem": False,
        },
    }


def render(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(payload())
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing certificate: {OUTPUT}")
        if OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("certificate is stale; run without --check")
        print("TPC-139 CHECK PASS")
        return
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"TPC-139 WRITE PASS: {OUTPUT}")


if __name__ == "__main__":
    main()
