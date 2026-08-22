#!/usr/bin/env python3
"""Materialize or check the canonical TPC-218 finite certificate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from prime_shell_packet_lift import AuditFailure, build_fixture, canonical  # noqa: E402


CERTIFICATE = ROOT / "results/certificate.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        expected = canonical(build_fixture())
        if args.check:
            if not CERTIFICATE.is_file():
                raise AuditFailure("certificate missing")
            if CERTIFICATE.read_text(encoding="utf-8") != expected:
                raise AuditFailure("certificate is stale")
        else:
            CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
            CERTIFICATE.write_text(expected, encoding="utf-8")
    except (AuditFailure, OSError, ValueError, ZeroDivisionError) as error:
        print(f"TPC218_CERTIFICATE=FAIL {error}", file=sys.stderr)
        return 1
    data = build_fixture()
    finite = data["finite_fixture"]
    prime = data["prime_label_alignment"]
    packet = data["packet_alignment"]
    print("TPC218_CERTIFICATE=PASS")
    print("q_labels=", len(finite["q_values"]))
    print("reduced_denominators=", len(finite["reduced_denominators"]))
    print("split_normalized_exponent=1/96")
    print("prime_alignment_ratio=", prime["coherent_to_diagonal_ratio"])
    print("packet_projection_ratio=", packet["projection_to_total_ratio"])
    print("claim_level=PROVED_STRUCTURAL_L1_PRIME_LABEL_AND_PACKET_PRESERVING_LIFT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
