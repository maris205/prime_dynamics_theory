#!/usr/bin/env python3
"""TPC-272: exact correlation-margin identities and a conditional budget compiler."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-272-correlation-margin-budget-compiler"
RESULT = PROJECT / "results/tpc272_certificate.json"
UPSTREAM_RESULT = ROOT / "papers/tpc-271-phase-radius-decoupling/results/tpc271_certificate.json"
UPSTREAM_PAYLOAD_SHA256 = "1f573ae367c3e93b32249c031663b7c5d0e3ce71924dd18ae41e8efb61a590bd"
STATUS = "PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER"
ROUND2_CLUE = "AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION"


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


Interval = tuple[Fraction, Fraction]


def fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    return Fraction(str(value))


def interval(values: object, positive: bool = True) -> Interval:
    need(isinstance(values, list) and len(values) == 2, "interval shape")
    lo, hi = fraction(values[0]), fraction(values[1])
    need(lo <= hi, "interval ordering")
    if positive:
        need(0 < lo, "positive interval")
    return lo, hi


def divide(left: Interval, right: Interval) -> Interval:
    need(left[0] >= 0 and right[0] > 0, "positive division")
    return left[0] / right[1], left[1] / right[0]


def reciprocal(value: Interval) -> Interval:
    return divide((Fraction(1), Fraction(1)), value)


def exact_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_text(value: Interval) -> list[str]:
    return [exact_text(value[0]), exact_text(value[1])]


def sixth(value: Fraction) -> Fraction:
    return value ** 6


def upstream() -> dict[str, Any]:
    raw = UPSTREAM_RESULT.read_bytes()
    data = json.loads(raw)
    need(data.get("payload_sha256") == UPSTREAM_PAYLOAD_SHA256,
         "TPC271 payload provenance")
    payload = data.get("payload")
    need(isinstance(payload, dict), "TPC271 payload")
    canonical = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(canonical).hexdigest() == UPSTREAM_PAYLOAD_SHA256,
         "TPC271 payload digest")
    return payload


def margin_classification(m6: Interval) -> str:
    one_eighth = sixth(Fraction(1, 8))
    one_thirty_second = sixth(Fraction(1, 32))
    if m6[0] > one_eighth:
        return "MARGIN_ABOVE_ONE_EIGHTH"
    if m6[0] > one_thirty_second:
        return "MARGIN_BETWEEN_ONE_EIGHTH_AND_ONE_THIRTY_SECOND"
    if m6[1] < one_thirty_second:
        return "MARGIN_BELOW_ONE_THIRTY_SECOND"
    return "MARGIN_UNRESOLVED_AT_ONE_THIRTY_SECOND"


def row_record(row: dict[str, Any]) -> dict[str, Any]:
    xi_c = interval(row["signed_scalar_normalized_interval"])
    xi = interval(row["endpoint_normalized_sixth_interval"])
    m6 = divide(xi_c, xi)
    amplification = reciprocal(m6)
    need(row.get("phase") == "NEGATIVE_REAL_AXIS", "upstream phase lock")
    need(interval(row["residual_scalar_interval"], positive=False)[1] < 0,
         "upstream signed interval")
    return {
        "scale": row["scale"],
        "profile_theta": row["profile_theta"],
        "role": row["role"],
        "phase": row["phase"],
        "margin_sixth_interval": interval_text(m6),
        "amplification_interval": interval_text(amplification),
        "margin_classification": margin_classification(m6),
        "phase_sign_locked": True,
        "positive_denominators_certified": True,
        "identity": "m^6=Xi_C/Xi and amplification=Xi/Xi_C=m^(-6)",
    }


def dyadic_record(low: dict[str, Any], high: dict[str, Any]) -> dict[str, Any]:
    low_m = interval(low["margin_sixth_interval"])
    high_m = interval(high["margin_sixth_interval"])
    ratio = divide(high_m, low_m)
    threshold = sixth(Fraction(1, 32))
    if ratio[1] < threshold:
        classification = "MARGIN_COLLAPSE_BELOW_ONE_THIRTY_SECOND"
    elif ratio[0] > sixth(Fraction(4)):
        classification = "MARGIN_RISE_ABOVE_FOUR"
    else:
        classification = "NO_EXTREME_MARGIN_RATIO_THRESHOLD"
    return {
        "low_scale": low["scale"],
        "high_scale": high["scale"],
        "label": f"{low['scale']}->{high['scale']}",
        "margin_sixth_ratio_interval": interval_text(ratio),
        "margin_ratio_classification": classification,
        "phase_sign_low": low["phase"],
        "phase_sign_high": high["phase"],
        "phase_sign_preserved": low["phase"] == high["phase"] == "NEGATIVE_REAL_AXIS",
        "sixth_power_threshold": "(1/32)^6",
        "positive_denominators_certified": True,
    }


def budget_record(sigma_c: Fraction) -> dict[str, str]:
    gate_gap = sigma_c - Fraction(1, 400)
    return {
        "scalar_effective_saving": exact_text(sigma_c),
        "target_gap": exact_text(Fraction(1, 400)),
        "maximum_allowed_margin_loss_eta": exact_text(gate_gap),
        "strict_condition": f"eta < {exact_text(gate_gap)}",
        "interpretation": "conditional; no source-level estimate is supplied here",
    }


def build_payload() -> dict[str, Any]:
    source = upstream()
    source_rows = source["base_rows"] + source["profile_rows"]
    rows = [row_record(row) for row in source_rows]
    by_scale = {row["scale"]: row for row in rows if row["profile_theta"] == "0/1"}
    dyadic = [dyadic_record(by_scale[a], by_scale[b])
              for a, b in ((64, 128), (96, 192), (128, 256), (192, 384))]
    need(dyadic[1]["margin_ratio_classification"] ==
         "MARGIN_COLLAPSE_BELOW_ONE_THIRTY_SECOND", "margin collapse")
    need(all(item["phase_sign_preserved"] for item in dyadic),
         "phase preservation")
    return {
        "schema": "TPC272_CORRELATION_MARGIN_BUDGET_CERTIFICATE_V1",
        "parameters": {
            "upstream": "TPC-271 finite phase-radius certificate",
            "upstream_payload_sha256": UPSTREAM_PAYLOAD_SHA256,
            "margin_definition": "m=abs(C_perp)/R",
            "rational_coordinate": "m^6=Xi_C/Xi",
            "target_exponents": "E0=5/3, E*=1997/1200, gap=1/400",
            "registered_scales": [64, 96, 128, 192, 256, 384],
        },
        "conditional_theorem": {
            "statement": "signed scalar saving sigma_c and m>=c*x^(-eta) imply endpoint saving sigma_c-eta",
            "endpoint_rule": "|C|+R <= (1+c^(-1))*x^(E0-sigma_c+eta+epsilon)",
            "strict_gate": "sigma_c-eta>1/400",
            "status": "PROVED_CONDITIONAL",
        },
        "finite_theorem": {
            "rows": len(rows),
            "base_rows": 6,
            "profile_rows": 3,
            "dyadic_rows": len(dyadic),
            "margin_identity": "PROVED_EXACT_FINITE",
            "sharp_two_dimensional_converse": "PROVED_EXACT",
            "finite_margin_audit": "NUMERICALLY_CERTIFIED",
            "phase_pattern": "ALL_NEGATIVE_REAL_AXIS",
            "collapse_pair": "96->192",
        },
        "rows": rows,
        "dyadic_margin_ratios": dyadic,
        "budget_examples": [budget_record(Fraction(1, 400)),
                            budget_record(Fraction(1, 200)),
                            budget_record(Fraction(1, 100))],
        "converse": {
            "dimension": 2,
            "realization": "w=(sqrt(W),0), g=sqrt(G)*(m,sqrt(1-m^2))",
            "margin_range": "0<m<=1",
            "conclusion": "phase sign alone gives no positive lower margin",
            "status": "PROVED_EXACT",
        },
        "firewall": {
            "TPC272_CONDITIONAL_BUDGET_COMPILER": "PROVED_CONDITIONAL",
            "TPC272_MARGIN_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC272_SHARP_CONVERSE": "PROVED_EXACT",
            "TPC272_FINITE_MARGIN_AUDIT": "NUMERICALLY_CERTIFIED",
            "TPC272_SOURCE_LEVEL_MARGIN": "OPEN_ASYMPTOTIC",
            "TPC272_SOURCE_LEVEL_SIGNED_SCALAR": "OPEN_ASYMPTOTIC",
            "TPC272_FIXED_POWER_CREDIT": 0,
            "TPC272_ARITHMETIC_ADVANCE": "NO",
            "TPC272_L2": "NONE",
            "TPC272_FULL_GATE_B": "OPEN",
            "TPC272_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC272_TWIN_PRIME_RESULT": "NONE",
            "TPC272_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    canonical = json.dumps(payload, ensure_ascii=True, sort_keys=True,
                            separators=(",", ":")) + "\n"
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(document(), ensure_ascii=True, sort_keys=True,
                                 separators=(",", ":")) + "\n", encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    expected = document()
    need(stored == expected, "certificate mismatch")
    canonical = json.dumps(stored, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")) + "\n"
    need(raw == canonical, "certificate not canonical")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC272_CERTIFICATE=PASS "
          f"rows={theorem['rows']} dyadic_rows={theorem['dyadic_rows']} "
          f"collapse_pair={theorem['collapse_pair']} "
          "conditional_gate=SIGMA_MINUS_ETA_GREATER_THAN_1_OVER_400")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC272_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
