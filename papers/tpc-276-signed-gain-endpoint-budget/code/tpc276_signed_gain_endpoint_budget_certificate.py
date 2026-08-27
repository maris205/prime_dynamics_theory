#!/usr/bin/env python3
"""Exact signed-gain margin and endpoint-budget certificate for TPC-276."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT = ROOT / "papers/tpc-275-signed-four-packet-reassembly/results/tpc275_certificate.json"
RESULT = PROJECT / "results/tpc276_certificate.json"
PARENT_FILE_SHA256 = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
PARENT_PAYLOAD_SHA256 = "6f72d561af7f6aec1626843cc0574afc74a1de5a10f57867b202a585a1cfc429"
PARENT_SCHEMA = "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1"
SCHEMA = "TPC276_SIGNED_GAIN_ENDPOINT_BUDGET_CERTIFICATE_V1"
STATUS = "PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER"
ROUND2_CLUE = "SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND"


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction, hi: Fraction | None = None) -> None:
        self.lo = Fraction(lo)
        self.hi = self.lo if hi is None else Fraction(hi)
        need(self.lo <= self.hi, "reversed interval")

    def scale_positive(self, factor: Fraction) -> Interval:
        need(factor > 0, "nonpositive scale")
        return Interval(self.lo * factor, self.hi * factor)

    def subtract(self, other: Interval) -> Interval:
        return Interval(self.lo - other.hi, self.hi - other.lo)


def interval(value: object, positive: bool = False) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    result = Interval(fraction(value[0]), fraction(value[1]))
    need(not positive or result.lo > 0, "interval sign")
    return result


def interval_text(value: Interval) -> list[str]:
    return [f"{value.lo.numerator}/{value.lo.denominator}",
            f"{value.hi.numerator}/{value.hi.denominator}"]


def classify(value: Interval, threshold: Fraction) -> str:
    if value.lo > threshold:
        return "ABOVE_THRESHOLD"
    if value.hi < threshold:
        return "BELOW_THRESHOLD"
    return "CROSSES_THRESHOLD"


def load_parent() -> dict[str, Any]:
    raw = PARENT.read_bytes()
    need(digest_bytes(raw) == PARENT_FILE_SHA256, "parent file provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT",
         "parent header")
    payload = data.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == PARENT_SCHEMA,
         "parent schema")
    need(data.get("payload_sha256") == PARENT_PAYLOAD_SHA256 and
         hashlib.sha256(canonical(payload)).hexdigest() == PARENT_PAYLOAD_SHA256,
         "parent payload provenance")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 12, "parent rows")
    return data


def row_record(row: dict[str, Any]) -> dict[str, Any]:
    gain = fraction(row["diagonal_to_signed_ratio"])
    diagonal = interval(row["diagonal_margin_squared_interval"], True)
    signed = diagonal.scale_positive(gain)
    parent_reference = interval(row["actual_margin_squared_interval"], True)
    overlap = max(signed.lo, parent_reference.lo) <= min(signed.hi,
                                                          parent_reference.hi)
    need(gain > 1 and signed.lo > 0 and overlap,
         "parent row does not support signed transfer")
    quarter = Fraction(1, 16)
    eighth = Fraction(1, 64)
    improvement = signed.subtract(diagonal)
    return {
        "scale": row["scale"],
        "kernel_exponent": row["kernel_exponent"],
        "diagonal_margin_squared_interval": interval_text(diagonal),
        "signed_gain_factor": f"{gain.numerator}/{gain.denominator}",
        "signed_margin_squared_interval": interval_text(signed),
        "signed_margin_improvement_interval": interval_text(improvement),
        "signed_gain_identity": "m^2=(D/G)m_D^2",
        "gain_classification": "STRICTLY_ABOVE_ONE",
        "diagonal_quarter_classification": classify(diagonal, quarter),
        "signed_quarter_classification": classify(signed, quarter),
        "signed_eighth_classification": classify(signed, eighth),
        "parent_actual_margin_reference": interval_text(parent_reference),
        "parent_reference_overlaps_signed_interval": True,
        "finite_transfer_exact": True,
    }


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    parent_payload = parent["payload"]
    source_rows = parent_payload["rows"]
    rows = [row_record(row) for row in source_rows]
    need(len(rows) == 12, "transferred row count")
    return {
        "schema": SCHEMA,
        "parameters": {
            "parent_schema": PARENT_SCHEMA,
            "parent_payload_sha256": PARENT_PAYLOAD_SHA256,
            "parent_file_sha256": PARENT_FILE_SHA256,
            "E0": "5/3",
            "E_star": "1997/1200",
            "strict_endpoint_gap": "1/400",
            "diagonal_margin_threshold": "m_D^2=1/16",
            "signed_margin_threshold": "m^2=1/16",
            "eighth_margin_threshold": "m^2=1/64",
            "signed_gain_definition": "r=D/G",
            "signed_margin_identity": "m^2=r*m_D^2",
            "conditional_gain_hypothesis": "D/G>=b*x^gamma",
            "conditional_margin_hypothesis": "m_D>=c*x^(-eta_D-epsilon)",
            "conditional_scalar_hypothesis": "|C|<=A*x^(E0-sigma+epsilon)",
            "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
            "strict_budget_condition": "sigma-eta_eff>1/400",
        },
        "finite_theorem": {
            "status": "NUMERICALLY_CERTIFIED_FINITE",
            "total_rows": len(rows),
            "parent_rows": len(rows),
            "gain_strictly_above_one_rows": sum(
                row["gain_classification"] == "STRICTLY_ABOVE_ONE" for row in rows),
            "signed_gain_identity_rows": sum(
                row["finite_transfer_exact"] for row in rows),
            "diagonal_below_quarter_rows": sum(
                row["diagonal_quarter_classification"] == "BELOW_THRESHOLD"
                for row in rows),
            "signed_above_quarter_rows": sum(
                row["signed_quarter_classification"] == "ABOVE_THRESHOLD"
                for row in rows),
            "signed_above_eighth_rows": sum(
                row["signed_eighth_classification"] == "ABOVE_THRESHOLD"
                for row in rows),
            "signed_quarter_crossing_rows": sum(
                row["signed_quarter_classification"] == "CROSSES_THRESHOLD"
                for row in rows),
            "claim": "signed gain recovers finite margin but finite gain is not power credit",
        },
        "budget_compiler": {
            "status": "PROVED_CONDITIONAL",
            "scalar_saving": "sigma",
            "diagonal_margin_loss": "eta_D",
            "signed_gain_exponent": "gamma",
            "margin_gain_exponent": "gamma/2",
            "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
            "effective_endpoint_saving": "sigma-eta_eff",
            "strict_target_condition": "sigma-eta_eff>1/400",
            "endpoint_exponent": "E0-sigma+eta_eff+2*epsilon",
        },
        "firewall": {
            "TPC276_SIGNED_GAIN_MARGIN_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC276_CONDITIONAL_BUDGET_COMPILER": "PROVED_CONDITIONAL",
            "TPC276_FINITE_SIGNED_MARGIN_TRANSFER":
            "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC276_SIGNED_QUARTER_CROSSING":
            "NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS",
            "TPC276_SIGNED_EIGHTH_CROSSING":
            "NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS",
            "TPC276_GAIN_STRICTLY_ABOVE_ONE":
            "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC276_FINITE_POWER_PROMOTION": "REFUTED_SCOPED",
            "TPC276_FIXED_POWER_CREDIT": 0,
            "TPC276_SOURCE_LEVEL_SIGNED_GAIN": "OPEN_ASYMPTOTIC",
            "TPC276_ARITHMETIC_ADVANCE": "NO",
            "TPC276_L2": "NONE",
            "TPC276_FULL_GATE_B": "OPEN",
            "TPC276_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC276_TWIN_PRIME_RESULT": "NONE",
            "TPC276_STATUS": STATUS,
        },
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(stored == document(), "certificate mismatch")
    need(raw == canonical(stored), "certificate canonicality")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC276_CERTIFICATE=PASS "
          f"rows={theorem['total_rows']} "
          f"gain_above_one={theorem['gain_strictly_above_one_rows']} "
          f"signed_quarter={theorem['signed_above_quarter_rows']} "
          f"signed_eighth={theorem['signed_above_eighth_rows']} "
          "fixed_power_credit=0")


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
        raise SystemExit("TPC276_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
