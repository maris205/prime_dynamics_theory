#!/usr/bin/env python3
"""Finite checks for TPC-101; not an asymptotic arithmetic theorem."""

from __future__ import annotations

import cmath
import json
import math


TOL = 2.0e-9
PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)


def primitive_root(q: int) -> int:
    n = q - 1
    factors: list[int] = []
    d = 2
    m = n
    while d * d <= m:
        if m % d == 0:
            factors.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        factors.append(m)
    for g in range(2, q):
        if all(pow(g, n // p, q) != 1 for p in factors):
            return g
    raise AssertionError("primitive root not found")


def character_table(q: int) -> tuple[list[int], list[list[complex]]]:
    n = q - 1
    g = primitive_root(q)
    logs = [0] * q
    x = 1
    for e in range(n):
        logs[x] = e
        x = (x * g) % q
    table: list[list[complex]] = []
    for k in range(n):
        table.append(
            [
                cmath.exp(2j * math.pi * k * logs[x] / n)
                for x in range(1, q)
            ]
        )
    return logs, table


def fourier(values: list[complex], chars: list[list[complex]]) -> list[complex]:
    return [
        sum(v * z.conjugate() for v, z in zip(values, chi))
        for chi in chars
    ]


def e_indicator(q: int, h: int) -> list[complex]:
    active = set(range(1, h + 1))
    active.update(q - j for j in range(1, h + 1))
    return [complex(int(x in active)) for x in range(1, q)]


def l2(values: list[complex]) -> float:
    return math.sqrt(sum(abs(v) ** 2 for v in values))


def centered(values: list[complex]) -> list[complex]:
    mean = sum(values) / len(values)
    return [v - mean for v in values]


def deterministic_weights(q: int) -> tuple[list[complex], list[complex]]:
    a = [
        complex(((7 * x + 3) % 11) - 5, ((5 * x + 1) % 7) - 3)
        for x in range(1, q)
    ]
    b = [
        complex(((3 * x + 2) % 9) - 4, ((2 * x + 4) % 5) - 2)
        / (1 + x)
        for x in range(1, q)
    ]
    return a, b


def incidence(q: int, h: int, a: list[complex], b: list[complex]) -> complex:
    active = set(range(1, h + 1))
    active.update(q - j for j in range(1, h + 1))
    return sum(
        a[omega - 1] * b[r - 1]
        for omega in range(1, q)
        for r in range(1, q)
        if (r * omega) % q in active
    )


def check_spectrum_and_functional() -> tuple[dict[str, int], float]:
    counts = {
        "exact_remainder_identity": 0,
        "fixed_filter_norm_bound": 0,
        "constructed_extremizer": 0,
        "wiener_hs_bound": 0,
        "delta_sharpness": 0,
        "full_window_endpoint": 0,
        "resolved_length_gain": 0,
    }
    max_error = 0.0
    for q in PRIMES:
        n = q - 1
        _, chars = character_table(q)
        a, b = deterministic_weights(q)
        ahat = fourier(a, chars)
        bhat = fourier(b, chars)
        for h in range(1, n // 2 + 1):
            ehat = fourier(e_indicator(q, h), chars)
            direct = incidence(q, h, a, b)
            principal = (2 * h / n) * sum(a) * sum(b)
            remainder = direct - principal
            spectral = sum(
                ehat[k] * ahat[(-k) % n] * bhat[(-k) % n]
                for k in range(1, n)
            ) / n
            err = abs(remainder - spectral)
            max_error = max(max_error, err)
            assert err < TOL * max(1.0, abs(direct))
            counts["exact_remainder_identity"] += 1

            s_sq = sum(
                abs(ehat[k]) ** 2 * abs(bhat[(-k) % n]) ** 2
                for k in range(1, n)
            ) / n
            s_mass = math.sqrt(max(0.0, s_sq))
            assert abs(remainder) <= s_mass * l2(centered(a)) + TOL
            counts["fixed_filter_norm_bound"] += 1

            y = [0j] * n
            for k in range(1, n):
                y[k] = ehat[k] * bhat[(-k) % n]
            target_ahat = [0j] * n
            for k in range(1, n):
                target_ahat[(-k) % n] = y[k].conjugate()
            a_ext = [
                sum(target_ahat[k] * chars[k][x - 1] for k in range(n)) / n
                for x in range(1, q)
            ]
            ext_r = incidence(q, h, a_ext, b)
            ext_r -= (2 * h / n) * sum(a_ext) * sum(b)
            if s_mass > TOL:
                assert abs(abs(ext_r) / l2(a_ext) - s_mass) < 5.0e-8
            counts["constructed_extremizer"] += 1

            g = math.sqrt(2 * h * (n - 2 * h) / n)
            assert s_mass <= sum(abs(z) for z in b) * g + TOL
            counts["wiener_hs_bound"] += 1

            b_delta = [0j] * n
            b_delta[(2 % q) - 1] = 3 - 4j
            delta_hat = fourier(b_delta, chars)
            delta_s_sq = sum(
                abs(ehat[k]) ** 2 * abs(delta_hat[(-k) % n]) ** 2
                for k in range(1, n)
            ) / n
            assert abs(math.sqrt(max(0.0, delta_s_sq)) - 5 * g) < 5.0e-8
            counts["delta_sharpness"] += 1

            if h == n // 2:
                assert g == 0.0
                assert max(abs(ehat[k]) for k in range(1, n)) < TOL
                counts["full_window_endpoint"] += 1

        for length in range(1, q + 1):
            h = min(n // 2, q // length)
            g = math.sqrt(2 * h * (n - 2 * h) / n)
            if length <= 2:
                assert g == 0.0
            else:
                assert g <= math.sqrt(2 * q / length) + TOL
            counts["resolved_length_gain"] += 1
    return counts, max_error


def check_principal_diagonal_transfer() -> int:
    checks = 0
    for q in PRIMES[2:]:
        n = q - 1
        data: dict[int, list[list[int]]] = {}
        for h in range(1, n // 2 + 1):
            cells: list[list[int]] = []
            for c in range(1, 1 + (h % 3) + 1):
                size = 1 + ((2 * h + c) % min(5, n))
                cells.append([1 + ((h + 3 * c + 2 * j) % 7) for j in range(size)])
            data[h] = cells
        max_weight = max(w for cells in data.values() for cell in cells for w in cell)
        principal = 0.0
        lhs = 0.0
        active = 0
        for h, cells in data.items():
            mass = sum(sum(cell) for cell in cells)
            diagonal = sum(
                sum(w * w for w in cell) - sum(cell) ** 2 / n
                for cell in cells
            )
            assert diagonal >= -TOL
            g = math.sqrt(2 * h * (n - 2 * h) / n)
            principal += (2 * h / n) * mass
            lhs += g * math.sqrt(max(0.0, diagonal))
            if g > 0 and mass > 0:
                active += 1
            checks += sum(len(cell) for cell in cells)
        rhs = math.sqrt(max_weight * active * n * principal)
        assert lhs <= rhs + TOL
        checks += 1
    return checks


def main() -> None:
    counts, max_error = check_spectrum_and_functional()
    counts["principal_diagonal_transfer"] = check_principal_diagonal_transfer()
    report = {
        "all_checks_passed": True,
        "counts": counts,
        "maximum_complex_roundoff": max_error,
        "description": (
            "Finite fixed-filter norm, Wiener-to-Hilbert-Schmidt, "
            "sharpness, length-gain, and diagonal-transfer regression; "
            "not an asymptotic Mobius or prime-pair theorem"
        ),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
