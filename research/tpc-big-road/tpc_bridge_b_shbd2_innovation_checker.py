#!/usr/bin/env python3
"""Read-only exact checker for the V19 SHB-D2 raw-row/innovation interface.

The checker proves finite algebra and fixture statements only.  In particular,
it does not prove the separated SHB-D2 estimate, a physical innovation bound,
or any arithmetic L2 advance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import lru_cache, reduce
from math import gcd
from typing import Iterable, Iterator


class CheckFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


PRIMES = (2, 3, 5, 7, 11, 13, 17, 19)
J_NUM = 133
J_DEN = 400
BASE_STAGE = 5
TERMINAL_STAGE = 7
P5 = math.prod(PRIMES[:BASE_STAGE])

SOURCE_PDF_SHA256 = (
    "49718b030ec4552dbf6b0cb8e3af541def02ca0def2447dad45bf41459a416f9"
)
SOURCE_LOCATOR = "Ford--Maynard, Lemma 5.2, printed page 19"

RAW_TERM_TYPES = (
    {
        "raw_type_id": "HB2-J1",
        "j": 1,
        "combinatorial_coefficient": 2,
        "ordered_slots": ("e1", "f1"),
        "slot_kinds": ("E", "F"),
        "distinguished_log_slot": "f1",
    },
    {
        "raw_type_id": "HB2-J2",
        "j": 2,
        "combinatorial_coefficient": -1,
        "ordered_slots": ("e1", "e2", "f1", "f2"),
        "slot_kinds": ("E", "E", "F", "F"),
        "distinguished_log_slot": "f1",
    },
)

ROUTING_CONVENTION = {
    "component_order": "SOURCE_SLOT_ORDER_E_THEN_F",
    "unit_slot_policy": "RETAIN_IN_OCCURRENCE_REMOVE_FOR_GROUPING",
    "large_component_order": "FIRST_IN_SOURCE_SLOT_ORDER",
    "subset_order": "INCREASING_ORIGINAL_SLOT_BITMASK",
    "h2_endpoint": "COMPLEMENT_POWER_400_LE_X_POWER_133",
    "master_lower_endpoint": "M_POWER_400_GT_(X_PHYS)_POWER_133",
    "master_upper_endpoint": "M_SQUARED_LE_ANALYTIC_X",
}

EXPECTED_CONTRACT = {
    "route_version": "V19",
    "physical_h0": 2,
    "HB_order_h": 2,
    "HB_root_s": 1,
    "J": "133/400",
    "analytic_physical_binding": "analytic_x=2*physical_X",
    "raw_term_type_count": 2,
    "raw_outer_coefficients": (2, -1),
    "raw_emitter": "PROVED_EXACT_FINITE_AFTER_DERIVED_ROUTING",
    "raw_row_representation": "COVECTOR_COORDINATE_SUM",
    "separated_template_registry": "ABSENT",
    "separated_SHB_D2_theorem": "OPEN_NEW_THEOREM",
    "source_innovation": "MANDATORY_FOR_LITERAL_RESIDUAL_PRIMALIZATION",
    "V16_Err_crosswalk": "ABSENT",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "strict_1_over_400": "UNPAID",
    "L2": "NONE",
    "TPC_207_TRIGGER": False,
}

EXPECTED_STATUS_REGISTRY_ITEMS = (
    ("HB2_PRIMARY_SOURCE", "LOCKED_PDF_SHA256_AND_PRINTED_PAGE"),
    ("HB2_ROOT_ONE_TERM_TYPES", "SOURCE_LOCKED_EXACTLY_TWO"),
    ("HB2_J1_OUTER_COEFFICIENT", "+2"),
    ("HB2_J2_OUTER_COEFFICIENT", "-1"),
    ("HB2_ORDERED_UNIT_SLOTS", "SOURCE_LOCKED_RETAINED"),
    ("HB2_ROOT_GE_2", "SEPARATE_PERFECT_POWER_REMAINDER"),
    ("HB2_CANONICAL_ROUTING", "DERIVED_EXACT_DETERMINISTIC_CONVENTION"),
    ("HB2_RAW_MASTER_EMITTER", "PROVED_EXACT_FINITE"),
    ("HB2_RAW_MASTER_TO_PRIMORIAL_COVECTOR", "PROVED_EXACT"),
    ("HB2_RAW_MASTER_K5_B7_ROWS", "120"),
    ("HB2_RAW_MASTER_K5_B7_COORDINATE_SUPPORT", "92"),
    ("HB2_RAW_MASTER_K5_B7_RANK", "56"),
    ("HB2_RAW_MASTER_K5_B7_INCREMENTAL_RANKS", "17,27,12"),
    ("HB2_RAW_MASTER_K5_B7_WRAP", "NONE"),
    ("HB2_RAW_MASTER_NORMS", "DECIMAL_DIAGNOSTIC_EXACT_FORMULA"),
    ("HB2_RAW_MASTER_CONDITIONING", "NOT_CERTIFIED"),
    ("SHB_D2_SEPARATED_TEMPLATE_REGISTRY", "ABSENT"),
    ("SHB_D2_MELLIN_PERRON_L1_TAIL_LEDGER", "ABSENT"),
    ("SHB_D2_ANALYTIC_SAVING", "OPEN_NEW_THEOREM"),
    ("R_P_RANGE_CHARACTERIZATION", "PROVED_EXACT"),
    ("R_P_ORTHOGONAL_PROJECTION", "PROVED_EXACT"),
    ("SHB_D2_RESIDUAL_HOMOGENEOUS_R_SOURCE", "STOP_SCOPED_RANGE_VIOLATION"),
    ("SHB_D2_SOURCE_INNOVATION", "MANDATORY_IF_RESIDUAL_IS_PRIMAL"),
    ("SOURCE_INNOVATION_VERSUS_V16_ERR", "DISTINCT_UNTYPED_CROSSWALK"),
    ("SOURCE_INNOVATION_DUHAMEL", "PROVED_EXACT_ONE_STEP"),
    ("SOURCE_INNOVATION_PHYSICAL_EVALUATION", "OPEN_NEW_THEOREM"),
    ("FIXED_ATOM_CREDIT", "0"),
    ("STRICT_1_OVER_400", "UNPAID"),
    ("L2", "NONE"),
    ("TPC_207_TRIGGER", "false"),
)

EXPECTED_REGISTRY_SHA256 = (
    "f17522e84c5c3a3de0ef0ab7ceb4f429e9aea8e89eee92d255d1b5d0fdc42342"
)


def canonical_raw_term_types() -> tuple[dict[str, object], ...]:
    """Return an independent literal lock for the two printed HB2 rows."""
    return (
        {
            "raw_type_id": "HB2-J1",
            "j": 1,
            "combinatorial_coefficient": 2,
            "ordered_slots": ("e1", "f1"),
            "slot_kinds": ("E", "F"),
            "distinguished_log_slot": "f1",
        },
        {
            "raw_type_id": "HB2-J2",
            "j": 2,
            "combinatorial_coefficient": -1,
            "ordered_slots": ("e1", "e2", "f1", "f2"),
            "slot_kinds": ("E", "E", "F", "F"),
            "distinguished_log_slot": "f1",
        },
    )


def canonical_routing_convention() -> dict[str, str]:
    """Return the exact derived-routing semantic lock."""
    return {
        "component_order": "SOURCE_SLOT_ORDER_E_THEN_F",
        "unit_slot_policy": "RETAIN_IN_OCCURRENCE_REMOVE_FOR_GROUPING",
        "large_component_order": "FIRST_IN_SOURCE_SLOT_ORDER",
        "subset_order": "INCREASING_ORIGINAL_SLOT_BITMASK",
        "h2_endpoint": "COMPLEMENT_POWER_400_LE_X_POWER_133",
        "master_lower_endpoint": "M_POWER_400_GT_(X_PHYS)_POWER_133",
        "master_upper_endpoint": "M_SQUARED_LE_ANALYTIC_X",
    }


def canonical_contract() -> dict[str, object]:
    """Return a fresh contract whose values are not mutable module truth."""
    return {
        "route_version": "V19",
        "physical_h0": 2,
        "HB_order_h": 2,
        "HB_root_s": 1,
        "J": "133/400",
        "analytic_physical_binding": "analytic_x=2*physical_X",
        "raw_term_type_count": 2,
        "raw_outer_coefficients": (2, -1),
        "raw_emitter": "PROVED_EXACT_FINITE_AFTER_DERIVED_ROUTING",
        "raw_row_representation": "COVECTOR_COORDINATE_SUM",
        "separated_template_registry": "ABSENT",
        "separated_SHB_D2_theorem": "OPEN_NEW_THEOREM",
        "source_innovation": "MANDATORY_FOR_LITERAL_RESIDUAL_PRIMALIZATION",
        "V16_Err_crosswalk": "ABSENT",
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "strict_1_over_400": "UNPAID",
        "L2": "NONE",
        "TPC_207_TRIGGER": False,
    }


def canonical_registry_items() -> tuple[tuple[str, str], ...]:
    """Return all 30 semantic rows independently of the published bundle."""
    return (
        ("HB2_PRIMARY_SOURCE", "LOCKED_PDF_SHA256_AND_PRINTED_PAGE"),
        ("HB2_ROOT_ONE_TERM_TYPES", "SOURCE_LOCKED_EXACTLY_TWO"),
        ("HB2_J1_OUTER_COEFFICIENT", "+2"),
        ("HB2_J2_OUTER_COEFFICIENT", "-1"),
        ("HB2_ORDERED_UNIT_SLOTS", "SOURCE_LOCKED_RETAINED"),
        ("HB2_ROOT_GE_2", "SEPARATE_PERFECT_POWER_REMAINDER"),
        ("HB2_CANONICAL_ROUTING", "DERIVED_EXACT_DETERMINISTIC_CONVENTION"),
        ("HB2_RAW_MASTER_EMITTER", "PROVED_EXACT_FINITE"),
        ("HB2_RAW_MASTER_TO_PRIMORIAL_COVECTOR", "PROVED_EXACT"),
        ("HB2_RAW_MASTER_K5_B7_ROWS", "120"),
        ("HB2_RAW_MASTER_K5_B7_COORDINATE_SUPPORT", "92"),
        ("HB2_RAW_MASTER_K5_B7_RANK", "56"),
        ("HB2_RAW_MASTER_K5_B7_INCREMENTAL_RANKS", "17,27,12"),
        ("HB2_RAW_MASTER_K5_B7_WRAP", "NONE"),
        ("HB2_RAW_MASTER_NORMS", "DECIMAL_DIAGNOSTIC_EXACT_FORMULA"),
        ("HB2_RAW_MASTER_CONDITIONING", "NOT_CERTIFIED"),
        ("SHB_D2_SEPARATED_TEMPLATE_REGISTRY", "ABSENT"),
        ("SHB_D2_MELLIN_PERRON_L1_TAIL_LEDGER", "ABSENT"),
        ("SHB_D2_ANALYTIC_SAVING", "OPEN_NEW_THEOREM"),
        ("R_P_RANGE_CHARACTERIZATION", "PROVED_EXACT"),
        ("R_P_ORTHOGONAL_PROJECTION", "PROVED_EXACT"),
        ("SHB_D2_RESIDUAL_HOMOGENEOUS_R_SOURCE", "STOP_SCOPED_RANGE_VIOLATION"),
        ("SHB_D2_SOURCE_INNOVATION", "MANDATORY_IF_RESIDUAL_IS_PRIMAL"),
        ("SOURCE_INNOVATION_VERSUS_V16_ERR", "DISTINCT_UNTYPED_CROSSWALK"),
        ("SOURCE_INNOVATION_DUHAMEL", "PROVED_EXACT_ONE_STEP"),
        ("SOURCE_INNOVATION_PHYSICAL_EVALUATION", "OPEN_NEW_THEOREM"),
        ("FIXED_ATOM_CREDIT", "0"),
        ("STRICT_1_OVER_400", "UNPAID"),
        ("L2", "NONE"),
        ("TPC_207_TRIGGER", "false"),
    )


def validate_exact_mapping(
    candidate: object,
    expected: dict[str, object],
    label: str,
) -> None:
    require(type(candidate) is dict, f"{label} must be an exact dict")
    candidate_dict = candidate
    require(set(candidate_dict) == set(expected), f"{label} exact key set changed")
    for key, locked in expected.items():
        actual = candidate_dict[key]
        require(type(actual) is type(locked), f"{label} field {key} has wrong exact type")
        require(actual == locked, f"{label} field {key} changed")


def validate_raw_term_types(candidate: object) -> None:
    expected = canonical_raw_term_types()
    require(type(candidate) is tuple, "raw term types must be an exact tuple")
    require(len(candidate) == len(expected), "raw term type count changed")
    for index, (actual, locked) in enumerate(zip(candidate, expected, strict=True)):
        validate_exact_mapping(actual, locked, f"raw term type {index}")


def validate_routing_convention(candidate: object) -> None:
    validate_exact_mapping(candidate, canonical_routing_convention(), "routing convention")


def validate_contract(candidate: object) -> None:
    validate_exact_mapping(candidate, canonical_contract(), "contract")


def validate_fixed_source_locks() -> None:
    require(PRIMES == (2, 3, 5, 7, 11, 13, 17, 19), "prime clock changed")
    require(J_NUM == 133 and J_DEN == 400, "J endpoint changed")
    require(BASE_STAGE == 5 and TERMINAL_STAGE == 7, "fixture stage range changed")
    require(P5 == 2310, "fixture base modulus changed")
    require(
        SOURCE_LOCATOR == "Ford--Maynard, Lemma 5.2, printed page 19",
        "source locator changed",
    )
    require(
        SOURCE_PDF_SHA256
        == "49718b030ec4552dbf6b0cb8e3af541def02ca0def2447dad45bf41459a416f9",
        "source PDF lock changed",
    )


def registry_hash(items: Iterable[tuple[str, str]]) -> str:
    payload = "".join(f"{key}={value}\n" for key, value in items)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_registry(candidate: object, expected_digest: object) -> None:
    semantic_locks = canonical_registry_items()
    require(type(candidate) is tuple, "registry must be an exact tuple")
    require(candidate == semantic_locks, "registry semantic content changed")
    keys = [key for key, _ in candidate]
    require(len(keys) == 30, "registry row count changed")
    require(len(set(keys)) == len(keys), "registry keys are not unique")
    locked_digest = "f17522e84c5c3a3de0ef0ab7ceb4f429e9aea8e89eee92d255d1b5d0fdc42342"
    require(type(expected_digest) is str, "registry digest has wrong exact type")
    require(expected_digest == locked_digest, "registry digest lock changed")
    require(
        registry_hash(candidate) == locked_digest,
        "registry final-LF hash changed",
    )


def validate_registry_semantics(
    candidate: tuple[tuple[str, str], ...],
    contract: dict[str, object],
    fixture: dict[str, object],
    innovation: dict[str, object],
) -> None:
    """Cross-bind the frozen rows to independently computed objects."""
    validate_contract(contract)
    validate_registry(candidate, EXPECTED_REGISTRY_SHA256)
    registry = dict(candidate)
    require(registry["HB2_RAW_MASTER_K5_B7_ROWS"] == str(fixture["rows"]), "registry/row computation mismatch")
    require(
        registry["HB2_RAW_MASTER_K5_B7_COORDINATE_SUPPORT"]
        == str(fixture["coordinate_support"]),
        "registry/support computation mismatch",
    )
    require(
        registry["HB2_RAW_MASTER_K5_B7_RANK"]
        == str(fixture["cumulative_ranks"]["7"]),
        "registry/rank computation mismatch",
    )
    require(
        registry["HB2_RAW_MASTER_K5_B7_INCREMENTAL_RANKS"]
        == ",".join(str(value) for value in fixture["incremental_ranks"]),
        "registry/incremental-rank computation mismatch",
    )
    require(
        innovation["range_criterion"]
        == "ZERO_ON_DELETED_AND_CONSTANT_ON_SURVIVOR_FIBERS",
        "registry/range computation mismatch",
    )
    require(
        contract["separated_template_registry"] == "ABSENT"
        and registry["SHB_D2_SEPARATED_TEMPLATE_REGISTRY"] == "ABSENT",
        "contract/registry template mismatch",
    )
    require(
        contract["separated_SHB_D2_theorem"] == "OPEN_NEW_THEOREM"
        and registry["SHB_D2_ANALYTIC_SAVING"] == "OPEN_NEW_THEOREM",
        "contract/registry theorem mismatch",
    )
    require(
        contract["arithmetic_advance"] == "NO"
        and registry["FIXED_ATOM_CREDIT"] == "0"
        and registry["STRICT_1_OVER_400"] == "UNPAID"
        and registry["L2"] == "NONE"
        and registry["TPC_207_TRIGGER"] == "false"
        and contract["TPC_207_TRIGGER"] is False,
        "contract/registry release firewall mismatch",
    )


@lru_cache(maxsize=None)
def factorization(n: int) -> tuple[tuple[int, int], ...]:
    require(type(n) is int and n >= 1, "factorization domain failure")
    value = n
    prime = 2
    factors: list[tuple[int, int]] = []
    while prime * prime <= value:
        exponent = 0
        while value % prime == 0:
            value //= prime
            exponent += 1
        if exponent:
            factors.append((prime, exponent))
        prime += 1
    if value > 1:
        factors.append((value, 1))
    return tuple(factors)


@lru_cache(maxsize=None)
def divisors(n: int) -> tuple[int, ...]:
    values = [1]
    for prime, exponent in factorization(n):
        values = [
            old * prime**power
            for old in values
            for power in range(exponent + 1)
        ]
    return tuple(sorted(values))


@lru_cache(maxsize=None)
def mobius(n: int) -> int:
    factors = factorization(n)
    if any(exponent > 1 for _, exponent in factors):
        return 0
    return -1 if len(factors) % 2 else 1


def log_vector(n: int) -> dict[int, int]:
    return {prime: exponent for prime, exponent in factorization(n)}


def add_log_vector(target: dict[int, int], n: int, scale: int) -> None:
    require(type(scale) is int, "formal-log scale must be an exact int")
    for prime, exponent in factorization(n):
        target[prime] = target.get(prime, 0) + scale * exponent
        if target[prime] == 0:
            del target[prime]


def mangoldt_vector(n: int) -> dict[int, int]:
    factors = factorization(n)
    if len(factors) != 1:
        return {}
    prime, _ = factors[0]
    return {prime: 1}


def validate_source_identity() -> int:
    cases = 0
    for top in (31, 36, 64, 127, 257, 359):
        cutoff = math.isqrt(top)
        for n in range(2, top + 1):
            a1: dict[int, int] = {}
            a2: dict[int, int] = {}
            for e in divisors(n):
                if e <= cutoff:
                    add_log_vector(a1, n // e, mobius(e))
            for e1 in divisors(n):
                if e1 > cutoff:
                    continue
                for e2 in divisors(n // e1):
                    if e2 > cutoff:
                        continue
                    remainder = n // (e1 * e2)
                    for f1 in divisors(remainder):
                        add_log_vector(
                            a2,
                            f1,
                            mobius(e1) * mobius(e2),
                        )
            combined: dict[int, int] = {}
            for prime, coefficient in a1.items():
                combined[prime] = combined.get(prime, 0) + 2 * coefficient
            for prime, coefficient in a2.items():
                combined[prime] = combined.get(prime, 0) - coefficient
                if combined[prime] == 0:
                    del combined[prime]
            require(
                combined == mangoldt_vector(n),
                f"HB2 root-one identity failed at top={top}, n={n}",
            )
            cases += 1
    return cases


def h2_complement(complement: int, analytic_x: int) -> bool:
    return complement**J_DEN <= analytic_x**J_NUM


def master_physical_window(group: int, analytic_x: int) -> bool:
    physical_x = analytic_x // 2
    return (
        group**J_DEN > physical_x**J_NUM
        and group * group <= analytic_x
    )


def route_occurrence(
    product: int,
    analytic_x: int,
    slots: tuple[int, ...],
    kinds: tuple[str, ...],
) -> tuple[str, int | None, int | None]:
    require(math.prod(slots) == product, "occurrence product changed")
    require(len(slots) == len(kinds), "slot kind arity changed")
    active = tuple(index for index, value in enumerate(slots) if value > 1)
    require(bool(active), "zero log occurrence cannot have no active slot")
    large = tuple(index for index in active if slots[index] ** 2 >= product)
    if large:
        first = large[0]
        complement = product // slots[first]
        if kinds[first] == "F" and h2_complement(complement, analytic_x):
            return ("H2", None, first)
        if kinds[first] == "F":
            selected_mask = sum(1 << index for index in active if index != first)
            group = complement
        else:
            selected_mask = 1 << first
            group = slots[first]
        require(
            master_physical_window(group, analytic_x),
            "large-component MASTER group left the physical window",
        )
        return ("MASTER", selected_mask, first)

    full_active_mask = sum(1 << index for index in active)
    candidates: list[tuple[int, int]] = []
    for mask in range(1, 1 << len(slots)):
        if mask & ~full_active_mask:
            continue
        if mask == full_active_mask:
            continue
        group = math.prod(
            slots[index]
            for index in active
            if mask & (1 << index)
        )
        if group**J_DEN >= product**J_NUM and group * group <= product:
            candidates.append((mask, group))
    require(bool(candidates), "no-large occurrence has no admissible subset")
    selected_mask, group = candidates[0]
    require(
        master_physical_window(group, analytic_x),
        "subset MASTER group left the physical window",
    )
    return ("MASTER", selected_mask, None)


def active_occurrences(
    product: int,
    analytic_x: int,
) -> Iterator[tuple[int, tuple[int, ...], tuple[str, ...]]]:
    cutoff = math.isqrt(analytic_x)
    for e1 in divisors(product):
        if e1 > cutoff:
            continue
        f1 = product // e1
        coefficient = 2 * mobius(e1)
        if coefficient and f1 > 1:
            yield coefficient, (e1, f1), ("E", "F")
    for e1 in divisors(product):
        if e1 > cutoff:
            continue
        remainder1 = product // e1
        for e2 in divisors(remainder1):
            if e2 > cutoff:
                continue
            remainder = remainder1 // e2
            coefficient = -mobius(e1) * mobius(e2)
            if not coefficient:
                continue
            for f1 in divisors(remainder):
                if f1 == 1:
                    continue
                f2 = remainder // f1
                yield coefficient, (e1, e2, f1, f2), (
                    "E",
                    "E",
                    "F",
                    "F",
                )


@lru_cache(maxsize=None)
def raw_master_numerator(
    product: int,
    analytic_x: int,
) -> tuple[tuple[tuple[int, int], ...], int, int]:
    numerator: dict[int, int] = {}
    master_count = 0
    h2_count = 0
    for coefficient, slots, kinds in active_occurrences(product, analytic_x):
        route, _, _ = route_occurrence(product, analytic_x, slots, kinds)
        if route == "H2":
            h2_count += 1
            continue
        master_count += 1
        distinguished_f1 = slots[1] if len(slots) == 2 else slots[2]
        add_log_vector(numerator, distinguished_f1, coefficient)
    return tuple(sorted(numerator.items())), master_count, h2_count


def primitive_direction(
    vector: dict[int, int],
) -> tuple[tuple[tuple[int, int], ...], int]:
    require(bool(vector), "zero vector has no primitive direction")
    content = reduce(gcd, (abs(value) for value in vector.values()))
    first_prime = min(vector)
    sign = 1 if vector[first_prime] > 0 else -1
    direction = tuple(
        sorted(
            (prime, sign * value // content)
            for prime, value in vector.items()
        )
    )
    scalar = sign * content
    return direction, scalar


def vector_scalar(
    vector: dict[int, int],
    direction: tuple[tuple[int, int], ...],
) -> int:
    direction_dict = dict(direction)
    first_prime = min(direction_dict)
    require(first_prime in vector, "direction support changed")
    require(
        vector[first_prime] % direction_dict[first_prime] == 0,
        "direction scalar ceased to be integral",
    )
    scalar = vector[first_prime] // direction_dict[first_prime]
    require(
        vector == {
            prime: scalar * coefficient
            for prime, coefficient in direction_dict.items()
        },
        "column formal-log direction changed",
    )
    return scalar


def stage_band(stage: int) -> range:
    prime = PRIMES[stage - 1]
    next_prime = PRIMES[stage]
    return range(
        (prime * prime - 1) // 2,
        (next_prime * next_prime - 3) // 2 + 1,
    )


def pullback_survives(integer: int, source_stage: int) -> bool:
    return all(
        integer % prime and (integer + 2) % prime
        for prime in PRIMES[BASE_STAGE:source_stage]
    )


def exact_fraction_rank(rows: Iterable[dict[int, int]]) -> int:
    pivots: dict[int, dict[int, Fraction]] = {}
    for integer_row in rows:
        row = {
            column: Fraction(value)
            for column, value in integer_row.items()
            if value
        }
        while row:
            column = min(row)
            if column not in pivots:
                pivot = row[column]
                pivots[column] = {
                    index: value / pivot for index, value in row.items()
                }
                break
            factor = row[column]
            for index, value in pivots[column].items():
                updated = row.get(index, Fraction(0)) - factor * value
                if updated:
                    row[index] = updated
                else:
                    row.pop(index, None)
    return len(pivots)


def build_k5_b7_fixture() -> dict[str, object]:
    require(P5 == 2310, "P5 changed")
    directions: dict[int, tuple[tuple[int, int], ...]] = {}
    symbolic_rows: list[tuple[int, int, dict[int, int]]] = []
    occurrence_master = 0
    occurrence_h2 = 0
    source_stage_supports: dict[int, set[int]] = defaultdict(set)
    for source_stage in range(BASE_STAGE, TERMINAL_STAGE + 1):
        for physical_x in stage_band(source_stage):
            analytic_x = 2 * physical_x
            require(analytic_x < P5, "k=5,b=7 no-wrap failed")
            row: dict[int, int] = {}
            for integer in range(physical_x + 1, analytic_x + 1):
                numerator_items, master_count, h2_count = raw_master_numerator(
                    integer,
                    analytic_x,
                )
                occurrence_master += master_count
                occurrence_h2 += h2_count
                if not pullback_survives(integer, source_stage):
                    continue
                numerator = dict(numerator_items)
                if not numerator:
                    continue
                direction, _ = primitive_direction(numerator)
                if integer in directions:
                    require(
                        directions[integer] == direction,
                        "fixture column has multiple formal-log directions",
                    )
                else:
                    directions[integer] = direction
                row[integer] = vector_scalar(numerator, direction)
                source_stage_supports[source_stage].add(integer)
            require(bool(row), "raw MASTER fixture row is empty")
            symbolic_rows.append((source_stage, physical_x, row))

    columns = sorted(directions)
    column_index = {integer: index for index, integer in enumerate(columns)}
    integer_rows = [
        {column_index[integer]: value for integer, value in row.items()}
        for _, _, row in symbolic_rows
    ]
    stage_ranks = {
        stage: exact_fraction_rank(
            integer_rows[index]
            for index, (row_stage, _, _) in enumerate(symbolic_rows)
            if row_stage == stage
        )
        for stage in range(BASE_STAGE, TERMINAL_STAGE + 1)
    }
    cumulative_ranks = {
        terminal: exact_fraction_rank(
            integer_rows[index]
            for index, (row_stage, _, _) in enumerate(symbolic_rows)
            if row_stage <= terminal
        )
        for terminal in range(BASE_STAGE, TERMINAL_STAGE + 1)
    }
    incremental_ranks = (
        cumulative_ranks[5],
        cumulative_ranks[6] - cumulative_ranks[5],
        cumulative_ranks[7] - cumulative_ranks[6],
    )

    require(len(symbolic_rows) == 120, "fixture row count changed")
    require(len(columns) == 92, "fixture support count changed")
    require(stage_ranks == {5: 17, 6: 29, 7: 12}, "stage ranks changed")
    require(
        cumulative_ranks == {5: 17, 6: 44, 7: 56},
        "cumulative ranks changed",
    )
    require(incremental_ranks == (17, 27, 12), "incremental ranks changed")
    require(
        {stage: len(values) for stage, values in source_stage_supports.items()}
        == {5: 43, 6: 51, 7: 41},
        "source-stage support counts changed",
    )

    with localcontext() as context:
        context.prec = 70
        log_primes = {
            prime: Decimal(prime).ln()
            for direction in directions.values()
            for prime, _ in direction
        }
        column_scales = {}
        for integer, direction in directions.items():
            numerator_value = sum(
                Decimal(coefficient) * log_primes[prime]
                for prime, coefficient in direction
            )
            require(numerator_value != 0, "formal-log direction evaluated to zero")
            column_scales[integer] = numerator_value / Decimal(integer).ln()
        raw_norms = []
        for _, _, row in symbolic_rows:
            norm_squared = sum(
                (Decimal(value) * column_scales[integer]) ** 2
                for integer, value in row.items()
            )
            require(norm_squared > 0, "fixture row norm vanished")
            raw_norms.append(norm_squared.sqrt())
        riesz_multiplier = Decimal(P5).sqrt()
        norm_diagnostic = {
            "precision_digits": context.prec,
            "raw_l2_min": format(min(raw_norms), ".18E"),
            "raw_l2_max": format(max(raw_norms), ".18E"),
            "base_Haar_Riesz_min": format(min(raw_norms) * riesz_multiplier, ".18E"),
            "base_Haar_Riesz_max": format(max(raw_norms) * riesz_multiplier, ".18E"),
            "conditioning": "NOT_CERTIFIED_COLUMN_LOG_SCALES_RETAINED",
        }

    return {
        "rows": len(symbolic_rows),
        "coordinate_support": len(columns),
        "stage_supports": {
            str(stage): len(source_stage_supports[stage])
            for stage in range(BASE_STAGE, TERMINAL_STAGE + 1)
        },
        "stage_ranks": {str(key): value for key, value in stage_ranks.items()},
        "cumulative_ranks": {
            str(key): value for key, value in cumulative_ranks.items()
        },
        "incremental_ranks": incremental_ranks,
        "master_occurrences_before_pullback": occurrence_master,
        "h2_occurrences_before_pullback": occurrence_h2,
        "norm_diagnostic": norm_diagnostic,
    }


def pair_mask(integer: int, prime: int) -> int:
    return int(integer % prime != 0 and (integer + 2) % prime != 0)


def replication(parent: tuple[Fraction, ...], modulus: int, prime: int) -> tuple[Fraction, ...]:
    require(gcd(modulus, prime) == 1, "replication requires a new prime")
    child = [Fraction(0) for _ in range(modulus * prime)]
    for residue, value in enumerate(parent):
        for copy in range(prime):
            integer = residue + copy * modulus
            if pair_mask(integer, prime):
                child[integer] = value
    return tuple(child)


def adjoint(child: tuple[Fraction, ...], modulus: int, prime: int) -> tuple[Fraction, ...]:
    require(gcd(modulus, prime) == 1, "adjoint requires a new prime")
    return tuple(
        sum(
            child[residue + copy * modulus]
            for copy in range(prime)
            if pair_mask(residue + copy * modulus, prime)
        )
        / prime
        for residue in range(modulus)
    )


def raw_covector_pullback(
    row: tuple[Fraction, ...],
    modulus: int,
    prime: int,
) -> tuple[Fraction, ...]:
    require(gcd(modulus, prime) == 1, "covector pullback requires a new prime")
    return tuple(
        sum(
            row[residue + copy * modulus]
            for copy in range(prime)
            if pair_mask(residue + copy * modulus, prime)
        )
        for residue in range(modulus)
    )


def dot(row: tuple[Fraction, ...], vector: tuple[Fraction, ...]) -> Fraction:
    require(len(row) == len(vector), "dot arity mismatch")
    return sum((left * right for left, right in zip(row, vector)), Fraction(0))


def validate_range_projection_and_witness() -> dict[str, object]:
    modulus = 6
    prime = 5
    alpha = Fraction(3, 5)
    parent = tuple(Fraction(index - 2) for index in range(modulus))
    child = replication(parent, modulus, prime)
    require(
        adjoint(child, modulus, prime)
        == tuple(alpha * value for value in parent),
        "R*R=alpha I failed",
    )

    arbitrary = tuple(Fraction((index * 7 + 3) % 11 - 5) for index in range(30))
    projected_parent = tuple(
        value / alpha for value in adjoint(arbitrary, modulus, prime)
    )
    projected = replication(projected_parent, modulus, prime)
    projected_twice_parent = tuple(
        value / alpha for value in adjoint(projected, modulus, prime)
    )
    projected_twice = replication(projected_twice_parent, modulus, prime)
    require(projected_twice == projected, "orthogonal projection is not idempotent")
    innovation = tuple(
        value - projection for value, projection in zip(arbitrary, projected)
    )
    require(
        adjoint(innovation, modulus, prime) == (Fraction(0),) * modulus,
        "source innovation is not orthogonal to ran R",
    )

    beta = tuple(Fraction((index % 5) - 2) for index in range(30))
    beta_pullback = raw_covector_pullback(beta, modulus, prime)
    require(
        dot(beta, arbitrary)
        == dot(beta_pullback, projected_parent) + dot(beta, innovation),
        "one-step source-innovation Duhamel identity failed",
    )

    analytic_x = 26
    physical_x = 13
    require(5 * 5 <= analytic_x + 2 < 7 * 7, "witness stage clock failed")
    require(physical_x * 2 == analytic_x, "witness x=2X binding failed")
    left = 14
    right = 26
    require(physical_x < left <= analytic_x, "left witness left shell")
    require(physical_x < right <= analytic_x, "right witness left shell")
    require(left % modulus == right % modulus == 2, "witness parent changed")
    require(pair_mask(left, prime) == 1, "left witness is not a survivor")
    require(pair_mask(right, prime) == 1, "right witness is not a survivor")
    require((left + 2) % 2 == 0 and (right + 2) % 2 == 0, "baseline zero failed")
    require(mangoldt_vector(left + 2) == {2: 1}, "Lambda(16) changed")
    require(mangoldt_vector(right + 2) == {}, "Lambda(28) changed")

    previous_x = 24
    previous_values: dict[int, list[dict[int, int]]] = defaultdict(list)
    for integer in range(previous_x // 2 + 1, previous_x + 1):
        if pair_mask(integer, prime) and (integer + 2) % 2 == 0:
            previous_values[integer % modulus].append(mangoldt_vector(integer + 2))
    require(
        all(
            len({tuple(sorted(value.items())) for value in values}) <= 1
            for values in previous_values.values()
        ),
        "an earlier exact baseline-zero witness exists at x=24",
    )

    require(math.prod(PRIMES[:4]) > PRIMES[5] ** 2, "large-stage base inequality failed")
    return {
        "range_criterion": "ZERO_ON_DELETED_AND_CONSTANT_ON_SURVIVOR_FIBERS",
        "projection": "alpha^-1 R R*",
        "source_innovation": "(I-alpha^-1 R R*)v",
        "smallest_no_wrap_same_shell_survivor_constancy_witness": {
            "child_stage": 3,
            "P_parent": 6,
            "new_prime": 5,
            "analytic_x": analytic_x,
            "physical_X": physical_x,
            "same_parent_survivors": (left, right),
            "residual_values": ("log(2)", "0"),
        },
        "large_stage_induction_base": "P4=210>p6^2=169",
    }


def mutation_value(value: object) -> object:
    if type(value) is bool:
        return 1 if value is False else 0
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "_MUTATED"
    if type(value) is tuple:
        return value + (999,)
    raise CheckFailure("unhandled mutation value type")


def run_mutations() -> dict[str, int]:
    contract_base = canonical_contract()
    contract_rejected = 0
    for key in contract_base:
        candidate = dict(contract_base)
        candidate[key] = mutation_value(candidate[key])
        try:
            validate_contract(candidate)
        except CheckFailure:
            contract_rejected += 1
        else:
            raise CheckFailure(f"contract mutation escaped at {key}")

    missing = dict(contract_base)
    missing.pop("physical_h0")
    try:
        validate_contract(missing)
    except CheckFailure:
        contract_rejected += 1
    else:
        raise CheckFailure("missing contract field escaped")

    extra = dict(contract_base)
    extra["unknown"] = "value"
    try:
        validate_contract(extra)
    except CheckFailure:
        contract_rejected += 1
    else:
        raise CheckFailure("extra contract field escaped")

    coordinated_contract = dict(contract_base)
    coordinated_contract.update(
        {
            "separated_template_registry": "PRESENT_FALSE_PROMOTION",
            "separated_SHB_D2_theorem": "PROVED_FALSE_PROMOTION",
            "arithmetic_advance": "YES",
            "fixed_atom_credit": 1,
            "strict_1_over_400": "PAID_FALSE_PROMOTION",
            "L2": "FULL_FALSE_PROMOTION",
            "TPC_207_TRIGGER": True,
        }
    )
    try:
        validate_contract(coordinated_contract)
    except CheckFailure:
        contract_rejected += 1
    else:
        raise CheckFailure("coordinated contract false release escaped")

    registry_base = canonical_registry_items()
    registry_rejected = 0
    for index, (key, value) in enumerate(registry_base):
        candidate = list(registry_base)
        candidate[index] = (key, value + "_MUTATED")
        rebound = tuple(candidate)
        try:
            validate_registry(rebound, registry_hash(rebound))
        except CheckFailure:
            registry_rejected += 1
        else:
            raise CheckFailure(f"registry mutation escaped at {key}")

    replacement = list(registry_base)
    replacement[-1] = ("UNKNOWN_REPLACEMENT_ROW", "false")
    try:
        rebound = tuple(replacement)
        validate_registry(rebound, registry_hash(rebound))
    except CheckFailure:
        registry_rejected += 1
    else:
        raise CheckFailure("unknown registry key replacement with rehash escaped")

    reordered = tuple(reversed(registry_base))
    try:
        validate_registry(reordered, registry_hash(reordered))
    except CheckFailure:
        registry_rejected += 1
    else:
        raise CheckFailure("registry reorder with rehash escaped")

    false_release = list(registry_base)
    false_release[-4:] = [
        ("FIXED_ATOM_CREDIT", "1"),
        ("STRICT_1_OVER_400", "PAID_FALSE_PROMOTION"),
        ("L2", "FULL_FALSE_PROMOTION"),
        ("TPC_207_TRIGGER", "true"),
    ]
    false_release_tuple = tuple(false_release)
    try:
        validate_registry(false_release_tuple, registry_hash(false_release_tuple))
    except CheckFailure:
        registry_rejected += 1
    else:
        raise CheckFailure("coordinated registry false release with rehash escaped")

    try:
        validate_registry(registry_base, EXPECTED_REGISTRY_SHA256 + "0")
    except CheckFailure:
        registry_rejected += 1
    else:
        raise CheckFailure("registry digest rebinding escaped")

    raw_base = canonical_raw_term_types()
    raw_rejected = 0
    for row_index, row in enumerate(raw_base):
        for key in row:
            candidate = [dict(item) for item in raw_base]
            candidate[row_index][key] = mutation_value(candidate[row_index][key])
            try:
                validate_raw_term_types(tuple(candidate))
            except CheckFailure:
                raw_rejected += 1
            else:
                raise CheckFailure(f"raw type mutation escaped at row={row_index}, key={key}")
    raw_missing = [dict(item) for item in raw_base]
    raw_missing[0].pop("ordered_slots")
    for label, candidate in (
        ("missing field", tuple(raw_missing)),
        ("extra field", ({**raw_base[0], "unknown": 1}, raw_base[1])),
        ("empty family", ()),
    ):
        try:
            validate_raw_term_types(candidate)
        except CheckFailure:
            raw_rejected += 1
        else:
            raise CheckFailure(f"raw type {label} escaped")

    routing_base = canonical_routing_convention()
    routing_rejected = 0
    for key in routing_base:
        candidate = dict(routing_base)
        candidate[key] = candidate[key] + "_FALSE_PROMOTION"
        try:
            validate_routing_convention(candidate)
        except CheckFailure:
            routing_rejected += 1
        else:
            raise CheckFailure(f"routing mutation escaped at {key}")
    routing_missing = dict(routing_base)
    routing_missing.pop("h2_endpoint")
    routing_extra = dict(routing_base)
    routing_extra["unknown"] = "value"
    for label, candidate in (("missing", routing_missing), ("extra", routing_extra)):
        try:
            validate_routing_convention(candidate)
        except CheckFailure:
            routing_rejected += 1
        else:
            raise CheckFailure(f"routing {label} mutation escaped")

    return {
        "contract_mutations_rejected": contract_rejected,
        "registry_mutations_rejected": registry_rejected,
        "raw_type_mutations_rejected": raw_rejected,
        "routing_mutations_rejected": routing_rejected,
    }


def run_check() -> dict[str, object]:
    validate_fixed_source_locks()
    validate_raw_term_types(RAW_TERM_TYPES)
    validate_routing_convention(ROUTING_CONVENTION)
    validate_contract(EXPECTED_CONTRACT)
    validate_registry(EXPECTED_STATUS_REGISTRY_ITEMS, EXPECTED_REGISTRY_SHA256)
    source_identity_cases = validate_source_identity()
    fixture = build_k5_b7_fixture()
    innovation = validate_range_projection_and_witness()
    validate_registry_semantics(
        EXPECTED_STATUS_REGISTRY_ITEMS,
        EXPECTED_CONTRACT,
        fixture,
        innovation,
    )
    mutations = run_mutations()
    require(fixture["rows"] == 120, "computed fixture/registry row mismatch")
    require(fixture["coordinate_support"] == 92, "computed support/registry mismatch")
    require(fixture["cumulative_ranks"]["7"] == 56, "computed rank/registry mismatch")
    registry = dict(EXPECTED_STATUS_REGISTRY_ITEMS)
    result = {
        "check": True,
        "route_version": EXPECTED_CONTRACT["route_version"],
        "source": {
            "locator": SOURCE_LOCATOR,
            "pdf_sha256": SOURCE_PDF_SHA256,
            "root_one_identity_cases": source_identity_cases,
            "raw_term_types": len(RAW_TERM_TYPES),
            "outer_coefficients": tuple(
                row["combinatorial_coefficient"] for row in RAW_TERM_TYPES
            ),
        },
        "routing": dict(ROUTING_CONVENTION),
        "fixture_k5_b7": fixture,
        "innovation": innovation,
        "registry": {
            "rows": len(EXPECTED_STATUS_REGISTRY_ITEMS),
            "sha256": registry_hash(EXPECTED_STATUS_REGISTRY_ITEMS),
        },
        "mutations": mutations,
        "claim_ceiling": "EXACT_L0_RAW_ROW_AND_SOURCE_INNOVATION_INTERFACE",
        "separated_SHB_D2": EXPECTED_CONTRACT["separated_SHB_D2_theorem"],
        "arithmetic_advance": EXPECTED_CONTRACT["arithmetic_advance"] == "YES",
        "fixed_atom_credit": EXPECTED_CONTRACT["fixed_atom_credit"],
        "strict_1_over_400": registry["STRICT_1_OVER_400"],
        "L2": registry["L2"],
        "TPC_207_TRIGGER": EXPECTED_CONTRACT["TPC_207_TRIGGER"],
    }
    require(
        set(result)
        == {
            "check",
            "route_version",
            "source",
            "routing",
            "fixture_k5_b7",
            "innovation",
            "registry",
            "mutations",
            "claim_ceiling",
            "separated_SHB_D2",
            "arithmetic_advance",
            "fixed_atom_credit",
            "strict_1_over_400",
            "L2",
            "TPC_207_TRIGGER",
        },
        "result key set changed",
    )
    require(result["check"] is True, "result check flag changed")
    require(result["arithmetic_advance"] is False, "arithmetic advance promoted")
    require(result["TPC_207_TRIGGER"] is False, "TPC-207 trigger promoted")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="run the read-only exact V19 checks",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.check:
        raise SystemExit("read-only checker requires --check")
    result = run_check()
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
