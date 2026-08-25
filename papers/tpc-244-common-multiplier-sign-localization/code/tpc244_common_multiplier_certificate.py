#!/usr/bin/env python3
"""Produce and check the exact TPC-244 sign-localization certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "results" / "tpc244_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
BASELINE_HEAD = "ba1aa9ddb12f42ae390a6d709f40225b2562c009"
HANDOFF_SHA256 = "46704f3f8b61a469799deb6a568451ff8e1298677b57cd4359851dce9d6d74f0"
SOURCE_HASHES = {
    "TPC214_BRIDGE": "8779910e87c77df2b2c1efbd7caac9b03560b71089280b72c9d1e30a34874f69",
    "TPC214_PROOF": "eec983abf4d69fbb14d965872b11513d822df97f682f602c2e0ab35f1eac7c84",
    "TPC228_DERIVATION": "453d7eb8fb39f6af8c24e6e592d7ee5c732cd0e3e9adabeb6b0223c7f6ecdf0f",
    "TPC228_PROOF": "1b6f91f100b89222dc08a070623e6162539b8e88b17b807b2d4ccfb6338da61d",
    "TPC236_SOURCE": "039d9e6e8684eed34ede58b9491c3ddfc57e2097bd36cb930348d4cebc226272",
    "TPC237_SOURCE": "35b338da0a5c8e84c4189022f717e029f45dc1f644291f9748487b8e2bf81d9a",
    "TPC237_PROOF": "9464a698148f57c7b0ed57ad1f45760585d68b6b8d56969de2347833b6aee425",
    "TPC242_PROOF": "b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba",
    "TPC243_PROOF": "e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf",
}
MUTATIONS = [
    "arithmetic_promotion",
    "bool_int_confusion",
    "common_vs_asymmetric_lane_multiplier",
    "complex_multiplier_missing_conjugation",
    "duplicate_json_key",
    "hard_window_factor_two",
    "inner_product_orientation",
    "internal_mobius_erasure",
    "literal_v59_attachment_promotion",
    "nonfinite_json_constant",
    "sign_cut_orientation",
    "strict_endpoint_promotion",
]

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class CertificateFailure(RuntimeError):
    """Fail-closed certificate error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CertificateFailure(message)


def q(value: int | Fraction) -> Fraction:
    demand(type(value) in (int, Fraction), "rational input type")
    return Fraction(value)


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (q(real), q(imag))


def z_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def z_mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def z_conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def z_scale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = q(scalar)
    return (factor * value[0], factor * value[1])


def z_abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def vector_add(left: Vector, right: Vector) -> Vector:
    demand(len(left) == len(right), "vector dimension mismatch")
    return tuple(z_add(a, b) for a, b in zip(left, right))


def vector_scale(value: Vector, scalar: int | Fraction) -> Vector:
    return tuple(z_scale(coordinate, scalar) for coordinate in value)


