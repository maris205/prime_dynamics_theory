#!/usr/bin/env python3
"""Exact source-native polarized collision compiler for TPC-228."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from typing import Iterable


Gaussian = tuple[Fraction, Fraction]
Coordinate = tuple[int, int]
Vector = dict[Coordinate, Gaussian]
Rows = dict[int, Vector]

ZERO: Gaussian = (Fraction(0), Fraction(0))
ONE: Gaussian = (Fraction(1), Fraction(0))
I_POWERS: tuple[Gaussian, ...] = (
    (Fraction(1), Fraction(0)),
    (Fraction(0), Fraction(1)),
    (Fraction(-1), Fraction(0)),
    (Fraction(0), Fraction(-1)),
)


class CompilerFailure(RuntimeError):
    """Raised when a declared TPC-228 identity fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CompilerFailure(message)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gsub(left: Gaussian, right: Gaussian) -> Gaussian:
    return gadd(left, gneg(right))


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gscale(value: Gaussian, scalar: Fraction | int) -> Gaussian:
    coefficient = Fraction(scalar)
    return value[0] * coefficient, value[1] * coefficient


def giszero(value: Gaussian) -> bool:
    return value == ZERO


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def gaussian_text(value: Gaussian) -> str:
    real, imag = value
    if imag == 0:
        return fraction_text(real)
    if real == 0:
        return f"{fraction_text(imag)}i"
    sign = "+" if imag > 0 else "-"
    return f"{fraction_text(real)}{sign}{fraction_text(abs(imag))}i"


def add_to(vector: Vector, coordinate: Coordinate, value: Gaussian) -> None:
    vector[coordinate] = gadd(vector.get(coordinate, ZERO), value)
    if giszero(vector[coordinate]):
        del vector[coordinate]


def vector_add(left: Vector, right: Vector) -> Vector:
    result = dict(left)
    for coordinate, value in right.items():
        add_to(result, coordinate, value)
    return result


def vector_scale(value: Vector, scalar: Gaussian) -> Vector:
    return {
        coordinate: gmul(scalar, entry)
        for coordinate, entry in value.items()
        if not giszero(gmul(scalar, entry))
    }


def vector_sum(values: Iterable[Vector]) -> Vector:
    result: Vector = {}
    for value in values:
        result = vector_add(result, value)
    return result


def inner(left: Vector, right: Vector) -> Gaussian:
    """Hilbert inner product linear in the first argument."""

    result = ZERO
    for coordinate, value in left.items():
        if coordinate in right:
            result = gadd(result, gmul(value, gconj(right[coordinate])))
    return result


def squared_norm(value: Vector) -> Fraction:
    result = inner(value, value)
    require(result[1] == 0 and result[0] >= 0, "invalid squared norm")
    return result[0]


def packet_rows(beta_rows: Rows, w_rows: Rows, packet: int) -> Rows:
    require(set(beta_rows) == set(w_rows), "source row labels mismatch")
    require(type(packet) is int and 0 <= packet < 4, "packet index")
    phase = I_POWERS[packet]
    return {
        q: vector_add(beta_rows[q], vector_scale(w_rows[q], phase))
        for q in beta_rows
    }


def packet_ap_minus_diagonal(beta_rows: Rows, w_rows: Rows, packet: int) -> Fraction:
    rows = packet_rows(beta_rows, w_rows, packet)
    ap = squared_norm(vector_sum(rows.values()))
    diagonal = sum((squared_norm(row) for row in rows.values()), Fraction(0))
    return ap - diagonal


def four_phase_off_diagonal(beta_rows: Rows, w_rows: Rows) -> Gaussian:
    result = ZERO
    for packet in range(4):
        result = gadd(
            result,
            gscale(I_POWERS[packet], packet_ap_minus_diagonal(beta_rows, w_rows, packet)),
        )
    return gscale(result, Fraction(1, 4))


def direct_off_diagonal(beta_rows: Rows, w_rows: Rows) -> Gaussian:
    require(set(beta_rows) == set(w_rows), "source row labels mismatch")
    result = ZERO
    for q, beta in beta_rows.items():
        for r, w in w_rows.items():
            if q != r:
                result = gadd(result, inner(beta, w))
    return result


