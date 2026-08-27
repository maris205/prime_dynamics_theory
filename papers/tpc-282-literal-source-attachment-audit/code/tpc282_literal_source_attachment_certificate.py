#!/usr/bin/env python3
"""Finite source-lock certificate for the literal TPC packet attachment.

The calculation is deliberately downstream of the frozen TPC-275 physical
operator.  It replays the twelve registered rows, records the actual projected
source scalar C=<w_perp,S>, and separates finite non-vanishing from an
asymptotic lower bound.  All interval endpoints are inherited outward decimal
intervals; the packet output itself is exact rational arithmetic.
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
PARENT_PROJECT = ROOT / "papers/tpc-275-signed-four-packet-reassembly"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc275_signed_four_packet_reassembly_certificate.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc275_certificate.json"
RESULT = PROJECT / "results/tpc282_certificate.json"

PARENT_CODE_SHA256 = "abceae5328b5f454cabc06c2e95811224217f15d050f1672ce4e60fc154ad405"
PARENT_RESULT_SHA256 = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
ENGINE_CODE_SHA256 = "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3"
SCHEMA = "TPC282_LITERAL_SOURCE_ATTACHMENT_CERTIFICATE_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_"
    "ASYMPTOTIC_NONDEGENERACY_OPEN")
ROUND2_CLUE = "QUANTIFY_SOURCE_ATTACHMENT_STABILITY_RADIUS_AND_SIGN_FLIPS"

spec = importlib.util.spec_from_file_location("frozen_tpc275", PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen TPC-275 producer unavailable")
PARENT_MODULE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT_MODULE)


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


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction endpoint")
    return Fraction(value)


def parse_interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = parse_fraction(value[0]), parse_fraction(value[1])
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
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT",
         "parent status")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1",
         "parent schema")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent row count")
    return data


def parent_row_map(parent: dict[str, Any]) -> dict[tuple[int, int, int, int], dict[str, Any]]:
    result: dict[tuple[int, int, int, int], dict[str, Any]] = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["kernel_exponent"]))
        need(key not in result, "duplicate parent row")
        result[key] = row
    return result


BASE_CASES = PARENT_MODULE.BASE_CASES
EXPONENTS = PARENT_MODULE.EXPONENTS


def abs_lower(interval: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = interval
    need(hi < 0 or lo > 0, "sign-separated interval")
    return -hi if hi < 0 else lo


def row_record(parent_row: dict[str, Any]) -> dict[str, Any]:
    scale, height, q0, exponent = (
        int(parent_row["scale"]), int(parent_row["H"]),
        int(parent_row["Q"]), int(parent_row["kernel_exponent"]))
    # TPC-275 is the frozen physical replay.  Re-running it here checks that
    # the source-lock paper has not silently replaced the literal operator.
    replay = PARENT_MODULE.row_record(scale, height, q0, exponent)
    need(replay["signed_output_energy"] == parent_row["signed_output_energy"],
         "parent signed-output drift")
    audit = PARENT_MODULE.ENGINE.audit_case(
        scale, height, q0, exponent,
        int(parent_row["comparison_cutoff_z"]),
        "TPC282_LITERAL_SOURCE_ATTACHMENT_LOCK")
    c = parse_interval(audit["residual_scalar_interval"])
    w = parse_interval(audit["residual_w_norm_squared_interval"])
    y = parse_fraction(parent_row["signed_output_energy"])
    rho = parse_interval(audit["rho_squared_interval"])
    need(c[1] < 0 or c[0] > 0, "finite attachment crosses zero")
    need(w[0] > 0 and y > 0 and rho[0] > 0 and rho[1] < 1,
         "positive source/output geometry")
    sign = "NEGATIVE" if c[1] < 0 else "POSITIVE"
    return {
        "scale": scale, "H": height, "Q": q0, "kernel_exponent": exponent,
        "comparison_cutoff_z": int(parent_row["comparison_cutoff_z"]),
        "index_count": int(parent_row["index_count"]),
        "source_scalar_C_interval": interval_text(c),
        "projected_source_norm_squared_interval": interval_text(w),
        "projected_output_norm_squared": str(y),
        "attachment_cosine_squared_interval": interval_text(rho),
        "attachment_sign": sign,
        "finite_nonzero_attachment": True,
        "parent_signed_output_match": True,
        "source_definition": "w_perp=(I-P_3)w; S=A_perp beta; C=<w_perp,S>",
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    mapping = parent_row_map(parent)
    rows: list[dict[str, Any]] = []
    for scale, height, q0 in BASE_CASES:
        for exponent in EXPONENTS:
            key = (scale, height, q0, exponent)
            need(key in mapping, "missing registered row")
            rows.append(row_record(mapping[key]))
    need(len(rows) == 12, "row census")
    negative = sum(row["attachment_sign"] == "NEGATIVE" for row in rows)
    positive = sum(row["attachment_sign"] == "POSITIVE" for row in rows)
    need(negative == 11 and positive == 1, "sign census")
    weakest_c = min(rows, key=lambda row: abs_lower(
        parse_interval(row["source_scalar_C_interval"])))
    weakest_rho = min(rows, key=lambda row: parse_interval(
        row["attachment_cosine_squared_interval"])[0])
    return {
        "schema": SCHEMA,
        "source_lock": {
            "parent_schema": "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1",
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_result_sha256": PARENT_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "operator": "literal V59 prime-shell operator followed by A_perp=(I-P_3)A",
            "source_readout": "w_perp=(I-P_3)w from the actual comparison weights",
            "row_count": len(rows),
        },
        "finite_theorem": {
            "statement": "all registered literal rows have a sign-separated nonzero source attachment",
            "negative_rows": negative, "positive_rows": positive,
            "zero_crossing_rows": 0, "fixed_power_credit": 0,
            "asymptotic_nonvanishing": "OPEN",
        },
        "weakest_rows": {
            "smallest_absolute_C": {
                "scale": weakest_c["scale"], "H": weakest_c["H"],
                "Q": weakest_c["Q"], "kernel_exponent": weakest_c["kernel_exponent"],
                "lower_absolute_C": str(abs_lower(parse_interval(
                    weakest_c["source_scalar_C_interval"]))),
            },
            "smallest_attachment_cosine_squared": {
                "scale": weakest_rho["scale"], "H": weakest_rho["H"],
                "Q": weakest_rho["Q"], "kernel_exponent": weakest_rho["kernel_exponent"],
                "lower_rho_squared": str(parse_interval(
                    weakest_rho["attachment_cosine_squared_interval"])[0]),
            },
        },
        "rows": rows,
        "firewall": {
            "TPC282_SOURCE_ATTACHMENT": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC282_SOURCE_SIGN": "11_NEGATIVE_1_POSITIVE_FINITE",
            "TPC282_UNIFORM_ASYMPTOTIC_NONDEGENERACY": "OPEN",
            "TPC282_FIXED_POWER_CREDIT": 0,
            "TPC282_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC282_FULL_GATE_B": "OPEN",
            "TPC282_TWIN_PRIME_RESULT": "NONE",
            "TPC282_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": build_payload(load_parent())}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    data = document()
    data["payload_sha256"] = hashlib.sha256(canonical(data["payload"])).hexdigest()
    RESULT.write_bytes(canonical(data))


def check_data(data: dict[str, Any]) -> None:
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(data.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(), "payload hash")
    source = payload["source_lock"]
    need(source["row_count"] == 12 and
         source["parent_code_sha256"] == PARENT_CODE_SHA256 and
         source["parent_result_sha256"] == PARENT_RESULT_SHA256,
         "source lock")
    finite = payload["finite_theorem"]
    need(finite["negative_rows"] == 11 and finite["positive_rows"] == 1 and
         finite["zero_crossing_rows"] == 0 and
         finite["asymptotic_nonvanishing"] == "OPEN", "finite theorem")
    need(len(payload["rows"]) == 12, "row count")
    for row in payload["rows"]:
        c = parse_interval(row["source_scalar_C_interval"])
        rho = parse_interval(row["attachment_cosine_squared_interval"])
        need(c[1] < 0 or c[0] > 0, "row sign")
        need(rho[0] > 0 and rho[1] < 1, "row cosine")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    regenerated = document()
    regenerated["payload_sha256"] = hashlib.sha256(
        canonical(regenerated["payload"])).hexdigest()
    need(data == regenerated, "certificate is not reproducible")
    print("TPC282_CERTIFICATE=PASS source_rows=12 negative=11 positive=1 "
          "zero_crossings=0 weakest_rho_squared=3.357e-05 "
          "fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        if args.write:
            write()
        else:
            check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC282_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
