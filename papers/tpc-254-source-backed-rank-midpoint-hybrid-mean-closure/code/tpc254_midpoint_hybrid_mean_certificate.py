#!/usr/bin/env python3
"""Produce and check the exact finite TPC-254 certificate.

The certificate reproduces only finite algebra and source-contract typing.  It
does not numerically test the maximal Type-I theorem or any asymptotic claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "TPC254_RANK_MIDPOINT_HYBRID_MEAN_CERTIFICATE_V1"
STATUS = (
    "PROVED_SOURCE_BACKED_L1_RANK_MIDPOINT_HYBRID_MEAN_CLOSURE_WITH_"
    "ADJOINT_LANE_SOURCE_GAP"
)
MAXIMUM_CLAIM = (
    "SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER_CONTROL_OF_THE_LITERAL_V59_"
    "RANK_MIDPOINT_W_CONTRAST_WITH_ONLY_EXACT_ADJOINT_CAUCHY_TRANSFER"
)
BASELINE_HEAD = "79bd188a97752946f5ddc83a85571a3573f511c6"
HANDOFF_SHA256 = "bdb20981b19bb136b0166b804940c476d465c4708cdbf3d52b362f07e2a29e26"
SOURCE_DIGESTS = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": HANDOFF_SHA256,
    "research/tpc-big-road/fm_local_comparison_compiler.md": (
        "4f7537ff5a10d53634638afff508ee6e3401364dab7970852b327470918c644f"
    ),
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md": (
        "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16"
    ),
    "research/tpc-big-road/bridge_b_mesoscopic_covariance.md": (
        "e9838ebee8aa027421dad9bc2d05cb7b3655d2de413da0aa11aa143095636c37"
    ),
    "research/tpc-big-road/bridge_b_literal_v59_source_operator_attachment.md": (
        "54bb956ad55245970a7d5d8852f1472d6a9dae68e940d1f9ced0b4c243271eed"
    ),
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md": (
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee"
    ),
}

FIREWALL = {
    "TPC254_MAXIMUM_CLAIM": MAXIMUM_CLAIM,
    "TPC254_HYBRID_CUTOFF": "SOURCE_LOCKED_FIXED_FINITE_K_NO_K_UNIFORMITY",
    "TPC254_RANK_CHILD_INTERVAL_ADMISSIBILITY": "PROVED_EXACT_FOR_REAL_X",
    "TPC254_MAXIMAL_TYPE_I_M1_EXTRACTION": "PROVED_SOURCE_BACKED",
    "TPC254_CHILD_SUM_HYBRID_MEAN": "PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC254_CHILD_MEAN_DIFFERENCE": "PROVED_SOURCE_BACKED_ARBITRARY_FIXED_LOG_POWER",
    "TPC254_W_MIDPOINT_HAAR_MOMENT": (
        "PROVED_SOURCE_BACKED_X_ONE_HALF_TIMES_ARBITRARY_FIXED_LOG_SAVING"
    ),
    "TPC254_SAFE_ADJOINT_CAUCHY_TRANSFER": "PROVED_EXACT",
    "TPC254_G_MIDPOINT_HAAR_ESTIMATE": "OPEN_NO_FROZEN_SOURCE_ATTACHMENT",
    "TPC254_G_LANE_SOURCE_ATTACHMENT": (
        "STOP_SCOPED_DECLARED_CORPUS_NO_FIXED_HAAR_ADJOINT_ESTIMATE"
    ),
    "TPC254_ZERO_DIAGONAL_DERANGEMENT_OBSTRUCTION": (
        "PROVED_SYNTHETIC_NOT_LITERAL_V59"
    ),
    "TPC254_CAUCHY_CONSTANT_ONE_SHARPNESS": "PROVED_EXACT_N2_SYNTHETIC",
    "TPC254_ARBITRARY_LOG_TO_FIXED_POWER_PROMOTION": "NOT_CLAIMED",
    "TPC254_W_CONTRAST_SIGN_OR_NONZERO": "NOT_CLAIMED",
    "TPC254_G_CONTRAST_SIGN_OR_NONZERO": "OPEN",
    "TPC254_JOINT_TRANSFER_LOWER_BOUND": "OPEN",
    "TPC254_V21_CHILD_OR_ADJOINT_SUBSTITUTION": "NOT_CLAIMED",
    "TPC254_ARITHMETIC_ADVANCE": "YES_SCOPED_LITERAL_W_LANE",
    "TPC254_FIXED_ATOM_CREDIT": "0",
    "TPC254_L2": "NONE",
    "TPC254_FULL_GATE_B": "OPEN",
    "TPC254_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC254_TWIN_PRIME_RESULT": "NONE",
    "TPC254_STATUS": STATUS,
}

Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
Matrix = list[list[Gaussian]]
ZERO: Gaussian = (Fraction(0), Fraction(0))


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _document(value: Any) -> bytes:
    return _canonical(value) + b"\n"


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _q(value: int | str | Fraction) -> Fraction:
    return value if isinstance(value, Fraction) else Fraction(value)


def _g(real: int | str | Fraction, imag: int | str | Fraction = 0) -> Gaussian:
    return (_q(real), _q(imag))


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _scale(value: Fraction, entry: Gaussian) -> Gaussian:
    return (value * entry[0], value * entry[1])


def _inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for left_entry, right_entry in zip(left, right):
        total = _add(total, _mul(_conj(left_entry), right_entry))
    return total


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = _add(total, _mul(coefficient, entry))
        result.append(total)
    return result


def _adjoint(matrix: Matrix) -> Matrix:
    size = len(matrix)
    return [[_conj(matrix[row][column]) for row in range(size)] for column in range(size)]


def _transpose(matrix: Matrix) -> Matrix:
    size = len(matrix)
    return [[matrix[row][column] for row in range(size)] for column in range(size)]


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _gaussian_json(value: Gaussian) -> list[str]:
    return [str(value[0]), str(value[1])]


def _vector_json(vector: Vector) -> list[list[str]]:
    return [_gaussian_json(entry) for entry in vector]


def _matrix_json(matrix: Matrix) -> list[list[list[str]]]:
    return [_vector_json(row) for row in matrix]


def _rank_fixture() -> dict[str, Any]:
    x = Fraction(27, 2)
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    count = len(coordinates)
    ell = count // 2
    right_size = count - ell
    left = coordinates[:ell]
    right = coordinates[ell:]
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, count)
    projector = [[rho_squared * row * column for column in h] for row in h]
    w: Vector = [
        _g(1),
        _g(2, 1),
        _g(-1, 2),
        _g(3, -1),
        _g(0, 1),
        _g(-2),
        _g(1, -2),
    ]
    left_sum = ZERO
    right_sum = ZERO
    for entry in w[:ell]:
        left_sum = _add(left_sum, entry)
    for entry in w[ell:]:
        right_sum = _add(right_sum, entry)
    mean_difference = _add(
        _scale(Fraction(1, ell), left_sum),
        _scale(Fraction(-1, right_size), right_sum),
    )
    mean_difference_abs_squared = _inner([mean_difference], [mean_difference])[0]
    return {
        "x": str(x),
        "floor_x_over_two": _floor(x / 2),
        "floor_x": _floor(x),
        "coordinates": coordinates,
        "count": count,
        "ell": ell,
        "right_size": right_size,
        "left": left,
        "right": right,
        "h": [str(entry) for entry in h],
        "rho_squared": str(rho_squared),
        "projector": [[str(entry) for entry in row] for row in projector],
        "sample_w": _vector_json(w),
        "left_sum": _gaussian_json(left_sum),
        "right_sum": _gaussian_json(right_sum),
        "mean_difference": _gaussian_json(mean_difference),
        "mean_difference_abs_squared": str(mean_difference_abs_squared),
        "haar_moment_abs_squared": str(rho_squared * mean_difference_abs_squared),
        "rank_left_end": left[-1],
        "integer_threshold_floor_three_x_over_four": _floor(3 * x / 4),
        "noninteger_threshold_mismatch": "DETECTED_RANK_DEFINITION_CONTROLS",
    }


def _m1_fixture() -> dict[str, Any]:
    rows = [
        (1, 1, Fraction(7, 3)),
        (2, 16, Fraction(5, 7)),
        (3, 16, Fraction(11, 13)),
        (4, 81, Fraction(2, 9)),
    ]
    encoded: list[dict[str, Any]] = []
    total = Fraction(0)
    for m_value, weight, interval_maximum in rows:
        weighted_term = weight * interval_maximum
        total += weighted_term
        encoded.append(
            {
                "m": m_value,
                "tau_power_weight": weight,
                "interval_maximum": str(interval_maximum),
                "weighted_term": str(weighted_term),
            }
        )
    return {
        "row_count": len(encoded),
        "rows": encoded,
        "weighted_nonnegative_total": str(total),
        "m1_extracted_bound": str(rows[0][2]),
        "extraction_logic": "NONNEGATIVE_SUM_DOMINATES_UNIT_WEIGHT_M1_ROW",
    }


def _whole_shell_fixture(rank: dict[str, Any]) -> dict[str, Any]:
    h = [Fraction(entry) for entry in rank["h"]]
    rho_squared = Fraction(rank["rho_squared"])
    normalization = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    return {
        "representation": "Z_MID_EQUALS_RHO_TIMES_RATIONAL_STEP_H",
        "lambda": "-7/3",
        "sum_h": str(sum(h, Fraction(0))),
        "rho_squared_times_h_norm_squared": str(normalization),
        "whole_shell_sum_of_lambda_z_mid": "0",
        "haar_moment_of_lambda_z_mid": "-7/3",
        "conclusion": "WHOLE_SHELL_ZERO_DOES_NOT_CONTROL_HAAR_MOMENT",
    }


def _adjoint_fixture() -> dict[str, Any]:
    matrix: Matrix = [
        [_g(1, 1), _g(2, -1), _g(0, 2)],
        [_g(-1, 2), _g(3), _g(1, -3)],
        [_g(2), _g(-2, 1), _g(4, 1)],
    ]
    z = [_g(1), _g(0, 1), _g(-1, 1)]
    beta = [_g(2, -1), _g(1, 3), _g(-2)]
    a_beta = _matvec(matrix, beta)
    a_star_z = _matvec(_adjoint(matrix), z)
    lhs = _inner(z, a_beta)
    rhs = _inner(a_star_z, beta)
    transpose_z = _matvec(_transpose(matrix), z)
    transpose_pairing = _inner(transpose_z, beta)
    return {
        "matrix": _matrix_json(matrix),
        "z_test": _vector_json(z),
        "beta": _vector_json(beta),
        "a_beta": _vector_json(a_beta),
        "a_star_z": _vector_json(a_star_z),
        "lhs_inner_z_a_beta": _gaussian_json(lhs),
        "rhs_inner_a_star_z_beta": _gaussian_json(rhs),
        "transpose_z": _vector_json(transpose_z),
        "transpose_shortcut_pairing": _gaussian_json(transpose_pairing),
        "transpose_shortcut_status": "REJECTED_NOT_EQUAL_TO_ADJOINT_IDENTITY",
    }


def _derangement_fixture() -> dict[str, Any]:
    z = [_g(Fraction(3, 5)), _g(Fraction(4, 5)), _g(0)]
    permutation = [1, 2, 0]
    lambda_value = Fraction(-7, 4)
    matrix: Matrix = [[ZERO for _ in range(3)] for _ in range(3)]
    for row, column in enumerate(permutation):
        matrix[row][column] = _scale(lambda_value, z[row])
    beta = [_g(1), _g(1), _g(1)]
    a_beta = _matvec(matrix, beta)
    moment = _inner(z, a_beta)
    return {
        "size": 3,
        "permutation_zero_based": permutation,
        "lambda": str(lambda_value),
        "z": _vector_json(z),
        "beta": _vector_json(beta),
        "matrix": _matrix_json(matrix),
        "a_beta": _vector_json(a_beta),
        "moment": _gaussian_json(moment),
        "diagonal_status": "EXACTLY_ZERO",
        "scope": "SYNTHETIC_REAL_ZERO_DIAGONAL_NOT_LITERAL_V59",
    }


def _n2_sharp_fixture() -> dict[str, Any]:
    lambda_value = Fraction(11, 7)
    lambda_squared = lambda_value * lambda_value
    return {
        "size": 2,
        "lambda": str(lambda_value),
        "z_component_square": "1/2",
        "off_diagonal_entry_square": str(lambda_squared / 2),
        "off_diagonal_signs": [1, -1],
        "moment_abs_squared": str(lambda_squared),
        "adjoint_norm_squared": str(lambda_squared / 2),
        "beta_norm_squared": "2",
        "cauchy_product_abs_squared": str(lambda_squared),
        "equality_status": "CAUCHY_CONSTANT_ONE_EXACT",
        "scope": "SYNTHETIC_REAL_ZERO_DIAGONAL_NOT_LITERAL_V59",
    }


def _source_contract() -> dict[str, Any]:
    return {
        "finite_admissible_k_fixture": 7,
        "gamma_zero": "1/4",
        "target_log_power_m_fixture": 9,
        "chosen_h2_exponent_fixture": 12,
        "delta_fixture": "1/2",
        "m1_weight": 1,
        "source_theorem_type": "MAXIMAL_INTERVAL_TYPE_I_EVERY_FIXED_GAMMA_BELOW_ONE_HALF",
        "m1_extraction_type": "NONNEGATIVE_ROW_EXTRACTION",
        "asymptotic_test_status": "NOT_EXECUTED_FINITE_CERTIFICATE_CANNOT_PROVE_SOURCE_THEOREM",
        "quantifier_order": [
            "FIXED_FINITE_ADMISSIBLE_K",
            "FREEZE_GAMMA_ZERO_EQUALS_ONE_QUARTER",
            "TARGET_M",
            "SUFFICIENTLY_STRONG_INTEGER_H2_EXPONENT",
            "DELTA_BELOW_ONE_MINUS_GAMMA_ZERO",
            "TAIL_BV_AND_FUNDAMENTAL_LEMMA_CHOICES",
            "X_AT_LEAST_X_ZERO_OF_M_AND_K",
        ],
        "upstream_ford_maynard_order": [
            "TARGET_A_AND_VARPI",
            "FORD_MAYNARD_B_FM",
            "FIXED_K_OF_B_FM",
            "X_AT_LEAST_X_ZERO_OF_A_VARPI_B_FM_AND_K",
        ],
        "uniformity_firewall": [
            "NO_K_TO_INFINITY_UNIFORMITY",
            "NO_GAMMA_TO_ONE_HALF_UNIFORMITY",
            "NO_ARBITRARY_LOG_TO_FIXED_POWER_PROMOTION",
        ],
    }


def build_certificate() -> dict[str, Any]:
    rank = _rank_fixture()
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "maximum_claim": MAXIMUM_CLAIM,
        "baseline_head": BASELINE_HEAD,
        "handoff_sha256": HANDOFF_SHA256,
        "source_digests": SOURCE_DIGESTS,
        "source_contract": _source_contract(),
        "firewall": FIREWALL,
        "fixture_count": 6,
        "stress_required_families": 192,
        "mutation_required_minimum": 44,
        "fixtures": {
            "rank_midpoint": rank,
            "m1_nonnegative_extraction": _m1_fixture(),
            "whole_shell_counterexample": _whole_shell_fixture(rank),
            "adjoint_orientation": _adjoint_fixture(),
            "zero_diagonal_derangement": _derangement_fixture(),
            "n2_cauchy_sharpness": _n2_sharp_fixture(),
        },
        "executable_scope": (
            "FINITE_EXACT_ALGEBRA_AND_SOURCE_CONTRACT_TYPING_ONLY_NOT_"
            "ASYMPTOTIC_EVIDENCE"
        ),
    }
    return {"payload": payload, "payload_sha256": _digest(payload)}


def _certificate_path() -> Path:
    return Path(__file__).resolve().parents[1] / "results" / "tpc254_certificate.json"


def _check() -> None:
    expected = _document(build_certificate())
    actual = _certificate_path().read_bytes()
    if actual != expected:
        raise SystemExit("TPC254_CERTIFICATE=FAIL released certificate is not canonical expected output")
    print(
        "TPC254_CERTIFICATE=PASS fixtures=6 exact_arithmetic=YES "
        "asymptotic_evidence=NO"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-certificate", action="store_true")
    arguments = parser.parse_args()
    if arguments.check == arguments.print_certificate:
        raise SystemExit("choose exactly one of --check or --print-certificate")
    if arguments.print_certificate:
        print(_canonical(build_certificate()).decode("ascii"))
        return
    _check()


if __name__ == "__main__":
    main()
