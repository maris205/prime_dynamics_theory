#!/usr/bin/env python3
"""Small smoke tests for the floating zero-Mellin diagnostic."""

from __future__ import annotations

import math

from zero_mellin_diagnostic import (
    C2,
    evaluate_scale,
    prime_list,
    small_coefficient,
    tau_array,
    von_mangoldt_array,
)


def test_arrays() -> None:
    primes = prime_list(100)
    values = von_mangoldt_array(100, primes)
    assert values[1] == 0.0
    assert values[12] == 0.0
    assert math.isclose(values[8], math.log(2))
    assert math.isclose(values[49], math.log(7))
    tau = tau_array(20)
    assert tau[1] == 1
    assert tau[12] == 6


def test_small_coefficient_against_divisors() -> None:
    primes = prime_list(200)
    values = von_mangoldt_array(200, primes)
    r0, r1, cutoff = 50, 100, 13
    actual = small_coefficient(r0, r1, cutoff, values)
    for r in range(r0, r1 + 1):
        expected = sum(values[d] - 1.0 for d in range(1, cutoff + 1) if r % d == 0)
        assert math.isclose(actual[r - r0], expected, abs_tol=1e-12)


def test_scale_additivity() -> None:
    x, h = 512, 2
    primes = prime_list(2 * x + h + 10)
    values = von_mangoldt_array(2 * x + h + 10, primes)
    tau = tau_array(2 * x)
    row = evaluate_scale(x, h, values, tau)
    assert math.isclose(
        row["complete_over_XlogX"],
        row["small_over_XlogX"] + row["large_over_XlogX"],
        abs_tol=1e-12,
    )
    assert 0.6 < C2 < 0.7


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def test_scale_against_independent_double_sum() -> None:
    for x, h in ((50, 2), (64, -3), (100, 7)):
        limit = 2 * x + abs(h) + 10
        values = von_mangoldt_array(limit, prime_list(limit))
        tau = tau_array(2 * x)
        row = evaluate_scale(x, h, values, tau)
        cutoff = math.isqrt(x)
        direct = {"complete": 0.0, "small": 0.0, "large": 0.0}
        for r in range(x + 1, 2 * x + 1):
            target = r + h
            target_lambda = values[target] if 0 <= target < len(values) else 0.0
            for d in divisors(r):
                term = (values[d] - 1.0) * target_lambda
                direct["complete"] += term
                direct["small" if d <= cutoff else "large"] += term
        scale = x * math.log(x)
        assert math.isclose(row["complete_over_XlogX"], direct["complete"] / scale, abs_tol=1e-12)
        assert math.isclose(row["small_over_XlogX"], direct["small"] / scale, abs_tol=1e-12)
        assert math.isclose(row["large_over_XlogX"], direct["large"] / scale, abs_tol=1e-12)


def main() -> None:
    tests = [
        test_arrays,
        test_small_coefficient_against_divisors,
        test_scale_additivity,
        test_scale_against_independent_double_sum,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"{len(tests)} tests passed")


if __name__ == "__main__":
    main()
