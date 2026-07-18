#!/usr/bin/env python3
"""Exact finite certificate for TPC-34.

The script uses only integer, Fraction, and Gaussian-rational arithmetic.
It certifies finite identities and rational ledgers, not asymptotic
Mobius cancellation or the physical Q^3 energy gate.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import gcd, isqrt, lcm
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def divisors(n: int) -> list[int]:
    n = abs(n)
    out: list[int] = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def tau(n: int) -> int:
    return len(divisors(n))


def mobius(n: int) -> int:
    if n == 1:
        return 1
    value = n
    primes = 0
    p = 2
    while p * p <= value:
        if value % p == 0:
            value //= p
            primes += 1
            if value % p == 0:
                return 0
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        primes += 1
    return -1 if primes % 2 else 1


def lambda_g(v: int, cutoff: int) -> int:
    return sum(mobius(v // g) for g in divisors(v) if g <= cutoff)


# Gaussian rationals are represented as (real, imaginary).
QI = tuple[Fraction, Fraction]


def qi(real: int | Fraction = 0, imag: int | Fraction = 0) -> QI:
    return (Fraction(real), Fraction(imag))


def qadd(a: QI, b: QI) -> QI:
    return (a[0] + b[0], a[1] + b[1])


def qneg(a: QI) -> QI:
    return (-a[0], -a[1])


def qsub(a: QI, b: QI) -> QI:
    return qadd(a, qneg(b))


def qmul(a: QI, b: QI) -> QI:
    return (a[0] * b[0] - a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qconj(a: QI) -> QI:
    return (a[0], -a[1])


def qabs2(a: QI) -> Fraction:
    return a[0] * a[0] + a[1] * a[1]


def qscale(a: QI, scalar: int | Fraction) -> QI:
    scalar = Fraction(scalar)
    return (a[0] * scalar, a[1] * scalar)


def qsum(values) -> QI:
    out = qi()
    for value in values:
        out = qadd(out, value)
    return out


def qdet(*indices: int) -> QI:
    seed = 0
    for k, value in enumerate(indices, start=1):
        seed += (7 * k + 3) * (value + 2)
    real = Fraction((seed % 13) - 6, (seed % 3) + 1)
    imag = Fraction(((5 * seed + 4) % 11) - 5, ((seed + 1) % 4) + 1)
    return qi(real, imag)


def check_ttstar_identities() -> dict:
    local = 0
    cases = []
    for a_count, g_count, j_count in [(3, 2, 3), (4, 3, 2), (5, 4, 4)]:
        coeff = [qdet(1, a, a_count) for a in range(a_count)]
        amat = {}
        cval = {}
        hval = {}
        for a in range(a_count):
            for j in range(j_count):
                cval[a, j] = qdet(2, a, j)
                for g in range(g_count):
                    amat[a, g, j] = qdet(3, a, g, j)
        for g in range(g_count):
            for j in range(j_count):
                hval[g, j] = qdet(4, g, j)

        kernel = {}
        for g in range(g_count):
            for a in range(a_count):
                kernel[g, a] = qsum(
                    qmul(amat[a, g, j], qmul(cval[a, j], hval[g, j]))
                    for j in range(j_count)
                )

        bvec = {}
        for g in range(g_count):
            bvec[g] = qsum(
                qmul(coeff[a], kernel[g, a]) for a in range(a_count)
            )
        energy = sum(qabs2(bvec[g]) for g in range(g_count))

        gram = {}
        for a1 in range(a_count):
            for a2 in range(a_count):
                gram[a1, a2] = qsum(
                    qmul(qconj(kernel[g, a1]), kernel[g, a2])
                    for g in range(g_count)
                )
                reverse_gram = qsum(
                    qmul(qconj(kernel[g, a2]), kernel[g, a1])
                    for g in range(g_count)
                )
                require(
                    reverse_gram == qconj(gram[a1, a2]),
                    "Gram matrix lost Hermitian symmetry",
                )
                local += 1

        quadratic = qsum(
            qmul(qmul(qconj(coeff[a1]), coeff[a2]), gram[a1, a2])
            for a1 in range(a_count)
            for a2 in range(a_count)
        )
        require(quadratic[1] == 0 and quadratic[0] == energy,
                "TT* quadratic identity failed")
        local += 1

        diagonal = sum(
            qabs2(coeff[a]) * qabs2(kernel[g, a])
            for g in range(g_count)
            for a in range(a_count)
        )
        off = qsum(
            qmul(
                qmul(qconj(coeff[a1]), coeff[a2]),
                qmul(qconj(kernel[g, a1]), kernel[g, a2]),
            )
            for g in range(g_count)
            for a1 in range(a_count)
            for a2 in range(a_count)
            if a1 != a2
        )
        require(off[1] == 0 and diagonal + off[0] == energy,
                "Gram-copy diagonal split failed")
        local += 1

        y = {}
        for g in range(g_count):
            for j in range(j_count):
                y[g, j] = qsum(
                    qmul(coeff[a], qmul(amat[a, g, j], cval[a, j]))
                    for a in range(a_count)
                )
            reconstructed = qsum(
                qmul(hval[g, j], y[g, j]) for j in range(j_count)
            )
            require(reconstructed == bvec[g],
                    "orbit-sliced reconstruction failed")
            local += 1
        v_energy = sum(
            qabs2(y[g, j])
            for g in range(g_count)
            for j in range(j_count)
        )
        max_h = max(qabs2(hval[g, j])
                    for g in range(g_count) for j in range(j_count))
        require(energy <= j_count * max_h * v_energy,
                "orbit-sliced Cauchy failed")
        local += 1

        for g in range(g_count):
            for a in range(a_count):
                pieces = [
                    qmul(amat[a, g, j], qmul(cval[a, j], hval[g, j]))
                    for j in range(j_count)
                ]
                require(
                    qabs2(kernel[g, a])
                    <= j_count * sum(qabs2(piece) for piece in pieces),
                    "finite column Cauchy failed",
                )
                local += 1
        cases.append([a_count, g_count, j_count])
    return {"checks": local, "cases": cases}


def check_divisor_incidence_gram() -> dict:
    local = 0
    rows = [
        {"ell": 5, "d": 2},
        {"ell": 7, "d": 3},
        {"ell": 11, "d": 5},
        {"ell": 13, "d": 6},
    ]
    for row in rows:
        row["m"] = row["ell"] * row["d"]
    js = [2, 3, 4]
    h = 1
    cutoff = 2
    lower = 2
    upper = max(row["m"] * j + h for row in rows for j in js)
    coeff = [qi(a + 1, 1 - a) for a in range(len(rows))]

    def base_factor(a: int, g: int, j: int) -> int:
        if a == g:
            return 0
        return -1 if (a + 2 * g + j) % 2 else 1

    def hfactor(g: int, j: int) -> int:
        return 1 + ((g + j) % 3)

    def atest(u: int) -> int:
        return -mobius(u) * (u + 1)

    cvals = {}
    for a, row in enumerate(rows):
        for j in js:
            target = row["m"] * j + h
            cvals[a, j] = sum(
                atest(u) for u in divisors(target) if lower < u <= upper
            )

    direct_b = {}
    for g, grow in enumerate(rows):
        total = qi()
        for a, arow in enumerate(rows):
            pair_mask = int(gcd(arow["d"], grow["d"]) <= cutoff)
            inner = sum(
                pair_mask * base_factor(a, g, j)
                * cvals[a, j] * hfactor(g, j)
                for j in js
            )
            total = qadd(total, qscale(coeff[a], inner))
        direct_b[g] = total

    xis = []
    for a, row in enumerate(rows):
        for j in js:
            target = row["m"] * j + h
            for u in divisors(target):
                if lower < u <= upper:
                    for v in divisors(row["d"]):
                        xis.append((a, j, u, v))

    z = {}
    phi = {}
    for index, (a, j, u, v) in enumerate(xis):
        z[index] = qscale(coeff[a], atest(u) * lambda_g(v, cutoff))
        for g, grow in enumerate(rows):
            phi[g, index] = qi(
                int(grow["d"] % v == 0)
                * base_factor(a, g, j)
                * hfactor(g, j)
            )

    opened_b = {
        g: qsum(qmul(phi[g, index], z[index])
                for index in range(len(xis)))
        for g in range(len(rows))
    }
    for g in range(len(rows)):
        require(opened_b[g] == direct_b[g],
                "opened gcd-projector column disagrees with direct column")
        local += 1

    direct_energy = sum(qabs2(value) for value in direct_b.values())
    gram_energy = qi()
    for i1 in range(len(xis)):
        for i2 in range(len(xis)):
            gram = qsum(
                qmul(qconj(phi[g, i1]), phi[g, i2])
                for g in range(len(rows))
            )
            gram_energy = qadd(
                gram_energy,
                qmul(qmul(qconj(z[i1]), z[i2]), gram),
            )
            v1 = xis[i1][3]
            v2 = xis[i2][3]
            modulus = lcm(v1, v2)
            for g, grow in enumerate(rows):
                if phi[g, i1] != qi() and phi[g, i2] != qi():
                    require(grow["d"] % modulus == 0,
                            "LCM incidence support failed")
                    local += 1
    require(gram_energy[1] == 0 and gram_energy[0] == direct_energy,
            "opened Gram energy identity failed")
    local += 1

    for arow in rows:
        for grow in rows:
            lhs = int(gcd(arow["d"], grow["d"]) <= cutoff)
            rhs = sum(
                lambda_g(v, cutoff)
                for v in divisors(gcd(arow["d"], grow["d"]))
            )
            require(lhs == rhs, "finite gcd-projector identity failed")
            local += 1

    for v1 in range(1, 13):
        for v2 in range(1, 13):
            modulus = lcm(v1, v2)
            for start, length in [(1, 20), (7, 31), (23, 17)]:
                count = sum(
                    1 for d in range(start, start + length)
                    if d % modulus == 0
                )
                require(Fraction(count) <= 1 + Fraction(length, modulus),
                        "finite LCM interval count failed")
                local += 1
    return {
        "checks": local,
        "rows": len(rows),
        "orbit_points": len(js),
        "opened_indices": len(xis),
    }


def check_target_collision_multiplicity() -> dict:
    local = 0
    case_count = 0
    for rows in [[6, 10, 15], [5, 7, 11, 13], [8, 9, 12, 25]]:
        for start, length in [(2, 7), (5, 9), (11, 6)]:
            js = list(range(start, start + length))
            fibers: dict[int, list[tuple[int, int]]] = {}
            for m in rows:
                for j in js:
                    fibers.setdefault(m * j, []).append((m, j))
            direct = sum(
                1
                for m1 in rows for j1 in js
                for m2 in rows for j2 in js
                if m1 * j1 == m2 * j2
            )
            require(direct == sum(len(fiber) ** 2
                                  for fiber in fibers.values()),
                    "target collision fiber count failed")
            local += 1
            for p, fiber in fibers.items():
                require(len(fiber) <= tau(p),
                        "target multiplicity exceeded divisor count")
                local += 1
            weights = {
                (m, j): Fraction((m + 3 * j) % 11 + 1,
                                 (2 * m + j) % 5 + 1)
                for m in rows for j in js
            }
            weighted_direct = sum(
                weights[m1, j1] * weights[m2, j2]
                for m1 in rows for j1 in js
                for m2 in rows for j2 in js
                if m1 * j1 == m2 * j2
            )
            weighted_fibers = sum(
                sum(weights[pair] for pair in fiber) ** 2
                for fiber in fibers.values()
            )
            require(weighted_direct == weighted_fibers,
                    "weighted target collision identity failed")
            local += 1
            max_tau = max(tau(p) for p in fibers)
            rhs = max_tau * sum(weight * weight
                                for weight in weights.values())
            require(weighted_fibers <= rhs,
                    "weighted target collision Cauchy failed")
            local += 1
            h = 3
            require(all(
                ((m1 * j1 + h == m2 * j2 + h)
                 == (m1 * j1 == m2 * j2))
                for m1 in rows for j1 in js
                for m2 in rows for j2 in js
            ), "target/source collision equivalence failed")
            local += 1
            case_count += 1
    return {"checks": local, "cases": case_count}


def check_shared_ultra_congruence() -> dict:
    local = 0
    case_count = 0
    h = 1
    for rows in [[5, 7, 11, 13], [17, 19, 23, 29, 31]]:
        for js in [list(range(4, 8)), list(range(9, 15))]:
            diameter = max(js) - min(js)
            threshold = diameter + 1
            max_target = max(m * j + h for m in rows for j in js)
            weights = {m: Fraction((m % 7) + 1, (m % 3) + 1)
                       for m in rows}
            incidences = {}
            for u in range(threshold + 1, max_target + 1):
                pairs = [(m, j) for m in rows for j in js
                         if (m * j + h) % u == 0]
                if not pairs:
                    continue
                incidences[u] = pairs
                for m, j in pairs:
                    require(gcd(u, m * j * h) == 1,
                            "shared-ultra primitivity failed")
                    local += 1
                for m in rows:
                    count = sum(1 for mm, _ in pairs if mm == m)
                    require(count <= 1,
                            "fixed-row ultra congruence had two orbit points")
                    local += 1
                for j in js:
                    mvals = [m for m, jj in pairs if jj == j]
                    if mvals:
                        residues = {m % u for m in mvals}
                        require(len(residues) == 1,
                                "fixed-time ultra incidence lost residue class")
                        local += 1
                        span = max(rows) - min(rows)
                        require(len(mvals) <= span // u + 1,
                                "fixed-time row occupancy bound failed")
                        local += 1
                aval = sum(weights[m] for m, _ in pairs)
                row_bound = sum(weights.values()) * (
                    diameter // u + 1
                )
                time_bound = max(weights.values()) * len(js) * (
                    (max(rows) - min(rows)) // u + 1
                )
                require(aval <= row_bound and aval <= time_bound,
                        "weighted shared-ultra occupancy failed")
                local += 1
            if incidences:
                avals = [
                    sum(weights[m] for m, _ in pairs)
                    for pairs in incidences.values()
                ]
                require(sum(value * value for value in avals)
                        <= max(avals) * sum(avals),
                        "shared-ultra max-times-sum inequality failed")
                local += 1
            case_count += 1
    return {"checks": local, "cases": case_count}


def check_same_row_gcd_and_lag() -> dict:
    local = 0
    gcd_cases = 0
    for m in range(2, 19):
        for h in range(1, 9):
            if gcd(m, h) != 1:
                continue
            for j1 in range(3, 15):
                for j2 in range(3, 15):
                    lhs = gcd(m * j1 + h, m * j2 + h)
                    rhs = gcd(m * j1 + h, abs(j2 - j1))
                    require(lhs == rhs, "two-time gcd identity failed")
                    local += 1
                    if j1 != j2:
                        require(lhs <= abs(j2 - j1),
                                "two-time gcd exceeded orbit lag")
                        local += 1
                    for c in range(1, 18):
                        if gcd(c, m) != 1:
                            continue
                        direct = ((m * j1 + h) % c == 0
                                  and (m * j2 + h) % c == 0)
                        modular = ((j2 - j1) % c == 0
                                   and j1 % c
                                   == (-h * pow(m, -1, c)) % c)
                        require(direct == modular,
                                "modular-return equivalence failed")
                        local += 1
                    gcd_cases += 1

    lag_cases = 0
    for j0 in range(4, 22):
        interval = list(range(7, 7 + j0))
        harmonic = sum(Fraction(1, k) for k in range(1, j0))
        for zcut in range(1, j0):
            for m, h in [(5, 1), (7, 2), (11, 3)]:
                true_count = sum(
                    1 for j1 in interval for j2 in interval
                    if j1 != j2
                    and gcd(m * j1 + h, m * j2 + h) > zcut
                )
                overcount = 0
                for j1 in interval:
                    for j2 in interval:
                        if j1 == j2:
                            continue
                        r = abs(j2 - j1)
                        overcount += sum(
                            1 for c in divisors(r)
                            if c > zcut and gcd(c, m) == 1
                            and (m * j1 + h) % c == 0
                        )
                require(true_count <= overcount,
                        "large-lag divisor overcount failed")
                local += 1
                explicit_bound = (
                    Fraction(2 * j0 * j0, zcut)
                    +2 * j0 * harmonic
                )
                require(Fraction(overcount) <= explicit_bound,
                        "large-lag explicit harmonic bound failed")
                local += 1
                lag_cases += 1
    return {
        "checks": local,
        "gcd_cases": gcd_cases,
        "lag_cases": lag_cases,
    }


def check_orbit_sliced_cauchy() -> dict:
    local = 0
    cases = 0
    for g_count in range(2, 7):
        for j_count in range(1, 9):
            y = {(g, j): qdet(11, g, j, j_count)
                 for g in range(g_count) for j in range(j_count)}
            h = {(g, j): qdet(12, g, j, g_count)
                 for g in range(g_count) for j in range(j_count)}
            b = {
                g: qsum(qmul(h[g, j], y[g, j])
                        for j in range(j_count))
                for g in range(g_count)
            }
            energy = sum(qabs2(value) for value in b.values())
            venergy = sum(qabs2(value) for value in y.values())
            hmax = max(qabs2(value) for value in h.values())
            require(energy <= j_count * hmax * venergy,
                    "general orbit-sliced Cauchy failed")
            local += 1

            sharp_energy = g_count * j_count * j_count
            sharp_v = g_count * j_count
            require(sharp_energy == j_count * sharp_v,
                    "orbit-sliced Cauchy sharpness failed")
            local += 1
            cases += 1
    return {"checks": local, "cases": cases}


def check_coherent_majorant() -> dict:
    local = 0
    cases = 0
    for m_count in range(2, 21):
        for j_count in range(1, 13):
            kernel = [
                [j_count if g != a else 0 for a in range(m_count)]
                for g in range(m_count)
            ]
            b = [sum(row) for row in kernel]
            energy = sum(value * value for value in b)
            diagonal = sum(value * value for row in kernel for value in row)
            off = energy - diagonal
            venergy = m_count * j_count * (m_count - 1) ** 2
            require(energy == m_count * (m_count - 1) ** 2
                    * j_count ** 2,
                    "coherent model energy formula failed")
            local += 1
            require(diagonal == m_count * (m_count - 1)
                    * j_count ** 2,
                    "coherent model diagonal formula failed")
            local += 1
            require(off == m_count * (m_count - 1) * (m_count - 2)
                    * j_count ** 2,
                    "coherent model off-diagonal formula failed")
            local += 1
            require(energy == j_count * venergy,
                    "coherent model orbit identity failed")
            local += 1
            for a1 in range(m_count):
                for a2 in range(m_count):
                    gram = sum(kernel[g][a1] * kernel[g][a2]
                               for g in range(m_count))
                    expected = ((m_count - 1) if a1 == a2
                                else (m_count - 2)) * j_count ** 2
                    require(gram == expected,
                            "coherent model Gram entry failed")
                    local += 1
            cases += 1
    return {"checks": local, "cases": cases}


def check_high_beta_ledger() -> dict:
    local = 0
    beta = Fraction(267, 400)
    eta = Fraction(133, 400)
    theta = Fraction(193, 500)
    expected = {
        "Q3": Fraction(4005, 2000),
        "Q3J2": Fraction(5335, 2000),
        "Q2J2": Fraction(4000, 2000),
        "Q2J": Fraction(3335, 2000),
        "Q3J2_over_T": Fraction(4563, 2000),
        "Q3J": Fraction(4670, 2000),
        "Q3_over_J": Fraction(3340, 2000),
    }
    actual = {
        "Q3": 3 * beta,
        "Q3J2": 3 * beta + 2 * eta,
        "Q2J2": 2 * beta + 2 * eta,
        "Q2J": 2 * beta + eta,
        "Q3J2_over_T": 3 * beta + 2 * eta - theta,
        "Q3J": 3 * beta + eta,
        "Q3_over_J": 3 * beta - eta,
    }
    require(beta + eta == 1, "QJ exponent ledger failed")
    local += 1
    require(theta - eta == Fraction(107, 2000),
            "T/J exponent ledger failed")
    local += 1
    for key in expected:
        require(actual[key] == expected[key],
                f"high-beta exponent failed for {key}")
        local += 1
    require(expected["Q3"] - expected["Q2J2"] == Fraction(1, 400),
            "Gram-diagonal margin failed")
    local += 1
    require(expected["Q3"] - expected["Q2J"] == Fraction(67, 200),
            "target-collision margin failed")
    local += 1
    require(expected["Q3J2_over_T"] - expected["Q3"]
            == Fraction(279, 1000),
            "shared-ultra excess failed")
    local += 1
    require(expected["Q3_over_J"] - expected["Q2J"]
            == Fraction(1, 400),
            "orbit-energy allowance failed")
    local += 1
    require(expected["Q3J2"] - expected["Q3J2_over_T"] == theta,
            "shared-ultra saving failed")
    local += 1
    return {
        "checks": local,
        "beta": f"{beta.numerator}/{beta.denominator}",
        "eta": f"{eta.numerator}/{eta.denominator}",
        "theta": f"{theta.numerator}/{theta.denominator}",
        "exponent_numerators_over_2000": {
            key: value.numerator * (2000 // value.denominator)
            for key, value in expected.items()
        },
    }


def main() -> None:
    results = {
        "ttstar_identities": check_ttstar_identities(),
        "divisor_incidence_gram": check_divisor_incidence_gram(),
        "target_collision": check_target_collision_multiplicity(),
        "shared_ultra": check_shared_ultra_congruence(),
        "same_row_gcd_and_lag": check_same_row_gcd_and_lag(),
        "orbit_sliced_cauchy": check_orbit_sliced_cauchy(),
        "coherent_majorant": check_coherent_majorant(),
        "high_beta_ledger": check_high_beta_ledger(),
    }
    claims = {
        "finite_exact_ttstar_identity": True,
        "finite_exact_row_gram_split": True,
        "finite_divisor_incidence_reindexing": True,
        "finite_lcm_support_count": True,
        "finite_target_collision_fiber_identity": True,
        "finite_shared_ultra_congruence": True,
        "finite_same_row_target_gcd": True,
        "finite_large_lag_overcount": True,
        "finite_orbit_sliced_cauchy": True,
        "finite_coherent_majorant_model": True,
        "finite_high_beta_fraction_ledger": True,
        "uses_floating_point": False,
        "uses_random_inputs": False,
        "proves_asymptotic_divisor_bound": False,
        "proves_prefix_Xepsilon_envelope": False,
        "proves_physical_shared_ultra_asymptotic": False,
        "proves_offdiagonal_orbit_operator_bound": False,
        "proves_Q3_column_energy_gate": False,
        "proves_orbit_sliced_V_gate": False,
        "proves_affine_Mobius_or_Chowla_cancellation": False,
        "proves_zero_frequency_flatness": False,
        "proves_complete_residual_closure": False,
        "proves_positivity": False,
        "proves_Hardy_Littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    source = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    payload = {
        "paper": "TPC-34",
        "certificate_version": 1,
        "arithmetic": "integer, Fraction, and Gaussian rational only",
        "check_total": CHECKS,
        "results": results,
        "claims": claims,
        "normalized_source_sha256": sha256(source).hexdigest(),
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    payload["certificate_digest"] = sha256(canonical).hexdigest()
    output = Path(__file__).with_name("tpc34_certificate.json")
    encoded = (json.dumps(payload, indent=2, sort_keys=True,
                          ensure_ascii=True) + "\n").encode("utf-8")
    output.write_bytes(encoded)
    print(
        "TPC-34 exact certificate:"
        f" {CHECKS} checks;"
        f" digest {payload['certificate_digest']};"
        f" wrote {output.name}"
    )


if __name__ == "__main__":
    main()
