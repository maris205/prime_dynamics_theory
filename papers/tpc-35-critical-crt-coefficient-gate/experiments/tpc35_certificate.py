#!/usr/bin/env python3
"""Exact finite certificate for TPC-35.

This standard-library script uses only integers, Fraction, and a
hand-written Gaussian-rational arithmetic.  It checks finite identities
behind the proposed aspect-ratio, CRT, character-spectrum, and integer
incidence results.  It does not certify any asymptotic Mobius estimate,
joint multi-modulus dispersion, or prime-pair claim.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import ast
import json
from math import gcd, lcm
from pathlib import Path


CHECKS = 0


def require(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(message)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def euler_phi(n: int) -> int:
    value = n
    p = 2
    work = n
    while p * p <= work:
        if work % p == 0:
            value -= value // p
            while work % p == 0:
                work //= p
        p += 1
    if work > 1:
        value -= value // work
    return value


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
    return (
        a[0] * b[0] - a[1] * b[1],
        a[0] * b[1] + a[1] * b[0],
    )


def qconj(a: QI) -> QI:
    return (a[0], -a[1])


def qscale(a: QI, scalar: int | Fraction) -> QI:
    scalar = Fraction(scalar)
    return (a[0] * scalar, a[1] * scalar)


def qabs2(a: QI) -> Fraction:
    return a[0] * a[0] + a[1] * a[1]


def qsum(values) -> QI:
    out = qi()
    for value in values:
        out = qadd(out, value)
    return out


def qinner(a: list[QI], b: list[QI]) -> QI:
    return qsum(qmul(qconj(x), y) for x, y in zip(a, b))


def qnorm2(a: list[QI]) -> Fraction:
    return sum(qabs2(x) for x in a)


def qdet(*indices: int) -> QI:
    seed = 0
    for k, value in enumerate(indices, start=1):
        seed += (11 * k + 5) * (value + 3)
    real = Fraction((seed % 17) - 8, (seed % 4) + 1)
    imag = Fraction(((7 * seed + 3) % 13) - 6, ((seed + 2) % 5) + 1)
    return qi(real, imag)


def qmat(rows: int, cols: int) -> list[list[QI]]:
    return [[qi() for _ in range(cols)] for _ in range(rows)]


def qidentity(n: int) -> list[list[QI]]:
    return [[qi(int(i == j)) for j in range(n)] for i in range(n)]


def qmat_mul(a: list[list[QI]], b: list[list[QI]]) -> list[list[QI]]:
    rows = len(a)
    inner = len(b)
    cols = len(b[0])
    return [
        [qsum(qmul(a[i][k], b[k][j]) for k in range(inner))
         for j in range(cols)]
        for i in range(rows)
    ]


def qmat_vec(a: list[list[QI]], x: list[QI]) -> list[QI]:
    return [qsum(qmul(entry, value) for entry, value in zip(row, x))
            for row in a]


def qmat_require_equal(
    a: list[list[QI]], b: list[list[QI]], message: str
) -> None:
    require(len(a) == len(b), message + " row count")
    for row_a, row_b in zip(a, b):
        require(len(row_a) == len(row_b), message + " column count")
        for entry_a, entry_b in zip(row_a, row_b):
            require(entry_a == entry_b, message)


def phase(seed: int, j: int, a: int) -> QI:
    units = [qi(1), qi(0, 1), qi(-1), qi(0, -1)]
    return units[(seed + 3 * j + 5 * a + 2 * j * a) % 4]


def row_gram(rmat: list[list[QI]]) -> list[list[QI]]:
    t = len(rmat)
    n = len(rmat[0])
    return [
        [qsum(qmul(qconj(rmat[j][a]), rmat[j][b])
              for j in range(t))
         for b in range(n)]
        for a in range(n)
    ]


def sylvester_hadamard(n: int) -> list[list[int]]:
    require(n >= 1 and n & (n - 1) == 0,
            "Hadamard order was not a power of two")
    out = [[1]]
    while len(out) < n:
        size = len(out)
        out = [
            [out[i % size][j % size]
             * (-1 if i >= size and j >= size else 1)
             for j in range(2 * size)]
            for i in range(2 * size)
        ]
    return out


def check_aspect_ratio_gram() -> dict:
    start = CHECKS
    cases = []
    for n, t, seed in [(5, 2, 0), (7, 3, 1), (8, 3, 2), (9, 4, 3)]:
        rmat = [[phase(seed, j, a) for a in range(n)]
                for j in range(t)]
        amat = [[qi(int(g != a)) for a in range(n)] for g in range(n)]
        gram = qmat(n, n)
        for j in range(t):
            mmat = [[qmul(amat[g][a], rmat[j][a])
                     for a in range(n)] for g in range(n)]
            for a in range(n):
                for b in range(n):
                    gram[a][b] = qadd(
                        gram[a][b],
                        qsum(qmul(qconj(mmat[g][a]), mmat[g][b])
                             for g in range(n)),
                    )
        pmat = row_gram(rmat)
        formula = [
            [qadd(qi(t if a == b else 0),
                  qscale(pmat[a][b], n - 2))
             for b in range(n)]
            for a in range(n)
        ]
        qmat_require_equal(gram, formula, "aspect-ratio Gram formula")
        omat = qmat(n, n)
        for a in range(n):
            require(gram[a][a] == qi((n - 1) * t),
                    "aspect-ratio Gram diagonal")
            for b in range(n):
                omat[a][b] = gram[a][b] if a != b else qi()
                expected = qscale(
                    qsub(pmat[a][b], qi(t if a == b else 0)), n - 2
                )
                require(omat[a][b] == expected,
                        "aspect-ratio off-Gram formula")
        require(sum(pmat[a][a][0] for a in range(n)) == n * t,
                "unit-column trace identity")
        hs2 = sum(qabs2(omat[a][b])
                  for a in range(n) for b in range(n))
        lower = (n - 2) ** 2 * n * t * (n - t)
        require(hs2 >= lower, "aspect-ratio Hilbert--Schmidt lower bound")

        gamma = [qdet(1, seed, a, n, t) for a in range(n)]
        lhs = qinner(gamma, qmat_vec(omat, gamma))
        rgamma = qmat_vec(rmat, gamma)
        rhs = qi((n - 2) * (qnorm2(rgamma) - t * qnorm2(gamma)))
        require(lhs == rhs and lhs[1] == 0,
                "coefficient-specific aspect-ratio quadratic identity")
        cases.append([n, t, seed])

    sharp_cases = []
    for n, t in [(4, 1), (8, 3), (8, 4), (16, 5), (16, 8)]:
        had = sylvester_hadamard(n)
        rmat = [[qi(had[j][a]) for a in range(n)] for j in range(t)]
        pmat = row_gram(rmat)
        p2 = qmat_mul(pmat, pmat)
        qmat_require_equal(p2,
                           [[qscale(pmat[a][b], n) for b in range(n)]
                            for a in range(n)],
                           "tight-frame projector identity")
        omat = [[qscale(qsub(pmat[a][b], qi(t if a == b else 0)),
                            n - 2)
                 for b in range(n)] for a in range(n)]
        hs2 = sum(qabs2(entry) for row in omat for entry in row)
        require(hs2 == (n - 2) ** 2 * n * t * (n - t),
                "tight-frame HS equality")

        top = [qconj(rmat[0][a]) for a in range(n)]
        require(qmat_vec(pmat, top) == [qscale(x, n) for x in top],
                "tight-frame top eigenvector")
        require(qmat_vec(omat, top)
                == [qscale(x, (n - 2) * (n - t)) for x in top],
                "off-Gram top eigenvalue")

        projection = [[qsub(qi(int(a == b)),
                            qscale(pmat[a][b], Fraction(1, n)))
                       for b in range(n)] for a in range(n)]
        null = None
        for col in range(n):
            candidate = [projection[a][col] for a in range(n)]
            if qnorm2(candidate) != 0:
                null = candidate
                break
        require(null is not None, "tight-frame null vector exists")
        require(qmat_vec(pmat, null) == [qi() for _ in range(n)],
                "tight-frame null eigenvector")
        require(qmat_vec(omat, null)
                == [qscale(x, -(n - 2) * t) for x in null],
                "off-Gram null eigenvalue")
        sharp_cases.append([n, t])
    return {
        "checks": CHECKS - start,
        "generic_cases": cases,
        "tight_frame_cases": sharp_cases,
    }


def check_same_source_blocks() -> dict:
    start = CHECKS
    cases = []
    for n, r, t, seed in [
        (6, 2, 2, 0), (8, 2, 3, 1), (12, 3, 4, 2), (12, 2, 3, 3)
    ]:
        require(n % r == 0 and n >= 2 * r,
                "same-source block dimensions")
        rmat = [[phase(seed, j, a) for a in range(n)]
                for j in range(t)]
        bmat = [[qi(int(a // r == b // r)) for b in range(n)]
                for a in range(n)]
        amat = [[qi(int(a // r != b // r)) for b in range(n)]
                for a in range(n)]
        a2 = qmat_mul(amat, amat)
        expected_a2 = [
            [qadd(qi(n - 2 * r), qscale(bmat[a][b], r))
             for b in range(n)]
            for a in range(n)
        ]
        qmat_require_equal(a2, expected_a2,
                           "same-source mask-square identity")

        gram = qmat(n, n)
        for j in range(t):
            mmat = [[qmul(amat[g][a], rmat[j][a])
                     for a in range(n)] for g in range(n)]
            for a in range(n):
                for b in range(n):
                    gram[a][b] = qadd(
                        gram[a][b],
                        qsum(qmul(qconj(mmat[g][a]), mmat[g][b])
                             for g in range(n)),
                    )
        pmat = row_gram(rmat)
        block_p = [[pmat[a][b] if a // r == b // r else qi()
                    for b in range(n)] for a in range(n)]
        formula = [[qadd(qscale(pmat[a][b], n - 2 * r),
                         qscale(block_p[a][b], r))
                    for b in range(n)] for a in range(n)]
        qmat_require_equal(gram, formula, "same-source Gram identity")

        omat = qmat(n, n)
        for a in range(n):
            require(gram[a][a] == qi((n - r) * t),
                    "same-source Gram diagonal")
            for b in range(n):
                omat[a][b] = gram[a][b] if a != b else qi()
                delta = qi(t if a == b else 0)
                expected = qadd(
                    qscale(qsub(pmat[a][b], delta), n - 2 * r),
                    qscale(qsub(block_p[a][b],
                                delta if a // r == b // r else qi()), r),
                )
                require(omat[a][b] == expected,
                        "same-source off-Gram identity")
        cases.append([n, r, t, seed])

    witness_cases = []
    for n, r, t in [(8, 2, 3), (16, 2, 4), (16, 4, 4)]:
        had = sylvester_hadamard(n)
        rmat = [[qi(had[j][a]) for a in range(n)] for j in range(t)]
        pmat = row_gram(rmat)
        block_p = [[pmat[a][b] if a // r == b // r else qi()
                    for b in range(n)] for a in range(n)]
        omat = [[
            qadd(
                qscale(qsub(pmat[a][b], qi(t if a == b else 0)),
                       n - 2 * r),
                qscale(qsub(block_p[a][b],
                            qi(t if a == b else 0)), r),
            ) for b in range(n)
        ] for a in range(n)]
        top = [qconj(rmat[0][a]) for a in range(n)]
        image = qmat_vec(omat, top)
        lower = (n - 2 * r) * (n - t) - r * t
        require(lower >= 0, "same-source witness lower bound nonnegative")
        require(qmat_vec(pmat, top) == [qscale(x, n) for x in top],
                "same-source top frame eigenvector")
        block_energy = qinner(top, qmat_vec(block_p, top))
        require(block_energy[1] == 0 and block_energy[0] >= 0,
                "same-source block energy nonnegative")
        rayleigh = qinner(top, image)
        expected_rayleigh = (
            (n - 2 * r) * (n - t) * qnorm2(top)
            + r * (block_energy[0] - t * qnorm2(top))
        )
        require(rayleigh == qi(expected_rayleigh),
                "same-source Rayleigh decomposition")
        require(rayleigh[0] >= lower * qnorm2(top),
                "same-source corrected Rayleigh lower bound")
        require(qnorm2(image) >= lower * lower * qnorm2(top),
                "same-source operator lower-bound witness")
        witness_cases.append([n, r, t, lower])
    return {
        "checks": CHECKS - start,
        "identity_cases": cases,
        "lower_bound_witnesses": witness_cases,
    }


def check_ultra_crt() -> dict:
    start = CHECKS
    counterexample = {"h": 2, "u1": 4, "u2": 4, "m1": 1, "m2": 3}
    ce_r1 = (-counterexample["h"]
             * pow(counterexample["m1"], -1, counterexample["u1"])) \
        % counterexample["u1"]
    ce_r2 = (-counterexample["h"]
             * pow(counterexample["m2"], -1, counterexample["u2"])) \
        % counterexample["u2"]
    ce_g = gcd(counterexample["u1"], counterexample["u2"])
    require(ce_r1 == ce_r2
            and (counterexample["m1"] - counterexample["m2"]) % ce_g != 0,
            "missing-h-primitivity CRT counterexample")
    cases = 0
    compatible = 0
    physically_primitive = 0
    occupancy_cases = 0
    for h in range(1, 4):
        for u1 in range(2, 12):
            for u2 in range(2, 12):
                g = gcd(u1, u2)
                ell = lcm(u1, u2)
                for m1 in range(1, 11):
                    if gcd(m1, u1) != 1:
                        continue
                    for m2 in range(1, 11):
                        if gcd(m2, u2) != 1:
                            continue
                        r1 = (-h * pow(m1, -1, u1)) % u1
                        r2 = (-h * pow(m2, -1, u2)) % u2
                        reduced_g = g // gcd(g, h)
                        condition = (m1 - m2) % reduced_g == 0
                        require(((r1 - r2) % g == 0) == condition,
                                "general ultra CRT compatibility criterion")
                        if (gcd(u1, h * m1) == 1
                                and gcd(u2, h * m2) == 1):
                            require(condition == ((m1 - m2) % g == 0),
                                    "physically primitive ultra criterion")
                            physically_primitive += 1
                        solutions = [j for j in range(ell)
                                     if j % u1 == r1 and j % u2 == r2]
                        require(len(solutions) == (1 if condition else 0),
                                "ultra CRT unique-class count")
                        cases += 1
                        if not condition:
                            continue
                        compatible += 1
                        residue = solutions[0]
                        require((m1 * residue + h) % u1 == 0
                                and (m2 * residue + h) % u2 == 0,
                                "ultra CRT reconstructed residue")
                        intervals = [
                            (-7, min(6, ell - 1)),
                            (0, min(8, ell - 1)),
                            (5, ell + 2),
                        ]
                        for left, length in intervals:
                            if length <= 0:
                                continue
                            brute = sum(
                                1 for j in range(left + 1, left + length + 1)
                                if j % u1 == r1 and j % u2 == r2
                            )
                            floor_count = (
                                (left + length - residue) // ell
                                - (left - residue) // ell
                            )
                            require(brute == floor_count,
                                    "ultra CRT interval floor formula")
                            if ell > length:
                                require(brute in (0, 1),
                                        "short-orbit CRT occupancy")
                            occupancy_cases += 1
    return {
        "checks": CHECKS - start,
        "parameter_cases": cases,
        "compatible_cases": compatible,
        "physically_primitive_cases": physically_primitive,
        "missing_h_primitivity_counterexample": counterexample,
        "interval_cases": occupancy_cases,
    }


def check_short_orbit_congruence_operator() -> dict:
    start = CHECKS
    cases = []
    for length, row_count, h in [(4, 5, 1), (6, 7, 1), (8, 9, 1)]:
        left = length + 2
        interval = list(range(left + 1, left + length + 1))
        rows = [m for m in range(2, 3 * row_count + 5)
                if gcd(m, h) == 1][:row_count]
        atoms = []
        for j in interval:
            for m in rows:
                u = m * j + h
                require(u > length and gcd(u, h * m) == 1,
                        "terminal short-orbit atom primitivity")
                atoms.append((m, u))
        incidence = {
            (j, atom): int((atom[0] * j + h) % atom[1] == 0)
            for j in interval for atom in atoms
        }
        for atom in atoms:
            require(sum(incidence[j, atom] for j in interval) <= 1,
                    "short-orbit atom hit two times")
        occupancies = {
            j: sum(incidence[j, atom] for atom in atoms)
            for j in interval
        }
        delta = max(occupancies.values())
        require(delta == row_count,
                "terminal short-orbit occupancy multiplicity")
        for j1 in interval:
            for j2 in interval:
                gram = sum(incidence[j1, atom] * incidence[j2, atom]
                           for atom in atoms)
                require(gram == (occupancies[j1] if j1 == j2 else 0),
                        "short-orbit row Gram diagonalization")

        coeff = {atom: qdet(15, length, atom[0], atom[1]) for atom in atoms}
        output = {
            j: qsum(qscale(coeff[atom], incidence[j, atom]) for atom in atoms)
            for j in interval
        }
        output_energy = sum(qabs2(value) for value in output.values())
        input_energy = sum(qabs2(value) for value in coeff.values())
        require(output_energy <= delta * input_energy,
                "sharp short-orbit congruence large sieve")

        maximizing_j = max(interval, key=lambda j: occupancies[j])
        witness = {atom: qi(incidence[maximizing_j, atom]) for atom in atoms}
        witness_input = sum(qabs2(value) for value in witness.values())
        witness_output = sum(
            qabs2(qsum(qscale(witness[atom], incidence[j, atom])
                       for atom in atoms))
            for j in interval
        )
        require(witness_output == delta * witness_input,
                "short-orbit operator constant sharpness")
        cases.append([length, row_count, len(atoms), delta])
    return {"checks": CHECKS - start, "cases": cases}


def first_nonmultiples(q: int, start: int, count: int) -> list[int]:
    out = []
    value = start
    while len(out) < count:
        if value % q != 0:
            out.append(value)
        value += 1
    return out


def residue_max(values: list[int], q: int) -> int:
    counts = {r: 0 for r in range(1, q)}
    for value in values:
        require(value % q != 0, "incomplete set contains zero residue")
        counts[value % q] += 1
    return max(counts.values())


def check_incomplete_plancherel_saturation() -> dict:
    start = CHECKS
    set_cases = 0
    for q in [3, 5, 7, 11, 13]:
        for jlen in range(1, 2 * q + 2):
            for extra in [0, 2, q]:
                slen = jlen + extra
                jset = first_nonmultiples(q, 2 - q, jlen)
                sset = first_nonmultiples(q, q + 1, slen)
                nuj = residue_max(jset, q)
                nus = residue_max(sset, q)
                require(nuj >= ceil_div(jlen, q - 1)
                        and nus >= ceil_div(slen, q - 1),
                        "nonzero-residue pigeonhole bound")
                rms2 = Fraction(nuj * nus * q, jlen * slen)
                require(rms2 * jlen >= 1,
                        "sharp half-orbit RMS lower barrier")
                set_cases += 1

    envelope_cases = 0
    for a in range(2, 11):
        for b in range(a, 13):
            jlen = a * a
            slen = b * b
            q0 = a * b
            optimum = (Fraction(1, a) + Fraction(1, b)) ** 2
            at_optimum = (
                Fraction(1, q0) + Fraction(1, jlen)
                + Fraction(1, slen) + Fraction(q0, jlen * slen)
            )
            require(at_optimum == optimum,
                    "continuous incomplete-Plancherel optimum")
            for qvalue in range(1, 2 * q0 + 2):
                majorant = (
                    Fraction(1, qvalue) + Fraction(1, jlen)
                    + Fraction(1, slen)
                    + Fraction(qvalue, jlen * slen)
                )
                defect = Fraction((qvalue - q0) ** 2,
                                  qvalue * jlen * slen)
                require(majorant == optimum + defect,
                        "incomplete-Plancherel square completion")
                require(majorant >= optimum,
                        "incomplete-Plancherel saturation lower bound")
                envelope_cases += 1
    return {
        "checks": CHECKS - start,
        "residue_set_cases": set_cases,
        "continuous_envelope_cases": envelope_cases,
    }


def primitive_root(q: int) -> int:
    if q == 3:
        return 2
    if q == 5:
        return 2
    raise RuntimeError("certificate character table supports q=3,5 only")


def root_unit(order: int, exponent: int) -> QI:
    if order == 1:
        return qi(1)
    if order == 2:
        return qi(1 if exponent % 2 == 0 else -1)
    if order == 4:
        return [qi(1), qi(0, 1), qi(-1), qi(0, -1)][exponent % 4]
    raise RuntimeError("non-Gaussian root of unity requested")


def character_table(q: int) -> list[dict[int, QI]]:
    order = q - 1
    generator = primitive_root(q)
    logs = {}
    value = 1
    for exponent in range(order):
        logs[value] = exponent
        value = value * generator % q
    return [
        {x: root_unit(order, r * logs[x]) for x in range(1, q)}
        for r in range(order)
    ]


def centered(values: list[QI]) -> list[QI]:
    mean = qscale(qsum(values), Fraction(1, len(values)))
    return [qsub(value, mean) for value in values]


def check_product_slope_spectrum() -> dict:
    start = CHECKS
    cases = 0
    character_checks = 0
    saturation_cases = 0
    for q in [3, 5]:
        chars = character_table(q)
        order = q - 1
        for r1 in range(order):
            for r2 in range(order):
                inner = qsum(qmul(chars[r1][x], qconj(chars[r2][x]))
                             for x in range(1, q))
                require(inner == qi(order if r1 == r2 else 0),
                        "multiplicative-character orthogonality")
        for seed in [0, 1, 2]:
            f = centered([qdet(20, q, seed, x) for x in range(q)])
            g = centered([qdet(21, seed, q, x) for x in range(q)])
            require(qsum(f) == qi() and qsum(g) == qi(),
                    "finite-field vectors were not centered")
            for h in range(1, q):
                rvals = {}
                for s in range(1, q):
                    sinv = pow(s, -1, q)
                    for a in range(1, q):
                        rvals[s, a] = qsum(
                            qmul(f[d], g[(sinv * (a * d + h)) % q])
                            for d in range(q)
                        )
                energies = []
                for r, char in enumerate(chars):
                    energy = sum(
                        qabs2(qsum(qmul(rvals[s, a], qconj(char[a]))
                                   for a in range(1, q)))
                        for s in range(1, q)
                    )
                    if r == 0:
                        formula = q * q * qabs2(f[0]) * (
                            sum(qabs2(value) for value in g) - qabs2(g[0])
                        )
                    else:
                        fchar = qsum(qmul(f[d], char[d])
                                     for d in range(1, q))
                        gchar = qsum(qmul(g[u], qconj(char[u]))
                                     for u in range(1, q))
                        formula = qabs2(fchar) * (
                            q * sum(qabs2(value) for value in g)
                            - qabs2(gchar)
                        )
                    require(energy == formula,
                            "product-slope explicit character energy")
                    energies.append(energy)
                    character_checks += 1

                direct_projective_energy = sum(
                    qabs2(rvals[s, a])
                    for s in range(1, q) for a in range(1, q)
                )
                require(Fraction(sum(energies), order)
                        == direct_projective_energy,
                        "average character versus projective energy")

                bvec = {ell: qdet(22, seed, h, ell)
                        for ell in range(1, q)}
                output_energy = 0
                for j in range(1, q):
                    for s in range(1, q):
                        value = qsum(qmul(bvec[ell],
                                          rvals[s, (ell * j) % q])
                                     for ell in range(1, q))
                        output_energy += qabs2(value)
                spectral_energy = 0
                for r, char in enumerate(chars):
                    bhat_bar = qsum(qmul(bvec[ell], char[ell])
                                    for ell in range(1, q))
                    spectral_energy += qabs2(bhat_bar) * energies[r]
                require(Fraction(output_energy)
                        == Fraction(spectral_energy, order),
                        "product-slope character spectral identity")

                for r, char in enumerate(chars):
                    witness = {ell: qconj(char[ell])
                               for ell in range(1, q)}
                    witness_output = 0
                    for j in range(1, q):
                        for s in range(1, q):
                            value = qsum(qmul(witness[ell],
                                              rvals[s, (ell * j) % q])
                                         for ell in range(1, q))
                            witness_output += qabs2(value)
                    witness_norm = sum(qabs2(value)
                                       for value in witness.values())
                    require(Fraction(witness_output, witness_norm)
                            == energies[r],
                            "product-slope operator eigencharacter")
                    character_checks += 1
                cases += 1
        # A nonprincipal character placed on the f-leg concentrates the
        # entire spectrum in one character and realizes the q-1
        # average-to-maximum gap.
        for target in range(1, order):
            target_char = chars[target]
            f = [qi()] + [qconj(target_char[d]) for d in range(1, q)]
            g = [qsub(qi(1), qi(Fraction(1, q)))] \
                + [qi(Fraction(-1, q)) for _ in range(1, q)]
            require(qsum(f) == qi() and qsum(g) == qi(),
                    "character-concentrated vectors were not centered")
            h = 1
            rvals = {}
            for s in range(1, q):
                sinv = pow(s, -1, q)
                for a in range(1, q):
                    rvals[s, a] = qsum(
                        qmul(f[d], g[(sinv * (a * d + h)) % q])
                        for d in range(q)
                    )
            energies = []
            for char in chars:
                energies.append(sum(
                    qabs2(qsum(qmul(rvals[s, a], qconj(char[a]))
                               for a in range(1, q)))
                    for s in range(1, q)
                ))
            require(energies[target] > 0
                    and all(energy == 0 for r, energy in enumerate(energies)
                            if r != target),
                    "product-slope one-character spectral concentration")
            average_energy = Fraction(sum(energies), order)
            require(max(energies) == order * average_energy,
                    "product-slope average-to-maximum factor")
            saturation_cases += 1
    return {
        "checks": CHECKS - start,
        "field_seed_shift_cases": cases,
        "character_energy_and_witness_checks": character_checks,
        "average_to_maximum_saturation_cases": saturation_cases,
    }


def check_alias_ladder() -> dict:
    start = CHECKS
    bbound = 1000
    moduli = [5, 7, 11, 13]
    prefix_data = []
    for count in range(1, 5):
        packet = moduli[:count]
        modulus = 1
        for q in packet:
            modulus = lcm(modulus, q)
        alias_radius = bbound // modulus
        require(2 * alias_radius + 1
                == len(list(range(-alias_radius, alias_radius + 1))),
                "alias-ladder cardinality")
        for value in range(-bbound, bbound + 1):
            simultaneous = all(value % q == 0 for q in packet)
            joined = value % modulus == 0
            alias_sum = sum(1 for k in range(-alias_radius,
                                             alias_radius + 1)
                            if value == k * modulus)
            require(simultaneous == joined and alias_sum == int(joined),
                    "exact finite alias decomposition")
        prefix_data.append([count, modulus, alias_radius])
    require(prefix_data[2][1] < bbound < prefix_data[3][1],
            "three/four-modulus finite threshold")
    require(prefix_data[3][2] == 0,
            "four-modulus no-wrap certificate")

    for packet, bound in [([4, 6], 80), ([6, 10, 15], 120),
                          ([8, 12, 18], 160)]:
        modulus = 1
        for q in packet:
            modulus = lcm(modulus, q)
        radius = bound // modulus
        for value in range(-bound, bound + 1):
            lhs = all(value % q == 0 for q in packet)
            rhs = sum(1 for k in range(-radius, radius + 1)
                      if value == k * modulus)
            require(rhs == int(lhs), "noncoprime alias LCM identity")

    eta = Fraction(133, 400)
    beta = Fraction(267, 400)
    exponents = [1 - r * eta for r in range(1, 5)]
    require(exponents == [Fraction(267, 400), Fraction(134, 400),
                          Fraction(1, 400), Fraction(-33, 100)],
            "three/four-modulus exponent ladder")
    require(exponents[2] > 0 and exponents[3] < 0,
            "near-no-wrap versus strict no-wrap threshold")
    require(exponents[2] == beta - 2 * eta,
            "three-modulus alias versus orbit allowance")
    return {
        "checks": CHECKS - start,
        "bound": bbound,
        "coprime_prefixes": prefix_data,
        "exponents": [f"{x.numerator}/{x.denominator}" for x in exponents],
    }


def correlation_modulus(
    modulus: int, f: list[QI], g: list[QI], a: int, s: int, h: int
) -> QI:
    sinv = pow(s, -1, modulus)
    return qsum(qmul(f[d], g[(sinv * (a * d + h)) % modulus])
                for d in range(modulus))


def check_crt_lift_non_tensorization() -> dict:
    start = CHECKS
    lift_cases = []
    for p, cofactors in [(3, [2, 4, 5, 7, 8]),
                         (5, [2, 3, 4, 6, 7])]:
        for mprime in cofactors:
            if gcd(p, mprime) != 1:
                continue
            modulus = p * mprime
            h = 1
            fsmall = [qdet(30, p, mprime, x) for x in range(p)]
            gsmall = [qdet(31, mprime, p, x) for x in range(p)]
            flift = [fsmall[x % p] for x in range(modulus)]
            glift = [gsmall[x % p] for x in range(modulus)]
            mean_f = qscale(qsum(fsmall), Fraction(1, p))
            mean_g = qscale(qsum(gsmall), Fraction(1, p))
            require(qscale(qsum(flift), Fraction(1, modulus)) == mean_f
                    and qscale(qsum(glift), Fraction(1, modulus)) == mean_g,
                    "CRT coordinate lift preserves means")
            units = [x for x in range(1, modulus) if gcd(x, modulus) == 1]
            require(len(units) == (p - 1) * euler_phi(mprime),
                    "CRT unit count")
            for residue in range(1, p):
                require(sum(1 for x in units if x % p == residue)
                        == euler_phi(mprime),
                        "CRT unit reduction fiber")

            small = {(a, s): correlation_modulus(
                        p, fsmall, gsmall, a, s, h
                     ) for a in range(1, p) for s in range(1, p)}
            energy_m = 0
            for a in units:
                for s in units:
                    large_value = correlation_modulus(
                        modulus, flift, glift, a, s, h
                    )
                    require(large_value
                            == qscale(small[a % p, s % p], mprime),
                            "exact CRT lift of affine correlation")
                    centered_large = qsub(
                        large_value,
                        qscale(qmul(mean_f, mean_g), modulus),
                    )
                    energy_m += qabs2(centered_large)
            energy_p = sum(
                qabs2(qsub(value, qscale(qmul(mean_f, mean_g), p)))
                for value in small.values()
            )
            factor = mprime * mprime * euler_phi(mprime) ** 2
            require(energy_m == factor * energy_p,
                    "CRT lifted determinant-fiber energy")
            phi_m = len(units)
            require(Fraction(energy_m, modulus * modulus * phi_m * phi_m)
                    == Fraction(energy_p,
                                p * p * (p - 1) * (p - 1)),
                    "CRT normalized RMS non-tensorization")
            lift_cases.append([p, mprime, modulus])

    conservation_cases = 0
    for xsize in [50, 100, 399, 1000]:
        for jsize in [3, 7, 13, 25]:
            for product in [2, 5, 11, 31, 101, 401]:
                lhs = ((1 + Fraction(xsize, product))
                       * (1 + Fraction(product, jsize)))
                expanded = (1 + Fraction(xsize, product)
                            + Fraction(product, jsize)
                            + Fraction(xsize, jsize))
                require(lhs == expanded,
                        "alias-coverage product expansion")
                require(lhs >= Fraction(xsize, jsize),
                        "alias-coverage conservation inequality")
                conservation_cases += 1
    return {
        "checks": CHECKS - start,
        "crt_lift_cases": lift_cases,
        "alias_coverage_cases": conservation_cases,
    }


def check_integer_line_incidence() -> dict:
    start = CHECKS
    box_cases = []
    for h, amax, smax, xmax, ymax in [
        (1, 8, 7, 9, 11), (2, 9, 8, 10, 13), (3, 10, 7, 11, 14)
    ]:
        lines = [(a, s) for a in range(1, amax + 1)
                 for s in range(1, smax + 1) if gcd(a, s) == 1]
        points = [(x, y) for x in range(1, xmax + 1)
                  for y in range(1, ymax + 1)]
        point_set = set(points)
        incidence = {
            (line, point): int(line[1] * point[1] - line[0] * point[0] == h)
            for line in lines for point in points
        }
        line_points = {
            line: [point for point in points if incidence[line, point]]
            for line in lines
        }
        point_lines = {
            point: [line for line in lines if incidence[line, point]]
            for point in points
        }
        multiplicity = {point: len(point_lines[point]) for point in points}

        gram = {}
        for i, line1 in enumerate(lines):
            a, s = line1
            for k, line2 in enumerate(lines):
                ap, sp = line2
                common = sum(incidence[line1, point]
                             * incidence[line2, point] for point in points)
                gram[i, k] = common
                if i == k:
                    require(common == len(line_points[line1]),
                            "integer line Gram diagonal")
                else:
                    delta = ap * s - a * sp
                    require(delta != 0,
                            "distinct positive primitive lines were parallel")
                    xnum = h * (sp - s)
                    ynum = h * (ap - a)
                    integral = xnum % delta == 0 and ynum % delta == 0
                    intersection = (xnum // delta, ynum // delta)
                    expected = int(integral and intersection in point_set)
                    require(common == expected,
                            "integer line intersection formula")

        for i, line in enumerate(lines):
            row_sum = sum(gram[i, k] for k in range(len(lines)))
            direct = sum(multiplicity[point] for point in line_points[line])
            require(row_sum == direct,
                    "line-Gram Schur row-sum identity")
            plist = line_points[line]
            a, s = line
            occupancy_bound = 1 + min((xmax - 1) // s,
                                      (ymax - 1) // a)
            require(len(plist) <= occupancy_bound,
                    "fixed-line box occupancy bound")
            for p1 in plist:
                for p2 in plist:
                    dx = p2[0] - p1[0]
                    dy = p2[1] - p1[1]
                    require(dx % s == 0 and dy % a == 0
                            and dx // s == dy // a,
                            "fixed-line point-step identity")

        for point in points:
            llist = point_lines[point]
            if llist:
                require(h % gcd(point[0], point[1]) == 0,
                        "point incidence gcd obstruction")
            step_a = point[1] // gcd(point[0], point[1])
            step_s = point[0] // gcd(point[0], point[1])
            coefficient_bound = 1 + min((amax - 1) // step_a,
                                        (smax - 1) // step_s)
            require(len(llist) <= coefficient_bound,
                    "fixed-point coefficient occupancy bound")
            for l1 in llist:
                for l2 in llist:
                    da = l2[0] - l1[0]
                    ds = l2[1] - l1[1]
                    require(da % step_a == 0 and ds % step_s == 0
                            and da // step_a == ds // step_s,
                            "fixed-point coefficient-step identity")

        fvec = {point: qdet(40, h, point[0], point[1]) for point in points}
        image = {
            line: qsum(fvec[point] for point in line_points[line])
            for line in lines
        }
        image_energy = sum(qabs2(value) for value in image.values())
        fenergy = sum(qabs2(value) for value in fvec.values())
        row_bound = max(
            sum(multiplicity[point] for point in line_points[line])
            for line in lines
        )
        require(image_energy <= row_bound * fenergy,
                "finite line-incidence Schur bound")

        zvec = {line: qdet(41, h, line[0], line[1]) for line in lines}
        dual = {
            point: qsum(zvec[line] for line in point_lines[point])
            for point in points
        }
        dual_energy = sum(qabs2(value) for value in dual.values())
        zenergy = sum(qabs2(value) for value in zvec.values())
        dual_bound = max(
            sum(len(line_points[line]) for line in point_lines[point])
            for point in points
        )
        require(dual_energy <= dual_bound * zenergy,
                "finite dual line-incidence Schur bound")
        box_cases.append([h, len(lines), len(points),
                          sum(multiplicity.values())])

    sharp_cases = []
    for tvalue in [3, 5, 8]:
        for scount in [4, 7, 10]:
            h = 1
            point = (1, tvalue)
            lines = [(s * tvalue - h, s) for s in range(1, scount + 1)]
            require(all(gcd(a, s) == 1 and s * point[1] - a * point[0] == h
                        for a, s in lines),
                    "sharp ambient incidence family")
            require(len(set(lines)) == scount,
                    "sharp ambient coefficient multiplicity")
            sharp_cases.append([tvalue, scount])
    return {
        "checks": CHECKS - start,
        "box_cases": box_cases,
        "sharp_point_multiplicity_cases": sharp_cases,
    }


def check_source_constraints() -> dict:
    start = CHECKS
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    float_nodes = [node for node in ast.walk(tree)
                   if isinstance(node, ast.Constant)
                   and isinstance(node.value, float)]
    assert_nodes = [node for node in ast.walk(tree)
                    if isinstance(node, ast.Assert)]
    division_nodes = [node for node in ast.walk(tree)
                      if isinstance(node, ast.BinOp)
                      and isinstance(node.op, ast.Div)]
    import_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            import_names.append(node.module or "")
    require(not float_nodes, "certificate source contains a float literal")
    require(not assert_nodes, "certificate source contains assert")
    require(not division_nodes, "certificate source contains true division")
    require(not any(name == "random" or name.startswith("random.")
                    for name in import_names),
            "certificate source imports random")
    return {"checks": CHECKS - start}


def main() -> None:
    results = {
        "aspect_ratio_gram": check_aspect_ratio_gram(),
        "same_source_blocks": check_same_source_blocks(),
        "ultra_crt": check_ultra_crt(),
        "short_orbit_congruence": check_short_orbit_congruence_operator(),
        "incomplete_plancherel": check_incomplete_plancherel_saturation(),
        "product_slope_spectrum": check_product_slope_spectrum(),
        "alias_ladder": check_alias_ladder(),
        "crt_non_tensorization": check_crt_lift_non_tensorization(),
        "integer_line_incidence": check_integer_line_incidence(),
        "source_constraints": check_source_constraints(),
    }
    claims = {
        "finite_aspect_ratio_gram_identity": True,
        "finite_aspect_ratio_hs_bound_and_sharpness": True,
        "finite_same_source_block_identity": True,
        "finite_same_source_lower_bound_witness": True,
        "finite_ultra_crt_compatibility_and_occupancy": True,
        "finite_short_orbit_congruence_operator": True,
        "finite_incomplete_plancherel_saturation": True,
        "finite_product_slope_character_spectrum": True,
        "finite_three_four_modulus_alias_ladder": True,
        "finite_crt_lift_non_tensorization": True,
        "finite_integer_line_incidence_counts": True,
        "uses_floating_point": False,
        "uses_random_inputs": False,
        "proves_uniform_physical_operator_gate": False,
        "proves_coefficient_specific_Mobius_gate": False,
        "proves_affine_Mobius_or_Chowla_cancellation": False,
        "proves_physical_same_ultra_asymptotic": False,
        "proves_joint_three_or_four_modulus_dispersion": False,
        "proves_full_crt_tensorization": False,
        "proves_low_coordinate_crt_mode_suppression": False,
        "proves_asymptotic_integer_incidence_conductor": False,
        "proves_Q3_column_energy_gate": False,
        "proves_zero_frequency_flatness": False,
        "proves_positivity": False,
        "proves_Hardy_Littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    source = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    payload = {
        "paper": "TPC-35",
        "certificate_version": 1,
        "arithmetic": "integer, Fraction, and Gaussian rational only",
        "check_total": CHECKS,
        "results": results,
        "claims": claims,
        "normalized_source_sha256": sha256(source).hexdigest(),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True).encode("utf-8")
    payload["certificate_digest"] = sha256(canonical).hexdigest()
    output = Path(__file__).with_name("tpc35_certificate.json")
    output.write_bytes((json.dumps(payload, indent=2, sort_keys=True,
                                   ensure_ascii=True) + "\n").encode("utf-8"))
    print(
        "TPC-35 exact certificate:"
        f" {CHECKS} checks;"
        f" digest {payload['certificate_digest']};"
        f" wrote {output.name}"
    )


if __name__ == "__main__":
    main()
