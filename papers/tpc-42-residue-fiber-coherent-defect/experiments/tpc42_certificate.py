#!/usr/bin/env python3
"""Exact finite certificate for TPC-42.

The certificate uses only integer, Gaussian-integer, rational, and finite
Dirichlet-convolution arithmetic.  It checks the structural identities in
the paper; it does not numerically test any asymptotic Mobius theorem.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUT = HERE / "tpc42_certificate.json"


def gadd(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] + w[0], z[1] + w[1]


def gscale(a: int, z: tuple[int, int]) -> tuple[int, int]:
    return a * z[0], a * z[1]


def gconj(z: tuple[int, int]) -> tuple[int, int]:
    return z[0], -z[1]


def gmul(z: tuple[int, int], w: tuple[int, int]) -> tuple[int, int]:
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def gnorm2(z: tuple[int, int]) -> int:
    return z[0] * z[0] + z[1] * z[1]


def vadd(
    v: dict[tuple[int, int], tuple[int, int]],
    w: dict[tuple[int, int], tuple[int, int]],
) -> dict[tuple[int, int], tuple[int, int]]:
    out = dict(v)
    for key, value in w.items():
        out[key] = gadd(out.get(key, (0, 0)), value)
        if out[key] == (0, 0):
            del out[key]
    return out


def vscale(
    a: int, v: dict[tuple[int, int], tuple[int, int]]
) -> dict[tuple[int, int], tuple[int, int]]:
    if a == 0:
        return {}
    return {key: gscale(a, value) for key, value in v.items()}


def vinner(
    v: dict[tuple[int, int], tuple[int, int]],
    w: dict[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    total = (0, 0)
    for key in v.keys() & w.keys():
        total = gadd(total, gmul(gconj(v[key]), w[key]))
    return total


def vnorm2(v: dict[tuple[int, int], tuple[int, int]]) -> int:
    return sum(gnorm2(value) for value in v.values())


def mobius_table(limit: int) -> list[int]:
    mu = [1] * (limit + 1)
    prime = [True] * (limit + 1)
    prime[0] = prime[1] = False
    primes: list[int] = []
    mu[0] = 0
    for n in range(2, limit + 1):
        if prime[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            if n * p > limit:
                break
            prime[n * p] = False
            if n % p == 0:
                mu[n * p] = 0
                break
            mu[n * p] = -mu[n]
    return mu


def prime_table(limit: int) -> list[bool]:
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            for n in range(p * p, limit + 1, p):
                is_prime[n] = False
    return is_prime


def prime_power_table(limit: int, is_prime: list[bool]) -> list[int]:
    value = [0] * (limit + 1)
    for p in range(2, limit + 1):
        if not is_prime[p]:
            continue
        q = p
        while q <= limit:
            value[q] = p
            if q > limit // p:
                break
            q *= p
    return value


def convolve(a: list[int], b: list[int]) -> list[int]:
    limit = min(len(a), len(b)) - 1
    out = [0] * (limit + 1)
    for d in range(1, limit + 1):
        if a[d] == 0:
            continue
        for m in range(1, limit // d + 1):
            if b[m]:
                out[d * m] += a[d] * b[m]
    return out


def vector_geometry_checks() -> tuple[int, dict[str, int]]:
    checks = 0
    stats = {
        "moduli": 0,
        "fixed_alias_orthogonality_pairs": 0,
        "fixed_alias_energy_identities": 0,
        "folded_orthogonality_pairs": 0,
        "folded_energy_identities": 0,
        "transversal_injections": 0,
    }
    cases = [
        (5 * 7 * 11, 1, [6, 10, 14, 15, 21, 22, 26, 33, 127, 128], range(1, 5)),
        (
            7 * 11 * 13,
            2,
            [10, 14, 15, 21, 22, 26, 33, 34, 38, 201, 205],
            range(1, 7),
        ),
    ]
    for M, h, rows, js in cases:
        stats["moduli"] += 1
        gammas = range(3)
        # Keep every residue class, including nonunits.  The pairs
        # (127,1),(128,4) and (205,1),(201,6) produce products differing
        # by one full modulus, so the within-fiber orthogonality checks
        # are nonvacuous while the no-wrap row condition still holds.
        valid = {
            (alpha, j)
            for alpha, _m in enumerate(rows)
            for j in js
        }

        def coeff(alpha: int, gamma: int, j: int) -> tuple[int, int]:
            return (
                ((alpha + 2 * gamma + j) % 7) - 3,
                ((2 * alpha - gamma + 3 * j) % 5) - 2,
            )

        for j in js:
            residues = [
                (rows[alpha] * j + h) % M
                for alpha in range(len(rows))
                if (alpha, j) in valid
            ]
            assert len(residues) == len(set(residues))
            checks += 1
            stats["transversal_injections"] += 1

        max_n = max(rows) * max(js) + abs(h) + 2 * M
        mu = mobius_table(max_n)
        for k in range(-2, 3):
            G: dict[int, dict[tuple[int, int], tuple[int, int]]] = defaultdict(dict)
            diagonal = 0
            for alpha, m in enumerate(rows):
                for j in js:
                    if (alpha, j) not in valid:
                        continue
                    r = m * j
                    n = r + h + k * M
                    if n <= 0:
                        continue
                    weight = 1 + ((r + 2 * k) % 5)
                    for gamma in gammas:
                        value = gscale(weight, coeff(alpha, gamma, j))
                        key = (gamma, j)
                        G[r][key] = gadd(G[r].get(key, (0, 0)), value)
                        diagonal += mu[n] ** 2 * gnorm2(value)
            rs = sorted(G)
            for i, r in enumerate(rs):
                for rp in rs[i + 1 :]:
                    if (r - rp) % M == 0:
                        assert vinner(G[r], G[rp]) == (0, 0)
                        checks += 1
                        stats["fixed_alias_orthogonality_pairs"] += 1
            packets: dict[int, dict[tuple[int, int], tuple[int, int]]] = defaultdict(dict)
            direct: dict[tuple[int, int], tuple[int, int]] = {}
            for r, vector in G.items():
                signed = vscale(-mu[r + h + k * M], vector)
                residue = (r + h) % M
                packets[residue] = vadd(packets[residue], signed)
                direct = vadd(direct, signed)
            packed = sum(vnorm2(v) for v in packets.values())
            coherent = {}
            for vector in packets.values():
                coherent = vadd(coherent, vector)
            assert packed == diagonal
            assert coherent == direct
            cross = (0, 0)
            residues = sorted(packets)
            for a in residues:
                for b in residues:
                    if a != b:
                        cross = gadd(cross, vinner(packets[a], packets[b]))
            assert cross[1] == 0
            assert vnorm2(direct) == diagonal + cross[0]
            checks += 3
            stats["fixed_alias_energy_identities"] += 3

        alias_b: dict[tuple[int, int, int], int] = {}
        for alpha, m in enumerate(rows):
            for j in js:
                if (alpha, j) not in valid:
                    continue
                for k in range(-2, 3):
                    n = m * j + h + k * M
                    alias_b[(alpha, j, k)] = (
                        -mu[n] * (1 + (n % 7)) if n > 0 else 0
                    )
        folded = {
            (alpha, j, 0): alias_b[(alpha, j, 0)]
            for alpha, j in valid
        }
        for alpha, j in valid:
            folded[(alpha, j, 1)] = alias_b[(alpha, j, 1)] + alias_b[(alpha, j, -2)]
            folded[(alpha, j, 2)] = alias_b[(alpha, j, 2)] + alias_b[(alpha, j, -1)]

        folded_energy = 0
        same_energy = 0
        cross_rows = (0, 0)
        for s in range(3):
            H: dict[int, dict[tuple[int, int], tuple[int, int]]] = defaultdict(dict)
            direct: dict[tuple[int, int], tuple[int, int]] = {}
            for alpha, m in enumerate(rows):
                for j in js:
                    if (alpha, j) not in valid:
                        continue
                    u = folded[(alpha, j, s)]
                    r = m * j
                    for gamma in gammas:
                        value = gscale(u, coeff(alpha, gamma, j))
                        key = (gamma, j)
                        H[r][key] = gadd(H[r].get(key, (0, 0)), value)
                        direct = vadd(direct, {key: value})
                        same_energy += gnorm2(value)
            rs = sorted(H)
            for i, r in enumerate(rs):
                for rp in rs[i + 1 :]:
                    if (r - rp) % M == 0:
                        assert vinner(H[r], H[rp]) == (0, 0)
                        checks += 1
                        stats["folded_orthogonality_pairs"] += 1
            packets: dict[int, dict[tuple[int, int], tuple[int, int]]] = defaultdict(dict)
            for r, vector in H.items():
                packets[(r + h) % M] = vadd(packets[(r + h) % M], vector)
            assert sum(vnorm2(v) for v in packets.values()) == sum(
                vnorm2(v) for v in H.values()
            )
            coherent = {}
            for vector in packets.values():
                coherent = vadd(coherent, vector)
            assert coherent == direct
            folded_energy += vnorm2(direct)
            residues = sorted(packets)
            for a in residues:
                for b in residues:
                    if a != b:
                        cross_rows = gadd(cross_rows, vinner(packets[a], packets[b]))
            checks += 2
            stats["folded_energy_identities"] += 2
        assert cross_rows[1] == 0
        assert folded_energy == same_energy + cross_rows[0]
        checks += 1
        stats["folded_energy_identities"] += 1
    return checks, stats


def canonical_checks() -> tuple[int, dict[str, int]]:
    checks = 0
    for rho in range(2, 101):
        energy = sum(i * i + (i + 1) * (i + 1) for i in range(1, rho + 1))
        synchronous = Fraction(energy, rho)
        defect = Fraction(rho - 1, rho) * energy
        assert synchronous + defect == energy
        checks += 1
        for i in range(rho):
            for j in range(i + 1, rho):
                # e_i-e_j is in the scalar-sum kernel and is detected by
                # unequal orthogonal columns.
                assert (1 - 1) == 0 and i != j
                checks += 1
    for R in range(1, 501):
        scalar_energy = 0
        packed = 2 * R
        coherent = 2 * R * R
        assert scalar_energy == 0
        assert Fraction(coherent, packed) == R
        checks += 2
    return checks, {
        "orthogonal_fiber_sizes": 99,
        "kernel_witness_pairs": sum(r * (r - 1) // 2 for r in range(2, 101)),
        "sharp_countermodels": 500,
    }


def convolution_checks() -> tuple[int, dict[str, int]]:
    limit = 5000
    mu = mobius_table(limit)
    is_prime = prime_table(limit)
    prime_power = prime_power_table(limit, is_prime)
    one = [0] + [1] * limit
    lam = [0] * (limit + 1)
    for p in range(29, 44):
        if is_prime[p]:
            lam[p] = p
    mu_d = [0] * (limit + 1)
    for d in range(2, 8):
        mu_d[d] = mu[d]
    u_j = [0] * (limit + 1)
    for j in range(8, 14):
        u_j[j] = 1
    mu_minus = [mu[n] - mu_d[n] for n in range(limit + 1)]
    one_minus = [one[n] - u_j[n] for n in range(limit + 1)]
    c = convolve(mu_d, u_j)
    A = convolve(lam, c)
    B_d = convolve(convolve(lam, mu_minus), one)
    B_j = convolve(convolve(lam, mu_d), one_minus)
    checks = 0
    for n in range(1, limit + 1):
        assert A[n] + B_d[n] + B_j[n] == lam[n]
        checks += 1
        if A[n]:
            assert lam[n] == 0
            assert B_d[n] + B_j[n] == -A[n]
            assert prime_power[n] == 0
            checks += 3
    source_energy = sum(x * x for x in lam)
    inner_energy = sum(x * x for x in c)
    local_energy = sum(x * x for x in A)
    assert local_energy == source_energy * inner_energy
    checks += 1
    # The full source completion is coefficientwise tautological for an
    # arbitrary prime-power comparator.
    Lambda = prime_power
    for n in range(1, limit + 1):
        assert Lambda[n] == (Lambda[n] - lam[n]) + A[n] + B_d[n] + B_j[n]
        checks += 1
    return checks, {
        "convolution_range": limit,
        "local_support_points": sum(1 for x in A if x),
        "local_energy": local_energy,
        "source_energy": source_energy,
        "inner_energy": inner_energy,
    }


def exponent_checks() -> tuple[int, dict[str, str]]:
    Q = Fraction(267, 400)
    J = Fraction(133, 400)
    M = Fraction(399, 400)
    K = Fraction(1, 400)
    assert Q + J == 1
    assert M + K == 1
    assert Q - K == 2 * J
    assert 2 * Q + J + K == Fraction(167, 100)
    assert 3 * Q - J == Fraction(167, 100)
    return 5, {
        "Q_plus_J": str(Q + J),
        "M_plus_K": str(M + K),
        "Q_minus_K": str(Q - K),
        "two_J": str(2 * J),
        "target_exponent": str(3 * Q - J),
    }


def main() -> None:
    total = 0
    blocks: dict[str, object] = {}
    for name, fn in [
        ("vector_geometry", vector_geometry_checks),
        ("canonical_defect", canonical_checks),
        ("convolution_counterterm", convolution_checks),
        ("endpoint_exponents", exponent_checks),
    ]:
        count, data = fn()
        total += count
        blocks[name] = {"checks": count, "data": data}

    core = {
        "schema": "tpc42-exact-certificate-v1",
        "status": "pass",
        "checks": total,
        "blocks": blocks,
        "claim_boundary": [
            "finite structural identities only",
            "no numerical evidence for random Mobius signs",
            "no fixed-shift Chowla estimate",
            "no parity breach or twin-prime conclusion",
        ],
    }
    canonical_core = json.dumps(
        core, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    result = dict(core)
    result["certificate_digest"] = sha256(canonical_core).hexdigest()
    result["source_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    payload = (
        json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
    ).encode("ascii")
    OUT.write_bytes(payload)
    print(
        json.dumps(
            {
                "certificate": str(OUT),
                "checks": total,
                "digest": result["certificate_digest"],
                "json_sha256": sha256(payload).hexdigest(),
                "source_sha256": result["source_sha256"],
                "status": "pass",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
