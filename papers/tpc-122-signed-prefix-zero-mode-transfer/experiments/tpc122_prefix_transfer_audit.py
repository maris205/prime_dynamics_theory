#!/usr/bin/env python3
"""Finite deterministic audit for the TPC-122 Abel/BV transfer."""

from __future__ import annotations

import json
from pathlib import Path


TOL = 1.0e-11


def close_complex(a: complex, b: complex) -> bool:
    return abs(a - b) <= TOL * max(1.0, abs(a), abs(b))


def prefixes(values: list[complex]) -> list[complex]:
    out: list[complex] = []
    total = 0j
    for value in values:
        total += value
        out.append(total)
    return out


def bv_star(weights: list[complex]) -> float:
    if not weights:
        return 0.0
    return abs(weights[-1]) + sum(
        abs(weights[k] - weights[k + 1])
        for k in range(len(weights) - 1)
    )


def audit() -> dict:
    # TPC-111 factor-allocation crosswalk:
    # c_theta * sum_i W_theta(r_i) sigma_theta(r_i)
    # = sum_i sigma_i * (c_theta W_theta(r_i)).
    outer_coefficient = 1.75 - 0.25j
    outer_weights = [0.3 + 0.1j, -0.4j, 0.8 - 0.2j]
    outer_signs = [1 - 1j, -0.5 + 0.25j, 2 + 0.5j]
    original_outer_pairing = outer_coefficient * sum(
        weight * sign for weight, sign in zip(outer_weights, outer_signs)
    )
    allocated_outer_pairing = sum(
        sign * (outer_coefficient * weight)
        for weight, sign in zip(outer_weights, outer_signs)
    )
    provenance_crosswalk_ok = close_complex(
        original_outer_pairing, allocated_outer_pairing
    )

    sigma = [1 + 2j, -0.5 + 0.25j, 2 - 1j, -1.5 - 0.5j, 0.2 + 0.8j]
    weights = [0.7 - 0.1j, 0.2 + 0.4j, -0.3 + 0.2j, -0.1j, 0.5]
    pref = prefixes(sigma)
    direct = sum(a * b for a, b in zip(sigma, weights))
    abel = pref[-1] * weights[-1] + sum(
        pref[k] * (weights[k] - weights[k + 1])
        for k in range(len(weights) - 1)
    )
    abel_ok = close_complex(direct, abel)

    delta = max(abs(value) for value in pref)
    holder_ok = abs(direct) <= delta * bv_star(weights) + TOL

    k_star = max(range(len(pref)), key=lambda k: abs(pref[k]))
    phase = pref[k_star].conjugate() / abs(pref[k_star])
    extremizer = [phase if k <= k_star else 0j for k in range(len(pref))]
    sharp_value = abs(sum(a * b for a, b in zip(sigma, extremizer)))
    sharp_ok = close_complex(complex(sharp_value), complex(delta)) and abs(
        bv_star(extremizer) - 1.0
    ) <= TOL

    # Final cancellation alone does not control all prefixes.
    n = 20
    bad_prefix = [1.0] * n + [-1.0] * n
    bad_pref = prefixes([complex(x) for x in bad_prefix])
    final_zero_large_prefix = abs(bad_pref[-1]) <= TOL and max(
        abs(x) for x in bad_pref
    ) == n

    # Both the prefix branch and the content remainder must clear
    # lambda_D/2.
    ledger_cases = [
        (0.10, 0.02, 0.09, 0.16, True),
        (0.10, 0.02, 0.07, 0.16, False),
        (0.08, 0.02, 0.20, 0.16, False),
        (0.15, 0.05, 0.10, 0.20, True),
    ]
    ledger_ok = all(
        (
            (delta_exp + TOL >= ell + lam_d / 2)
            and (eta_cont + TOL >= lam_d / 2)
        )
        == expected
        for delta_exp, ell, eta_cont, lam_d, expected in ledger_cases
    )

    # A subpower union of uniformly typed classes takes the minimum reserve.
    class_exponents = [(0.16, 0.03), (0.12, 0.01), (0.20, 0.07)]
    eta_cont = 0.10
    eta_zero = min(
        [delta_exp - ell for delta_exp, ell in class_exponents]
        + [eta_cont]
    )
    class_ledger_ok = abs(eta_zero - 0.10) <= TOL

    class_bottleneck_eta = min(
        [delta_exp - ell for delta_exp, ell in class_exponents] + [0.20]
    )
    class_bottleneck_ok = abs(class_bottleneck_eta - 0.11) <= TOL

    negative_class_exponents = [(0.03, 0.05), (0.10, 0.02)]
    negative_class_rejected = not all(
        delta_exp - ell >= 0
        for delta_exp, ell in negative_class_exponents
    )

    reserve_cases = [
        (0.10, 0.02, 0.09, 0.16, 0.0),
        (0.15, 0.05, 0.12, 0.18, 0.02),
    ]
    reserve_formula_ok = all(
        abs(
            2.0 * min(delta_exp - ell, content_exp)
            - lam_d
            - expected
        )
        <= TOL
        for delta_exp, ell, content_exp, lam_d, expected in reserve_cases
    )

    status = all(
        [
            provenance_crosswalk_ok,
            abel_ok,
            holder_ok,
            sharp_ok,
            final_zero_large_prefix,
            ledger_ok,
            class_ledger_ok,
            class_bottleneck_ok,
            negative_class_rejected,
            reserve_formula_ok,
        ]
    )
    return {
        "schema": "tpc-122-signed-prefix-zero-mode-transfer-v1",
        "status": "PASS" if status else "FAIL",
        "checks": {
            "finite_tpc111_factor_allocation_identity": provenance_crosswalk_ok,
            "abel_identity": abel_ok,
            "bv_prefix_bound": holder_ok,
            "sharp_step_extremizer": sharp_ok,
            "final_sum_does_not_control_prefixes": final_zero_large_prefix,
            "compatibility_exponent_ledger": ledger_ok,
            "subpower_class_minimum_ledger": class_ledger_ok,
            "class_bottleneck_ledger": class_bottleneck_ok,
            "negative_class_reserve_rejected": negative_class_rejected,
            "determinant_reserve_formula": reserve_formula_ok,
        },
        "sample": {
            "direct_real": direct.real,
            "direct_imag": direct.imag,
            "max_prefix": delta,
            "bv_norm": bv_star(weights),
            "sharp_value": sharp_value,
            "sample_eta_Z": eta_zero,
        },
        "claim_boundary": {
            "actual_growing_prefix_saving": False,
            "actual_outer_bv_envelope": False,
            "actual_content_remainder_bound": False,
            "uniform_subpower_class_hypothesis": False,
            "positive_eta_Z": False,
            "fixed_h0_L2_saving": False,
        },
    }


def main() -> None:
    payload = audit()
    out = Path(__file__).with_suffix(".json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if payload["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
