#!/usr/bin/env python3
"""Exact finite provenance tests for the TPC-119 H8 certificate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


ATOMS = ("a0", "a1", "a2")
CANONICAL = {
    ("a0", "main"): Fraction(1, 3),
    ("a0", "tail"): Fraction(2, 3),
    ("a1", "main"): Fraction(1),
    ("a2", "main"): Fraction(1, 2),
    ("a2", "soft"): Fraction(1, 2),
}
COEFFICIENT = {
    "a0": Fraction(6),
    "a1": Fraction(-5),
    "a2": Fraction(8),
}


def column_sums(records: dict[tuple[str, str], Fraction]) -> dict[str, Fraction]:
    return {
        atom: sum(
            (weight for (source, _), weight in records.items() if source == atom),
            Fraction(0),
        )
        for atom in ATOMS
    }


def scalar(records: dict[tuple[str, str], Fraction]) -> Fraction:
    return sum(
        (weight * COEFFICIENT[source] for (source, _), weight in records.items()),
        Fraction(0),
    )


def canonical_pass(
    records: dict[tuple[str, str], Fraction],
    shifts: dict[tuple[str, str], int],
    normalizations: dict[tuple[str, str], Fraction],
) -> bool:
    return (
        records == CANONICAL
        and column_sums(records) == {atom: Fraction(1) for atom in ATOMS}
        and set(shifts) == set(CANONICAL)
        and all(value == 6 for value in shifts.values())
        and set(normalizations) == set(CANONICAL)
        and all(value == 1 for value in normalizations.values())
    )


def certificate() -> dict:
    checks = 0
    shifts = {leaf: 6 for leaf in CANONICAL}
    norms = {leaf: Fraction(1) for leaf in CANONICAL}

    assert canonical_pass(CANONICAL, shifts, norms)
    checks += 1
    assert scalar(CANONICAL) == sum(COEFFICIENT.values())
    checks += 1

    deleted = dict(CANONICAL)
    deleted.pop(("a2", "soft"))
    assert not canonical_pass(deleted, {k: 6 for k in deleted}, {k: Fraction(1) for k in deleted})
    checks += 1

    rescaled = {key: 2 * value for key, value in CANONICAL.items()}
    assert not canonical_pass(rescaled, shifts, norms)
    checks += 1

    wrong_shift = dict(shifts)
    wrong_shift[("a0", "tail")] = 2
    assert not canonical_pass(CANONICAL, wrong_shift, norms)
    checks += 1

    wrong_norm = dict(norms)
    wrong_norm[("a1", "main")] = Fraction(3, 2)
    assert not canonical_pass(CANONICAL, shifts, wrong_norm)
    checks += 1

    # Scalar-preserving null-pair inflation is rejected by canonical equality.
    inflated = dict(CANONICAL)
    inflated[("a1", "null-plus")] = Fraction(7)
    inflated[("a1", "null-minus")] = Fraction(-7)
    assert scalar(inflated) == scalar(CANONICAL)
    checks += 1
    inflated_shifts = {key: 6 for key in inflated}
    inflated_norms = {key: Fraction(1) for key in inflated}
    assert not canonical_pass(inflated, inflated_shifts, inflated_norms)
    checks += 1

    # Equal-valued atoms cannot be exchanged when provenance is part of the key.
    equal_values = dict(COEFFICIENT)
    equal_values["a2"] = equal_values["a0"]
    surrogate = dict(CANONICAL)
    surrogate[("a0", "surrogate")] = surrogate.pop(("a2", "soft"))
    surrogate_scalar = sum(
        (weight * equal_values[source] for (source, _), weight in surrogate.items()),
        Fraction(0),
    )
    canonical_equal_scalar = sum(
        (weight * equal_values[source] for (source, _), weight in CANONICAL.items()),
        Fraction(0),
    )
    assert surrogate_scalar == canonical_equal_scalar
    checks += 1
    assert surrogate != CANONICAL
    checks += 1

    retained = {
        key: value for key, value in CANONICAL.items() if key[1] != "soft"
    }
    soft = {key: value for key, value in CANONICAL.items() if key[1] == "soft"}
    assert {
        key: retained.get(key, Fraction(0)) + soft.get(key, Fraction(0))
        for key in CANONICAL
    } == CANONICAL
    checks += 1
    assert scalar(retained) + scalar(soft) == scalar(CANONICAL)
    checks += 1

    return {
        "schema": "tpc119-hard-packet-reconnection-audit-v1",
        "status": "PASS",
        "assertions_checked": checks,
        "native_atoms": len(ATOMS),
        "canonical_leaves": len(CANONICAL),
        "column_sums": {
            atom: str(value) for atom, value in column_sums(CANONICAL).items()
        },
        "adversarial_cases": {
            "deletion_rejected": True,
            "global_rescaling_rejected": True,
            "wrong_fixed_shift_rejected": True,
            "second_normalization_rejected": True,
            "scalar_preserving_null_pair_rejected": True,
            "equal_value_surrogate_provenance_rejected": True,
        },
        "route_verdict": {
            "finite_certificate_theorem": "PROVED_L0",
            "tpc15_native_atom_anchor": "PROVED_L1",
            "full_composite_leaf_archive_present": False,
            "H8_canonical_leaf_audit": "NOT_TESTABLE_FROM_CURRENT_ARTIFACTS",
            "snapshot_date": "2026-07-26",
            "fixed_h0_L2_progress": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = certificate()
    target = Path(__file__).with_suffix(".json")
    if args.write:
        target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.check:
        expected = json.loads(target.read_text(encoding="utf-8"))
        if result != expected:
            raise SystemExit("certificate mismatch")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
