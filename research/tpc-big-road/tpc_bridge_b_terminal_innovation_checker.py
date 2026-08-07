#!/usr/bin/env python3
"""Read-only exact checker for the V20 terminal-innovation bypass stop.

The checker proves finite linear algebra, exact no-wrap identities and the
V19 k=5,b=7 component-rank fixture.  It does not prove a signed SHB-D2
estimate, an all-horizon quotient theorem, a Logistic return or TPC.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import runpy
from fractions import Fraction
from pathlib import Path
from typing import Iterable


class CheckFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


V19_PATH = Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py")
V19_CANONICAL_SHA256 = (
    "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
)
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23)

CONTRACT = {
    "route_version": "V20",
    "physical_h0": 2,
    "analytic_physical_binding": "x=2X",
    "residual": "Lambda(t+2)-b_x^((log x)^K)(t)",
    "raw_row": "V19_COMBINED_MASTER_COVECTOR",
    "terminal_no_wrap": True,
    "terminal_innovation_small_error": False,
    "automatic_stage_cancellation": False,
    "path_state_dimension_reduction": False,
    "combined_raw_signed_saving": "OPEN_NEW_ARITHMETIC_THEOREM",
    "separated_template_registry": "ABSENT",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}

REGISTRY_ITEMS = (
    ("V19_RAW_EMITTER_DEPENDENCY", "LOCKED_CANONICAL_FINAL_LF_SHA256"),
    ("PHYSICAL_H0", "2"),
    ("ANALYTIC_PHYSICAL_BINDING", "x=2X"),
    ("FIBER_ORTHOGONAL_PROJECTION", "PROVED_EXACT"),
    ("FIBER_SOURCE_INNOVATION_FORMULA", "PROVED_EXACT"),
    ("FIBER_PHYSICAL_EVALUATION_FORMULA", "PROVED_EXACT"),
    ("TERMINAL_NO_WRAP_CLOCK", "PROVED_FOR_SUFFICIENTLY_LARGE_STAGE"),
    ("TERMINAL_INNOVATION_NORM_IDENTITY", "PROVED_EXACT"),
    ("TERMINAL_INNOVATION_NORM_FLOOR", "RATIO_(p-3)/(p-2)"),
    ("TERMINAL_INNOVATION_SUPPORT", "EXPANDS_ON_SURVIVORS"),
    ("TERMINAL_RAW_EVALUATION_IDENTITY", "PROVED_EXACT"),
    ("TERMINAL_RAW_EVALUATION_ERROR", "O_K(x^(1/2+o(1)))"),
    ("TERMINAL_RAW_SAVING_EQUIVALENCE", "PROVED_AT_LOG_POWER_TARGET"),
    ("GROWING_HORIZON_WEIGHTS", "NONNEGATIVE_PARTITION_OF_ONE"),
    ("GROWING_HORIZON_AUTOMATIC_CANCELLATION", "STOP_SCOPED_FALSE"),
    ("TERMINAL_WEIGHT_DOMINANCE", "PROVED_EXACT"),
    ("AFFINE_PATH_DECOMPOSITION", "PROVED_EXACT_ORTHOGONAL"),
    ("AFFINE_PATH_SYNTHESIS", "EXACT_WEIGHTED_ISOMETRY"),
    ("AFFINE_PATH_DIMENSION", "FULL_TERMINAL_DIMENSION"),
    ("CHANGING_SCALE_RAW_PULLBACK_CHAIN", "STOP_SCOPED_EXACT_166_168_WITNESS"),
    ("WHOLE_INNOVATION_QUOTIENT", "STOP_SCOPED_ACTUAL_ROW_VALUE_20_OVER_11"),
    ("V20_RAW_SOURCE_ROWS", "120"),
    ("V20_RAW_SOURCE_COORDINATES", "110"),
    ("V20_RAW_COORDINATE_PARTITIONS", "3984"),
    ("V20_RAW_SOURCE_RANK", "65"),
    ("V20_BASE_COMPONENT_RANK", "56"),
    ("V20_TERMINAL_ETA_RANK", "50"),
    ("V20_ALL_ETA_RANK", "54"),
    ("V20_ETA_BASE_UNION_RANK", "76"),
    ("INNOVATION_AUTOMATIC_SMOOTHING_BYPASS", "STOP_SCOPED_TERMINAL_NEAR_IDENTITY"),
    ("DIRECT_SIGNED_TERMINAL_INNOVATION_THEOREM", "OPEN_NEW_ARITHMETIC_THEOREM"),
    ("SEPARATED_SHB_D2_TEMPLATE_REGISTRY", "ABSENT"),
    ("ARITHMETIC_ADVANCE", "NO"),
    ("FIXED_ATOM_CREDIT", "0"),
    ("STRICT_1_OVER_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", "false"),
)

REGISTRY_SHA256 = "0408cb3e4fd0bbfb7815df0df24902d4cc9fa1b75875e66f41482c30768652ee"


def canonical_contract() -> dict[str, object]:
    return {
        "route_version": "V20",
        "physical_h0": 2,
        "analytic_physical_binding": "x=2X",
        "residual": "Lambda(t+2)-b_x^((log x)^K)(t)",
        "raw_row": "V19_COMBINED_MASTER_COVECTOR",
        "terminal_no_wrap": True,
        "terminal_innovation_small_error": False,
        "automatic_stage_cancellation": False,
        "path_state_dimension_reduction": False,
        "combined_raw_signed_saving": "OPEN_NEW_ARITHMETIC_THEOREM",
        "separated_template_registry": "ABSENT",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def canonical_registry_items() -> tuple[tuple[str, str], ...]:
    return (
        ("V19_RAW_EMITTER_DEPENDENCY", "LOCKED_CANONICAL_FINAL_LF_SHA256"),
        ("PHYSICAL_H0", "2"),
        ("ANALYTIC_PHYSICAL_BINDING", "x=2X"),
        ("FIBER_ORTHOGONAL_PROJECTION", "PROVED_EXACT"),
        ("FIBER_SOURCE_INNOVATION_FORMULA", "PROVED_EXACT"),
        ("FIBER_PHYSICAL_EVALUATION_FORMULA", "PROVED_EXACT"),
        ("TERMINAL_NO_WRAP_CLOCK", "PROVED_FOR_SUFFICIENTLY_LARGE_STAGE"),
        ("TERMINAL_INNOVATION_NORM_IDENTITY", "PROVED_EXACT"),
        ("TERMINAL_INNOVATION_NORM_FLOOR", "RATIO_(p-3)/(p-2)"),
        ("TERMINAL_INNOVATION_SUPPORT", "EXPANDS_ON_SURVIVORS"),
        ("TERMINAL_RAW_EVALUATION_IDENTITY", "PROVED_EXACT"),
        ("TERMINAL_RAW_EVALUATION_ERROR", "O_K(x^(1/2+o(1)))"),
        ("TERMINAL_RAW_SAVING_EQUIVALENCE", "PROVED_AT_LOG_POWER_TARGET"),
        ("GROWING_HORIZON_WEIGHTS", "NONNEGATIVE_PARTITION_OF_ONE"),
        ("GROWING_HORIZON_AUTOMATIC_CANCELLATION", "STOP_SCOPED_FALSE"),
        ("TERMINAL_WEIGHT_DOMINANCE", "PROVED_EXACT"),
        ("AFFINE_PATH_DECOMPOSITION", "PROVED_EXACT_ORTHOGONAL"),
        ("AFFINE_PATH_SYNTHESIS", "EXACT_WEIGHTED_ISOMETRY"),
        ("AFFINE_PATH_DIMENSION", "FULL_TERMINAL_DIMENSION"),
        ("CHANGING_SCALE_RAW_PULLBACK_CHAIN", "STOP_SCOPED_EXACT_166_168_WITNESS"),
        ("WHOLE_INNOVATION_QUOTIENT", "STOP_SCOPED_ACTUAL_ROW_VALUE_20_OVER_11"),
        ("V20_RAW_SOURCE_ROWS", "120"),
        ("V20_RAW_SOURCE_COORDINATES", "110"),
        ("V20_RAW_COORDINATE_PARTITIONS", "3984"),
        ("V20_RAW_SOURCE_RANK", "65"),
        ("V20_BASE_COMPONENT_RANK", "56"),
        ("V20_TERMINAL_ETA_RANK", "50"),
        ("V20_ALL_ETA_RANK", "54"),
        ("V20_ETA_BASE_UNION_RANK", "76"),
        ("INNOVATION_AUTOMATIC_SMOOTHING_BYPASS", "STOP_SCOPED_TERMINAL_NEAR_IDENTITY"),
        ("DIRECT_SIGNED_TERMINAL_INNOVATION_THEOREM", "OPEN_NEW_ARITHMETIC_THEOREM"),
        ("SEPARATED_SHB_D2_TEMPLATE_REGISTRY", "ABSENT"),
        ("ARITHMETIC_ADVANCE", "NO"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "false"),
    )


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_exact_mapping(candidate: object, expected: dict[str, object], label: str) -> None:
    require(type(candidate) is dict, f"{label} must be an exact dict")
    require(set(candidate) == set(expected), f"{label} exact key set changed")
    for key, locked in expected.items():
        actual = candidate[key]
        require(type(actual) is type(locked), f"{label} field {key} has wrong type")
        require(actual == locked, f"{label} field {key} changed")


def validate_contract(candidate: object) -> None:
    validate_exact_mapping(candidate, canonical_contract(), "contract")


def validate_registry(candidate: object, digest: object) -> None:
    locked = canonical_registry_items()
    require(type(candidate) is tuple, "registry must be an exact tuple")
    require(candidate == locked, "registry semantic content changed")
    require(len(candidate) == 37, "registry row count changed")
    require(len({key for key, _ in candidate}) == 37, "registry keys are not unique")
    hard_digest = "0408cb3e4fd0bbfb7815df0df24902d4cc9fa1b75875e66f41482c30768652ee"
    require(type(digest) is str, "registry digest has wrong type")
    require(digest == hard_digest, "registry digest binding changed")
    require(registry_hash(candidate) == hard_digest, "registry final-LF hash changed")


def canonical_lf_bytes(data: bytes) -> bytes:
    normalized = data.replace(b"\r\n", b"\n")
    require(b"\r" not in normalized, "dependency contains a bare carriage return")
    return normalized


def load_v19() -> dict[str, object]:
    locked_path = Path("research/tpc-big-road/tpc_bridge_b_shbd2_innovation_checker.py")
    locked_sha = "e572bd9157ce4e733dc411ed8eb29df90d34be0ecf17023186f1648389ded519"
    require(V19_PATH == locked_path, "V19 dependency path changed")
    require(V19_CANONICAL_SHA256 == locked_sha, "V19 dependency digest constant changed")
    require(locked_path.is_file(), "V19 dependency is absent")
    digest = hashlib.sha256(canonical_lf_bytes(locked_path.read_bytes())).hexdigest()
    require(digest == locked_sha, "V19 dependency canonical hash mismatch")
    namespace = runpy.run_path(str(locked_path))
    result = namespace["run_check"]()
    require(type(result) is dict and result.get("check") is True, "V19 dependency failed")
    require(result.get("TPC_207_TRIGGER") is False, "V19 dependency promoted TPC-207")
    require(result.get("arithmetic_advance") is False, "V19 dependency promoted arithmetic")
    return namespace


def pair_mask(integer: int, prime: int) -> int:
    return int(integer % prime != 0 and (integer + 2) % prime != 0)


def replication(parent: tuple[Fraction, ...], modulus: int, prime: int) -> tuple[Fraction, ...]:
    require(math.gcd(modulus, prime) == 1, "replication requires a new prime")
    child = [Fraction(0) for _ in range(modulus * prime)]
    for residue, value in enumerate(parent):
        for copy in range(prime):
            integer = residue + copy * modulus
            if pair_mask(integer, prime):
                child[integer] = value
    return tuple(child)


def adjoint(child: tuple[Fraction, ...], modulus: int, prime: int) -> tuple[Fraction, ...]:
    require(len(child) == modulus * prime, "adjoint arity changed")
    return tuple(
        sum(
            child[residue + copy * modulus]
            for copy in range(prime)
            if pair_mask(residue + copy * modulus, prime)
        )
        / prime
        for residue in range(modulus)
    )


def projection(child: tuple[Fraction, ...], modulus: int, prime: int) -> tuple[Fraction, ...]:
    alpha = Fraction(prime - 2, prime)
    parent = tuple(value / alpha for value in adjoint(child, modulus, prime))
    return replication(parent, modulus, prime)


def dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    require(len(left) == len(right), "dot arity changed")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def normalized_norm_squared(vector: tuple[Fraction, ...]) -> Fraction:
    return dot(vector, vector) / len(vector)


def validate_fiber_formulas() -> dict[str, int]:
    cases = 0
    for modulus, prime in ((6, 5), (30, 7), (210, 11)):
        child = tuple(
            Fraction(((index * 17 + 5) % 23) - 11, (index % 3) + 1)
            for index in range(modulus * prime)
        )
        beta = tuple(Fraction(((index * 11 + 4) % 19) - 9) for index in range(modulus * prime))
        projected = projection(child, modulus, prime)
        eta = tuple(value - mean for value, mean in zip(child, projected))
        require(adjoint(eta, modulus, prime) == (Fraction(0),) * modulus, "eta left ker R*")
        require(projection(projected, modulus, prime) == projected, "projection is not idempotent")
        formula = Fraction(0)
        for residue in range(modulus):
            survivors = [
                residue + copy * modulus
                for copy in range(prime)
                if pair_mask(residue + copy * modulus, prime)
            ]
            deleted = [
                residue + copy * modulus
                for copy in range(prime)
                if not pair_mask(residue + copy * modulus, prime)
            ]
            require(len(survivors) == prime - 2 and len(deleted) == 2, "fiber sizes changed")
            vbar = sum((child[index] for index in survivors), Fraction(0)) / (prime - 2)
            bbar = sum((beta[index] for index in survivors), Fraction(0)) / (prime - 2)
            for index in deleted:
                require(eta[index] == child[index], "deleted innovation value changed")
                formula += beta[index] * child[index]
            for index in survivors:
                require(eta[index] == child[index] - vbar, "survivor innovation value changed")
                formula += (beta[index] - bbar) * (child[index] - vbar)
        require(dot(beta, eta) == formula, "physical innovation evaluation formula failed")
        cases += 1
    return {"fiber_cases": cases}


def validate_no_wrap_terminal() -> dict[str, object]:
    modulus = 2310
    prime = 13
    analytic_x = 168
    require(modulus > analytic_x, "terminal fixture wrapped")
    child = [Fraction(0) for _ in range(modulus * prime)]
    beta = [Fraction(0) for _ in range(modulus * prime)]
    for integer in range(analytic_x // 2 + 1, analytic_x + 1):
        child[integer] = Fraction(((integer * 7) % 17) - 8, (integer % 5) + 1)
        beta[integer] = Fraction(((integer * 5) % 13) - 6)
    child_tuple = tuple(child)
    beta_tuple = tuple(beta)
    projected = projection(child_tuple, modulus, prime)
    eta = tuple(value - mean for value, mean in zip(child_tuple, projected))
    deleted_energy = Fraction(0)
    survivor_energy = Fraction(0)
    deleted_active = 0
    survivor_active = 0
    survivor_eval = Fraction(0)
    absolute_eval = Fraction(0)
    for integer in range(analytic_x // 2 + 1, analytic_x + 1):
        value = child_tuple[integer]
        if value == 0:
            continue
        absolute_eval += abs(beta_tuple[integer] * value)
        if pair_mask(integer, prime):
            survivor_active += 1
            survivor_energy += value * value
            survivor_eval += beta_tuple[integer] * value
        else:
            deleted_active += 1
            deleted_energy += value * value
    eta_energy_sum = dot(eta, eta)
    locked_energy_sum = deleted_energy + Fraction(prime - 3, prime - 2) * survivor_energy
    require(eta_energy_sum == locked_energy_sum, "terminal norm identity failed")
    require(
        eta_energy_sum >= Fraction(prime - 3, prime - 2) * dot(child_tuple, child_tuple),
        "terminal norm floor failed",
    )
    expected_support = deleted_active + (prime - 2) * survivor_active
    require(sum(value != 0 for value in eta) == expected_support, "terminal support formula failed")
    original_eval = dot(beta_tuple, child_tuple)
    eta_eval = dot(beta_tuple, eta)
    require(
        eta_eval == original_eval - survivor_eval / (prime - 2),
        "terminal raw evaluation identity failed",
    )
    require(abs(original_eval - eta_eval) * (prime - 2) <= absolute_eval, "evaluation bound failed")
    return {
        "parent_modulus": modulus,
        "prime": prime,
        "analytic_x": analytic_x,
        "floor": f"{prime - 3}/{prime - 2}",
        "deleted_active": deleted_active,
        "survivor_active": survivor_active,
        "eta_support": expected_support,
    }


def validate_horizon_partition() -> dict[str, int]:
    horizon = (13, 17, 19, 23)
    cases = 0
    for integer in range(1, 300):
        later = Fraction(1)
        eta_weights: list[Fraction] = []
        for prime in reversed(horizon):
            q_value = Fraction(pair_mask(integer, prime), prime - 2)
            eta_weights.append(later * (1 - q_value))
            if prime == horizon[-1]:
                require(
                    eta_weights[-1] >= Fraction(prime - 3, prime - 2),
                    "terminal weight lost dominance",
                )
            later *= q_value
        base_weight = later
        require(base_weight + sum(eta_weights, Fraction(0)) == 1, "horizon partition failed")
        require(base_weight >= 0 and all(weight >= 0 for weight in eta_weights), "negative weight appeared")
        terminal_q = Fraction(pair_mask(integer, horizon[-1]), horizon[-1] - 2)
        require(base_weight + sum(eta_weights[1:], Fraction(0)) == terminal_q, "terminal remainder changed")
        cases += 1
    return {"horizon_primes": len(horizon), "coordinate_cases": cases}


def validate_path_isometry() -> dict[str, object]:
    base_modulus = 6
    p1 = 5
    p2 = 7
    middle_modulus = base_modulus * p1
    terminal_modulus = middle_modulus * p2
    terminal = tuple(Fraction(((index * 13 + 7) % 29) - 14) for index in range(terminal_modulus))
    pi2 = projection(terminal, middle_modulus, p2)
    eta2 = tuple(value - mean for value, mean in zip(terminal, pi2))
    middle = tuple(value / Fraction(p2 - 2, p2) for value in adjoint(terminal, middle_modulus, p2))
    pi1 = projection(middle, base_modulus, p1)
    eta1 = tuple(value - mean for value, mean in zip(middle, pi1))
    base = tuple(value / Fraction(p1 - 2, p1) for value in adjoint(middle, base_modulus, p1))
    term0 = replication(replication(base, base_modulus, p1), middle_modulus, p2)
    term1 = replication(eta1, middle_modulus, p2)
    reconstructed = tuple(a + b + c for a, b, c in zip(term0, term1, eta2))
    require(reconstructed == terminal, "path synthesis failed")
    require(dot(term0, term1) == dot(term0, eta2) == dot(term1, eta2) == 0, "path terms not orthogonal")
    alpha1 = Fraction(p1 - 2, p1)
    alpha2 = Fraction(p2 - 2, p2)
    weighted = (
        alpha2 * alpha1 * normalized_norm_squared(base)
        + alpha2 * normalized_norm_squared(eta1)
        + normalized_norm_squared(eta2)
    )
    require(weighted == normalized_norm_squared(terminal), "weighted path norm failed")
    dimension = base_modulus + (middle_modulus - base_modulus) + (terminal_modulus - middle_modulus)
    require(dimension == terminal_modulus, "path dimension telescoping failed")
    return {"terminal_dimension": terminal_modulus, "path_dimension": dimension}


def exact_rank(v19: dict[str, object], rows: Iterable[dict[int, Fraction]], columns: dict[int, int]) -> int:
    encoded = ({columns[key]: value for key, value in row.items() if value} for row in rows)
    return v19["exact_fraction_rank"](encoded)


def validate_raw_rank_and_witnesses(v19: dict[str, object]) -> dict[str, object]:
    base_stage = v19["BASE_STAGE"]
    terminal_stage = v19["TERMINAL_STAGE"]
    directions: dict[int, tuple[tuple[int, int], ...]] = {}
    source_rows: list[tuple[int, int, dict[int, Fraction]]] = []
    partition_count = 0
    for stage in range(base_stage, terminal_stage + 1):
        for physical_x in v19["stage_band"](stage):
            analytic_x = 2 * physical_x
            row: dict[int, Fraction] = {}
            for integer in range(physical_x + 1, analytic_x + 1):
                numerator_items, _, _ = v19["raw_master_numerator"](integer, analytic_x)
                numerator = dict(numerator_items)
                if not numerator:
                    continue
                direction, _ = v19["primitive_direction"](numerator)
                if integer in directions:
                    require(directions[integer] == direction, "raw source column direction changed")
                else:
                    directions[integer] = direction
                row[integer] = Fraction(v19["vector_scalar"](numerator, direction))
            require(bool(row), "raw source row is empty")
            partition_count += len(row)
            source_rows.append((stage, physical_x, row))
    column_index = {integer: index for index, integer in enumerate(sorted(directions))}
    raw_rank = exact_rank(v19, (row for _, _, row in source_rows), column_index)
    base_rows: list[dict[int, Fraction]] = []
    terminal_eta_rows: list[dict[int, Fraction]] = []
    all_eta_rows: list[dict[int, Fraction]] = []
    component_rows: list[dict[int, Fraction]] = []
    for stage, _, row in source_rows:
        current = {integer: Fraction(1) for integer in row}
        eta_weights: list[dict[int, Fraction]] = []
        for source_stage in range(stage, base_stage, -1):
            prime = PRIMES[source_stage - 1]
            eta_weight: dict[int, Fraction] = {}
            next_weight: dict[int, Fraction] = {}
            for integer, later in current.items():
                q_value = Fraction(pair_mask(integer, prime), prime - 2)
                eta_weight[integer] = later * (1 - q_value)
                next_weight[integer] = later * q_value
            eta_weights.append(eta_weight)
            current = next_weight
        if eta_weights:
            terminal_eta_rows.append(
                {integer: row[integer] * value for integer, value in eta_weights[0].items() if row[integer] * value}
            )
        for weights in eta_weights:
            component = {
                integer: row[integer] * value
                for integer, value in weights.items()
                if row[integer] * value
            }
            all_eta_rows.append(component)
            component_rows.append(component)
        base_component = {
            integer: row[integer] * value
            for integer, value in current.items()
            if row[integer] * value
        }
        base_rows.append(base_component)
        component_rows.append(base_component)
    ranks = {
        "raw_source": raw_rank,
        "base": exact_rank(v19, base_rows, column_index),
        "terminal_eta": exact_rank(v19, terminal_eta_rows, column_index),
        "all_eta": exact_rank(v19, all_eta_rows, column_index),
        "eta_base_union": exact_rank(v19, component_rows, column_index),
    }
    require(len(source_rows) == 120, "raw source row count changed")
    require(len(column_index) == 110, "raw source coordinate count changed")
    require(partition_count == 3984, "raw coordinate partition count changed")
    require(ranks == {"raw_source": 65, "base": 56, "terminal_eta": 50, "all_eta": 54, "eta_base_union": 76}, "component ranks changed")
    require(len(terminal_eta_rows) == 96 and len(all_eta_rows) == 132 and len(component_rows) == 252, "component row counts changed")

    numerator_84 = dict(v19["raw_master_numerator"](84, 166)[0])
    require(numerator_84 == {2: 2, 3: 1, 7: 1}, "x=166,t=84 witness changed")
    require(pair_mask(84, 13) == 1, "t=84 stopped surviving p=13")
    require(not (168 // 2 < 84 <= 168), "strict-shell witness changed")
    numerator_90 = dict(v19["raw_master_numerator"](90, 168)[0])
    require(numerator_90 == {2: 2, 3: 4, 5: 2}, "x=168,t=90 numerator changed")
    require(pair_mask(90, 13) == 1, "t=90 stopped surviving p=13")
    require(Fraction(2) * Fraction(10, 11) == Fraction(20, 11), "innovation sensitivity changed")
    return {
        "rows": len(source_rows),
        "coordinates": len(column_index),
        "partitions": partition_count,
        "terminal_eta_rows": len(terminal_eta_rows),
        "all_eta_rows": len(all_eta_rows),
        "component_rows": len(component_rows),
        "ranks": ranks,
        "changing_scale_witness": "x166_t84_vs_x168_strict_shell",
        "innovation_sensitivity": "20/11",
    }


def mutation_value(value: object) -> object:
    if type(value) is bool:
        return 1 if value is False else 0
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_FALSE_PROMOTION"
    raise CheckFailure("unhandled contract mutation type")


def run_mutations() -> dict[str, int]:
    base = canonical_contract()
    contract_rejected = 0
    for key in base:
        candidate = dict(base)
        candidate[key] = mutation_value(candidate[key])
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_rejected += 1
        else:
            raise CheckFailure(f"contract mutation escaped at {key}")
    missing = dict(base)
    missing.pop("physical_h0")
    extra = dict(base)
    extra["unknown"] = "value"
    coordinated = dict(base)
    coordinated.update(
        {
            "terminal_innovation_small_error": True,
            "automatic_stage_cancellation": True,
            "path_state_dimension_reduction": True,
            "combined_raw_signed_saving": "PROVED_FALSE_PROMOTION",
            "arithmetic_advance": "YES",
            "fixed_atom_credit": 1,
            "strict_1_over_400": "PAID_FALSE_PROMOTION",
            "L2": "FULL_FALSE_PROMOTION",
            "TPC_207_TRIGGER": True,
        }
    )
    for label, candidate in (("missing", missing), ("extra", extra), ("coordinated", coordinated)):
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_rejected += 1
        else:
            raise CheckFailure(f"{label} contract mutation escaped")

    registry = canonical_registry_items()
    registry_rejected = 0
    for index, (key, value) in enumerate(registry):
        candidate = list(registry)
        candidate[index] = (key, value + "_FALSE_PROMOTION")
        rebound = tuple(candidate)
        try:
            validate_registry(rebound, registry_hash(rebound))
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"registry mutation escaped at {key}")
    replacement = list(registry)
    replacement[-1] = ("UNKNOWN_REPLACEMENT_ROW", "false")
    false_release = list(registry)
    false_release[-5:] = [
        ("ARITHMETIC_ADVANCE", "YES"),
        ("FIXED_ATOM_CREDIT", "1"),
        ("STRICT_1_OVER_400", "PAID"),
        ("L2", "FULL"),
        ("TPC_207_TRIGGER", "true"),
    ]
    for label, candidate in (("replacement", tuple(replacement)), ("false release", tuple(false_release))):
        try:
            validate_registry(candidate, registry_hash(candidate))
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"registry {label} with rehash escaped")
    return {
        "contract_mutations_rejected": contract_rejected,
        "registry_mutations_rejected": registry_rejected,
    }


def validate_registry_semantics(registry: tuple[tuple[str, str], ...], fixture: dict[str, object]) -> None:
    values = dict(registry)
    require(values["V20_RAW_SOURCE_ROWS"] == str(fixture["rows"]), "registry/raw rows mismatch")
    require(values["V20_RAW_SOURCE_COORDINATES"] == str(fixture["coordinates"]), "registry/coordinates mismatch")
    require(values["V20_RAW_COORDINATE_PARTITIONS"] == str(fixture["partitions"]), "registry/partitions mismatch")
    rank_keys = {
        "V20_RAW_SOURCE_RANK": "raw_source",
        "V20_BASE_COMPONENT_RANK": "base",
        "V20_TERMINAL_ETA_RANK": "terminal_eta",
        "V20_ALL_ETA_RANK": "all_eta",
        "V20_ETA_BASE_UNION_RANK": "eta_base_union",
    }
    for registry_key, fixture_key in rank_keys.items():
        require(values[registry_key] == str(fixture["ranks"][fixture_key]), f"registry/rank mismatch: {registry_key}")
    require(values["ARITHMETIC_ADVANCE"] == "NO", "registry promoted arithmetic")
    require(values["TPC_207_TRIGGER"] == "false", "registry promoted TPC-207")


def run_check() -> dict[str, object]:
    require(PRIMES == (2, 3, 5, 7, 11, 13, 17, 19, 23), "prime clock changed")
    validate_contract(CONTRACT)
    validate_registry(REGISTRY_ITEMS, REGISTRY_SHA256)
    v19 = load_v19()
    fiber = validate_fiber_formulas()
    terminal = validate_no_wrap_terminal()
    horizon = validate_horizon_partition()
    path = validate_path_isometry()
    fixture = validate_raw_rank_and_witnesses(v19)
    validate_registry_semantics(REGISTRY_ITEMS, fixture)
    mutations = run_mutations()
    registry = dict(REGISTRY_ITEMS)
    result = {
        "check": True,
        "route_version": CONTRACT["route_version"],
        "dependency": {"path": str(V19_PATH).replace("\\", "/"), "canonical_sha256": V19_CANONICAL_SHA256},
        "fiber": fiber,
        "terminal_no_wrap": terminal,
        "horizon": horizon,
        "path_state": path,
        "raw_fixture": fixture,
        "registry": {"rows": len(REGISTRY_ITEMS), "sha256": registry_hash(REGISTRY_ITEMS)},
        "mutations": mutations,
        "claim_ceiling": "EXACT_L0_TERMINAL_INNOVATION_EQUIVALENCE_AND_BYPASS_STOP",
        "signed_terminal_innovation_saving": "OPEN_NEW_ARITHMETIC_THEOREM",
        "arithmetic_advance": CONTRACT["arithmetic_advance"] == "YES",
        "fixed_atom_credit": CONTRACT["fixed_atom_credit"],
        "strict_1_over_400": registry["STRICT_1_OVER_400"],
        "L2": registry["L2"],
        "TPC_207_TRIGGER": CONTRACT["TPC_207_TRIGGER"],
    }
    require(result["arithmetic_advance"] is False, "result promoted arithmetic")
    require(result["TPC_207_TRIGGER"] is False, "result promoted TPC-207")
    require(result["check"] is True, "result check flag changed")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the read-only exact V20 checks")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.check:
        raise SystemExit("read-only checker requires --check")
    print(json.dumps(run_check(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
