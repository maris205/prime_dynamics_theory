#!/usr/bin/env python3
"""Independent strict validator and adversarial mutation suite for TPC-254."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
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
SOURCE_CONTRACT = {
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
FRACTION_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

Gaussian = tuple[Fraction, Fraction]
Vector = list[Gaussian]
Matrix = list[list[Gaussian]]
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


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CertificateError("duplicate JSON key: " + key)
        result[key] = value
    return result


def _constant(token: str) -> Any:
    raise CertificateError("nonfinite JSON token: " + token)


def _keys(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise CertificateError(location + ": object shape mismatch")
    return value


def _integer(value: Any, location: str) -> int:
    if type(value) is not int:
        raise CertificateError(location + ": expected exact integer, never bool")
    return value


def _integer_list(value: Any, location: str) -> list[int]:
    if not isinstance(value, list):
        raise CertificateError(location + ": expected integer list")
    return [_integer(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _fraction(value: Any, location: str) -> Fraction:
    if not isinstance(value, str) or FRACTION_PATTERN.fullmatch(value) is None:
        raise CertificateError(location + ": expected canonical rational string")
    parsed = Fraction(value)
    if str(parsed) != value:
        raise CertificateError(location + ": noncanonical rational string")
    return parsed


def _gaussian(value: Any, location: str) -> Gaussian:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(location + ": expected Gaussian-rational pair")
    return (_fraction(value[0], location + ".real"), _fraction(value[1], location + ".imag"))


def _vector(value: Any, length: int, location: str) -> Vector:
    if not isinstance(value, list) or len(value) != length:
        raise CertificateError(location + ": vector shape mismatch")
    return [_gaussian(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _matrix(value: Any, size: int, location: str) -> Matrix:
    if not isinstance(value, list) or len(value) != size:
        raise CertificateError(location + ": matrix row mismatch")
    return [_vector(row, size, f"{location}[{index}]") for index, row in enumerate(value)]


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


def _validate_rank(value: Any) -> None:
    expected_keys = {
        "x", "floor_x_over_two", "floor_x", "coordinates", "count", "ell",
        "right_size", "left", "right", "h", "rho_squared", "projector",
        "sample_w", "left_sum", "right_sum", "mean_difference",
        "mean_difference_abs_squared", "haar_moment_abs_squared", "rank_left_end",
        "integer_threshold_floor_three_x_over_four", "noninteger_threshold_mismatch",
    }
    rank = _keys(value, expected_keys, "rank_midpoint")
    x = _fraction(rank["x"], "rank.x")
    floor_half = _floor(x / 2)
    floor_x = _floor(x)
    if _integer(rank["floor_x_over_two"], "rank.floor_x_over_two") != floor_half:
        raise CertificateError("rank: floor x/2 mismatch")
    if _integer(rank["floor_x"], "rank.floor_x") != floor_x:
        raise CertificateError("rank: floor x mismatch")
    coordinates = _integer_list(rank["coordinates"], "rank.coordinates")
    expected_coordinates = list(range(floor_half + 1, floor_x + 1))
    if coordinates != expected_coordinates:
        raise CertificateError("rank: active coordinate interval mismatch")
    count = _integer(rank["count"], "rank.count")
    if count != len(coordinates) or count < 2:
        raise CertificateError("rank: count mismatch")
    ell = _integer(rank["ell"], "rank.ell")
    right_size = _integer(rank["right_size"], "rank.right_size")
    if ell != count // 2 or right_size != count - ell:
        raise CertificateError("rank: child sizes mismatch")
    left = _integer_list(rank["left"], "rank.left")
    right = _integer_list(rank["right"], "rank.right")
    if left != coordinates[:ell] or right != coordinates[ell:]:
        raise CertificateError("rank: child endpoints mismatch")
    h_raw = rank["h"]
    if not isinstance(h_raw, list) or len(h_raw) != count:
        raise CertificateError("rank: h shape mismatch")
    h = [_fraction(entry, f"rank.h[{index}]") for index, entry in enumerate(h_raw)]
    expected_h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    if h != expected_h or sum(h, Fraction(0)) != 0:
        raise CertificateError("rank: rational Haar step mismatch")
    rho_squared = _fraction(rank["rho_squared"], "rank.rho_squared")
    if rho_squared != Fraction(ell * right_size, count):
        raise CertificateError("rank: rho squared mismatch")
    projector_raw = rank["projector"]
    if not isinstance(projector_raw, list) or len(projector_raw) != count:
        raise CertificateError("rank: projector row mismatch")
    projector: list[list[Fraction]] = []
    for row_index, row in enumerate(projector_raw):
        if not isinstance(row, list) or len(row) != count:
            raise CertificateError("rank: projector column mismatch")
        projector.append([
            _fraction(entry, f"rank.projector[{row_index}][{column_index}]")
            for column_index, entry in enumerate(row)
        ])
    expected_projector = [[rho_squared * a * b for b in h] for a in h]
    if projector != expected_projector:
        raise CertificateError("rank: projector product mismatch")
    w = _vector(rank["sample_w"], count, "rank.sample_w")
    left_sum = ZERO
    right_sum = ZERO
    for entry in w[:ell]:
        left_sum = _add(left_sum, entry)
    for entry in w[ell:]:
        right_sum = _add(right_sum, entry)
    if _gaussian(rank["left_sum"], "rank.left_sum") != left_sum:
        raise CertificateError("rank: left sum mismatch")
    if _gaussian(rank["right_sum"], "rank.right_sum") != right_sum:
        raise CertificateError("rank: right sum mismatch")
    mean_difference = _add(
        _scale(Fraction(1, ell), left_sum),
        _scale(Fraction(-1, right_size), right_sum),
    )
    if _gaussian(rank["mean_difference"], "rank.mean_difference") != mean_difference:
        raise CertificateError("rank: child mean difference mismatch")
    mean_abs_squared = _inner([mean_difference], [mean_difference])[0]
    if _fraction(rank["mean_difference_abs_squared"], "rank.mean_abs_squared") != mean_abs_squared:
        raise CertificateError("rank: mean square mismatch")
    if _fraction(rank["haar_moment_abs_squared"], "rank.haar_square") != rho_squared * mean_abs_squared:
        raise CertificateError("rank: Haar moment square mismatch")
    if _integer(rank["rank_left_end"], "rank.rank_left_end") != left[-1]:
        raise CertificateError("rank: left endpoint ledger mismatch")
    wrong_threshold = _floor(3 * x / 4)
    if _integer(
        rank["integer_threshold_floor_three_x_over_four"], "rank.integer_threshold"
    ) != wrong_threshold:
        raise CertificateError("rank: noninteger threshold fixture mismatch")
    if left[-1] == wrong_threshold:
        raise CertificateError("rank: fixture failed to expose noninteger threshold error")
    if rank["noninteger_threshold_mismatch"] != "DETECTED_RANK_DEFINITION_CONTROLS":
        raise CertificateError("rank: threshold firewall mismatch")


def _validate_m1(value: Any) -> None:
    fixture = _keys(
        value,
        {"row_count", "rows", "weighted_nonnegative_total", "m1_extracted_bound", "extraction_logic"},
        "m1",
    )
    rows = fixture["rows"]
    if not isinstance(rows, list):
        raise CertificateError("m1: rows must be list")
    if _integer(fixture["row_count"], "m1.row_count") != len(rows) or not rows:
        raise CertificateError("m1: row count mismatch")
    total = Fraction(0)
    first_maximum: Fraction | None = None
    for index, raw_row in enumerate(rows):
        row = _keys(
            raw_row,
            {"m", "tau_power_weight", "interval_maximum", "weighted_term"},
            f"m1.rows[{index}]",
        )
        m_value = _integer(row["m"], f"m1.rows[{index}].m")
        weight = _integer(row["tau_power_weight"], f"m1.rows[{index}].weight")
        maximum = _fraction(row["interval_maximum"], f"m1.rows[{index}].maximum")
        weighted = _fraction(row["weighted_term"], f"m1.rows[{index}].weighted")
        if m_value < 1 or weight < 0 or maximum < 0 or weighted != weight * maximum:
            raise CertificateError("m1: nonnegative weighted row mismatch")
        if index == 0:
            if m_value != 1 or weight != 1:
                raise CertificateError("m1: first row is not unit-weight m=1")
            first_maximum = maximum
        total += weighted
    if _fraction(fixture["weighted_nonnegative_total"], "m1.total") != total:
        raise CertificateError("m1: total mismatch")
    if first_maximum is None or _fraction(fixture["m1_extracted_bound"], "m1.bound") != first_maximum:
        raise CertificateError("m1: extracted bound mismatch")
    if total < first_maximum:
        raise CertificateError("m1: nonnegative extraction failed")
    if fixture["extraction_logic"] != "NONNEGATIVE_SUM_DOMINATES_UNIT_WEIGHT_M1_ROW":
        raise CertificateError("m1: extraction label mismatch")


def _validate_whole_shell(value: Any, rank: dict[str, Any]) -> None:
    fixture = _keys(
        value,
        {"representation", "lambda", "sum_h", "rho_squared_times_h_norm_squared",
         "whole_shell_sum_of_lambda_z_mid", "haar_moment_of_lambda_z_mid", "conclusion"},
        "whole_shell",
    )
    h = [_fraction(entry, "whole_shell.h") for entry in rank["h"]]
    rho_squared = _fraction(rank["rho_squared"], "whole_shell.rho_squared")
    lambda_value = _fraction(fixture["lambda"], "whole_shell.lambda")
    if fixture["representation"] != "Z_MID_EQUALS_RHO_TIMES_RATIONAL_STEP_H":
        raise CertificateError("whole_shell: representation mismatch")
    if _fraction(fixture["sum_h"], "whole_shell.sum_h") != sum(h, Fraction(0)):
        raise CertificateError("whole_shell: zero sum mismatch")
    normalization = rho_squared * sum((entry * entry for entry in h), Fraction(0))
    if _fraction(fixture["rho_squared_times_h_norm_squared"], "whole_shell.norm") != normalization:
        raise CertificateError("whole_shell: normalization mismatch")
    if normalization != 1 or _fraction(fixture["whole_shell_sum_of_lambda_z_mid"], "whole_shell.sum") != 0:
        raise CertificateError("whole_shell: shell-zero construction mismatch")
    if _fraction(fixture["haar_moment_of_lambda_z_mid"], "whole_shell.moment") != lambda_value:
        raise CertificateError("whole_shell: nonzero Haar moment mismatch")
    if fixture["conclusion"] != "WHOLE_SHELL_ZERO_DOES_NOT_CONTROL_HAAR_MOMENT":
        raise CertificateError("whole_shell: conclusion mismatch")


def _validate_adjoint(value: Any) -> None:
    fixture = _keys(
        value,
        {"matrix", "z_test", "beta", "a_beta", "a_star_z", "lhs_inner_z_a_beta",
         "rhs_inner_a_star_z_beta", "transpose_z", "transpose_shortcut_pairing",
         "transpose_shortcut_status"},
        "adjoint",
    )
    matrix = _matrix(fixture["matrix"], 3, "adjoint.matrix")
    z = _vector(fixture["z_test"], 3, "adjoint.z")
    beta = _vector(fixture["beta"], 3, "adjoint.beta")
    a_beta = _matvec(matrix, beta)
    a_star_z = _matvec(_adjoint(matrix), z)
    if _vector(fixture["a_beta"], 3, "adjoint.a_beta") != a_beta:
        raise CertificateError("adjoint: A beta mismatch")
    if _vector(fixture["a_star_z"], 3, "adjoint.a_star_z") != a_star_z:
        raise CertificateError("adjoint: A star z mismatch")
    lhs = _inner(z, a_beta)
    rhs = _inner(a_star_z, beta)
    if _gaussian(fixture["lhs_inner_z_a_beta"], "adjoint.lhs") != lhs:
        raise CertificateError("adjoint: lhs mismatch")
    if _gaussian(fixture["rhs_inner_a_star_z_beta"], "adjoint.rhs") != rhs or lhs != rhs:
        raise CertificateError("adjoint: orientation identity mismatch")
    transpose_z = _matvec(_transpose(matrix), z)
    transpose_pairing = _inner(transpose_z, beta)
    if _vector(fixture["transpose_z"], 3, "adjoint.transpose_z") != transpose_z:
        raise CertificateError("adjoint: transpose fixture mismatch")
    if _gaussian(fixture["transpose_shortcut_pairing"], "adjoint.transpose_pairing") != transpose_pairing:
        raise CertificateError("adjoint: transpose pairing mismatch")
    if transpose_pairing == lhs or fixture["transpose_shortcut_status"] != "REJECTED_NOT_EQUAL_TO_ADJOINT_IDENTITY":
        raise CertificateError("adjoint: transpose shortcut was not rejected")


def _validate_derangement(value: Any) -> None:
    fixture = _keys(
        value,
        {"size", "permutation_zero_based", "lambda", "z", "beta", "matrix", "a_beta",
         "moment", "diagonal_status", "scope"},
        "derangement",
    )
    size = _integer(fixture["size"], "derangement.size")
    if size < 2:
        raise CertificateError("derangement: size too small")
    permutation = _integer_list(fixture["permutation_zero_based"], "derangement.permutation")
    if sorted(permutation) != list(range(size)) or any(index == image for index, image in enumerate(permutation)):
        raise CertificateError("derangement: permutation is not a derangement")
    lambda_value = _fraction(fixture["lambda"], "derangement.lambda")
    z = _vector(fixture["z"], size, "derangement.z")
    beta = _vector(fixture["beta"], size, "derangement.beta")
    if _inner(z, z) != (Fraction(1), Fraction(0)):
        raise CertificateError("derangement: z is not a unit vector")
    if beta != [(Fraction(1), Fraction(0))] * size:
        raise CertificateError("derangement: beta is not all ones")
    matrix = _matrix(fixture["matrix"], size, "derangement.matrix")
    expected: Matrix = [[ZERO for _ in range(size)] for _ in range(size)]
    for row, column in enumerate(permutation):
        expected[row][column] = _scale(lambda_value, z[row])
    if matrix != expected or any(matrix[index][index] != ZERO for index in range(size)):
        raise CertificateError("derangement: zero-diagonal matrix mismatch")
    a_beta = _matvec(matrix, beta)
    if _vector(fixture["a_beta"], size, "derangement.a_beta") != a_beta:
        raise CertificateError("derangement: A beta mismatch")
    expected_a_beta = [_scale(lambda_value, entry) for entry in z]
    if a_beta != expected_a_beta:
        raise CertificateError("derangement: arbitrary signed scale failed")
    if _gaussian(fixture["moment"], "derangement.moment") != _inner(z, a_beta):
        raise CertificateError("derangement: moment mismatch")
    if fixture["diagonal_status"] != "EXACTLY_ZERO" or fixture["scope"] != "SYNTHETIC_REAL_ZERO_DIAGONAL_NOT_LITERAL_V59":
        raise CertificateError("derangement: scope firewall mismatch")


def _validate_n2(value: Any) -> None:
    fixture = _keys(
        value,
        {"size", "lambda", "z_component_square", "off_diagonal_entry_square",
         "off_diagonal_signs", "moment_abs_squared", "adjoint_norm_squared",
         "beta_norm_squared", "cauchy_product_abs_squared", "equality_status", "scope"},
        "n2",
    )
    if _integer(fixture["size"], "n2.size") != 2:
        raise CertificateError("n2: size mismatch")
    lambda_value = _fraction(fixture["lambda"], "n2.lambda")
    lambda_squared = lambda_value * lambda_value
    if _fraction(fixture["z_component_square"], "n2.z_square") != Fraction(1, 2):
        raise CertificateError("n2: z component square mismatch")
    if _fraction(fixture["off_diagonal_entry_square"], "n2.offdiag") != lambda_squared / 2:
        raise CertificateError("n2: matrix square mismatch")
    if _integer_list(fixture["off_diagonal_signs"], "n2.signs") != [1, -1]:
        raise CertificateError("n2: signs mismatch")
    moment_squared = _fraction(fixture["moment_abs_squared"], "n2.moment")
    adjoint_squared = _fraction(fixture["adjoint_norm_squared"], "n2.adjoint")
    beta_squared = _fraction(fixture["beta_norm_squared"], "n2.beta")
    product_squared = _fraction(fixture["cauchy_product_abs_squared"], "n2.product")
    if moment_squared != lambda_squared or adjoint_squared != lambda_squared / 2:
        raise CertificateError("n2: squared norm ledger mismatch")
    if beta_squared != 2 or product_squared != adjoint_squared * beta_squared:
        raise CertificateError("n2: Cauchy product mismatch")
    if product_squared != moment_squared:
        raise CertificateError("n2: constant-one equality failed")
    if fixture["equality_status"] != "CAUCHY_CONSTANT_ONE_EXACT" or fixture["scope"] != "SYNTHETIC_REAL_ZERO_DIAGONAL_NOT_LITERAL_V59":
        raise CertificateError("n2: scope firewall mismatch")


def validate_document(raw: bytes, verify_sources: bool) -> dict[str, Any]:
    try:
        document = json.loads(raw.decode("ascii"), object_pairs_hook=_pairs, parse_constant=_constant)
    except UnicodeDecodeError as error:
        raise CertificateError("certificate must be ASCII") from error
    except json.JSONDecodeError as error:
        raise CertificateError("invalid strict JSON") from error
    if raw != _canonical(document) + b"\n":
        raise CertificateError("certificate bytes are not canonical one-line JSON")
    outer = _keys(document, {"payload", "payload_sha256"}, "document")
    payload = _keys(
        outer["payload"],
        {"schema", "status", "maximum_claim", "baseline_head", "handoff_sha256",
         "source_digests", "source_contract", "firewall", "fixture_count",
         "stress_required_families", "mutation_required_minimum", "fixtures",
         "executable_scope"},
        "payload",
    )
    if outer["payload_sha256"] != _digest(payload):
        raise CertificateError("payload digest mismatch")
    if payload["schema"] != SCHEMA or payload["status"] != STATUS:
        raise CertificateError("schema or status mismatch")
    if payload["maximum_claim"] != MAXIMUM_CLAIM:
        raise CertificateError("maximum claim mismatch")
    if payload["baseline_head"] != BASELINE_HEAD or payload["handoff_sha256"] != HANDOFF_SHA256:
        raise CertificateError("baseline provenance mismatch")
    if payload["source_digests"] != SOURCE_DIGESTS:
        raise CertificateError("source digest contract mismatch")
    if payload["source_contract"] != SOURCE_CONTRACT:
        raise CertificateError("source theorem quantifier contract mismatch")
    for integer_key in (
        "finite_admissible_k_fixture", "target_log_power_m_fixture",
        "chosen_h2_exponent_fixture", "m1_weight",
    ):
        _integer(payload["source_contract"][integer_key], "source_contract." + integer_key)
    if not Fraction(payload["source_contract"]["delta_fixture"]) < 1 - Fraction(payload["source_contract"]["gamma_zero"]):
        raise CertificateError("source contract delta is not below one minus gamma")
    if payload["firewall"] != FIREWALL:
        raise CertificateError("claim firewall mismatch")
    if _integer(payload["fixture_count"], "payload.fixture_count") != 6:
        raise CertificateError("fixture count mismatch")
    if _integer(payload["stress_required_families"], "payload.stress_required_families") != 192:
        raise CertificateError("stress family contract mismatch")
    if _integer(payload["mutation_required_minimum"], "payload.mutation_required_minimum") < 44:
        raise CertificateError("mutation minimum is below 44")
    if payload["executable_scope"] != "FINITE_EXACT_ALGEBRA_AND_SOURCE_CONTRACT_TYPING_ONLY_NOT_ASYMPTOTIC_EVIDENCE":
        raise CertificateError("executable scope mismatch")
    fixtures = _keys(
        payload["fixtures"],
        {"rank_midpoint", "m1_nonnegative_extraction", "whole_shell_counterexample",
         "adjoint_orientation", "zero_diagonal_derangement", "n2_cauchy_sharpness"},
        "fixtures",
    )
    _validate_rank(fixtures["rank_midpoint"])
    _validate_m1(fixtures["m1_nonnegative_extraction"])
    _validate_whole_shell(fixtures["whole_shell_counterexample"], fixtures["rank_midpoint"])
    _validate_adjoint(fixtures["adjoint_orientation"])
    _validate_derangement(fixtures["zero_diagonal_derangement"])
    _validate_n2(fixtures["n2_cauchy_sharpness"])
    if verify_sources:
        repository = Path(__file__).resolve().parents[3]
        for relative_path, expected_digest in SOURCE_DIGESTS.items():
            if relative_path == "TPC_HANDOFF.md":
                snapshot = subprocess.run(
                    ["git", "show", BASELINE_HEAD + ":" + relative_path],
                    cwd=repository,
                    capture_output=True,
                    check=False,
                )
                if snapshot.returncode != 0 or snapshot.stderr != b"":
                    raise CertificateError("cannot read baseline handoff Git blob")
                source_bytes = snapshot.stdout
            else:
                source_bytes = (repository / relative_path).read_bytes()
            actual_digest = hashlib.sha256(source_bytes).hexdigest()
            if actual_digest != expected_digest:
                raise CertificateError("source hash mismatch: " + relative_path)
    return document


def _set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    cursor: Any = document
    for component in path[:-1]:
        cursor = cursor[component]
    cursor[path[-1]] = value


def _seal(document: dict[str, Any]) -> None:
    document["payload_sha256"] = _digest(document["payload"])


def _expect_rejected(raw: bytes, label: str) -> None:
    try:
        validate_document(raw, verify_sources=False)
    except (CertificateError, ValueError, TypeError, KeyError, IndexError):
        return
    raise CertificateError("mutation escaped independent checker: " + label)


def _mutation_suite(document: dict[str, Any]) -> int:
    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("payload", "schema"), "TPC254_BAD"),
        ("status", ("payload", "status"), "OPEN"),
        ("maximum_claim", ("payload", "maximum_claim"), "TOO_STRONG"),
        ("baseline", ("payload", "baseline_head"), "0" * 40),
        ("handoff", ("payload", "handoff_sha256"), "0" * 64),
        ("source_hash", ("payload", "source_digests", "AGENTS.md"), "0" * 64),
        ("firewall", ("payload", "firewall", "TPC254_FULL_GATE_B"), "CLOSED"),
        ("fixture_count_bool", ("payload", "fixture_count"), True),
        ("fixture_count", ("payload", "fixture_count"), 7),
        ("stress_count_bool", ("payload", "stress_required_families"), False),
        ("stress_count", ("payload", "stress_required_families"), 191),
        ("mutation_floor", ("payload", "mutation_required_minimum"), 43),
        ("source_k_bool", ("payload", "source_contract", "finite_admissible_k_fixture"), True),
        ("source_gamma", ("payload", "source_contract", "gamma_zero"), "1/2"),
        ("source_m", ("payload", "source_contract", "target_log_power_m_fixture"), 10),
        ("source_b", ("payload", "source_contract", "chosen_h2_exponent_fixture"), 8),
        ("source_delta", ("payload", "source_contract", "delta_fixture"), "3/4"),
        ("source_m1_weight_bool", ("payload", "source_contract", "m1_weight"), True),
        ("quantifier_order", ("payload", "source_contract", "quantifier_order", 0), "TARGET_M"),
        ("uniformity", ("payload", "source_contract", "uniformity_firewall", 0), "UNIFORM_K"),
        ("rank_x", ("payload", "fixtures", "rank_midpoint", "x"), "13"),
        ("rank_x_noncanonical", ("payload", "fixtures", "rank_midpoint", "x"), "54/4"),
        ("floor_half_bool", ("payload", "fixtures", "rank_midpoint", "floor_x_over_two"), True),
        ("floor_x", ("payload", "fixtures", "rank_midpoint", "floor_x"), 14),
        ("coordinate_bool", ("payload", "fixtures", "rank_midpoint", "coordinates", 0), True),
        ("coordinate", ("payload", "fixtures", "rank_midpoint", "coordinates", 2), 10),
        ("count_bool", ("payload", "fixtures", "rank_midpoint", "count"), True),
        ("count", ("payload", "fixtures", "rank_midpoint", "count"), 8),
        ("ell", ("payload", "fixtures", "rank_midpoint", "ell"), 4),
        ("right_size", ("payload", "fixtures", "rank_midpoint", "right_size"), 3),
        ("left", ("payload", "fixtures", "rank_midpoint", "left", 2), 10),
        ("right", ("payload", "fixtures", "rank_midpoint", "right", 0), 9),
        ("h", ("payload", "fixtures", "rank_midpoint", "h", 0), "1/4"),
        ("rho", ("payload", "fixtures", "rank_midpoint", "rho_squared"), "7/12"),
        ("projector", ("payload", "fixtures", "rank_midpoint", "projector", 0, 0), "1"),
        ("sample_w", ("payload", "fixtures", "rank_midpoint", "sample_w", 0, 0), "2"),
        ("left_sum", ("payload", "fixtures", "rank_midpoint", "left_sum", 0), "3"),
        ("right_sum", ("payload", "fixtures", "rank_midpoint", "right_sum", 1), "0"),
        ("mean_difference", ("payload", "fixtures", "rank_midpoint", "mean_difference", 0), "1/5"),
        ("mean_square", ("payload", "fixtures", "rank_midpoint", "mean_difference_abs_squared"), "1"),
        ("haar_square", ("payload", "fixtures", "rank_midpoint", "haar_moment_abs_squared"), "1"),
        ("left_end_bool", ("payload", "fixtures", "rank_midpoint", "rank_left_end"), True),
        ("left_end", ("payload", "fixtures", "rank_midpoint", "rank_left_end"), 10),
        ("threshold", ("payload", "fixtures", "rank_midpoint", "integer_threshold_floor_three_x_over_four"), 9),
        ("threshold_label", ("payload", "fixtures", "rank_midpoint", "noninteger_threshold_mismatch"), "MISSED"),
        ("m1_row_count_bool", ("payload", "fixtures", "m1_nonnegative_extraction", "row_count"), True),
        ("m1_m_bool", ("payload", "fixtures", "m1_nonnegative_extraction", "rows", 0, "m"), True),
        ("m1_m", ("payload", "fixtures", "m1_nonnegative_extraction", "rows", 0, "m"), 2),
        ("m1_weight", ("payload", "fixtures", "m1_nonnegative_extraction", "rows", 0, "tau_power_weight"), 2),
        ("m1_negative", ("payload", "fixtures", "m1_nonnegative_extraction", "rows", 1, "interval_maximum"), "-1"),
        ("m1_term", ("payload", "fixtures", "m1_nonnegative_extraction", "rows", 2, "weighted_term"), "1"),
        ("m1_total", ("payload", "fixtures", "m1_nonnegative_extraction", "weighted_nonnegative_total"), "1"),
        ("m1_bound", ("payload", "fixtures", "m1_nonnegative_extraction", "m1_extracted_bound"), "1"),
        ("whole_lambda", ("payload", "fixtures", "whole_shell_counterexample", "lambda"), "0"),
        ("whole_sum", ("payload", "fixtures", "whole_shell_counterexample", "sum_h"), "1"),
        ("whole_norm", ("payload", "fixtures", "whole_shell_counterexample", "rho_squared_times_h_norm_squared"), "2"),
        ("whole_moment", ("payload", "fixtures", "whole_shell_counterexample", "haar_moment_of_lambda_z_mid"), "0"),
        ("adjoint_matrix", ("payload", "fixtures", "adjoint_orientation", "matrix", 0, 0, 0), "2"),
        ("adjoint_z", ("payload", "fixtures", "adjoint_orientation", "z_test", 0, 0), "2"),
        ("adjoint_beta", ("payload", "fixtures", "adjoint_orientation", "beta", 0, 1), "0"),
        ("adjoint_abeta", ("payload", "fixtures", "adjoint_orientation", "a_beta", 0, 0), "0"),
        ("adjoint_astarz", ("payload", "fixtures", "adjoint_orientation", "a_star_z", 0, 0), "0"),
        ("adjoint_lhs", ("payload", "fixtures", "adjoint_orientation", "lhs_inner_z_a_beta", 0), "0"),
        ("adjoint_rhs", ("payload", "fixtures", "adjoint_orientation", "rhs_inner_a_star_z_beta", 0), "0"),
        ("derangement_size_bool", ("payload", "fixtures", "zero_diagonal_derangement", "size"), True),
        ("derangement_fixed_point", ("payload", "fixtures", "zero_diagonal_derangement", "permutation_zero_based", 0), 0),
        ("derangement_lambda", ("payload", "fixtures", "zero_diagonal_derangement", "lambda"), "1"),
        ("derangement_diagonal", ("payload", "fixtures", "zero_diagonal_derangement", "matrix", 0, 0, 0), "1"),
        ("derangement_moment", ("payload", "fixtures", "zero_diagonal_derangement", "moment", 0), "0"),
        ("n2_size_bool", ("payload", "fixtures", "n2_cauchy_sharpness", "size"), True),
        ("n2_lambda", ("payload", "fixtures", "n2_cauchy_sharpness", "lambda"), "2"),
        ("n2_offdiag", ("payload", "fixtures", "n2_cauchy_sharpness", "off_diagonal_entry_square"), "1"),
        ("n2_sign_bool", ("payload", "fixtures", "n2_cauchy_sharpness", "off_diagonal_signs", 0), True),
        ("n2_moment", ("payload", "fixtures", "n2_cauchy_sharpness", "moment_abs_squared"), "1"),
        ("n2_adjoint", ("payload", "fixtures", "n2_cauchy_sharpness", "adjoint_norm_squared"), "1"),
        ("n2_beta", ("payload", "fixtures", "n2_cauchy_sharpness", "beta_norm_squared"), "1"),
        ("n2_product", ("payload", "fixtures", "n2_cauchy_sharpness", "cauchy_product_abs_squared"), "1"),
    ]
    rejected = 0
    for label, path, value in mutations:
        mutated = copy.deepcopy(document)
        _set_path(mutated, path, value)
        _seal(mutated)
        _expect_rejected(_canonical(mutated) + b"\n", label)
        rejected += 1
    digest_mutation = copy.deepcopy(document)
    digest_mutation["payload_sha256"] = "0" * 64
    _expect_rejected(_canonical(digest_mutation) + b"\n", "digest")
    rejected += 1
    canonical = _canonical(document)
    duplicate = canonical.replace(b'{"payload":', b'{"payload":null,"payload":', 1) + b"\n"
    _expect_rejected(duplicate, "duplicate-key")
    rejected += 1
    nonfinite = canonical.replace(b'"fixture_count":6', b'"fixture_count":NaN', 1) + b"\n"
    _expect_rejected(nonfinite, "nonfinite-token")
    rejected += 1
    _expect_rejected(canonical + b" \n", "noncanonical-whitespace")
    rejected += 1
    _expect_rejected(canonical + b"\n\n", "two-newlines")
    rejected += 1
    return rejected


def _certificate_path() -> Path:
    return Path(__file__).resolve().parents[1] / "results" / "tpc254_certificate.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    raw = _certificate_path().read_bytes()
    document = validate_document(raw, verify_sources=True)
    rejected = _mutation_suite(document)
    if rejected < 44:
        raise SystemExit("TPC254_INDEPENDENT_CHECK=FAIL insufficient mutations")
    print(
        "TPC254_INDEPENDENT_CHECK=PASS mutations_rejected=" + str(rejected)
        + " source_hashes=" + str(len(SOURCE_DIGESTS))
    )


if __name__ == "__main__":
    main()
