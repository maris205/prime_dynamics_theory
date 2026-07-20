#!/usr/bin/env python3
"""Exact finite certificate for TPC-45.

The script uses only the Python standard library and exact integer/rational
arithmetic.  It checks the algebraic band deletion, grouped-energy identity,
affine high-prime normal form, low-averaged Gram projection, determinant
ladder, and all rational exponent ledgers.  It does not test an asymptotic
Möbius-cancellation or prime-pair statement.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "tpc45_certificate.json"

Gaussian = tuple[int, int]
Entry = tuple[int, Gaussian]
Packet = list[list[Entry]]


class Certificate:
    def __init__(self) -> None:
        self.checks = 0
        self.families: dict[str, int] = defaultdict(int)

    def check(self, condition: bool, family: str) -> None:
        self.checks += 1
        self.families[family] += 1
        if not condition:
            raise RuntimeError(f"certificate failure in {family}")


def factorization(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorization requires n >= 1")
    result: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        result[n] = result.get(n, 0) + 1
    return result


def is_prime(n: int) -> bool:
    return n > 1 and factorization(n) == {n: 1}


def is_squarefree(n: int) -> bool:
    return all(exponent == 1 for exponent in factorization(n).values())


def mobius(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def primes_in_interval(lower: int, upper: int) -> list[int]:
    return [p for p in range(max(2, lower), upper + 1) if is_prime(p)]


def prime_support(packet: Packet) -> list[int]:
    support: set[int] = set()
    for coordinate in packet:
        for label, _coefficient in coordinate:
            support.update(factorization(label))
    return sorted(support)


def environments(primes: list[int]):
    for mask in range(1 << len(primes)):
        yield {
            p: (-1 if mask & (1 << index) else 1)
            for index, p in enumerate(primes)
        }


def character(label: int, epsilon: dict[int, int]) -> int:
    value = 1
    for p in factorization(label):
        value *= epsilon[p]
    return value


def gadd(a: Gaussian, b: Gaussian) -> Gaussian:
    return a[0] + b[0], a[1] + b[1]


def gscale(scale: int, value: Gaussian) -> Gaussian:
    return scale * value[0], scale * value[1]


def gnorm2(value: Gaussian) -> int:
    return value[0] * value[0] + value[1] * value[1]


def ginner_real(a: Gaussian, b: Gaussian) -> int:
    return a[0] * b[0] + a[1] * b[1]


def energy(packet: Packet, epsilon: dict[int, int]) -> int:
    total = 0
    for coordinate in packet:
        value = (0, 0)
        for label, coefficient in coordinate:
            value = gadd(value, gscale(character(label, epsilon), coefficient))
        total += gnorm2(value)
    return total


def diagonal(packet: Packet) -> int:
    return sum(
        gnorm2(coefficient)
        for coordinate in packet
        for _label, coefficient in coordinate
    )


def deterministic_coefficient(row: int, coordinate: int) -> Gaussian:
    real = ((7 * row + 3 * coordinate + 2) % 11) - 5
    imag = ((5 * row + 2 * coordinate + 1) % 9) - 4
    return (real, imag) if (real, imag) != (0, 0) else (1, -1)


def actual_band_fixture() -> tuple[Packet, list[int], dict[str, int]]:
    """Build squarefree actual labels u=d(ell*d*j+1)."""
    rows = [(11, 6), (13, 7), (17, 10), (19, 11)]
    orbit = [29, 30, 31]
    active: list[tuple[int, int, int, int]] = []
    packet: Packet = []
    for coordinate, j in enumerate(orbit):
        entries: list[Entry] = []
        for row, (ell, d) in enumerate(rows):
            n = ell * d * j + 1
            if not is_squarefree(n):
                continue
            label = d * n
            assert gcd(d, n) == 1 and is_squarefree(label)
            entries.append((label, deterministic_coefficient(row, coordinate)))
            active.append((ell, d, j, n))
        packet.append(entries)
    n_minus = min(item[3] for item in active)
    n_plus = max(item[3] for item in active)
    ell_plus = max(item[0] for item in active)
    band = primes_in_interval(isqrt(n_plus) + 1, n_minus // ell_plus)
    metadata = {
        "n_minus": n_minus,
        "n_plus": n_plus,
        "ell_plus": ell_plus,
        "band_lower": isqrt(n_plus) + 1,
        "band_upper": n_minus // ell_plus,
        "active_atoms": len(active),
    }
    return packet, band, metadata


def delete_band(packet: Packet, band: list[int]):
    grouped_packet: Packet = []
    fiber_sizes: list[int] = []
    atom_map: list[list[tuple[int, int, int]]] = []
    for coordinate in packet:
        grouped: dict[int, Gaussian] = defaultdict(lambda: (0, 0))
        counts: dict[int, int] = defaultdict(int)
        mapped: list[tuple[int, int, int]] = []
        for label, coefficient in coordinate:
            hits = [p for p in band if label % p == 0]
            if len(hits) > 1:
                raise RuntimeError("toy label contains two band primes")
            if hits:
                transformed = label // hits[0]
                sign = -1
            else:
                transformed = label
                sign = 1
            grouped[transformed] = gadd(
                grouped[transformed], gscale(sign, coefficient)
            )
            counts[transformed] += 1
            mapped.append((label, transformed, sign))
        grouped_packet.append(sorted(grouped.items()))
        fiber_sizes.extend(counts.values())
        atom_map.append(mapped)
    return grouped_packet, max(fiber_sizes, default=0), atom_map


def check_actual_band(cert: Certificate) -> dict[str, int]:
    packet, band, metadata = actual_band_fixture()
    cert.check(bool(band), "band_nonempty")
    cert.check(len(band) >= 2, "band_nonempty")
    support = prime_support(packet)
    remaining = [p for p in support if p not in band]
    grouped, rho, atom_map = delete_band(packet, band)

    for coordinate in atom_map:
        for original, transformed, sign in coordinate:
            hits = [p for p in band if original % p == 0]
            cert.check(len(hits) <= 1, "unique_band_prime")
            if hits:
                cert.check(original == hits[0] * transformed, "band_deletion")
                cert.check(mobius(original) == -mobius(transformed), "physical_sign")
                cert.check(sign == -1, "physical_sign")
            else:
                cert.check(original == transformed and sign == 1, "band_deletion")

    for epsilon_remaining in environments(remaining):
        original_environment = dict(epsilon_remaining)
        original_environment.update({p: -1 for p in band})
        cert.check(
            energy(packet, original_environment)
            == energy(grouped, epsilon_remaining),
            "grouped_energy_identity",
        )

    cert.check(diagonal(grouped) <= rho * diagonal(packet), "fiber_cauchy")
    return {
        **metadata,
        "band_prime_count": len(band),
        "band_hit_count": sum(
            original != transformed
            for coordinate in atom_map
            for original, transformed, _sign in coordinate
        ),
        "max_fiber": rho,
        "atomic_diagonal": diagonal(packet),
        "grouped_diagonal": diagonal(grouped),
    }


def high_split(label: int, y: int) -> tuple[int, int]:
    high = [p for p in factorization(label) if p > y]
    if len(high) > 1:
        raise RuntimeError("label has more than one high prime")
    return (1, label) if not high else (high[0], label // high[0])


def affine_fixture() -> Packet:
    return [
        [(30, (2, 1)), (202, (1, -2)), (309, (3, 1)), (535, (-2, 2))],
        [(42, (-1, 3)), (505, (2, 2)), (721, (1, -3))],
    ]


def check_affine_form(cert: Certificate) -> dict[str, int]:
    packet = affine_fixture()
    y = 50
    high_primes = sorted(
        {high_split(label, y)[0] for coordinate in packet for label, _ in coordinate}
        - {1}
    )
    low_primes = sorted(
        {p for coordinate in packet for label, _ in coordinate for p in factorization(label) if p <= y}
    )

    v0: list[Gaussian] = []
    vectors: dict[int, list[Gaussian]] = {
        p: [(0, 0) for _ in packet] for p in high_primes
    }
    for i, coordinate in enumerate(packet):
        base = (0, 0)
        seen: set[int] = set()
        for label, coefficient in coordinate:
            p, residual = high_split(label, y)
            if p == 1:
                base = gadd(base, gscale(mobius(label), coefficient))
            else:
                cert.check(p not in seen, "affine_matching")
                seen.add(p)
                vectors[p][i] = gadd(
                    vectors[p][i], gscale(mobius(residual), coefficient)
                )
        v0.append(base)

    for high_environment in environments(high_primes):
        physical_low = {p: -1 for p in low_primes}
        full_environment = {**physical_low, **high_environment}
        affine_energy = 0
        for i in range(len(packet)):
            value = v0[i]
            for p in high_primes:
                value = gadd(value, gscale(high_environment[p], vectors[p][i]))
            affine_energy += gnorm2(value)
        cert.check(
            affine_energy == energy(packet, full_environment),
            "affine_normal_form",
        )

    return {
        "affine_threshold": y,
        "affine_high_primes": len(high_primes),
        "affine_low_primes": len(low_primes),
    }


def rough_gram_fixture() -> Packet:
    return [
        [(30, (1, 2)), (202, (2, -1)), (206, (-3, 1)),
         (321, (2, 2)), (327, (-1, -2))],
        [(42, (3, 1)), (505, (-2, 1)), (515, (1, 3)),
         (749, (2, -3)), (763, (-1, 1))],
    ]


def check_rough_gram(cert: Certificate) -> dict[str, int]:
    packet = rough_gram_fixture()
    y = 50
    support = prime_support(packet)
    low_primes = [p for p in support if p <= y]
    high_primes = [p for p in support if p > y]

    lifted: dict[int, dict[tuple[int, int], Gaussian]] = defaultdict(dict)
    high_diagonal = 0
    for i, coordinate in enumerate(packet):
        for label, coefficient in coordinate:
            p, residual = high_split(label, y)
            if p == 1:
                continue
            key = (i, residual)
            cert.check(key not in lifted[p], "lifted_matching")
            lifted[p][key] = coefficient
            high_diagonal += gnorm2(coefficient)

    total_diagonal = diagonal(packet)
    cert.check(high_diagonal <= total_diagonal, "high_diagonal")
    for high_environment in environments(high_primes):
        average_numerator = 0
        low_count = 0
        for low_environment in environments(low_primes):
            average_numerator += energy(
                packet, {**low_environment, **high_environment}
            )
            low_count += 1
        cert.check(average_numerator % low_count == 0, "rough_average_integral")
        averaged = average_numerator // low_count

        gram = total_diagonal
        for index, p in enumerate(high_primes):
            for q in high_primes[index + 1:]:
                inner = 0
                for key in set(lifted[p]).intersection(lifted[q]):
                    inner += ginner_real(lifted[p][key], lifted[q][key])
                gram += 2 * high_environment[p] * high_environment[q] * inner
        cert.check(averaged == gram, "rough_gram_projection")

    physical_sum_norm = 0
    keys = {
        key for vector in lifted.values() for key in vector
    }
    for key in keys:
        value = (0, 0)
        for p in high_primes:
            value = gadd(value, lifted[p].get(key, (0, 0)))
        physical_sum_norm += gnorm2(value)
    physical_formula = total_diagonal - high_diagonal + physical_sum_norm
    physical_environment = {p: -1 for p in high_primes}
    average_numerator = sum(
        energy(packet, {**low, **physical_environment})
        for low in environments(low_primes)
    )
    cert.check(
        average_numerator == (1 << len(low_primes)) * physical_formula,
        "physical_rough_synthesis",
    )
    return {
        "rough_threshold": y,
        "rough_high_primes": len(high_primes),
        "rough_low_primes": len(low_primes),
        "rough_atomic_diagonal": total_diagonal,
        "rough_high_diagonal": high_diagonal,
        "rough_physical_synthesis": physical_sum_norm,
    }


def check_determinant_ladder(cert: Certificate) -> dict[str, int]:
    h = 1
    j = 20
    d = 5
    r = 3
    ladder = [(11, 367), (29, 967)]
    g = gcd(r, d * j)
    cert.check(g == 1 and h % g == 0, "ladder_solubility")
    for ell, p in ladder:
        n = ell * d * j + h
        cert.check(is_prime(ell) and is_prime(p), "ladder_primes")
        cert.check(n == p * r, "fixed_determinant")
        cert.check(r * p - d * j * ell == h, "fixed_determinant")
        residual = d * r
        cert.check(mobius(d * n) == -mobius(residual), "ladder_coherence")

    ell_step = r // g
    prime_step = d * j // g
    delta_t = (ladder[1][0] - ladder[0][0]) // ell_step
    cert.check(
        ladder[1][0] == ladder[0][0] + ell_step * delta_t,
        "ladder_parameterization",
    )
    cert.check(
        ladder[1][1] == ladder[0][1] + prime_step * delta_t,
        "ladder_parameterization",
    )
    determinant = prime_step * ladder[0][0] - ell_step * ladder[0][1]
    cert.check(determinant == -h // g, "ladder_determinant")

    coherent = [
        (11, 5, 3, 367),
        (11, 15, 1, 3301),
        (17, 15, 1, 5101),
        (19, 15, 1, 5701),
        (29, 5, 3, 967),
    ]
    signs: set[int] = set()
    for ell, divisor, cofactor, p in coherent:
        cert.check(is_prime(ell) and is_prime(p), "coherent_fiber_primes")
        cert.check(
            cofactor * p - divisor * j * ell == h,
            "coherent_fiber_equation",
        )
        cert.check(divisor * cofactor == 15, "coherent_residual")
        signs.add(mobius(p * divisor * cofactor))
    cert.check(signs == {-mobius(15)}, "coherent_physical_sign")
    return {
        "ladder_length": len(ladder),
        "ladder_parameter_step": delta_t,
        "coherent_fiber_size": len(coherent),
        "coherent_residual": 15,
    }


def check_operator_norm(cert: Certificate) -> dict[str, int]:
    fibers = [1, 3, 5, 2]
    rho = max(fibers)
    for size in fibers:
        coefficients = [(index + 1, 2 - index) for index in range(size)]
        summed = (sum(z[0] for z in coefficients), sum(z[1] for z in coefficients))
        input_norm = sum(gnorm2(z) for z in coefficients)
        cert.check(gnorm2(summed) <= size * input_norm, "fiber_operator_upper")
    equality_vector = [(1, -2)] * rho
    output = (rho, -2 * rho)
    cert.check(
        gnorm2(output) == rho * sum(gnorm2(z) for z in equality_vector),
        "fiber_operator_sharp",
    )
    return {"abstract_max_fiber": rho, "squared_operator_norm": rho}


def check_exponents(cert: Certificate) -> dict[str, str]:
    lambda_q = Fraction(267, 400)
    lambda_j = Fraction(133, 400)
    lambda_d = Fraction(10049, 52500)
    lambda_l = lambda_q - lambda_d
    lambda_0 = 1 + lambda_d
    lambda_1 = Fraction(1, 2) + lambda_d
    budget = Fraction(1, 400)
    cert.check(lambda_q + lambda_j == 1, "exponent_scale")
    cert.check(lambda_l == Fraction(99979, 210000), "exponent_scale")
    cert.check(1 - lambda_l == Fraction(110021, 210000), "band_endpoint")
    cert.check(lambda_0 == Fraction(62549, 52500), "label_exponent")
    cert.check(lambda_1 == Fraction(36299, 52500), "label_exponent")

    old_cost = lambda_0 / 501
    old_gap = budget - old_cost
    cert.check(old_gap == Fraction(12829, 105210000), "old_cutoff_gap")

    legacy_extension = Fraction(1, 10000)
    legacy_tradeoff_gap = budget - old_cost - legacy_extension
    cert.check(
        legacy_tradeoff_gap == Fraction(577, 26302500),
        "tradeoff_gap",
    )

    wider_cost = Fraction(1, 1000) + lambda_0 / 1001
    wider_gap = budget - wider_cost
    cert.check(wider_gap == Fraction(65119, 210210000), "tradeoff_gap")

    improved_cost = lambda_1 * Fraction(3, 1003)
    improved_gap = budget - improved_cost
    cert.check(
        improved_cost == Fraction(36299, 17552500),
        "residual_cutoff",
    )
    cert.check(
        improved_gap == Fraction(30329, 70210000),
        "residual_cutoff",
    )
    a_star = Fraction(145196, 144671)
    cert.check(
        a_star == 1 / (1 - 1 / (400 * lambda_1)),
        "residual_cutoff",
    )
    return {
        "lambda_Q": str(lambda_q),
        "lambda_J": str(lambda_j),
        "lambda_D": str(lambda_d),
        "lambda_L": str(lambda_l),
        "lambda_original_label": str(lambda_0),
        "lambda_residual_label": str(lambda_1),
        "old_cutoff_gap": str(old_gap),
        "legacy_band_extension": str(legacy_extension),
        "legacy_tradeoff_gap": str(legacy_tradeoff_gap),
        "wider_tradeoff_gap": str(wider_gap),
        "improved_residual_gap": str(improved_gap),
        "improved_A_star": str(a_star),
    }


def main() -> None:
    cert = Certificate()
    report = {
        "schema": "tpc45-exact-certificate-v1",
        "scope": (
            "finite exact algebra and rational exponent checks only; "
            "no asymptotic Mobius cancellation or prime-pair claim"
        ),
        "actual_band": check_actual_band(cert),
        "affine_form": check_affine_form(cert),
        "rough_gram": check_rough_gram(cert),
        "determinant_ladder": check_determinant_ladder(cert),
        "operator_norm": check_operator_norm(cert),
        "exponents": check_exponents(cert),
    }
    report["checks"] = cert.checks
    report["families"] = dict(sorted(cert.families.items()))
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["payload_sha256"] = sha256(canonical.encode("utf-8")).hexdigest()
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"TPC-45 certificate: {cert.checks} exact checks passed")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
