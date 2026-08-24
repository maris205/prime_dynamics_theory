#!/usr/bin/env python3
"""Exact Gram criterion for TPC-227 packet/profile axis separation.

All computations use ``Fraction`` arithmetic.  A finite synthesis operator is
represented by a tuple of output rows.  The four-phase polarization compiler
is compatible with a fixed physical operator precisely when the four Gram
matrices agree with the physical Gram matrix.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from typing import Iterable


Matrix = tuple[tuple[Fraction, ...], ...]


class AxisSeparationFailure(RuntimeError):
    """Raised when an exact TPC-227 invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise AxisSeparationFailure(message)


def matrix(rows: Iterable[Iterable[int | Fraction]]) -> Matrix:
    result = tuple(tuple(Fraction(value) for value in row) for row in rows)
    require(bool(result), "matrix must have at least one row")
    width = len(result[0])
    require(width > 0, "matrix must have at least one column")
    require(all(len(row) == width for row in result), "ragged matrix")
    return result


def shape(value: Matrix) -> tuple[int, int]:
    return len(value), len(value[0])


def zero(rows: int, columns: int) -> Matrix:
    return tuple(tuple(Fraction(0) for _ in range(columns)) for _ in range(rows))


def add(left: Matrix, right: Matrix) -> Matrix:
    require(shape(left) == shape(right), "matrix-add shape mismatch")
    return tuple(
        tuple(a + b for a, b in zip(row_left, row_right, strict=True))
        for row_left, row_right in zip(left, right, strict=True)
    )


def subtract(left: Matrix, right: Matrix) -> Matrix:
    require(shape(left) == shape(right), "matrix-subtract shape mismatch")
    return tuple(
        tuple(a - b for a, b in zip(row_left, row_right, strict=True))
        for row_left, row_right in zip(left, right, strict=True)
    )


def scale(value: Matrix, scalar: int | Fraction) -> Matrix:
    coefficient = Fraction(scalar)
    return tuple(tuple(coefficient * entry for entry in row) for row in value)


def transpose(value: Matrix) -> Matrix:
    rows, columns = shape(value)
    return tuple(tuple(value[row][column] for row in range(rows)) for column in range(columns))


def multiply(left: Matrix, right: Matrix) -> Matrix:
    left_rows, inner = shape(left)
    right_rows, right_columns = shape(right)
    require(inner == right_rows, "matrix-product shape mismatch")
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(inner)), Fraction(0))
            for j in range(right_columns)
        )
        for i in range(left_rows)
    )


def gram(operator: Matrix) -> Matrix:
    return multiply(transpose(operator), operator)


def matrix_is_zero(value: Matrix) -> bool:
    return all(entry == 0 for row in value for entry in row)


def matrix_equal(left: Matrix, right: Matrix) -> bool:
    return shape(left) == shape(right) and left == right


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def matrix_text(value: Matrix) -> list[list[str]]:
    return [[fraction_text(entry) for entry in row] for row in value]


def dft_moments(grams: tuple[Matrix, Matrix, Matrix, Matrix]) -> dict[str, Matrix]:
    """Return the real matrix components of A0, A1 and A2.

    A_k=(1/4) sum_j i^(kj) Q_j.  Since each Q_j is real symmetric,
    A1 is stored through its real and imaginary components.
    """

    q0, q1, q2, q3 = grams
    base_shape = shape(q0)
    require(all(shape(value) == base_shape for value in grams), "Gram shape mismatch")
    return {
        "A0": scale(add(add(q0, q1), add(q2, q3)), Fraction(1, 4)),
        "A1_real": scale(subtract(q0, q2), Fraction(1, 4)),
        "A1_imag": scale(subtract(q1, q3), Fraction(1, 4)),
        "A2": scale(add(subtract(q0, q1), subtract(q2, q3)), Fraction(1, 4)),
    }


def compatibility_record(name: str, operators: tuple[Matrix, Matrix, Matrix, Matrix], target: Matrix) -> dict[str, object]:
    target_gram = gram(target)
    grams = tuple(gram(operator) for operator in operators)
    moments = dft_moments(grams)  # type: ignore[arg-type]
    compatible = (
        matrix_equal(moments["A0"], target_gram)
        and matrix_is_zero(moments["A1_real"])
        and matrix_is_zero(moments["A1_imag"])
        and matrix_is_zero(moments["A2"])
    )
    gram_equalities = tuple(matrix_equal(value, target_gram) for value in grams)
    require(compatible == all(gram_equalities), f"DFT/Gram equivalence failed for {name}")
    return {
        "name": name,
        "compatible_with_target": compatible,
        "all_packet_grams_equal_target": all(gram_equalities),
        "packet_gram_equalities": list(gram_equalities),
        "packet_grams_all_equal_each_other": all(value == grams[0] for value in grams),
        "target_gram": matrix_text(target_gram),
        "A0_minus_target": matrix_text(subtract(moments["A0"], target_gram)),
        "A1_real": matrix_text(moments["A1_real"]),
        "A1_imag": matrix_text(moments["A1_imag"]),
        "A2": matrix_text(moments["A2"]),
    }


