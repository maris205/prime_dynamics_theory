#!/usr/bin/env python3
"""Produce the exact TPC-252 partition-refinement certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
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
ONE: Gaussian = (Fraction(1), Fraction(0))


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


def _scale(scalar: Gaussian, vector: Vector) -> Vector:
    return [_mul(scalar, entry) for entry in vector]


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


def _inner(left: Vector, right: Vector) -> Gaussian:
    total = ZERO
    for x, y in zip(left, right):
        total = _add_scalar(total, _mul(_conj(x), y))
    return total


def _norm2(vector: Vector) -> Fraction:
    value = _inner(vector, vector)
    if value[1] != 0 or value[0] < 0:
        raise ValueError("invalid exact squared norm")
    return value[0]


def _sqrt_fraction(value: Fraction) -> Fraction:
    if value < 0:
        raise ValueError("negative rational square root")
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator or denominator * denominator != value.denominator:
        raise ValueError(f"non-rational square root requested: {value}")
    return Fraction(numerator, denominator)


def _real_vector(values: list[int | str | Fraction]) -> Vector:
    return [_g(value) for value in values]


def _linear_combination(terms: list[tuple[Gaussian, list[Fraction]]]) -> Vector:
    vectors = [_scale(scalar, [_g(entry) for entry in basis]) for scalar, basis in terms]
    return _vadd(*vectors)


def _identity(size: int) -> Matrix:
    return [[ONE if row == column else ZERO for column in range(size)] for row in range(size)]


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
    z_vector = [_g(entry) for entry in z]
    return _scale(_inner(z_vector, vector), z_vector)


def _r_trans(w: Vector, g: Vector, blocks: list[list[int]]) -> Fraction:
    total = Fraction(0)
    for block in blocks:
        w_block = _restrict(w, block)
        g_block = _restrict(g, block)
        local = [list(range(len(block)))]
        w_perp = _residual(w_block, local)
        g_perp = _residual(g_block, local)
        total += _sqrt_fraction(_norm2(w_perp) * _norm2(g_perp))
    return total


def _gram(vectors: list[Vector]) -> list[list[Gaussian]]:
    return [[_inner(left, right) for right in vectors] for left in vectors]


def _transverse_gram(vectors: list[Vector], blocks: list[list[int]]) -> list[list[Gaussian]]:
    return _gram([_residual(vector, blocks) for vector in vectors])


def _encode_scalar(value: Gaussian) -> list[str]:
    return [str(value[0]), str(value[1])]


def _encode_vector(vector: Vector) -> list[list[str]]:
    return [_encode_scalar(entry) for entry in vector]


def _encode_matrix(matrix: Matrix) -> list[list[list[str]]]:
    return [_encode_vector(row) for row in matrix]


def _encode_gram(matrix: list[list[Gaussian]]) -> list[list[list[str]]]:
    return [[_encode_scalar(entry) for entry in row] for row in matrix]


def _binary_refinement_fixture() -> dict[str, Any]:
    half = Fraction(1, 2)
    u = [half, half, half, half]
    z = [half, half, -half, -half]
    t = [half, -half, half, -half]
    w = _linear_combination([(_g(2), u), (_g(1, 1), z), (_g(1), t)])
    g_vector = _linear_combination([(_g(3), u), (_g(2, 2), z), (_g(2), t)])
    matrix = _identity(4)
    beta = list(g_vector)
    coarse = [[0, 1, 2, 3]]
    refined = [[0, 1], [2, 3]]

    mw = _average_projection(w, coarse)
    mg = _average_projection(g_vector, coarse)
    mpw = _average_projection(w, refined)
    mpg = _average_projection(g_vector, refined)
    zw = _rank_one(z, w)
    zg = _rank_one(z, g_vector)
    z_vector = [_g(entry) for entry in z]
    moment_w = _inner(z_vector, w)
    moment_g = _inner(z_vector, g_vector)
    delta = _mul(_conj(moment_w), moment_g)
    c_coarse = _inner(mw, mg)
    c_refined = _inner(mpw, mpg)
    q_coarse = _inner(_residual(w, coarse), _residual(g_vector, coarse))
    q_refined = _inner(_residual(w, refined), _residual(g_vector, refined))
    scalar = _inner(w, g_vector)
    r_coarse = _r_trans(w, g_vector, coarse)
    r_refined = _r_trans(w, g_vector, refined)

    if _matvec(matrix, beta) != g_vector:
        raise ValueError("binary fixture source replay failed")
    if _vadd(mw, zw) != mpw or _vadd(mg, zg) != mpg:
        raise ValueError("rank-one block-averaging update failed")
    if c_refined != _add_scalar(c_coarse, delta):
        raise ValueError("longitudinal covariance update failed")
    if q_refined != _sub_scalar(q_coarse, delta):
        raise ValueError("transverse covariance update failed")
    if scalar != _add_scalar(c_coarse, q_coarse) or scalar != _add_scalar(c_refined, q_refined):
        raise ValueError("binary fixture orthogonal decomposition failed")
    if r_refined > r_coarse:
        raise ValueError("binary fixture transverse radius increased")

    fixed_probes = [w, g_vector, _linear_combination([(_g(1, -1), u), (_g(2, -1), z), (_g(-1), t)])]
    gram_coarse = _transverse_gram(fixed_probes, coarse)
    gram_refined = _transverse_gram(fixed_probes, refined)
    moments = [_inner(z_vector, probe) for probe in fixed_probes]
    expected_refined = [
        [
            _sub_scalar(gram_coarse[i][j], _mul(_conj(moments[i]), moments[j]))
            for j in range(len(fixed_probes))
        ]
        for i in range(len(fixed_probes))
    ]
    if gram_refined != expected_refined:
        raise ValueError("fixed-family projected Gram update failed")

    return {
        "label": "EXACT_GAUSSIAN_RATIONAL_BINARY_REFINEMENT_REPLAY",
        "dimension": 4,
        "coarse_blocks": coarse,
        "refined_blocks": refined,
        "split_sizes": [2, 2, 4],
        "z": [str(entry) for entry in z],
        "A": _encode_matrix(matrix),
        "beta": _encode_vector(beta),
        "w": _encode_vector(w),
        "g": _encode_vector(g_vector),
        "derived": {
            "M_coarse_w": _encode_vector(mw),
            "M_refined_w": _encode_vector(mpw),
            "M_coarse_g": _encode_vector(mg),
            "M_refined_g": _encode_vector(mpg),
            "z_tensor_z_w": _encode_vector(zw),
            "z_tensor_z_g": _encode_vector(zg),
            "z_norm_squared": str(_norm2(z_vector)),
            "z_old_block_sum": str(sum(z, Fraction(0))),
            "moment_w": _encode_scalar(moment_w),
            "moment_g": _encode_scalar(moment_g),
            "covariance_increment": _encode_scalar(delta),
            "C_long_coarse": _encode_scalar(c_coarse),
            "C_long_refined": _encode_scalar(c_refined),
            "Q_trans_coarse": _encode_scalar(q_coarse),
            "Q_trans_refined": _encode_scalar(q_refined),
            "C_x": _encode_scalar(scalar),
            "R_trans_coarse": str(r_coarse),
            "R_trans_refined": str(r_refined),
        },
        "fixed_probe_gram": {
            "scope": FIXED_GRAM_SCOPE,
            "probes": [_encode_vector(probe) for probe in fixed_probes],
            "z_moments": [_encode_scalar(moment) for moment in moments],
            "coarse_transverse_gram": _encode_gram(gram_coarse),
            "refined_transverse_gram": _encode_gram(gram_refined),
        },
    }


def _native_projected_groups(matrix: Matrix, beta: Vector, w: Vector, blocks: list[list[int]]) -> tuple[list[dict[str, Any]], Fraction]:
    dimension = len(beta)
    groups: list[dict[str, Any]] = []
    total_radius = Fraction(0)
    for c, output_block in enumerate(blocks):
        local_partition = [list(range(len(output_block)))]
        w_block = _restrict(w, output_block)
        w_perp = _residual(w_block, local_partition)
        projected: list[Vector] = []
        for input_block in blocks:
            beta_b = [beta[index] if index in input_block else ZERO for index in range(dimension)]
            probe = _restrict(_matvec(matrix, beta_b), output_block)
            projected.append(_residual(probe, local_partition))
        gram_perp = _gram(projected)
        norms_squared = [_norm2(probe) for probe in projected]
        active = [index for index, value in enumerate(norms_squared) if value != 0]
        if len(active) > 1:
            raise ValueError("special exact native audit expects at most one active projected probe")
        diagonal = sum(norms_squared, Fraction(0))
        ell_one_squared = diagonal
        mu = Fraction(0)
        upper_squared = diagonal
        contribution = _sqrt_fraction(_norm2(w_perp) * upper_squared)
        total_radius += contribution
        groups.append({
            "c": c,
            "projected_probes": [_encode_vector(probe) for probe in projected],
            "gram_perp": _encode_gram(gram_perp),
            "active_count": len(active),
            "D": str(diagonal),
            "L_squared": str(ell_one_squared),
            "mu": str(mu),
            "U_squared": str(upper_squared),
            "w_perp_squared": str(_norm2(w_perp)),
            "radius_contribution": str(contribution),
        })
    return groups, total_radius


def _partition_metrics(w: Vector, g_vector: Vector, blocks: list[list[int]]) -> dict[str, Any]:
    mw = _average_projection(w, blocks)
    mg = _average_projection(g_vector, blocks)
    c_long = _inner(mw, mg)
    q_trans = _inner(_residual(w, blocks), _residual(g_vector, blocks))
    return {
        "C_long": _encode_scalar(c_long),
        "Q_trans": _encode_scalar(q_trans),
        "R_trans": str(_r_trans(w, g_vector, blocks)),
    }


def _two_coordinate_witness() -> dict[str, Any]:
    matrix: Matrix = [[ZERO, ONE], [ONE, ZERO]]
    beta = _real_vector([-1, 1])
    w = _real_vector([1, -1])
    g_vector = _matvec(matrix, beta)
    coarse = [[0, 1]]
    singleton = [[0], [1]]
    scalar = _inner(w, g_vector)
    coarse_groups, coarse_rcoh = _native_projected_groups(matrix, beta, w, coarse)
    singleton_groups, singleton_rcoh = _native_projected_groups(matrix, beta, w, singleton)
    coarse_metrics = _partition_metrics(w, g_vector, coarse)
    fine_metrics = _partition_metrics(w, g_vector, singleton)
    coarse_metrics["R_coh"] = str(coarse_rcoh)
    fine_metrics["R_coh"] = str(singleton_rcoh)
    if scalar != _g(2):
        raise ValueError("two-coordinate source scalar changed")
    if coarse_metrics != {
        "C_long": ["0", "0"], "Q_trans": ["2", "0"], "R_trans": "2", "R_coh": "2"
    }:
        raise ValueError("coarse witness values changed")
    if fine_metrics != {
        "C_long": ["2", "0"], "Q_trans": ["0", "0"], "R_trans": "0", "R_coh": "0"
    }:
        raise ValueError("fine witness values changed")

    margin_rows: list[dict[str, str]] = []
    for external_error in (Fraction(0), Fraction(1, 2), Fraction(2), Fraction(3)):
        direct = max(abs(scalar[0]) - external_error, Fraction(0))
        coarse_margin = max(Fraction(0) - coarse_rcoh - external_error, Fraction(0))
        fine_margin = max(abs(scalar[0]) - singleton_rcoh - external_error, Fraction(0))
        maximum = max(coarse_margin, fine_margin)
        if maximum != direct:
            raise ValueError("two-coordinate margin maximum failed")
        margin_rows.append({
            "E": str(external_error),
            "coarse_margin": str(coarse_margin),
            "singleton_margin": str(fine_margin),
            "maximum": str(maximum),
            "direct_external_bound": str(direct),
        })

    return {
        "label": NONINVARIANCE_LABEL,
        "quantifier": "THERE_EXISTS_ONE_FIXED_A_BETA_W_WITH_PARTITION_DEPENDENCE",
        "dimension": 2,
        "A": _encode_matrix(matrix),
        "beta": _encode_vector(beta),
        "w": _encode_vector(w),
        "g": _encode_vector(g_vector),
        "C_x": _encode_scalar(scalar),
        "coarse": {"blocks": coarse, "metrics": coarse_metrics, "groups": coarse_groups},
        "singleton": {"blocks": singleton, "metrics": fine_metrics, "groups": singleton_groups},
        "margin_rows": margin_rows,
    }


def _stable_source_fixture() -> dict[str, Any]:
    matrix: Matrix = [[ZERO, ONE], [ONE, ZERO]]
    beta = _real_vector([1, 1])
    w = _real_vector([2, 2])
    g_vector = _matvec(matrix, beta)
    coarse = _partition_metrics(w, g_vector, [[0, 1]])
    fine = _partition_metrics(w, g_vector, [[0], [1]])
    if coarse != fine or coarse["C_long"] != ["4", "0"]:
        raise ValueError("stable-source counterexample failed")
    return {
        "label": "SAME_SOURCE_STABILITY_COUNTEREXAMPLE_TO_EVERY_SOURCE_INSTABILITY",
        "A": _encode_matrix(matrix),
        "beta": _encode_vector(beta),
        "w": _encode_vector(w),
        "g": _encode_vector(g_vector),
        "coarse_metrics": coarse,
        "fine_metrics": fine,
        "contrast_covariance_increment": ["0", "0"],
    }


def _singleton_fixture() -> dict[str, Any]:
    matrix = [
        [_g(0), _g(1), _g(-1)],
        [_g(2), _g(0), _g(1)],
        [_g(-1), _g(3), _g(0)],
    ]
    beta = _real_vector([1, 2, -1])
    w = _real_vector([2, -1, 3])
    g_vector = _matvec(matrix, beta)
    blocks = [[0], [1], [2]]
    groups, r_coh = _native_projected_groups(matrix, beta, w, blocks)
    metrics = _partition_metrics(w, g_vector, blocks)
    scalar = _inner(w, g_vector)
    metrics["R_coh"] = str(r_coh)
    if g_vector != _real_vector([3, 1, 5]) or scalar != _g(20):
        raise ValueError("singleton source replay failed")
    if metrics != {
        "C_long": ["20", "0"], "Q_trans": ["0", "0"], "R_trans": "0", "R_coh": "0"
    }:
        raise ValueError("singleton collapse failed")
    for group in groups:
        if any(group[key] != "0" for key in ("D", "L_squared", "mu", "U_squared", "radius_contribution")):
            raise ValueError("singleton projected data did not vanish")
    return {
        "label": "SINGLETON_COLLAPSE_EXACT_FINITE_SOURCE_REPLAY",
        "dimension": 3,
        "blocks": blocks,
        "A": _encode_matrix(matrix),
        "beta": _encode_vector(beta),
        "w": _encode_vector(w),
        "g": _encode_vector(g_vector),
        "C_x": _encode_scalar(scalar),
        "metrics": metrics,
        "groups": groups,
        "kappa": "UNDEFINED_WHEN_D_EQUALS_ZERO",
    }


def build_document() -> dict[str, Any]:
    payload = {
        "claim_status": CLAIM_STATUS,
        "maximum_claim": MAXIMUM_CLAIM,
        "evidence_label": "EXACT_RATIONAL_STRUCTURAL_REPRODUCTION_ONLY",
        "source_lock": {
            "baseline_HEAD": BASELINE_HEAD,
            "handoff_sha256": HANDOFF_SHA256,
            "source_digests": SOURCE_DIGESTS,
            "literal_source_scope": "I_x=(x/2,x] finite physical coordinates; C_x=<w,A_x beta>",
            "inner_product": "conjugate-linear first",
            "lambda_cb": "1",
        },
        "definitions": {
            "block_projection": "M_P is orthogonal block averaging",
            "rank_one_action": "(z tensor z)h=z<z,h>",
            "binary_update": "M_P'=M_P+z tensor z",
            "covariance_update": "C_long(P')=C_long(P)+conjugate(<z,w>)<z,g>",
            "transverse_update": "Q_trans(P')=Q_trans(P)-conjugate(<z,w>)<z,g>",
            "mu_empty_pair_rule": "mu=0 when fewer than two projected probes are active",
            "kappa_zero_rule": "kappa is undefined at D=0",
            "external_E": "independently certified and fixed while optimizing partitions",
        },
        "firewall": FIREWALL,
        "binary_refinement": _binary_refinement_fixture(),
        "two_coordinate_noninvariance": _two_coordinate_witness(),
        "stable_source_counterexample": _stable_source_fixture(),
        "singleton_collapse": _singleton_fixture(),
        "universal_margin_identity": {
            "statement": "max_P [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+ for every fixed E>=0",
            "upper_reason": "|C_long(P)|-R_coh(P)<=|C_x|",
            "attainment": "the singleton partition has C_long=C_x and R_coh=0",
            "adaptive_partition_gain_over_direct_bound": "0",
        },
        "counts": {
            "binary_refinement_replays": 1,
            "fixed_probe_families": 1,
            "same_source_noninvariance_witnesses": 1,
            "same_source_stability_counterexamples": 1,
            "singleton_replays": 1,
            "two_coordinate_legal_partitions_exhausted": 2,
            "margin_E_values_checked": 4,
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
    parser.add_argument("--check", action="store_true", help="compare with the canonical released JSON")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "tpc252_certificate.json",
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
            f"PASS {SCHEMA} digest={document['digest']} binary=1 fixed_gram=1 "
            "noninvariance=1 stability=1 singleton=1 margin_E=4 canonical_bytes=1"
        )
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(expected_text, encoding="ascii")
    print(
        f"WROTE {args.output} digest={document['digest']} binary=1 fixed_gram=1 "
        "noninvariance=1 stability=1 singleton=1 margin_E=4 canonical_bytes=1"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
