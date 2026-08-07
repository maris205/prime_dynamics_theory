#!/usr/bin/env python3
"""Read-only exact checker for the V21 wrapped-covariance normal form.

The checker verifies the finite algebra, the local residue profiles, the
normalization ledger and literal V19 finite witnesses used by V21.  It locks
the V20 dependency but does not claim to prove Bombieri--Vinogradov, the
Rosser--Iwaniec fundamental lemma, the centered covariance estimate or TPC.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from fractions import Fraction
from pathlib import Path
from typing import Iterable


class CheckFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


V20_PATH = Path("research/tpc-big-road/tpc_bridge_b_terminal_innovation_checker.py")
V20_CANONICAL_SHA256 = (
    "ce62b12023a4d65a8eb7ff2e01db50110d7d96183c5db771e11728da10ce50a7"
)
V19_PATH = Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py")
V19_CANONICAL_SHA256 = (
    "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
)


CONTRACT = {
    "route_version": "V21",
    "physical_h0": 2,
    "analytic_physical_binding": "x=2X",
    "residual": "Lambda(t+2)-b_x^((log x)^K)(t)",
    "raw_row": "V19_COMBINED_MASTER_COVECTOR",
    "mesoscopic_modulus": "Q_mes=x^(1/3)_DISTINCT_FROM_PACKET_Q",
    "prime_ensemble": "ALL_PRIMES_Q_mes_LT_q_LE_2Q_mes_EQUAL_WEIGHT",
    "fiber_normalization": "ACTUAL_n_(q,a)",
    "outer_absolute_value": "ONCE_AFTER_COMPLETE_ENSEMBLE",
    "low_frequency_mean": "PROVED_SOURCE_BACKED_AP_COMPILER",
    "centered_covariance": "OPEN_NEW_ARITHMETIC_THEOREM",
    "automatic_centering_saving": False,
    "automatic_fixed_low_rank": False,
    "mean_only_deletion_carrier": False,
    "good_modulus_selection": False,
    "arithmetic_subgate_advance": "YES_F12_ONLY",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}


REGISTRY_ITEMS = (
    ("V20_TERMINAL_INNOVATION_DEPENDENCY", "LOCKED_CANONICAL_FINAL_LF_SHA256"),
    ("V19_RAW_EMITTER_TRANSITIVE_DEPENDENCY", "LOCKED_BY_V20_AND_RECHECKED"),
    ("PHYSICAL_H0", "2"),
    ("ANALYTIC_PHYSICAL_BINDING", "x=2X"),
    ("PHYSICAL_RESIDUAL", "Lambda(t+2)-b_x^((log x)^K)(t)"),
    ("PHYSICAL_RAW_ROW", "V19_COMBINED_MASTER_COVECTOR"),
    ("MESOSCOPIC_Q", "x^(1/3)_DISTINCT_FROM_PACKET_Q"),
    ("PRIME_MODULUS_ENSEMBLE", "COMPLETE_PREDECLARED_EQUAL_WEIGHT"),
    ("GOOD_MODULUS_SELECTION", "FORBIDDEN_AND_UNUSED"),
    ("WRAPPED_FIBER_COUNTS", "ACTUAL_FLOOR_OR_CEILING"),
    ("WRAPPED_MEAN_CENTERED_SPLIT", "PROVED_EXACT"),
    ("WRAPPED_PAIR_DIFFERENCE_FORM", "PROVED_EXACT"),
    ("ALGEBRAIC_COORDINATE_NORMALIZATION", "NO_HAAR_OR_RIESZ_SCALAR"),
    ("LAMBDA_LOCAL_PROFILE", "PROVED_EXACT_WITH_MINUS_TWO_POWER_EXCEPTION"),
    ("HYBRID_LOCAL_PROFILE", "PROVED_EXACT_FOR_q_GT_z"),
    ("RESIDUAL_LOCAL_PROFILE", "PROVED_EXACT_THREE_RESIDUE_TYPES"),
    ("RESIDUAL_PROFILE_TOTAL_MASS", "ZERO"),
    ("DETERMINISTIC_PROFILE_CLOSED_FORM", "PROVED_EXACT"),
    ("DETERMINISTIC_PROFILE_ENSEMBLE", "O(x^(2/3)log^4x)"),
    ("BETA_LITERAL_POINTWISE", "ABS_LE_3d4"),
    ("BETA_L1_LEDGER", "O(x_log^3x)"),
    ("BETA_L2_SQUARED_LEDGER", "O(x_log^15x)"),
    ("LAMBDA_AP_REMAINDER", "PROVED_SOURCE_BACKED_MAXIMAL_BV"),
    ("HYBRID_AP_REMAINDER", "PROVED_SOURCE_BACKED_DERIVED_SIEVE_COROLLARY"),
    ("FULL_RESIDUAL_AP_REMAINDER", "PROVED_BY_LITERAL_LINEAR_SUBTRACTION"),
    ("WRAPPED_LOW_FREQUENCY_MEAN", "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER"),
    ("F12_WEIGHTED_MEAN_SQUARE_IMPLICATION", "PROVED_EXACT_SUFFICIENT_NORM"),
    ("CENTERED_PAIR_KERNEL", "q_DIVIDES_t_MINUS_u"),
    ("CENTERED_PROJECTION_RANK", "H_MINUS_q_WHEN_H_GE_q"),
    ("CENTERED_PHYSICAL_COVARIANCE", "OPEN_NEW_ARITHMETIC_THEOREM"),
    ("CENTERED_PRIMARY_SOURCE_ATTACHMENT", "STOP_SCOPED_NO_SURVIVOR_IN_SIX_CHECKED_FAMILIES"),
    ("AUTOMATIC_CENTERING_ENERGY_SAVING", "STOP_SCOPED_PROJECTION_NORM_ONE"),
    ("AUTOMATIC_CENTERED_FIXED_LOW_RANK", "STOP_SCOPED_RANK_H_MINUS_q"),
    ("MEAN_ONLY_DELETION_CARRIER", "STOP_SCOPED_EXACT_NONCOMMUTATION"),
    ("V21_PRIME_ENSEMBLE_X1000", "11_13_17_19"),
    ("V21_PRIME_ENSEMBLE_X1000_R", "4"),
    ("V21_LITERAL_BETA_X166_RAW_ENERGY", "64177/1764"),
    ("V21_LITERAL_BETA_X166_M30_CENTERED_RATIO", "16340/192531"),
    ("V21_LITERAL_BETA_X166_M35_CENTERED_RATIO", "3544/6639"),
    ("V21_COVARIANCE_SATURATION", "-1/2"),
    ("V21_MEAN_SATURATION", "6"),
    ("V21_DELETION_NONCOMMUTATION", "-1/3"),
    ("ARITHMETIC_SUBGATE_ADVANCE", "YES_F12_ONLY"),
    ("ARITHMETIC_ADVANCE", "NO"),
    ("FIXED_ATOM_CREDIT", "0"),
    ("STRICT_1_OVER_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", "false"),
)

REGISTRY_SHA256 = "757ca58fabffda4d2ac5d3b3ce3103f0b0474d47f5ff0f104eee4c9996c00e74"


def canonical_contract() -> dict[str, object]:
    return {
        "route_version": "V21",
        "physical_h0": 2,
        "analytic_physical_binding": "x=2X",
        "residual": "Lambda(t+2)-b_x^((log x)^K)(t)",
        "raw_row": "V19_COMBINED_MASTER_COVECTOR",
        "mesoscopic_modulus": "Q_mes=x^(1/3)_DISTINCT_FROM_PACKET_Q",
        "prime_ensemble": "ALL_PRIMES_Q_mes_LT_q_LE_2Q_mes_EQUAL_WEIGHT",
        "fiber_normalization": "ACTUAL_n_(q,a)",
        "outer_absolute_value": "ONCE_AFTER_COMPLETE_ENSEMBLE",
        "low_frequency_mean": "PROVED_SOURCE_BACKED_AP_COMPILER",
        "centered_covariance": "OPEN_NEW_ARITHMETIC_THEOREM",
        "automatic_centering_saving": False,
        "automatic_fixed_low_rank": False,
        "mean_only_deletion_carrier": False,
        "good_modulus_selection": False,
        "arithmetic_subgate_advance": "YES_F12_ONLY",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def canonical_registry_items() -> tuple[tuple[str, str], ...]:
    return (
        ("V20_TERMINAL_INNOVATION_DEPENDENCY", "LOCKED_CANONICAL_FINAL_LF_SHA256"),
        ("V19_RAW_EMITTER_TRANSITIVE_DEPENDENCY", "LOCKED_BY_V20_AND_RECHECKED"),
        ("PHYSICAL_H0", "2"),
        ("ANALYTIC_PHYSICAL_BINDING", "x=2X"),
        ("PHYSICAL_RESIDUAL", "Lambda(t+2)-b_x^((log x)^K)(t)"),
        ("PHYSICAL_RAW_ROW", "V19_COMBINED_MASTER_COVECTOR"),
        ("MESOSCOPIC_Q", "x^(1/3)_DISTINCT_FROM_PACKET_Q"),
        ("PRIME_MODULUS_ENSEMBLE", "COMPLETE_PREDECLARED_EQUAL_WEIGHT"),
        ("GOOD_MODULUS_SELECTION", "FORBIDDEN_AND_UNUSED"),
        ("WRAPPED_FIBER_COUNTS", "ACTUAL_FLOOR_OR_CEILING"),
        ("WRAPPED_MEAN_CENTERED_SPLIT", "PROVED_EXACT"),
        ("WRAPPED_PAIR_DIFFERENCE_FORM", "PROVED_EXACT"),
        ("ALGEBRAIC_COORDINATE_NORMALIZATION", "NO_HAAR_OR_RIESZ_SCALAR"),
        ("LAMBDA_LOCAL_PROFILE", "PROVED_EXACT_WITH_MINUS_TWO_POWER_EXCEPTION"),
        ("HYBRID_LOCAL_PROFILE", "PROVED_EXACT_FOR_q_GT_z"),
        ("RESIDUAL_LOCAL_PROFILE", "PROVED_EXACT_THREE_RESIDUE_TYPES"),
        ("RESIDUAL_PROFILE_TOTAL_MASS", "ZERO"),
        ("DETERMINISTIC_PROFILE_CLOSED_FORM", "PROVED_EXACT"),
        ("DETERMINISTIC_PROFILE_ENSEMBLE", "O(x^(2/3)log^4x)"),
        ("BETA_LITERAL_POINTWISE", "ABS_LE_3d4"),
        ("BETA_L1_LEDGER", "O(x_log^3x)"),
        ("BETA_L2_SQUARED_LEDGER", "O(x_log^15x)"),
        ("LAMBDA_AP_REMAINDER", "PROVED_SOURCE_BACKED_MAXIMAL_BV"),
        ("HYBRID_AP_REMAINDER", "PROVED_SOURCE_BACKED_DERIVED_SIEVE_COROLLARY"),
        ("FULL_RESIDUAL_AP_REMAINDER", "PROVED_BY_LITERAL_LINEAR_SUBTRACTION"),
        ("WRAPPED_LOW_FREQUENCY_MEAN", "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER"),
        ("F12_WEIGHTED_MEAN_SQUARE_IMPLICATION", "PROVED_EXACT_SUFFICIENT_NORM"),
        ("CENTERED_PAIR_KERNEL", "q_DIVIDES_t_MINUS_u"),
        ("CENTERED_PROJECTION_RANK", "H_MINUS_q_WHEN_H_GE_q"),
        ("CENTERED_PHYSICAL_COVARIANCE", "OPEN_NEW_ARITHMETIC_THEOREM"),
        ("CENTERED_PRIMARY_SOURCE_ATTACHMENT", "STOP_SCOPED_NO_SURVIVOR_IN_SIX_CHECKED_FAMILIES"),
        ("AUTOMATIC_CENTERING_ENERGY_SAVING", "STOP_SCOPED_PROJECTION_NORM_ONE"),
        ("AUTOMATIC_CENTERED_FIXED_LOW_RANK", "STOP_SCOPED_RANK_H_MINUS_q"),
        ("MEAN_ONLY_DELETION_CARRIER", "STOP_SCOPED_EXACT_NONCOMMUTATION"),
        ("V21_PRIME_ENSEMBLE_X1000", "11_13_17_19"),
        ("V21_PRIME_ENSEMBLE_X1000_R", "4"),
        ("V21_LITERAL_BETA_X166_RAW_ENERGY", "64177/1764"),
        ("V21_LITERAL_BETA_X166_M30_CENTERED_RATIO", "16340/192531"),
        ("V21_LITERAL_BETA_X166_M35_CENTERED_RATIO", "3544/6639"),
        ("V21_COVARIANCE_SATURATION", "-1/2"),
        ("V21_MEAN_SATURATION", "6"),
        ("V21_DELETION_NONCOMMUTATION", "-1/3"),
        ("ARITHMETIC_SUBGATE_ADVANCE", "YES_F12_ONLY"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "false"),
    )


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def canonical_lf_bytes(data: bytes) -> bytes:
    normalized = data.replace(b"\r\n", b"\n")
    require(b"\r" not in normalized, "dependency contains a bare carriage return")
    return normalized


def validate_exact_mapping(candidate: object, expected: dict[str, object], label: str) -> None:
    require(type(candidate) is dict, f"{label} must be an exact dict")
    require(set(candidate) == set(expected), f"{label} exact key set changed")
    for key, locked in expected.items():
        actual = candidate[key]
        require(type(actual) is type(locked), f"{label} field {key} has wrong type")
        require(actual == locked, f"{label} field {key} changed")


def validate_contract(candidate: object) -> None:
    locked = {
        "route_version": "V21",
        "physical_h0": 2,
        "analytic_physical_binding": "x=2X",
        "residual": "Lambda(t+2)-b_x^((log x)^K)(t)",
        "raw_row": "V19_COMBINED_MASTER_COVECTOR",
        "mesoscopic_modulus": "Q_mes=x^(1/3)_DISTINCT_FROM_PACKET_Q",
        "prime_ensemble": "ALL_PRIMES_Q_mes_LT_q_LE_2Q_mes_EQUAL_WEIGHT",
        "fiber_normalization": "ACTUAL_n_(q,a)",
        "outer_absolute_value": "ONCE_AFTER_COMPLETE_ENSEMBLE",
        "low_frequency_mean": "PROVED_SOURCE_BACKED_AP_COMPILER",
        "centered_covariance": "OPEN_NEW_ARITHMETIC_THEOREM",
        "automatic_centering_saving": False,
        "automatic_fixed_low_rank": False,
        "mean_only_deletion_carrier": False,
        "good_modulus_selection": False,
        "arithmetic_subgate_advance": "YES_F12_ONLY",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    validate_exact_mapping(candidate, locked, "contract")


def validate_registry(candidate: object, digest: object) -> None:
    locked = canonical_registry_items()
    hard_digest = "757ca58fabffda4d2ac5d3b3ce3103f0b0474d47f5ff0f104eee4c9996c00e74"
    require(type(candidate) is tuple, "registry must be an exact tuple")
    require(candidate == locked, "registry semantic content changed")
    require(len(candidate) == 48, "registry row count changed")
    require(len({key for key, _ in candidate}) == 48, "registry keys are not unique")
    require(type(digest) is str, "registry digest has wrong type")
    require(digest == hard_digest, "registry digest binding changed")
    require(registry_hash(candidate) == hard_digest, "registry final-LF hash changed")


def load_dependencies() -> tuple[dict[str, object], dict[str, object]]:
    v20_path = Path("research/tpc-big-road/tpc_bridge_b_terminal_innovation_checker.py")
    v20_sha = "ce62b12023a4d65a8eb7ff2e01db50110d7d96183c5db771e11728da10ce50a7"
    v19_path = Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py")
    v19_sha = "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
    require(V20_PATH == v20_path, "V20 dependency path changed")
    require(V20_CANONICAL_SHA256 == v20_sha, "V20 dependency digest constant changed")
    require(V19_PATH == v19_path, "V19 dependency path changed")
    require(V19_CANONICAL_SHA256 == v19_sha, "V19 dependency digest constant changed")
    require(v20_path.is_file() and v19_path.is_file(), "dependency is absent")
    require(
        hashlib.sha256(canonical_lf_bytes(v20_path.read_bytes())).hexdigest() == v20_sha,
        "V20 dependency canonical hash mismatch",
    )
    require(
        hashlib.sha256(canonical_lf_bytes(v19_path.read_bytes())).hexdigest() == v19_sha,
        "V19 dependency canonical hash mismatch",
    )
    v20 = runpy.run_path(str(v20_path))
    v20_result = v20["run_check"]()
    require(type(v20_result) is dict and v20_result.get("check") is True, "V20 failed")
    require(v20_result.get("TPC_207_TRIGGER") is False, "V20 promoted TPC-207")
    require(v20_result.get("arithmetic_advance") is False, "V20 promoted arithmetic")
    v19 = runpy.run_path(str(v19_path))
    return v20, v19


def shell_integers(analytic_x: int) -> tuple[int, ...]:
    require(type(analytic_x) is int and analytic_x >= 2, "analytic x is invalid")
    return tuple(range(analytic_x // 2 + 1, analytic_x + 1))


def fibers(analytic_x: int, modulus: int) -> tuple[tuple[int, ...], ...]:
    require(type(modulus) is int and modulus >= 2, "modulus is invalid")
    shell = shell_integers(analytic_x)
    return tuple(tuple(t for t in shell if t % modulus == a) for a in range(modulus))


def dot(left: dict[int, Fraction], right: dict[int, Fraction]) -> Fraction:
    require(set(left) == set(right), "dot-product domains differ")
    return sum((left[t] * right[t] for t in left), Fraction(0))


def wrapped_split(
    analytic_x: int,
    modulus: int,
    beta: dict[int, Fraction],
    residual: dict[int, Fraction],
) -> dict[str, Fraction]:
    shell = shell_integers(analytic_x)
    require(set(beta) == set(shell), "beta shell changed")
    require(set(residual) == set(shell), "residual shell changed")
    scalar = dot(beta, residual)
    mean = Fraction(0)
    centered = Fraction(0)
    pair = Fraction(0)
    for fiber in fibers(analytic_x, modulus):
        if not fiber:
            continue
        count = len(fiber)
        beta_sum = sum((beta[t] for t in fiber), Fraction(0))
        residual_sum = sum((residual[t] for t in fiber), Fraction(0))
        residual_mean = residual_sum / count
        mean += beta_sum * residual_mean
        centered += sum(
            (beta[t] * (residual[t] - residual_mean) for t in fiber),
            Fraction(0),
        )
        pair += sum(
            (
                (beta[t] - beta[u]) * (residual[t] - residual[u])
                for t in fiber
                for u in fiber
            ),
            Fraction(0),
        ) / (2 * count)
    require(scalar == mean + centered, "wrapped mean-centered split failed")
    require(centered == pair, "wrapped pair-difference identity failed")
    return {"scalar": scalar, "mean": mean, "centered": centered, "pair": pair}


def validate_wrapped_algebra() -> dict[str, int]:
    cases = 0
    edge_cases = 0
    for analytic_x in (24, 25, 31, 64, 100, 166):
        shell = shell_integers(analytic_x)
        for modulus in (3, 5, 7, 11, 30, 35):
            beta = {
                t: Fraction(((7 * t + analytic_x) % 13) - 6, (t % 3) + 1)
                for t in shell
            }
            residual = {
                t: Fraction(((5 * t + modulus) % 17) - 8, (t % 4) + 1)
                for t in shell
            }
            wrapped_split(analytic_x, modulus, beta, residual)
            counts = tuple(len(fiber) for fiber in fibers(analytic_x, modulus))
            require(max(counts) - min(counts) <= 1, "ragged fiber gap exceeded one")
            require(sum(counts) == len(shell), "fiber cover is not exactly once")
            if max(counts) != min(counts):
                edge_cases += 1
            cases += 1
    return {"identity_cases": cases, "ragged_edge_cases": edge_cases}


def lambda_profile(prime: int, residue: int) -> Fraction:
    return Fraction(0) if residue % prime == (-2) % prime else Fraction(prime, prime - 1)


def hybrid_profile(prime: int, residue: int) -> Fraction:
    if residue % prime == 0:
        return Fraction(prime, prime - 1)
    return Fraction(prime * (prime - 2), (prime - 1) ** 2)


def residual_profile(prime: int, residue: int) -> Fraction:
    return lambda_profile(prime, residue) - hybrid_profile(prime, residue)


def validate_local_profiles() -> dict[str, int]:
    cases = 0
    for prime in (5, 7, 11, 13, 101, 211):
        values = tuple(residual_profile(prime, residue) for residue in range(prime))
        require(values[0] == 0, "zero-residue profile changed")
        require(
            values[(-2) % prime] == Fraction(-prime * (prime - 2), (prime - 1) ** 2),
            "minus-two profile changed",
        )
        require(sum(values, Fraction(0)) == 0, "residual profile lost mean zero")
        expected_l1 = Fraction(2 * prime * (prime - 2), (prime - 1) ** 2)
        expected_l2 = Fraction(prime * prime * (prime - 2), (prime - 1) ** 3)
        require(sum((abs(value) for value in values), Fraction(0)) == expected_l1, "profile l1 changed")
        require(sum((value * value for value in values), Fraction(0)) == expected_l2, "profile l2 changed")
        cases += prime
    return {"residue_cases": cases, "prime_cases": 6}


def validate_deterministic_profile() -> dict[str, int]:
    cases = 0
    for prime in (5, 7, 11, 13):
        fiber_sums = {
            residue: Fraction(((residue + 3) * (prime + 2)) % 19 - 9, (residue % 3) + 1)
            for residue in range(prime)
        }
        direct = sum(
            (fiber_sums[a] * residual_profile(prime, a) for a in range(prime)),
            Fraction(0),
        )
        total = sum(fiber_sums.values(), Fraction(0))
        closed = (
            Fraction(prime, (prime - 1) ** 2) * (total - fiber_sums[0])
            - Fraction(prime, prime - 1) * fiber_sums[(-2) % prime]
        )
        require(direct == closed, "deterministic profile closed form failed")
        cases += 1
    return {"closed_form_cases": cases}


def literal_beta_fraction(v19: dict[str, object], integer: int, analytic_x: int) -> Fraction:
    numerator_items = v19["raw_master_numerator"](integer, analytic_x)[0]
    if not numerator_items:
        return Fraction(0)
    numerator = dict(numerator_items)
    factorization = dict(v19["factorization"](integer))
    require(set(numerator) <= set(factorization), "raw numerator has an extraneous prime")
    ratios = {
        Fraction(numerator.get(prime, 0), exponent)
        for prime, exponent in factorization.items()
    }
    require(len(ratios) == 1, "literal beta is not rational on the locked fixture")
    return ratios.pop()


def centered_energy(vector: dict[int, Fraction], analytic_x: int, modulus: int) -> Fraction:
    energy = Fraction(0)
    for fiber in fibers(analytic_x, modulus):
        if not fiber:
            continue
        mean = sum((vector[t] for t in fiber), Fraction(0)) / len(fiber)
        energy += sum(((vector[t] - mean) ** 2 for t in fiber), Fraction(0))
    return energy


def validate_literal_beta_fixtures(v19: dict[str, object]) -> dict[str, object]:
    analytic_x = 166
    shell = shell_integers(analytic_x)
    beta = {t: literal_beta_fraction(v19, t, analytic_x) for t in shell}
    expected_points = {84: 1, 90: 2, 91: -1, 114: 1, 120: 2, 121: Fraction(-1, 2), 150: 2}
    for integer, expected in expected_points.items():
        require(beta[integer] == expected, f"literal beta point {integer} changed")
    raw_energy = sum((value * value for value in beta.values()), Fraction(0))
    centered_30 = centered_energy(beta, analytic_x, 30)
    centered_35 = centered_energy(beta, analytic_x, 35)
    require(raw_energy == Fraction(64177, 1764), "literal beta raw energy changed")
    require(centered_30 / raw_energy == Fraction(16340, 192531), "M30 ratio changed")
    require(centered_35 / raw_energy == Fraction(3544, 6639), "M35 ratio changed")

    covariance_residual = {t: Fraction(0) for t in shell}
    covariance_residual[91] = 1
    covariance_residual[121] = -1
    covariance = wrapped_split(analytic_x, 30, beta, covariance_residual)
    require(covariance["scalar"] == Fraction(-1, 2), "covariance witness scalar changed")
    require(covariance["mean"] == 0, "covariance witness leaked into mean")
    require(covariance["centered"] == Fraction(-1, 2), "covariance witness changed")

    mean_residual = {t: Fraction(0) for t in shell}
    for integer in (90, 120, 150):
        mean_residual[integer] = 1
    mean_witness = wrapped_split(analytic_x, 30, beta, mean_residual)
    require(mean_witness["scalar"] == 6, "mean witness scalar changed")
    require(mean_witness["mean"] == 6, "mean witness did not saturate")
    require(mean_witness["centered"] == 0, "mean witness leaked into covariance")

    return {
        "analytic_x": analytic_x,
        "support": sum(value != 0 for value in beta.values()),
        "raw_energy": str(raw_energy),
        "M30_centered_ratio": str(centered_30 / raw_energy),
        "M35_centered_ratio": str(centered_35 / raw_energy),
        "covariance_saturation": str(covariance["centered"]),
        "mean_saturation": str(mean_witness["mean"]),
    }


def pair_mask(integer: int, prime: int) -> int:
    return int(integer % prime != 0 and (integer + 2) % prime != 0)


def conditional_mean(vector: dict[int, Fraction], analytic_x: int, modulus: int) -> dict[int, Fraction]:
    output = {t: Fraction(0) for t in shell_integers(analytic_x)}
    for fiber in fibers(analytic_x, modulus):
        if not fiber:
            continue
        mean = sum((vector[t] for t in fiber), Fraction(0)) / len(fiber)
        for t in fiber:
            output[t] = mean
    return output


def validate_projection_firewalls() -> dict[str, object]:
    analytic_x = 166
    shell = shell_integers(analytic_x)
    vector = {t: Fraction(0) for t in shell}
    vector[91] = 1
    vector[121] = -1
    projected = conditional_mean(vector, analytic_x, 30)
    centered = {t: vector[t] - projected[t] for t in shell}
    require(projected == {t: Fraction(0) for t in shell}, "mean-zero norm-one witness failed")
    require(dot(centered, centered) == dot(vector, vector), "centered projection contracted norm-one witness")

    deletion_input = {t: Fraction(0) for t in shell}
    deletion_input[84] = 1
    deletion_input[114] = -1
    require(
        conditional_mean(deletion_input, analytic_x, 30) == {t: Fraction(0) for t in shell},
        "deletion witness did not start in the centered kernel",
    )
    deleted = {t: Fraction(pair_mask(t, 7)) * deletion_input[t] for t in shell}
    deleted_mean = conditional_mean(deleted, analytic_x, 30)
    require(deleted_mean[84] == Fraction(-1, 3), "deletion noncommutation value changed")
    require(any(value != 0 for value in deleted_mean.values()), "deletion unexpectedly commuted")
    return {"projection_norm_ratio": "1", "deletion_mean_at_84": str(deleted_mean[84])}


def exact_matrix_rank(rows: list[list[Fraction]]) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    columns = len(matrix[0])
    require(all(len(row) == columns for row in matrix), "rank matrix is ragged")
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - factor * matrix[pivot_row][index]
                for index in range(columns)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def validate_centered_projection_rank() -> dict[str, int]:
    cases = 0
    largest_rank = 0
    for analytic_x, modulus in ((24, 3), (24, 5), (31, 7), (64, 11), (166, 30), (166, 35)):
        shell = shell_integers(analytic_x)
        dimension = len(shell)
        require(dimension >= modulus, "rank fixture has empty residue fibers")
        rows: list[list[Fraction]] = []
        for output in shell:
            row: list[Fraction] = []
            output_fiber = next(fiber for fiber in fibers(analytic_x, modulus) if output in fiber)
            for source in shell:
                entry = Fraction(int(output == source))
                if source in output_fiber:
                    entry -= Fraction(1, len(output_fiber))
                row.append(entry)
            rows.append(row)
        rank = exact_matrix_rank(rows)
        require(rank == dimension - modulus, "centered projection rank formula changed")
        largest_rank = max(largest_rank, rank)
        cases += 1
    return {"rank_cases": cases, "largest_fixture_rank": largest_rank}


def is_prime(integer: int) -> bool:
    if integer < 2:
        return False
    divisor = 2
    while divisor * divisor <= integer:
        if integer % divisor == 0:
            return False
        divisor += 1
    return True


def validate_complete_prime_ensemble(v19: dict[str, object]) -> dict[str, object]:
    analytic_x = 1000
    q_mes = 10
    ensemble = tuple(q for q in range(q_mes + 1, 2 * q_mes + 1) if is_prime(q))
    require(ensemble == (11, 13, 17, 19), "complete prime ensemble changed")
    shell = shell_integers(analytic_x)
    beta = {t: literal_beta_fraction(v19, t, analytic_x) for t in shell}
    residual = {
        t: Fraction(((13 * t + 5) % 29) - 14, (t % 6) + 1)
        for t in shell
    }
    scalar = dot(beta, residual)
    mean_average = Fraction(0)
    centered_average = Fraction(0)
    for modulus in ensemble:
        split = wrapped_split(analytic_x, modulus, beta, residual)
        require(split["scalar"] == scalar, "ensemble member changed the physical scalar")
        mean_average += split["mean"]
        centered_average += split["centered"]
    mean_average /= len(ensemble)
    centered_average /= len(ensemble)
    require(scalar == mean_average + centered_average, "1/R ensemble normalization failed")
    return {
        "analytic_x": analytic_x,
        "Q_mes": q_mes,
        "primes": ensemble,
        "R": len(ensemble),
        "one_over_R_identity": True,
    }


def validate_f12_normalization() -> dict[str, object]:
    analytic_x = 1000
    modulus = 13
    shell = shell_integers(analytic_x)
    beta = {t: Fraction(((11 * t + 7) % 23) - 11, (t % 5) + 1) for t in shell}
    error_by_residue = {a: Fraction(((7 * a + 1) % 17) - 8, (a % 4) + 1) for a in range(modulus)}
    beta_energy = dot(beta, beta)
    beta_projection_energy = Fraction(0)
    error_norm = Fraction(0)
    pairing = Fraction(0)
    for a, fiber in enumerate(fibers(analytic_x, modulus)):
        require(bool(fiber), "normalization fixture has an empty fiber")
        count = len(fiber)
        beta_sum = sum((beta[t] for t in fiber), Fraction(0))
        beta_projection_energy += beta_sum * beta_sum / count
        error_norm += error_by_residue[a] * error_by_residue[a] / count
        pairing += beta_sum * error_by_residue[a] / count
    require(beta_projection_energy <= beta_energy, "conditional expectation increased beta energy")
    require(pairing * pairing <= beta_projection_energy * error_norm, "weighted Cauchy failed")
    counts = tuple(len(fiber) for fiber in fibers(analytic_x, modulus))
    require(set(counts) == {38, 39}, "edge normalization counts changed")
    return {
        "fiber_min": min(counts),
        "fiber_max": max(counts),
        "beta_projection_contracts": True,
        "weighted_cauchy": True,
        "required_log_loss": "B>=2A+17_USING_BETA_L2_LOG15",
    }


def validate_exponent_ledger() -> dict[str, str]:
    theta = Fraction(1, 3)
    sieve_delta = Fraction(1, 6)
    deterministic = 1 - theta
    lattice = theta + sieve_delta
    require(deterministic == Fraction(2, 3), "deterministic exponent changed")
    require(lattice == Fraction(1, 2), "sieve lattice exponent changed")
    require(deterministic < 1 and lattice < 1, "power-scale error reached the main scale")
    require(4 * theta > 1, "four-prime incidence argument lost power separation")
    return {
        "Q_mes_exponent": str(theta),
        "Rosser_level_D_exponent": str(sieve_delta),
        "deterministic_error_exponent": str(deterministic),
        "lattice_error_exponent": str(lattice),
    }


def mutation_value(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_MUTATED"
    raise CheckFailure("unhandled contract mutation type")


def run_mutations() -> dict[str, int]:
    contract_rejected = 0
    base_contract = canonical_contract()
    for key in base_contract:
        candidate = dict(base_contract)
        candidate[key] = mutation_value(candidate[key])
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_rejected += 1
        else:
            raise CheckFailure(f"contract mutation escaped at {key}")
    for label, candidate in (
        ("missing", {key: value for key, value in base_contract.items() if key != "physical_h0"}),
        ("extra", {**base_contract, "UNKNOWN_FIELD": True}),
        ("wrong_type", {**base_contract, "TPC_207_TRIGGER": 0}),
        (
            "coordinated_release",
            {
                **base_contract,
                "centered_covariance": "PROVED_FALSE_PROMOTION",
                "arithmetic_advance": "YES",
                "strict_1_over_400": "PAID",
                "TPC_207_TRIGGER": True,
            },
        ),
    ):
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_rejected += 1
        else:
            raise CheckFailure(f"{label} contract mutation escaped")

    registry_rejected = 0
    locked = canonical_registry_items()
    hard_digest = "757ca58fabffda4d2ac5d3b3ce3103f0b0474d47f5ff0f104eee4c9996c00e74"
    for index, (key, value) in enumerate(locked):
        candidate = list(locked)
        candidate[index] = (key, value + "_MUTATED")
        candidate_tuple = tuple(candidate)
        try:
            validate_registry(candidate_tuple, registry_hash(candidate_tuple))
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"registry value mutation escaped at {key}")
    for index, (key, value) in enumerate(locked):
        candidate = list(locked)
        candidate[index] = (key + "_REPLACED", value)
        candidate_tuple = tuple(candidate)
        try:
            validate_registry(candidate_tuple, registry_hash(candidate_tuple))
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"registry key mutation escaped at {key}")
    for label, candidate, digest in (
        ("missing", locked[:-1], registry_hash(locked[:-1])),
        ("extra", locked + (("UNKNOWN", "ROW"),), registry_hash(locked + (("UNKNOWN", "ROW"),))),
        ("duplicate", locked[:-1] + (locked[0],), registry_hash(locked[:-1] + (locked[0],))),
        ("wrong_type", list(locked), hard_digest),
        ("wrong_digest", locked, "0" * 64),
    ):
        try:
            validate_registry(candidate, digest)
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"{label} registry mutation escaped")
    return {
        "contract_mutations_rejected": contract_rejected,
        "registry_mutations_rejected": registry_rejected,
    }


def validate_registry_semantics(
    registry: tuple[tuple[str, str], ...],
    contract: dict[str, object],
    fixture: dict[str, object],
    centered_rank: dict[str, int],
    prime_ensemble: dict[str, object],
) -> None:
    validate_contract(contract)
    semantic_locks = {
        "V20_TERMINAL_INNOVATION_DEPENDENCY": "LOCKED_CANONICAL_FINAL_LF_SHA256",
        "V19_RAW_EMITTER_TRANSITIVE_DEPENDENCY": "LOCKED_BY_V20_AND_RECHECKED",
        "PHYSICAL_H0": "2",
        "ANALYTIC_PHYSICAL_BINDING": "x=2X",
        "PHYSICAL_RESIDUAL": "Lambda(t+2)-b_x^((log x)^K)(t)",
        "PHYSICAL_RAW_ROW": "V19_COMBINED_MASTER_COVECTOR",
        "MESOSCOPIC_Q": "x^(1/3)_DISTINCT_FROM_PACKET_Q",
        "PRIME_MODULUS_ENSEMBLE": "COMPLETE_PREDECLARED_EQUAL_WEIGHT",
        "GOOD_MODULUS_SELECTION": "FORBIDDEN_AND_UNUSED",
        "WRAPPED_FIBER_COUNTS": "ACTUAL_FLOOR_OR_CEILING",
        "WRAPPED_MEAN_CENTERED_SPLIT": "PROVED_EXACT",
        "WRAPPED_PAIR_DIFFERENCE_FORM": "PROVED_EXACT",
        "ALGEBRAIC_COORDINATE_NORMALIZATION": "NO_HAAR_OR_RIESZ_SCALAR",
        "LAMBDA_LOCAL_PROFILE": "PROVED_EXACT_WITH_MINUS_TWO_POWER_EXCEPTION",
        "HYBRID_LOCAL_PROFILE": "PROVED_EXACT_FOR_q_GT_z",
        "RESIDUAL_LOCAL_PROFILE": "PROVED_EXACT_THREE_RESIDUE_TYPES",
        "RESIDUAL_PROFILE_TOTAL_MASS": "ZERO",
        "DETERMINISTIC_PROFILE_CLOSED_FORM": "PROVED_EXACT",
        "DETERMINISTIC_PROFILE_ENSEMBLE": "O(x^(2/3)log^4x)",
        "BETA_LITERAL_POINTWISE": "ABS_LE_3d4",
        "BETA_L1_LEDGER": "O(x_log^3x)",
        "BETA_L2_SQUARED_LEDGER": "O(x_log^15x)",
        "LAMBDA_AP_REMAINDER": "PROVED_SOURCE_BACKED_MAXIMAL_BV",
        "HYBRID_AP_REMAINDER": "PROVED_SOURCE_BACKED_DERIVED_SIEVE_COROLLARY",
        "FULL_RESIDUAL_AP_REMAINDER": "PROVED_BY_LITERAL_LINEAR_SUBTRACTION",
        "WRAPPED_LOW_FREQUENCY_MEAN": "PROVED_SOURCE_BACKED_ARBITRARY_LOG_POWER",
        "F12_WEIGHTED_MEAN_SQUARE_IMPLICATION": "PROVED_EXACT_SUFFICIENT_NORM",
        "CENTERED_PAIR_KERNEL": "q_DIVIDES_t_MINUS_u",
        "CENTERED_PROJECTION_RANK": "H_MINUS_q_WHEN_H_GE_q",
        "CENTERED_PHYSICAL_COVARIANCE": "OPEN_NEW_ARITHMETIC_THEOREM",
        "CENTERED_PRIMARY_SOURCE_ATTACHMENT": "STOP_SCOPED_NO_SURVIVOR_IN_SIX_CHECKED_FAMILIES",
        "AUTOMATIC_CENTERING_ENERGY_SAVING": "STOP_SCOPED_PROJECTION_NORM_ONE",
        "AUTOMATIC_CENTERED_FIXED_LOW_RANK": "STOP_SCOPED_RANK_H_MINUS_q",
        "MEAN_ONLY_DELETION_CARRIER": "STOP_SCOPED_EXACT_NONCOMMUTATION",
        "V21_PRIME_ENSEMBLE_X1000": "11_13_17_19",
        "V21_PRIME_ENSEMBLE_X1000_R": "4",
        "V21_LITERAL_BETA_X166_RAW_ENERGY": "64177/1764",
        "V21_LITERAL_BETA_X166_M30_CENTERED_RATIO": "16340/192531",
        "V21_LITERAL_BETA_X166_M35_CENTERED_RATIO": "3544/6639",
        "V21_COVARIANCE_SATURATION": "-1/2",
        "V21_MEAN_SATURATION": "6",
        "V21_DELETION_NONCOMMUTATION": "-1/3",
        "ARITHMETIC_SUBGATE_ADVANCE": "YES_F12_ONLY",
        "ARITHMETIC_ADVANCE": "NO",
        "FIXED_ATOM_CREDIT": "0",
        "STRICT_1_OVER_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": "false",
    }
    require(type(registry) is tuple, "semantic registry must be an exact tuple")
    rows = dict(registry)
    require(len(rows) == len(registry) == 48, "semantic registry keys are not exact")
    require(rows == semantic_locks, "registry semantic promotion")
    require(rows["V21_LITERAL_BETA_X166_RAW_ENERGY"] == fixture["raw_energy"], "raw energy registry mismatch")
    require(rows["V21_LITERAL_BETA_X166_M30_CENTERED_RATIO"] == fixture["M30_centered_ratio"], "M30 registry mismatch")
    require(rows["V21_LITERAL_BETA_X166_M35_CENTERED_RATIO"] == fixture["M35_centered_ratio"], "M35 registry mismatch")
    require(rows["V21_COVARIANCE_SATURATION"] == fixture["covariance_saturation"], "covariance registry mismatch")
    require(rows["V21_MEAN_SATURATION"] == fixture["mean_saturation"], "mean registry mismatch")
    require(rows["CENTERED_PROJECTION_RANK"] == "H_MINUS_q_WHEN_H_GE_q", "rank registry mismatch")
    require(centered_rank["largest_fixture_rank"] == 53, "rank fixture summary changed")
    require("_".join(str(q) for q in prime_ensemble["primes"]) == rows["V21_PRIME_ENSEMBLE_X1000"], "ensemble registry mismatch")
    require(str(prime_ensemble["R"]) == rows["V21_PRIME_ENSEMBLE_X1000_R"], "ensemble R registry mismatch")
    require(rows["ARITHMETIC_ADVANCE"] == "NO", "registry promoted arithmetic")
    require(rows["TPC_207_TRIGGER"] == "false", "registry promoted TPC-207")
    require(str(contract["physical_h0"]) == rows["PHYSICAL_H0"], "contract/registry h0 mismatch")
    require(contract["analytic_physical_binding"] == rows["ANALYTIC_PHYSICAL_BINDING"], "contract/registry binding mismatch")
    require(contract["residual"] == rows["PHYSICAL_RESIDUAL"], "contract/registry residual mismatch")
    require(contract["raw_row"] == rows["PHYSICAL_RAW_ROW"], "contract/registry raw-row mismatch")
    require(contract["mesoscopic_modulus"].startswith("Q_mes=x^(1/3)"), "contract/registry Q mismatch")
    require(contract["good_modulus_selection"] is False, "contract selected good moduli")
    require(contract["centered_covariance"] == rows["CENTERED_PHYSICAL_COVARIANCE"], "contract/registry centered mismatch")
    require(contract["automatic_centering_saving"] is False, "contract promoted automatic centering")
    require(contract["automatic_fixed_low_rank"] is False, "contract promoted fixed low rank")
    require(contract["mean_only_deletion_carrier"] is False, "contract promoted mean-only carrier")
    require(contract["arithmetic_subgate_advance"] == rows["ARITHMETIC_SUBGATE_ADVANCE"], "contract/registry subgate mismatch")
    require(contract["arithmetic_advance"] == rows["ARITHMETIC_ADVANCE"], "contract/registry arithmetic mismatch")
    require(str(contract["fixed_atom_credit"]) == rows["FIXED_ATOM_CREDIT"], "contract/registry fixed-atom mismatch")
    require(contract["strict_1_over_400"] == rows["STRICT_1_OVER_400"], "contract/registry strict mismatch")
    require(contract["L2"] == rows["L2"], "contract/registry L2 mismatch")
    require(str(contract["TPC_207_TRIGGER"]).lower() == rows["TPC_207_TRIGGER"], "contract/registry TPC-207 mismatch")


def run_check() -> dict[str, object]:
    validate_contract(CONTRACT)
    validate_registry(REGISTRY_ITEMS, REGISTRY_SHA256)
    _, v19 = load_dependencies()
    algebra = validate_wrapped_algebra()
    profiles = validate_local_profiles()
    deterministic = validate_deterministic_profile()
    fixture = validate_literal_beta_fixtures(v19)
    firewalls = validate_projection_firewalls()
    centered_rank = validate_centered_projection_rank()
    prime_ensemble = validate_complete_prime_ensemble(v19)
    normalization = validate_f12_normalization()
    exponents = validate_exponent_ledger()
    validate_registry_semantics(REGISTRY_ITEMS, CONTRACT, fixture, centered_rank, prime_ensemble)
    mutations = run_mutations()
    locked_contract = {
        "route_version": "V21",
        "low_frequency_mean": "PROVED_SOURCE_BACKED_AP_COMPILER",
        "centered_covariance": "OPEN_NEW_ARITHMETIC_THEOREM",
        "arithmetic_subgate_advance": "YES_F12_ONLY",
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }
    locked_registry = REGISTRY_ITEMS
    locked_registry_payload = "".join(f"{key}={value}\n" for key, value in locked_registry)
    locked_registry_digest = hashlib.sha256(locked_registry_payload.encode("utf-8")).hexdigest()
    result = {
        "check": True,
        "route_version": locked_contract["route_version"],
        "dependencies": {
            "V20_canonical_sha256": "ce62b12023a4d65a8eb7ff2e01db50110d7d96183c5db771e11728da10ce50a7",
            "V19_canonical_sha256": "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519",
        },
        "algebra": algebra,
        "profiles": profiles,
        "deterministic": deterministic,
        "literal_fixture": fixture,
        "firewalls": firewalls,
        "centered_rank": centered_rank,
        "prime_ensemble": prime_ensemble,
        "normalization": normalization,
        "exponents": exponents,
        "registry": {"rows": len(locked_registry), "sha256": locked_registry_digest},
        "mutations": mutations,
        "claim_ceiling": "EXACT_L0_WRAPPED_NORMAL_FORM_AND_SOURCE_BACKED_MEAN_COMPILER",
        "low_frequency_mean": locked_contract["low_frequency_mean"],
        "centered_covariance": locked_contract["centered_covariance"],
        "arithmetic_subgate_advance": locked_contract["arithmetic_subgate_advance"],
        "arithmetic_advance": False,
        "fixed_atom_credit": locked_contract["fixed_atom_credit"],
        "strict_1_over_400": locked_contract["strict_1_over_400"],
        "L2": locked_contract["L2"],
        "TPC_207_TRIGGER": locked_contract["TPC_207_TRIGGER"],
    }
    require(result["TPC_207_TRIGGER"] is False, "result promoted TPC-207")
    require(result["arithmetic_advance"] is False, "result promoted arithmetic")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the read-only exact audit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    require(args.check, "the checker requires the explicit --check flag")
    print(json.dumps(run_check(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
