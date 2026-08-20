"""Produce or verify the canonical TPC-214 certificate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from shared_frequency_clusters import build_certificate, write_certificate  # noqa: E402


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = ROOT / "results/certificate.json"
    expected = build_certificate()
    if args.check:
        if not path.is_file():
            print("TPC214_CERTIFICATE_CHECK=FAIL missing certificate", file=sys.stderr)
            return 1
        actual = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        if actual != expected:
            print("TPC214_CERTIFICATE_CHECK=FAIL stale or noncanonical", file=sys.stderr)
            return 1
        print("TPC214_CERTIFICATE_CHECK=PASS")
        for family in actual["families"]:
            print(
                "family=%s ratio=%s factorization=%s"
                % (
                    ",".join(str(value) for value in family["divisors"]),
                    family["physical_to_direct_ratio"],
                    family["cluster_factorization"],
                )
            )
        return 0
    write_certificate(path)
    print("TPC214_CERTIFICATE_WRITE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
