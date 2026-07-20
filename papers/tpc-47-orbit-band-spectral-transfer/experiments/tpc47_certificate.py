#!/usr/bin/env python3
"""Deterministic exact certificate for TPC-47.

The certificate has three arithmetic layers.

* A finite cyclic analogue over F_601 verifies the literal fiberwise
  orbit-comb projection, the full signed actual-mask reassembly, the
  low-profile plus tail decomposition, determinant-frequency transfer,
  and the physical residual label s=d(m)r.
* Gaussian rationals verify Hilbert-space projection, Plancherel,
  finite-difference tail, commutation, and signed reassembly identities.
* Rational interval arithmetic, with pi enclosed by Machin's formula,
  certifies finite sinc-comb Gram matrices and the thin-sector witnesses.

The finite cyclic portion is an exact finite analogue, not a proof of
the continuous asymptotic Fourier-tail estimates in the paper.  No
randomness or floating-point arithmetic is used.
"""

from __future__ import annotations

import ast
from fractions import Fraction
from hashlib import sha256
import itertools
import json
from math import comb, gcd
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def prime_divisors(n: int) -> tuple[int, ...]:
    ans = []
    d = 2
    work = n
    while d * d <= work:
        if work % d == 0:
            ans.append(d)
            while work % d == 0:
                work //= d
        d += 1
    if work > 1:
        ans.append(work)
    return tuple(ans)


def is_squarefree(n: int) -> bool:
    return all(n % (p * p) != 0 for p in prime_divisors(n))


def primitive_root(p: int) -> int:
    require(is_prime(p), "primitive-root modulus is prime")
    factors = prime_divisors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError("primitive root not found")


def mod_dft(values: list[int], omega: int, modulus: int) -> list[int]:
    n = len(values)
    return [
        sum(
            values[j] * pow(omega, (-j * q) % n, modulus)
            for j in range(n)
        ) % modulus
        for q in range(n)
    ]


def mod_idft(values: list[int], omega: int, modulus: int) -> list[int]:
    n = len(values)
    inv_n = pow(n, -1, modulus)
    return [
        inv_n * sum(
            values[q] * pow(omega, (j * q) % n, modulus)
            for q in range(n)
        ) % modulus
        for j in range(n)
    ]


def mod_project(
    values: list[int], band: set[int], omega: int, modulus: int
) -> list[int]:
    transformed = mod_dft(values, omega, modulus)
    retained = [
        transformed[q] if q in band else 0
        for q in range(len(values))
    ]
    return mod_idft(retained, omega, modulus)


def cyclic_difference(values: list[int], modulus: int) -> list[int]:
    n = len(values)
    return [
        (values[(j + 1) % n] - values[j]) % modulus
        for j in range(n)
    ]


