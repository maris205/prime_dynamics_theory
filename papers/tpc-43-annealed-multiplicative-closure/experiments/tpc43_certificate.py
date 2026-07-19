#!/usr/bin/env python3
"""Exact finite certificate for TPC-43.

The certificate checks only finite algebra and combinatorics.  It uses no
floating-point arithmetic and performs no random sampling.  In particular,
it does not test a Mobius-cancellation asymptotic or a prime-pair statement.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE.joinpath("tpc43_certificate.json")

Gaussian = tuple[int, int]
Row = tuple[int, int]


class Certificate:
    def __init__(self) -> None:
        self.checks = 0
        self.stats: dict[str, int] = defaultdict(int)

    def check(self, condition: bool, family: str) -> None:
        self.checks += 1
        self.stats[family] += 1
        if not condition:
            raise RuntimeError(f"certificate failure in {family}")


def prime_table(limit: int) -> list[bool]:
    table = [True] * (limit + 1)
    table[0] = False
    table[1] = False
    for p in range(2, isqrt(limit) + 1):
        if table[p]:
            for n in range(p * p, limit + 1, p):
                table[n] = False
    return table


def factorization(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorization requires a positive integer")
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def is_squarefree(n: int) -> bool:
    return all(e == 1 for e in factorization(n).values())


def mobius(n: int) -> int:
    factors = factorization(n)
    if any(e > 1 for e in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def divisors(n: int) -> list[int]:
    values = [1]
    for p, e in factorization(n).items():
        old = list(values)
        power = 1
        for _ in range(e):
            power *= p
            values.extend(d * power for d in old)
    return sorted(values)


def tau(n: int) -> int:
    value = 1
    for e in factorization(n).values():
        value *= e + 1
    return value


def squarefree_kernel(a: int, b: int) -> int:
    g = gcd(a, b)
    return a * b // (g * g)


def prime_support(values: list[int]) -> list[int]:
    support: set[int] = set()
    for value in values:
        support.update(factorization(value))
    return sorted(support)


def environments(primes: list[int]):
    for mask in range(1 << len(primes)):
        yield {
            p: (-1 if mask & (1 << index) else 1)
            for index, p in enumerate(primes)
        }


def character(n: int, epsilon: dict[int, int]) -> int:
    value = 1
    for p in factorization(n):
        value *= epsilon[p]
    return value


def random_multiplicative(n: int, epsilon: dict[int, int]) -> int:
    if not is_squarefree(n):
        return 0
    return character(n, epsilon)


def gadd(z: Gaussian, w: Gaussian) -> Gaussian:
    return z[0] + w[0], z[1] + w[1]


def gconj(z: Gaussian) -> Gaussian:
    return z[0], -z[1]


def gmul(z: Gaussian, w: Gaussian) -> Gaussian:
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def gscale(a: int, z: Gaussian) -> Gaussian:
    return a * z[0], a * z[1]


def gnorm2(z: Gaussian) -> int:
    return z[0] * z[0] + z[1] * z[1]


def build_rows(h: int, dmax: int, ellmax: int) -> list[Row]:
    prime = prime_table(ellmax)
    used_products: set[int] = set()
    rows: list[Row] = []
    for d in range(1, dmax + 1):
        if not is_squarefree(d) or gcd(d, abs(h)) != 1:
            continue
        for ell in range(2, ellmax + 1):
            if not prime[ell]:
                continue
            product = ell * d
            if product in used_products:
                continue
            used_products.add(product)
            rows.append((ell, d))
    return rows


def check_exponent_ledger(cert: Certificate) -> None:
    q_exp = Fraction(267, 400)
    j_exp = Fraction(133, 400)
    d_exp = Fraction(10049, 52500)
    k_exp = Fraction(1, 400)
    cert.check(q_exp + j_exp == 1, "endpoint_exponent_ledger")
    cert.check(q_exp - 2 * j_exp == k_exp, "endpoint_exponent_ledger")
    cert.check(d_exp < j_exp, "endpoint_exponent_ledger")
    cert.check(k_exp > 0, "endpoint_exponent_ledger")


def check_multiplicative_identity(cert: Certificate) -> None:
    squarefree = [n for n in range(1, 61) if is_squarefree(n)]
    for d in squarefree:
        for n in squarefree:
            s = squarefree_kernel(d, n)
            cert.check(is_squarefree(s), "squarefree_kernel")
            primes = prime_support([d, n])
            for epsilon in environments(primes):
                left = random_multiplicative(d, epsilon) * random_multiplicative(n, epsilon)
                cert.check(left == character(s, epsilon), "kernel_character_identity")
    primes = prime_support(list(range(2, 121)))
    all_minus = {p: -1 for p in primes}
    for n in range(1, 121):
        cert.check(
            random_multiplicative(n, all_minus) == mobius(n),
            "all_minus_is_mobius",
        )


def check_product_fibers(cert: Certificate) -> None:
    h = 1
    modulus = 31
    rows = build_rows(h, 24, 43)
    for j in range(10, 17):
        for k in range(-2, 3):
            c = h + k * modulus
            cert.check(c != 0, "nonzero_alias_intercept")
            fibers: dict[int, list[tuple[int, int, int, int]]] = defaultdict(list)
            for ell, d in rows:
                n = ell * d * j + c
                if n < 1 or not is_squarefree(n):
                    continue
                g = gcd(d, n)
                s = squarefree_kernel(d, n)
                fibers[s].append((ell, d, n, g))
                cert.check(g == gcd(d, abs(c)), "gcd_is_intercept")
                cert.check(gcd(s, g) == 1, "kernel_gcd_separation")
                cert.check(d * n == s * g * g, "fiber_product_identity")
                recovered_n = s * g * g // d
                recovered_ell = (recovered_n - c) // (d * j)
                cert.check(recovered_n == n, "divisor_reconstruction")
                cert.check(recovered_ell == ell, "divisor_reconstruction")
            for s, fiber in fibers.items():
                bound = sum(tau(s * g * g) for g in divisors(abs(c)))
                cert.check(len(fiber) <= bound, "fiber_multiplicity_bound")
                keys = {(g, d) for _ell, d, _n, g in fiber}
                cert.check(len(keys) == len(fiber), "reconstruction_uniqueness")


def zero_alias_rows(h: int, j: int, dmax: int, ellmax: int):
    rows = []
    for ell, d in build_rows(h, dmax, ellmax):
        n = ell * d * j + h
        if n > 0 and is_squarefree(n):
            rows.append((ell, d, n, d * n))
    return rows


def check_zero_alias_injection(cert: Certificate) -> None:
    for h in (1, 5, -5):
        dmax = 16
        for j in range(abs(h) * dmax + 1, abs(h) * dmax + 7):
            rows = zero_alias_rows(h, j, dmax, 47)
            labels = [u for _ell, _d, _n, u in rows]
            cert.check(len(labels) == len(set(labels)), "zero_alias_injectivity")
            for _ell, d, n, u in rows:
                cert.check(gcd(d, n) == 1, "zero_alias_coprimality")
                cert.check(is_squarefree(u), "zero_alias_squarefree_label")


def toy_energy_packet() -> tuple[list[tuple[int, int, int, int]], list[list[Gaussian]]]:
    rows = zero_alias_rows(1, 11, 8, 23)[:6]
    if len(rows) != 6:
        raise RuntimeError("toy packet construction changed")
    coefficients: list[list[Gaussian]] = []
    for coordinate in range(4):
        one_coordinate: list[Gaussian] = []
        for index in range(len(rows)):
            one_coordinate.append(
                (
                    ((3 * index + 2 * coordinate) % 7) - 3,
                    ((2 * index - coordinate) % 5) - 2,
                )
            )
        coefficients.append(one_coordinate)
    return rows, coefficients


def energy_at(
    rows: list[tuple[int, int, int, int]],
    coefficients: list[list[Gaussian]],
    epsilon: dict[int, int],
) -> int:
    energy = 0
    for coordinate in coefficients:
        value = (0, 0)
        for coeff, (_ell, _d, _n, u) in zip(coordinate, rows):
            value = gadd(value, gscale(character(u, epsilon), coeff))
        energy += gnorm2(value)
    return energy


def grouped_spectrum(
    rows: list[tuple[int, int, int, int]],
    coefficients: list[list[Gaussian]],
) -> tuple[int, dict[int, int]]:
    diagonal = 0
    grouped: dict[int, Gaussian] = defaultdict(lambda: (0, 0))
    for coordinate in coefficients:
        for alpha, coeff_a in enumerate(coordinate):
            diagonal += gnorm2(coeff_a)
            for beta, coeff_b in enumerate(coordinate):
                if alpha == beta:
                    continue
                u_a = rows[alpha][3]
                u_b = rows[beta][3]
                kappa = squarefree_kernel(u_a, u_b)
                contribution = gmul(coeff_a, gconj(coeff_b))
                grouped[kappa] = gadd(grouped[kappa], contribution)
    real_grouped: dict[int, int] = {}
    for kappa, value in grouped.items():
        if value[1] != 0:
            raise RuntimeError("grouped Walsh coefficient is not real")
        real_grouped[kappa] = value[0]
    return diagonal, real_grouped


def check_energy_and_walsh_corner(cert: Certificate) -> None:
    rows, coefficients = toy_energy_packet()
    labels = [row[3] for row in rows]
    cert.check(len(labels) == len(set(labels)), "toy_label_injection")
    primes = prime_support(labels)
    diagonal, grouped = grouped_spectrum(rows, coefficients)
    total_energy = 0
    centered_square_total = 0
    environment_count = 0
    for epsilon in environments(primes):
        environment_count += 1
        energy = energy_at(rows, coefficients, epsilon)
        spectral = diagonal + sum(
            value * character(kappa, epsilon)
            for kappa, value in grouped.items()
        )
        cert.check(energy == spectral, "exact_walsh_energy_expansion")
        total_energy += energy
        centered_square_total += (energy - diagonal) * (energy - diagonal)
    cert.check(
        total_energy == environment_count * diagonal,
        "exact_annealed_diagonal",
    )
    cert.check(
        centered_square_total
        == environment_count * sum(value * value for value in grouped.values()),
        "exact_walsh_parseval",
    )

    for alpha, (_ell_a, d_a, n_a, u_a) in enumerate(rows):
        for beta, (_ell_b, d_b, n_b, u_b) in enumerate(rows):
            kappa = squarefree_kernel(u_a, u_b)
            physical_four = mobius(d_a) * mobius(n_a) * mobius(d_b) * mobius(n_b)
            cert.check(physical_four == mobius(kappa), "literal_four_to_one")

    for z in (2, 3, 5, 11, 29):
        small_primes = [p for p in primes if p <= z]
        total = 0
        count = 0
        for epsilon_small in environments(small_primes):
            epsilon = {
                p: (epsilon_small[p] if p in epsilon_small else -1)
                for p in primes
            }
            total += energy_at(rows, coefficients, epsilon)
            count += 1
        rough = diagonal
        for kappa, value in grouped.items():
            least = min(factorization(kappa))
            if least > z:
                rough += mobius(kappa) * value
        cert.check(total == count * rough, "rough_kernel_filtration")


def check_one_corner_extremizer(cert: Certificate) -> None:
    primes = [2, 3, 5, 7, 11, 13]
    product = 1
    for p in primes:
        product *= p
    labels = divisors(product)
    r_size = len(labels)
    total_square = 0
    nonzero_points = 0
    all_minus_value = 0
    for epsilon in environments(primes):
        value = sum(mobius(u) * character(u, epsilon) for u in labels)
        product_value = 1
        for p in primes:
            product_value *= 1 - epsilon[p]
        cert.check(value == product_value, "one_corner_product_identity")
        total_square += value * value
        if value != 0:
            nonzero_points += 1
        if all(epsilon[p] == -1 for p in primes):
            all_minus_value = value
    cert.check(r_size == 1 << len(primes), "one_corner_label_count")
    cert.check(total_square == r_size * r_size, "one_corner_second_moment")
    cert.check(all_minus_value == r_size, "one_corner_all_minus_value")
    cert.check(nonzero_points == 1, "one_corner_support")


def check_source_hygiene(cert: Certificate) -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_float = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Constant) and isinstance(node.value, float)
    ]
    forbidden_assert = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    forbidden_division = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div)
    ]
    forbidden_random = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            forbidden_random.extend(alias for alias in node.names if alias.name == "random")
        if isinstance(node, ast.ImportFrom) and node.module == "random":
            forbidden_random.append(node)
    cert.check(not forbidden_float, "source_hygiene")
    cert.check(not forbidden_assert, "source_hygiene")
    cert.check(not forbidden_division, "source_hygiene")
    cert.check(not forbidden_random, "source_hygiene")


def main() -> None:
    cert = Certificate()
    check_exponent_ledger(cert)
    check_multiplicative_identity(cert)
    check_product_fibers(cert)
    check_zero_alias_injection(cert)
    check_energy_and_walsh_corner(cert)
    check_one_corner_extremizer(cert)
    check_source_hygiene(cert)

    payload = {
        "schema": "tpc43-exact-certificate-v1",
        "checks": cert.checks,
        "stats": dict(sorted(cert.stats.items())),
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    canonical_payload = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    result = dict(payload)
    result["certificate_digest"] = sha256(canonical_payload).hexdigest()
    OUT.write_text(
        json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        encoding="ascii",
        newline="\n",
    )
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
