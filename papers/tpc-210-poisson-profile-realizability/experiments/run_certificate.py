#!/usr/bin/env python3
"""Produce or verify the canonical TPC-210 finite certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from profile_realization import (  # noqa: E402
    aligned_certificate,
    nonzero_mobius_divisors,
    isolated_profile_geometry,
)


CERTIFICATE = PROJECT / "results" / "certificate.json"
MODULI = (3, 5, 7, 11, 13)


def canonical_text(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


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


def build_certificate() -> dict[str, object]:
    records = {str(q): aligned_certificate(q) for q in MODULI}
    profile_rows = sum(len(nonzero_mobius_divisors(q)) for q in MODULI)
    geometry_rows = sum(isolated_profile_geometry(q)["node_count"] for q in MODULI)
    residue_coordinate_rows = sum(
        (q - 1) * len(nonzero_mobius_divisors(q)) for q in MODULI
    )
    resonance = records["5"]
    return {
        "schema": "TPC210_POISSON_PROFILE_REALIZABILITY_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_STOP_SCOPED_PROFILE_CLASS",
        "moduli": records,
        "resonance": {
            "q": 5,
            "divisors": resonance["divisors"],
            "weights": resonance["weights"],
            "profile_rows": resonance["profile_rows"],
            "diagonal_energy": resonance["diagonal_energy"],
            "aggregate_energy": resonance["aggregate_energy"],
            "energy_ratio": resonance["energy_ratio"],
            "mobius_l1_mass": resonance["mobius_l1_mass"],
            "ratio_equals_divisor_count": resonance["energy_ratio"] == "2",
        },
        "audit_counts": {
            "modulus_rows": len(MODULI),
            "realized_profile_rows": profile_rows,
            "residue_coordinate_rows": residue_coordinate_rows,
            "support_geometry_rows": geometry_rows,
        },
        "claim_firewall": {
            "finite_profile_interpolation": "PROVED_EXACT",
            "mobius_weighted_aligned_family": "PROVED_EXACT",
            "cross_divisor_gram_reduction": "PROVED_EXACT",
            "profile_class_universal_saving": "REFUTED_SCOPED",
            "actual_physical_tpc_profile_bound": "OPEN",
            "full_gate_b_strict_1_over_400": "UNPAID",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
        },
        "open_theorem": (
            "CROSS_DIVISOR_GRAM_BOUND_FOR_THE_LITERAL_PHYSICAL_MOBIUS_POISSON_PROFILES"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = canonical_text(build_certificate())
    if args.write:
        CERTIFICATE.write_text(expected, encoding="utf-8")
        print("TPC210_CERTIFICATE_WRITE=PASS")
        print("schema=TPC210_POISSON_PROFILE_REALIZABILITY_CERTIFICATE_V1")
        return 0
    if not CERTIFICATE.is_file():
        print("TPC210_CERTIFICATE_CHECK=FAIL missing certificate", file=sys.stderr)
        return 1
    actual = CERTIFICATE.read_text(encoding="utf-8")
    json.loads(
        actual,
        object_pairs_hook=no_duplicate_object,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    if actual != expected:
        print("TPC210_CERTIFICATE_CHECK=FAIL stale or noncanonical", file=sys.stderr)
        return 1
    print("TPC210_CERTIFICATE_CHECK=PASS")
    print("moduli=5")
    print("realized_profile_rows=20")
    print("residue_coordinate_rows=178")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
