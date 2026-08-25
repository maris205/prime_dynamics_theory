#!/usr/bin/env python3
"""Independent semantic validator and mutation suite for TPC-252."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any


SCHEMA = "TPC252_PARTITION_REFINEMENT_CERTIFICATE_V1"
CLAIM_STATUS = "PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY"
MAXIMUM_CLAIM = (
    "UNIVERSAL_SINGLETON_COLLAPSE_AND_MARGIN_OPTIMALITY_WITH_EXACT_BINARY_"
    "REFINEMENT_RANK_ONE_COVARIANCE_UPDATE_TRANSVERSE_RADIUS_MONOTONICITY_"
    "AND_EXISTENTIAL_SAME_SOURCE_SYNTHETIC_PARTITION_NONINVARIANCE"
)
BASELINE_HEAD = "7cc2b62a615aa2bde49fbfa8eec5fb01117a98d1"
HANDOFF_SHA256 = "a71cab0ab1930b864ae319f73e90f2c750bd8d4ebdc4321ee7923e01ff606147"
NONINVARIANCE_LABEL = (
    "SYNTHETIC_EXACT_FINITE_SOURCE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_"
    "ARITHMETIC_INSTANCE"
)
FIXED_GRAM_SCOPE = (
    "FIXED_PROBE_FAMILY_ONLY_NATIVE_COMMON_INPUT_OUTPUT_REPARTITION_CHANGES_"
    "PROBE_INDEXING"
)
FRACTION_PATTERN = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")

FIREWALL = {
    "TPC252_SINGLETON_THEOREM": "EVERY_FINITE_LITERAL_TPC247_SOURCE_SCALAR",
    "TPC252_BINARY_BLOCK_AVERAGING_UPDATE": "EXACT_FOR_FIXED_W_G",
    "TPC252_FIXED_PROBE_GRAM_UPDATE": "FIXED_PROBE_FAMILY_ONLY",
    "TPC252_NATIVE_REPARTITIONED_PROBE_GRAM_UPDATE": "NOT_CLAIMED_INDEXING_CHANGES",
    "TPC252_SAME_SOURCE_WITNESS": NONINVARIANCE_LABEL,
    "TPC252_EVERY_SOURCE_INSTABILITY": "REFUTED",
    "TPC252_R_COH_REFINEMENT_MONOTONICITY": "NOT_CLAIMED",
    "TPC252_ACTUAL_V59_COARSE_NONZERO_CONTRAST": "NOT_PROVED",
    "TPC252_CANONICAL_PARTITION": "NONE",
    "TPC252_ASYMPTOTIC_ADVANCE": "NO",
    "TPC252_ARITHMETIC_ADVANCE": "NO",
    "TPC252_L2": "NONE",
    "TPC252_GATE_B": "OPEN",
    "TPC252_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC252_FIXED_ATOM_CREDIT": "0",
    "TPC252_ROUTE_A": "NONE",
    "TPC252_TWIN_PRIME_RESULT": "NONE",
}

SOURCE_DIGESTS = {
    "tpc247_tree": "c984cbb9c51fabea54e02618e96efa587b5c1d266a8ac0768c365ad4fc497bf9",
    "tpc250_tree": "7c54ebe446e54ee3f1a01594cb732e07ffa13da625a8c0283c86b3a5d10c35bf",
    "tpc251_tree": "1bb25514ff7f5bac16d5e4ee54466731edff481d116f443faf43ebe95cbbb2f2",
    "bridge_tpc247": "54bb956ad55245970a7d5d8852f1472d6a9dae68e940d1f9ced0b4c243271eed",
    "bridge_tpc250": "05a9b2e66d152e5325fa0f823f8e6f9c3365dcd515f579dfd199ebe0e7b03d7b",
    "bridge_tpc251": "283505a75f3038b4c4e8f3c296988afabd06fa28de0671adba55d18fbdcb445b",
}

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


def _digest(payload: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(payload)).hexdigest()


def _fraction(value: Any, location: str) -> Fraction:
    if not isinstance(value, str) or FRACTION_PATTERN.fullmatch(value) is None:
        raise CertificateError(f"{location}: expected canonical rational string")
    parsed = Fraction(value)
    if str(parsed) != value:
        raise CertificateError(f"{location}: noncanonical rational string")
    return parsed


def _gaussian(value: Any, location: str) -> Gaussian:
    if not isinstance(value, list) or len(value) != 2:
        raise CertificateError(f"{location}: expected Gaussian-rational pair")
    return (_fraction(value[0], location + ".real"), _fraction(value[1], location + ".imag"))


def _vector(value: Any, length: int, location: str) -> Vector:
    if not isinstance(value, list) or len(value) != length:
        raise CertificateError(f"{location}: vector shape mismatch")
    return [_gaussian(entry, f"{location}[{index}]") for index, entry in enumerate(value)]


def _matrix(value: Any, size: int, location: str) -> Matrix:
    if not isinstance(value, list) or len(value) != size:
        raise CertificateError(f"{location}: matrix row count mismatch")
    return [_vector(row, size, f"{location}[{index}]") for index, row in enumerate(value)]


def _add_scalar(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _sub_scalar(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] - right[0], left[1] - right[1])


def _mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _vadd(*vectors: Vector) -> Vector:
    if not vectors:
        return []
    result: Vector = []
    for entries in zip(*vectors):
        total = ZERO
        for entry in entries:
            total = _add_scalar(total, entry)
        result.append(total)
    return result


def _vsub(left: Vector, right: Vector) -> Vector:
    return [_sub_scalar(x, y) for x, y in zip(left, right)]


def _scale(scalar: Gaussian, vector: Vector) -> Vector:
    return [_mul(scalar, entry) for entry in vector]


def _inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for x, y in zip(left, right):
        total = _add_scalar(total, _mul(_conj(x), y))
    return total


def _norm2(vector: Vector) -> Fraction:
    value = _inner(vector, vector)
    if value[1] != 0 or value[0] < 0:
        raise CertificateError("invalid exact squared norm")
    return value[0]


def _sqrt_fraction(value: Fraction, location: str) -> Fraction:
    if value < 0:
        raise CertificateError(f"{location}: negative rational square root")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise CertificateError(f"{location}: non-rational square root")
    return Fraction(numerator, denominator)


def _matvec(matrix: Matrix, vector: Vector) -> Vector:
    result: Vector = []
    for row in matrix:
        total = ZERO
        for coefficient, entry in zip(row, vector):
            total = _add_scalar(total, _mul(coefficient, entry))
        result.append(total)
    return result


def _restrict(vector: Vector, block: list[int]) -> Vector:
    return [vector[index] for index in block]


def _check_partition(value: Any, dimension: int, location: str) -> list[list[int]]:
    if not isinstance(value, list) or not value:
        raise CertificateError(f"{location}: partition must be nonempty")
    blocks: list[list[int]] = []
    seen: list[int] = []
    for block_index, raw_block in enumerate(value):
        if not isinstance(raw_block, list) or not raw_block:
            raise CertificateError(f"{location}[{block_index}]: block must be nonempty")
        if any(type(index) is not int for index in raw_block):
            raise CertificateError(f"{location}[{block_index}]: indices must be exact integers")
        block = list(raw_block)
        blocks.append(block)
        seen.extend(block)
    if sorted(seen) != list(range(dimension)) or len(set(seen)) != dimension:
        raise CertificateError(f"{location}: blocks must be disjoint and exhaustive")
    return blocks


def _average_projection(vector: Vector, blocks: list[list[int]]) -> Vector:
    result = [ZERO for _ in vector]
    for block in blocks:
        total = ZERO
        for index in block:
            total = _add_scalar(total, vector[index])
        mean = (total[0] / len(block), total[1] / len(block))
        for index in block:
            result[index] = mean
    return result


def _residual(vector: Vector, blocks: list[list[int]]) -> Vector:
    return _vsub(vector, _average_projection(vector, blocks))


def _rank_one(z: list[Fraction], vector: Vector) -> Vector:
    z_vector = [(entry, Fraction(0)) for entry in z]
    return _scale(_inner(z_vector, vector), z_vector)


def _r_trans(w: Vector, g_vector: Vector, blocks: list[list[int]]) -> Fraction:
    total = Fraction(0)
    for block_index, block in enumerate(blocks):
        local = [list(range(len(block)))]
        w_perp = _residual(_restrict(w, block), local)
        g_perp = _residual(_restrict(g_vector, block), local)
        total += _sqrt_fraction(
            _norm2(w_perp) * _norm2(g_perp), f"R_trans block {block_index}"
        )
    return total


def _gram(vectors: list[Vector]) -> list[list[Gaussian]]:
    return [[_inner(left, right) for right in vectors] for left in vectors]


def _transverse_gram(vectors: list[Vector], blocks: list[list[int]]) -> list[list[Gaussian]]:
    return _gram([_residual(vector, blocks) for vector in vectors])


def _expect_gaussian(raw: Any, expected: Gaussian, location: str) -> None:
    if _gaussian(raw, location) != expected:
        raise CertificateError(f"{location}: Gaussian value mismatch")


def _expect_vector(raw: Any, expected: Vector, location: str) -> None:
    if _vector(raw, len(expected), location) != expected:
        raise CertificateError(f"{location}: vector mismatch")


def _expect_gram(raw: Any, expected: list[list[Gaussian]], location: str) -> None:
    if not isinstance(raw, list) or len(raw) != len(expected):
        raise CertificateError(f"{location}: Gram row count mismatch")
    for i, row in enumerate(raw):
        if not isinstance(row, list) or len(row) != len(expected[i]):
            raise CertificateError(f"{location}[{i}]: Gram column count mismatch")
        for j, entry in enumerate(row):
            _expect_gaussian(entry, expected[i][j], f"{location}[{i}][{j}]")


def _check_binary(record: Any) -> None:
    required = {
        "label", "dimension", "coarse_blocks", "refined_blocks", "split_sizes", "z",
        "A", "beta", "w", "g", "derived", "fixed_probe_gram",
    }
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("binary refinement shape mismatch")
    if record.get("label") != "EXACT_GAUSSIAN_RATIONAL_BINARY_REFINEMENT_REPLAY":
        raise CertificateError("binary refinement label mismatch")
    dimension = record.get("dimension")
    if type(dimension) is not int or dimension != 4:
        raise CertificateError("binary refinement dimension mismatch")
    coarse = _check_partition(record.get("coarse_blocks"), dimension, "binary.coarse")
    refined = _check_partition(record.get("refined_blocks"), dimension, "binary.refined")
    if coarse != [[0, 1, 2, 3]] or refined != [[0, 1], [2, 3]]:
        raise CertificateError("binary release partition changed")
    split_sizes = record.get("split_sizes")
    if not isinstance(split_sizes, list) or any(type(value) is not int for value in split_sizes):
        raise CertificateError("binary split sizes must be exact integers")
    if split_sizes != [2, 2, 4]:
        raise CertificateError("binary split size ledger mismatch")
    raw_z = record.get("z")
    if not isinstance(raw_z, list) or len(raw_z) != dimension:
        raise CertificateError("binary z shape mismatch")
    z = [_fraction(entry, f"binary.z[{index}]") for index, entry in enumerate(raw_z)]
    if z != [Fraction(1, 2), Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2)]:
        raise CertificateError("binary normalized contrast mismatch")
    matrix = _matrix(record.get("A"), dimension, "binary.A")
    beta = _vector(record.get("beta"), dimension, "binary.beta")
    w = _vector(record.get("w"), dimension, "binary.w")
    g_vector = _vector(record.get("g"), dimension, "binary.g")
    if _matvec(matrix, beta) != g_vector:
        raise CertificateError("binary source replay A beta=g failed")

    mw = _average_projection(w, coarse)
    mg = _average_projection(g_vector, coarse)
    mpw = _average_projection(w, refined)
    mpg = _average_projection(g_vector, refined)
    zw = _rank_one(z, w)
    zg = _rank_one(z, g_vector)
    if _vadd(mw, zw) != mpw or _vadd(mg, zg) != mpg:
        raise CertificateError("binary projector rank-one update failed")
    z_vector = [(entry, Fraction(0)) for entry in z]
    moment_w = _inner(z_vector, w)
    moment_g = _inner(z_vector, g_vector)
    delta = _mul(_conj(moment_w), moment_g)
    if delta == _mul(moment_w, moment_g):
        raise CertificateError("binary fixture does not detect missing conjugation")
    c_coarse = _inner(mw, mg)
    c_refined = _inner(mpw, mpg)
    q_coarse = _inner(_residual(w, coarse), _residual(g_vector, coarse))
    q_refined = _inner(_residual(w, refined), _residual(g_vector, refined))
    scalar = _inner(w, g_vector)
    r_coarse = _r_trans(w, g_vector, coarse)
    r_refined = _r_trans(w, g_vector, refined)
    if c_refined != _add_scalar(c_coarse, delta):
        raise CertificateError("binary C_long covariance update failed")
    if q_refined != _sub_scalar(q_coarse, delta):
        raise CertificateError("binary Q_trans covariance update failed")
    if scalar != _add_scalar(c_coarse, q_coarse) or scalar != _add_scalar(c_refined, q_refined):
        raise CertificateError("binary orthogonal scalar decomposition failed")
    if r_refined > r_coarse:
        raise CertificateError("binary R_trans monotonicity failed")
    if (moment_w, moment_g, delta, c_coarse, c_refined, q_coarse, q_refined, scalar) != (
        (Fraction(1), Fraction(1)),
        (Fraction(2), Fraction(2)),
        (Fraction(4), Fraction(0)),
        (Fraction(6), Fraction(0)),
        (Fraction(10), Fraction(0)),
        (Fraction(6), Fraction(0)),
        (Fraction(2), Fraction(0)),
        (Fraction(12), Fraction(0)),
    ) or (r_coarse, r_refined) != (Fraction(6), Fraction(2)):
        raise CertificateError("binary recommended exact values changed")

    derived = record.get("derived")
    expected_keys = {
        "M_coarse_w", "M_refined_w", "M_coarse_g", "M_refined_g",
        "z_tensor_z_w", "z_tensor_z_g", "z_norm_squared", "z_old_block_sum",
        "moment_w", "moment_g", "covariance_increment", "C_long_coarse",
        "C_long_refined", "Q_trans_coarse", "Q_trans_refined", "C_x",
        "R_trans_coarse", "R_trans_refined",
    }
    if not isinstance(derived, dict) or set(derived) != expected_keys:
        raise CertificateError("binary derived shape mismatch")
    for key, expected in (
        ("M_coarse_w", mw), ("M_refined_w", mpw), ("M_coarse_g", mg),
        ("M_refined_g", mpg), ("z_tensor_z_w", zw), ("z_tensor_z_g", zg),
    ):
        _expect_vector(derived.get(key), expected, "binary.derived." + key)
    for key, expected in (
        ("moment_w", moment_w), ("moment_g", moment_g), ("covariance_increment", delta),
        ("C_long_coarse", c_coarse), ("C_long_refined", c_refined),
        ("Q_trans_coarse", q_coarse), ("Q_trans_refined", q_refined), ("C_x", scalar),
    ):
        _expect_gaussian(derived.get(key), expected, "binary.derived." + key)
    if _fraction(derived.get("z_norm_squared"), "binary.z_norm_squared") != _norm2(z_vector):
        raise CertificateError("binary z norm mismatch")
    if _fraction(derived.get("z_old_block_sum"), "binary.z_old_block_sum") != sum(z, Fraction(0)):
        raise CertificateError("binary z mean mismatch")
    if _fraction(derived.get("R_trans_coarse"), "binary.R_coarse") != r_coarse:
        raise CertificateError("binary coarse R_trans mismatch")
    if _fraction(derived.get("R_trans_refined"), "binary.R_refined") != r_refined:
        raise CertificateError("binary refined R_trans mismatch")

    gram_record = record.get("fixed_probe_gram")
    required_gram = {
        "scope", "probes", "z_moments", "coarse_transverse_gram", "refined_transverse_gram"
    }
    if not isinstance(gram_record, dict) or set(gram_record) != required_gram:
        raise CertificateError("fixed probe Gram shape mismatch")
    if gram_record.get("scope") != FIXED_GRAM_SCOPE:
        raise CertificateError("fixed probe Gram scope mismatch")
    raw_probes = gram_record.get("probes")
    if not isinstance(raw_probes, list) or len(raw_probes) != 3:
        raise CertificateError("fixed probe family size mismatch")
    probes = [_vector(probe, dimension, f"fixed.probes[{index}]") for index, probe in enumerate(raw_probes)]
    moments = [_inner(z_vector, probe) for probe in probes]
    raw_moments = gram_record.get("z_moments")
    if not isinstance(raw_moments, list) or len(raw_moments) != len(moments):
        raise CertificateError("fixed probe moment shape mismatch")
    for index, moment in enumerate(moments):
        _expect_gaussian(raw_moments[index], moment, f"fixed.moments[{index}]")
    gram_coarse = _transverse_gram(probes, coarse)
    gram_refined = _transverse_gram(probes, refined)
    _expect_gram(gram_record.get("coarse_transverse_gram"), gram_coarse, "fixed.gram_coarse")
    _expect_gram(gram_record.get("refined_transverse_gram"), gram_refined, "fixed.gram_refined")
    for i in range(len(probes)):
        for j in range(len(probes)):
            expected = _sub_scalar(gram_coarse[i][j], _mul(_conj(moments[i]), moments[j]))
            if gram_refined[i][j] != expected:
                raise CertificateError("fixed-family projected Gram rank-one subtraction failed")


def _native_projected_groups(matrix: Matrix, beta: Vector, w: Vector, blocks: list[list[int]]) -> tuple[list[dict[str, Any]], Fraction]:
    dimension = len(beta)
    groups: list[dict[str, Any]] = []
    total_radius = Fraction(0)
    for c, output_block in enumerate(blocks):
        local = [list(range(len(output_block)))]
        w_perp = _residual(_restrict(w, output_block), local)
        projected: list[Vector] = []
        for input_block in blocks:
            beta_b = [beta[index] if index in input_block else ZERO for index in range(dimension)]
            probe = _restrict(_matvec(matrix, beta_b), output_block)
            projected.append(_residual(probe, local))
        gram_perp = _gram(projected)
        norms_squared = [_norm2(probe) for probe in projected]
        active = [index for index, value in enumerate(norms_squared) if value != 0]
        if len(active) > 1:
            raise CertificateError("special native audit unexpectedly has multiple active probes")
        diagonal = sum(norms_squared, Fraction(0))
        upper_squared = diagonal
        contribution = _sqrt_fraction(_norm2(w_perp) * upper_squared, "native radius")
        total_radius += contribution
        groups.append({
            "c": c,
            "projected": projected,
            "gram": gram_perp,
            "active_count": len(active),
            "D": diagonal,
            "L_squared": diagonal,
            "mu": Fraction(0),
            "U_squared": upper_squared,
            "w_perp_squared": _norm2(w_perp),
            "radius_contribution": contribution,
        })
    return groups, total_radius


def _check_group_records(raw: Any, expected: list[dict[str, Any]], location: str) -> None:
    if not isinstance(raw, list) or len(raw) != len(expected):
        raise CertificateError(f"{location}: group count mismatch")
    keys = {
        "c", "projected_probes", "gram_perp", "active_count", "D", "L_squared",
        "mu", "U_squared", "w_perp_squared", "radius_contribution",
    }
    for index, (record, calculated) in enumerate(zip(raw, expected)):
        if not isinstance(record, dict) or set(record) != keys:
            raise CertificateError(f"{location}[{index}]: group shape mismatch")
        if type(record.get("c")) is not int or record.get("c") != calculated["c"]:
            raise CertificateError(f"{location}[{index}]: c type/value mismatch")
        if type(record.get("active_count")) is not int or record.get("active_count") != calculated["active_count"]:
            raise CertificateError(f"{location}[{index}]: active count mismatch")
        raw_probes = record.get("projected_probes")
        probes = calculated["projected"]
        if not isinstance(raw_probes, list) or len(raw_probes) != len(probes):
            raise CertificateError(f"{location}[{index}]: projected probe count mismatch")
        for probe_index, probe in enumerate(probes):
            _expect_vector(raw_probes[probe_index], probe, f"{location}[{index}].probe[{probe_index}]")
        _expect_gram(record.get("gram_perp"), calculated["gram"], f"{location}[{index}].gram")
        for key in ("D", "L_squared", "mu", "U_squared", "w_perp_squared", "radius_contribution"):
            if _fraction(record.get(key), f"{location}[{index}].{key}") != calculated[key]:
                raise CertificateError(f"{location}[{index}]: {key} mismatch")


def _partition_values(w: Vector, g_vector: Vector, blocks: list[list[int]]) -> tuple[Gaussian, Gaussian, Fraction]:
    c_long = _inner(_average_projection(w, blocks), _average_projection(g_vector, blocks))
    q_trans = _inner(_residual(w, blocks), _residual(g_vector, blocks))
    return c_long, q_trans, _r_trans(w, g_vector, blocks)


def _check_metric_record(raw: Any, expected: tuple[Gaussian, Gaussian, Fraction], r_coh: Fraction, location: str) -> None:
    if not isinstance(raw, dict) or set(raw) != {"C_long", "Q_trans", "R_trans", "R_coh"}:
        raise CertificateError(f"{location}: metric shape mismatch")
    _expect_gaussian(raw.get("C_long"), expected[0], location + ".C_long")
    _expect_gaussian(raw.get("Q_trans"), expected[1], location + ".Q_trans")
    if _fraction(raw.get("R_trans"), location + ".R_trans") != expected[2]:
        raise CertificateError(f"{location}: R_trans mismatch")
    if _fraction(raw.get("R_coh"), location + ".R_coh") != r_coh:
        raise CertificateError(f"{location}: R_coh mismatch")


def _check_noninvariance(record: Any) -> None:
    required = {
        "label", "quantifier", "dimension", "A", "beta", "w", "g", "C_x",
        "coarse", "singleton", "margin_rows",
    }
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("noninvariance fixture shape mismatch")
    if record.get("label") != NONINVARIANCE_LABEL:
        raise CertificateError("noninvariance literal/synthetic evidence label mismatch")
    if record.get("quantifier") != "THERE_EXISTS_ONE_FIXED_A_BETA_W_WITH_PARTITION_DEPENDENCE":
        raise CertificateError("noninvariance quantifier mismatch")
    dimension = record.get("dimension")
    if type(dimension) is not int or dimension != 2:
        raise CertificateError("noninvariance dimension mismatch")
    matrix = _matrix(record.get("A"), dimension, "noninvariance.A")
    beta = _vector(record.get("beta"), dimension, "noninvariance.beta")
    w = _vector(record.get("w"), dimension, "noninvariance.w")
    g_vector = _vector(record.get("g"), dimension, "noninvariance.g")
    if matrix != [[ZERO, (Fraction(1), Fraction(0))], [(Fraction(1), Fraction(0)), ZERO]]:
        raise CertificateError("noninvariance primary-bridge swap operator changed")
    if beta != [(Fraction(-1), Fraction(0)), (Fraction(1), Fraction(0))]:
        raise CertificateError("noninvariance primary-bridge beta signs changed")
    if w != [(Fraction(1), Fraction(0)), (Fraction(-1), Fraction(0))]:
        raise CertificateError("noninvariance primary-bridge w signs changed")
    if _matvec(matrix, beta) != g_vector:
        raise CertificateError("noninvariance fixed-source replay failed")
    if g_vector != w:
        raise CertificateError("noninvariance primary-bridge g signs changed")
    scalar = _inner(w, g_vector)
    _expect_gaussian(record.get("C_x"), scalar, "noninvariance.C_x")
    if scalar != (Fraction(2), Fraction(0)):
        raise CertificateError("noninvariance scalar changed")

    parts: list[tuple[str, list[list[int]], tuple[Gaussian, Gaussian, Fraction], Fraction]] = []
    for name, expected_blocks in (("coarse", [[0, 1]]), ("singleton", [[0], [1]])):
        raw_part = record.get(name)
        if not isinstance(raw_part, dict) or set(raw_part) != {"blocks", "metrics", "groups"}:
            raise CertificateError(f"noninvariance.{name}: partition record shape mismatch")
        blocks = _check_partition(raw_part.get("blocks"), dimension, f"noninvariance.{name}.blocks")
        if blocks != expected_blocks:
            raise CertificateError(f"noninvariance.{name}: legal partition changed")
        groups, r_coh = _native_projected_groups(matrix, beta, w, blocks)
        values = _partition_values(w, g_vector, blocks)
        _check_metric_record(raw_part.get("metrics"), values, r_coh, f"noninvariance.{name}.metrics")
        _check_group_records(raw_part.get("groups"), groups, f"noninvariance.{name}.groups")
        parts.append((name, blocks, values, r_coh))
    if parts[0][2] == parts[1][2]:
        raise CertificateError("same-source witness is partition invariant")
    if parts[0][2] != ((Fraction(0), Fraction(0)), (Fraction(2), Fraction(0)), Fraction(2)):
        raise CertificateError("coarse noninvariance values changed")
    if parts[1][2] != ((Fraction(2), Fraction(0)), (Fraction(0), Fraction(0)), Fraction(0)):
        raise CertificateError("singleton noninvariance values changed")
    if (parts[0][3], parts[1][3]) != (Fraction(2), Fraction(0)):
        raise CertificateError("noninvariance coherence radii changed")

    rows = record.get("margin_rows")
    expected_errors = [Fraction(0), Fraction(1, 2), Fraction(2), Fraction(3)]
    if not isinstance(rows, list) or len(rows) != len(expected_errors):
        raise CertificateError("margin row count mismatch")
    for row, external_error in zip(rows, expected_errors):
        keys = {"E", "coarse_margin", "singleton_margin", "maximum", "direct_external_bound"}
        if not isinstance(row, dict) or set(row) != keys:
            raise CertificateError("margin row shape mismatch")
        if _fraction(row.get("E"), "margin.E") != external_error:
            raise CertificateError("margin E mismatch")
        direct = max(abs(scalar[0]) - external_error, Fraction(0))
        coarse_margin = max(abs(parts[0][2][0][0]) - parts[0][3] - external_error, Fraction(0))
        singleton_margin = max(abs(parts[1][2][0][0]) - parts[1][3] - external_error, Fraction(0))
        expected = {
            "coarse_margin": coarse_margin,
            "singleton_margin": singleton_margin,
            "maximum": max(coarse_margin, singleton_margin),
            "direct_external_bound": direct,
        }
        if expected["maximum"] != direct:
            raise CertificateError("two-coordinate exhaustive margin optimum failed")
        for key, value in expected.items():
            if _fraction(row.get(key), "margin." + key) != value:
                raise CertificateError(f"margin {key} mismatch")


def _check_stability(record: Any) -> None:
    required = {
        "label", "A", "beta", "w", "g", "coarse_metrics", "fine_metrics",
        "contrast_covariance_increment",
    }
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("stable-source fixture shape mismatch")
    if record.get("label") != "SAME_SOURCE_STABILITY_COUNTEREXAMPLE_TO_EVERY_SOURCE_INSTABILITY":
        raise CertificateError("stable-source label mismatch")
    matrix = _matrix(record.get("A"), 2, "stability.A")
    beta = _vector(record.get("beta"), 2, "stability.beta")
    w = _vector(record.get("w"), 2, "stability.w")
    g_vector = _vector(record.get("g"), 2, "stability.g")
    if _matvec(matrix, beta) != g_vector:
        raise CertificateError("stable-source A beta replay failed")
    coarse = _partition_values(w, g_vector, [[0, 1]])
    fine = _partition_values(w, g_vector, [[0], [1]])
    if coarse != fine or coarse != ((Fraction(4), Fraction(0)), (Fraction(0), Fraction(0)), Fraction(0)):
        raise CertificateError("stable-source counterexample semantics failed")
    for key, raw in (("coarse_metrics", record.get("coarse_metrics")), ("fine_metrics", record.get("fine_metrics"))):
        if not isinstance(raw, dict) or set(raw) != {"C_long", "Q_trans", "R_trans"}:
            raise CertificateError(f"stability.{key}: metric shape mismatch")
        _expect_gaussian(raw.get("C_long"), coarse[0], f"stability.{key}.C_long")
        _expect_gaussian(raw.get("Q_trans"), coarse[1], f"stability.{key}.Q_trans")
        if _fraction(raw.get("R_trans"), f"stability.{key}.R_trans") != coarse[2]:
            raise CertificateError("stable-source R_trans mismatch")
    _expect_gaussian(record.get("contrast_covariance_increment"), ZERO, "stability.increment")


def _check_singleton(record: Any) -> None:
    required = {
        "label", "dimension", "blocks", "A", "beta", "w", "g", "C_x",
        "metrics", "groups", "kappa",
    }
    if not isinstance(record, dict) or set(record) != required:
        raise CertificateError("singleton fixture shape mismatch")
    if record.get("label") != "SINGLETON_COLLAPSE_EXACT_FINITE_SOURCE_REPLAY":
        raise CertificateError("singleton fixture label mismatch")
    dimension = record.get("dimension")
    if type(dimension) is not int or dimension != 3:
        raise CertificateError("singleton dimension mismatch")
    blocks = _check_partition(record.get("blocks"), dimension, "singleton.blocks")
    if blocks != [[0], [1], [2]]:
        raise CertificateError("singleton partition mismatch")
    matrix = _matrix(record.get("A"), dimension, "singleton.A")
    beta = _vector(record.get("beta"), dimension, "singleton.beta")
    w = _vector(record.get("w"), dimension, "singleton.w")
    g_vector = _vector(record.get("g"), dimension, "singleton.g")
    if _matvec(matrix, beta) != g_vector:
        raise CertificateError("singleton A beta replay failed")
    scalar = _inner(w, g_vector)
    _expect_gaussian(record.get("C_x"), scalar, "singleton.C_x")
    groups, r_coh = _native_projected_groups(matrix, beta, w, blocks)
    values = _partition_values(w, g_vector, blocks)
    _check_metric_record(record.get("metrics"), values, r_coh, "singleton.metrics")
    _check_group_records(record.get("groups"), groups, "singleton.groups")
    if values != (scalar, ZERO, Fraction(0)) or r_coh != 0:
        raise CertificateError("singleton scalar/radius collapse failed")
    for group in groups:
        if any(group[key] != 0 for key in ("D", "L_squared", "mu", "U_squared", "radius_contribution")):
            raise CertificateError("singleton projected probes or coherence data did not vanish")
        if any(any(entry != ZERO for entry in probe) for probe in group["projected"]):
            raise CertificateError("singleton projected probe is nonzero")
        if any(any(entry != ZERO for entry in row) for row in group["gram"]):
            raise CertificateError("singleton projected Gram is nonzero")
    if record.get("kappa") != "UNDEFINED_WHEN_D_EQUALS_ZERO":
        raise CertificateError("singleton kappa used at D=0")


def check_document(document: Any) -> None:
    if not isinstance(document, dict) or set(document) != {"schema", "payload", "digest"}:
        raise CertificateError("top-level shape mismatch")
    if document.get("schema") != SCHEMA:
        raise CertificateError("schema mismatch")
    payload = document.get("payload")
    digest = document.get("digest")
    if not isinstance(payload, dict) or not isinstance(digest, str) or _digest(payload) != digest:
        raise CertificateError("payload digest mismatch")
    required = {
        "claim_status", "maximum_claim", "evidence_label", "source_lock", "definitions",
        "firewall", "binary_refinement", "two_coordinate_noninvariance",
        "stable_source_counterexample", "singleton_collapse", "universal_margin_identity", "counts",
    }
    if set(payload) != required:
        raise CertificateError("payload shape mismatch")
    if payload.get("claim_status") != CLAIM_STATUS or payload.get("maximum_claim") != MAXIMUM_CLAIM:
        raise CertificateError("claim status/ceiling mismatch")
    if payload.get("evidence_label") != "EXACT_RATIONAL_STRUCTURAL_REPRODUCTION_ONLY":
        raise CertificateError("evidence label mismatch")
    source = payload.get("source_lock")
    expected_source = {
        "baseline_HEAD": BASELINE_HEAD,
        "handoff_sha256": HANDOFF_SHA256,
        "source_digests": SOURCE_DIGESTS,
        "literal_source_scope": "I_x=(x/2,x] finite physical coordinates; C_x=<w,A_x beta>",
        "inner_product": "conjugate-linear first",
        "lambda_cb": "1",
    }
    if source != expected_source:
        raise CertificateError("source lock mismatch")
    expected_definitions = {
        "block_projection": "M_P is orthogonal block averaging",
        "rank_one_action": "(z tensor z)h=z<z,h>",
        "binary_update": "M_P'=M_P+z tensor z",
        "covariance_update": "C_long(P')=C_long(P)+conjugate(<z,w>)<z,g>",
        "transverse_update": "Q_trans(P')=Q_trans(P)-conjugate(<z,w>)<z,g>",
        "mu_empty_pair_rule": "mu=0 when fewer than two projected probes are active",
        "kappa_zero_rule": "kappa is undefined at D=0",
        "external_E": "independently certified and fixed while optimizing partitions",
    }
    if payload.get("definitions") != expected_definitions:
        raise CertificateError("definition ledger mismatch")
    if payload.get("firewall") != FIREWALL:
        raise CertificateError("claim firewall mismatch")
    expected_counts = {
        "binary_refinement_replays": 1,
        "fixed_probe_families": 1,
        "same_source_noninvariance_witnesses": 1,
        "same_source_stability_counterexamples": 1,
        "singleton_replays": 1,
        "two_coordinate_legal_partitions_exhausted": 2,
        "margin_E_values_checked": 4,
    }
    counts = payload.get("counts")
    if not isinstance(counts, dict) or set(counts) != set(expected_counts):
        raise CertificateError("certificate count shape mismatch")
    for key, expected in expected_counts.items():
        value = counts.get(key)
        if type(value) is not int or value != expected:
            raise CertificateError(f"certificate count mismatch: {key}")
    if payload.get("universal_margin_identity") != {
        "statement": "max_P [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+ for every fixed E>=0",
        "upper_reason": "|C_long(P)|-R_coh(P)<=|C_x|",
        "attainment": "the singleton partition has C_long=C_x and R_coh=0",
        "adaptive_partition_gain_over_direct_bound": "0",
    }:
        raise CertificateError("universal margin identity ledger mismatch")
    _check_binary(payload.get("binary_refinement"))
    _check_noninvariance(payload.get("two_coordinate_noninvariance"))
    _check_stability(payload.get("stable_source_counterexample"))
    _check_singleton(payload.get("singleton_collapse"))


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

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["dimension"] = True
    cases.append(("typed_bool_dimension", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["counts"]["binary_refinement_replays"] = True
    cases.append(("typed_bool_count", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["z"][0] = "2/4"
    cases.append(("noncanonical_rational", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["refined_blocks"][1][-1] = 2
    cases.append(("duplicate_nonexhaustive_partition", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["A"][0][0] = ["2", "0"]
    cases.append(("source_operator_semantics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["g"][0] = ["0", "0"]
    cases.append(("source_image_semantics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["derived"]["covariance_increment"] = ["0", "4"]
    cases.append(("missing_covariance_conjugation", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["derived"]["C_long_refined"] = ["9", "0"]
    cases.append(("longitudinal_update", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["derived"]["Q_trans_refined"] = ["3", "0"]
    cases.append(("transverse_update", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["derived"]["R_trans_refined"] = "7"
    cases.append(("transverse_radius_monotonicity", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["fixed_probe_gram"]["scope"] = "NATIVE_REPARTITIONED_PROBES"
    cases.append(("fixed_probe_scope", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["binary_refinement"]["fixed_probe_gram"]["refined_transverse_gram"][0][1] = ["99", "0"]
    cases.append(("fixed_probe_gram_semantics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["two_coordinate_noninvariance"]["label"] = "LITERAL_V59_INSTANCE"
    cases.append(("synthetic_literal_confusion", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["two_coordinate_noninvariance"]["quantifier"] = "FOR_EVERY_SOURCE"
    cases.append(("universal_instability_quantifier", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["two_coordinate_noninvariance"]["coarse"]["metrics"]["C_long"] = ["1", "0"]
    cases.append(("same_source_partition_metrics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["two_coordinate_noninvariance"]["margin_rows"][1]["maximum"] = "2"
    cases.append(("margin_maximum_semantics", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["stable_source_counterexample"]["contrast_covariance_increment"] = ["1", "0"]
    cases.append(("stable_source_counterexample", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["singleton_collapse"]["groups"][0]["projected_probes"][0][0] = ["1", "0"]
    cases.append(("singleton_projected_probe", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["singleton_collapse"]["kappa"] = "0"
    cases.append(("kappa_at_D_zero", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["firewall"]["TPC252_EVERY_SOURCE_INSTABILITY"] = "PROVED"
    cases.append(("every_source_instability_promotion", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["firewall"]["TPC252_R_COH_REFINEMENT_MONOTONICITY"] = "PROVED"
    cases.append(("R_coh_monotonicity_promotion", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["firewall"]["TPC252_ARITHMETIC_ADVANCE"] = "YES"
    cases.append(("arithmetic_promotion", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["source_lock"]["handoff_sha256"] = "0" * 64
    cases.append(("source_hash_rebound", mutated, True))

    mutated = copy.deepcopy(document)
    mutated["payload"]["counts"]["margin_E_values_checked"] = 5
    cases.append(("count_semantics", mutated, True))

    stale = copy.deepcopy(document)
    stale["payload"]["singleton_collapse"]["metrics"]["C_long"] = ["19", "0"]
    cases.append(("stale_digest", stale, False))

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
    parser.add_argument("--check", action="store_true", help="validate the release and run mutations")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc252_certificate.json",
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
        "binary=1 fixed_gram=1 noninvariance=1 stability=1 singleton=1 margin_E=4 canonical_bytes=1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
