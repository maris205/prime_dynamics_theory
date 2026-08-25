#!/usr/bin/env python3
"""Produce the exact TPC-253 rank-midpoint contrast certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
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


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _document_text(value: Any) -> str:
    return _canonical(value).decode("ascii") + "\n"


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _q(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _g(real: int | str | Fraction, imag: int | str | Fraction = 0) -> Gaussian:
    return (_q(real), _q(imag))


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


def _vadd(left: Vector, right: Vector) -> Vector:
    return [_add(x, y) for x, y in zip(left, right)]


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
        raise ValueError("rank midpoint requires N>=2")
    ell = count // 2
    right_size = count - ell
    left = coordinates[:ell]
    right = coordinates[ell:]
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, count)
    return coordinates, ell, right_size, left, right, h, rho_squared


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


def _matrix_add(left: RMatrix, right: RMatrix) -> RMatrix:
    return [
        [left[row][column] + right[row][column] for column in range(len(left))]
        for row in range(len(left))
    ]


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
    values: Vector = []
    for coordinate in coordinates:
        divisor_sum = 0
        for divisor in range(1, coordinate + 1):
            if coordinate % divisor != 0:
                continue
            if divisor**400 * x.denominator**133 <= x.numerator**133:
                divisor_sum += _mobius(divisor)
        values.append(_g(_lambda_over_log(coordinate) - divisor_sum))
    return values


def _kernel_samples() -> dict[int, Gaussian]:
    return {
        -4: _g("1/2", "1/3"),
        -3: _g("-2/3", "1/5"),
        -2: _g("3/4", "-1/6"),
        -1: _g("2/5", "1/7"),
        1: _g("-1/3", "2/7"),
        2: _g("5/6", "1/4"),
        3: _g("1/5", "-2/3"),
        4: _g("-3/7", "1/2"),
    }


def _literal_sample_matrix(
    coordinates: list[int], q_primes: list[int], samples: dict[int, Gaussian]
) -> GMatrix:
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
                    total = _add(
                        total,
                        _scale_real(Fraction(q_value) * bracket, samples[u - t]),
                    )
            row.append(total)
        matrix.append(row)
    return matrix


def _kernel_counts(
    coordinates: list[int], q_primes: list[int], beta: Vector, matrix: GMatrix
) -> dict[str, int]:
    ordered = len(coordinates) * len(coordinates) * len(q_primes)
    deleted = len(coordinates) * len(q_primes)
    mask_survivors = 0
    post_diagonal = 0
    expansion = 0
    for u_index, u in enumerate(coordinates):
        for t_index, t in enumerate(coordinates):
            for q_value in q_primes:
                if u % q_value != 0 and t % q_value != 0:
                    mask_survivors += 1
                    if u != t:
                        post_diagonal += 1
                        if beta[t_index] != ZERO and matrix[u_index][t_index] != ZERO:
                            expansion += 1
    nonzero_matrix = sum(entry != ZERO for row in matrix for entry in row)
    return {
        "ordered_u_t_q_triplets": ordered,
        "deleted_diagonal_triplets": deleted,
        "unit_mask_survivors_before_diagonal": mask_survivors,
        "active_operator_triplets": post_diagonal,
        "nonzero_matrix_entries": nonzero_matrix,
        "nonzero_beta_expansion_terms": expansion,
    }


def _expanded_h_moment(
    coordinates: list[int],
    h: list[Fraction],
    q_primes: list[int],
    samples: dict[int, Gaussian],
    beta: Vector,
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
                factor = h[u_index] * q_value * bracket
                total = _add(total, _mul(_scale_real(factor, samples[u - t]), beta[t_index]))
    return total


def _encode_scalar(value: Gaussian) -> list[str]:
    return [str(value[0]), str(value[1])]


def _encode_vector(vector: Vector) -> list[list[str]]:
    return [_encode_scalar(entry) for entry in vector]


def _encode_gmatrix(matrix: GMatrix) -> list[list[list[str]]]:
    return [_encode_vector(row) for row in matrix]


def _encode_rmatrix(matrix: RMatrix) -> list[list[str]]:
    return [[str(entry) for entry in row] for row in matrix]


def _kernel_fixture() -> tuple[dict[str, Any], Vector]:
    x = Fraction(21, 2)
    coordinates, ell, right_size, _left, _right, h, _rho_squared = _rank_data(x)
    q_primes = _prime_shell(x)
    samples = _kernel_samples()
    beta = _literal_beta(x, coordinates)
    matrix = _literal_sample_matrix(coordinates, q_primes, samples)
    g_vector = _matvec(matrix, beta)
    h_vector = [_g(entry) for entry in h]
    direct = _inner(h_vector, g_vector)
    expanded = _expanded_h_moment(coordinates, h, q_primes, samples, beta)
    adjoint_h = _matvec(_adjoint(matrix), h_vector)
    adjoint_pairing = _inner(adjoint_h, beta)
    if q_primes != [3]:
        raise ValueError("literal prime-shell fixture changed")
    if beta != [_g(0), _g(0), _g(Fraction(1, 3)), _g(Fraction(-1, 2)), _g(0)]:
        raise ValueError("literal beta fixture changed")
    if direct != expanded or direct != adjoint_pairing:
        raise ValueError("kernel expansion or safe adjoint identity failed")
    if matrix == _adjoint(matrix):
        raise ValueError("non-self-adjoint audit fixture became self-adjoint")
    return {
        "label": KERNEL_FIXTURE_LABEL,
        "evidence_scope": "STRUCTURAL_EXACT_SAMPLE_REPLAY_NOT_ACTUAL_V59_NUMERICAL_DATA",
        "x": str(x),
        "coordinates": coordinates,
        "H_definition": "H=x^(21/32)",
        "Q_definition": "Q=x^(1/3)",
        "Q_x_definition": "q prime with Q<q<=2Q",
        "q_primes": q_primes,
        "kernel_sample_definition": "K_H(h)=hat(psi_+)(h/H)",
        "kernel_samples": {str(key): _encode_scalar(value) for key, value in samples.items()},
        "beta_definition": "Lambda(t)/log(t)-sum_{d|t,d^400<=x^133}mu(d)",
        "beta": _encode_vector(beta),
        "A": _encode_gmatrix(matrix),
        "g": _encode_vector(g_vector),
        "h_A_beta": _encode_scalar(direct),
        "h_literal_kernel_expansion": _encode_scalar(expanded),
        "A_star_h": _encode_vector(adjoint_h),
        "A_star_h_beta_pairing": _encode_scalar(adjoint_pairing),
        "rho_crosswalk": "<z,A_x beta>=rho<h,A_x beta>=rho<A_x^*h,beta>",
        "sample_matrix_self_adjoint": "NO_NONLITERAL_SAMPLE_ONLY_NO_CLAIM_FOR_LITERAL_A_X",
        "factor_ledger": {
            "output_input_orientation": "A_x(u,t)",
            "outer_prime_weight": "q",
            "unit_masks": "1_(q does not divide u)1_(q does not divide t)",
            "deleted_diagonal": "1_(u!=t)",
            "physical_kernel": "K_H(u-t)",
            "centered_residue_bracket": "1_(u=t mod q)-1/(q-1)",
            "literal_input": "beta(t)",
        },
        "counts": _kernel_counts(coordinates, q_primes, beta, matrix),
    }, g_vector


def _midpoint_fixture(g_vector: Vector) -> dict[str, Any]:
    x = Fraction(21, 2)
    coordinates, ell, right_size, left, right, h, rho_squared = _rank_data(x)
    size = len(coordinates)
    w = [
        _g(2, "1/3"),
        _g("-1/2", 2),
        _g("3/2", -1),
        _g(-2, "1/4"),
        _g(1, "3/2"),
    ]
    coarse = _coarse_matrix(size)
    midpoint = _mid_matrix(ell, right_size)
    projector = _contrast_projector(h, rho_squared)
    if midpoint != _matrix_add(coarse, projector):
        raise ValueError("exact rational projector update failed")
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
    transfer = _scale_real(rho_squared, _mul(_conj(h_w), h_g))
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
    h_sum = sum(h, Fraction(0))
    z_norm_squared = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    if h_sum != 0 or z_norm_squared != 1:
        raise ValueError("rank-midpoint contrast normalization failed")
    if c_coarse != c_coarse_formula or c_mid != c_mid_formula:
        raise ValueError("partial-sum longitudinal formulas failed")
    if c_mid != _add(c_coarse, transfer):
        raise ValueError("conjugate-first covariance transfer failed")
    if q_mid != _sub(q_coarse, transfer):
        raise ValueError("opposite transverse covariance update failed")
    if within != q_mid:
        raise ValueError("within-child covariance failed")
    if scalar != _add(c_coarse, q_coarse) or scalar != _add(c_mid, q_mid):
        raise ValueError("coarse or midpoint scalar decomposition failed")
    return {
        "label": "EXACT_GAUSSIAN_RATIONAL_ODD_RANK_MIDPOINT_REPLAY",
        "x": str(x),
        "coordinates": coordinates,
        "N": size,
        "ell": ell,
        "r": right_size,
        "L": left,
        "R": right,
        "rho_squared": str(rho_squared),
        "h": [str(entry) for entry in h],
        "h_sum": str(h_sum),
        "z_norm_squared": str(z_norm_squared),
        "exact_radical_policy": "STORE_RHO_SQUARED_H_I_H_J_NEVER_FLOAT_RHO",
        "projectors": {
            "M_coarse": _encode_rmatrix(coarse),
            "M_mid": _encode_rmatrix(midpoint),
            "z_tensor_z": _encode_rmatrix(projector),
            "identity": "M_mid=M_coarse+z tensor z",
        },
        "w": _encode_vector(w),
        "g": _encode_vector(g_vector),
        "partial_sums": {
            "W_L": _encode_scalar(w_left),
            "W_R": _encode_scalar(w_right),
            "G_L": _encode_scalar(g_left),
            "G_R": _encode_scalar(g_right),
            "h_moment_w": _encode_scalar(h_w),
            "h_moment_g": _encode_scalar(h_g),
        },
        "derived": {
            "M_coarse_w": _encode_vector(coarse_w),
            "M_mid_w": _encode_vector(midpoint_w),
            "M_coarse_g": _encode_vector(coarse_g),
            "M_mid_g": _encode_vector(midpoint_g),
            "C_x": _encode_scalar(scalar),
            "C_long_coarse": _encode_scalar(c_coarse),
            "C_long_coarse_partial_sum": _encode_scalar(c_coarse_formula),
            "C_long_mid": _encode_scalar(c_mid),
            "C_long_mid_partial_sum": _encode_scalar(c_mid_formula),
            "conjugate_first_transfer": _encode_scalar(transfer),
            "Q_trans_coarse": _encode_scalar(q_coarse),
            "Q_trans_mid": _encode_scalar(q_mid),
            "opposite_Q_update": _encode_scalar(_scale_real(Fraction(-1), transfer)),
            "within_child_covariance": _encode_scalar(within),
        },
    }


def _integer_crosswalk() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for integer_x in range(3, 11):
        coordinates, ell, right_size, left, right, _h, _rho_squared = _rank_data(Fraction(integer_x))
        endpoint = integer_x // 2 + ell
        threshold = (3 * integer_x) // 4
        if endpoint != threshold or left != [n for n in coordinates if n <= threshold]:
            raise ValueError("integer three-quarter crosswalk failed")
        rows.append({
            "x": integer_x,
            "x_mod_4": integer_x % 4,
            "N": len(coordinates),
            "ell": ell,
            "r": right_size,
            "left_endpoint": endpoint,
            "floor_3x_over_4": threshold,
            "L": left,
            "R": right,
        })
    return rows


def _synthetic_controls(midpoint: dict[str, Any]) -> dict[str, Any]:
    rho_squared = Fraction(midpoint["rho_squared"])
    h = [Fraction(value) for value in midpoint["h"]]
    unit = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    zero = sum(h, Fraction(0))
    if unit != 1 or zero != 0:
        raise ValueError("synthetic control normalization failed")
    return {
        "label": CONTROL_LABEL,
        "literal_status": "NOT_LITERAL_NUMERICAL_V59_INSTANCES",
        "constant_factor_annihilation": {
            "sum_h": str(zero),
            "constant_w_transfer": "0",
            "constant_g_transfer": "0",
        },
        "sign_controls": [
            {"w": "z", "g": "z", "transfer": str(unit)},
            {"w": "z", "g": "-z", "transfer": str(-unit)},
        ],
        "conclusion": "SOURCE_FREE_GEOMETRY_DOES_NOT_DECIDE_SIGN_NONZERO_OR_SCALE",
    }


def build_document() -> dict[str, Any]:
    kernel, g_vector = _kernel_fixture()
    midpoint = _midpoint_fixture(g_vector)
    crosswalk = _integer_crosswalk()
    controls = _synthetic_controls(midpoint)
    payload = {
        "claim_status": CLAIM_STATUS,
        "maximum_claim": MAXIMUM_CLAIM,
        "evidence_label": "EXACT_RATIONAL_STRUCTURAL_REPRODUCTION_ONLY",
        "source_lock": {
            "baseline_HEAD": BASELINE_HEAD,
            "handoff_sha256": HANDOFF_SHA256,
            "source_frozen_bridge": "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md",
            "source_digests": SOURCE_DIGESTS,
            "inner_product": "conjugate-linear first",
            "literal_scalar": "C_x=<w,A_x beta>",
        },
        "definitions": {
            "physical_interval": "I_x=(x/2,x] intersect Z in increasing order",
            "rank_midpoint": "ell=floor(N/2), r=N-ell, L=first ell coordinates, R=remaining r",
            "contrast": "z=rho(1_L/ell-1_R/r), rho^2=ell*r/N",
            "exact_projector": "(z tensor z)_(i,j)=rho^2*h_i*h_j",
            "partial_sum_moment": "<z,f>=rho(S_f(L)/ell-S_f(R)/r)",
            "adjoint": "(A_x^*z)(t)=sum_u conjugate(A_x(u,t))z(u)",
        },
        "firewall": FIREWALL,
        "midpoint_fixture": midpoint,
        "integer_crosswalk": crosswalk,
        "kernel_fixture": kernel,
        "synthetic_controls": controls,
        "counts": {
            "rank_midpoint_replays": 1,
            "nonintegral_rational_x_replays": 1,
            "integer_crosswalk_rows": len(crosswalk),
            "integer_residue_classes_covered": len({row["x_mod_4"] for row in crosswalk}),
            "literal_kernel_formula_replays": 1,
            "safe_adjoint_replays": 1,
            "constant_annihilation_controls": 2,
            "sign_controls": 2,
        },
    }
    return {"schema": SCHEMA, "payload": payload, "digest": _digest(payload)}


class StrictJSONError(ValueError):
    pass


def _strict_loads(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise StrictJSONError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value: str) -> Any:
        raise StrictJSONError(f"nonfinite JSON token: {value}")

    try:
        return json.loads(text, object_pairs_hook=hook, parse_constant=reject_constant)
    except json.JSONDecodeError as error:
        raise StrictJSONError(f"invalid JSON: {error}") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare with canonical released JSON")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc253_certificate.json",
    )
    args = parser.parse_args()
    document = build_document()
    expected_text = _document_text(document)
    if args.check:
        try:
            raw_text = args.output.read_text(encoding="ascii")
            existing = _strict_loads(raw_text)
        except (OSError, UnicodeError, StrictJSONError) as error:
            print(f"FAIL unreadable or non-strict certificate: {error}")
            return 1
        if existing != document:
            print("FAIL released certificate differs from exact regenerated document")
            return 1
        if raw_text != expected_text:
            print("FAIL released certificate is not canonical strict JSON")
            return 1
        print(
            f"PASS {SCHEMA} digest={document['digest']} midpoint=1 crosswalk=8 "
            "kernel=1 adjoint=1 controls=4 canonical_bytes=1"
        )
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected_text, encoding="ascii")
    print(
        f"WROTE {args.output} digest={document['digest']} midpoint=1 crosswalk=8 "
        "kernel=1 adjoint=1 controls=4 canonical_bytes=1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
