#!/usr/bin/env python3
"""Independent replay of the TPC-284 finite control atlas.

The producer is intentionally not imported.  This checker loads only the
frozen TPC-268 operator, reconstructs the six controls, and compares every
interval and sign in the released certificate.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-284-admissible-source-control-atlas"
ENGINE_PATH = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-283-source-attachment-stability-radius/results/"
    "tpc283_certificate.json")
RESULT = PROJECT / "results/tpc284_certificate.json"
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
PARENT_SHA256 = (
    "145c0f324772fba966e6ac0bc2a27e0bd4611758400ea43b3721ae516217af8b")
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_"
    "SIGN_FLIP_OBSTRUCTION")
SCHEMA = "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1"
BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)
EXPONENTS = (1, 2)
CONTROLS = (
    ("H_MINUS_2", -2, 0, 0), ("H_PLUS_2", 2, 0, 0),
    ("Z_MINUS_1", 0, 0, -1), ("Z_PLUS_1", 0, 0, 1),
    ("Q_MINUS_1", 0, -1, 0), ("Q_PLUS_1", 0, 1, 0),
)

spec = importlib.util.spec_from_file_location("independent_tpc268", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("TPC284_INDEPENDENT_CHECK=FAIL engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction endpoint")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = fraction(value[0]), fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def interval_text(value: Any) -> list[str]:
    # ``audit_case`` has already serialized its interval; normalize the
    # decimal endpoints as exact rationals before comparing the certificate.
    need(isinstance(value, list) and len(value) == 2, "engine interval")
    return [str(fraction(value[0])), str(fraction(value[1]))]


def baseline_signs() -> dict[tuple[int, int, int, int], str]:
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_SHA256, "parent provenance")
    parent = json.loads(raw)
    need(raw == canonical(parent), "parent canonicality")
    result: dict[tuple[int, int, int, int], str] = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["kernel_exponent"]))
        c = interval(row["source_scalar_C_interval"])
        need(c[1] < 0 or c[0] > 0, "parent sign")
        result[key] = "NEGATIVE" if c[1] < 0 else "POSITIVE"
    need(len(result) == 12, "parent row census")
    return result


def check() -> None:
    need(digest(ENGINE_PATH.read_bytes()) == ENGINE_SHA256, "engine hash")
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "result canonicality")
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS, "result header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA, "result schema")
    need(data["payload_sha256"] == digest(canonical(payload)),
         "result payload hash")
    baseline = baseline_signs()
    rows = payload["rows"]
    need(len(rows) == 72, "result row census")
    expected_flips = {
        (128, 1, "Q_PLUS_1"), (128, 2, "Q_PLUS_1"),
        (192, 1, "Z_MINUS_1"), (192, 1, "Q_MINUS_1"),
        (192, 2, "Q_MINUS_1"), (256, 1, "Z_MINUS_1"),
        (256, 1, "Q_MINUS_1"), (256, 2, "Q_PLUS_1"),
    }
    actual_flips = set()
    negative = positive = 0
    for row in rows:
        scale, bh, bq, bz = (int(row["scale"]), int(row["base_H"]),
                              int(row["base_Q"]), int(row["base_z"]))
        exponent = int(row["kernel_exponent"])
        control = str(row["control"])
        spec_row = next((item for item in CONTROLS if item[0] == control), None)
        need(spec_row is not None, "control name")
        _, dh, dq, dz = spec_row
        need((bh, bq, bz) in {(h, q, z) for _, h, q, z in BASE_CASES},
             "base parameters")
        audit = ENGINE.audit_case(scale, bh + dh, bq + dq, exponent,
                                  bz + dz, "TPC284_" + control)
        c = interval_text(audit["residual_scalar_interval"])
        rho = interval_text(audit["rho_squared_interval"])
        need(c == row["source_scalar_C_interval"], "source interval mismatch")
        need(rho == row["rho_squared_interval"], "rho interval mismatch")
        lo, hi = interval(c)
        rlo, _ = interval(rho)
        need(hi < 0 or lo > 0, "crossing control")
        sign = "NEGATIVE" if hi < 0 else "POSITIVE"
        need(sign == row["attachment_sign"], "sign mismatch")
        key = (scale, bh, bq, exponent)
        need(row["baseline_sign"] == baseline[key], "baseline mismatch")
        flip = sign != baseline[key]
        need(row["sign_flip"] is flip and rlo > 0, "semantic row mismatch")
        if flip:
            actual_flips.add((scale, exponent, control))
        negative += sign == "NEGATIVE"
        positive += sign == "POSITIVE"
    need(negative == 60 and positive == 12 and
         actual_flips == expected_flips, "atlas census")
    need(payload["finite_theorem"] == {
        "all_rows_finite_nonzero": True,
        "asymptotic_control_stability": "OPEN",
        "fixed_power_credit": 0,
        "literal_source_class_exhaustion": "NOT_CLAIMED",
        "negative_rows": 60,
        "positive_rows": 12,
        "rows": 72,
        "sign_flip_rows_against_baseline": 8,
        "statement": "six declared local schedule controls are sign-separated on all 72 registered finite rows",
        "zero_crossing_rows": 0,
    }, "theorem census")
    print("TPC284_INDEPENDENT_CHECK=PASS rows=72 negative=60 positive=12 "
          "sign_flips=8 exact_interval_replay=72")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC284_INDEPENDENT_CHECK=FAIL: " + str(error))