def resonance_operators(h: int = 400) -> dict[str, Matrix]:
    """Return the one-coordinate 3--7 collision blocks at Q=25."""

    require(type(h) is int and h > 0, "h must be positive integer")
    c = Fraction(1, h)
    return {
        "physical_aligned": matrix(((c, c),)),
        "row_odd_sign": matrix(((c, -c),)),
    }


def certificate_payload() -> dict[str, object]:
    blocks = resonance_operators()
    physical = blocks["physical_aligned"]
    odd = blocks["row_odd_sign"]
    minus_physical = scale(physical, -1)
    twice_physical = scale(physical, 2)
    three_physical = scale(physical, 3)
    four_physical = scale(physical, 4)

    fixtures = {
        "common_physical": compatibility_record(
            "common_physical", (physical, physical, physical, physical), physical
        ),
        "packet_global_signs": compatibility_record(
            "packet_global_signs",
            (physical, minus_physical, physical, minus_physical),
            physical,
        ),
        "row_dependent_odd_sign": compatibility_record(
            "row_dependent_odd_sign", (odd, odd, odd, odd), physical
        ),
        "alternating_scale": compatibility_record(
            "alternating_scale",
            (physical, twice_physical, physical, twice_physical),
            physical,
        ),
        "fully_unequal_scale": compatibility_record(
            "fully_unequal_scale",
            (physical, twice_physical, three_physical, four_physical),
            physical,
        ),
        "mixed_row_profile": compatibility_record(
            "mixed_row_profile", (physical, odd, physical, odd), physical
        ),
    }

    require(fixtures["common_physical"]["compatible_with_target"] is True, "common fixture")
    require(fixtures["packet_global_signs"]["compatible_with_target"] is True, "sign invisibility")
    for key in (
        "row_dependent_odd_sign",
        "alternating_scale",
        "fully_unequal_scale",
        "mixed_row_profile",
    ):
        require(fixtures[key]["compatible_with_target"] is False, f"expected obstruction: {key}")

    q_physical = gram(physical)
    q_odd = gram(odd)
    difference = subtract(q_odd, q_physical)
    require(difference[0][1] == Fraction(-1, 80000), "Q25 off-diagonal mismatch")
    require(difference[1][0] == Fraction(-1, 80000), "symmetric mismatch")

    transcript = "\n".join(
        f"{name}|{record['compatible_with_target']}|{record['packet_grams_all_equal_each_other']}"
        for name, record in sorted(fixtures.items())
    )

    return {
        "schema": "tpc227-packet-profile-axis-separation-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "author": "Liang Wang",
        "affiliation": "Huazhong University of Science and Technology",
        "theorem": {
            "criterion": "four-phase compatibility iff T_j^*T_j=T^*T for j=0,1,2,3",
            "physical_V59_packet_axis": "a^(j)=beta+i^j w",
            "physical_V59_profile_axis": "one common psi_+(v)",
            "global_packet_phase": "GRAM_INVISIBLE",
            "row_dependent_profile_sign": "NOT_SOURCE_TRANSFERABLE_WITHOUT_GRAM_EQUALITY",
        },
        "q25_resonance_block": {
            "h": 400,
            "physical_operator": matrix_text(physical),
            "odd_row_operator": matrix_text(odd),
            "physical_gram": matrix_text(q_physical),
            "odd_row_gram": matrix_text(q_odd),
            "gram_difference": matrix_text(difference),
            "off_diagonal_difference": "-1/80000",
        },
        "fixtures": fixtures,
        "fixture_digest": sha256(transcript.encode()).hexdigest(),
        "checks": {
            "operator_dft_inversion_exact": True,
            "common_physical_transform_passes": True,
            "global_packet_signs_are_gram_invisible": True,
            "row_dependent_odd_sign_fails_physical_gram": True,
            "packet_dependent_scale_contamination_detected": True,
            "q25_resonance_off_diagonal_mismatch_exact": True,
        },
        "firewall": {
            "TPC226_balanced_profile_AP_saving": "PROVED_EXACT_FINITE_PROFILE",
            "TPC226_balanced_profile_V59_source_transfer": "REFUTED_SCOPED_AS_AUTOMATIC_INFERENCE",
            "V59_source_native_common_profile_compiler": "OPEN",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
        "round2_clue": "KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON",
    }


def validate_payload(data: dict[str, object]) -> None:
    require(data.get("schema") == "tpc227-packet-profile-axis-separation-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level")
    theorem = data.get("theorem")
    require(type(theorem) is dict, "theorem object")
    require(
        theorem.get("criterion") == "four-phase compatibility iff T_j^*T_j=T^*T for j=0,1,2,3",
        "criterion",
    )
    fixtures = data.get("fixtures")
    require(type(fixtures) is dict and len(fixtures) == 6, "fixtures")
    require(fixtures["common_physical"]["compatible_with_target"] is True, "common")
    require(fixtures["packet_global_signs"]["compatible_with_target"] is True, "global signs")
    require(fixtures["row_dependent_odd_sign"]["compatible_with_target"] is False, "row signs")
    checks = data.get("checks")
    require(type(checks) is dict and all(type(v) is bool and v for v in checks.values()), "checks")


def build_certificate() -> dict[str, object]:
    payload = certificate_payload()
    validate_payload(payload)
    return payload
