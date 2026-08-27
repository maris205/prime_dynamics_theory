#!/usr/bin/env python3
"""Independent replay and sign-path checker for TPC-278."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc278_certificate.json"
PRODUCER_PATH = PROJECT / "code/tpc278_cross_scale_gain_stability_certificate.py"
PARENT_REPLAY = ROOT / (
    "papers/tpc-277-four-packet-gain-floor/experiments/"
    "tpc277_independent_checker.py"
)

spec = importlib.util.spec_from_file_location("tpc278_producer", PRODUCER_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("producer unavailable")
PRODUCER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PRODUCER)
spec2 = importlib.util.spec_from_file_location("tpc277_column_replay", PARENT_REPLAY)
if spec2 is None or spec2.loader is None:
    raise RuntimeError("parent replay unavailable")
REPLAY = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(REPLAY)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def digest(diagonal: Fraction, signed: Fraction) -> str:
    raw = (json.dumps({
        "D": f"{diagonal.numerator}/{diagonal.denominator}",
        "G": f"{signed.numerator}/{signed.denominator}",
    }, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def interval(value: Fraction) -> list[str]:
    return PRODUCER.interval_text(value)


def check() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(data["claim_status"] == PRODUCER.STATUS, "status")
    rows = data["payload"]["rows"]
    need(len(rows) == len(PRODUCER.CASES), "row count")
    observed = {}
    for case, row in zip(PRODUCER.CASES, rows):
        diagonal, signed, shell = REPLAY.replay(case)
        key = (case[0], case[1], case[2], case[3])
        observed[key] = "NEGATIVE_CROSS" if signed < diagonal else \
            "POSITIVE_CROSS" if signed > diagonal else "ZERO_CROSS"
        need(row["prime_shell"] == shell, "shell")
        need(row["exact_replay_digest"] == digest(diagonal, signed),
             "digest")
        gain = diagonal / signed
        need(row["gain_interval"] == interval(gain), "gain interval")
        need(row["cross_sign"] == observed[key], "cross sign")
        need(row["gain_classification"] == (
            "ABOVE_ONE" if gain > 1 else "BELOW_ONE" if gain < 1 else "EQUAL_ONE"
        ), "gain classification")
    need(observed[(128, 24, 5, 5)] == "NEGATIVE_CROSS" and
         observed[(128, 24, 6, 5)] == "POSITIVE_CROSS", "N128 flip")
    need(observed[(192, 32, 6, 5)] == "NEGATIVE_CROSS" and
         observed[(192, 32, 7, 5)] == "POSITIVE_CROSS", "N192 shell flip")
    need(observed[(256, 38, 5, 6)] == "POSITIVE_CROSS" and
         observed[(256, 38, 6, 6)] == "NEGATIVE_CROSS", "N256 flip")
    need(observed[(192, 29, 6, 5)] == "POSITIVE_CROSS" and
         observed[(192, 32, 6, 5)] == "NEGATIVE_CROSS", "clock flip")
    print("TPC278_INDEPENDENT_CHECK=PASS rows=12 exact_replays=12 "
          "negative=8 positive=4 flips=4")


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("TPC278_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
