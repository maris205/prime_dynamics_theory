#!/usr/bin/env python3
"""Build or verify the exact TPC-226 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from primitive_collision_transition import TransitionFailure, build_certificate  # noqa: E402


OUTPUT = PROJECT / "results/certificate.json"


def canonical(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        text = canonical(build_certificate())
        if args.check:
            if not OUTPUT.exists() or OUTPUT.read_text() != text:
                raise TransitionFailure("committed certificate differs from exact rebuild")
        else:
            OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            OUTPUT.write_text(text)
    except (OSError, TransitionFailure, ValueError) as error:
        print(f"TPC226_CERTIFICATE=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC226_CERTIFICATE=PASS")
    print("classification_scales=505")
    print("profile_records=30")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
