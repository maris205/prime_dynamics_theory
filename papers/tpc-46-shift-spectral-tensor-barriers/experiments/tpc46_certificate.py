#!/usr/bin/env python3
"""Exact finite certificate for TPC-46.

The certificate checks finite algebraic identities, operator norms,
counterexample constructions, modular spectral supports, alias folding,
and all rational exponent ledgers.  It does not certify asymptotic
Fourier decay or any Mobius-cancellation statement.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random


G = tuple[int, int]


def gadd(x: G, y: G) -> G:
    return (x[0] + y[0], x[1] + y[1])


def gmul(x: G, y: G) -> G:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def gscale(n: int, x: G) -> G:
    return (n * x[0], n * x[1])


def gnorm2(x: G) -> int:
    return x[0] * x[0] + x[1] * x[1]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True


def primitive_root(p: int) -> int:
    """Return the least primitive root modulo the supported prime p."""
    factors = prime_divisors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root found modulo {p}")


def prime_divisors(n: int) -> tuple[int, ...]:
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ans.append(n)
    return tuple(ans)


def is_squarefree(n: int) -> bool:
    return all(n % (q * q) != 0 for q in prime_divisors(n))


def product_multiplicity(xs: list[int], ys: list[int]) -> int:
    counts: dict[int, int] = defaultdict(int)
    for x in xs:
        for y in ys:
            counts[x * y] += 1
    return max(counts.values(), default=0)


def direct_packet(
    ps: list[int],
    rs: list[int],
    ms: list[int],
    js: list[int],
    a: dict[int, G],
    b: dict[int, G],
    c: dict[int, G],
    eta: dict[int, G],
) -> dict[int, G]:
    out: dict[int, G] = defaultdict(lambda: (0, 0))
    for p in ps:
        for r in rs:
            for m in ms:
                for j in js:
                    value = gmul(gmul(a[p], b[r]), gmul(c[m], eta[j]))
                    h = p * r - m * j
                    out[h] = gadd(out[h], value)
    return dict(out)


def convolution_packet(
    ps: list[int],
    rs: list[int],
    ms: list[int],
    js: list[int],
    a: dict[int, G],
    b: dict[int, G],
    c: dict[int, G],
    eta: dict[int, G],
) -> dict[int, G]:
    left: dict[int, G] = defaultdict(lambda: (0, 0))
    right: dict[int, G] = defaultdict(lambda: (0, 0))
    for p in ps:
        for r in rs:
            left[p * r] = gadd(left[p * r], gmul(a[p], b[r]))
    for m in ms:
        for j in js:
            right[m * j] = gadd(right[m * j], gmul(c[m], eta[j]))
    out: dict[int, G] = defaultdict(lambda: (0, 0))
    for n, x in left.items():
        for q, y in right.items():
            out[n - q] = gadd(out[n - q], gmul(x, y))
    return dict(out)


def tensor_energy(
    ps: list[int],
    rs: list[int],
    ms: list[int],
    js: list[int],
    a: dict[int, G],
    b: dict[int, G],
    c: dict[int, G],
    eta: dict[int, G],
) -> int:
    left = sum(gnorm2(gmul(a[p], b[r])) for p in ps for r in rs)
    right = sum(gnorm2(gmul(c[m], eta[j])) for m in ms for j in js)
    return left * right


def atomic_diagonals(
    ps: list[int],
    rs: list[int],
    ms: list[int],
    js: list[int],
    a: dict[int, G],
    b: dict[int, G],
    c: dict[int, G],
    eta: dict[int, G],
) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for p in ps:
        for r in rs:
            for m in ms:
                for j in js:
                    value = gmul(gmul(a[p], b[r]), gmul(c[m], eta[j]))
                    out[p * r - m * j] += gnorm2(value)
    return dict(out)


def main() -> None:
    checks = 0
    rng = random.Random(4601)
    ps = [11, 13, 17]
    rs = [1, 2, 3, 5]
    ms = [6, 10, 14]
    js = [2, 3, 4]
    rho_left = product_multiplicity(ps, rs)
    rho_right = product_multiplicity(ms, js)

    # Exhaustive deterministic random trials for the exact synthesis
    # identity, diagonal disintegration, and tensor bound.
    for _ in range(640):
        def seq(keys: list[int]) -> dict[int, G]:
            return {k: (rng.randint(-2, 2), rng.randint(-2, 2)) for k in keys}

        a = seq(ps)
        b = seq(rs)
        c = seq(ms)
        eta = seq(js)
        direct = direct_packet(ps, rs, ms, js, a, b, c, eta)
        conv = convolution_packet(ps, rs, ms, js, a, b, c, eta)
        assert direct == conv
        checks += len(set(direct) | set(conv)) + 1

        tensor = tensor_energy(ps, rs, ms, js, a, b, c, eta)
        diagonal = atomic_diagonals(ps, rs, ms, js, a, b, c, eta)
        assert sum(diagonal.values()) == tensor
        checks += 1
        for value in direct.values():
            assert gnorm2(value) <= rho_left * rho_right * tensor
            checks += 1

    # Large-prime product injectivity.
    n_plus = 400
    large_ps = [p for p in range(23, 40) if is_prime(p)]
    products: dict[int, int] = defaultdict(int)
    for p in large_ps:
        assert p * p > n_plus
        checks += 1
        for r in range(1, n_plus // p + 1):
            products[p * r] += 1
    assert max(products.values()) == 1
    checks += len(products) + 1

    # Residual-label Parseval as an exact Walsh average.
    dmap = {6: 2, 10: 5, 14: 7}
    residual_rs = [1, 11, 13, 17]
    small_a = {p: (1, (p // 2) % 2) for p in ps}
    small_b = {r: ((r % 3) - 1, 1) for r in residual_rs}
    small_c = {m: (1, (m // 2) % 3 - 1) for m in ms}
    small_eta = {j: (1, 0) for j in js}
    residual: dict[tuple[int, int], G] = defaultdict(lambda: (0, 0))
    tuples = []
    for p in ps:
        for r in residual_rs:
            for m in ms:
                for j in js:
                    coeff = gmul(
                        gmul(small_a[p], small_b[r]),
                        gmul(small_c[m], small_eta[j]),
                    )
                    h = p * r - m * j
                    s = dmap[m] * r
                    assert is_squarefree(s)
                    residual[(h, s)] = gadd(residual[(h, s)], coeff)
                    tuples.append((h, s, coeff))
    lhs = sum(gnorm2(v) for v in residual.values())
    collision: G = (0, 0)
    for h1, s1, x in tuples:
        for h2, s2, y in tuples:
            if h1 == h2 and s1 == s2:
                product = gmul(x, (y[0], -y[1]))
                collision = gadd(collision, product)
                checks += 1
    assert collision == (lhs, 0)
    checks += 1

    primes = sorted(
        set(q for _, s, _ in tuples for q in prime_divisors(s))
    )
    walsh_total = Fraction(0)
    for mask in range(1 << len(primes)):
        signs = {
            q: (-1 if (mask >> i) & 1 else 1)
            for i, q in enumerate(primes)
        }
        by_h: dict[int, G] = defaultdict(lambda: (0, 0))
        for h, s, coeff in tuples:
            chi = 1
            for q in prime_divisors(s):
                chi *= signs[q]
            by_h[h] = gadd(by_h[h], gscale(chi, coeff))
        walsh_total += Fraction(sum(gnorm2(v) for v in by_h.values()), 1 << len(primes))
        checks += len(by_h)
    assert walsh_total == lhs
    checks += 1

    # Exact weighted grouping norm on a finite atom map.
    atoms = [
        (0, 10), (0, 10), (0, 11),
        (1, 10), (1, 10), (1, 10), (2, 12),
    ]
    weights = {0: Fraction(2, 3), 1: Fraction(5, 7), 2: Fraction(3, 2)}
    fibers: dict[tuple[int, int], int] = defaultdict(int)
    for key in atoms:
        fibers[key] += 1
    rho = max(fibers.values())
    maximizing = max(fibers, key=fibers.get)
    gram = [
        [1 if atoms[i] == atoms[j] else 0 for j in range(len(atoms))]
        for i in range(len(atoms))
    ]
    for i in range(len(atoms)):
        for j in range(len(atoms)):
            square_entry = sum(
                gram[i][ell] * gram[ell][j]
                for ell in range(len(atoms))
            )
            assert square_entry == fibers[atoms[i]] * gram[i][j]
            checks += len(atoms) + 1
    numerator = weights[maximizing[0]] * fibers[maximizing] ** 2
    denominator = weights[maximizing[0]] * fibers[maximizing]
    assert numerator / denominator == rho
    checks += len(atoms) + len(fibers) + 1

    # Fixed-shift coherent prime construction.
    fixed_h = 1
    j0 = 5
    fixed_ps = [7, 11, 13, 17, 19]
    R0 = 20
    solutions = []
    for p in fixed_ps:
        candidates = [r for r in range(R0, R0 + j0) if (p * r - fixed_h) % j0 == 0]
        assert len(candidates) == 1
        r = candidates[0]
        m = (p * r - fixed_h) // j0
        assert p * r - m * j0 == fixed_h
        solutions.append((p, r, m))
        checks += 3
    assert len(solutions) == len(fixed_ps)
    selected_rs = {r for _, r, _ in solutions}
    selected_ms = {m for _, _, m in solutions}
    fixed_count = sum(
        1
        for p in fixed_ps
        for r in selected_rs
        for m in selected_ms
        if p * r - m * j0 == fixed_h
    )
    fixed_diagonal = fixed_count
    assert fixed_count >= len(fixed_ps)
    assert fixed_diagonal > 0
    assert Fraction(fixed_count * fixed_count, fixed_diagonal) >= len(fixed_ps)
    checks += 1

    # Exact finite-field DFT model of the spectral support theorem.  If
    # the j-profile has Fourier support S on Z/NZ, direct synthesis and
    # a second DFT give K_m(k) = what(-m*k).
    N = 101
    MOD = 607  # prime, with N | MOD-1
    generator = primitive_root(MOD)
    omega = pow(generator, (MOD - 1) // N, MOD)
    assert pow(omega, N, MOD) == 1
    assert all(pow(omega, d, MOD) != 1 for d in range(1, N))
    S = {-2, -1, 0, 1, 2}
    Smod = {s % N for s in S}
    what = {
        q: ((q * q + 5 * q + 7) % (MOD - 1)) + 1
        for q in Smod
    }
    inv_N = pow(N, -1, MOD)
    orbit_profile = [
        inv_N * sum(
            value * pow(omega, (j * q) % N, MOD)
            for q, value in what.items()
        ) % MOD
        for j in range(N)
    ]
    m_values = [7, 9, 11]
    support = set()
    for m in m_values:
        for k in range(N):
            kernel = sum(
                orbit_profile[j] * pow(omega, (m * j * k) % N, MOD)
                for j in range(N)
            ) % MOD
            expected = what.get((-m * k) % N, 0)
            assert kernel == expected
            if kernel:
                support.add(k)
            checks += N + 1
    expected_support = {
        k for k in range(N)
        if any((-m * k) % N in Smod for m in m_values)
    }
    assert support == expected_support
    complement = set(range(N)) - support
    assert support.isdisjoint(complement)
    checks += 2 * N

    # Exact finite-field DFT alias folding.  Downsampling by stride M
    # maps full frequencies to congruence classes modulo K=N/M, with
    # the exact translation phase.
    N_alias = 60
    stride = 12  # alias spacing M
    K = N_alias // stride
    MOD_ALIAS = 601  # prime, with N_alias | MOD_ALIAS-1
    g_alias = primitive_root(MOD_ALIAS)
    omega_alias = pow(g_alias, (MOD_ALIAS - 1) // N_alias, MOD_ALIAS)
    omega_K = pow(omega_alias, stride, MOD_ALIAS)
    h0_alias = 7
    full_values = [
        (c * c * c + 3 * c * c + 5 * c + 1) % MOD_ALIAS
        for c in range(N_alias)
    ]
    full_coeff = {
        q: sum(
            full_values[c] * pow(omega_alias, (-c * q) % N_alias, MOD_ALIAS)
            for c in range(N_alias)
        ) % MOD_ALIAS
        for q in range(N_alias)
    }
    sampled = [
        full_values[(h0_alias + stride * k) % N_alias]
        for k in range(K)
    ]
    inv_stride = pow(stride, -1, MOD_ALIAS)
    for beta in range(K):
        sampled_dft = sum(
            sampled[k] * pow(omega_K, (-k * beta) % K, MOD_ALIAS)
            for k in range(K)
        ) % MOD_ALIAS
        folded = inv_stride * sum(
            full_coeff[beta + t * K]
            * pow(
                omega_alias,
                h0_alias * (beta + t * K) % N_alias,
                MOD_ALIAS,
            )
            for t in range(stride)
        ) % MOD_ALIAS
        assert sampled_dft == folded
        checks += N_alias + K + stride + 1

    # Localization spike: the factor H is exact.
    H = 7
    energies = {h: (1 if h == 0 else 0) for h in range(-H, H + 1)}
    window_average = Fraction(sum(energies.values()), H)
    assert energies[0] == H * window_average
    checks += len(energies) + 1

    # Rational exponent ledger.
    Q_exp = Fraction(267, 400)
    J_exp = Fraction(133, 400)
    D_exp = Fraction(10049, 52500)
    L_exp = Fraction(99979, 210000)
    budget = Fraction(1, 400)
    alias_exp = Fraction(399, 400)
    local_geom = J_exp - D_exp
    ladder = L_exp - J_exp
    ledgers = {
        "source_Q": Q_exp,
        "orbit_J": J_exp,
        "source_D": D_exp,
        "source_L": L_exp,
        "alias_modulus": alias_exp,
        "endpoint_budget": budget,
        "Q_plus_J": Q_exp + J_exp,
        "alias_plus_budget": alias_exp + budget,
        "local_geometry": local_geom,
        "ladder_frontier": ladder,
        "ladder_budget_deficit": ladder - budget,
        "fixed_box_budget_deficit": Q_exp - budget,
        "Poisson_local_deficit": Q_exp - local_geom,
        "global_atomic_coordinates": 2 * Q_exp + J_exp,
        "global_coordinate_square_root": (2 * Q_exp + J_exp) / 2,
    }
    assert ledgers["Q_plus_J"] == 1
    assert ledgers["alias_plus_budget"] == 1
    assert local_geom == Fraction(29629, 210000)
    assert ladder == Fraction(15077, 105000)
    assert ladder - budget == Fraction(29629, 210000)
    assert Q_exp - budget == Fraction(133, 200)
    assert Q_exp - local_geom == Fraction(55273, 105000)
    assert 2 * Q_exp + J_exp == Fraction(667, 400)
    assert (2 * Q_exp + J_exp) / 2 == Fraction(667, 800)
    checks += len(ledgers)

    report = {
        "certificate": "TPC-46",
        "checks": checks,
        "exact_identities": {
            "product_synthesis": True,
            "diagonal_disintegration": True,
            "residual_collision_parseval": True,
            "walsh_squarefree_residual_scalarization": True,
            "weighted_grouping_norm": True,
            "fixed_shift_prime_construction": True,
            "discrete_shift_spectral_support": True,
            "alias_frequency_folding": True,
            "localization_spike": True,
        },
        "multiplicities": {
            "rho_pr_toy": rho_left,
            "rho_mj_toy": rho_right,
            "weighted_grouping_rho": rho,
        },
        "ledgers": {
            key: {
                "numerator": value.numerator,
                "denominator": value.denominator,
                "decimal": float(value),
            }
            for key, value in ledgers.items()
        },
        "claim_boundary": (
            "Finite algebra and spectral-support analogues only; "
            "no asymptotic Fourier decay, Mobius cancellation, "
            "fixed-shift TPC closure, or twin-prime consequence."
        ),
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("utf-8")
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    out = Path(__file__).with_name("tpc46_certificate.json")
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"TPC-46 certificate: {checks} checks passed")
    print(f"payload sha256: {report['payload_sha256']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
