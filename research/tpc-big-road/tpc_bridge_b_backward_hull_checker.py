#!/usr/bin/env python3
"""Exact read-only checks for the typed Bridge-B backward-dual core.

This checker separates algebraic covector pullback from the normalized-Haar
Hilbert adjoint.  It verifies only the canonical mean/interval core and the
source-backed deletion-innovation formula.  The PBAPT Type-II family is not
materialized in the repository, so a complete physical-dual hull is required
to remain NOT_TESTABLE.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from fractions import Fraction


PRIMES = (2, 3, 5, 7, 11, 13, 17)

REGISTRY = {
    "BRIDGE_B_ADJOINT_ATOM_PULLBACK": "PROVED_EXACT_SURVIVOR_COLLAPSE",
    "BRIDGE_B_ALGEBRAIC_DUAL_PULLBACK": "PROVED_EXACT",
    "BRIDGE_B_ALL_GLOBAL_CHARACTERS": "STOP_SCOPED_FULL_PRIMORIAL_RANK",
    "BRIDGE_B_ARITHMETIC_ADVANCE": "NO",
    "BRIDGE_B_BACKWARD_INCREMENT_SUPPORT": "PROVED_EXACT_AT_MOST_THREE",
    "BRIDGE_B_BASE_INCOMING_FORCING": "PRIMAL_VECTOR_NOT_CANONICAL_DUAL",
    "BRIDGE_B_COMPLETE_DECLARED_DUAL_FAMILY": "NOT_TYPED",
    "BRIDGE_B_COMPLETE_HULL_RANK": "NOT_TESTABLE_FAIL_CLOSED",
    "BRIDGE_B_CORE_DUAL_FAMILY": "CANONICAL_MEAN_PLUS_ACTUAL_INTERVALS",
    "BRIDGE_B_CORE_HULL_ASYMPTOTIC": "OPEN_NO_UNIFORM_HORIZON_THEOREM",
    "BRIDGE_B_CORE_HULL_K4_B6": "PROVED_EXACT_RANK_119_OF_210",
    "BRIDGE_B_CORE_HULL_K5_B6": "PROVED_EXACT_RANK_85_OF_2310",
    "BRIDGE_B_CORE_HULL_K6_B6": "PROVED_EXACT_RANK_61_OF_30030",
    "BRIDGE_B_DELETION_INNOVATION_ACTIVE_REGISTRY": "ABSENT",
    "BRIDGE_B_DELETION_INNOVATION_AGGREGATE": "PROVED_EXACT_FORMULA",
    "BRIDGE_B_FIXED_HORIZON_WINDOWED_SUPPORT": "PROVED_O_H_LOWERCASE_P_K_SQUARED_AND_O_PRIMORIAL",
    "BRIDGE_B_HAAR_ADJOINT": "PROVED_EXACT_P_INVERSE_AVERAGE",
    "BRIDGE_B_INDIVIDUAL_DELETION_MODES": "CONDITIONAL_NOT_CANONICAL_FAMILY",
    "BRIDGE_B_LATER_DELETION_FORCING_PULLBACK": "PROVED_EXACT_SCALAR_MEAN",
    "BRIDGE_B_MAXIMAL_WINDOWED_FOURIER_BANK": "CONDITIONAL_RANK_AT_MOST_Q_PLUS_3_BANDCOUNT_MINUS_3",
    "BRIDGE_B_NONZERO_ERR_HULL_RANK": "DIAGNOSTIC_ONLY_NOT_NECESSARY_OBSTRUCTION",
    "BRIDGE_B_PBAPT_TYPEII_PRIMORIAL_CROSSWALK": "ABSENT",
    "BRIDGE_B_RIESZ_SCALING": "PROVED_EXACT_SOURCE_OVER_TARGET_MODULUS",
    "BRIDGE_B_SHB_D2_TYPEII_ROWS": "OPEN_MATERIALIZATION_GATE",
    "BRIDGE_B_TPC32_PACKET_TO_PRIMORIAL_DUAL": "ABSENT",
    "BRIDGE_B_TYPED_WINDOWED_FORCED_INNOVATION": "SELECTED_OPEN_NEW_THEOREM",
    "BRIDGE_B_UNTYPED_PLACEHOLDER_TO_COMPLETE_HULL": "STOP_SCOPED_FAIL_CLOSED",
    "BRIDGE_B_ZERO_DEFECT_HULL_RANK": "VALID_NECESSARY_OBSTRUCTION",
    "FIXED_ATOM_CREDIT": "0",
    "L2": "NONE",
    "STRICT_1_OVER_400": "UNPAID",
    "TPC_207_TRIGGER": "false",
}

EXPECTED_REGISTRY_SHA256 = "57ddfe6635fe56020516680d9be5732ea39196d0bac5f6d4492a9c7d7890cd9b"

CONTRACT_KEYS = frozenset(
    {
        "representation",
        "forcing_kind",
        "individual_modes_canonical",
        "universal_typeii_attached",
        "packet_aux_modulus_as_deletion_prime",
        "nonzero_err_treated_as_exact",
        "pbapt_attachment",
        "pbapt_row_registry",
        "pbapt_source_locator",
        "complete_declared_family",
        "complete_hull_rank",
        "tpc_207_trigger",
    }
)

FALSE_CONTRACT_FIELDS = (
    "individual_modes_canonical",
    "universal_typeii_attached",
    "packet_aux_modulus_as_deletion_prime",
    "nonzero_err_treated_as_exact",
    "pbapt_attachment",
    "complete_declared_family",
    "tpc_207_trigger",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_registry_bytes(registry: dict[str, str]) -> bytes:
    return "".join(
        f"{key}\t{registry[key]}\n" for key in sorted(registry)
    ).encode("utf-8")


def registry_sha256(registry: dict[str, str]) -> str:
    return hashlib.sha256(canonical_registry_bytes(registry)).hexdigest()


def primorial(stage: int) -> int:
    require(1 <= stage <= len(PRIMES), "unsupported prime stage")
    value = 1
    for prime in PRIMES[:stage]:
        value *= prime
    return value


def stage_band(stage: int) -> tuple[int, int, int]:
    require(2 <= stage < len(PRIMES), "stage band requires consecutive odd primes")
    physical_prime = PRIMES[stage - 1]
    next_prime = PRIMES[stage]
    lower = (physical_prime * physical_prime - 1) // 2
    upper = (next_prime * next_prime - 3) // 2
    count = upper - lower + 1
    require(
        count == (next_prime * next_prime - physical_prime * physical_prime) // 2,
        "stage-band cardinality failed",
    )
    return lower, upper, count


def survives_new_prime(integer: int, new_prime: int) -> bool:
    return integer % new_prime != 0 and (integer + 2) % new_prime != 0


def replication_deletion(parent: list[Fraction], new_prime: int) -> list[Fraction]:
    parent_modulus = len(parent)
    require(math.gcd(parent_modulus, new_prime) == 1, "non-coprime extension")
    child = [Fraction() for _ in range(parent_modulus * new_prime)]
    for residue, value in enumerate(parent):
        for copy_index in range(new_prime):
            lifted = residue + copy_index * parent_modulus
            if survives_new_prime(lifted, new_prime):
                child[lifted] = value
    return child


def haar_adjoint(child: list[Fraction], parent_modulus: int, new_prime: int) -> list[Fraction]:
    require(len(child) == parent_modulus * new_prime, "adjoint dimension mismatch")
    result = [Fraction() for _ in range(parent_modulus)]
    for residue in range(parent_modulus):
        result[residue] = sum(
            (
                child[residue + copy_index * parent_modulus]
                for copy_index in range(new_prime)
                if survives_new_prime(residue + copy_index * parent_modulus, new_prime)
            ),
            Fraction(),
        ) / new_prime
    return result


def algebraic_pullback(child_row: list[Fraction], parent_modulus: int, new_prime: int) -> list[Fraction]:
    require(len(child_row) == parent_modulus * new_prime, "pullback dimension mismatch")
    result = [Fraction() for _ in range(parent_modulus)]
    for residue in range(parent_modulus):
        result[residue] = sum(
            (
                child_row[residue + copy_index * parent_modulus]
                for copy_index in range(new_prime)
                if survives_new_prime(residue + copy_index * parent_modulus, new_prime)
            ),
            Fraction(),
        )
    return result


def forcing(parent_modulus: int, new_prime: int) -> list[Fraction]:
    alpha = Fraction(new_prime - 2, new_prime)
    lifted_one = replication_deletion([Fraction(1)] * parent_modulus, new_prime)
    return [value - alpha for value in lifted_one]


def exact_rank(matrix: list[list[int | Fraction]]) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(width > 0 and all(len(row) == width for row in matrix), "ragged matrix")
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def pulled_interval_row(base_stage: int, source_stage: int, scale: int) -> dict[int, int]:
    require(base_stage <= source_stage, "wrong pullback direction")
    base_modulus = primorial(base_stage)
    intervening_primes = PRIMES[base_stage:source_stage]
    result: dict[int, int] = {}
    for integer in range(scale + 1, 2 * scale + 1):
        if all(survives_new_prime(integer, prime) for prime in intervening_primes):
            residue = integer % base_modulus
            result[residue] = result.get(residue, 0) + 1
    return {residue: value for residue, value in result.items() if value}


def pulled_increment(base_stage: int, source_stage: int, scale: int) -> dict[int, int]:
    base_modulus = primorial(base_stage)
    intervening_primes = PRIMES[base_stage:source_stage]
    result: dict[int, int] = {}
    for integer, sign in ((scale, -1), (2 * scale - 1, 1), (2 * scale, 1)):
        if all(survives_new_prime(integer, prime) for prime in intervening_primes):
            residue = integer % base_modulus
            result[residue] = result.get(residue, 0) + sign
    return {residue: value for residue, value in result.items() if value}


def sparse_difference(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    keys = set(left) | set(right)
    return {
        key: left.get(key, 0) - right.get(key, 0)
        for key in keys
        if left.get(key, 0) != right.get(key, 0)
    }


def interval_rows(base_stage: int, terminal_stage: int) -> list[dict[int, int]]:
    rows: list[dict[int, int]] = []
    for source_stage in range(base_stage, terminal_stage + 1):
        lower, upper, _ = stage_band(source_stage)
        for scale in range(lower, upper + 1):
            rows.append(pulled_interval_row(base_stage, source_stage, scale))
    return rows


def sparse_rows_rank(rows: list[dict[int, int]], modulus: int) -> tuple[int, set[int]]:
    support = set().union(*(set(row) for row in rows)) if rows else set()
    columns = sorted(support)
    matrix = [[row.get(column, 0) for column in columns] for row in rows]
    return exact_rank(matrix), support


def core_hull_fixture(base_stage: int, terminal_stage: int) -> dict[str, int | str]:
    modulus = primorial(base_stage)
    rows = interval_rows(base_stage, terminal_stage)
    interval_rank, support = sparse_rows_rank(rows, modulus)
    if len(support) < modulus:
        hull_rank = interval_rank + 1
    else:
        dense = [[row.get(column, 0) for column in range(modulus)] for row in rows]
        dense.append([1] * modulus)
        hull_rank = exact_rank(dense)
    return {
        "base_stage": base_stage,
        "terminal_stage": terminal_stage,
        "depth": terminal_stage - base_stage,
        "primorial": modulus,
        "rows_including_mean": len(rows) + 1,
        "interval_rank": interval_rank,
        "core_hull_rank": hull_rank,
        "support_size": len(support),
    }


def incoming_forcing_augmented_rank(base_stage: int, terminal_stage: int) -> int:
    modulus = primorial(base_stage)
    rows = interval_rows(base_stage, terminal_stage)
    if modulus <= 210:
        dense = [[Fraction(row.get(column, 0)) for column in range(modulus)] for row in rows]
        dense.append([Fraction(1)] * modulus)
        if base_stage >= 2:
            dense.append(forcing(primorial(base_stage - 1), PRIMES[base_stage - 1]))
        return exact_rank(dense)

    interval_rank, support = sparse_rows_rank(rows, modulus)
    outside = [column for column in range(modulus) if column not in support]
    require(len(outside) >= 2, "large fixture lacks outside witnesses")
    incoming = forcing(primorial(base_stage - 1), PRIMES[base_stage - 1])
    witness_pair = next(
        (
            (left, right)
            for left in outside
            for right in outside
            if incoming[left] != incoming[right]
        ),
        None,
    )
    require(witness_pair is not None, "incoming forcing did not separate outside support")
    return interval_rank + 2


def adjoint_fixtures() -> list[dict[str, int | str]]:
    output: list[dict[str, int | str]] = []
    for parent_modulus, new_prime in ((2, 3), (6, 5), (30, 7), (210, 11)):
        child_modulus = parent_modulus * new_prime
        alpha = Fraction(new_prime - 2, new_prime)
        child_one = [Fraction(1)] * child_modulus
        require(
            haar_adjoint(child_one, parent_modulus, new_prime)
            == [alpha] * parent_modulus,
            "mean adjoint failed",
        )
        g = forcing(parent_modulus, new_prime)
        require(
            haar_adjoint(g, parent_modulus, new_prime)
            == [alpha * (1 - alpha)] * parent_modulus,
            "forcing did not collapse to mean",
        )
        for child_residue in range(child_modulus):
            atom = [Fraction()] * child_modulus
            atom[child_residue] = Fraction(1)
            expected = [Fraction()] * parent_modulus
            if survives_new_prime(child_residue, new_prime):
                expected[child_residue % parent_modulus] = Fraction(1, new_prime)
            require(
                haar_adjoint(atom, parent_modulus, new_prime) == expected,
                "atom adjoint failed",
            )
        sample = [Fraction((index * index + 3 * index + 1) % 17) for index in range(child_modulus)]
        raw = algebraic_pullback(sample, parent_modulus, new_prime)
        hilbert = haar_adjoint(sample, parent_modulus, new_prime)
        require(raw == [new_prime * value for value in hilbert], "Riesz scale failed")
        output.append(
            {
                "parent_modulus": parent_modulus,
                "new_prime": new_prime,
                "alpha": f"{alpha.numerator}/{alpha.denominator}",
                "survivor_children_per_parent": new_prime - 2,
            }
        )
    return output


def increment_histograms() -> dict[str, dict[str, int]]:
    expected = {
        2: {0: 33, 1: 62, 2: 31, 3: 9},
        3: {0: 10, 1: 33, 2: 55, 3: 30},
        4: {0: 2, 1: 14, 2: 36, 3: 65},
        5: {0: 0, 1: 5, 2: 19, 3: 58},
        6: {0: 0, 1: 0, 2: 0, 3: 59},
    }
    output: dict[str, dict[str, int]] = {}
    for base_stage in range(2, 7):
        histogram = {0: 0, 1: 0, 2: 0, 3: 0}
        increments = 0
        for source_stage in range(base_stage, 7):
            lower, upper, _ = stage_band(source_stage)
            for scale in range(lower + 1, upper + 1):
                direct = pulled_increment(base_stage, source_stage, scale)
                difference = sparse_difference(
                    pulled_interval_row(base_stage, source_stage, scale),
                    pulled_interval_row(base_stage, source_stage, scale - 1),
                )
                require(direct == difference, "pulled increment identity failed")
                require(len(direct) <= 3, "backward increment expanded")
                histogram[len(direct)] += 1
                increments += 1
        require(histogram == expected[base_stage], "increment histogram changed")
        output[f"k{base_stage}"] = {
            "increments": increments,
            "support_0": histogram[0],
            "support_1": histogram[1],
            "support_2": histogram[2],
            "support_3": histogram[3],
        }
    return output


def deletion_weight_row(stage: int, scale: int, next_prime: int) -> list[Fraction]:
    modulus = primorial(stage)
    row = [Fraction() for _ in range(modulus)]
    for integer in range(scale + 1, 2 * scale + 1):
        deleted = int(not survives_new_prime(integer, next_prime))
        row[integer % modulus] += Fraction(deleted) - Fraction(2, next_prime)
    return row


def interval_row(stage: int, scale: int) -> list[Fraction]:
    modulus = primorial(stage)
    row = [Fraction() for _ in range(modulus)]
    for integer in range(scale + 1, 2 * scale + 1):
        row[integer % modulus] += 1
    return row


def deletion_aggregate_fixtures() -> list[dict[str, int]]:
    fixtures: list[dict[str, int]] = []
    for stage, scales in ((4, (24, 37, 59)), (5, (60, 71, 83))):
        next_prime = PRIMES[stage]
        alpha = Fraction(next_prime - 2, next_prime)
        for scale in scales:
            current = interval_row(stage, scale)
            pulled = pulled_interval_row(stage, stage + 1, scale)
            pulled_dense = [Fraction(pulled.get(index, 0)) for index in range(primorial(stage))]
            derived = [alpha * left - right for left, right in zip(current, pulled_dense)]
            require(
                derived == deletion_weight_row(stage, scale, next_prime),
                "deletion aggregate adjacent-stage identity failed",
            )
            fixtures.append({"stage": stage, "scale": scale, "next_prime": next_prime})

    for prime in (5, 7, 11, 13):
        for residue in range(prime):
            coefficients = [Fraction() for _ in range(prime)]
            for frequency in range(1, prime):
                coefficients[(frequency * residue) % prime] += Fraction(1, prime)
                coefficients[(frequency * (residue + 2)) % prime] += Fraction(1, prime)
            deleted = int(residue in (0, prime - 2))
            target = [Fraction()] * prime
            target[0] = Fraction(deleted) - Fraction(2, prime)
            difference = [left - right for left, right in zip(coefficients, target)]
            require(
                all(value == difference[0] for value in difference),
                "cyclotomic deletion Fourier identity failed",
            )
    return fixtures


def windowed_bank_fixtures() -> list[dict[str, int]]:
    output: list[dict[str, int]] = []
    for stage in range(4, 7):
        lower, upper, band_count = stage_band(stage)
        next_prime = PRIMES[stage]

        def sliced_row(scale: int, residue_class: int) -> dict[int, int]:
            row: dict[int, int] = {}
            for integer in range(scale + 1, 2 * scale + 1):
                if integer % next_prime == residue_class:
                    row[integer] = 1
            return row

        for scale in range(lower + 1, upper + 1):
            for residue_class in range(next_prime):
                direct: dict[int, int] = {}
                for integer, sign in ((scale, -1), (2 * scale - 1, 1), (2 * scale, 1)):
                    if integer % next_prime == residue_class:
                        direct[integer] = direct.get(integer, 0) + sign
                direct = {key: value for key, value in direct.items() if value}
                difference = sparse_difference(
                    sliced_row(scale, residue_class),
                    sliced_row(scale - 1, residue_class),
                )
                require(direct == difference, "windowed Fourier slice identity failed")
                require(len(direct) <= 3, "windowed Fourier slice difference expanded")
        generator_upper_bound = next_prime + 3 * (band_count - 1)
        require(generator_upper_bound < primorial(stage), "finite bank lost subprimorial control")
        output.append(
            {
                "stage": stage,
                "next_prime": next_prime,
                "band_count": band_count,
                "generator_upper_bound": generator_upper_bound,
                "primorial": primorial(stage),
            }
        )
    return output


def canonical_contract() -> dict[str, object]:
    return {
        "representation": "COVECTOR_COORDINATE_SUM",
        "forcing_kind": "PRIMAL_FORCING",
        "individual_modes_canonical": False,
        "universal_typeii_attached": False,
        "packet_aux_modulus_as_deletion_prime": False,
        "nonzero_err_treated_as_exact": False,
        "pbapt_attachment": False,
        "pbapt_row_registry": (),
        "pbapt_source_locator": None,
        "complete_declared_family": False,
        "complete_hull_rank": None,
        "tpc_207_trigger": False,
    }


def validate_contract(contract: dict[str, object]) -> None:
    require(type(contract) is dict, "contract is not a literal dictionary")
    require(set(contract) == CONTRACT_KEYS, "contract field set is incomplete or enlarged")
    require(
        type(contract["representation"]) is str
        and contract["representation"] == "COVECTOR_COORDINATE_SUM",
        "untyped or noncanonical dual representation",
    )
    require(
        type(contract["forcing_kind"]) is str
        and contract["forcing_kind"] == "PRIMAL_FORCING",
        "forcing promoted to dual",
    )
    for field in FALSE_CONTRACT_FIELDS:
        require(type(contract[field]) is bool, f"{field} is not a literal bool")
        require(contract[field] is False, f"forbidden current-state promotion: {field}")
    require(
        type(contract["pbapt_row_registry"]) is tuple
        and len(contract["pbapt_row_registry"]) == 0,
        "PBAPT row registry is not the source-locked empty tuple",
    )
    require(
        contract["pbapt_source_locator"] is None,
        "PBAPT source locator claimed without a materialized row registry",
    )
    require(
        contract["complete_hull_rank"] is None,
        "untyped family claimed a complete hull rank",
    )


def validate_registry_semantics(
    registry: dict[str, str], contract: dict[str, object]
) -> None:
    validate_contract(contract)
    require(type(registry) is dict, "registry is not a literal dictionary")
    require(len(registry) == 32, "canonical registry row count changed")
    require(all(type(key) is str for key in registry), "registry has a non-string key")
    require(all(type(value) is str for value in registry.values()), "registry has a non-string value")
    semantic_locks = {
        "BRIDGE_B_ADJOINT_ATOM_PULLBACK": "PROVED_EXACT_SURVIVOR_COLLAPSE",
        "BRIDGE_B_ALGEBRAIC_DUAL_PULLBACK": "PROVED_EXACT",
        "BRIDGE_B_ALL_GLOBAL_CHARACTERS": "STOP_SCOPED_FULL_PRIMORIAL_RANK",
        "BRIDGE_B_ARITHMETIC_ADVANCE": "NO",
        "BRIDGE_B_BACKWARD_INCREMENT_SUPPORT": "PROVED_EXACT_AT_MOST_THREE",
        "BRIDGE_B_BASE_INCOMING_FORCING": "PRIMAL_VECTOR_NOT_CANONICAL_DUAL",
        "BRIDGE_B_COMPLETE_DECLARED_DUAL_FAMILY": "NOT_TYPED",
        "BRIDGE_B_COMPLETE_HULL_RANK": "NOT_TESTABLE_FAIL_CLOSED",
        "BRIDGE_B_CORE_DUAL_FAMILY": "CANONICAL_MEAN_PLUS_ACTUAL_INTERVALS",
        "BRIDGE_B_CORE_HULL_ASYMPTOTIC": "OPEN_NO_UNIFORM_HORIZON_THEOREM",
        "BRIDGE_B_CORE_HULL_K4_B6": "PROVED_EXACT_RANK_119_OF_210",
        "BRIDGE_B_CORE_HULL_K5_B6": "PROVED_EXACT_RANK_85_OF_2310",
        "BRIDGE_B_CORE_HULL_K6_B6": "PROVED_EXACT_RANK_61_OF_30030",
        "BRIDGE_B_DELETION_INNOVATION_ACTIVE_REGISTRY": "ABSENT",
        "BRIDGE_B_DELETION_INNOVATION_AGGREGATE": "PROVED_EXACT_FORMULA",
        "BRIDGE_B_FIXED_HORIZON_WINDOWED_SUPPORT": "PROVED_O_H_LOWERCASE_P_K_SQUARED_AND_O_PRIMORIAL",
        "BRIDGE_B_HAAR_ADJOINT": "PROVED_EXACT_P_INVERSE_AVERAGE",
        "BRIDGE_B_INDIVIDUAL_DELETION_MODES": "CONDITIONAL_NOT_CANONICAL_FAMILY",
        "BRIDGE_B_LATER_DELETION_FORCING_PULLBACK": "PROVED_EXACT_SCALAR_MEAN",
        "BRIDGE_B_MAXIMAL_WINDOWED_FOURIER_BANK": "CONDITIONAL_RANK_AT_MOST_Q_PLUS_3_BANDCOUNT_MINUS_3",
        "BRIDGE_B_NONZERO_ERR_HULL_RANK": "DIAGNOSTIC_ONLY_NOT_NECESSARY_OBSTRUCTION",
        "BRIDGE_B_PBAPT_TYPEII_PRIMORIAL_CROSSWALK": "ABSENT",
        "BRIDGE_B_RIESZ_SCALING": "PROVED_EXACT_SOURCE_OVER_TARGET_MODULUS",
        "BRIDGE_B_SHB_D2_TYPEII_ROWS": "OPEN_MATERIALIZATION_GATE",
        "BRIDGE_B_TPC32_PACKET_TO_PRIMORIAL_DUAL": "ABSENT",
        "BRIDGE_B_TYPED_WINDOWED_FORCED_INNOVATION": "SELECTED_OPEN_NEW_THEOREM",
        "BRIDGE_B_UNTYPED_PLACEHOLDER_TO_COMPLETE_HULL": "STOP_SCOPED_FAIL_CLOSED",
        "BRIDGE_B_ZERO_DEFECT_HULL_RANK": "VALID_NECESSARY_OBSTRUCTION",
        "FIXED_ATOM_CREDIT": "0",
        "L2": "NONE",
        "STRICT_1_OVER_400": "UNPAID",
        "TPC_207_TRIGGER": "false",
    }
    require(set(registry) == set(semantic_locks), "registry exact key set changed")
    for key, expected in semantic_locks.items():
        require(registry.get(key) == expected, f"registry semantic promotion: {key}")
    require(contract["pbapt_attachment"] is False, "contract/registry PBAPT mismatch")
    require(contract["complete_declared_family"] is False, "contract/registry family mismatch")
    require(contract["complete_hull_rank"] is None, "contract/registry rank mismatch")
    require(contract["tpc_207_trigger"] is False, "contract/registry TPC-207 mismatch")


def validate_registry_bundle(
    registry: dict[str, str], expected_digest: str, contract: dict[str, object]
) -> None:
    require(type(expected_digest) is str, "registry digest is not a string")
    require(expected_digest != "TO_BE_FILLED", "registry hash is not frozen")
    require(registry_sha256(registry) == expected_digest, "canonical V18 registry hash mismatch")
    validate_registry_semantics(registry, contract)


def schema_mutations() -> dict[str, str]:
    base = canonical_contract()
    validate_contract(base)
    mutations = {
        "missing_riesz_type": ({"representation": "ALGEBRAIC_EQUALS_HAAR"}, None),
        "forcing_promoted_to_dual": ({"forcing_kind": "DUAL_ROW"}, None),
        "aggregate_expanded_to_all_modes": ({"individual_modes_canonical": True}, None),
        "universal_typeii_reintroduced": ({"universal_typeii_attached": True}, None),
        "packet_aux_modulus_conflated": ({"packet_aux_modulus_as_deletion_prime": True}, None),
        "nonzero_err_claimed_exact": ({"nonzero_err_treated_as_exact": True}, None),
        "empty_pbapt_claimed_attached": ({"pbapt_attachment": True}, None),
        "empty_pbapt_claimed_complete": ({"complete_declared_family": True}, None),
        "incomplete_family_claimed_rank": ({"complete_hull_rank": 1}, None),
        "incomplete_family_bool_rank": ({"complete_hull_rank": True}, None),
        "tpc_207_flip": ({"tpc_207_trigger": True}, None),
        "required_field_omitted": ({}, "individual_modes_canonical"),
        "unknown_field_injected": ({"unknown_claim": True}, None),
        "individual_modes_zero": ({"individual_modes_canonical": 0}, None),
        "universal_typeii_empty_string": ({"universal_typeii_attached": ""}, None),
        "packet_aux_empty_list": ({"packet_aux_modulus_as_deletion_prime": []}, None),
        "nonzero_err_none": ({"nonzero_err_treated_as_exact": None}, None),
        "pbapt_attachment_zero": ({"pbapt_attachment": 0}, None),
        "complete_family_empty_string": ({"complete_declared_family": ""}, None),
        "tpc_trigger_none": ({"tpc_207_trigger": None}, None),
        "pbapt_registry_without_source": ({"pbapt_row_registry": ({"id": "fake"},)}, None),
        "pbapt_source_without_registry": ({"pbapt_source_locator": "fake:1"}, None),
        "coordinated_empty_pbapt_positive_rank": (
            {"pbapt_attachment": True, "complete_declared_family": True, "complete_hull_rank": 1},
            None,
        ),
        "coordinated_empty_pbapt_negative_rank": (
            {"pbapt_attachment": True, "complete_declared_family": True, "complete_hull_rank": -7},
            None,
        ),
    }
    detected: dict[str, str] = {}
    for label, (change, delete_key) in mutations.items():
        mutated = copy.deepcopy(base)
        mutated.update(change)
        if delete_key is not None:
            del mutated[delete_key]
        try:
            validate_contract(mutated)
        except AssertionError:
            detected[label] = "DETECTED"
        else:
            raise AssertionError(f"schema mutation escaped: {label}")
    return detected


def registry_semantic_mutations() -> dict[str, str]:
    contract = canonical_contract()
    mutations: dict[str, tuple[dict[str, str], str | None]] = {}
    for index, key in enumerate(sorted(REGISTRY), start=1):
        mutations[f"row_{index:02d}_semantic_rewrite"] = (
            {key: f"MUTATED_FALSE_PROMOTION_{index:02d}"},
            None,
        )
    first_key = sorted(REGISTRY)[0]
    mutations["unknown_key_replacement_with_rehash"] = (
        {"UNKNOWN_REPLACEMENT_ROW": REGISTRY[first_key]},
        first_key,
    )
    mutations["coordinated_false_release_with_rehash"] = (
        {
            "BRIDGE_B_ARITHMETIC_ADVANCE": "YES_FALSE_PROMOTION",
            "BRIDGE_B_COMPLETE_HULL_RANK": "PROVED_FAKE_RANK_1",
            "TPC_207_TRIGGER": "true",
        },
        None,
    )
    detected: dict[str, str] = {}
    for label, (changes, delete_key) in mutations.items():
        mutated = copy.deepcopy(REGISTRY)
        mutated.update(changes)
        if delete_key is not None:
            del mutated[delete_key]
        coordinated_digest = registry_sha256(mutated)
        try:
            validate_registry_bundle(mutated, coordinated_digest, contract)
        except AssertionError:
            detected[label] = "DETECTED"
        else:
            raise AssertionError(f"registry semantic mutation escaped: {label}")
    return detected


def run_check() -> dict[str, object]:
    digest = registry_sha256(REGISTRY)
    contract = canonical_contract()
    validate_registry_bundle(REGISTRY, EXPECTED_REGISTRY_SHA256, contract)

    expected_core = {
        (2, 2): (9, 5, 5),
        (2, 3): (21, 6, 6),
        (2, 4): (57, 6, 6),
        (2, 5): (81, 6, 6),
        (2, 6): (141, 6, 6),
        (3, 3): (13, 13, 14),
        (3, 4): (49, 30, 30),
        (3, 5): (73, 30, 30),
        (3, 6): (133, 30, 30),
        (4, 4): (37, 37, 38),
        (4, 5): (61, 61, 62),
        (4, 6): (121, 119, 120),
        (5, 5): (25, 25, 26),
        (5, 6): (85, 85, 86),
        (6, 6): (61, 61, 62),
    }
    core_fixtures: list[dict[str, int | str]] = []
    for key, expected in expected_core.items():
        fixture = core_hull_fixture(*key)
        incoming_rank = incoming_forcing_augmented_rank(*key)
        require(
            (
                fixture["rows_including_mean"],
                fixture["core_hull_rank"],
                incoming_rank,
            )
            == expected,
            f"core hull fixture changed: {key}",
        )
        fixture["incoming_forcing_augmented_rank"] = incoming_rank
        core_fixtures.append(fixture)

    u103 = pulled_interval_row(4, 6, 103)
    u104 = pulled_interval_row(4, 6, 104)
    u109 = pulled_interval_row(4, 6, 109)
    u110 = pulled_interval_row(4, 6, 110)
    require(u103 == u104 and u109 == u110, "literal zero-increment relations changed")

    return {
        "status": "PASS",
        "claim_level": "EXACT_TYPED_CORE_BACKWARD_HULL_NO_ARITHMETIC_ADVANCE",
        "adjoint_fixtures": adjoint_fixtures(),
        "core_hull_fixtures": core_fixtures,
        "increment_histograms": increment_histograms(),
        "literal_zero_increment_relations": ["u_103=u_104", "u_109=u_110"],
        "deletion_aggregate_fixtures": deletion_aggregate_fixtures(),
        "conditional_windowed_bank_fixtures": windowed_bank_fixtures(),
        "schema_mutations": schema_mutations(),
        "registry_semantic_mutations": registry_semantic_mutations(),
        "pbapt_attachment": contract["pbapt_attachment"],
        "pbapt_row_registry_count": len(contract["pbapt_row_registry"]),
        "pbapt_source_locator": contract["pbapt_source_locator"],
        "complete_declared_family": contract["complete_declared_family"],
        "complete_hull_rank": contract["complete_hull_rank"],
        "registry_rows": len(REGISTRY),
        "registry_sha256": digest,
        "arithmetic_advance": False,
        "tpc_207_trigger": contract["tpc_207_trigger"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="run exact read-only checks")
    mode.add_argument(
        "--registry-hash", action="store_true", help="print the canonical registry hash"
    )
    args = parser.parse_args()
    if args.registry_hash:
        print(registry_sha256(REGISTRY))
        return 0
    print(json.dumps(run_check(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
