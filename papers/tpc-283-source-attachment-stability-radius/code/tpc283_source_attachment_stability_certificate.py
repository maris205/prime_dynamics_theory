#!/usr/bin/env python3
"""Exact stability-radius theorem and finite audit for TPC-282 attachments."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_PROJECT = ROOT / "papers/tpc-282-literal-source-attachment-audit"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc282_literal_source_attachment_certificate.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc282_certificate.json"
RESULT = PROJECT / "results/tpc283_certificate.json"
PARENT_CODE_SHA256 = "57cd9f3a7e2aa8284d2dbd0109b972cc711b6b28daf56a7d2526ae21806b53e1"
PARENT_RESULT_SHA256 = "58c457135a5d22c597556a8c38f6abc6458d52d78817c04542c3c3307a0b3bf3"
PARENT_SCHEMA = "TPC282_LITERAL_SOURCE_ATTACHMENT_CERTIFICATE_V1"
SCHEMA = "TPC283_SOURCE_ATTACHMENT_STABILITY_RADIUS_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_HILBERT_SOURCE_ZEROING_RADIUS_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_VULNERABILITY_AUDIT")
ROUND2_CLUE = "TEST_ADMISSIBLE_LITERAL_SOURCE_CONTROLS_AFTER_UNRESTRICTED_ZEROING_OBSTRUCTION"


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


def frac(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = frac(value[0]), frac(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def itext(value: tuple[Fraction, Fraction]) -> list[str]:
    return [str(value[0]), str(value[1])]


def load_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "parent result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_"
         "ASYMPTOTIC_NONDEGENERACY_OPEN", "parent status")
    need(data["payload"].get("schema") == PARENT_SCHEMA and
         len(data["payload"].get("rows", [])) == 12, "parent schema")
    return data


def fixture_record(name: str, w: tuple[Fraction, Fraction],
                   s: tuple[Fraction, Fraction]) -> dict[str, Any]:
    dot = w[0] * s[0] + w[1] * s[1]
    ww = w[0] * w[0] + w[1] * w[1]
    yy = s[0] * s[0] + s[1] * s[1]
    need(ww > 0 and yy > 0, "fixture positivity")
    radius = dot * dot / (ww * yy)
    perturb = (-dot * s[0] / yy, -dot * s[1] / yy)
    residual = (w[0] + perturb[0], w[1] + perturb[1])
    need(residual[0] * s[0] + residual[1] * s[1] == 0,
         "fixture zeroing")
    return {
        "name": name,
        "w": [str(w[0]), str(w[1])], "S": [str(s[0]), str(s[1])],
        "C": str(dot), "W": str(ww), "Y": str(yy),
        "relative_zeroing_radius_squared": str(radius),
        "zeroing_perturbation": [str(perturb[0]), str(perturb[1])],
        "residual_attachment": "0/1",
    }


FIXTURES = (
    ("axis", (Fraction(2), Fraction(3)), (Fraction(1), Fraction(0))),
    ("diagonal", (Fraction(5, 2), Fraction(-1)), (Fraction(1), Fraction(2))),
    ("near_orthogonal", (Fraction(1), Fraction(1)),
     (Fraction(1), Fraction(-1))),
    ("negative_attachment", (Fraction(-3), Fraction(2)),
     (Fraction(2), Fraction(1))),
)


def row_record(row: dict[str, Any]) -> dict[str, Any]:
    c = interval(row["source_scalar_C_interval"])
    w = interval(row["projected_source_norm_squared_interval"])
    y = frac(row["projected_output_norm_squared"])
    rho = interval(row["attachment_cosine_squared_interval"])
    need(w[0] > 0 and y > 0 and rho[0] > 0 and rho[1] < Fraction(9, 100),
         "parent row does not meet radius audit")
    return {
        "scale": int(row["scale"]), "H": int(row["H"]),
        "Q": int(row["Q"]), "kernel_exponent": int(row["kernel_exponent"]),
        "source_scalar_C_interval": itext(c),
        "source_norm_squared_interval": itext(w),
        "signal_norm_squared": str(y),
        "relative_zeroing_radius_squared_interval": itext(rho),
        "zeroing_radius_upper_less_than": "3/10",
        "zeroing_radius_squared_upper_less_than": "9/100",
        "ten_percent_radius_squared": "1/100",
        "information_model_adversary": True,
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows = [row_record(row) for row in parent["payload"]["rows"]]
    below_ten = sum(interval(row["relative_zeroing_radius_squared_interval"])[1]
                    < Fraction(1, 100) for row in rows)
    below_thirty = sum(interval(row["relative_zeroing_radius_squared_interval"])[1]
                       < Fraction(9, 100) for row in rows)
    need(below_ten == 6 and below_thirty == 12, "radius census")
    fixtures = [fixture_record(name, w, s) for name, w, s in FIXTURES]
    return {
        "schema": SCHEMA,
        "exact_theorem": {
            "hyperplane": "H_S={u:<u,S>=0}",
            "distance_squared": "dist(w,H_S)^2=C^2/Y",
            "minimizer": "w_star=w-(C/Y)S",
            "relative_distance_squared": "dist(w,H_S)^2/W=C^2/(WY)=rho^2",
            "zeroing_identity": "<w_star,S>=0",
            "uniqueness": "unique minimum-norm perturbation when S is nonzero",
            "scope": "Hilbert-space source representative; not an admissible-source theorem",
        },
        "parent_lock": {
            "schema": PARENT_SCHEMA, "code_sha256": PARENT_CODE_SHA256,
            "result_sha256": PARENT_RESULT_SHA256, "rows": 12,
        },
        "finite_audit": {
            "rows": 12, "positive_radius_rows": 12,
            "relative_radius_upper_below_3_over_10": below_thirty,
            "relative_radius_upper_below_1_over_10": below_ten,
            "fixed_power_credit": 0,
            "physical_admissibility": "NOT_ESTABLISHED",
        },
        "fixtures": fixtures,
        "rows": rows,
        "firewall": {
            "TPC283_ZEROING_RADIUS": "PROVED_EXACT",
            "TPC283_FINITE_VULNERABILITY": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC283_UNRESTRICTED_ADVERSARY": "INFORMATION_MODEL_ONLY",
            "TPC283_ADMISSIBLE_LITERAL_SOURCE_STABILITY": "OPEN",
            "TPC283_FIXED_POWER_CREDIT": 0,
            "TPC283_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC283_FULL_GATE_B": "OPEN",
            "TPC283_TWIN_PRIME_RESULT": "NONE",
            "TPC283_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload(load_parent())
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
    need(data == document(), "certificate is not reproducible")
    p = data["payload"]
    need(p["finite_audit"] == {
        "fixed_power_credit": 0, "physical_admissibility": "NOT_ESTABLISHED",
        "positive_radius_rows": 12,
        "relative_radius_upper_below_1_over_10": 6,
        "relative_radius_upper_below_3_over_10": 12, "rows": 12,
    }, "audit census")
    need(len(p["fixtures"]) == 4 and len(p["rows"]) == 12,
         "certificate census")
    print("TPC283_CERTIFICATE=PASS theorem=EXACT_ZEROING_RADIUS rows=12 "
          "under_30_percent=12 under_10_percent=6 fixed_power_credit=0")


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
        raise SystemExit("TPC283_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
