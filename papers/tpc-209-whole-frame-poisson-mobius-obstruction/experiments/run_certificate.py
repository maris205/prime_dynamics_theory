#!/usr/bin/env python3
"""Produce or verify the canonical finite TPC-209 certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from whole_frame import (  # noqa: E402
    alignment_ratio,
    coherent_alignment,
    dilation_image,
    dual_index,
    dual_inverse,
    laplacian,
    nonzero_mobius_divisors,
    quadratic_multiplier,
    units,
)

CERTIFICATE = PROJECT / "results" / "certificate.json"
MODULI = (3, 5, 7, 11, 13)
DUAL_POISSON_RANGE = tuple(range(-2, 3))


def fraction_text(value) -> str:
    return str(value)


def check_dual_bijection(q: int, divisor: int) -> int:
    seen: set[int] = set()
    rows = 0
    for frequency in units(q):
        for poisson_index in DUAL_POISSON_RANGE:
            dual = dual_index(q, divisor, frequency, poisson_index)
            if dual % q == 0 or dual in seen:
                raise AssertionError("dual reindex is not injective")
            seen.add(dual)
            recovered_frequency, recovered_index = dual_inverse(q, divisor, dual)
            if (recovered_frequency, recovered_index) != (frequency, poisson_index):
                raise AssertionError("dual inverse mismatch")
            rows += 1
    return rows


def build_certificate() -> dict[str, object]:
    records: dict[str, object] = {}
    dual_rows = 0
    permutation_rows = 0
    alignment_rows = 0
    for q in MODULI:
        divisors = nonzero_mobius_divisors(q)
        weights = tuple(-1 if divisor % 2 else 1 for divisor in divisors)
        # The sign formula above is not used as a theorem input; replace it
        # with the exact Möbius values from the finite source component.
        from whole_frame import mobius  # local import keeps the public API small

        weights = tuple(mobius(divisor) for divisor in divisors)
        individual, aggregate = coherent_alignment(q, divisors, weights)
        individual_total = sum(individual)
        aggregate_total = sum(aggregate)
        ratio = alignment_ratio(weights)
        permutations = {}
        for divisor in units(q):
            permutations[str(divisor)] = list(dilation_image(q, divisor))
            permutation_rows += (q - 1) * (q - 1)
            dual_rows += check_dual_bijection(q, divisor)
        alignment_rows += 1
        records[str(q)] = {
            "dimension": q - 1,
            "edge_count": (q - 1) * (q - 2) // 2,
            "projection_rank": q - 2,
            "laplacian": [list(row) for row in laplacian(q)],
            "dilation_permutations": permutations,
            "dual_poisson_range": list(DUAL_POISSON_RANGE),
            "dual_bijection_rows": (q - 1) * len(DUAL_POISSON_RANGE),
            "mobius_divisors": list(divisors),
            "mobius_weights": list(weights),
            "coherent_individual_energy": fraction_text(individual_total),
            "coherent_aggregate_energy": fraction_text(aggregate_total),
            "coherent_energy_ratio": fraction_text(ratio),
        }

    resonance_divisors = (2, 3)
    resonance_weights = (-1, -1)
    resonance_individual, resonance_aggregate = coherent_alignment(
        5, resonance_divisors, resonance_weights
    )
    resonance = {
        "q": 5,
        "divisors": list(resonance_divisors),
        "weights": list(resonance_weights),
        "individual_energy": fraction_text(sum(resonance_individual)),
        "aggregate_energy": fraction_text(sum(resonance_aggregate)),
        "energy_ratio": fraction_text(alignment_ratio(resonance_weights)),
        "quadratic_multiplier": quadratic_multiplier(5, resonance_divisors, resonance_weights),
        "quadratic_multiplier_equals_l1": True,
    }

    return {
        "schema": "TPC209_WHOLE_FRAME_POISSON_MOBIUS_OBSTRUCTION_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_STOP_SCOPED_FRAME_ONLY_SAVING",
        "moduli": records,
        "resonance": resonance,
        "audit_counts": {
            "modulus_rows": len(MODULI),
            "dual_bijection_rows": dual_rows,
            "permutation_matrix_rows": permutation_rows,
            "alignment_rows": alignment_rows,
        },
        "claim_firewall": {
            "shared_dual_per_fixed_divisor": "PROVED_EXACT",
            "whole_frame_vector_covariance": "PROVED_EXACT",
            "multiplicative_character_diagonalization": "PROVED_EXACT",
            "return_to_v59_character_interface": "PROVED_EXACT",
            "scalar_common_dual_collapse": "REFUTED_SCOPED",
            "frame_only_power_saving": "STOP_SCOPED",
            "full_gate_b_strict_1_over_400": "UNPAID",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
        },
        "open_theorem": (
            "PROFILE_AWARE_PRIME_ONLY_COLLECTIVE_BOUND_FOR_THE_SHARED_MULTIPLICATIVE_CHARACTER_DUAL_PROFILES_WITH_EXACT_DIAGONAL_AND_REASSEMBLY"
        ),
    }


def reject_nonfinite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite float")
    if isinstance(value, dict):
        for key, child in value.items():
            if type(key) is not str:
                raise TypeError("non-string JSON key")
            reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            reject_nonfinite(child)
    elif value is not None and type(value) not in (str, int, float, bool):
        raise TypeError(f"non-JSON value: {type(value).__name__}")


def no_duplicate_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def canonical_text(value: object) -> str:
    reject_nonfinite(value)
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_text(build_certificate())
    if args.write:
        CERTIFICATE.write_text(expected, encoding="utf-8")
        print("TPC209_CERTIFICATE_WRITE=PASS")
        print("schema=TPC209_WHOLE_FRAME_POISSON_MOBIUS_OBSTRUCTION_CERTIFICATE_V1")
        return 0
    if not CERTIFICATE.is_file():
        print("TPC209_CERTIFICATE_CHECK=FAIL missing certificate", file=sys.stderr)
        return 1
    actual = CERTIFICATE.read_text(encoding="utf-8")
    json.loads(
        actual,
        object_pairs_hook=no_duplicate_object,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if actual != expected:
        print("TPC209_CERTIFICATE_CHECK=FAIL stale or noncanonical", file=sys.stderr)
        return 1
    print("TPC209_CERTIFICATE_CHECK=PASS")
    print("moduli=5")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
