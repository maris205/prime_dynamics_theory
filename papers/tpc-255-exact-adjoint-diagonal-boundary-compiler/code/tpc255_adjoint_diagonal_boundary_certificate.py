#!/usr/bin/env python3
"""Check the exact finite TPC-255 algebra certificate.

The finite fixture substitutes a non-even Gaussian-rational kernel into the
literal V59 operator shape.  It checks algebra and source-contract typing only;
it is not numerical evidence for any asymptotic estimate or Poisson theorem.
"""

from __future__ import annotations

import argparse
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
    "TPC255_COMPLETE_UNIT_CENTERED_ROW": (
        "PROVED_EXACT_SOURCE_BACKED_ZERO_FOR_H_GREATER_THAN_2Q"
    ),
    "TPC255_DELETED_DIAGONAL_RETURN": "PROVED_EXACT",
    "TPC255_HARD_WINDOW_LEAKAGE": "PROVED_EXACT_IDENTITY_NO_ESTIMATE",
    "TPC255_CHILD_JUMP_LEAKAGE": (
        "PROVED_EXACT_WITH_COEFFICIENT_PLUS_MINUS_ONE_OVER_RHO"
    ),
    "TPC255_BQ_WEIGHTED_BETA_MIDPOINT": "PROVED_EXACT_REDUCTION_NO_ESTIMATE",
    "TPC255_INPUT_UNIT_MASK_CORRECTION": "PROVED_EXACT_RETAINED",
    "TPC255_OUTPUT_UNIT_MASK_CORRECTION": (
        "PROVED_EXACT_RETAINED_AND_JOINTLY_CENTERED_ONLY"
    ),
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


def _g(real: int | Fraction, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


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


def _scale(value: Fraction, entry: Gaussian) -> Gaussian:
    return (value * entry[0], value * entry[1])


def _gsum(values: list[Gaussian]) -> Gaussian:
    total = ZERO
    for value in values:
        total = _add(total, value)
    return total


def _gj(value: Gaussian) -> list[str]:
    return [str(value[0]), str(value[1])]


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


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
    while q_value**3 * x.denominator <= 8 * x.numerator:
        if _is_prime(q_value) and q_value**3 * x.denominator > x.numerator:
            result.append(q_value)
        q_value += 1
    return result


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
        prime += 1
    if remainder > 1:
        sign = -sign
    return sign


def _lambda_over_log(value: int) -> Fraction:
    for prime in range(2, value + 1):
        if not _is_prime(prime) or value % prime != 0:
            continue
        remainder = value
        exponent = 0
        while remainder % prime == 0:
            remainder //= prime
            exponent += 1
        if remainder == 1:
            return Fraction(1, exponent)
    return Fraction(0)


def _literal_beta(x: Fraction, coordinates: list[int]) -> list[Fraction]:
    result: list[Fraction] = []
    for value in coordinates:
        divisor_sum = 0
        for divisor in range(1, value + 1):
            if value % divisor != 0:
                continue
            if (
                divisor**400 * x.denominator**133
                <= x.numerator**133
            ):
                divisor_sum += _mobius(divisor)
        result.append(_lambda_over_log(value) - divisor_sum)
    return result


def _kernel() -> dict[int, Gaussian]:
    result: dict[int, Gaussian] = {}
    for shift in range(-9, 10):
        if shift == 0:
            result[shift] = _g(1)
        else:
            real = Fraction(((7 * shift + 3) % 17) - 8, abs(shift) + 2)
            imag = Fraction(((5 * shift + 1) % 13) - 6, abs(shift) + 3)
            result[shift] = (real, imag)
    return result


def _rank(x: Fraction) -> tuple[list[int], int, int, list[Fraction], Fraction]:
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    if len(coordinates) < 2:
        raise ValueError("rank midpoint requires N>=2")
    ell = len(coordinates) // 2
    right_size = len(coordinates) - ell
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, len(coordinates))
    return coordinates, ell, right_size, h, rho_squared


