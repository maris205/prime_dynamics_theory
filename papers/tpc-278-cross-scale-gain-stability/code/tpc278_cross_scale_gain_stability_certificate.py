#!/usr/bin/env python3
"""Exact shell/clock stability certificate for the TPC-278 gain audit."""

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
PARENT_PROJECT = ROOT / "papers/tpc-277-four-packet-gain-floor"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc277_four_packet_gain_floor_certificate.py"
)
PARENT_RESULT = PARENT_PROJECT / "results/tpc277_certificate.json"
RESULT = PROJECT / "results/tpc278_certificate.json"
PARENT_CODE_SHA256 = "90fe6ababc93f9465ad067049e404d34a14c7ae0476316cab6507155705bbe4e"
PARENT_RESULT_SHA256 = "beb2aabc6a46e59a3f0eca9ca3d3170136378845ee316017fdd0299159482949"
SCHEMA = "TPC278_CROSS_SCALE_GAIN_STABILITY_CERTIFICATE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION"
ROUND2_CLUE = "FORMULATE_MINIMAL_SOURCE_LEVEL_COHERENCE_TO_GAIN_THEOREM"
GRID = 10**15

spec = importlib.util.spec_from_file_location("tpc278_parent", PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-277 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval_text(value: Fraction) -> list[str]:
    scaled = value * GRID
    lower = scaled.numerator // scaled.denominator
    upper = lower + int(scaled.numerator % scaled.denominator != 0)
    return [fraction_text(Fraction(lower, GRID)),
            fraction_text(Fraction(upper, GRID))]


def load_parent() -> dict[str, Any]:
    code_raw = PARENT_CODE.read_bytes()
    result_raw = PARENT_RESULT.read_bytes()
    need(digest_bytes(code_raw) == PARENT_CODE_SHA256, "parent code hash")
    need(digest_bytes(result_raw) == PARENT_RESULT_SHA256, "parent result hash")
    data = json.loads(result_raw)
    need(result_raw == canonical(data), "parent result canonicality")
    need(data["payload"]["schema"] ==
         "TPC277_FOUR_PACKET_GAIN_FLOOR_CERTIFICATE_V1", "parent schema")
    need(data["claim_status"] == PARENT.STATUS, "parent status")
    return data


CASES = (
    # scale, H, Q, z, s, role
    (128, 24, 4, 5, 2, "SHELL_MINUS"),
    (128, 24, 5, 5, 2, "SHELL_REFERENCE"),
    (128, 24, 6, 5, 2, "SHELL_PLUS"),
    (192, 32, 5, 5, 2, "SHELL_MINUS"),
    (192, 32, 6, 5, 2, "NATURAL_CONTROL"),
    (192, 32, 7, 5, 2, "SHELL_PLUS"),
    (256, 38, 5, 6, 2, "SHELL_MINUS"),
    (256, 38, 6, 6, 2, "NATURAL_CONTROL"),
    (256, 38, 7, 6, 2, "SHELL_PLUS"),
    (192, 29, 6, 5, 2, "CLOCK_MINUS"),
    (192, 35, 6, 5, 2, "CLOCK_PLUS"),
    (384, 50, 7, 7, 2, "NATURAL_CONTROL"),
)


def exact_digest(diagonal: Fraction, signed: Fraction) -> str:
    return hashlib.sha256(canonical({
        "D": fraction_text(diagonal), "G": fraction_text(signed)
    })).hexdigest()


def row_record(case: tuple[int, int, int, int, int, str],
               parent: dict[str, Any]) -> dict[str, Any]:
    scale, height, q0, z, exponent, role = case
    diagonal, signed, shell = PARENT.exact_packet_energies(
        scale, height, q0, z, exponent)
    gain = diagonal / signed
    cancellation = (diagonal - signed) / diagonal
    cross_ratio = (signed - diagonal) / (2 * diagonal)
    sign = "NEGATIVE_CROSS" if signed < diagonal else \
        "POSITIVE_CROSS" if signed > diagonal else "ZERO_CROSS"
    return {
        "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": z, "kernel_exponent": exponent,
        "role": role, "prime_shell": shell,
        "gain_interval": interval_text(gain),
        "cancellation_fraction_interval": interval_text(cancellation),
        "cross_ratio_interval": interval_text(cross_ratio),
        "gain_classification": "ABOVE_ONE" if gain > 1 else
            "BELOW_ONE" if gain < 1 else "EQUAL_ONE",
        "cross_sign": sign,
        "exact_replay_digest": exact_digest(diagonal, signed),
        "matrix_entry_arithmetic": "EXACT_RATIONAL",
        "source_identity": "TPC277_LITERAL_SOURCE_PACKET_REPLAY",
    }


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    rows = [row_record(case, parent) for case in CASES]
    controls = [row for row in rows if row["role"] == "NATURAL_CONTROL"]
    negative = [row for row in rows if row["cross_sign"] == "NEGATIVE_CROSS"]
    positive = [row for row in rows if row["cross_sign"] == "POSITIVE_CROSS"]
    need(len(rows) == 12 and len(controls) == 3 and len(negative) == 8 and
         len(positive) == 4, "classification census")
    # The three unchanged rows must agree with the TPC-277 intervals.
    parent_rows = {(int(row["scale"]), int(row["kernel_exponent"])): row
                   for row in parent["payload"]["rows"]}
    for row in controls:
        upstream = parent_rows[(row["scale"], row["kernel_exponent"])]
        need(row["gain_interval"] == upstream["gain_interval"],
             "control transfer")
    flips = [
        {"scale": 128, "from_Q": 5, "to_Q": 6,
         "from_sign": "NEGATIVE_CROSS", "to_sign": "POSITIVE_CROSS"},
        {"scale": 192, "from_Q": 6, "to_Q": 7,
         "from_sign": "NEGATIVE_CROSS", "to_sign": "POSITIVE_CROSS"},
        {"scale": 256, "from_Q": 5, "to_Q": 6,
         "from_sign": "POSITIVE_CROSS", "to_sign": "NEGATIVE_CROSS"},
        {"scale": 192, "from_H": 29, "to_H": 32,
         "from_sign": "POSITIVE_CROSS", "to_sign": "NEGATIVE_CROSS"},
    ]
    return {
        "schema": SCHEMA,
        "parameters": {
            "upstream_schema": "TPC277_FOUR_PACKET_GAIN_FLOOR_CERTIFICATE_V1",
            "upstream_code_sha256": PARENT_CODE_SHA256,
            "upstream_result_sha256": PARENT_RESULT_SHA256,
            "operator": "same literal prime shell, beta, masks, deleted diagonal, P3",
            "varying_parameters": ["Q shell endpoint", "H clock"],
            "fixed_parameters": ["N", "z", "s=2", "source beta", "projection"],
            "interval_grid": str(GRID),
        },
        "finite_theorem": {
            "total_rows": len(rows), "natural_controls": len(controls),
            "negative_cross_rows": len(negative),
            "positive_cross_rows": len(positive),
            "shell_or_clock_sign_flips": len(flips),
            "stable_natural_gain": "r>1 on 3 controls",
            "stability_claim": "r>=1 is REFUTED_SCOPED under declared finite Q/H perturbations",
        },
        "flips": flips,
        "rows": rows,
        "firewall": {
            "TPC278_LITERAL_SOURCE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC278_NATURAL_CONTROLS": "NUMERICALLY_CERTIFIED_FINITE_3_ROWS",
            "TPC278_SHELL_CLOCK_FLIPS": "NUMERICALLY_CERTIFIED_FINITE_4_FLIPS",
            "TPC278_SIGNED_GAIN_STABILITY": "REFUTED_SCOPED_FINITE",
            "TPC278_SOURCE_LEVEL_UNIFORMITY": "OPEN_ASYMPTOTIC",
            "TPC278_FIXED_POWER_CREDIT": 0,
            "TPC278_ARITHMETIC_ADVANCE": "NO",
            "TPC278_L2": "NONE",
            "TPC278_FULL_GATE_B": "OPEN",
            "TPC278_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC278_TWIN_PRIME_RESULT": "NONE",
            "TPC278_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA and
         data["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(),
         "certificate hash/schema")
    theorem = payload["finite_theorem"]
    need(theorem == {
        "natural_controls": 3, "negative_cross_rows": 8,
        "positive_cross_rows": 4, "shell_or_clock_sign_flips": 4,
        "stable_natural_gain": "r>1 on 3 controls",
        "stability_claim": "r>=1 is REFUTED_SCOPED under declared finite Q/H perturbations",
        "total_rows": 12,
    }, "theorem census")
    need(payload["firewall"]["TPC278_FIXED_POWER_CREDIT"] == 0,
         "power credit")
    print("TPC278_CERTIFICATE=PASS rows=12 controls=3 sign_flips=4 "
          "stability=REFUTED_SCOPED fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            ZeroDivisionError, json.JSONDecodeError) as error:
        raise SystemExit("TPC278_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