def matrix_rank_mod(matrix: list[list[int]], modulus: int) -> int:
    if not matrix:
        return 0
    a = [[value % modulus for value in row] for row in matrix]
    rows = len(a)
    columns = len(a[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (r for r in range(rank, rows) if a[r][column]), None
        )
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], -1, modulus)
        a[rank] = [(inverse * value) % modulus for value in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [
                (a[r][c] - factor * a[rank][c]) % modulus
                for c in range(columns)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def null_vector_mod(matrix: list[list[int]], modulus: int) -> list[int]:
    if not matrix:
        return [1]
    a = [[value % modulus for value in row] for row in matrix]
    rows = len(a)
    columns = len(a[0])
    pivot_columns = []
    rank = 0
    for column in range(columns):
        pivot = next(
            (r for r in range(rank, rows) if a[r][column]), None
        )
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], -1, modulus)
        a[rank] = [(inverse * value) % modulus for value in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [
                (a[r][c] - factor * a[rank][c]) % modulus
                for c in range(columns)
            ]
        pivot_columns.append(column)
        rank += 1
        if rank == rows:
            break
    free_columns = [
        c for c in range(columns) if c not in pivot_columns
    ]
    require(bool(free_columns), "nullspace has a free column")
    free = free_columns[-1]
    vector = [0] * columns
    vector[free] = 1
    for r in range(rank - 1, -1, -1):
        pivot = pivot_columns[r]
        vector[pivot] = -sum(
            a[r][c] * vector[c]
            for c in range(pivot + 1, columns)
        ) % modulus
    return vector


def check_cyclic_actual_transfer() -> dict:
    """Check the complete finite actual-mask/residual spectral model."""
    start = CHECKS
    n = 60
    modulus = 601
    generator = primitive_root(modulus)
    omega = pow(generator, (modulus - 1) // n, modulus)
    require(pow(omega, n, modulus) == 1, "60th root closes")
    for exponent in range(1, n):
        require(pow(omega, exponent, modulus) != 1,
                "60th root has exact order")
    require((n * pow(n, -1, modulus)) % modulus == 1,
            "cyclic transform normalization is invertible")

    h0 = 3
    branch = {0, 20, 40}
    core_band = {q % n for q in range(-2, 3)}
    orbit_band = {
        (q + branch_frequency) % n
        for q in core_band
        for branch_frequency in branch
    }
    profile_band = {q % n for q in range(-1, 2)}
    coefficient_band = {
        (q + branch_frequency) % n
        for q in profile_band
        for branch_frequency in branch
    }
    product_support = {
        (q + u + t) % n
        for q in orbit_band
        for u in profile_band
        for t in branch
    }
    require(len(orbit_band) == 15, "finite orbit-comb band size")
    require(len(coefficient_band) == 9,
            "finite actual-coefficient comb band size")
    require(len(product_support) == 21,
            "profile-broadened comb support size")

    rows = [
        (7, 11, 77),
        (11, 13, 143),
        (13, 7, 91),
        (17, 11, 187),
    ]
    outputs = [
        (19, 7, 133),
        (23, 11, 253),
        (29, 13, 377),
    ]
    expected_mask = [
        [1, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
    ]
    row_signs = [2, -3, 5, -7]
    row_weights = [11, 13, 17, 19]
    primes = [37, 41, 43]
    cofactors = [1, 17]

    for prime in primes:
        require(is_prime(prime), "toy source prime is prime")
    for ell, divisor, source_integer in rows:
        require(source_integer == ell * divisor,
                "source row product is literal")
        require(gcd(ell, divisor) == 1,
                "source row factors are coprime")
        require(is_squarefree(divisor), "source divisor is squarefree")
        require(gcd(source_integer, n) == 1,
                "source slope is a cyclic unit")

    def actual_mask(row_index: int, output_index: int) -> int:
        ell, divisor, source_integer = rows[row_index]
        out_ell, out_divisor, out_integer = outputs[output_index]
        return int(
            ell != out_ell
            and abs(source_integer - out_integer) > 50
            and gcd(divisor, out_divisor) <= 3
        )

    for row_index in range(len(rows)):
        for output_index in range(len(outputs)):
            require(
                actual_mask(row_index, output_index)
                == expected_mask[row_index][output_index],
                "literal actual static mask table",
            )
    require(sum(map(sum, expected_mask)) == 7,
            "actual mask has seven active row-output entries")

    residuals = sorted({
        divisor * cofactor
        for _, divisor, _ in rows
        for cofactor in cofactors
    })
    require(residuals == [7, 11, 13, 119, 187, 221],
            "literal residual label set")
    for _, divisor, _ in rows:
        for cofactor in cofactors:
            require(is_squarefree(divisor * cofactor),
                    "supported residual label is squarefree")

    fibers = [
        (output_index, residual)
        for output_index in range(len(outputs))
        for residual in residuals
    ]
    z_full = {}
    z_low = {}
    z_high = {}
    z_hat = {}
    z_low_hat = {}
    for fiber_index, fiber in enumerate(fibers):
        transformed = [
            1 + (
                31 * (fiber_index + 1)
                + 7 * q * q
                + 13 * q
            ) % (modulus - 1)
            for q in range(n)
        ]
        low_transformed = [
            transformed[q] if q in orbit_band else 0
            for q in range(n)
        ]
        full = mod_idft(transformed, omega, modulus)
        low = mod_idft(low_transformed, omega, modulus)
        high = [(full[j] - low[j]) % modulus for j in range(n)]
        z_full[fiber] = full
        z_low[fiber] = low
        z_high[fiber] = high
        z_hat[fiber] = transformed
        z_low_hat[fiber] = low_transformed

        round_trip = mod_dft(full, omega, modulus)
        projected_transform = mod_dft(low, omega, modulus)
        second_projection = mod_project(low, orbit_band, omega, modulus)
        for q in range(n):
            require(round_trip[q] == transformed[q],
                    "fiber DFT round trip")
            require(projected_transform[q] == low_transformed[q],
                    "fiberwise comb projection")
        for j in range(n):
            require(second_projection[j] == low[j],
                    "fiberwise comb projector is idempotent")
            require((low[j] + high[j]) % modulus == full[j],
                    "fiber low-high decomposition")
        require(any(value for value in low),
                "projected finite fiber is nonzero")
        require(any(value for value in high),
                "high finite fiber is nonzero")

    profile_full = {}
    profile_low = {}
    profile_high = {}
    profile_low_hat = {}
    for row_index in range(len(rows)):
        for residue in range(h0):
            transformed = [
                0 if q in coefficient_band and q not in profile_band
                else 1 + (
                    17 * (row_index + 1)
                    + 29 * (residue + 1)
                    + 5 * q * q
                    + 11 * q
                ) % (modulus - 1)
                for q in range(n)
            ]
            low_transformed = [
                transformed[q] if q in profile_band else 0
                for q in range(n)
            ]
            full = mod_idft(transformed, omega, modulus)
            low = mod_idft(low_transformed, omega, modulus)
            high = [(full[j] - low[j]) % modulus for j in range(n)]
            key = (row_index, residue)
            profile_full[key] = full
            profile_low[key] = low
            profile_high[key] = high
            profile_low_hat[key] = low_transformed

            round_trip = mod_dft(full, omega, modulus)
            low_round_trip = mod_dft(low, omega, modulus)
            for q in range(n):
                require(round_trip[q] == transformed[q],
                        "profile DFT round trip")
            for j in range(n):
                require((low[j] + high[j]) % modulus == full[j],
                        "profile low-tail split")
            for q in set(range(n)) - profile_band:
                require(low_round_trip[q] == 0,
                        "low profile support")

            difference = full
            for order in range(1, 4):
                difference = cyclic_difference(difference, modulus)
                difference_transform = mod_dft(
                    difference, omega, modulus
                )
                for q in range(n):
                    multiplier = pow(
                        (pow(omega, q, modulus) - 1) % modulus,
                        order,
                        modulus,
                    )
                    require(
                        difference_transform[q]
                        == multiplier * transformed[q] % modulus,
                        "finite-difference Fourier multiplier",
                    )

    delta_hat = {}
    for residue in range(h0):
        delta = [int(j % h0 == residue) for j in range(n)]
        transformed = mod_dft(delta, omega, modulus)
        delta_hat[residue] = transformed
        for q in range(n):
            expected = 0
            if q in branch:
                expected = (
                    (n // h0)
                    * pow(omega, (-residue * q) % n, modulus)
                ) % modulus
            require(transformed[q] == expected,
                    "progression selector transform")

    # A row-delta signed projective representation is deliberately
    # reassembled as a whole.  No individual layer is selected.
    for row_index in range(len(rows)):
        for output_index in range(len(outputs)):
            for residue in range(h0):
                for j in range(n):
                    selector = int(j % h0 == residue)
                    direct = (
                        row_signs[row_index]
                        * actual_mask(row_index, output_index)
                        * selector
                        * profile_full[(row_index, residue)][j]
                    ) % modulus
                    reassembled = sum(
                        row_signs[layer]
                        * int(layer == row_index)
                        * actual_mask(layer, output_index)
                        * selector
                        * profile_full[(layer, residue)][j]
                        for layer in range(len(rows))
                    ) % modulus
                    low_part = sum(
                        row_signs[layer]
                        * int(layer == row_index)
                        * actual_mask(layer, output_index)
                        * selector
                        * profile_low[(layer, residue)][j]
                        for layer in range(len(rows))
                    ) % modulus
                    tail_part = sum(
                        row_signs[layer]
                        * int(layer == row_index)
                        * actual_mask(layer, output_index)
                        * selector
                        * profile_high[(layer, residue)][j]
                        for layer in range(len(rows))
                    ) % modulus
                    require(reassembled == direct,
                            "whole signed actual-mask reassembly")
                    require((low_part + tail_part) % modulus == direct,
                            "whole signed low-tail reassembly")

    # The low piece above is also the canonical projection of the
    # complete, already-reassembled actual coefficient.  The deliberate
    # zeroes at the two noncentral copies of the profile band prevent a
    # finite-cyclic wraparound from masquerading as continuous smooth
    # profile mass.
    for row_index in range(len(rows)):
        for output_index in range(len(outputs)):
            full_actual = [
                row_signs[row_index]
                * actual_mask(row_index, output_index)
                * profile_full[(row_index, j % h0)][j]
                % modulus
                for j in range(n)
            ]
            layer_low = [
                row_signs[row_index]
                * actual_mask(row_index, output_index)
                * profile_low[(row_index, j % h0)][j]
                % modulus
                for j in range(n)
            ]
            layer_tail = [
                row_signs[row_index]
                * actual_mask(row_index, output_index)
                * profile_high[(row_index, j % h0)][j]
                % modulus
                for j in range(n)
            ]
            canonical_low = mod_project(
                full_actual, coefficient_band, omega, modulus
            )
            for j in range(n):
                require(canonical_low[j] == layer_low[j],
                        "canonical whole-coefficient lowpass")
                require(
                    (canonical_low[j] + layer_tail[j]) % modulus
                    == full_actual[j],
                    "canonical whole-coefficient low-tail split",
                )

    kernel_cache = {}
    active_layer_fibers = []
    inv_n_squared = pow(n, -2, modulus)
    for row_index, (_, divisor, source_integer) in enumerate(rows):
        supported_residuals = {divisor * r for r in cofactors}
        for output_index in range(len(outputs)):
            if not actual_mask(row_index, output_index):
                continue
            for residual in sorted(supported_residuals):
                fiber = (output_index, residual)
                for residue in range(h0):
                    key = (row_index, output_index, residual, residue)
                    delta = [int(j % h0 == residue) for j in range(n)]
                    values = [
                        delta[j]
                        * profile_low[(row_index, residue)][j]
                        * z_low[fiber][j]
                        % modulus
                        for j in range(n)
                    ]
                    transformed = mod_dft(values, omega, modulus)
                    expected_transform = []
                    for q in range(n):
                        convolution = 0
                        for t in branch:
                            for u in profile_band:
                                v = (q - t - u) % n
                                convolution += (
                                    delta_hat[residue][t]
                                    * profile_low_hat[
                                        (row_index, residue)
                                    ][u]
                                    * z_low_hat[fiber][v]
                                )
                        expected_transform.append(
                            inv_n_squared * convolution % modulus
                        )
                    for q in range(n):
                        require(
                            transformed[q] == expected_transform[q],
                            "projected-profile-progression convolution",
                        )
                    for q in set(range(n)) - product_support:
                        require(transformed[q] == 0,
                                "profile-broadened comb support")

                    kernels = []
                    for k in range(n):
                        direct_kernel = sum(
                            values[j]
                            * pow(
                                omega,
                                (source_integer * j * k) % n,
                                modulus,
                            )
                            for j in range(n)
                        ) % modulus
                        expected_kernel = transformed[
                            (-source_integer * k) % n
                        ]
                        require(direct_kernel == expected_kernel,
                                "determinant orbit-to-shift transfer")
                        kernels.append(direct_kernel)
                    slope_support = {
                        k for k in range(n)
                        if (-source_integer * k) % n in product_support
                    }
                    for k in set(range(n)) - slope_support:
                        require(kernels[k] == 0,
                                "single-slope transferred gap")
                    kernel_cache[key] = kernels
                    active_layer_fibers.append(key)

    prime_weights = {p: (3 * p + 1) % modulus for p in primes}
    cofactor_weights = {1: 5, 17: -11}
    row_scalar = {
        row_index: row_weights[row_index] * row_signs[row_index]
        for row_index in range(len(rows))
    }
    residual_index = {s: index for index, s in enumerate(residuals)}
    packet_low = [
        [[0 for _ in residuals] for _ in outputs]
        for _ in range(n)
    ]
    packet_full = [
        [[0 for _ in residuals] for _ in outputs]
        for _ in range(n)
    ]
    packet_tail = [
        [[0 for _ in residuals] for _ in outputs]
        for _ in range(n)
    ]
    for prime in primes:
        for cofactor in cofactors:
            for row_index, (_, divisor, source_integer) in enumerate(rows):
                residual = divisor * cofactor
                s_index = residual_index[residual]
                for output_index in range(len(outputs)):
                    if not actual_mask(row_index, output_index):
                        continue
                    fiber = (output_index, residual)
                    base = (
                        prime_weights[prime]
                        * cofactor_weights[cofactor]
                        * row_scalar[row_index]
                    ) % modulus
                    for j in range(n):
                        residue = j % h0
                        h = (prime * cofactor - source_integer * j) % n
                        low_value = (
                            base
                            * profile_low[(row_index, residue)][j]
                            * z_low[fiber][j]
                        ) % modulus
                        tail_value = (
                            base
                            * profile_high[(row_index, residue)][j]
                            * z_low[fiber][j]
                        ) % modulus
                        full_value = (
                            base
                            * profile_full[(row_index, residue)][j]
                            * z_low[fiber][j]
                        ) % modulus
                        packet_low[h][output_index][s_index] = (
                            packet_low[h][output_index][s_index]
                            + low_value
                        ) % modulus
                        packet_tail[h][output_index][s_index] = (
                            packet_tail[h][output_index][s_index]
                            + tail_value
                        ) % modulus
                        packet_full[h][output_index][s_index] = (
                            packet_full[h][output_index][s_index]
                            + full_value
                        ) % modulus

    packet_frequency = {}
    for output_index, residual in fibers:
        s_index = residual_index[residual]
        low_sequence = [
            packet_low[h][output_index][s_index] for h in range(n)
        ]
        full_sequence = [
            packet_full[h][output_index][s_index] for h in range(n)
        ]
        tail_sequence = [
            packet_tail[h][output_index][s_index] for h in range(n)
        ]
        for h in range(n):
            require(
                (low_sequence[h] + tail_sequence[h]) % modulus
                == full_sequence[h],
                "literal packet low-tail identity",
            )
        transformed = mod_dft(low_sequence, omega, modulus)
        packet_frequency[(output_index, residual)] = transformed
        for k in range(n):
            rhs = 0
            for prime in primes:
                for cofactor in cofactors:
                    for row_index, (_, divisor, _) in enumerate(rows):
                        if divisor * cofactor != residual:
                            continue
                        if not actual_mask(row_index, output_index):
                            continue
                        base = (
                            prime_weights[prime]
                            * cofactor_weights[cofactor]
                            * row_scalar[row_index]
                        ) % modulus
                        phase = pow(
                            omega, (-prime * cofactor * k) % n, modulus
                        )
                        for residue in range(h0):
                            rhs += (
                                base
                                * phase
                                * kernel_cache[
                                    (
                                        row_index,
                                        output_index,
                                        residual,
                                        residue,
                                    )
                                ][k]
                            )
            require(transformed[k] == rhs % modulus,
                    "literal actual packet shift factorization")

    slopes = [source_integer % n for _, _, source_integer in rows]
    total_support = {
        k for k in range(n)
        if any((-slope * k) % n in product_support for slope in slopes)
    }
    global_gap = set(range(n)) - total_support
    expected_gap = {
        4, 5, 8, 10, 12, 15, 16,
        24, 25, 28, 30, 32, 35, 36,
        44, 45, 48, 50, 52, 55, 56,
    }
    require(global_gap == expected_gap,
            "literal four-slope transferred gap ledger")
    for transformed in packet_frequency.values():
        for k in global_gap:
            require(transformed[k] == 0,
                    "whole actual packet vanishes on transferred gap")
    require(any(
        value
        for transformed in packet_frequency.values()
        for value in transformed
    ), "whole projected actual packet is nonzero")

    return {
        "checks": CHECKS - start,
        "arithmetic": "F_601 on Z/60Z",
        "orbit_comb_band_size": len(orbit_band),
        "actual_coefficient_comb_band_size": len(coefficient_band),
        "profile_broadened_support_size": len(product_support),
        "single_slope_gap_size": n - len(product_support),
        "whole_packet_gap": sorted(global_gap),
        "whole_packet_gap_size": len(global_gap),
        "actual_mask_active_entries": sum(map(sum, expected_mask)),
        "residual_labels": residuals,
        "active_layer_fibers": len(active_layer_fibers),
    }


G = tuple[Fraction, Fraction]


def gaussian(real: int | Fraction, imag: int | Fraction = 0) -> G:
    return (Fraction(real), Fraction(imag))


def gadd(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def gsub(x: G, y: G) -> G:
    return (x[0] - y[0], x[1] - y[1])


def gmul(x: G, y: G) -> G:
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0],
    )


def gconj(x: G) -> G:
    return (x[0], -x[1])


def gscale(scale: int | Fraction, x: G) -> G:
    value = Fraction(scale)
    return (value * x[0], value * x[1])


def gnorm2(x: G) -> Fraction:
    return x[0] * x[0] + x[1] * x[1]


def ginner(x: list[G], y: list[G]) -> G:
    value = gaussian(0)
    for left, right in zip(x, y):
        value = gadd(value, gmul(left, gconj(right)))
    return value


def ipow(exponent: int) -> G:
    return [gaussian(1), gaussian(0, 1), gaussian(-1), gaussian(0, -1)][
        exponent % 4
    ]


def gaussian_dft(values: list[G]) -> list[G]:
    require(len(values) == 4, "Gaussian DFT has order four")
    return [
        sum_gaussian([
            gmul(values[j], ipow(-j * q)) for j in range(4)
        ])
        for q in range(4)
    ]


def gaussian_idft(values: list[G]) -> list[G]:
    require(len(values) == 4, "Gaussian inverse DFT has order four")
    return [
        gscale(Fraction(1, 4), sum_gaussian([
            gmul(values[q], ipow(j * q)) for q in range(4)
        ]))
        for j in range(4)
    ]


def sum_gaussian(values: list[G]) -> G:
    total = gaussian(0)
    for value in values:
        total = gadd(total, value)
    return total


def gaussian_project(values: list[G], band: set[int]) -> list[G]:
    transformed = gaussian_dft(values)
    retained = [
        transformed[q] if q in band else gaussian(0) for q in range(4)
    ]
    return gaussian_idft(retained)


def gaussian_difference(values: list[G]) -> list[G]:
    return [gsub(values[(j + 1) % 4], values[j]) for j in range(4)]


def vector_norm2(values: list[G]) -> Fraction:
    return sum((gnorm2(value) for value in values), Fraction())


def check_gaussian_hilbert_identities() -> dict:
    start = CHECKS
    band = {0, 1}
    vectors = []
    for seed in range(1, 49):
        vector = [
            gaussian(
                ((seed + 2) * (j + 3) + j * j) % 13 - 6,
                ((seed + 5) * (2 * j + 1) + 3 * j * j) % 17 - 8,
            )
            for j in range(4)
        ]
        vectors.append(vector)

        transformed = gaussian_dft(vector)
        round_trip = gaussian_idft(transformed)
        projected = gaussian_project(vector, band)
        projected_twice = gaussian_project(projected, band)
        complement = [
            gsub(vector[j], projected[j]) for j in range(4)
        ]
        for j in range(4):
            require(round_trip[j] == vector[j],
                    "Gaussian DFT inversion")
            require(projected_twice[j] == projected[j],
                    "Gaussian orbit projector idempotence")
            require(gadd(projected[j], complement[j]) == vector[j],
                    "Gaussian projection decomposition")
        require(
            vector_norm2(vector)
            == vector_norm2(projected) + vector_norm2(complement),
            "Gaussian projection Pythagoras",
        )
        require(vector_norm2(projected) <= vector_norm2(vector),
                "Gaussian projection contraction")

        difference = vector
        for order in range(1, 4):
            difference = gaussian_difference(difference)
            difference_transform = gaussian_dft(difference)
            for q in range(4):
                multiplier = ipow(q)
                multiplier = gsub(multiplier, gaussian(1))
                power = gaussian(1)
                for _ in range(order):
                    power = gmul(power, multiplier)
                require(
                    difference_transform[q]
                    == gmul(power, transformed[q]),
                    "Gaussian finite-difference multiplier",
                )
            high_energy = sum(
                (gnorm2(transformed[q]) for q in [1, 2, 3]),
                Fraction(),
            )
            difference_energy = sum(
                (gnorm2(value) for value in difference_transform),
                Fraction(),
            )
            require(
                high_energy * (2 ** order) <= difference_energy,
                "exact discrete Sobolev tail inequality",
            )

    for index in range(0, len(vectors), 2):
        x = vectors[index]
        y = vectors[index + 1]
        px = gaussian_project(x, band)
        py = gaussian_project(y, band)
        require(ginner(px, y) == ginner(x, py),
                "Gaussian projector self-adjointness")

    # Residual signs act in a tensor factor disjoint from orbit time.
    for sign in [-1, 1]:
        for vector in vectors[:8]:
            signed = [gscale(sign, value) for value in vector]
            projected_signed = gaussian_project(signed, band)
            signed_projected = [
                gscale(sign, value)
                for value in gaussian_project(vector, band)
            ]
            for j in range(4):
                require(projected_signed[j] == signed_projected[j],
                        "residual unitary commutes with orbit projection")

    # Signed projective reassembly bound and its aligned sharpness.
    absolute_coefficients = [1, 2, 3, 5]
    phases = [ipow(q) for q in range(4)]
    mass = sum(absolute_coefficients)
    for seed in range(32):
        layers = []
        for layer in range(4):
            vector = [
                gaussian(
                    ((seed + 1) * (layer + 2) * (j + 1)) % 11 - 5,
                    ((seed + 3) * (layer + 1) + 2 * j) % 13 - 6,
                )
                for j in range(4)
            ]
            layers.append([
                gmul(phases[layer], value) for value in vector
            ])
        reassembled = [
            sum_gaussian([
                gscale(absolute_coefficients[layer], layers[layer][j])
                for layer in range(4)
            ])
            for j in range(4)
        ]
        weighted_layer_energy = sum(
            Fraction(absolute_coefficients[layer])
            * vector_norm2(layers[layer])
            for layer in range(4)
        )
        require(
            vector_norm2(reassembled)
            <= mass * weighted_layer_energy,
            "signed Hilbert reassembly bound",
        )

    aligned = [gaussian(2, -1), gaussian(-3, 4), gaussian(1, 5), gaussian(-2)]
    aligned_sum = [gscale(mass, value) for value in aligned]
    require(
        vector_norm2(aligned_sum)
        == mass * mass * vector_norm2(aligned),
        "projective mass-square sharpness",
    )

    return {
        "checks": CHECKS - start,
        "arithmetic": "Gaussian rationals",
        "deterministic_vectors": len(vectors),
        "projector_band": sorted(band),
        "signed_reassembly_trials": 32,
    }


Interval = tuple[Fraction, Fraction]


def interval(value: int | Fraction) -> Interval:
    point = Fraction(value)
    return (point, point)


def iadd(x: Interval, y: Interval) -> Interval:
    return (x[0] + y[0], x[1] + y[1])


def ineg(x: Interval) -> Interval:
    return (-x[1], -x[0])


def isub(x: Interval, y: Interval) -> Interval:
    return iadd(x, ineg(y))


def imul(x: Interval, y: Interval) -> Interval:
    products = [
        x[0] * y[0], x[0] * y[1], x[1] * y[0], x[1] * y[1]
    ]
    return (min(products), max(products))


def iscale(scale: int | Fraction, x: Interval) -> Interval:
    return imul(interval(scale), x)


def ireciprocal(x: Interval) -> Interval:
    require(not (x[0] <= 0 <= x[1]),
            "interval reciprocal avoids zero")
    candidates = [
        Fraction(x[0].denominator, x[0].numerator),
        Fraction(x[1].denominator, x[1].numerator),
    ]
    return (min(candidates), max(candidates))


def idiv(x: Interval, y: Interval) -> Interval:
    return imul(x, ireciprocal(y))


def atan_inverse_interval(q: int, terms: int) -> Interval:
    total = Fraction()
    for n in range(terms):
        term = Fraction(1, (2 * n + 1) * q ** (2 * n + 1))
        total += term if n % 2 == 0 else -term
    next_term = Fraction(
        1, (2 * terms + 1) * q ** (2 * terms + 1)
    )
    next_signed = next_term if terms % 2 == 0 else -next_term
    other = total + next_signed
    return (min(total, other), max(total, other))


def pi_interval() -> Interval:
    atan_five = atan_inverse_interval(5, 160)
    atan_239 = atan_inverse_interval(239, 48)
    return isub(iscale(16, atan_five), iscale(4, atan_239))


def comb_sinc_entry(diff: int, inverse_pi: Interval) -> Interval:
    """H0=3, Omega=1/12 comb-sinc kernel."""
    if diff == 0:
        return interval(Fraction(1, 2))
    if diff % 3 != 0:
        return interval(0)
    reduced = diff // 3
    if reduced % 2 == 0:
        return interval(0)
    magnitude = abs(reduced)
    sign = -1 if ((magnitude - 1) // 2) % 2 else 1
    return iscale(Fraction(sign, magnitude), inverse_pi)


def interval_ldl_positive(matrix: list[list[Interval]]) -> int:
    size = len(matrix)
    lower = [[interval(0) for _ in range(size)] for _ in range(size)]
    diagonal = [interval(0) for _ in range(size)]
    pivot_checks = 0
    for k in range(size):
        value = matrix[k][k]
        for j in range(k):
            value = isub(
                value,
                imul(imul(lower[k][j], lower[k][j]), diagonal[j]),
            )
        diagonal[k] = value
        require(value[0] > 0, "rigorous sinc-comb LDL pivot")
        pivot_checks += 1
        lower[k][k] = interval(1)
        for i in range(k + 1, size):
            numerator = matrix[i][k]
            for j in range(k):
                numerator = isub(
                    numerator,
                    imul(
                        imul(lower[i][j], lower[k][j]), diagonal[j]
                    ),
                )
            lower[i][k] = idiv(numerator, diagonal[k])
    return pivot_checks


def interval_quadratic(
    coefficients: list[int], positions: list[int], inverse_pi: Interval
) -> Interval:
    total = interval(0)
    for i, left in enumerate(coefficients):
        for j, right in enumerate(coefficients):
            total = iadd(
                total,
                iscale(
                    left * right,
                    comb_sinc_entry(
                        positions[i] - positions[j], inverse_pi
                    ),
                ),
            )
    return total


def check_sinc_comb_and_mass_frontier() -> dict:
    start = CHECKS
    enclosed_pi = pi_interval()
    require(enclosed_pi[0] > 3, "Machin lower bound for pi")
    require(enclosed_pi[1] < Fraction(22, 7),
            "Machin upper bound for pi")
    inverse_pi = ireciprocal(enclosed_pi)

    pivot_checks = 0
    for size in range(1, 13):
        matrix = [
            [
                comb_sinc_entry(i - j, inverse_pi)
                for j in range(size)
            ]
            for i in range(size)
        ]
        pivot_checks += interval_ldl_positive(matrix)
        trace = sum(
            (matrix[j][j][0] for j in range(size)), Fraction()
        )
        require(trace == Fraction(size, 2),
                "exact comb time-bandwidth trace")

    witness_ratios = []
    for order in range(1, 13):
        coefficients = [
            (-1) ** k * comb(order, k) for k in range(order + 1)
        ]
        positions = [3 * k for k in range(order + 1)]
        energy = interval_quadratic(coefficients, positions, inverse_pi)
        norm_squared = sum(value * value for value in coefficients)
        require(norm_squared == comb(2 * order, order),
                "central-binomial difference norm")
        require(4 * order * norm_squared * norm_squared >= 16 ** order,
                "exact central-binomial lower bound")
        require(energy[0] > 0,
                "rigorous nonzero projected finite-support witness")

        # The paper's elementary bound is
        # E <= (1/2) (pi/2)^(2n) for H0=3, Omega=1/12.
        pi_over_two = iscale(Fraction(1, 2), enclosed_pi)
        power = interval(1)
        for _ in range(2 * order):
            power = imul(power, pi_over_two)
        theorem_bound = iscale(Fraction(1, 2), power)
        require(energy[1] <= theorem_bound[0],
                "rigorous thin-sector energy bound")
        witness_ratios.append({
            "order": order,
            "norm_squared": norm_squared,
            "energy_upper_numerator": str(energy[1].numerator),
            "energy_upper_denominator": str(energy[1].denominator),
        })

    # Rational ledger for the comb measure and trace.
    for h0 in [1, 2, 3, 4]:
        omega_width = Fraction(1, 4 * h0)
        measure = 2 * h0 * omega_width
        require(measure == Fraction(1, 2),
                "comb band rational measure")
        for window_size in [1, 2, 5, 13, 29]:
            for dimension in [1, 3]:
                trace = 2 * dimension * h0 * window_size * omega_width
                require(trace == Fraction(dimension * window_size, 2),
                        "comb trace rational ledger")

    return {
        "checks": CHECKS - start,
        "arithmetic": "Fraction interval arithmetic",
        "comb_parameters": {"H0": 3, "Omega": "1/12"},
        "certified_consecutive_gram_size": 12,
        "ldl_pivot_checks": pivot_checks,
        "difference_witness_orders": 12,
        "pi_interval_width": {
            "numerator": str(
                (enclosed_pi[1] - enclosed_pi[0]).numerator
            ),
            "denominator": str(
                (enclosed_pi[1] - enclosed_pi[0]).denominator
            ),
        },
        "witnesses": witness_ratios,
    }


def check_finite_rank_boundary() -> dict:
    start = CHECKS
    n = 7
    modulus = 29
    generator = primitive_root(modulus)
    omega = pow(generator, (modulus - 1) // n, modulus)
    require(pow(omega, n, modulus) == 1, "seventh root closes")
    for exponent in range(1, n):
        require(pow(omega, exponent, modulus) != 1,
                "seventh root has exact order")
    band = [-2, -1, 0, 1, 2]
    full_rank_subsets = 0
    for size in range(1, 6):
        for support in itertools.combinations(range(n), size):
            matrix = [
                [pow(omega, (frequency * j) % n, modulus)
                 for j in support]
                for frequency in band
            ]
            require(matrix_rank_mod(matrix, modulus) == size,
                    "finite partial Fourier injectivity")
            full_rank_subsets += 1
    require(full_rank_subsets == 119,
            "finite injective-support count")

    null_witnesses = 0
    for support in itertools.combinations(range(n), 6):
        matrix = [
            [pow(omega, (frequency * j) % n, modulus)
             for j in support]
            for frequency in band
        ]
        require(matrix_rank_mod(matrix, modulus) == 5,
                "finite cyclic dimension boundary rank")
        vector = null_vector_mod(matrix, modulus)
        require(any(vector), "finite cyclic null vector is nonzero")
        for row in matrix:
            require(sum(x * y for x, y in zip(row, vector)) % modulus == 0,
                    "finite cyclic null vector equation")
        null_witnesses += 1
    require(null_witnesses == 7, "six-point null-witness count")
    return {
        "checks": CHECKS - start,
        "arithmetic": "F_29 on Z/7Z",
        "band_size": len(band),
        "full_rank_supports": full_rank_subsets,
        "six_point_null_witnesses": null_witnesses,
        "boundary": (
            "Finite cyclic dimension boundary only; the global sinc "
            "projector remains injective on every finite support."
        ),
    }


def check_failure_witnesses() -> dict:
    start = CHECKS
    modulus = 29
    n = 7
    generator = primitive_root(modulus)
    omega = pow(generator, (modulus - 1) // n, modulus)

    # Selecting one signed projective layer is not an operation on the
    # whole coefficient.
    layer = [(3 * j * j + 5 * j + 1) % modulus for j in range(n)]
    opposite = [(-value) % modulus for value in layer]
    for j in range(n):
        require((layer[j] + opposite[j]) % modulus == 0,
                "signed layers cancel only after whole reassembly")
    require(any(layer), "one cancelled layer is nonzero")

    # Projection and multiplication do not commute.
    z = [pow(omega, j, modulus) for j in range(n)]
    multiplier = [pow(omega, -j % n, modulus) for j in range(n)]
    zero_band = {0}
    projected_z = mod_project(z, zero_band, omega, modulus)
    product_after_projection = [
        multiplier[j] * projected_z[j] % modulus for j in range(n)
    ]
    product_before_projection = mod_project(
        [multiplier[j] * z[j] % modulus for j in range(n)],
        zero_band,
        omega,
        modulus,
    )
    for value in product_after_projection:
        require(value == 0, "multiplier times projected high mode is zero")
    for value in product_before_projection:
        require(value == 1, "projected product recovers constant mode")

    # A tapered finite window has full cyclic spectrum.
    tapered = [1, 3, 3, 1, 0, 0, 0]
    tapered_transform = mod_dft(tapered, omega, modulus)
    for q in range(n):
        expected = pow(
            (1 + pow(omega, -q % n, modulus)) % modulus,
            3,
            modulus,
        )
        require(tapered_transform[q] == expected,
                "binomial-window transform")
        require(tapered_transform[q] != 0,
                "finite window destroys exact band support")

    # Residual aggregation before projection loses Hilbert geometry.
    residual_one = [1, -2, 3, -4]
    residual_two = [-value for value in residual_one]
    for left, right in zip(residual_one, residual_two):
        require(left + right == 0,
                "residual aggregation cancellation")
    separate_energy = sum(value * value for value in residual_one)
    separate_energy += sum(value * value for value in residual_two)
    require(separate_energy == 60,
            "separate residual Hilbert energy survives")

    # One orbit mode maps to different shift frequencies for different
    # determinant slopes.  A post-synthesis shift filter is not the
    # orbit projector.
    orbit_mode = [pow(omega, j, modulus) for j in range(n)]
    orbit_transform = mod_dft(orbit_mode, omega, modulus)
    supports = []
    for slope in [1, 2]:
        kernel = [
            orbit_transform[(-slope * k) % n] for k in range(n)
        ]
        supports.append({k for k, value in enumerate(kernel) if value})
    require(supports[0] == {6}, "slope-one shift image")
    require(supports[1] == {3}, "slope-two shift image")
    require(supports[0] != supports[1],
            "orbit projection is not one shift-frequency deletion")

    # The fixed residue selector creates all progression branches.
    modulus_60 = 601
    generator_60 = primitive_root(modulus_60)
    omega_60 = pow(generator_60, 10, modulus_60)
    selector = [int(j % 3 == 1) for j in range(60)]
    selector_transform = mod_dft(selector, omega_60, modulus_60)
    constant_transform = mod_dft([1] * 60, omega_60, modulus_60)
    for frequency in [20, 40]:
        require(selector_transform[frequency] != 0,
                "progression branch is present")
        require(constant_transform[frequency] == 0,
                "omitting progression loses a branch")

    # A pure high profile can make the entire full packet a tail.
    high_frequency = 10
    high_profile = [
        pow(omega_60, high_frequency * j % 60, modulus_60)
        for j in range(60)
    ]
    low_profile = mod_project(
        high_profile, {59, 0, 1}, omega_60, modulus_60
    )
    for value in low_profile:
        require(value == 0, "pure high profile has zero declared low part")
    require(any(high_profile), "pure high profile full tail is nonzero")

    # Orthogonal projection is not coordinatewise domination.
    delta = [gaussian(1), gaussian(0), gaussian(0), gaussian(0)]
    constant_projection = gaussian_project(delta, {0})
    for j in [1, 2, 3]:
        require(constant_projection[j] != gaussian(0),
                "projection spills outside the original coordinate")
        require(gnorm2(delta[j]) == 0,
                "original off-coordinate atom vanishes")
    require(vector_norm2(constant_projection) <= vector_norm2(delta),
            "global contraction survives coordinate spill")

    # The projective mass-square reassembly loss is sharp.
    base = [gaussian(1, 2), gaussian(-2, 3)]
    coefficients = [1, 2, 5, 7]
    mass = sum(coefficients)
    coherent = [gscale(mass, value) for value in base]
    require(
        vector_norm2(coherent) == mass * mass * vector_norm2(base),
        "aligned tails attain projective mass-square loss",
    )

    return {
        "checks": CHECKS - start,
        "witnesses": [
            "signed_layer_selection",
            "projection_multiplier_noncommutation",
            "finite_window_full_spectrum",
            "residual_preaggregation",
            "orbit_vs_shift_projection",
            "progression_branch_omission",
            "uncontrolled_high_profile_tail",
            "coordinatewise_projection_spill",
            "projective_mass_square_sharpness",
        ],
    }


def check_source_constraints() -> dict:
    start = CHECKS
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    float_nodes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    assert_nodes = [
        node for node in ast.walk(tree) if isinstance(node, ast.Assert)
    ]
    true_divisions = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    require(not float_nodes, "certificate source has no float literal")
    require(not assert_nodes, "certificate source has no assert statement")
    require(not true_divisions, "certificate source has no true division")
    require(not any(name == "random" or name.startswith("random.")
                    for name in imports),
            "certificate source has no random import")
    return {"checks": CHECKS - start}


def main() -> None:
    results = {
        "cyclic_actual_transfer": check_cyclic_actual_transfer(),
        "gaussian_hilbert_identities": check_gaussian_hilbert_identities(),
        "sinc_comb_and_mass_frontier":
            check_sinc_comb_and_mass_frontier(),
        "finite_rank_boundary": check_finite_rank_boundary(),
        "failure_witnesses": check_failure_witnesses(),
        "source_constraints": check_source_constraints(),
    }
    claims = {
        "finite_cyclic_model_is_only_an_analogue": True,
        "literal_fiberwise_output_residual_projection": True,
        "literal_residual_label_s_equals_d_times_r": True,
        "full_signed_actual_mask_reassembly": True,
        "canonical_whole_actual_coefficient_lowpass": True,
        "whole_profile_low_plus_tail_identity": True,
        "finite_difference_fourier_identity": True,
        "progression_comb_convolution_support": True,
        "determinant_orbit_to_shift_transfer": True,
        "whole_finite_actual_packet_gap": True,
        "orthogonal_projection_contraction": True,
        "residual_unitary_commutation": True,
        "rigorous_finite_sinc_comb_gram_positivity": True,
        "finite_support_thin_sector_witness": True,
        "finite_cyclic_rank_boundary": True,
        "uniform_low_sector_mass_lower_bound": False,
        "high_frequency_complement_controlled": False,
        "asymptotic_continuous_fourier_tail_certified": False,
        "fixed_shift_atomic_bessel_bound": False,
        "mobius_cancellation": False,
        "parity_barrier_broken": False,
        "hardy_littlewood_prime_pair_asymptotic": False,
        "twin_prime_conjecture": False,
    }
    source = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    payload = {
        "arithmetic": (
            "finite fields, Gaussian rationals, and Fraction interval "
            "arithmetic; no floats or randomness"
        ),
        "certificate_version": 1,
        "check_total": CHECKS,
        "claims": claims,
        "normalized_source_sha256": sha256(source).hexdigest(),
        "paper": "TPC-47",
        "results": results,
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    payload["certificate_digest"] = sha256(canonical).hexdigest()
    output = Path(__file__).with_name("tpc47_certificate.json")
    output_bytes = (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True)
        + "\n"
    ).encode("utf-8")
    output.write_bytes(output_bytes)
    print(
        "TPC-47 exact certificate:"
        f" {CHECKS} checks;"
        f" digest {payload['certificate_digest']};"
        f" source_sha256 {payload['normalized_source_sha256']};"
        f" json_sha256 {sha256(output_bytes).hexdigest()};"
        f" wrote {output.name}"
    )


if __name__ == "__main__":
    main()
