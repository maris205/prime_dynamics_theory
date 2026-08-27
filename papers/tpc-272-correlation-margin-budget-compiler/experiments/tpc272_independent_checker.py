#!/usr/bin/env python3
"""Independent exact replay of the TPC-272 correlation-margin certificate."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-272-correlation-margin-budget-compiler"
RESULT = PROJECT / "results/tpc272_certificate.json"
UPSTREAM = ROOT / "papers/tpc-271-phase-radius-decoupling/results/tpc271_certificate.json"
UPSTREAM_SHA = "1f573ae367c3e93b32249c031663b7c5d0e3ce71924dd18ae41e8efb61a590bd"
STATUS = "PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def f(value: object) -> Fraction:
    return Fraction(str(value))


def bounds(value: object, positive: bool = True) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = f(value[0]), f(value[1])
    need(lo <= hi, "interval order")
    if positive:
        need(lo > 0, "positive interval")
    return lo, hi


def quotient(a: tuple[Fraction, Fraction],
             b: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    need(a[0] >= 0 and b[0] > 0, "quotient sign")
    return a[0] / b[1], a[1] / b[0]


def exact_pair(value: tuple[Fraction, Fraction]) -> list[str]:
    return [f"{value[0].numerator}/{value[0].denominator}",
            f"{value[1].numerator}/{value[1].denominator}"]


def load(path: Path) -> dict:
    raw = path.read_bytes()
    data = json.loads(raw)
    canonical = (json.dumps(data, ensure_ascii=True, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "noncanonical JSON: " + path.name)
    return data


def check() -> None:
    upstream = load(UPSTREAM)
    up_payload = upstream["payload"]
    up_canonical = (json.dumps(up_payload, ensure_ascii=True, sort_keys=True,
                               separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(up_canonical).hexdigest() == UPSTREAM_SHA,
         "upstream provenance")
    data = load(RESULT)
    need(data["claim_status"] == STATUS, "status")
    payload = data["payload"]
    need(payload["schema"] == "TPC272_CORRELATION_MARGIN_BUDGET_CERTIFICATE_V1",
         "schema")
    payload_canonical = (json.dumps(payload, ensure_ascii=True, sort_keys=True,
                                     separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(payload_canonical).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["parameters"]["upstream_payload_sha256"] == UPSTREAM_SHA,
         "stored upstream digest")
    rows = up_payload["base_rows"] + up_payload["profile_rows"]
    actual = payload["rows"]
    need(len(actual) == len(rows) == 9, "row count")
    expected_classes = {
        (64, "0/1"): "MARGIN_ABOVE_ONE_EIGHTH",
        (96, "0/1"): "MARGIN_ABOVE_ONE_EIGHTH",
        (128, "0/1"): "MARGIN_BETWEEN_ONE_EIGHTH_AND_ONE_THIRTY_SECOND",
        (192, "0/1"): "MARGIN_BELOW_ONE_THIRTY_SECOND",
        (256, "0/1"): "MARGIN_BETWEEN_ONE_EIGHTH_AND_ONE_THIRTY_SECOND",
        (384, "0/1"): "MARGIN_BELOW_ONE_THIRTY_SECOND",
        (96, "1/2"): "MARGIN_ABOVE_ONE_EIGHTH",
        (128, "1/2"): "MARGIN_ABOVE_ONE_EIGHTH",
        (256, "1/2"): "MARGIN_BELOW_ONE_THIRTY_SECOND",
    }
    eighth6 = f(1) / 8**6
    thirtysecond6 = f(1) / 32**6
    for source, stored in zip(rows, actual):
        key = (source["scale"], source["profile_theta"])
        need(stored["scale"] == source["scale"] and
             stored["profile_theta"] == source["profile_theta"], "row key")
        scalar = bounds(source["signed_scalar_normalized_interval"])
        endpoint = bounds(source["endpoint_normalized_sixth_interval"])
        expected = quotient(scalar, endpoint)
        need(stored["margin_sixth_interval"] == exact_pair(expected),
             "margin recomputation")
        amplification = quotient((f(1), f(1)), expected)
        need(stored["amplification_interval"] == exact_pair(amplification),
             "amplification recomputation")
        need(stored["phase"] == "NEGATIVE_REAL_AXIS" and
             stored["phase_sign_locked"] is True and
             stored["margin_classification"] == expected_classes[key],
             "row semantics")
        if expected[0] > eighth6:
            need(stored["margin_classification"] == "MARGIN_ABOVE_ONE_EIGHTH",
                 "eighth threshold")
        elif expected[0] > thirtysecond6:
            need(stored["margin_classification"] ==
                 "MARGIN_BETWEEN_ONE_EIGHTH_AND_ONE_THIRTY_SECOND",
                 "middle threshold")
        else:
            need(expected[1] < thirtysecond6 and stored["margin_classification"] ==
                 "MARGIN_BELOW_ONE_THIRTY_SECOND", "low threshold")
    dyadic = payload["dyadic_margin_ratios"]
    need(len(dyadic) == 4, "dyadic count")
    expected_labels = ["64->128", "96->192", "128->256", "192->384"]
    expected_classes_d = [
        "NO_EXTREME_MARGIN_RATIO_THRESHOLD",
        "MARGIN_COLLAPSE_BELOW_ONE_THIRTY_SECOND",
        "NO_EXTREME_MARGIN_RATIO_THRESHOLD",
        "MARGIN_RISE_ABOVE_FOUR",
    ]
    bases = {r["scale"]: r for r in actual if r["profile_theta"] == "0/1"}
    for item, label, cls in zip(dyadic, expected_labels, expected_classes_d):
        low, high = (int(x) for x in label.split("->"))
        ratio = quotient(bounds(bases[high]["margin_sixth_interval"]),
                         bounds(bases[low]["margin_sixth_interval"]))
        need(item["label"] == label and
             item["margin_sixth_ratio_interval"] == exact_pair(ratio) and
             item["margin_ratio_classification"] == cls and
             item["phase_sign_preserved"] is True, "dyadic replay")
    theorem = payload["conditional_theorem"]
    need(theorem["status"] == "PROVED_CONDITIONAL" and
         theorem["strict_gate"] == "sigma_c-eta>1/400", "conditional theorem")
    converse = payload["converse"]
    need(converse["status"] == "PROVED_EXACT" and
         converse["margin_range"] == "0<m<=1", "converse")
    firewall = payload["firewall"]
    need(firewall["TPC272_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC272_SOURCE_LEVEL_MARGIN"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC272_FULL_GATE_B"] == "OPEN", "claim firewall")
    print("TPC272_INDEPENDENT_CHECK=PASS rows=9 dyadic_rows=4 "
          "margin_identity=EXACT collapse_pair=96->192 "
          "source_level_margin=OPEN")


if __name__ == "__main__":
    try:
        check()
    except Exception as exc:
        print("TPC272_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
