#!/usr/bin/env python3
"""Deterministic finite certificate for TPC-108."""

import cmath
import json
import math
from pathlib import Path


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def e(t):
    return cmath.exp(2j * math.pi * t)


def block_sum(coeffs, alpha):
    return sum(value * e(-alpha * z) for z, value in enumerate(coeffs))


def ttstar_sum(coeffs, alpha):
    n = len(coeffs)
    answer = 0j
    for h in range(-(n - 1), n):
        corr = 0j
        for z in range(n):
            zh = z + h
            if 0 <= zh < n:
                corr += coeffs[zh] * coeffs[z].conjugate()
        answer += e(-alpha * h) * corr
    return answer


def alias_rhs(coeffs, q):
    buckets = [0j] * q
    for z, value in enumerate(coeffs):
        buckets[z % q] += value
    return q * sum(abs(value) ** 2 for value in buckets)


def full_frequency_lhs(coeffs, q, omega):
    return sum(
        abs(
            sum(
                value * e(-r * omega * z / q)
                for z, value in enumerate(coeffs)
            )
        )
        ** 2
        for r in range(q)
    )


def abel_bound(sequence, alpha):
    prefixes = []
    running = 0j
    for n, value in enumerate(sequence, start=1):
        running += value * e(alpha * n)
        prefixes.append(running)
    untwisted = abs(sum(sequence))
    sup_prefix = max(abs(value) for value in prefixes)
    bound = sup_prefix * (1 + len(sequence) * abs(1 - e(-alpha)))
    return untwisted, bound


def run():
    checks = 0
    coeffs = [1 + 0j, -1j, 0.5 + 0.25j, -0.75, 1.25j, 0.2 - 0.4j]
    alpha = 0.173
    direct = abs(block_sum(coeffs, alpha)) ** 2
    shifted = ttstar_sum(coeffs, alpha)
    assert close(direct, shifted.real)
    assert abs(shifted.imag) < 1e-9
    checks += 2

    for q, omega, data in (
        (7, 3, coeffs),
        (5, 2, coeffs + [0.3j, -0.6, 0.2 + 0.1j]),
    ):
        lhs = full_frequency_lhs(data, q, omega)
        rhs = alias_rhs(data, q)
        assert close(lhs, rhs)
        checks += 1

    n = 37
    alpha_generic = 2.5 / n
    matched = [e(alpha_generic * z) for z in range(n)]
    saturated = abs(block_sum(matched, alpha_generic))
    assert close(saturated, n)
    assert n * min(alpha_generic, 1 - alpha_generic) > 1
    checks += 2

    sequence = [1 if (n * n + 3 * n + 1) % 7 < 4 else -1 for n in range(1, 65)]
    untwisted, bound = abel_bound(sequence, 64 ** (-0.8))
    assert untwisted <= bound + 1e-9
    checks += 1

    result = {
        "schema": "tpc-108-generic-affine-certificate-v1",
        "status": "PASS",
        "checks": checks,
        "claim_boundary": {
            "finite_identity_only": True,
            "complete_frequency_average_only": True,
            "actual_H3_estimate": False,
            "fixed_h0_L2_estimate": False,
            "prime_pair_result": False,
        },
        "ttstar": {
            "direct_energy": direct,
            "shifted_energy_real": shifted.real,
            "shifted_energy_imag": shifted.imag,
        },
        "generic_saturation": {
            "length": n,
            "N_times_phase_distance": n * alpha_generic,
            "sum_abs": saturated,
        },
        "abel_check": {
            "untwisted_sum_abs": untwisted,
            "finite_bound": bound,
        },
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
