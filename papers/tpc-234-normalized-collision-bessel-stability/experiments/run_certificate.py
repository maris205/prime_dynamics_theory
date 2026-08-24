#!/usr/bin/env python3
"""Write or check the deterministic TPC-234 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from normalized_collision import build_certificate  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "results" / "certificate.json"
    generated = build_certificate()
    if args.write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(generated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print("TPC234_CERTIFICATE=WRITTEN")
    elif args.check:
        if json.loads(target.read_text(encoding="utf-8")) != generated:
            raise SystemExit("TPC234 certificate mismatch")
        print("TPC234_CERTIFICATE=PASS")
    else:
        print(json.dumps(generated, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