def _v(q_value: int, t_value: int, u_value: int) -> Fraction:
    if u_value % q_value == 0:
        return Fraction(0)
    return Fraction(1 if u_value % q_value == t_value % q_value else 0) - Fraction(
        1, q_value - 1
    )


def _row_terms(
    coordinates: list[int],
    h: list[Fraction],
    kernel: dict[int, Gaussian],
    q_value: int,
    t_index: int,
) -> tuple[Gaussian, Gaussian, Gaussian, Gaussian]:
    t_value = coordinates[t_index]
    p_star = ZERO
    e_star = ZERO
    j_star = ZERO
    coordinate_set = set(coordinates)
    for shift, kernel_value in kernel.items():
        u_value = t_value + shift
        row_value = _scale(_v(q_value, t_value, u_value), _conj(kernel_value))
        p_star = _add(p_star, row_value)
        if u_value not in coordinate_set:
            e_star = _add(e_star, row_value)
        else:
            u_index = u_value - coordinates[0]
            j_star = _add(j_star, _scale(h[u_index] - h[t_index], row_value))
    diagonal = _scale(
        -Fraction(q_value - 2, q_value - 1) * h[t_index],
        _conj(kernel[0]),
    )
    return p_star, e_star, j_star, diagonal


def _astar_direct(
    coordinates: list[int],
    h: list[Fraction],
    kernel: dict[int, Gaussian],
    q_shell: list[int],
    t_index: int,
) -> Gaussian:
    t_value = coordinates[t_index]
    total = ZERO
    for q_value in q_shell:
        if t_value % q_value == 0:
            continue
        for u_index, u_value in enumerate(coordinates):
            if u_value == t_value:
                continue
            coefficient = q_value * _v(q_value, t_value, u_value)
            total = _add(
                total,
                _scale(
                    coefficient * h[u_index],
                    _conj(kernel.get(u_value - t_value, ZERO)),
                ),
            )
    return total


