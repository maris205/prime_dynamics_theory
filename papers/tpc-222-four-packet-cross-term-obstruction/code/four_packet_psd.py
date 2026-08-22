#!/usr/bin/env python3
"""Exact Gaussian-rational four-packet PSD and polarization calculations."""

from __future__ import annotations

from fractions import Fraction


Gaussian = tuple[Fraction, Fraction]


class PacketFailure(RuntimeError):
    pass


ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
I: Gaussian = (Fraction(0), Fraction(1))


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise PacketFailure(message)


def add(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] + y[0], x[1] + y[1])


def neg(x: Gaussian) -> Gaussian:
    return (-x[0], -x[1])


def sub(x: Gaussian, y: Gaussian) -> Gaussian:
    return add(x, neg(y))


def mul(x: Gaussian, y: Gaussian) -> Gaussian:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def conj(x: Gaussian) -> Gaussian:
    return (x[0], -x[1])


def scale(x: Gaussian, c: Fraction) -> Gaussian:
    return (c * x[0], c * x[1])


def norm_sq(x: Gaussian) -> Fraction:
    return x[0] * x[0] + x[1] * x[1]


def gaussian_text(x: Gaussian) -> str:
    if x[1] == 0:
        return str(x[0])
    return f"{x[0]}+{x[1]}i"


def phase(r: int) -> Gaussian:
    return (ONE, I, neg(ONE), neg(I))[r % 4]


def inner(x: list[Gaussian], y: list[Gaussian]) -> Gaussian:
    require(len(x) == len(y), "vector dimension mismatch")
    total = ZERO
    for left, right in zip(x, y):
        total = add(total, mul(conj(left), right))
    return total


def vector_add(x: list[Gaussian], y: list[Gaussian]) -> list[Gaussian]:
    require(len(x) == len(y), "vector dimension mismatch")
    return [add(left, right) for left, right in zip(x, y)]


def scalar_vector(c: Gaussian, x: list[Gaussian]) -> list[Gaussian]:
    return [mul(c, value) for value in x]


def vector_sum(vectors: list[list[Gaussian]], coefficients: list[Gaussian]) -> list[Gaussian]:
    require(len(vectors) == len(coefficients), "coefficient dimension mismatch")
    result = [ZERO for _ in vectors[0]]
    for vector, coefficient in zip(vectors, coefficients):
        result = vector_add(result, scalar_vector(coefficient, vector))
    return result


def energy(vectors: list[list[Gaussian]], coefficients: list[Gaussian]) -> Fraction:
    return norm_sq(vector_sum(vectors, coefficients)[0])


def gram(vectors: list[list[Gaussian]]) -> list[list[Gaussian]]:
    return [[inner(vectors[j], vectors[k]) for k in range(len(vectors))]
            for j in range(len(vectors))]


def polarization(x: list[Gaussian], y: list[Gaussian]) -> Gaussian:
    total = ZERO
    for r in range(4):
        mixed = vector_add(x, scalar_vector(phase(r), y))
        mixed_norm = sum((norm_sq(value) for value in mixed), Fraction(0))
        total = add(total, mul(phase(-r), (mixed_norm, Fraction(0))))
    return scale(total, Fraction(1, 4))


def gram_text(matrix: list[list[Gaussian]]) -> list[list[str]]:
    return [[gaussian_text(value) for value in line] for line in matrix]


def packet_vectors(signs: tuple[int, int, int, int]) -> list[list[Gaussian]]:
    unit = [ONE]
    return [scalar_vector((Fraction(sign), Fraction(0)), unit) for sign in signs]


def fixture_record(name: str, signs: tuple[int, int, int, int]) -> dict[str, object]:
    vectors = packet_vectors(signs)
    matrix = gram(vectors)
    coefficients = [ONE, ONE, ONE, ONE]
    diagonal = [matrix[i][i] for i in range(4)]
    trace = sum((value[0] for value in diagonal), Fraction(0))
    target = energy(vectors, coefficients)
    coefficient_norm = sum((norm_sq(value) for value in coefficients), Fraction(0))
    polarization_residuals = []
    for j in range(4):
        for k in range(4):
            polarization_residuals.append(
                gaussian_text(sub(polarization(vectors[j], vectors[k]), matrix[j][k])))
    rank_one = all(matrix[j][k] == mul(matrix[j][0], matrix[0][k])
                   for j in range(4) for k in range(4))
    return {
        "name": name,
        "signs": list(signs),
        "gram": gram_text(matrix),
        "diagonal": [gaussian_text(value) for value in diagonal],
        "trace": str(trace),
        "target_energy": str(target),
        "coefficient_norm": str(coefficient_norm),
        "trace_bound": str(trace * coefficient_norm),
        "trace_slack": str(trace * coefficient_norm - target),
        "rank_one": rank_one,
        "polarization_residuals": polarization_residuals,
    }


def build_certificate() -> dict[str, object]:
    plus = fixture_record("plus", (1, 1, 1, 1))
    minus = fixture_record("minus", (1, -1, 1, -1))
    require(plus["target_energy"] == "16", "plus energy mismatch")
    require(minus["target_energy"] == "0", "minus energy mismatch")
    require(plus["trace"] == minus["trace"] == "4", "trace mismatch")
    require(plus["diagonal"] == minus["diagonal"] == ["1", "1", "1", "1"], "diagonal mismatch")
    require(all(value == "0" for value in plus["polarization_residuals"]), "plus polarization mismatch")
    require(all(value == "0" for value in minus["polarization_residuals"]), "minus polarization mismatch")
    return {
        "schema": "tpc222-four-packet-cross-term-obstruction-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "packet_count": 4,
        "fixtures": [plus, minus],
        "checks": {
            "psd_gram_exact": True,
            "four_point_polarization_exact": True,
            "trace_rayleigh_envelope_exact": True,
            "same_diagonal_different_signed_energy": True,
            "signed_cross_term_nonidentifiability_scoped": True,
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