def inner(first: Vector, second: Vector) -> Gaussian:
    """Conjugate-linear in the first slot and linear in the second."""
    demand(len(first) == len(second), "inner-product dimension mismatch")
    total = z()
    for left, right in zip(first, second):
        total = z_add(total, z_mul(z_conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    result = inner(value, value)
    demand(result[1] == 0 and result[0] >= 0, "invalid squared norm")
    return result[0]


def i_power(exponent: int) -> Gaussian:
    demand(type(exponent) is int, "phase exponent type")
    return (z(1), z(0, 1), z(-1), z(0, -1))[exponent % 4]


def fraction_record(value: Fraction) -> dict[str, int]:
    demand(type(value) is Fraction, "fraction record type")
    return {"denominator": value.denominator, "numerator": value.numerator}


def gaussian_record(value: Gaussian) -> dict[str, dict[str, int]]:
    return {"im": fraction_record(value[1]), "re": fraction_record(value[0])}


def vector_record(value: Vector) -> list[dict[str, dict[str, int]]]:
    return [gaussian_record(coordinate) for coordinate in value]


def sign_patterns(size: int) -> list[tuple[int, ...]]:
    demand(type(size) is int and size >= 0, "sign-pattern size")
    return list(itertools.product((-1, 1), repeat=size))


def direct_sum_fixture() -> dict[str, Any]:
    labels = ("h5", "h7", "h35")
    multipliers = (2, -3, 5)
    b_blocks: tuple[Vector, ...] = (
        (z(1, 1), z(2)),
        (z(-1), z(1, 1)),
        (z(Fraction(1, 2), -1), z(2, 1)),
    )
    w_blocks: tuple[Vector, ...] = (
        (z(2, -1), z(-1, 2)),
        (z(3), z(0, 1)),
        (z(-2), z(1, -1)),
    )

    expected_cov = z()
    expected_b_norm = Fraction(0)
    expected_w_norm = Fraction(0)
    for scalar, b_value, w_value in zip(multipliers, b_blocks, w_blocks):
        expected_cov = z_add(expected_cov, z_scale(inner(w_value, b_value), scalar * scalar))
        expected_b_norm += Fraction(scalar * scalar) * norm_sq(b_value)
        expected_w_norm += Fraction(scalar * scalar) * norm_sq(w_value)

    covariances: list[Gaussian] = []
    b_norms: list[Fraction] = []
    w_norms: list[Fraction] = []
    for signs in sign_patterns(len(labels)):
        b_flat: list[Gaussian] = []
        w_flat: list[Gaussian] = []
        for sign, scalar, b_value, w_value in zip(signs, multipliers, b_blocks, w_blocks):
            b_flat.extend(vector_scale(b_value, sign * scalar))
            w_flat.extend(vector_scale(w_value, sign * scalar))
        b_vector = tuple(b_flat)
        w_vector = tuple(w_flat)
        covariances.append(inner(w_vector, b_vector))
        b_norms.append(norm_sq(b_vector))
        w_norms.append(norm_sq(w_vector))

    demand(all(value == expected_cov for value in covariances), "direct covariance invariance")
    demand(all(value == expected_b_norm for value in b_norms), "direct B norm invariance")
    demand(all(value == expected_w_norm for value in w_norms), "direct W norm invariance")
    return {
        "block_count": len(labels),
        "blocks": list(labels),
        "common_multipliers": list(multipliers),
        "covariance": gaussian_record(expected_cov),
        "b_norm_sq": fraction_record(expected_b_norm),
        "w_norm_sq": fraction_record(expected_w_norm),
        "pattern_count": len(covariances),
        "all_common_sign_patterns_invariant": True,
        "classification": FINITE_CLASS,
    }


def overlap_fixture() -> dict[str, Any]:
    labels = ("h5", "h7", "h35")
    multipliers = (2, -3, 5)
    b_images: tuple[Vector, ...] = (
        (z(1), z()),
        (z(1), z(1)),
        (z(), z(1)),
    )
    w_images: tuple[Vector, ...] = (
        (z(1), z(1)),
        (z(), z(1)),
        (z(1), z(-1)),
    )

    matrix = [[inner(w_value, b_value) for b_value in b_images] for w_value in w_images]
    diagonal = z()
    edges: dict[tuple[int, int], Gaussian] = {}
    for h in range(3):
        diagonal = z_add(diagonal, z_scale(matrix[h][h], multipliers[h] ** 2))
        for k in range(h + 1, 3):
            pair = z_add(matrix[h][k], matrix[k][h])
            edges[(h, k)] = z_scale(pair, multipliers[h] * multipliers[k])

    all_positive = tuple(1 for _ in labels)
    q_values: dict[str, dict[str, dict[str, int]]] = {}
    for signs in sign_patterns(3):
        b_total: Vector = (z(), z())
        w_total: Vector = (z(), z())
        for sign, scalar, b_value, w_value in zip(signs, multipliers, b_images, w_images):
            b_total = vector_add(b_total, vector_scale(b_value, sign * scalar))
            w_total = vector_add(w_total, vector_scale(w_value, sign * scalar))
        direct_q = inner(w_total, b_total)
        polynomial_q = diagonal
        for (h, k), edge in edges.items():
            polynomial_q = z_add(polynomial_q, z_scale(edge, signs[h] * signs[k]))
        demand(direct_q == polynomial_q, "overlap polynomial identity")

        baseline_q = diagonal
        for edge in edges.values():
            baseline_q = z_add(baseline_q, edge)
        cut_sum = z()
        for (h, k), edge in edges.items():
            if signs[h] != signs[k]:
                cut_sum = z_add(cut_sum, edge)
        demand(z_add(baseline_q, z_scale(cut_sum, -2)) == direct_q, "cut identity")
        key = "".join("+" if sign == 1 else "-" for sign in signs)
        q_values[key] = gaussian_record(direct_q)

    demand(len({json.dumps(value, sort_keys=True) for value in q_values.values()}) > 1,
           "overlap fixture must be sign-sensitive")
    edge_records = {
        labels[h] + "--" + labels[k]: gaussian_record(value)
        for (h, k), value in edges.items()
    }
    return {
        "blocks": list(labels),
        "common_multipliers": list(multipliers),
        "diagonal_D": gaussian_record(diagonal),
        "symmetrized_edges": edge_records,
        "q_by_sign_pattern": q_values,
        "pattern_count": len(q_values),
        "cut_identity_all_patterns": True,
        "sign_sensitive": True,
        "classification": FINITE_CLASS,
    }


def synthesize(coefficients: Vector, frequency_quarters: tuple[int, ...], start: int, length: int) -> Vector:
    demand(len(coefficients) == len(frequency_quarters), "frequency coefficient length")
    output: list[Gaussian] = []
    for n_value in range(start, start + length):
        total = z()
        for coefficient, frequency in zip(coefficients, frequency_quarters):
            total = z_add(total, z_mul(coefficient, i_power(n_value * frequency)))
        output.append(total)
    return tuple(output)


def hard_window_fixture() -> dict[str, Any]:
    frequencies = (0, 1, 2, 3)
    block_index = (0, 0, 1, 2)
    multipliers = (2, -3, 5)
    b_local: Vector = (z(1, 1), z(2, -1), z(-1, 2), z(Fraction(1, 2), 1))
    w_local: Vector = (z(2, -1), z(-1, 1), z(1), z(-2, 1))
    start = -3
    length = 17
    row_bound = Fraction(6)
    epsilon = row_bound / length

    records: dict[str, Any] = {}
    physical_values: list[Gaussian] = []
    coefficient_covariance: Gaussian | None = None
    b_norm_sq: Fraction | None = None
    w_norm_sq: Fraction | None = None
    individual_bound_sq: Fraction | None = None
    max_error_sq = Fraction(0)

    for signs in sign_patterns(3):
        b_coeff = tuple(
            z_scale(value, signs[block] * multipliers[block])
            for value, block in zip(b_local, block_index)
        )
        w_coeff = tuple(
            z_scale(value, signs[block] * multipliers[block])
            for value, block in zip(w_local, block_index)
        )
        covariance = inner(w_coeff, b_coeff)
        bn = norm_sq(b_coeff)
        wn = norm_sq(w_coeff)
        if coefficient_covariance is None:
            coefficient_covariance = covariance
            b_norm_sq = bn
            w_norm_sq = wn
            individual_bound_sq = epsilon * epsilon * bn * wn
        demand(covariance == coefficient_covariance, "hard-window coefficient covariance")
        demand(bn == b_norm_sq and wn == w_norm_sq, "hard-window coefficient norms")

        b_signal = synthesize(b_coeff, frequencies, start, length)
        w_signal = synthesize(w_coeff, frequencies, start, length)
        physical = z_scale(inner(w_signal, b_signal), Fraction(1, length))
        error = z_add(physical, z_scale(covariance, -1))
        error_sq = z_abs_sq(error)
        demand(individual_bound_sq is not None and error_sq <= individual_bound_sq,
               "hard-window individual transfer bound")
        max_error_sq = max(max_error_sq, error_sq)
        physical_values.append(physical)
        key = "".join("+" if sign == 1 else "-" for sign in signs)
        records[key] = {
            "physical_covariance": gaussian_record(physical),
            "error_abs_sq": fraction_record(error_sq),
        }

    demand(b_norm_sq is not None and w_norm_sq is not None, "hard-window nonempty fixture")
    pair_bound_sq = Fraction(4) * epsilon * epsilon * b_norm_sq * w_norm_sq
    max_pair_difference_sq = Fraction(0)
    for left in physical_values:
        for right in physical_values:
            difference_sq = z_abs_sq(z_add(left, z_scale(right, -1)))
            max_pair_difference_sq = max(max_pair_difference_sq, difference_sq)
            demand(difference_sq <= pair_bound_sq, "hard-window pairwise transfer bound")

    return {
        "frequency_quarters": list(frequencies),
        "block_index": list(block_index),
        "interval_M": start,
        "interval_N": length,
        "row_bound_R": fraction_record(row_bound),
        "epsilon": fraction_record(epsilon),
        "coefficient_covariance": gaussian_record(coefficient_covariance),
        "b_norm_sq": fraction_record(b_norm_sq),
        "w_norm_sq": fraction_record(w_norm_sq),
        "individual_bound_sq": fraction_record(individual_bound_sq),
        "pairwise_bound_sq": fraction_record(pair_bound_sq),
        "maximum_error_abs_sq": fraction_record(max_error_sq),
        "maximum_pair_difference_abs_sq": fraction_record(max_pair_difference_sq),
        "patterns": records,
        "pattern_count": len(records),
        "individual_transfer_all_patterns": True,
        "pairwise_factor_two_all_ordered_pairs": True,
        "ordered_pair_count": len(records) ** 2,
        "classification": FINITE_CLASS,
    }


def payload_without_digest() -> dict[str, Any]:
    return {
        "certificate_version": 1,
        "task": "TPC-244",
        "status": STATUS,
        "source_lock": {
            "baseline_head": BASELINE_HEAD,
            "tpc_handoff_sha256": HANDOFF_SHA256,
            "files": SOURCE_HASHES,
        },
        "object_lock": {
            "inner_product": "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
            "coefficient_space": "FINITE_ORTHOGONAL_DIRECT_SUM_OF_BLOCKS",
            "common_multiplier": "SAME_C_H_ON_BOTH_LANES",
            "literal_cluster": "C_h=sum_(d_in_D_x,h|d)mu(d)log(d)/d",
            "physical_covariance_orientation": "Q_I=N^(-1)<T_W,T_B>=F_1",
        },
        "theorem": {
            "classification": "PROVED_STRUCTURAL_L1_ONLY",
            "direct_sum_covariance": "<W,B>=sum_h|C_h|^2<w_h,b_h>",
            "common_unit_phase_invariance": "EXACT_COVARIANCE_AND_BOTH_NORMS",
            "internal_mobius_signs": "PRESERVED_INSIDE_ABS_C_H",
            "overlap_polynomial": "Q(s)=D+sum_(h<k)s_hs_kS_hk",
            "sign_cut_identity": "Q(s)-Q(1)=-2sum_(cut_edges)S_hk",
            "all_sign_invariance": "IFF_EVERY_SYMMETRIZED_EDGE_S_HK_IS_ZERO",
            "hard_window_pairwise_transfer": "<=2epsilon||W||_2||B||_2",
        },
        "fixtures": {
            "direct_sum": direct_sum_fixture(),
            "overlap": overlap_fixture(),
            "hard_window": hard_window_fixture(),
        },
        "scope_firewall": {
            "LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT": "OPEN",
            "PHYSICAL_SPECIALIZATION": "CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT",
            "COEFFICIENT_NORM_PAYMENT": "OPEN",
            "SIGNED_C_H_CANCELLATION": "NONE",
            "ARITHMETIC_L2": "NONE",
            "ARITHMETIC_ADVANCE": "NO",
            "FIXED_ATOM_CREDIT": 0,
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "FULL_GATE_B": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
            "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE": False,
        },
        "route_evaluation": {
            "strongest_positive_result": "COMMON_OUTER_PHASE_INVISIBLE_AND_ALL_NONORTHOGONAL_SIGN_SENSITIVITY_LOCALIZED_TO_CUT_EDGES",
            "strongest_obstruction": "OUTER_C_H_SIGN_CANNOT_CONTROL_SAME_BLOCK_MAIN_COVARIANCE",
            "open_theorem": "LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT_WITH_PAYABLE_NORMS",
            "reusable_structure": "COMMON_MULTIPLIER_DIAGONAL_TO_SIGN_CUT_TO_HARD_WINDOW_LEAKAGE",
            "ROUND2_CLUE": "DECOMPOSE_WITHIN_BLOCK_COVARIANCE_INTO_LONGITUDINAL_AND_TRANSVERSE_PARTS",
        },
        "mutation_firewalls": {
            "rejected": MUTATIONS,
            "rejected_count": len(MUTATIONS),
        },
    }


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def build_document() -> dict[str, Any]:
    payload = payload_without_digest()
    result = dict(payload)
    result["payload_sha256"] = hashlib.sha256(canonical_json(payload)).hexdigest()
    return result


def strict_json_loads(text: str) -> object:
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in pairs:
            demand(type(key) is str and key not in output, "duplicate JSON key")
            output[key] = value
        return output

    def reject_constant(value: str) -> object:
        raise CertificateFailure("nonfinite JSON constant: " + value)

    def reject_float(value: str) -> object:
        raise CertificateFailure("floating JSON number: " + value)

    return json.loads(
        text,
        object_pairs_hook=pairs_hook,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )


def same_typed(candidate: object, expected: object) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return candidate.keys() == expected.keys() and all(
            same_typed(candidate[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(candidate) == len(expected) and all(
            same_typed(left, right) for left, right in zip(candidate, expected)
        )
    return candidate == expected


def write_certificate() -> None:
    document = build_document()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical_json(document) + b"\n")


def check_certificate() -> None:
    demand(CERTIFICATE.is_file(), "missing certificate")
    raw = CERTIFICATE.read_bytes()
    demand(raw.endswith(b"\n") and raw.count(b"\n") == 1, "certificate newline discipline")
    stored = strict_json_loads(raw.decode("ascii"))
    expected = build_document()
    demand(same_typed(stored, expected), "certificate payload mismatch")
    demand(raw == canonical_json(expected) + b"\n", "noncanonical certificate bytes")


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_certificate()
            mode = "write"
        else:
            check_certificate()
            mode = "check"
        document = build_document()
        print("TPC244_COMMON_MULTIPLIER_CERTIFICATE=PASS")
        print("mode=" + mode)
        print("status=" + STATUS)
        print("direct_sign_patterns=" + str(document["fixtures"]["direct_sum"]["pattern_count"]))
        print("overlap_sign_patterns=" + str(document["fixtures"]["overlap"]["pattern_count"]))
        print("hard_window_ordered_pairs=" + str(document["fixtures"]["hard_window"]["ordered_pair_count"]))
        print("literal_v59_two_lane_attachment=OPEN")
        print("arithmetic_advance=NO")
    except (CertificateFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC244_COMMON_MULTIPLIER_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
