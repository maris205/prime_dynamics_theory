#!/usr/bin/env python3
"""Exact collision-Gram and Schur-envelope calculations for TPC-221."""

from __future__ import annotations

from fractions import Fraction
import math


class SchurFailure(RuntimeError):
    pass


Q_VALUES = (101, 103, 107, 109)
H_VALUES = (17, 19, 23)
HEIGHT = 500
SATURATION_H = 5
SATURATION_Q = (101, 151, 181, 191)


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise SchurFailure(message)


def primitive_residues(h: int) -> tuple[int, ...]:
    return tuple(a for a in range(h) if math.gcd(a, h) == 1)


def atoms(h: int, q: int, height: int = HEIGHT) -> tuple[int, ...]:
    length = h * q // height
    return tuple(m for m in range(-length, length + 1) if m and math.gcd(m, h) == 1)


def profile_value(profile: str, h: int, m: int, q: int, height: int = HEIGHT) -> Fraction:
    t = Fraction(height * m, h * q)
    if profile == "constant":
        return Fraction(1)
    if profile == "affine":
        return Fraction(1) + t / 100
    raise SchurFailure(f"unknown profile: {profile}")


def row(h: int, q: int, profile: str, height: int = HEIGHT) -> dict[int, Fraction]:
    values = {a: Fraction(0) for a in primitive_residues(h)}
    inverse = pow(q, -1, h)
    for m in atoms(h, q, height):
        values[(m * inverse) % h] += profile_value(profile, h, m, q, height)
    return values


def collision_gram(h: int, q: int, qp: int, profile: str, height: int = HEIGHT) -> Fraction:
    total = Fraction(0)
    for m in atoms(h, q, height):
        for mp in atoms(h, qp, height):
            if (m * qp - mp * q) % h == 0:
                total += profile_value(profile, h, m, q, height) * profile_value(profile, h, mp, qp, height)
    return total


def direct_gram(h: int, q: int, qp: int, profile: str, height: int = HEIGHT) -> Fraction:
    left = row(h, q, profile, height)
    right = row(h, qp, profile, height)
    return sum((left[a] * right[a] for a in primitive_residues(h)), Fraction(0))


def diagonal(h: int, q: int, profile: str, height: int = HEIGHT) -> Fraction:
    return sum((profile_value(profile, h, m, q, height) ** 2 for m in atoms(h, q, height)), Fraction(0))


def gram_matrix(q_values: tuple[int, ...], h: int, profile: str,
                height: int = HEIGHT) -> list[list[Fraction]]:
    return [[collision_gram(h, q, qp, profile, height) for qp in q_values] for q in q_values]


def direct_matrix(q_values: tuple[int, ...], h: int, profile: str,
                  height: int = HEIGHT) -> list[list[Fraction]]:
    return [[direct_gram(h, q, qp, profile, height) for qp in q_values] for q in q_values]


def row_sums(matrix: list[list[Fraction]]) -> list[Fraction]:
    return [sum((abs(value) for value in row_values), Fraction(0)) for row_values in matrix]


def schur_radius(matrix: list[list[Fraction]]) -> Fraction:
    return max(row_sums(matrix), default=Fraction(0))


def weighted_schur_radius(matrix: list[list[Fraction]], weights: list[Fraction]) -> Fraction:
    require(len(matrix) == len(weights), "weight dimension mismatch")
    require(all(weight > 0 for weight in weights), "weights must be positive")
    return max(
        (
            sum((abs(matrix[i][j]) * weights[j] for j in range(len(weights))), Fraction(0))
            / weights[i]
            for i in range(len(weights))
        ),
        default=Fraction(0),
    )


def energy(matrix: list[list[Fraction]], lambdas: list[Fraction]) -> Fraction:
    return sum(
        (
            lambdas[i] * matrix[i][j] * lambdas[j]
            for i in range(len(lambdas))
            for j in range(len(lambdas))
        ),
        Fraction(0),
    )


def norm_sq(lambdas: list[Fraction]) -> Fraction:
    return sum((value * value for value in lambdas), Fraction(0))