def _coordinate_fixture() -> dict[str, Any]:
    x = Fraction(64)
    coordinates, ell, right_size, h, rho_squared = _rank(x)
    q_shell = _prime_shell(x)
    kernel = _kernel()
    beta = _literal_beta(x, coordinates)
    direct: list[Gaussian] = []
    predicted: list[Gaussian] = []
    p_rows: list[Gaussian] = []
    e_rows: list[Gaussian] = []
    j_rows: list[Gaussian] = []
    diagonal_rows: list[Gaussian] = []
    input_masked_rows = 0
    output_masked_terms = 0
    child_checks = 0
    for t_index, t_value in enumerate(coordinates):
        direct_value = _astar_direct(coordinates, h, kernel, q_shell, t_index)
        formula_value = ZERO
        p_total = ZERO
        e_total = ZERO
        j_total = ZERO
        d_total = ZERO
        for q_value in q_shell:
            if t_value % q_value == 0:
                input_masked_rows += 1
                continue
            p_star, e_star, j_star, diagonal = _row_terms(
                coordinates, h, kernel, q_value, t_index
            )
            p_total = _add(p_total, _scale(Fraction(q_value) * h[t_index], p_star))
            e_total = _add(e_total, _scale(-Fraction(q_value) * h[t_index], e_star))
            j_total = _add(j_total, _scale(Fraction(q_value), j_star))
            d_total = _add(d_total, _scale(Fraction(q_value), diagonal))
            for u_value in coordinates:
                if u_value % q_value == 0:
                    output_masked_terms += 1
            opposite = range(ell, len(coordinates)) if t_index < ell else range(0, ell)
            jump_direct = ZERO
            for u_index in opposite:
                row = _scale(
                    _v(q_value, t_value, coordinates[u_index]),
                    _conj(kernel.get(coordinates[u_index] - t_value, ZERO)),
                )
                jump_direct = _add(
                    jump_direct,
                    _scale(h[u_index] - h[t_index], row),
                )
            if jump_direct != j_star:
                raise ValueError("child jump support identity failed")
            child_checks += 1
        formula_value = _gsum([p_total, e_total, j_total, d_total])
        if direct_value != formula_value:
            raise ValueError("coordinate decomposition failed")
        direct.append(direct_value)
        predicted.append(formula_value)
        p_rows.append(p_total)
        e_rows.append(e_total)
        j_rows.append(j_total)
        diagonal_rows.append(d_total)

    a_beta: list[Gaussian] = []
    for u_index, u_value in enumerate(coordinates):
        total = ZERO
        for t_index, t_value in enumerate(coordinates):
            if u_value == t_value:
                continue
            for q_value in q_shell:
                if u_value % q_value == 0 or t_value % q_value == 0:
                    continue
                coefficient = q_value * _v(q_value, t_value, u_value) * beta[t_index]
                total = _add(
                    total,
                    _scale(coefficient, kernel.get(u_value - t_value, ZERO)),
                )
        a_beta.append(total)
    lhs = _gsum([_scale(h[index], value) for index, value in enumerate(a_beta)])
    rhs = _gsum(
        [_scale(beta[index], _conj(value)) for index, value in enumerate(direct)]
    )
    scalar_parts = {
        "complete_row_alias": _gj(
            _gsum([_scale(beta[index], _conj(value)) for index, value in enumerate(p_rows)])
        ),
        "hard_window": _gj(
            _gsum([_scale(beta[index], _conj(value)) for index, value in enumerate(e_rows)])
        ),
        "child_jump": _gj(
            _gsum([_scale(beta[index], _conj(value)) for index, value in enumerate(j_rows)])
        ),
        "deleted_diagonal": _gj(
            _gsum(
                [_scale(beta[index], _conj(value)) for index, value in enumerate(diagonal_rows)]
            )
        ),
    }
    scalar_sum = _gsum(
        [
            (Fraction(entry[0]), Fraction(entry[1]))
            for entry in scalar_parts.values()
        ]
    )
    b_q = sum((Fraction(q * (q - 2), q - 1) for q in q_shell), Fraction(0))
    h_beta = sum((h[index] * beta[index] for index in range(len(h))), Fraction(0))
    input_correction = Fraction(0)
    for q_value in q_shell:
        weight = Fraction(q_value * (q_value - 2), q_value - 1)
        input_correction += weight * sum(
            (
                h[index] * beta[index]
                for index, t_value in enumerate(coordinates)
                if t_value % q_value == 0
            ),
            Fraction(0),
        )
    diagonal_bq = -b_q * h_beta + input_correction
    diagonal_scalar = Fraction(scalar_parts["deleted_diagonal"][0])
    if lhs != rhs or rhs != scalar_sum or diagonal_scalar != diagonal_bq:
        raise ValueError("scalar adjoint or B_Q identity failed")
    if rho_squared * sum((entry * entry for entry in h), Fraction(0)) != 1:
        raise ValueError("rank normalization failed")
    if kernel[1] == kernel[-1] or kernel[-1][1] == 0:
        raise ValueError("kernel fixture lost non-even complex witness")
    return {
        "x": str(x),
        "coordinates": coordinates,
        "count": len(coordinates),
        "ell": ell,
        "right_size": right_size,
        "rho_squared": str(rho_squared),
        "h_sha256": _digest([str(entry) for entry in h]),
        "rank_normalization": "1",
        "q_shell": q_shell,
        "b_q": str(b_q),
        "kernel_support": [min(kernel), max(kernel)],
        "kernel_sha256": _digest(
            [[shift, *_gj(kernel[shift])] for shift in sorted(kernel)]
        ),
        "kernel_zero": _gj(kernel[0]),
        "kernel_non_even_witness": [_gj(kernel[-1]), _gj(kernel[1])],
        "literal_beta_sha256": _digest([str(entry) for entry in beta]),
        "literal_beta_nonzero_count": sum(entry != 0 for entry in beta),
        "a_star_h_sha256": _digest([_gj(entry) for entry in direct]),
        "formula_sha256": _digest([_gj(entry) for entry in predicted]),
        "p_lane_sha256": _digest([_gj(entry) for entry in p_rows]),
        "e_lane_sha256": _digest([_gj(entry) for entry in e_rows]),
        "j_lane_sha256": _digest([_gj(entry) for entry in j_rows]),
        "diagonal_lane_sha256": _digest([_gj(entry) for entry in diagonal_rows]),
        "coordinate_identities": len(coordinates),
        "child_jump_checks": child_checks,
        "input_masked_q_rows": input_masked_rows,
        "output_masked_terms_seen": output_masked_terms,
        "lhs_inner_h_a_beta": _gj(lhs),
        "rhs_inner_astar_h_beta": _gj(rhs),
        "scalar_parts": scalar_parts,
        "scalar_sum": _gj(scalar_sum),
        "h_beta": str(h_beta),
        "input_unit_correction": str(input_correction),
        "diagonal_bq_reassembly": str(diagonal_bq),
        "fixture_scope": (
            "NONLITERAL_NON_EVEN_GAUSSIAN_RATIONAL_KERNEL_SUBSTITUTED_INTO_"
            "THE_LITERAL_OPERATOR_SHAPE_FOR_FINITE_ALGEBRA_ONLY"
        ),
    }