def q25_rows(beta_amplitudes: dict[tuple[int, int], int], w_amplitudes: dict[tuple[int, int], int]) -> tuple[Rows, Rows]:
    """Build the two shared-coordinate restriction of the Q25 3--7 collision."""

    h = 400
    row_atoms = {
        (37, 3): (h, 119),
        (37, -3): (h, 281),
        (47, -7): (h, 119),
        (47, 7): (h, 281),
    }
    require(set(beta_amplitudes) <= set(row_atoms), "unknown beta atom")
    require(set(w_amplitudes) <= set(row_atoms), "unknown w atom")
    beta_rows: Rows = {37: {}, 47: {}}
    w_rows: Rows = {37: {}, 47: {}}
    for atom, coordinate in row_atoms.items():
        q, _ = atom
        beta_value = Fraction(beta_amplitudes.get(atom, 0), h)
        w_value = Fraction(w_amplitudes.get(atom, 0), h)
        if beta_value:
            add_to(beta_rows[q], coordinate, (beta_value, Fraction(0)))
        if w_value:
            add_to(w_rows[q], coordinate, (w_value, Fraction(0)))
    return beta_rows, w_rows


def fixture_record(name: str, beta: dict[tuple[int, int], int], w: dict[tuple[int, int], int]) -> dict[str, object]:
    beta_rows, w_rows = q25_rows(beta, w)
    packet_values = [packet_ap_minus_diagonal(beta_rows, w_rows, packet) for packet in range(4)]
    polarized = four_phase_off_diagonal(beta_rows, w_rows)
    direct = direct_off_diagonal(beta_rows, w_rows)
    require(polarized == direct, f"compiler mismatch: {name}")
    return {
        "name": name,
        "packet_AP_minus_diagonal": [fraction_text(value) for value in packet_values],
        "four_phase_value": gaussian_text(polarized),
        "direct_collision_value": gaussian_text(direct),
        "sign": "POSITIVE" if direct[0] > 0 else "NEGATIVE" if direct[0] < 0 else "ZERO",
    }


def general_three_row_control() -> dict[str, object]:
    c01 = (9, 1)
    c12 = (9, 2)
    beta: Rows = {
        11: {c01: (Fraction(1, 3), Fraction(0))},
        13: {c01: (Fraction(2, 3), Fraction(0)), c12: (Fraction(-1, 2), Fraction(0))},
        17: {c12: (Fraction(3, 5), Fraction(0))},
    }
    w: Rows = {
        11: {c01: (Fraction(-2, 7), Fraction(0))},
        13: {c01: (Fraction(5, 11), Fraction(0)), c12: (Fraction(7, 13), Fraction(0))},
        17: {c12: (Fraction(-11, 17), Fraction(0))},
    }
    polarized = four_phase_off_diagonal(beta, w)
    direct = direct_off_diagonal(beta, w)
    require(polarized == direct, "three-row compiler mismatch")
    return {
        "row_count": 3,
        "collision_coordinates": 2,
        "four_phase_value": gaussian_text(polarized),
        "direct_value": gaussian_text(direct),
    }


def no_collision_control() -> dict[str, object]:
    beta: Rows = {
        11: {(7, 1): (Fraction(2), Fraction(0))},
        13: {(7, 2): (Fraction(3), Fraction(0))},
    }
    w: Rows = {
        11: {(7, 1): (Fraction(5), Fraction(0))},
        13: {(7, 2): (Fraction(7), Fraction(0))},
    }
    value = four_phase_off_diagonal(beta, w)
    require(value == ZERO and direct_off_diagonal(beta, w) == ZERO, "no-collision control")
    return {"four_phase_value": "0", "direct_value": "0"}


