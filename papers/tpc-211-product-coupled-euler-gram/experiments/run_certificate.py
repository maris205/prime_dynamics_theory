#!/usr/bin/env python3
"""Produce or verify the exact TPC-211 finite certificate."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from product_coupled import finite_case  # noqa: E402


CERTIFICATE = PROJECT / "results" / "certificate.json"
CASES = ((5, 7), (5, 7, 11), (5, 7, 11, 13))
CUTOFF = 3


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
    records = {
        "-".join(str(prime) for prime in primes): finite_case(primes, CUTOFF)
        for primes in CASES
    }
    return {
        "schema": "TPC211_PRODUCT_COUPLED_EULER_GRAM_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING",
        "cutoff": CUTOFF,
        "cases": records,
        "theorem_contract": {
            "local_profile_family": "DELTA_S=P_S-B_S_FROM_LITERAL_V46_EULER_FACTORS",
            "full_divisor_rank": "PROVED_EXACT_FOR_ALL_ACTIVE_PRIME_SETS",
            "logarithmic_mobius_packet": "PROVED_EXACT_MARKED_PRIME_DERIVATIVE",
            "shared_endpoint_alignment": "PROVED_EXACT_FINITE_SURROGATE",
            "incomplete_transition_packet": "OPEN_BOUNDARY_REMAINDER",
            "actual_tpc_arithmetic_saving": "OPEN",
        },
        "audit_counts": {
            "prime_set_rows": len(CASES),
            "profile_rows": sum((1 << len(primes)) - 1 for primes in CASES),
            "crt_residue_rows": sum(
                math.prod(primes) * ((1 << len(primes)) - 1) for primes in CASES
            ),
            "derivative_rows": sum(len(primes) for primes in CASES),
        },
        "claim_firewall": {
            "product_coupling_identities": "PROVED_EXACT",
            "literal_product_profile_full_rank": "PROVED_EXACT",
            "complete_packet_derivative_compression": "PROVED_EXACT",
            "shared_endpoint_alignment": "PROVED_STRUCTURAL_FINITE",
            "product_coupling_universal_saving": "REFUTED_SCOPED",
            "transition_boundary_control": "OPEN",
            "physical_tpc_cross_divisor_gram_bound": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        },
        "open_theorem": (
            "CONTROL_THE_TRUNCATED_LITERAL_TRANSITION_PACKET_AFTER_THE_"
            "COMPLETE_DIVISOR_DERIVATIVE_AND_RECIPROCAL_EMITTER"
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
        print("TPC211_CERTIFICATE_WRITE=PASS")
        print("schema=TPC211_PRODUCT_COUPLED_EULER_GRAM_CERTIFICATE_V1")
        return 0

    if not CERTIFICATE.is_file():
        print("TPC211_CERTIFICATE_CHECK=FAIL missing certificate", file=sys.stderr)
        return 1
    actual = CERTIFICATE.read_text(encoding="utf-8")
    parsed = json.loads(
        actual,
        object_pairs_hook=no_duplicate_object,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
    )
    reject_nonfinite(parsed)
    if actual != expected:
        print("TPC211_CERTIFICATE_CHECK=FAIL stale or noncanonical", file=sys.stderr)
        return 1
    print("TPC211_CERTIFICATE_CHECK=PASS")
    print(f"prime_set_rows={len(CASES)}")
    print(f"profile_rows={sum((1 << len(primes)) - 1 for primes in CASES)}")
    print("claim_level=PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