def _source_contract() -> dict[str, Any]:
    h_value = Fraction(16)
    q_value = Fraction(7)
    psi_zero = Fraction(7, 5)
    zero_mode = h_value * psi_zero / (q_value * (q_value - 1))
    x = Fraction(27, 5)
    coordinates, ell, right_size, h, rho_squared = _rank(x)
    naive_left = [entry for entry in coordinates if entry <= _floor(3 * x / 4)]
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
            "residue_class_main_term": str(h_value * psi_zero / q_value),
            "kernel_zero": "1",
            "normalizations_are_distinct": True,
        },
        "noninteger_rank": {
            "x": str(x),
            "coordinates": coordinates,
            "ell": ell,
            "right_size": right_size,
            "rank_left": coordinates[:ell],
            "naive_three_quarter_left": naive_left,
            "mismatch_detected": coordinates[:ell] != naive_left,
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


def build_certificate() -> dict[str, Any]:
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "maximum_claim": MAXIMUM_CLAIM,
        "baseline_head": BASELINE_HEAD,
        "handoff_sha256": HANDOFF_SHA256,
        "source_digests": SOURCE_DIGESTS,
        "firewall": FIREWALL,
        "source_contract": _source_contract(),
        "fixture": _coordinate_fixture(),
        "mutation_classes": MUTATION_CLASSES,
        "mutation_required_minimum": 64,
        "stress_required_families": 192,
        "executable_scope": (
            "FINITE_EXACT_ALGEBRA_AND_SOURCE_CONTRACT_TYPING_ONLY_NOT_"
            "ASYMPTOTIC_EVIDENCE"
        ),
    }
    return {"payload": payload, "payload_sha256": _digest(payload)}


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _source_bytes(path: str) -> bytes:
    repository = _repository_root()
    bridge = "research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md"
    if path == bridge:
        return (repository / path).read_bytes().replace(b"\r\n", b"\n")
    completed = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + path],
        cwd=repository,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0 or completed.stderr:
        raise SystemExit("TPC255_CERTIFICATE=FAIL source lock unavailable: " + path)
    return completed.stdout.replace(b"\r\n", b"\n")


def _verify_sources() -> None:
    for path, expected in SOURCE_DIGESTS.items():
        observed = hashlib.sha256(_source_bytes(path)).hexdigest()
        if observed != expected:
            raise SystemExit("TPC255_CERTIFICATE=FAIL source hash mismatch: " + path)


def _certificate_path() -> Path:
    return Path(__file__).resolve().parents[1] / "results" / "tpc255_certificate.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    _verify_sources()
    expected = _document(build_certificate())
    if _certificate_path().read_bytes() != expected:
        raise SystemExit("TPC255_CERTIFICATE=FAIL released certificate mismatch")
    fixture = build_certificate()["payload"]["fixture"]
    print(
        "TPC255_CERTIFICATE=PASS coordinate_identities="
        + str(fixture["coordinate_identities"])
        + " child_jump_checks=" + str(fixture["child_jump_checks"])
        + " exact_arithmetic=YES asymptotic_evidence=NO"
    )


if __name__ == "__main__":
    main()
