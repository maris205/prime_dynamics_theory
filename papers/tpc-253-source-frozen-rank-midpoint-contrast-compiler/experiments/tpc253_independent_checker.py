#!/usr/bin/env python3
"""Independent semantic validator and mutation suite for TPC-253."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "TPC253_RANK_MIDPOINT_CONTRAST_CERTIFICATE_V1"
CLAIM_STATUS = "PROVED_STRUCTURAL_L1_SOURCE_FROZEN_RANK_MIDPOINT_CONTRAST_COMPILER"
MAXIMUM_CLAIM = (
    "EXACT_SOURCE_FROZEN_RANK_MIDPOINT_PROJECTOR_PARTIAL_SUM_LONGITUDINAL_"
    "TRANSVERSE_LITERAL_TPC247_KERNEL_AND_SAFE_ADJOINT_COMPILER_WITH_"
    "NONLITERAL_SHARP_SIGN_CONTROLS"
)
BASELINE_HEAD = "d7f1155999eb494bdbb98aefe1041a5d8928578f"
HANDOFF_SHA256 = "f2ad77eb42eab18b427b7a8032c68d687209a0d884851ee3c05513c83bf5e91c"
SOURCE_DIGESTS = {
    "source_frozen_tpc253_bridge": "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16",
    "tpc247_tree": "c984cbb9c51fabea54e02618e96efa587b5c1d266a8ac0768c365ad4fc497bf9",
    "bridge_tpc247": "54bb956ad55245970a7d5d8852f1472d6a9dae68e940d1f9ced0b4c243271eed",
    "tpc252_tree": "919fb268d805289ab589738926baad73e6e8830db7e4700bdb014c7ac6238c22",
    "bridge_tpc252": "2763e2b1b67e1ad0e7dd68f0429eed7ae250691d60fdb1c94fcdff89a579f5f3",
}
KERNEL_FIXTURE_LABEL = (
    "NONLITERAL_EXACT_KERNEL_SAMPLE_SUBSTITUTION_INTO_THE_LITERAL_TPC247_FORMULA"
)
CONTROL_LABEL = "NONLITERAL_SYNTHETIC_FINITE_HILBERT_SPACE_CONTROLS"
FRACTION_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

FIREWALL = {
    "TPC253_RANK_MIDPOINT_PARTITION": "PROVED_SOURCE_ONLY_DETERMINISTIC",
    "TPC253_INTEGER_THREE_QUARTER_CROSSWALK": "PROVED_EXACT",
    "TPC253_MIDPOINT_CONTRAST_NORMALIZATION": "PROVED_EXACT",
    "TPC253_PARTIAL_SUM_MOMENT_COMPILER": "PROVED_EXACT",
    "TPC253_LITERAL_V59_G_MOMENT_EXPANSION": "PROVED_EXACT",
    "TPC253_MIDPOINT_LONGITUDINAL_FORMULA": "PROVED_EXACT",
    "TPC253_COARSE_TO_MIDPOINT_COVARIANCE_TRANSFER": "PROVED_EXACT",
    "TPC253_WITHIN_CHILD_COVARIANCE_DECOMPOSITION": "PROVED_EXACT",
    "TPC253_SAFE_ADJOINT_CROSSWALK": "PROVED_EXACT",
    "TPC253_A_X_SELF_ADJOINTNESS": "NOT_CLAIMED",
    "TPC253_MIDPOINT_V59_CANONICALITY": "NOT_CLAIMED_SOURCE_ONLY_MODELING_CHOICE",
    "TPC253_SMOOTH_V59_PARTITION_IDENTIFICATION": "NOT_CLAIMED",
    "TPC253_ACTUAL_V59_NUMERICAL_REPLAY": "NOT_TESTABLE_FROM_LOCKED_MATERIAL",
    "TPC253_MIDPOINT_CONTRAST_SIGN_OR_NONZERO": "OPEN",
    "TPC253_ASYMPTOTIC_ADVANCE": "NO",
    "TPC253_ARITHMETIC_ADVANCE": "NO",
    "TPC253_FIXED_ATOM_CREDIT": "0",
    "TPC253_L2": "NONE",
    "TPC253_FULL_GATE_B": "OPEN",
    "TPC253_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC253_TWIN_PRIME_RESULT": "NONE",
}

Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
GMatrix = list[list[Gaussian]]
RMatrix = list[list[Fraction]]
ZERO: Gaussian = (Fraction(0), Fraction(0))


class CertificateError(ValueError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _fraction(value: Any, location: str) -> Fraction:
    if not isinstance(value, str) or FRACTION_PATTERN.fullmatch(value) is None:
        raise CertificateError(f"{location}: expected canonical rational string")
    parsed = Fraction(value)
    if str(parsed) != value:
        raise CertificateError(f"{location}: noncanonical rational string")
    return parsed


def _integer(value: Any, location: str) -> int:
    if type(value) is not int:
        raise CertificateError(f"{location}: expected exact integer, not bool or another type")
    return value


def _integer_list(value: Any, location: str) -> list[int]:
    if not isinstance(value, list):
        raise CertificateError(f"{location}: expected integer list")
    return [_integer(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _gaussian(value: Any, location: str) -> Gaussian:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{location}: expected Gaussian-rational pair")
    return (_fraction(value[0], location + ".real"), _fraction(value[1], location + ".imag"))


def _vector(value: Any, length: int, location: str) -> Vector:
    if not isinstance(value, list) or len(value) != length:
        raise CertificateError(f"{location}: vector shape mismatch")
    return [_gaussian(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _gmatrix(value: Any, size: int, location: str) -> GMatrix:
    if not isinstance(value, list) or len(value) != size:
        raise CertificateError(f"{location}: matrix row count mismatch")
    return [_vector(row, size, f"{location}[{index}]") for index, row in enumerate(value)]


def _rmatrix(value: Any, size: int, location: str) -> RMatrix:
    if not isinstance(value, list) or len(value) != size:
        raise CertificateError(f"{location}: rational matrix row count mismatch")
    result: RMatrix = []
    for row_index, row in enumerate(value):
        if not isinstance(row, list) or len(row) != size:
            raise CertificateError(f"{location}[{row_index}]: rational matrix column mismatch")
        result.append([
            _fraction(entry, f"{location}[{row_index}][{column_index}]")
            for column_index, entry in enumerate(row)
        ])
    return result


def _keys(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise CertificateError(f"{location}: object shape mismatch")
    return value


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _sub(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def _mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _scale_real(value: Fraction, scalar: Gaussian) -> Gaussian:
    return (value * scalar[0], value * scalar[1])


def _vsub(left: Vector, right: Vector) -> Vector:
    return [_sub(x, y) for x, y in zip(left, right)]


def _inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for x, y in zip(left, right):
        total = _add(total, _mul(_conj(x), y))
    return total


def _matvec(matrix: GMatrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = _add(total, _mul(coefficient, entry))
        result.append(total)
    return result


def _rmatvec(matrix: RMatrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = _add(total, _scale_real(coefficient, entry))
        result.append(total)
    return result


def _adjoint(matrix: GMatrix) -> GMatrix:
    size = len(matrix)
    return [[_conj(matrix[row][column]) for row in range(size)] for column in range(size)]


def _sum_positions(vector: Vector, positions: list[int]) -> Gaussian:
    total = ZERO
    for position in positions:
        total = _add(total, vector[position])
    return total


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _rank_data(x: Fraction) -> tuple[list[int], int, int, list[int], list[int], list[Fraction], Fraction]:
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    count = len(coordinates)
    if count < 2:
        raise CertificateError("rank midpoint requires N>=2")
    ell = count // 2
    right_size = count - ell
    left = coordinates[:ell]
    right = coordinates[ell:]
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    return coordinates, ell, right_size, left, right, h, Fraction(ell * right_size, count)


def _coarse_matrix(size: int) -> RMatrix:
    return [[Fraction(1, size) for _ in range(size)] for _ in range(size)]


def _mid_matrix(ell: int, right_size: int) -> RMatrix:
    size = ell + right_size
    return [
        [
            Fraction(1, ell)
            if row < ell and column < ell
            else Fraction(1, right_size)
            if row >= ell and column >= ell
            else Fraction(0)
            for column in range(size)
        ]
        for row in range(size)
    ]


def _contrast_projector(h: list[Fraction], rho_squared: Fraction) -> RMatrix:
    return [[rho_squared * left * right for right in h] for left in h]


def _within_child_covariance(w: Vector, g_vector: Vector, ell: int) -> Gaussian:
    total = ZERO
    for positions in (list(range(ell)), list(range(ell, len(w)))):
        mean_w = _scale_real(Fraction(1, len(positions)), _sum_positions(w, positions))
        mean_g = _scale_real(Fraction(1, len(positions)), _sum_positions(g_vector, positions))
        for position in positions:
            total = _add(
                total,
                _mul(_conj(_sub(w[position], mean_w)), _sub(g_vector[position], mean_g)),
            )
    return total


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def _prime_shell(x: Fraction) -> list[int]:
    result: list[int] = []
    q_value = 2
    while Fraction(q_value**3) <= 8 * x:
        if _is_prime(q_value) and x < q_value**3:
            result.append(q_value)
        q_value += 1
    return result


def _lambda_over_log(value: int) -> Fraction:
    for prime in range(2, value + 1):
        if not _is_prime(prime) or value % prime != 0:
            continue
        remainder = value
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        return Fraction(1, exponent) if remainder == 1 else Fraction(0)
    return Fraction(0)


def _mobius(value: int) -> int:
    remainder = value
    sign = 1
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            remainder //= prime
            sign = -sign
            if remainder % prime == 0:
                return 0
            while remainder % prime == 0:
                remainder //= prime
        prime += 1
    if remainder > 1:
        sign = -sign
    return sign


def _literal_beta(x: Fraction, coordinates: list[int]) -> Vector:
    result: Vector = []
    for coordinate in coordinates:
        divisor_sum = 0
        for divisor in range(1, coordinate + 1):
            if coordinate % divisor == 0 and divisor**400 * x.denominator**133 <= x.numerator**133:
                divisor_sum += _mobius(divisor)
        result.append((_lambda_over_log(coordinate) - divisor_sum, Fraction(0)))
    return result


def _expected_samples() -> dict[int, Gaussian]:
    return {
        -4: (Fraction(1, 2), Fraction(1, 3)),
        -3: (Fraction(-2, 3), Fraction(1, 5)),
        -2: (Fraction(3, 4), Fraction(-1, 6)),
        -1: (Fraction(2, 5), Fraction(1, 7)),
        1: (Fraction(-1, 3), Fraction(2, 7)),
        2: (Fraction(5, 6), Fraction(1, 4)),
        3: (Fraction(1, 5), Fraction(-2, 3)),
        4: (Fraction(-3, 7), Fraction(1, 2)),
    }


def _literal_matrix(coordinates: list[int], q_primes: list[int], samples: dict[int, Gaussian]) -> GMatrix:
    matrix: GMatrix = []
    for u in coordinates:
        row: list[Gaussian] = []
        for t in coordinates:
            total = ZERO
            if u != t:
                for q_value in q_primes:
                    if u % q_value == 0 or t % q_value == 0:
                        continue
                    residue = Fraction(1 if u % q_value == t % q_value else 0)
                    bracket = residue - Fraction(1, q_value - 1)
                    total = _add(total, _scale_real(Fraction(q_value) * bracket, samples[u - t]))
            row.append(total)
        matrix.append(row)
    return matrix


def _expanded_h_moment(
    coordinates: list[int], h: list[Fraction], q_primes: list[int],
    samples: dict[int, Gaussian], beta: Vector,
) -> Gaussian:
    total = ZERO
    for u_index, u in enumerate(coordinates):
        for t_index, t in enumerate(coordinates):
            if u == t:
                continue
            for q_value in q_primes:
                if u % q_value == 0 or t % q_value == 0:
                    continue
                residue = Fraction(1 if u % q_value == t % q_value else 0)
                bracket = residue - Fraction(1, q_value - 1)
                sampled = _scale_real(h[u_index] * q_value * bracket, samples[u - t])
                total = _add(total, _mul(sampled, beta[t_index]))
    return total


def _kernel_counts(
    coordinates: list[int], q_primes: list[int], beta: Vector, matrix: GMatrix
) -> dict[str, int]:
    mask_survivors = 0
    active = 0
    expansion = 0
    for u_index, u in enumerate(coordinates):
        for t_index, t in enumerate(coordinates):
            for q_value in q_primes:
                if u % q_value != 0 and t % q_value != 0:
                    mask_survivors += 1
                    if u != t:
                        active += 1
                        if beta[t_index] != ZERO and matrix[u_index][t_index] != ZERO:
                            expansion += 1
    return {
        "ordered_u_t_q_triplets": len(coordinates) ** 2 * len(q_primes),
        "deleted_diagonal_triplets": len(coordinates) * len(q_primes),
        "unit_mask_survivors_before_diagonal": mask_survivors,
        "active_operator_triplets": active,
        "nonzero_matrix_entries": sum(entry != ZERO for row in matrix for entry in row),
        "nonzero_beta_expansion_terms": expansion,
    }


def _expect_gaussian(raw: Any, expected: Gaussian, location: str) -> None:
    if _gaussian(raw, location) != expected:
        raise CertificateError(f"{location}: Gaussian value mismatch")


def _expect_vector(raw: Any, expected: Vector, location: str) -> None:
    if _vector(raw, len(expected), location) != expected:
        raise CertificateError(f"{location}: vector mismatch")


def _check_kernel(record: Any) -> Vector:
    required = {
        "label", "evidence_scope", "x", "coordinates", "H_definition", "Q_definition",
        "Q_x_definition", "q_primes", "kernel_sample_definition", "kernel_samples",
        "beta_definition", "beta", "A", "g", "h_A_beta", "h_literal_kernel_expansion",
        "A_star_h", "A_star_h_beta_pairing", "rho_crosswalk", "sample_matrix_self_adjoint",
        "factor_ledger", "counts",
    }
    data = _keys(record, required, "kernel_fixture")
    if data["label"] != KERNEL_FIXTURE_LABEL:
        raise CertificateError("kernel fixture nonliteral label mismatch")
    expected_strings = {
        "evidence_scope": "STRUCTURAL_EXACT_SAMPLE_REPLAY_NOT_ACTUAL_V59_NUMERICAL_DATA",
        "H_definition": "H=x^(21/32)",
        "Q_definition": "Q=x^(1/3)",
        "Q_x_definition": "q prime with Q<q<=2Q",
        "kernel_sample_definition": "K_H(h)=hat(psi_+)(h/H)",
        "beta_definition": "Lambda(t)/log(t)-sum_{d|t,d^400<=x^133}mu(d)",
        "rho_crosswalk": "<z,A_x beta>=rho<h,A_x beta>=rho<A_x^*h,beta>",
        "sample_matrix_self_adjoint": "NO_NONLITERAL_SAMPLE_ONLY_NO_CLAIM_FOR_LITERAL_A_X",
    }
    for key, expected in expected_strings.items():
        if data[key] != expected:
            raise CertificateError(f"kernel fixture {key} mismatch")
    x = _fraction(data["x"], "kernel.x")
    if x != Fraction(21, 2):
        raise CertificateError("kernel fixture x changed")
    coordinates, ell, _r, _left, _right, h, _rho_squared = _rank_data(x)
    if _integer_list(data["coordinates"], "kernel.coordinates") != coordinates:
        raise CertificateError("kernel coordinates mismatch")
    q_primes = _integer_list(data["q_primes"], "kernel.q_primes")
    if q_primes != _prime_shell(x) or q_primes != [3]:
        raise CertificateError("kernel exact prime shell mismatch")
    raw_samples = _keys(
        data["kernel_samples"], {str(key) for key in _expected_samples()}, "kernel.samples"
    )
    samples = {int(key): _gaussian(value, f"kernel.samples.{key}") for key, value in raw_samples.items()}
    if samples != _expected_samples():
        raise CertificateError("kernel exact sample table mismatch")
    beta = _vector(data["beta"], len(coordinates), "kernel.beta")
    if beta != _literal_beta(x, coordinates):
        raise CertificateError("kernel literal beta semantics mismatch")
    matrix = _gmatrix(data["A"], len(coordinates), "kernel.A")
    expected_matrix = _literal_matrix(coordinates, q_primes, samples)
    if matrix != expected_matrix:
        raise CertificateError("literal TPC-247 sampled A_x formula mismatch")
    g_vector = _vector(data["g"], len(coordinates), "kernel.g")
    if g_vector != _matvec(matrix, beta):
        raise CertificateError("kernel g=A_x beta mismatch")
    h_vector = [(entry, Fraction(0)) for entry in h]
    direct = _inner(h_vector, g_vector)
    expanded = _expanded_h_moment(coordinates, h, q_primes, samples, beta)
    adjoint_h = _matvec(_adjoint(matrix), h_vector)
    adjoint_pairing = _inner(adjoint_h, beta)
    _expect_gaussian(data["h_A_beta"], direct, "kernel.h_A_beta")
    _expect_gaussian(data["h_literal_kernel_expansion"], expanded, "kernel.expansion")
    _expect_vector(data["A_star_h"], adjoint_h, "kernel.A_star_h")
    _expect_gaussian(data["A_star_h_beta_pairing"], adjoint_pairing, "kernel.adjoint_pairing")
    if direct != expanded or direct != adjoint_pairing:
        raise CertificateError("literal expansion or safe adjoint equality failed")
    if matrix == _adjoint(matrix):
        raise CertificateError("kernel fixture no longer detects unsafe self-adjoint substitution")
    expected_ledger = {
        "output_input_orientation": "A_x(u,t)",
        "outer_prime_weight": "q",
        "unit_masks": "1_(q does not divide u)1_(q does not divide t)",
        "deleted_diagonal": "1_(u!=t)",
        "physical_kernel": "K_H(u-t)",
        "centered_residue_bracket": "1_(u=t mod q)-1/(q-1)",
        "literal_input": "beta(t)",
    }
    if data["factor_ledger"] != expected_ledger:
        raise CertificateError("kernel literal-factor ledger mismatch")
    expected_counts = _kernel_counts(coordinates, q_primes, beta, matrix)
    counts = _keys(data["counts"], set(expected_counts), "kernel.counts")
    for key, expected in expected_counts.items():
        if _integer(counts[key], f"kernel.counts.{key}") != expected:
            raise CertificateError(f"kernel count mismatch: {key}")
    if ell != 2:
        raise CertificateError("kernel/midpoint shared rank changed")
    return g_vector


def _check_midpoint(record: Any, expected_g: Vector) -> None:
    required = {
        "label", "x", "coordinates", "N", "ell", "r", "L", "R", "rho_squared",
        "h", "h_sum", "z_norm_squared", "exact_radical_policy", "projectors", "w", "g",
        "partial_sums", "derived",
    }
    data = _keys(record, required, "midpoint_fixture")
    if data["label"] != "EXACT_GAUSSIAN_RATIONAL_ODD_RANK_MIDPOINT_REPLAY":
        raise CertificateError("midpoint fixture label mismatch")
    if data["exact_radical_policy"] != "STORE_RHO_SQUARED_H_I_H_J_NEVER_FLOAT_RHO":
        raise CertificateError("midpoint exact-radical policy mismatch")
    x = _fraction(data["x"], "midpoint.x")
    if x != Fraction(21, 2):
        raise CertificateError("midpoint x changed")
    coordinates, ell, right_size, left, right, h, rho_squared = _rank_data(x)
    size = len(coordinates)
    for key, value, expected in (
        ("N", data["N"], size), ("ell", data["ell"], ell), ("r", data["r"], right_size)
    ):
        if _integer(value, f"midpoint.{key}") != expected:
            raise CertificateError(f"midpoint {key} mismatch")
    for key, raw, expected in (
        ("coordinates", data["coordinates"], coordinates),
        ("L", data["L"], left),
        ("R", data["R"], right),
    ):
        if _integer_list(raw, f"midpoint.{key}") != expected:
            raise CertificateError(f"midpoint {key} mismatch")
    raw_h = data["h"]
    if not isinstance(raw_h, list) or len(raw_h) != size:
        raise CertificateError("midpoint h shape mismatch")
    parsed_h = [_fraction(entry, f"midpoint.h[{index}]") for index, entry in enumerate(raw_h)]
    if parsed_h != h or _fraction(data["rho_squared"], "midpoint.rho_squared") != rho_squared:
        raise CertificateError("midpoint h or rho-squared mismatch")
    if _fraction(data["h_sum"], "midpoint.h_sum") != 0:
        raise CertificateError("midpoint h does not annihilate constants")
    unit = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    if unit != 1 or _fraction(data["z_norm_squared"], "midpoint.z_norm_squared") != unit:
        raise CertificateError("midpoint contrast normalization mismatch")
    projectors = _keys(data["projectors"], {"M_coarse", "M_mid", "z_tensor_z", "identity"}, "midpoint.projectors")
    if projectors["identity"] != "M_mid=M_coarse+z tensor z":
        raise CertificateError("midpoint projector identity label mismatch")
    coarse = _rmatrix(projectors["M_coarse"], size, "midpoint.M_coarse")
    midpoint = _rmatrix(projectors["M_mid"], size, "midpoint.M_mid")
    projector = _rmatrix(projectors["z_tensor_z"], size, "midpoint.z_tensor_z")
    expected_coarse = _coarse_matrix(size)
    expected_mid = _mid_matrix(ell, right_size)
    expected_projector = _contrast_projector(h, rho_squared)
    if coarse != expected_coarse or midpoint != expected_mid or projector != expected_projector:
        raise CertificateError("midpoint exact rational projector matrices mismatch")
    if any(midpoint[i][j] != coarse[i][j] + projector[i][j] for i in range(size) for j in range(size)):
        raise CertificateError("M_mid=M_coarse+z tensor z failed")
    expected_w = [
        (Fraction(2), Fraction(1, 3)),
        (Fraction(-1, 2), Fraction(2)),
        (Fraction(3, 2), Fraction(-1)),
        (Fraction(-2), Fraction(1, 4)),
        (Fraction(1), Fraction(3, 2)),
    ]
    w = _vector(data["w"], size, "midpoint.w")
    g_vector = _vector(data["g"], size, "midpoint.g")
    if w != expected_w or g_vector != expected_g:
        raise CertificateError("midpoint release w/g fixture changed")
    coarse_w = _rmatvec(coarse, w)
    coarse_g = _rmatvec(coarse, g_vector)
    midpoint_w = _rmatvec(midpoint, w)
    midpoint_g = _rmatvec(midpoint, g_vector)
    left_positions = list(range(ell))
    right_positions = list(range(ell, size))
    w_left = _sum_positions(w, left_positions)
    w_right = _sum_positions(w, right_positions)
    g_left = _sum_positions(g_vector, left_positions)
    g_right = _sum_positions(g_vector, right_positions)
    h_w = _sub(_scale_real(Fraction(1, ell), w_left), _scale_real(Fraction(1, right_size), w_right))
    h_g = _sub(_scale_real(Fraction(1, ell), g_left), _scale_real(Fraction(1, right_size), g_right))
    partial = _keys(data["partial_sums"], {"W_L", "W_R", "G_L", "G_R", "h_moment_w", "h_moment_g"}, "midpoint.partial_sums")
    for key, expected in (
        ("W_L", w_left), ("W_R", w_right), ("G_L", g_left), ("G_R", g_right),
        ("h_moment_w", h_w), ("h_moment_g", h_g),
    ):
        _expect_gaussian(partial[key], expected, "midpoint.partial_sums." + key)
    transfer = _scale_real(rho_squared, _mul(_conj(h_w), h_g))
    unconjugated = _scale_real(rho_squared, _mul(h_w, h_g))
    if transfer == unconjugated:
        raise CertificateError("midpoint fixture does not detect first-slot conjugation")
    c_coarse_formula = _scale_real(
        Fraction(1, size), _mul(_conj(_add(w_left, w_right)), _add(g_left, g_right))
    )
    c_mid_formula = _add(
        _scale_real(Fraction(1, ell), _mul(_conj(w_left), g_left)),
        _scale_real(Fraction(1, right_size), _mul(_conj(w_right), g_right)),
    )
    c_coarse = _inner(coarse_w, coarse_g)
    c_mid = _inner(midpoint_w, midpoint_g)
    q_coarse = _inner(_vsub(w, coarse_w), _vsub(g_vector, coarse_g))
    q_mid = _inner(_vsub(w, midpoint_w), _vsub(g_vector, midpoint_g))
    within = _within_child_covariance(w, g_vector, ell)
    scalar = _inner(w, g_vector)
    if c_coarse != c_coarse_formula or c_mid != c_mid_formula:
        raise CertificateError("midpoint longitudinal partial-sum formulas failed")
    if c_mid != _add(c_coarse, transfer) or q_mid != _sub(q_coarse, transfer):
        raise CertificateError("midpoint covariance/opposite-Q transfer failed")
    if within != q_mid or scalar != _add(c_coarse, q_coarse) or scalar != _add(c_mid, q_mid):
        raise CertificateError("midpoint within-child or scalar decomposition failed")
    derived_expected_vectors = {
        "M_coarse_w": coarse_w, "M_mid_w": midpoint_w,
        "M_coarse_g": coarse_g, "M_mid_g": midpoint_g,
    }
    derived_expected_scalars = {
        "C_x": scalar,
        "C_long_coarse": c_coarse,
        "C_long_coarse_partial_sum": c_coarse_formula,
        "C_long_mid": c_mid,
        "C_long_mid_partial_sum": c_mid_formula,
        "conjugate_first_transfer": transfer,
        "Q_trans_coarse": q_coarse,
        "Q_trans_mid": q_mid,
        "opposite_Q_update": _scale_real(Fraction(-1), transfer),
        "within_child_covariance": within,
    }
    derived = _keys(data["derived"], set(derived_expected_vectors) | set(derived_expected_scalars), "midpoint.derived")
    for key, expected in derived_expected_vectors.items():
        _expect_vector(derived[key], expected, "midpoint.derived." + key)
    for key, expected in derived_expected_scalars.items():
        _expect_gaussian(derived[key], expected, "midpoint.derived." + key)


def _check_crosswalk(value: Any) -> None:
    if not isinstance(value, list) or len(value) != 8:
        raise CertificateError("integer crosswalk row count mismatch")
    keys = {"x", "x_mod_4", "N", "ell", "r", "left_endpoint", "floor_3x_over_4", "L", "R"}
    residues: set[int] = set()
    for row_index, row in enumerate(value):
        data = _keys(row, keys, f"crosswalk[{row_index}]")
        integer_x = _integer(data["x"], f"crosswalk[{row_index}].x")
        if integer_x != row_index + 3:
            raise CertificateError("integer crosswalk representative changed")
        coordinates, ell, right_size, left, right, _h, _rho_squared = _rank_data(Fraction(integer_x))
        expected_ints = {
            "x_mod_4": integer_x % 4,
            "N": len(coordinates),
            "ell": ell,
            "r": right_size,
            "left_endpoint": integer_x // 2 + ell,
            "floor_3x_over_4": (3 * integer_x) // 4,
        }
        for key, expected in expected_ints.items():
            if _integer(data[key], f"crosswalk[{row_index}].{key}") != expected:
                raise CertificateError(f"integer crosswalk {key} mismatch")
        if expected_ints["left_endpoint"] != expected_ints["floor_3x_over_4"]:
            raise CertificateError("integer floor(3x/4) crosswalk failed")
        if _integer_list(data["L"], f"crosswalk[{row_index}].L") != left:
            raise CertificateError("integer crosswalk L mismatch")
        if _integer_list(data["R"], f"crosswalk[{row_index}].R") != right:
            raise CertificateError("integer crosswalk R mismatch")
        residues.add(expected_ints["x_mod_4"])
    if residues != {0, 1, 2, 3}:
        raise CertificateError("integer crosswalk does not cover all residue classes")


def _check_controls(record: Any, midpoint: dict[str, Any]) -> None:
    data = _keys(
        record,
        {"label", "literal_status", "constant_factor_annihilation", "sign_controls", "conclusion"},
        "synthetic_controls",
    )
    if data["label"] != CONTROL_LABEL or data["literal_status"] != "NOT_LITERAL_NUMERICAL_V59_INSTANCES":
        raise CertificateError("synthetic controls are not labeled nonliteral")
    if data["conclusion"] != "SOURCE_FREE_GEOMETRY_DOES_NOT_DECIDE_SIGN_NONZERO_OR_SCALE":
        raise CertificateError("synthetic-control conclusion mismatch")
    h = [_fraction(entry, "controls.h") for entry in midpoint["h"]]
    rho_squared = _fraction(midpoint["rho_squared"], "controls.rho_squared")
    h_sum = sum(h, Fraction(0))
    unit = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    constant = _keys(
        data["constant_factor_annihilation"],
        {"sum_h", "constant_w_transfer", "constant_g_transfer"},
        "controls.constant",
    )
    if any(_fraction(constant[key], "controls.constant." + key) != 0 for key in constant):
        raise CertificateError("constant factor did not annihilate the contrast")
    rows = data["sign_controls"]
    if not isinstance(rows, list) or len(rows) != 2:
        raise CertificateError("synthetic sign-control count mismatch")
    expected = [("z", "z", unit), ("z", "-z", -unit)]
    for index, (row, (w_label, g_label, transfer)) in enumerate(zip(rows, expected)):
        item = _keys(row, {"w", "g", "transfer"}, f"controls.sign[{index}]")
        if item["w"] != w_label or item["g"] != g_label:
            raise CertificateError("synthetic sign-control labels mismatch")
        if _fraction(item["transfer"], f"controls.sign[{index}].transfer") != transfer:
            raise CertificateError("synthetic sign-control transfer mismatch")
    if h_sum != 0 or unit != 1:
        raise CertificateError("synthetic control geometry mismatch")


def check_document(document: Any) -> None:
    top = _keys(document, {"schema", "payload", "digest"}, "document")
    if top["schema"] != SCHEMA:
        raise CertificateError("schema mismatch")
    payload = top["payload"]
    if not isinstance(payload, dict) or not isinstance(top["digest"], str):
        raise CertificateError("payload/digest type mismatch")
    if _digest(payload) != top["digest"]:
        raise CertificateError("payload digest mismatch")
    required = {
        "claim_status", "maximum_claim", "evidence_label", "source_lock", "definitions",
        "firewall", "midpoint_fixture", "integer_crosswalk", "kernel_fixture",
        "synthetic_controls", "counts",
    }
    _keys(payload, required, "payload")
    if payload["claim_status"] != CLAIM_STATUS or payload["maximum_claim"] != MAXIMUM_CLAIM:
        raise CertificateError("claim status or maximum claim mismatch")
    if payload["evidence_label"] != "EXACT_RATIONAL_STRUCTURAL_REPRODUCTION_ONLY":
        raise CertificateError("evidence label mismatch")
    expected_source = {
        "baseline_HEAD": BASELINE_HEAD,
        "handoff_sha256": HANDOFF_SHA256,
        "source_frozen_bridge": "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md",
        "source_digests": SOURCE_DIGESTS,
        "inner_product": "conjugate-linear first",
        "literal_scalar": "C_x=<w,A_x beta>",
    }
    if payload["source_lock"] != expected_source:
        raise CertificateError("source lock mismatch")
    expected_definitions = {
        "physical_interval": "I_x=(x/2,x] intersect Z in increasing order",
        "rank_midpoint": "ell=floor(N/2), r=N-ell, L=first ell coordinates, R=remaining r",
        "contrast": "z=rho(1_L/ell-1_R/r), rho^2=ell*r/N",
        "exact_projector": "(z tensor z)_(i,j)=rho^2*h_i*h_j",
        "partial_sum_moment": "<z,f>=rho(S_f(L)/ell-S_f(R)/r)",
        "adjoint": "(A_x^*z)(t)=sum_u conjugate(A_x(u,t))z(u)",
    }
    if payload["definitions"] != expected_definitions:
        raise CertificateError("definition ledger mismatch")
    if payload["firewall"] != FIREWALL:
        raise CertificateError("claim firewall mismatch")
    expected_counts = {
        "rank_midpoint_replays": 1,
        "nonintegral_rational_x_replays": 1,
        "integer_crosswalk_rows": 8,
        "integer_residue_classes_covered": 4,
        "literal_kernel_formula_replays": 1,
        "safe_adjoint_replays": 1,
        "constant_annihilation_controls": 2,
        "sign_controls": 2,
    }
    counts = _keys(payload["counts"], set(expected_counts), "counts")
    for key, expected in expected_counts.items():
        if _integer(counts[key], "counts." + key) != expected:
            raise CertificateError(f"count mismatch: {key}")
    g_vector = _check_kernel(payload["kernel_fixture"])
    _check_midpoint(payload["midpoint_fixture"], g_vector)
    _check_crosswalk(payload["integer_crosswalk"])
    _check_controls(payload["synthetic_controls"], payload["midpoint_fixture"])


def _strict_loads(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CertificateError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> Any:
        raise CertificateError(f"nonfinite JSON token: {value}")

    try:
        return json.loads(text, object_pairs_hook=hook, parse_constant=reject_constant)
    except json.JSONDecodeError as error:
        raise CertificateError(f"invalid JSON: {error}") from error


def _validate_raw(raw_text: str) -> dict[str, Any]:
    document = _strict_loads(raw_text)
    check_document(document)
    if raw_text != _canonical(document).decode("ascii") + "\n":
        raise CertificateError("certificate bytes are not canonical strict JSON")
    return document


def _rebind(document: dict[str, Any]) -> None:
    document["digest"] = _digest(document["payload"])


def _reject_document(document: dict[str, Any], label: str, rebind: bool = True) -> None:
    if rebind:
        _rebind(document)
    try:
        check_document(document)
    except CertificateError:
        return
    raise CertificateError(f"mutation accepted: {label}")


def _reject_raw(raw_text: str, label: str) -> None:
    try:
        _validate_raw(raw_text)
    except CertificateError:
        return
    raise CertificateError(f"raw mutation accepted: {label}")


def run_mutations(document: dict[str, Any], raw_text: str) -> int:
    cases: list[tuple[str, dict[str, Any], bool]] = []

    def add_case(label: str, mutated: dict[str, Any], rebind: bool = True) -> None:
        cases.append((label, mutated, rebind))

    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["N"] = True
    add_case("typed_bool_N", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["coordinates"][0] = True
    add_case("typed_bool_coordinate", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["counts"]["rank_midpoint_replays"] = True
    add_case("typed_bool_count", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["integer_crosswalk"][0]["x"] = True
    add_case("typed_bool_crosswalk_integer", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["rho_squared"] = "12/10"
    add_case("noncanonical_rational", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["x"] = "11"
    add_case("rank_clock", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["coordinates"][0] = 7
    add_case("ordered_coordinates", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["ell"] = 3
    add_case("left_rank", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["r"] = 2
    add_case("right_rank", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["rho_squared"] = "1"
    add_case("rho_squared", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["h"][0] = "1/3"
    add_case("rank_midpoint_h", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["projectors"]["z_tensor_z"][0][0] = "0"
    add_case("exact_projector_product", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["projectors"]["M_coarse"][0][0] = "1/4"
    add_case("coarse_projector", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["projectors"]["M_mid"][0][0] = "1/3"
    add_case("midpoint_projector", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["w"][0] = ["0", "0"]
    add_case("w_fixture", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["g"][1] = ["0", "0"]
    add_case("g_fixture", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["partial_sums"]["W_L"] = ["0", "0"]
    add_case("partial_sum_W_L", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["partial_sums"]["h_moment_w"] = ["0", "0"]
    add_case("partial_sum_contrast", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["derived"]["C_long_coarse"] = ["0", "0"]
    add_case("coarse_longitudinal", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["derived"]["C_long_mid"] = ["0", "0"]
    add_case("mid_longitudinal", mutated)
    mutated = copy.deepcopy(document)
    transfer = mutated["payload"]["midpoint_fixture"]["derived"]["conjugate_first_transfer"]
    transfer[1] = str(-Fraction(transfer[1]))
    add_case("conjugate_first_transfer", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["derived"]["opposite_Q_update"] = ["0", "0"]
    add_case("opposite_Q_update", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["derived"]["Q_trans_mid"] = ["0", "0"]
    add_case("Q_trans_mid", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["midpoint_fixture"]["derived"]["within_child_covariance"] = ["0", "0"]
    add_case("within_child_covariance", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["label"] = "LITERAL_NUMERICAL_V59_REPLAY"
    add_case("kernel_literal_confusion", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["q_primes"][0] = 5
    add_case("prime_shell", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["kernel_samples"]["-1"] = ["0", "0"]
    add_case("kernel_sample", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["beta"][2] = ["1/2", "0"]
    add_case("literal_beta", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["A"][1][2] = ["0", "0"]
    add_case("literal_A_factor_compiler", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["g"][1] = ["0", "0"]
    add_case("kernel_g", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["h_literal_kernel_expansion"] = ["0", "0"]
    add_case("literal_kernel_expansion", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["A_star_h"][0] = ["1", "0"]
    add_case("adjoint_vector", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["A_star_h_beta_pairing"] = ["0", "0"]
    add_case("safe_adjoint_pairing", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["sample_matrix_self_adjoint"] = "YES"
    add_case("self_adjoint_promotion", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["factor_ledger"]["deleted_diagonal"] = "NONE"
    add_case("deleted_diagonal_factor", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["kernel_fixture"]["counts"]["active_operator_triplets"] = True
    add_case("typed_bool_nested_count", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["integer_crosswalk"][0]["floor_3x_over_4"] = 3
    add_case("integer_crosswalk_threshold", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["synthetic_controls"]["label"] = "LITERAL_V59_CONTROLS"
    add_case("synthetic_label", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["synthetic_controls"]["constant_factor_annihilation"]["constant_w_transfer"] = "1"
    add_case("constant_annihilation", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["synthetic_controls"]["sign_controls"][0]["transfer"] = "-1"
    add_case("positive_sign_control", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["synthetic_controls"]["sign_controls"][1]["transfer"] = "1"
    add_case("negative_sign_control", mutated)
    for key, value, label in (
        ("TPC253_A_X_SELF_ADJOINTNESS", "PROVED", "firewall_self_adjointness"),
        ("TPC253_MIDPOINT_V59_CANONICALITY", "PROVED", "firewall_canonicality"),
        ("TPC253_SMOOTH_V59_PARTITION_IDENTIFICATION", "PROVED", "firewall_smooth_partition"),
        ("TPC253_MIDPOINT_CONTRAST_SIGN_OR_NONZERO", "PROVED_POSITIVE", "firewall_sign"),
        ("TPC253_ASYMPTOTIC_ADVANCE", "YES", "firewall_asymptotic"),
        ("TPC253_ARITHMETIC_ADVANCE", "YES", "firewall_arithmetic"),
        ("TPC253_L2", "PROVED", "firewall_L2"),
        ("TPC253_FULL_GATE_B", "CLOSED", "firewall_gate_B"),
        ("TPC253_FULL_GATE_B_STRICT_1_OVER_400", "PAID", "firewall_one_over_400"),
        ("TPC253_TWIN_PRIME_RESULT", "PROVED", "firewall_twin_prime"),
    ):
        mutated = copy.deepcopy(document)
        mutated["payload"]["firewall"][key] = value
        add_case(label, mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["source_lock"]["handoff_sha256"] = "0" * 64
    add_case("handoff_hash", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["source_lock"]["source_digests"]["source_frozen_tpc253_bridge"] = "0" * 64
    add_case("bridge_hash", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["maximum_claim"] = "ARITHMETIC_THEOREM"
    add_case("maximum_claim", mutated)
    mutated = copy.deepcopy(document)
    mutated["payload"]["counts"]["integer_crosswalk_rows"] = 9
    add_case("count_semantics", mutated)
    stale = copy.deepcopy(document)
    stale["payload"]["midpoint_fixture"]["derived"]["C_x"] = ["0", "0"]
    add_case("stale_digest", stale, False)

    for label, mutated, rebind in cases:
        _reject_document(mutated, label, rebind)
    duplicate = raw_text.replace('"schema":', '"schema":"DUPLICATE","schema":', 1)
    _reject_raw(duplicate, "duplicate_json_key")
    nonfinite = raw_text.replace("{", '{"rogue":NaN,', 1)
    _reject_raw(nonfinite, "nonfinite_json_token")
    _reject_raw(raw_text[:-1] + " \n", "noncanonical_bytes")
    return len(cases) + 3


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate release and run mutations")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc253_certificate.json",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("the independent checker is read-only; pass --check")
    try:
        raw_text = args.input.read_text(encoding="ascii")
        document = _validate_raw(raw_text)
        mutation_count = run_mutations(document, raw_text)
    except (OSError, UnicodeError, CertificateError) as error:
        print(f"FAIL {error}")
        return 1
    print(
        f"PASS {SCHEMA} digest={document['digest']} mutations_rejected={mutation_count} "
        "midpoint=1 crosswalk=8 kernel=1 adjoint=1 controls=4 canonical_bytes=1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
