#!/usr/bin/env python3
"""Independent exact transfer checker for the TPC-276 budget certificate."""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-276-signed-gain-endpoint-budget"
PARENT = ROOT / "papers/tpc-275-signed-four-packet-reassembly/results/tpc275_certificate.json"
RESULT = PROJECT / "results/tpc276_certificate.json"
PARENT_FILE_SHA256 = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
PARENT_PAYLOAD_SHA256 = "6f72d561af7f6aec1626843cc0574afc74a1de5a10f57867b202a585a1cfc429"
PARENT_SCHEMA = "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1"
SCHEMA = "TPC276_SIGNED_GAIN_ENDPOINT_BUDGET_CERTIFICATE_V1"
STATUS = "PROVED_CONDITIONAL_SIGNED_GAIN_STRICT_ENDPOINT_BUDGET_PLUS_FINITE_TRANSFER"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def text_interval(value: tuple[Fraction, Fraction]) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def classify(value: tuple[Fraction, Fraction], threshold: Fraction) -> str:
    if value[0] > threshold:
        return "ABOVE_THRESHOLD"
    if value[1] < threshold:
        return "BELOW_THRESHOLD"
    return "CROSSES_THRESHOLD"


def load_parent() -> dict:
    raw = PARENT.read_bytes()
    need(digest_bytes(raw) == PARENT_FILE_SHA256, "parent file hash")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    payload = data["payload"]
    need(data["claim_status"] ==
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT" and
         payload["schema"] == PARENT_SCHEMA and
         data["payload_sha256"] == PARENT_PAYLOAD_SHA256 and
         hashlib.sha256(canonical(payload)).hexdigest() == PARENT_PAYLOAD_SHA256,
         "parent header/provenance")
    need(len(payload["rows"]) == 12, "parent row count")
    return data


def replay_row(parent_row: dict, output_row: dict) -> None:
    gain = frac(parent_row["diagonal_to_signed_ratio"])
    diagonal = interval(parent_row["diagonal_margin_squared_interval"])
    signed = (gain * diagonal[0], gain * diagonal[1])
    actual = interval(parent_row["actual_margin_squared_interval"])
    need(gain > 1 and max(signed[0], actual[0]) <= min(signed[1], actual[1]),
         "parent signed interval")
    need((output_row["scale"], output_row["kernel_exponent"]) ==
         (parent_row["scale"], parent_row["kernel_exponent"]), "row key")
    need(output_row["diagonal_margin_squared_interval"] ==
         text_interval(diagonal) and
         frac(output_row["signed_gain_factor"]) == gain and
         output_row["signed_margin_squared_interval"] == text_interval(signed),
         "signed transfer")
    improvement = (signed[0] - diagonal[1], signed[1] - diagonal[0])
    need(output_row["signed_margin_improvement_interval"] ==
         text_interval(improvement), "improvement interval")
    need(output_row["signed_gain_identity"] == "m^2=(D/G)m_D^2" and
         output_row["gain_classification"] == "STRICTLY_ABOVE_ONE" and
         output_row["diagonal_quarter_classification"] ==
         classify(diagonal, Fraction(1, 16)) and
         output_row["signed_quarter_classification"] ==
         classify(signed, Fraction(1, 16)) and
         output_row["signed_eighth_classification"] ==
         classify(signed, Fraction(1, 64)) and
         output_row["parent_actual_margin_reference"] == text_interval(actual) and
         output_row["parent_reference_overlaps_signed_interval"] is True and
         output_row["finite_transfer_exact"] is True, "row metadata")


