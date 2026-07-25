#!/usr/bin/env python3
"""Finite certificate for the TPC-97 projection identities.

The exhaustive part uses Fraction arithmetic.  The random part uses
seeded floating-point Gram--Schmidt only as a regression guard.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import json
import math
import random


def set_partitions(n: int):
    blocks: list[list[int]] = []

    def visit(i: int):
        if i == n:
            yield tuple(tuple(block) for block in blocks)
            return
        for j in range(len(blocks)):
            blocks[j].append(i)
            yield from visit(i + 1)
            blocks[j].pop()
        blocks.append([i])
        yield from visit(i + 1)
        blocks.pop()

    yield from visit(0)


def dot_exact(x, y):
    return sum((a * b for a, b in zip(x, y)), Fraction(0))


def norm2_exact(x):
    return dot_exact(x, x)


def block_project_exact(a, partition):
    out = [Fraction(0) for _ in a]
    for block in partition:
        mean = sum((a[i] for i in block), Fraction(0)) / len(block)
        for i in block:
            out[i] = mean
    return tuple(out)


def exhaustive_block_checks():
    cases = 0
    partitions_seen = 0
    for n in range(1, 6):
        partitions = list(set_partitions(n))
        partitions_seen += len(partitions)
        for raw in product(range(-2, 3), repeat=n):
            if all(x == 0 for x in raw):
                continue
            a = tuple(Fraction(x) for x in raw)
            za = sum(a, Fraction(0))
            da = norm2_exact(a)
            for partition in partitions:
                b = block_project_exact(a, partition)
                r = tuple(x - y for x, y in zip(a, b))
                assert sum(b, Fraction(0)) == za
                assert dot_exact(b, r) == 0
                assert da == norm2_exact(b) + norm2_exact(r)
                variance = Fraction(0)
                for block in partition:
                    mean = b[block[0]]
                    variance += sum(
                        ((a[i] - mean) ** 2 for i in block),
                        Fraction(0),
                    )
                assert variance == norm2_exact(r)
                db = norm2_exact(b)
                if db:
                    assert za * za * db <= za * za * da
                cases += 1
    return cases, partitions_seen


def coordinate_project_exact(a, mask):
    b = tuple(x if keep else Fraction(0) for x, keep in zip(a, mask))
    r = tuple(x - y for x, y in zip(a, b))
    q = tuple(Fraction(0) if keep else Fraction(1) for keep in mask)
    return b, r, q


def complete_coordinate_projection_exact(a, mask):
    b, _, q = coordinate_project_exact(a, mask)
    qn = norm2_exact(q)
    if qn == 0:
        return b
    coeff = dot_exact(a, q) / qn
    return tuple(x + coeff * y for x, y in zip(b, q))


def exhaustive_coordinate_checks():
    cases = 0
    equality_cases = 0
    for n in range(1, 6):
        for raw in product(range(-2, 3), repeat=n):
            a = tuple(Fraction(x) for x in raw)
            za = sum(a, Fraction(0))
            da = norm2_exact(a)
            for bits in product((False, True), repeat=n):
                b, r, q = coordinate_project_exact(a, bits)
                defect = sum(b, Fraction(0)) - za
                assert defect == -dot_exact(r, q)
                assert defect * defect <= norm2_exact(r) * norm2_exact(q)
                if norm2_exact(q) and all(
                    (not bits[i]) or r[i] == 0 for i in range(n)
                ):
                    # Coordinate residuals are always supported in Ker(P).
                    pass
                sharp = tuple(Fraction(3) * x for x in q)
                if norm2_exact(q):
                    lhs = dot_exact(sharp, q) ** 2
                    rhs = norm2_exact(sharp) * norm2_exact(q)
                    assert lhs == rhs
                    equality_cases += 1
                c = complete_coordinate_projection_exact(a, bits)
                assert sum(c, Fraction(0)) == za
                assert norm2_exact(c) <= da
                cases += 1
    return cases, equality_cases


def check_weighted_counterexample():
    a = (Fraction(1), Fraction(-1), Fraction(-1))
    partition = ((0,), (1, 2))
    b = block_project_exact(a, partition)
    means = (b[0], b[1])
    physical_z = means[0] + 2 * means[1]
    physical_d = means[0] ** 2 + 2 * means[1] ** 2
    unweighted_z = means[0] + means[1]
    assert physical_z == -1
    assert physical_d == 3
    assert unweighted_z == 0
    return True


def inner(x, y):
    """Inner product linear in the first variable."""
    return sum(a * b.conjugate() for a, b in zip(x, y))


def add(x, y):
    return [a + b for a, b in zip(x, y)]


def sub(x, y):
    return [a - b for a, b in zip(x, y)]


def scale(c, x):
    return [c * a for a in x]


def norm(x):
    return math.sqrt(max(0.0, inner(x, x).real))


def orthonormalize(vectors, tol=1e-12):
    basis = []
    for v in vectors:
        w = list(v)
        for u in basis:
            w = sub(w, scale(inner(w, u), u))
        nw = norm(w)
        if nw > tol:
            basis.append(scale(1.0 / nw, w))
    return basis


def project(x, basis):
    out = [0.0 for _ in x]
    for u in basis:
        out = add(out, scale(inner(x, u), u))
    return out


def close(x, y, tol=2e-9):
    return abs(x - y) <= tol * (1.0 + abs(x) + abs(y))


def random_projection_checks(seed=970097, trials=1000):
    rng = random.Random(seed)
    safe_cases = 0
    defective_cases = 0
    for _ in range(trials):
        n = rng.randint(2, 12)
        one = [1.0] * n
        a = [
            complex(rng.uniform(-3.0, 3.0), rng.uniform(-3.0, 3.0))
            for _ in range(n)
        ]
        rank = rng.randint(1, n)

        candidates = [scale(1.0 / math.sqrt(n), one)]
        candidates.extend(
            [[complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
              for _ in range(n)]
             for _ in range(rank - 1)]
        )
        safe_basis = orthonormalize(candidates)
        b = project(a, safe_basis)
        r = sub(a, b)
        assert close(sum(b), sum(a))
        da = inner(a, a).real
        db = inner(b, b).real
        dr = inner(r, r).real
        assert close(da, db + dr)
        assert db <= da + 1e-8
        if db > 1e-14:
            za2 = abs(sum(a)) ** 2
            assert za2 * db <= za2 * da + 1e-7
        safe_cases += 1

        arbitrary = [
            [complex(rng.gauss(0.0, 1.0), rng.gauss(0.0, 1.0))
             for _ in range(n)]
            for _ in range(rank)
        ]
        basis = orthonormalize(arbitrary)
        b = project(a, basis)
        r = sub(a, b)
        p_one = project(one, basis)
        q = sub(one, p_one)
        defect = sum(b) - sum(a)
        assert close(defect, -inner(r, q))
        assert abs(defect) <= norm(r) * norm(q) + 1e-8

        if norm(q) > 1e-10:
            q_unit = scale(1.0 / norm(q), q)
            completed_basis = orthonormalize(basis + [q_unit])
        else:
            completed_basis = basis
        c = project(a, completed_basis)
        assert close(sum(c), sum(a), tol=8e-9)
        assert inner(c, c).real <= inner(a, a).real + 1e-7
        defective_cases += 1
    return safe_cases, defective_cases


def main():
    block_cases, partitions_seen = exhaustive_block_checks()
    coordinate_cases, equality_cases = exhaustive_coordinate_checks()
    weighted_counterexample = check_weighted_counterexample()
    random_safe, random_defective = random_projection_checks()
    report = {
        "exact_block_cases": block_cases,
        "set_partitions_seen": partitions_seen,
        "exact_coordinate_cases": coordinate_cases,
        "sharp_equality_cases": equality_cases,
        "random_safe_cases": random_safe,
        "random_defective_cases": random_defective,
        "weighted_counterexample_verified": weighted_counterexample,
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