def certificate_payload() -> dict[str, object]:
    atoms = ((37, 3), (37, -3), (47, -7), (47, 7))
    all_one = {atom: 1 for atom in atoms}
    all_minus = {atom: -1 for atom in atoms}
    beta_p = {(37, 3): 1, (37, -3): 1}
    w_r = {(47, -7): 1, (47, 7): 1}
    row_opposite_w = {(37, 3): 1, (37, -3): 1, (47, -7): -1, (47, 7): -1}
    one_coordinate_beta = {(37, 3): 1}
    one_coordinate_w = {(47, -7): 1}

    fixtures = {
        "positive": fixture_record("positive", all_one, all_one),
        "negative": fixture_record("negative", all_one, all_minus),
        "row_cancellation": fixture_record("row_cancellation", all_one, row_opposite_w),
        "directed": fixture_record("directed", beta_p, w_r),
        "one_coordinate": fixture_record("one_coordinate", one_coordinate_beta, one_coordinate_w),
    }
    expected = {
        "positive": "1/40000",
        "negative": "-1/40000",
        "row_cancellation": "0",
        "directed": "1/80000",
        "one_coordinate": "1/160000",
    }
    for name, value in expected.items():
        require(fixtures[name]["direct_collision_value"] == value, f"fixture value: {name}")

    transcript = "\n".join(
        f"{name}|{record['four_phase_value']}|{','.join(record['packet_AP_minus_diagonal'])}"
        for name, record in sorted(fixtures.items())
    )
    return {
        "schema": "tpc228-source-native-polarized-collision-compiler-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "author": "Liang Wang",
        "affiliation": "Huazhong University of Science and Technology",
        "theorem": {
            "common_profile_packet_rule": "W_q^(j)=U_q+i^j V_q",
            "exact_compiler": "1/4 sum_j i^j(E_AP^(j)-E_diag^(j))=sum_(q!=r)<U_q,V_r>",
            "q25_resonance_formula": "sum over the two shared residues of beta_p*w_r+beta_r*w_p divided by h^2",
            "phase_axis": "SOURCE_SEQUENCE",
            "profile_axis": "COMMON_TRANSFORM",
        },
        "q25": {"Q": 25, "h": 400, "p": 37, "r": 47, "residues": [119, 281]},
        "fixtures": fixtures,
        "general_three_row_control": general_three_row_control(),
        "no_collision_control": no_collision_control(),
        "fixture_digest": sha256(transcript.encode()).hexdigest(),
        "checks": {
            "four_phase_compiler_exact": True,
            "diagonal_deleted_before_collision_sum": True,
            "packet_phase_on_source_axis": True,
            "common_profile_axis_preserved": True,
            "q25_positive_negative_zero_controls": True,
            "general_graph_control": True,
            "no_collision_control": True,
        },
        "firewall": {
            "actual_V59_to_primitive_atom_amplitude_crosswalk": "OPEN",
            "arithmetic_sign_theorem": "OPEN",
            "arithmetic_advance": "NO",
            "arithmetic_cancellation": "NONE",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
        "round2_clue": "ANALYZE_THE_SOURCE_NATIVE_3_7_COLLISION_GRAPH_AS_EXACT_TWO_BY_TWO_BLOCKS",
    }


def validate_payload(data: dict[str, object]) -> None:
    require(data.get("schema") == "tpc228-source-native-polarized-collision-compiler-v1", "schema")
    require(data.get("status") == "PASS", "status")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim")
    theorem = data.get("theorem")
    require(type(theorem) is dict, "theorem")
    require(theorem.get("phase_axis") == "SOURCE_SEQUENCE", "phase axis")
    require(theorem.get("profile_axis") == "COMMON_TRANSFORM", "profile axis")
    fixtures = data.get("fixtures")
    require(type(fixtures) is dict and len(fixtures) == 5, "fixtures")
    require(fixtures["positive"]["direct_collision_value"] == "1/40000", "positive")
    require(fixtures["negative"]["direct_collision_value"] == "-1/40000", "negative")
    require(fixtures["row_cancellation"]["direct_collision_value"] == "0", "zero")
    checks = data.get("checks")
    require(type(checks) is dict and all(type(value) is bool and value for value in checks.values()), "checks")


def build_certificate() -> dict[str, object]:
    data = certificate_payload()
    validate_payload(data)
    return data
