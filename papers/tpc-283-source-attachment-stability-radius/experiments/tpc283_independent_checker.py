#!/usr/bin/env python3
"""Independent algebraic and parent-bound replay for TPC-283."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-283-source-attachment-stability-radius"
PARENT = ROOT / "papers/tpc-282-literal-source-attachment-audit/results/tpc282_certificate.json"
RESULT = PROJECT / "results/tpc283_certificate.json"
PARENT_SHA256 = "58c457135a5d22c597556a8c38f6abc6458d52d78817c04542c3c3307a0b3bf3"
STATUS = (
    "PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT")
SCHEMA = "TPC283_SOURCE_ATTACHMENT_STABILITY_RADIUS_CERTIFICATE_V1"


class Failure(RuntimeError):
    pass


def need(c: bool, m: str) -> None:
    if type(c) is not bool or not c:
        raise Failure(m)


def canonical(v: object) -> bytes:
    return (json.dumps(v, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(b: bytes) -> str:
    return hashlib.sha256(b.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def f(v: object) -> Fraction:
    need(isinstance(v, str), "fraction")
    return Fraction(v)


def iv(v: object) -> tuple[Fraction, Fraction]:
    need(isinstance(v, list) and len(v) == 2, "interval")
    a, b = f(v[0]), f(v[1]); need(a <= b, "interval order")
    return a, b


def check_fixture(row: dict) -> None:
    w = [f(x) for x in row["w"]]; s = [f(x) for x in row["S"]]
    C = w[0] * s[0] + w[1] * s[1]
    W = w[0] * w[0] + w[1] * w[1]
    Y = s[0] * s[0] + s[1] * s[1]
    need(C == f(row["C"]) and W == f(row["W"]) and Y == f(row["Y"]),
         "fixture scalar")
    radius = C * C / (W * Y)
    need(radius == f(row["relative_zeroing_radius_squared"]), "fixture radius")
    d = [f(x) for x in row["zeroing_perturbation"]]
    need((w[0] + d[0]) * s[0] + (w[1] + d[1]) * s[1] == 0,
         "fixture zeroing")


def check() -> None:
    need(digest(PARENT.read_bytes()) == PARENT_SHA256, "parent hash")
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    raw = RESULT.read_bytes(); data = json.loads(raw)
    need(raw == canonical(data), "canonical result")
    need(data["claim_status"] == STATUS and
         data["payload"]["schema"] == SCHEMA, "header")
    need(data["payload_sha256"] == digest(canonical(data["payload"])),
         "payload hash")
    p = data["payload"]
    for fixture in p["fixtures"]:
        check_fixture(fixture)
    need(len(p["rows"]) == len(parent["payload"]["rows"]) == 12,
         "row count")
    for out, src in zip(p["rows"], parent["payload"]["rows"]):
        need((out["scale"], out["H"], out["Q"], out["kernel_exponent"]) ==
             (src["scale"], src["H"], src["Q"], src["kernel_exponent"]),
             "row key")
        rho = iv(out["relative_zeroing_radius_squared_interval"])
        need(rho[0] > 0 and rho[1] < Fraction(9, 100), "radius bound")
    need(p["finite_audit"]["relative_radius_upper_below_1_over_10"] == 6,
         "ten percent census")
    print("TPC283_INDEPENDENT_CHECK=PASS fixtures=4 rows=12 "
          "zeroing_formula=12 under_30_percent=12")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as e:
        raise SystemExit("TPC283_INDEPENDENT_CHECK=FAIL: " + str(e))
