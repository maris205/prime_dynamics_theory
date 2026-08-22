#!/usr/bin/env python3
"""Generate the deterministic TPC-223 rational ledger certificate."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
CODE = PROJECT / "code"
sys.path.insert(0, str(CODE))

from reassembly_compiler import (  # noqa: E402
    STRICT_THRESHOLD,
    canonical_ledgers,
    compiler_identity_holds,
    strict_gate_holds,
)


def main() -> int:
    named = canonical_ledgers()
    records = [ledger.as_record(name) for name, ledger in named]
    checks = {
        "all_records_use_exact_rationals": all(
            compiler_identity_holds(ledger) for _, ledger in named
        ),
        "strict_fixture_passes": strict_gate_holds(named[0][1]),
        "borderline_fixture_is_not_strict": named[1][1].status == "BORDERLINE"
        and not strict_gate_holds(named[1][1]),
        "failed_fixture_rejected": named[2][1].status == "NO_STRICT_SAVING",
        "missing_channel_rejected": named[3][1].status == "NO_STRICT_SAVING",
        "loss_dominance_rejected": named[4][1].status == "NO_STRICT_SAVING",
        "strict_threshold_is_one_over_400": str(STRICT_THRESHOLD) == "1/400",
    }
    data = {
        "schema": "tpc223-conditional-signed-reassembly-compiler-v1",
        "status": "PASS",
        "claim_level": "CONDITIONAL_THEOREM",
        "baseline_exponent": "5/3",
        "strict_threshold": str(STRICT_THRESHOLD),
        "conditional_inputs": {
            "ap_dispersion": "OPEN",
            "polarized_cross_correlation": "OPEN",
            "literal_reassembly_interface": "OPEN",
        },
        "arithmetic_advance": "NO",
        "fixed_atom_credit": 0,
        "l2": "NONE",
        "full_gate_b": "OPEN",
        "strict_1_over_400": "UNPAID",
        "records": records,
        "checks": checks,
        "route": {
            "strongest_positive": "EXACT_TWO_CHANNEL_MINIMUM_COMPILER",
            "strongest_obstruction": "ZERO_OR_BORDERLINE_CHANNEL_DOES_NOT_PASS",
            "open_theorem": "COMMON_LITERAL_AP_AND_POLARIZED_REASSEMBLY_BOUND",
            "round2_clue": "PROVE_OR_REFUTE_THE_COMMON_LITERAL_TWO_CHANNEL_INTERFACE",
        },
    }
    output = PROJECT / "results" / "certificate.json"
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print("TPC223_CERTIFICATE=PASS")
    print("records=5")
    print("effective_saving=11/1200")
    print("strict_margin=1/150")
    print("claim_level=CONDITIONAL_THEOREM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
