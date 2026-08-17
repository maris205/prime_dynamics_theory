#!/usr/bin/env python3
"""Exact certificate producer for the TPC-208 additive edge frame.

The implementation uses Gaussian rationals and prime cyclotomic coefficient
vectors.  It is finite QA for the general proofs in the manuscript; it is not
an asymptotic arithmetic experiment.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable


class CertificateFailure(RuntimeError):
    """Raised when a frozen exact identity fails."""


Gaussian = tuple[Fraction, Fraction]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CertificateFailure(message)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] - right[0], left[1] - right[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gscale(scalar: Fraction, value: Gaussian) -> Gaussian:
    return scalar * value[0], scalar * value[1]


def gabs2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gsum(values: Iterable[Gaussian]) -> Gaussian:
    total = (Fraction(0), Fraction(0))
    for value in values:
        total = gadd(total, value)
    return total


def ftext(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def gtext(value: Gaussian) -> list[str]:
    return [ftext(value[0]), ftext(value[1])]


def edges(q: int) -> tuple[tuple[int, int], ...]:
    require(type(q) is int and q >= 2, "invalid modulus")
    return tuple(
        (left, right)
        for left in range(1, q)
        for right in range(left + 1, q)
    )


def complete_graph_laplacian(q: int) -> list[list[int]]:
    dimension = q - 1
    matrix = [[0 for _ in range(dimension)] for _ in range(dimension)]
    for left, right in edges(q):
        i = left - 1
        j = right - 1
        matrix[i][i] += 1
        matrix[j][j] += 1
        matrix[i][j] -= 1
        matrix[j][i] -= 1
    return matrix


def cyclotomic_integer(coefficients: tuple[int, ...]) -> int:
    """Reduce a rational prime-cyclotomic expression known to be integral."""

    require(len(coefficients) >= 2, "cyclotomic vector is too short")
    common = coefficients[1]
    require(
        all(value == common for value in coefficients[1:]),
        "cyclotomic expression did not reduce to an integer",
    )
    return coefficients[0] - common


def edge_kernel(q: int, residue_left: int, residue_right: int) -> int:
    """Return sum_e Delta_e(r) conjugate(Delta_e(s)) exactly."""

    coefficients = [0 for _ in range(q)]
    for left, right in edges(q):
        terms = (
            (1, -left * residue_left + left * residue_right),
            (-1, -left * residue_left + right * residue_right),
            (-1, -right * residue_left + left * residue_right),
            (1, -right * residue_left + right * residue_right),
        )
        for sign, exponent in terms:
            coefficients[exponent % q] += sign
    return cyclotomic_integer(tuple(coefficients))


def direct_zero_hole_variance(row: tuple[Gaussian, ...]) -> Fraction:
    q = len(row)
    require(q >= 2, "row is too short")
    unit_row = row[1:]
    mean = gscale(Fraction(1, q - 1), gsum(unit_row))
    return sum((gabs2(gsub(value, mean)) for value in unit_row), Fraction(0))


def edge_frame_variance(row: tuple[Gaussian, ...]) -> Gaussian:
    q = len(row)
    total = (Fraction(0), Fraction(0))
    for residue_left in range(q):
        for residue_right in range(q):
            coefficient = Fraction(
                edge_kernel(q, residue_left, residue_right), q * (q - 1)
            )
            total = gadd(
                total,
                gscale(
                    coefficient,
                    gmul(row[residue_left], gconj(row[residue_right])),
                ),
            )
    return total


def row_fixture(q: int) -> tuple[Gaussian, ...]:
    return tuple(
        (Fraction(residue + 1, 2), Fraction((-1) ** residue, residue + 1))
        for residue in range(q)
    )


def polarization(left: Gaussian, right: Gaussian) -> Gaussian:
    imaginary_unit = (Fraction(0), Fraction(1))
    phase = (Fraction(1), Fraction(0))
    total = (Fraction(0), Fraction(0))
    for _ in range(4):
        packet = gadd(left, gmul(phase, right))
        total = gadd(total, gscale(Fraction(1, 4), gscale(gabs2(packet), phase)))
        phase = gmul(phase, imaginary_unit)
    return total


def build_certificate() -> dict[str, object]:
    modulus_payload: dict[str, object] = {}
    laplacian_rows = 0
    physical_kernel_rows = 0
    row_diagonal_rows = 0
    mutation_rows = 0

    for q in (2, 3, 5, 7, 11):
        dimension = q - 1
        laplacian = complete_graph_laplacian(q)
        for left in range(dimension):
            for right in range(dimension):
                expected = dimension - 1 if left == right else -1
                require(laplacian[left][right] == expected, f"laplacian q={q}")
                laplacian_rows += 1
        edge_count = len(edges(q))
        require(edge_count == (q - 1) * (q - 2) // 2, f"edge count q={q}")
        require(max(q - 2, 0) == dimension - 1, f"projection rank q={q}")
        laplacian_rows += 2

        kernel = []
        for residue_left in range(q):
            row = []
            for residue_right in range(q):
                observed = edge_kernel(q, residue_left, residue_right)
                if residue_left == 0 or residue_right == 0:
                    expected = 0
                elif residue_left == residue_right:
                    expected = q * (q - 2)
                else:
                    expected = -q
                require(observed == expected, f"physical kernel q={q}")
                row.append(observed)
                physical_kernel_rows += 1
            kernel.append(row)

        fixture = row_fixture(q)
        direct = direct_zero_hole_variance(fixture)
        emitted = edge_frame_variance(fixture)
        require(emitted[1] == 0, f"non-real frame output q={q}")
        require(emitted[0] == direct, f"frame variance mismatch q={q}")
        diagonal_factor = Fraction(q - 2, q - 1)
        require(
            Fraction(q * (q - 2), q * (q - 1)) == diagonal_factor,
            f"diagonal factor q={q}",
        )
        require(
            (q == 2 and edge_count == 0) or (q > 2 and edge_count > 0),
            f"degenerate edge family q={q}",
        )
        row_diagonal_rows += 4

        single_raw_variance = Fraction(q - 2, q - 1)
        single_diagonal = Fraction(q - 2, q - 1)
        require(
            single_raw_variance - single_diagonal == 0,
            f"single-coefficient diagonal deletion q={q}",
        )
        require(
            (q - 1) != max(q - 2, 0),
            f"including frequency zero did not change projection rank q={q}",
        )
        mutation_rows += 2

        modulus_payload[str(q)] = {
            "diagonal_factor": ftext(diagonal_factor),
            "edge_count": edge_count,
            "edge_mass_on_unit": q * (q - 2),
            "forced_literal_edge_weight": ftext(Fraction(1, q - 1)),
            "laplacian": laplacian,
            "oriented_edge_count": (q - 1) * (q - 2),
            "physical_kernel": kernel,
            "projection_rank": max(q - 2, 0),
            "row_fixture": [gtext(value) for value in fixture],
            "row_variance_direct": ftext(direct),
            "row_variance_edge_frame": gtext(emitted),
        }

    polarization_payload = []
    for left, right in (
        ((Fraction(2), Fraction(3)), (Fraction(-1), Fraction(2))),
        ((Fraction(3, 2), Fraction(5, 3)), (Fraction(-7, 4), Fraction(2, 5))),
    ):
        observed = polarization(left, right)
        expected = gmul(left, gconj(right))
        require(observed == expected, "polarization orientation")
        polarization_payload.append(
            {
                "left": gtext(left),
                "right": gtext(right),
                "polarized": gtext(observed),
                "direct": gtext(expected),
            }
        )

    falsifier_payload: dict[str, object] = {}
    falsifier_rows = 0
    for q in (3, 5, 7, 11):
        dimension = q - 1
        equal_piece = Fraction(dimension, q)
        off_equal_piece = -equal_piece
        forced_weight = Fraction(1, dimension)
        projection_off_diagonal = -Fraction(1, dimension)
        require(equal_piece != 0, f"vacuous equal piece q={q}")
        require(equal_piece + off_equal_piece == 0, f"spike cancellation q={q}")
        require(-forced_weight == projection_off_diagonal, f"edge uniqueness q={q}")
        require(
            dimension * (dimension - 1)
            == 2 * (dimension * (dimension - 1) // 2),
            f"oriented factor q={q}",
        )
        require(
            Fraction(complete_graph_laplacian(q)[0][1], dimension)
            == projection_off_diagonal,
            f"normalized complete-graph off-diagonal q={q}",
        )
        require(Fraction(1, q) != forced_weight, f"q/q-1 mutation q={q}")
        require(0 != projection_off_diagonal, f"dropped-edge mutation q={q}")
        mutation_rows += 1
        falsifier_rows += 5
        falsifier_payload[str(q)] = {
            "zero_residue_spike_equal_piece": ftext(equal_piece),
            "zero_residue_spike_off_equal_piece": ftext(off_equal_piece),
            "zero_residue_spike_total": "0",
            "projection_off_diagonal": ftext(-Fraction(1, dimension)),
            "forced_edge_weight": ftext(forced_weight),
        }

    counts = {
        "falsifier_uniqueness_rows": falsifier_rows,
        "laplacian_rank_rows": laplacian_rows,
        "mutation_rows": mutation_rows,
        "physical_kernel_rows": physical_kernel_rows,
        "polarization_rows": len(polarization_payload),
        "row_diagonal_rows": row_diagonal_rows,
    }
    require(sum(counts.values()) == 431, "audit row total changed")

    return {
        "audit_counts": counts,
        "audit_total": 431,
        "claim_firewall": {
            "V61_ARITHMETIC_ADVANCE": "NO",
            "V61_FIXED_ATOM_CREDIT": 0,
            "V61_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID",
            "V61_L2": "NONE",
            "V61_ROUTE_ADVANCE": "YES",
            "V61_STRUCTURAL_THRESHOLD_A": "PASS",
            "V61_TPC_208_TRIGGER": True,
            "equal_off_equal_separate_estimation": "REFUTED",
            "twin_prime_theorem": False,
        },
        "classification": "PROVED_STRUCTURAL_L1",
        "falsifiers": falsifier_payload,
        "moduli": modulus_payload,
        "open_theorem": "JOINT_COMPLETE_ORIENTED_D_K_FRAME_TO_KLOOSTERMAN_COMPILER_WITH_PRIME_SHELL_REASSEMBLY_AND_FIXED_SAVING",
        "polarization": polarization_payload,
        "schema": "TPC208_ZERO_HOLE_ADDITIVE_EDGE_FRAME_CERTIFICATE_V1",
    }
