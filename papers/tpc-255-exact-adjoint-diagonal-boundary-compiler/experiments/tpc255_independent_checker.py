#!/usr/bin/env python3
"""Independent strict validator and mutation audit for TPC-255."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "TPC255_EXACT_ADJOINT_DIAGONAL_BOUNDARY_CERTIFICATE_V1"
STATUS = "PROVED_EXACT_SOURCE_BACKED_L1_ADJOINT_DIAGONAL_HARD_WINDOW_CHILD_JUMP_COMPILER"
MAXIMUM_CLAIM = (
    "EXACT_SOURCE_BACKED_LITERAL_V59_ADJOINT_HAAR_DECOMPOSITION_INTO_BQ_"
    "WEIGHTED_BETA_MIDPOINT_INPUT_UNIT_CORRECTION_HARD_WINDOW_LEAKAGE_AND_"
    "CHILD_JUMP_LEAKAGE"
)
BASELINE_HEAD = "aa26b3b5a53d71035b337b430fd9b4a261b25233"
HANDOFF_SHA256 = "e3d31a130e97b00bad13f36a97447902259e89170fb8b7df82a0ac32cf11371e"
SOURCE_DIGESTS = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": HANDOFF_SHA256,
    "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md": (
        "cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97"
    ),
    "research/tpc-big-road/bridge_b_literal_v59_source_operator_attachment.md": (
        "54bb956ad55245970a7d5d8852f1472d6a9dae68e940d1f9ced0b4c243271eed"
    ),
    "research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md": (
        "31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16"
    ),
    "research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md": (
        "6e5cb92642bf8fc8f0a3a56a29c4c061359f3794e24345d76a62d2fccf5a21ee"
    ),
    "research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md": (
        "fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a"
    ),
    "research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md": (
        "74e42689e17efad75e9718a9d6ac3d8f3ec9c16239204a4915b0b7bdc17ae218"
    ),
}
FIREWALL = {
    "TPC255_MAXIMUM_CLAIM": MAXIMUM_CLAIM,
    "TPC255_LITERAL_ADJOINT_ORIENTATION": "PROVED_EXACT",
    "TPC255_COMPLETE_UNIT_CENTERED_ROW": "PROVED_EXACT_SOURCE_BACKED_ZERO_FOR_H_GREATER_THAN_2Q",
    "TPC255_DELETED_DIAGONAL_RETURN": "PROVED_EXACT",
    "TPC255_HARD_WINDOW_LEAKAGE": "PROVED_EXACT_IDENTITY_NO_ESTIMATE",
    "TPC255_CHILD_JUMP_LEAKAGE": "PROVED_EXACT_WITH_COEFFICIENT_PLUS_MINUS_ONE_OVER_RHO",
    "TPC255_BQ_WEIGHTED_BETA_MIDPOINT": "PROVED_EXACT_REDUCTION_NO_ESTIMATE",
    "TPC255_INPUT_UNIT_MASK_CORRECTION": "PROVED_EXACT_RETAINED",
    "TPC255_OUTPUT_UNIT_MASK_CORRECTION": "PROVED_EXACT_RETAINED_AND_JOINTLY_CENTERED_ONLY",
    "TPC255_KERNEL_EVENNESS_OR_SELF_ADJOINTNESS": "NOT_ASSUMED",
    "TPC255_ADJOINT_HAAR_SAVING": "OPEN",
    "TPC255_DIAGONAL_BOUNDARY_COLLECTIVE_CANCELLATION": "OPEN",
    "TPC255_SIGN_OR_NONZERO": "OPEN",
    "TPC255_ROUTE_ADVANCE": "YES_EXACT_LITERAL_STRUCTURE",
    "TPC255_LITERAL_ARITHMETIC_STRUCTURE_ADVANCE": "YES",
    "TPC255_ARITHMETIC_ADVANCE": "NO",
    "TPC255_FIXED_ATOM_CREDIT": "0",
    "TPC255_L2": "NONE",
    "TPC255_FULL_GATE_B": "OPEN",
    "TPC255_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
    "TPC255_TWIN_PRIME_RESULT": "NONE",
    "TPC255_STATUS": STATUS,
}
MUTATION_CLASSES = [
    "ADJOINT_CONJUGATE",
    "OUTER_Q_WEIGHT",
    "DELETED_DIAGONAL_SIGN",
    "Q_MINUS_2_VERSUS_Q_MINUS_1",
    "INPUT_UNIT_MASK",
    "OUTPUT_UNIT_MASK",
    "COMPLETE_ROW_P_SIGN",
    "EXTERIOR_E_SIGN",
    "CHILD_JUMP_J_SIGN",
    "CHILD_JUMP_RHO_COEFFICIENT",
    "NONINTEGER_RANK_THRESHOLD",
    "KERNEL_ZERO_NORMALIZATION",
    "POISSON_ZERO_MODE_NORMALIZATION",
    "SCHEMA_AND_SOURCE_HASH",
]

Gaussian = tuple[Fraction, Fraction]
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


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _scale(value: Fraction, entry: Gaussian) -> Gaussian:
    return (value * entry[0], value * entry[1])


def _sum(values: list[Gaussian]) -> Gaussian:
    total = ZERO
    for value in values:
        total = _add(total, value)
    return total


def _gj(value: Gaussian) -> list[str]:
    return [str(value[0]), str(value[1])]


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def _shell(x: Fraction) -> list[int]:
    values: list[int] = []
    q_value = 2
    while q_value**3 * x.denominator <= 8 * x.numerator:
        if _prime(q_value) and q_value**3 * x.denominator > x.numerator:
            values.append(q_value)
        q_value += 1
    return values


def _mu(value: int) -> int:
    remainder = value
    sign = 1
    prime = 2
    while prime * prime <= remainder:
        if remainder % prime == 0:
            remainder //= prime
            sign = -sign
            if remainder % prime == 0:
                return 0
        prime += 1
    return -sign if remainder > 1 else sign


def _lambda_ratio(value: int) -> Fraction:
    for prime in range(2, value + 1):
        if not _prime(prime) or value % prime:
            continue
        remainder = value
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        if remainder == 1:
            return Fraction(1, exponent)
    return Fraction(0)


def _beta(x: Fraction, coordinates: list[int]) -> list[Fraction]:
    values: list[Fraction] = []
    for coordinate in coordinates:
        divisor_sum = 0
        for divisor in range(1, coordinate + 1):
            if coordinate % divisor == 0 and (
                divisor**400 * x.denominator**133 <= x.numerator**133
            ):
                divisor_sum += _mu(divisor)
        values.append(_lambda_ratio(coordinate) - divisor_sum)
    return values


def _sample_kernel() -> dict[int, Gaussian]:
    values: dict[int, Gaussian] = {}
    for shift in range(-9, 10):
        if shift == 0:
            values[shift] = (Fraction(1), Fraction(0))
        else:
            values[shift] = (
                Fraction(((7 * shift + 3) % 17) - 8, abs(shift) + 2),
                Fraction(((5 * shift + 1) % 13) - 6, abs(shift) + 3),
            )
    return values


def _centered_row(q_value: int, t_value: int, u_value: int) -> Fraction:
    if u_value % q_value == 0:
        return Fraction(0)
    return Fraction(int(u_value % q_value == t_value % q_value)) - Fraction(
        1, q_value - 1
    )


def _independent_fixture() -> dict[str, Any]:
    x = Fraction(64)
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    count = len(coordinates)
    ell = count // 2
    right_size = count - ell
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, count)
    q_shell = _shell(x)
    kernel = _sample_kernel()
    beta = _beta(x, coordinates)
    coordinate_set = set(coordinates)
    astar: list[Gaussian] = []
    p_lanes: list[Gaussian] = []
    e_lanes: list[Gaussian] = []
    j_lanes: list[Gaussian] = []
    d_lanes: list[Gaussian] = []
    child_checks = 0
    input_masks = 0
    output_masks = 0
    for t_index, t_value in enumerate(coordinates):
        direct = ZERO
        p_lane = ZERO
        e_lane = ZERO
        j_lane = ZERO
        d_lane = ZERO
        for q_value in q_shell:
            if t_value % q_value == 0:
                input_masks += 1
                continue
            for u_index, u_value in enumerate(coordinates):
                if u_value % q_value == 0:
                    output_masks += 1
                if u_value != t_value:
                    direct = _add(
                        direct,
                        _scale(
                            Fraction(q_value)
                            * _centered_row(q_value, t_value, u_value)
                            * h[u_index],
                            _conj(kernel.get(u_value - t_value, ZERO)),
                        ),
                    )
            p_star = ZERO
            e_star = ZERO
            j_star = ZERO
            for shift, kernel_value in kernel.items():
                u_value = t_value + shift
                row = _scale(
                    _centered_row(q_value, t_value, u_value),
                    _conj(kernel_value),
                )
                p_star = _add(p_star, row)
                if u_value not in coordinate_set:
                    e_star = _add(e_star, row)
                else:
                    j_star = _add(
                        j_star,
                        _scale(h[u_value - coordinates[0]] - h[t_index], row),
                    )
            p_lane = _add(p_lane, _scale(Fraction(q_value) * h[t_index], p_star))
            e_lane = _add(e_lane, _scale(-Fraction(q_value) * h[t_index], e_star))
            j_lane = _add(j_lane, _scale(Fraction(q_value), j_star))
            d_lane = _add(
                d_lane,
                _scale(
                    -Fraction(q_value * (q_value - 2), q_value - 1) * h[t_index],
                    _conj(kernel[0]),
                ),
            )
            opposite = range(ell, count) if t_index < ell else range(ell)
            jump = ZERO
            for u_index in opposite:
                jump = _add(
                    jump,
                    _scale(
                        (h[u_index] - h[t_index])
                        * _centered_row(q_value, t_value, coordinates[u_index]),
                        _conj(kernel.get(coordinates[u_index] - t_value, ZERO)),
                    ),
                )
            if jump != j_star:
                raise CertificateError("independent child jump mismatch")
            child_checks += 1
        formula = _sum([p_lane, e_lane, j_lane, d_lane])
        if formula != direct:
            raise CertificateError("independent coordinate formula mismatch")
        astar.append(direct)
        p_lanes.append(p_lane)
        e_lanes.append(e_lane)
        j_lanes.append(j_lane)
        d_lanes.append(d_lane)
    a_beta: list[Gaussian] = []
    for u_value in coordinates:
        total = ZERO
        for t_index, t_value in enumerate(coordinates):
            if u_value == t_value:
                continue
            for q_value in q_shell:
                if u_value % q_value == 0 or t_value % q_value == 0:
                    continue
                total = _add(
                    total,
                    _scale(
                        Fraction(q_value)
                        * _centered_row(q_value, t_value, u_value)
                        * beta[t_index],
                        kernel.get(u_value - t_value, ZERO),
                    ),
                )
        a_beta.append(total)
    lhs = _sum([_scale(h[index], value) for index, value in enumerate(a_beta)])
    rhs = _sum(
        [_scale(beta[index], _conj(value)) for index, value in enumerate(astar)]
    )
    parts_values = {
        "complete_row_alias": _sum(
            [_scale(beta[index], _conj(value)) for index, value in enumerate(p_lanes)]
        ),
        "hard_window": _sum(
            [_scale(beta[index], _conj(value)) for index, value in enumerate(e_lanes)]
        ),
        "child_jump": _sum(
            [_scale(beta[index], _conj(value)) for index, value in enumerate(j_lanes)]
        ),
        "deleted_diagonal": _sum(
            [_scale(beta[index], _conj(value)) for index, value in enumerate(d_lanes)]
        ),
    }
    scalar_sum = _sum(list(parts_values.values()))
    b_q = sum((Fraction(q * (q - 2), q - 1) for q in q_shell), Fraction(0))
    h_beta = sum((h[index] * beta[index] for index in range(count)), Fraction(0))
    correction = Fraction(0)
    for q_value in q_shell:
        correction += Fraction(q_value * (q_value - 2), q_value - 1) * sum(
            (
                h[index] * beta[index]
                for index, t_value in enumerate(coordinates)
                if t_value % q_value == 0
            ),
            Fraction(0),
        )
    diagonal = -b_q * h_beta + correction
    if lhs != rhs or rhs != scalar_sum or parts_values["deleted_diagonal"] != (diagonal, 0):
        raise CertificateError("independent scalar reassembly mismatch")
    if rho_squared * sum((entry * entry for entry in h), Fraction(0)) != 1:
        raise CertificateError("independent rank normalization mismatch")
    return {
        "x": "64",
        "coordinates": coordinates,
        "count": count,
        "ell": ell,
        "right_size": right_size,
        "rho_squared": str(rho_squared),
        "h_sha256": _digest([str(entry) for entry in h]),
        "rank_normalization": "1",
        "q_shell": q_shell,
        "b_q": str(b_q),
        "kernel_support": [min(kernel), max(kernel)],
        "kernel_sha256": _digest([[shift, *_gj(kernel[shift])] for shift in sorted(kernel)]),
        "kernel_zero": _gj(kernel[0]),
        "kernel_non_even_witness": [_gj(kernel[-1]), _gj(kernel[1])],
        "literal_beta_sha256": _digest([str(entry) for entry in beta]),
        "literal_beta_nonzero_count": sum(entry != 0 for entry in beta),
        "a_star_h_sha256": _digest([_gj(entry) for entry in astar]),
        "formula_sha256": _digest([_gj(entry) for entry in astar]),
        "p_lane_sha256": _digest([_gj(entry) for entry in p_lanes]),
        "e_lane_sha256": _digest([_gj(entry) for entry in e_lanes]),
        "j_lane_sha256": _digest([_gj(entry) for entry in j_lanes]),
        "diagonal_lane_sha256": _digest([_gj(entry) for entry in d_lanes]),
        "coordinate_identities": count,
        "child_jump_checks": child_checks,
        "input_masked_q_rows": input_masks,
        "output_masked_terms_seen": output_masks,
        "lhs_inner_h_a_beta": _gj(lhs),
        "rhs_inner_astar_h_beta": _gj(rhs),
        "scalar_parts": {key: _gj(value) for key, value in parts_values.items()},
        "scalar_sum": _gj(scalar_sum),
        "h_beta": str(h_beta),
        "input_unit_correction": str(correction),
        "diagonal_bq_reassembly": str(diagonal),
        "fixture_scope": (
            "NONLITERAL_NON_EVEN_GAUSSIAN_RATIONAL_KERNEL_SUBSTITUTED_INTO_"
            "THE_LITERAL_OPERATOR_SHAPE_FOR_FINITE_ALGEBRA_ONLY"
        ),
    }


def _source_contract() -> dict[str, Any]:
    x = Fraction(27, 5)
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    ell = len(coordinates) // 2
    right_size = len(coordinates) - ell
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, len(coordinates))
    naive = [entry for entry in coordinates if entry <= _floor(3 * x / 4)]
    zero_mode = Fraction(16) * Fraction(7, 5) / (7 * 6)
    return {
        "poisson_attachment": {
            "theorem": "V43_D_EQUALS_1_COMPLETE_UNIT_CENTERED_ROW",
            "h_fixture": 16,
            "q_upper_clock_fixture": 4,
            "q_fixture": [5, 7],
            "strict_h_greater_than_2q_clock": True,
            "dual_ratios": ["16/5", "16/7"],
            "profile_support": ["-1", "1"],
            "reflected_conjugated_profile": "PHI_V_EQUALS_CONJUGATE_PSI_PLUS_OF_MINUS_V",
            "p_star_conclusion": "EXACT_ZERO_BY_SOURCE_THEOREM_NOT_FINITE_NUMERICAL_EVIDENCE",
        },
        "unit_mask": {
            "q": 7,
            "t_residue": 1,
            "period_sum_c": "-1/6",
            "period_sum_d": "1/6",
            "period_sum_v": "0",
            "h_fixture": 16,
            "psi_plus_zero_fixture": "7/5",
            "raw_zero_mode": str(-zero_mode),
            "correction_zero_mode": str(zero_mode),
            "combined_zero_mode": "0",
            "residue_class_main_term": "16/5",
            "kernel_zero": "1",
            "normalizations_are_distinct": True,
        },
        "noninteger_rank": {
            "x": "27/5",
            "coordinates": coordinates,
            "ell": ell,
            "right_size": right_size,
            "rank_left": coordinates[:ell],
            "naive_three_quarter_left": naive,
            "mismatch_detected": coordinates[:ell] != naive,
            "rho_squared": str(rho_squared),
            "rho_squared_h_norm_squared": str(
                rho_squared * sum((entry * entry for entry in h), Fraction(0))
            ),
        },
        "absolute_convergence": (
            "SMOOTH_COMPACTLY_SUPPORTED_FOURIER_PROFILE_IMPLIES_SCHWARTZ_"
            "PHYSICAL_KERNEL_AND_ABSOLUTE_LATTICE_SUMMABILITY"
        ),
        "asymptotic_test_status": (
            "NOT_EXECUTED_FINITE_CERTIFICATE_CANNOT_PROVE_UPSTREAM_POISSON_"
            "OR_ANY_ARITHMETIC_ESTIMATE"
        ),
    }


def _expected() -> dict[str, Any]:
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "maximum_claim": MAXIMUM_CLAIM,
        "baseline_head": BASELINE_HEAD,
        "handoff_sha256": HANDOFF_SHA256,
        "source_digests": SOURCE_DIGESTS,
        "firewall": FIREWALL,
        "source_contract": _source_contract(),
        "fixture": _independent_fixture(),
        "mutation_classes": MUTATION_CLASSES,
        "mutation_required_minimum": 64,
        "stress_required_families": 192,
        "executable_scope": (
            "FINITE_EXACT_ALGEBRA_AND_SOURCE_CONTRACT_TYPING_ONLY_NOT_"
            "ASYMPTOTIC_EVIDENCE"
        ),
    }
    return {"payload": payload, "payload_sha256": _digest(payload)}


def _strict_types(actual: Any, expected: Any, location: str = "root") -> None:
    if type(expected) is int:
        if type(actual) is not int:
            raise CertificateError(location + ": exact int required; bool rejected")
        return
    if type(expected) is bool:
        if type(actual) is not bool:
            raise CertificateError(location + ": exact bool required")
        return
    if isinstance(expected, str):
        if not isinstance(actual, str):
            raise CertificateError(location + ": string required")
        return
    if isinstance(expected, list):
        if not isinstance(actual, list) or len(actual) != len(expected):
            raise CertificateError(location + ": list shape mismatch")
        for index, expected_entry in enumerate(expected):
            _strict_types(actual[index], expected_entry, location + "[" + str(index) + "]")
        return
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(actual) != set(expected):
            raise CertificateError(location + ": object keys mismatch")
        for key, expected_entry in expected.items():
            _strict_types(actual[key], expected_entry, location + "." + key)
        return
    raise CertificateError(location + ": unsupported expected type")


def _parse(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as error:
        raise CertificateError("certificate must be ASCII-safe UTF-8") from error
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_constant=_constant)
    except (json.JSONDecodeError, CertificateError) as error:
        raise CertificateError("strict JSON parse failed: " + str(error)) from error
    if not isinstance(value, dict):
        raise CertificateError("top-level document must be object")
    if raw != _canonical(value) + b"\n":
        raise CertificateError("document is not canonical single-LF JSON")
    return value


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _verify_sources() -> None:
    repository = _repository_root()
    bridge = "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md"
    for path, expected_hash in SOURCE_DIGESTS.items():
        if path == bridge:
            source = (repository / path).read_bytes().replace(b"\r\n", b"\n")
        else:
            completed = subprocess.run(
                ["git", "show", BASELINE_HEAD + ":" + path],
                cwd=repository,
                check=False,
                capture_output=True,
            )
            if completed.returncode != 0 or completed.stderr:
                raise CertificateError("source lock unavailable: " + path)
            source = completed.stdout.replace(b"\r\n", b"\n")
        if hashlib.sha256(source).hexdigest() != expected_hash:
            raise CertificateError("source hash mismatch: " + path)


def _validate(raw: bytes, verify_sources: bool) -> dict[str, Any]:
    document = _parse(raw)
    expected = _expected()
    _strict_types(document, expected)
    if document != expected:
        raise CertificateError("certificate differs from independent exact reconstruction")
    if verify_sources:
        _verify_sources()
    return document


def _set_path(document: Any, path: tuple[Any, ...], value: Any) -> None:
    target = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def _seal(document: dict[str, Any]) -> None:
    document["payload_sha256"] = _digest(document["payload"])


def _expect_rejected(raw: bytes, label: str) -> None:
    try:
        _validate(raw, verify_sources=False)
    except CertificateError:
        return
    raise CertificateError("mutation survived: " + label)


def _mutation_suite(document: dict[str, Any]) -> tuple[int, dict[str, int]]:
    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("ADJOINT_CONJUGATE", ("payload", "fixture", "rhs_inner_astar_h_beta", 1), "507799/1596672"),
        ("OUTER_Q_WEIGHT", ("payload", "fixture", "b_q"), "23/12"),
        ("DELETED_DIAGONAL_SIGN", ("payload", "fixture", "diagonal_bq_reassembly"), "245/288"),
        ("Q_MINUS_2_VERSUS_Q_MINUS_1", ("payload", "fixture", "input_unit_correction"), "-5/84"),
        ("INPUT_UNIT_MASK", ("payload", "fixture", "input_masked_q_rows"), 0),
        ("OUTPUT_UNIT_MASK", ("payload", "fixture", "output_masked_terms_seen"), 0),
        ("COMPLETE_ROW_P_SIGN", ("payload", "fixture", "scalar_parts", "complete_row_alias", 0), "1100291/2280960"),
        ("EXTERIOR_E_SIGN", ("payload", "fixture", "scalar_parts", "hard_window", 0), "94751/7983360"),
        ("CHILD_JUMP_J_SIGN", ("payload", "fixture", "scalar_parts", "child_jump", 1), "-114683/532224"),
        ("CHILD_JUMP_RHO_COEFFICIENT", ("payload", "fixture", "child_jump_checks"), 52),
        ("NONINTEGER_RANK_THRESHOLD", ("payload", "source_contract", "noninteger_rank", "rank_left"), [3, 4]),
        ("KERNEL_ZERO_NORMALIZATION", ("payload", "fixture", "kernel_zero", 0), "0"),
        ("POISSON_ZERO_MODE_NORMALIZATION", ("payload", "source_contract", "unit_mask", "residue_class_main_term"), "16/7"),
        ("SCHEMA_AND_SOURCE_HASH", ("payload", "schema"), "TPC255_BROKEN"),
    ]
    extra_paths: list[tuple[Any, ...]] = [
        ("payload", "status"),
        ("payload", "maximum_claim"),
        ("payload", "baseline_head"),
        ("payload", "handoff_sha256"),
        ("payload", "mutation_required_minimum"),
        ("payload", "stress_required_families"),
        ("payload", "executable_scope"),
        ("payload", "fixture", "x"),
        ("payload", "fixture", "coordinates", 0),
        ("payload", "fixture", "coordinates", 15),
        ("payload", "fixture", "count"),
        ("payload", "fixture", "ell"),
        ("payload", "fixture", "right_size"),
        ("payload", "fixture", "rho_squared"),
        ("payload", "fixture", "h_sha256"),
        ("payload", "fixture", "rank_normalization"),
        ("payload", "fixture", "q_shell", 0),
        ("payload", "fixture", "kernel_support", 0),
        ("payload", "fixture", "kernel_sha256"),
        ("payload", "fixture", "kernel_non_even_witness", 0, 1),
        ("payload", "fixture", "literal_beta_sha256"),
        ("payload", "fixture", "literal_beta_nonzero_count"),
        ("payload", "fixture", "a_star_h_sha256"),
        ("payload", "fixture", "formula_sha256"),
        ("payload", "fixture", "p_lane_sha256"),
        ("payload", "fixture", "e_lane_sha256"),
        ("payload", "fixture", "j_lane_sha256"),
        ("payload", "fixture", "diagonal_lane_sha256"),
        ("payload", "fixture", "coordinate_identities"),
        ("payload", "fixture", "lhs_inner_h_a_beta", 0),
        ("payload", "fixture", "scalar_sum", 1),
        ("payload", "fixture", "h_beta"),
        ("payload", "fixture", "fixture_scope"),
        ("payload", "source_contract", "poisson_attachment", "h_fixture"),
        ("payload", "source_contract", "poisson_attachment", "q_upper_clock_fixture"),
        ("payload", "source_contract", "poisson_attachment", "q_fixture", 1),
        ("payload", "source_contract", "poisson_attachment", "strict_h_greater_than_2q_clock"),
        ("payload", "source_contract", "poisson_attachment", "dual_ratios", 0),
        ("payload", "source_contract", "poisson_attachment", "profile_support", 1),
        ("payload", "source_contract", "poisson_attachment", "p_star_conclusion"),
        ("payload", "source_contract", "unit_mask", "q"),
        ("payload", "source_contract", "unit_mask", "period_sum_c"),
        ("payload", "source_contract", "unit_mask", "period_sum_d"),
        ("payload", "source_contract", "unit_mask", "combined_zero_mode"),
        ("payload", "source_contract", "unit_mask", "normalizations_are_distinct"),
        ("payload", "source_contract", "noninteger_rank", "x"),
        ("payload", "source_contract", "noninteger_rank", "coordinates", 1),
        ("payload", "source_contract", "noninteger_rank", "ell"),
        ("payload", "source_contract", "noninteger_rank", "mismatch_detected"),
        ("payload", "source_contract", "absolute_convergence"),
        ("payload", "source_contract", "asymptotic_test_status"),
    ]
    for index, path in enumerate(extra_paths):
        target: Any = document
        for key in path:
            target = target[key]
        if type(target) is int:
            replacement: Any = True if index % 3 == 0 else target + 1
        elif type(target) is bool:
            replacement = not target
        elif isinstance(target, str):
            replacement = target + "_MUTATED"
        else:
            replacement = None
        mutations.append(("SCHEMA_AND_SOURCE_HASH", path, replacement))
    for path in SOURCE_DIGESTS:
        mutations.append(
            (
                "SCHEMA_AND_SOURCE_HASH",
                ("payload", "source_digests", path),
                "0" * 64,
            )
        )
    for index in range(len(FIREWALL)):
        key = sorted(FIREWALL)[index]
        mutations.append(
            ("SCHEMA_AND_SOURCE_HASH", ("payload", "firewall", key), "BROKEN")
        )
    counts = {label: 0 for label in MUTATION_CLASSES}
    rejected = 0
    for label, path, value in mutations:
        mutated = copy.deepcopy(document)
        _set_path(mutated, path, value)
        _seal(mutated)
        _expect_rejected(_canonical(mutated) + b"\n", label)
        counts[label] += 1
        rejected += 1
    digest_mutation = copy.deepcopy(document)
    digest_mutation["payload_sha256"] = "0" * 64
    _expect_rejected(_canonical(digest_mutation) + b"\n", "SCHEMA_AND_SOURCE_HASH")
    counts["SCHEMA_AND_SOURCE_HASH"] += 1
    rejected += 1
    canonical = _canonical(document)
    malformed = [
        canonical.replace(b'{"payload":', b'{"payload":null,"payload":', 1) + b"\n",
        canonical.replace(b'"count":32', b'"count":NaN', 1) + b"\n",
        canonical + b" \n",
        canonical + b"\n\n",
    ]
    for raw in malformed:
        _expect_rejected(raw, "SCHEMA_AND_SOURCE_HASH")
        counts["SCHEMA_AND_SOURCE_HASH"] += 1
        rejected += 1
    return rejected, counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    path = Path(__file__).resolve().parents[1] / "results" / "tpc255_certificate.json"
    document = _validate(path.read_bytes(), verify_sources=True)
    rejected, counts = _mutation_suite(document)
    if rejected < 64 or any(counts[label] == 0 for label in MUTATION_CLASSES):
        raise SystemExit("TPC255_INDEPENDENT_CHECK=FAIL mutation coverage")
    print(
        "TPC255_INDEPENDENT_CHECK=PASS mutations_rejected=" + str(rejected)
        + " classes=" + str(len(MUTATION_CLASSES))
        + " source_hashes=" + str(len(SOURCE_DIGESTS))
        + " producer_imported=NO"
    )


if __name__ == "__main__":
    main()