def check() -> None:
    parent = load_parent()
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS, "certificate header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() ==
         data["payload_sha256"] and payload["schema"] == SCHEMA,
         "certificate digest/schema")
    need(payload["parameters"] == {
        "E0": "5/3",
        "E_star": "1997/1200",
        "conditional_gain_hypothesis": "D/G>=b*x^gamma",
        "conditional_margin_hypothesis": "m_D>=c*x^(-eta_D-epsilon)",
        "conditional_scalar_hypothesis": "|C|<=A*x^(E0-sigma+epsilon)",
        "diagonal_margin_threshold": "m_D^2=1/16",
        "eighth_margin_threshold": "m^2=1/64",
        "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
        "signed_gain_definition": "r=D/G",
        "signed_margin_identity": "m^2=r*m_D^2",
        "signed_margin_threshold": "m^2=1/16",
        "strict_budget_condition": "sigma-eta_eff>1/400",
        "strict_endpoint_gap": "1/400",
        "parent_file_sha256": PARENT_FILE_SHA256,
        "parent_payload_sha256": PARENT_PAYLOAD_SHA256,
        "parent_schema": PARENT_SCHEMA,
    }, "parameters")
    parent_rows = parent["payload"]["rows"]
    rows = payload["rows"]
    need(len(rows) == 12, "row count")
    for parent_row, output_row in zip(parent_rows, rows):
        replay_row(parent_row, output_row)
    theorem = payload["finite_theorem"]
    need(theorem == {
        "claim": "signed gain recovers finite margin but finite gain is not power credit",
        "diagonal_below_quarter_rows": 12,
        "gain_strictly_above_one_rows": 12,
        "parent_rows": 12,
        "signed_above_eighth_rows": 5,
        "signed_above_quarter_rows": 3,
        "signed_gain_identity_rows": 12,
        "signed_quarter_crossing_rows": 0,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_rows": 12,
    }, "theorem ledger")
    need(payload["budget_compiler"] == {
        "diagonal_margin_loss": "eta_D",
        "effective_endpoint_saving": "sigma-eta_eff",
        "effective_margin_loss": "eta_eff=max(0,eta_D-gamma/2)",
        "endpoint_exponent": "E0-sigma+eta_eff+2*epsilon",
        "signed_gain_exponent": "gamma",
        "margin_gain_exponent": "gamma/2",
        "scalar_saving": "sigma",
        "status": "PROVED_CONDITIONAL",
        "strict_target_condition": "sigma-eta_eff>1/400",
    }, "budget compiler")
    firewall = payload["firewall"]
    need(firewall == {
        "TPC276_ARITHMETIC_ADVANCE": "NO",
        "TPC276_CONDITIONAL_BUDGET_COMPILER": "PROVED_CONDITIONAL",
        "TPC276_FINITE_POWER_PROMOTION": "REFUTED_SCOPED",
        "TPC276_FINITE_SIGNED_MARGIN_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_FIXED_POWER_CREDIT": 0,
        "TPC276_FULL_GATE_B": "OPEN",
        "TPC276_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
        "TPC276_GAIN_STRICTLY_ABOVE_ONE":
        "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
        "TPC276_L2": "NONE",
        "TPC276_SIGNED_EIGHTH_CROSSING":
        "NUMERICALLY_CERTIFIED_FINITE_FIVE_ROWS",
        "TPC276_SIGNED_GAIN_MARGIN_IDENTITY": "PROVED_EXACT_FINITE",
        "TPC276_SIGNED_QUARTER_CROSSING":
        "NUMERICALLY_CERTIFIED_FINITE_THREE_ROWS",
        "TPC276_SOURCE_LEVEL_SIGNED_GAIN": "OPEN_ASYMPTOTIC",
        "TPC276_STATUS": STATUS,
        "TPC276_TWIN_PRIME_RESULT": "NONE",
    }, "firewall")
    need(payload["round2_clue"] ==
         "SEEK_UNIFORM_SOURCE_LEVEL_SIGNED_GAIN_LOWER_BOUND", "round2 clue")
    print("TPC276_INDEPENDENT_CHECK=PASS rows=12 gain_above_one=12 "
          "signed_quarter=3 signed_eighth=5 fixed_power_credit=0")


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("TPC276_INDEPENDENT_CHECK=FAIL " + str(error))
        raise SystemExit(1)
