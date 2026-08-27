#!/usr/bin/env python3
"""Finite atlas of declared, local controls for the literal source attachment.

TPC-283 measured the distance to an unrestricted zero-attachment hyperplane.
This certificate asks the narrower question that is relevant to the physical
interface: what happens under six explicitly declared schedule controls,
namely H +/- 2, z +/- 1, and Q +/- 1?  The frozen TPC-268 operator is replayed
with outward interval arithmetic.  The output is deliberately a finite atlas;
no row is promoted to an asymptotic stability statement.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_PROJECT = ROOT / "papers/tpc-283-source-attachment-stability-radius"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc283_source_attachment_stability_certificate.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc283_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc284_certificate.json"

PARENT_CODE_SHA256 = (
    "d64644e2b19d668d0c71d81748741fdbbabd44f1852fc131b432a98dfe8fd4cc")
PARENT_RESULT_SHA256 = (
    "145c0f324772fba966e6ac0bc2a27e0bd4611758400ea43b3721ae516217af8b")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
SCHEMA = "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_"
    "SIGN_FLIP_OBSTRUCTION")
ROUND2_CLUE = (
    "COMPILE_PRIME_SHELL_CONTROL_CONSTRAINTS_BEFORE_ANY_"
    "ASYMPTOTIC_STABILITY_CLAIM")

BASE_CASES = (
    (64, 15, 4, 4),
    (96, 20, 5, 4),
    (128, 24, 5, 4),
    (192, 32, 6, 5),
    (256, 38, 6, 5),
    (384, 50, 7, 5),
)
EXPONENTS = (1, 2)
CONTROL_SPECS = (
    ("H_MINUS_2", -2, 0, 0, "clock height H decreased by 2"),
    ("H_PLUS_2", 2, 0, 0, "clock height H increased by 2"),
    ("Z_MINUS_1", 0, 0, -1, "comparison cutoff z decreased by 1"),
    ("Z_PLUS_1", 0, 0, 1, "comparison cutoff z increased by 1"),
    ("Q_MINUS_1", 0, -1, 0, "prime-shell lower endpoint Q decreased by 1"),
    ("Q_PLUS_1", 0, 1, 0, "prime-shell lower endpoint Q increased by 1"),
)

spec = importlib.util.spec_from_file_location("frozen_tpc268_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen TPC-268 engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = fraction(value[0]), fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def interval_text(value: tuple[Fraction, Fraction]) -> list[str]:
    return [str(value[0]), str(value[1])]


def load_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "parent result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_"
         "NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT",
         "parent status")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC283_SOURCE_ATTACHMENT_STABILITY_RADIUS_CERTIFICATE_V1",
         "parent schema")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent row count")
    return data


def parent_sign_map(parent: dict[str, Any]) -> dict[tuple[int, int, int, int], str]:
    result: dict[tuple[int, int, int, int], str] = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["kernel_exponent"]))
        need(key not in result, "duplicate parent row")
        c = interval(row["source_scalar_C_interval"])
        need(c[1] < 0 or c[0] > 0, "parent attachment crosses zero")
        result[key] = "NEGATIVE" if c[1] < 0 else "POSITIVE"
    expected = {(x, h, q, s) for x, h, q, _ in BASE_CASES for s in EXPONENTS}
    need(set(result) == expected, "parent key census")
    return result


def control_key(row: dict[str, Any]) -> tuple[int, int, int, int, str]:
    return (int(row["scale"]), int(row["base_H"]), int(row["base_Q"]),
            int(row["kernel_exponent"]), str(row["control"]))


def audit_row(scale: int, base_h: int, base_q: int, base_z: int,
              exponent: int, control: str, dh: int, dq: int, dz: int,
              description: str, baseline_sign: str) -> dict[str, Any]:
    height, q0, cutoff = base_h + dh, base_q + dq, base_z + dz
    need(height > 0 and q0 > 0 and cutoff > 0, "invalid controlled parameter")
    audit = ENGINE.audit_case(scale, height, q0, exponent, cutoff,
                              "TPC284_" + control)
    c = interval(audit["residual_scalar_interval"])
    rho = interval(audit["rho_squared_interval"])
    need(c[1] < 0 or c[0] > 0, "control attachment crosses zero")
    need(rho[0] > 0, "control normalized attachment is not positive")
    sign = "NEGATIVE" if c[1] < 0 else "POSITIVE"
    return {
        "scale": scale,
        "base_H": base_h,
        "base_Q": base_q,
        "base_z": base_z,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "control": control,
        "control_description": description,
        "delta_H": dh,
        "delta_Q": dq,
        "delta_z": dz,
        "control_class": "SCHEDULE_CONTROL_ONLY",
        "source_scalar_C_interval": interval_text(c),
        "rho_squared_interval": interval_text(rho),
        "attachment_sign": sign,
        "baseline_sign": baseline_sign,
        "sign_flip": sign != baseline_sign,
        "finite_nonzero_attachment": True,
        "physical_literal_operator_replayed": True,
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    baseline = parent_sign_map(parent)
    rows: list[dict[str, Any]] = []
    for scale, base_h, base_q, base_z in BASE_CASES:
        for exponent in EXPONENTS:
            base_sign = baseline[(scale, base_h, base_q, exponent)]
            for control, dh, dq, dz, description in CONTROL_SPECS:
                rows.append(audit_row(
                    scale, base_h, base_q, base_z, exponent, control,
                    dh, dq, dz, description, base_sign))
    need(len(rows) == 72, "control atlas row count")
    negative = sum(row["attachment_sign"] == "NEGATIVE" for row in rows)
    positive = sum(row["attachment_sign"] == "POSITIVE" for row in rows)
    crossing = sum(not row["finite_nonzero_attachment"] for row in rows)
    flips = [row for row in rows if row["sign_flip"]]
    need(negative == 60 and positive == 12 and crossing == 0,
         "control atlas sign census")
    expected_flips = {
        (128, 1, "Q_PLUS_1"),
        (128, 2, "Q_PLUS_1"),
        (192, 1, "Z_MINUS_1"),
        (192, 1, "Q_MINUS_1"),
        (192, 2, "Q_MINUS_1"),
        (256, 1, "Z_MINUS_1"),
        (256, 1, "Q_MINUS_1"),
        (256, 2, "Q_PLUS_1"),
    }
    actual_flips = {(row["scale"], row["kernel_exponent"], row["control"])
                    for row in flips}
    need(actual_flips == expected_flips and len(flips) == 8,
         "sign-flip census")
    weakest = min(rows, key=lambda row: interval(
        row["rho_squared_interval"])[0])
    strongest = max(rows, key=lambda row: interval(
        row["rho_squared_interval"])[1])
    need((weakest["scale"], weakest["kernel_exponent"], weakest["control"])
         == (192, 1, "H_PLUS_2"), "weakest-row key")
    need((strongest["scale"], strongest["kernel_exponent"], strongest["control"])
         == (64, 2, "Z_PLUS_1"), "strongest-row key")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "schema": "TPC283_SOURCE_ATTACHMENT_STABILITY_RADIUS_CERTIFICATE_V1",
            "code_sha256": PARENT_CODE_SHA256,
            "result_sha256": PARENT_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "baseline_rows": 12,
        },
        "control_families": [
            {"name": name, "delta_H": dh, "delta_Q": dq, "delta_z": dz,
             "description": description,
             "status": "DECLARED_FINITE_SCHEDULE_CONTROL"}
            for name, dh, dq, dz, description in CONTROL_SPECS
        ],
        "finite_theorem": {
            "statement": (
                "six declared local schedule controls are sign-separated on "
                "all 72 registered finite rows"),
            "rows": 72,
            "negative_rows": negative,
            "positive_rows": positive,
            "zero_crossing_rows": crossing,
            "sign_flip_rows_against_baseline": len(flips),
            "all_rows_finite_nonzero": True,
            "fixed_power_credit": 0,
            "asymptotic_control_stability": "OPEN",
            "literal_source_class_exhaustion": "NOT_CLAIMED",
        },
        "extremal_rows": {
            "weakest_lower_rho_squared": {
                "scale": weakest["scale"], "base_H": weakest["base_H"],
                "base_Q": weakest["base_Q"], "base_z": weakest["base_z"],
                "kernel_exponent": weakest["kernel_exponent"],
                "control": weakest["control"],
                "interval": weakest["rho_squared_interval"],
            },
            "largest_upper_rho_squared": {
                "scale": strongest["scale"], "base_H": strongest["base_H"],
                "base_Q": strongest["base_Q"], "base_z": strongest["base_z"],
                "kernel_exponent": strongest["kernel_exponent"],
                "control": strongest["control"],
                "interval": strongest["rho_squared_interval"],
            },
        },
        "rows": rows,
        "firewall": {
            "TPC284_CONTROL_ATLAS": "NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
            "TPC284_CONTROL_SIGN_CENSUS": "60_NEGATIVE_12_POSITIVE_0_CROSSING",
            "TPC284_SIGN_FLIP_OBSTRUCTION": "NUMERICALLY_CERTIFIED_FINITE_8_FLIPS",
            "TPC284_CONTINUOUS_LOCAL_STABILITY": "NOT_TESTED",
            "TPC284_ASYMPTOTIC_CONTROL_STABILITY": "OPEN",
            "TPC284_LITERAL_SOURCE_CLASS_THEOREM": "OPEN",
            "TPC284_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC284_FIXED_POWER_CREDIT": 0,
            "TPC284_FULL_GATE_B": "OPEN",
            "TPC284_TWIN_PRIME_RESULT": "NONE",
            "TPC284_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload(load_parent())
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def check_data(data: dict[str, Any]) -> None:
    need(data == document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    finite = data["payload"]["finite_theorem"]
    print("TPC284_CERTIFICATE=PASS rows=72 negative=60 positive=12 "
          "zero_crossings=0 sign_flips=8 fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC284_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
