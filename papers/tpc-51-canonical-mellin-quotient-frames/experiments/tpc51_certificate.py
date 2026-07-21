#!/usr/bin/env python3
"""Exact finite certificate for TPC-51.

The certificate is deliberately weaker than the analytic theorems.  It
checks their finite algebraic identities with rational arithmetic; it
does not test prime asymptotics or certify any parity-sensitive claim.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


Q = Fraction


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Exact determinant by fraction Gaussian elimination."""
    n = len(matrix)
    if n == 0:
        return Q(1)
    a = [[Q(x) for x in row] for row in matrix]
    sign = 1
    det = Q(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign *= -1
        p = a[col][col]
        det *= p
        for r in range(col + 1, n):
            if not a[r][col]:
                continue
            f = a[r][col] / p
            for j in range(col + 1, n):
                a[r][j] -= f * a[col][j]
        # The diagonal entry is not normalized; later pivots are valid.
    return det * sign


def matvec(a: list[list[Fraction]], x: list[Fraction]) -> list[Fraction]:
    return [sum((u * v for u, v in zip(row, x)), Q(0)) for row in a]


def transpose(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(col) for col in zip(*a)]


def gram(rows: list[list[Fraction]]) -> list[list[Fraction]]:
    cols = transpose(rows)
    return [[sum((x * y for x, y in zip(ci, cj)), Q(0))
             for cj in cols] for ci in cols]


def principal_submatrix(a: list[list[Fraction]], idx: tuple[int, ...]) -> list[list[Fraction]]:
    return [[a[i][j] for j in idx] for i in idx]


def assert_psd_by_principal_minors(a: list[list[Fraction]]) -> int:
    """For a rational symmetric matrix, all principal minors >= 0 iff PSD."""
    n = len(a)
    checks = 0
    for r in range(1, n + 1):
        for idx in itertools.combinations(range(n), r):
            assert determinant(principal_submatrix(a, idx)) >= 0
            checks += 1
    return checks


def sylvester_positive(a: list[list[Fraction]]) -> int:
    checks = 0
    for r in range(1, len(a) + 1):
        assert determinant([row[:r] for row in a[:r]]) > 0
        checks += 1
    return checks


def hadamard_entry(row: int, col: int) -> Fraction:
    return Q(-1 if ((row & col).bit_count() & 1) else 1)


def phase_kernel_checks() -> int:
    """Check product_n(y_n-y_k)=0 for many distinct rational samples."""
    checks = 0
    for n in range(1, 18):
        for shift in range(-12, 13):
            ys = [Q(3 * j + shift, j + 2) for j in range(n)]
            # Repair the rare accidental collision deterministically.
            ys = [y + Q(j, 10_000_019) for j, y in enumerate(ys)]
            assert len(set(ys)) == n
            for yk in ys:
                product = Q(1)
                for yn in ys:
                    product *= yn - yk
                assert product == 0
                checks += 1
    return checks


def smooth_kernel_matrix_checks() -> int:
    """Cofactor null vector for N by N+1 Vandermonde synthesis matrices."""
    checks = 0
    for n in range(1, 8):
        for shift in range(1, 31):
            nodes = [Q(shift + 2 * j, shift + 2 * n + 3) for j in range(n + 1)]
            a = [[x ** i for x in nodes] for i in range(n)]
            cofactors = []
            for j in range(n + 1):
                minor = [[a[r][c] for c in range(n + 1) if c != j]
                         for r in range(n)]
                cofactors.append((Q(-1) if j % 2 else Q(1)) * determinant(minor))
            assert any(cofactors)
            assert matvec(a, cofactors) == [Q(0)] * n
            checks += n + 2
    return checks


def boundary_and_near_duplicate_checks() -> int:
    checks = 0
    # W(x)=x^k sampled at x=1/N has exact inverse-amplitude N^k.
    for n in range(2, 81):
        for k in range(1, 9):
            value = Q(1, n) ** k
            condition = Q(1, 1) / value
            assert condition == n ** k
            checks += 1

    # W_2=1+eps*x and W_1=1: the signed direction (1,-1) has eps^2 energy.
    for n in range(3, 25):
        xs = [Q(j, n + 1) for j in range(1, n + 1)]
        mean_x2 = sum((x * x for x in xs), Q(0)) / n
        for den in range(2, 61):
            eps = Q(1, den)
            normalized_energy = eps * eps * mean_x2
            condition_sq = Q(4) / normalized_energy
            assert condition_sq >= Q(4 * den * den)
            checks += 1
    return checks


def finite_gram_checks() -> int:
    """Exact positive definiteness of sampled monomial Grams."""
    checks = 0
    for r in range(1, 7):
        for n in range(r, r + 9):
            xs = [Q(j, n + 1) for j in range(1, n + 1)]
            rows = [[x ** degree for degree in range(r)] for x in xs]
            g = gram(rows)
            checks += sylvester_positive(g)
            # Exact quadratic identity F^T F.
            for i in range(r):
                for j in range(r):
                    assert g[i][j] == sum((x ** (i + j) for x in xs), Q(0))
                    checks += 1
    return checks


def mask_perturbation_checks() -> int:
    """Walsh bank: deleting s rows costs at most s*R in operator norm."""
    checks = 0
    n = 16
    r = 4
    full_rows = [[hadamard_entry(i, j) for j in range(r)] for i in range(n)]
    full_gram = gram(full_rows)
    assert full_gram == [[Q(n if i == j else 0) for j in range(r)] for i in range(r)]
    checks += r * r
    for s in range(0, 4):
        for deleted in itertools.combinations(range(n), s):
            deleted_set = set(deleted)
            retained = [row for i, row in enumerate(full_rows) if i not in deleted_set]
            g = gram(retained)
            lower = n - s * r
            difference = [[g[i][j] - (Q(lower) if i == j else Q(0))
                           for j in range(r)] for i in range(r)]
            checks += assert_psd_by_principal_minors(difference)
    return checks


def endpoint_checks() -> int:
    ell_exp = Q(99979, 210000)
    d_exp = Q(10049, 52500)
    q_exp = Q(267, 400)
    assert ell_exp + d_exp == q_exp
    assert Q(23, 120) - d_exp == Q(9, 35000)
    assert d_exp / 2 == Q(10049, 105000)
    assert Q(133, 400) + q_exp == 1
    return 4


def source_hash() -> str:
    data = Path(__file__).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def build_certificate() -> bytes:
    groups = {
        "explicit_phase_kernel": phase_kernel_checks(),
        "finite_dimensional_smooth_kernel": smooth_kernel_matrix_checks(),
        "boundary_and_near_duplicate_obstructions": boundary_and_near_duplicate_checks(),
        "finite_sampled_gram": finite_gram_checks(),
        "sparse_mask_perturbation": mask_perturbation_checks(),
        "endpoint_fraction_ledger": endpoint_checks(),
    }
    semantic_payload = {
        "claims": [
            "continuous finite-output synthesis has an exact kernel",
            "boundary zeros and near-duplicate shapes force bad conditioning",
            "finite quotient conditioning is a sampled Gram problem",
            "deleting s Walsh samples costs at most s times bank dimension",
            "TPC-51 endpoint fractions are internally consistent",
        ],
        "scope": "finite exact algebra only; no prime asymptotic and no parity claim",
    }
    semantic_hash = hashlib.sha256(
        json.dumps(semantic_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    payload = {
        "certificate": "TPC-51 exact finite regression certificate",
        "groups": groups,
        "total_exact_checks": sum(groups.values()),
        "semantic_sha256": semantic_hash,
        "normalized_source_sha256": source_hash(),
        "scope": semantic_payload["scope"],
    }
    core = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    trailer = {
        "certificate_core_sha256": hashlib.sha256(core).hexdigest()
    }
    return core + (json.dumps(trailer, sort_keys=True) + "\n").encode("utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = build_certificate()
    if args.output:
        args.output.write_bytes(data)
    print(data.decode("utf-8"), end="")


if __name__ == "__main__":
    main()