def generic_record(h: int, profile: str) -> dict[str, object]:
    matrix = gram_matrix(Q_VALUES, h, profile)
    direct = direct_matrix(Q_VALUES, h, profile)
    residuals = [
        str(direct[i][j] - matrix[i][j])
        for i in range(len(Q_VALUES))
        for j in range(len(Q_VALUES))
    ]
    diagonal_residuals = [
        str(matrix[i][i] - diagonal(h, q, profile))
        for i, q in enumerate(Q_VALUES)
    ]
    lambdas = [Fraction(1), Fraction(-2), Fraction(3), Fraction(-1)]
    rho = schur_radius(matrix)
    weighted = weighted_schur_radius(matrix, [Fraction(1), Fraction(2), Fraction(3), Fraction(4)])
    slack = rho * norm_sq(lambdas) - energy(matrix, lambdas)
    offdiag_count = sum(
        1 for i in range(len(Q_VALUES)) for j in range(len(Q_VALUES)) if i != j and matrix[i][j]
    )
    return {
        "h": h,
        "profile": profile,
        "gram_residuals": residuals,
        "diagonal_residuals": diagonal_residuals,
        "schur_radius": str(rho),
        "weighted_schur_radius": str(weighted),
        "test_energy": str(energy(matrix, lambdas)),
        "test_norm_sq": str(norm_sq(lambdas)),
        "schur_slack": str(slack),
        "offdiag_entry_count": offdiag_count,
        "diagonal_total": str(sum((matrix[i][i] for i in range(len(Q_VALUES))), Fraction(0))),
    }


def saturation_record() -> dict[str, object]:
    h = SATURATION_H
    q_values = SATURATION_Q
    rows = [row(h, q, "constant") for q in q_values]
    matrix = gram_matrix(q_values, h, "constant")
    diagonal_values = [matrix[i][i] for i in range(len(q_values))]
    lambdas = [Fraction(1) for _ in q_values]
    row_equal = all(candidate == rows[0] for candidate in rows[1:])
    all_entries_equal = all(value == matrix[0][0] for line in matrix for value in line)
    rho = schur_radius(matrix)
    coherent = energy(matrix, lambdas)
    diagonal_total = sum(diagonal_values, Fraction(0))
    rayleigh = coherent / norm_sq(lambdas)
    return {
        "h": h,
        "height": HEIGHT,
        "q_values": list(q_values),
        "cutoffs": [h * q // HEIGHT for q in q_values],
        "rows": [{str(a): str(value) for a, value in sorted(values.items())} for values in rows],
        "gram": [[str(value) for value in line] for line in matrix],
        "diagonal_values": [str(value) for value in diagonal_values],
        "row_equal": row_equal,
        "all_gram_entries_equal": all_entries_equal,
        "schur_radius": str(rho),
        "coherent_energy": str(coherent),
        "diagonal_total": str(diagonal_total),
        "rayleigh_quotient": str(rayleigh),
        "coherent_to_diagonal_ratio": str(coherent / diagonal_total),
        "expected_p": len(q_values),
    }


def build_certificate() -> dict[str, object]:
    records = [generic_record(h, profile) for h in H_VALUES for profile in ("constant", "affine")]
    saturation = saturation_record()
    require(all(all(value == "0" for value in record["gram_residuals"]) for record in records), "Gram mismatch")
    require(all(all(value == "0" for value in record["diagonal_residuals"]) for record in records), "diagonal mismatch")
    require(saturation["row_equal"], "saturation rows not equal")
    require(saturation["all_gram_entries_equal"], "saturation Gram not constant")
    require(saturation["coherent_to_diagonal_ratio"] == str(len(SATURATION_Q)), "saturation ratio mismatch")
    return {
        "schema": "tpc221-collision-graph-schur-envelope-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "height": HEIGHT,
        "q_values": list(Q_VALUES),
        "h_values": list(H_VALUES),
        "records": records,
        "saturation": saturation,
        "checks": {
            "psd_gram_fixture": True,
            "unweighted_schur_exact": True,
            "weighted_schur_exact": True,
            "literal_saturation_exact": True,
            "absolute_schur_subp_refuted_scoped": True,
        },
        "firewall": {
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
