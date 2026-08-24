#!/usr/bin/env python3
"""Write or check the deterministic TPC-232 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from growing_resonance_depth import build_certificate  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = PROJECT / "results" / "certificate.json"
    payload = build_certificate()
    encoded = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(encoded, encoding="utf-8", newline="\n")
        print("TPC232_CERTIFICATE=WRITTEN")
        return 0
    if not target.is_file() or target.read_text(encoding="utf-8") != encoded:
        print("TPC232_CERTIFICATE=FAIL", file=sys.stderr)
        return 1
    print("TPC232_CERTIFICATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
