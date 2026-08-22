#!/usr/bin/env python3
"""Produce or read-only check the TPC-219 exact certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from longitudinal_transverse import build_certificate  # noqa: E402


OUT = ROOT / "results" / "certificate.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_certificate()
    if args.check:
        observed = json.loads(OUT.read_text())
        if observed != expected:
            raise SystemExit("TPC219 certificate mismatch")
        print("TPC219_CERTIFICATE=PASS")
        return 0
    OUT.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    print("TPC219_CERTIFICATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
