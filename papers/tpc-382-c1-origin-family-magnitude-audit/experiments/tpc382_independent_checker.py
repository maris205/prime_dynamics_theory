#!/usr/bin/env python3
"""Independent checker for the TPC-382 locked-certificate aggregation.

This file intentionally does not import the producer.  It reconstructs the
parent row sets and the finite spread/contrast statistics from scratch.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-382-c1-origin-family-magnitude-audit"
CERTIFICATE = PROJECT / "results/tpc382_certificate.json"
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
QS = (512, 2048, 8192)
CAP = 0.01

SPECS = {
    "TPC379": {
        "code": ROOT / "papers/tpc-379-c1-crossholdout-law-control/code/tpc379_c1_crossholdout_law_control.py",
        "certificate": ROOT / "papers/tpc-379-c1-crossholdout-law-control/results/tpc379_certificate.json",
        "code_sha256": "5f4a32af562127a158dcb9232ecc6e380717c27145857b1f814734c5d0597b82",
        "certificate_sha256": "a41800cb32f59b2d025a808b92fb52567fbef661181f89889074b861c40504c7",
        "schema": "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL",
        "count": 1024, "origins": (1200001, 1208021, 1216041)},
    "TPC380": {
        "code": ROOT / "papers/tpc-380-c1-law-control-count-replay/code/tpc380_c1_law_control_count_replay.py",
        "certificate": ROOT / "papers/tpc-380-c1-law-control-count-replay/results/tpc380_certificate.json",
        "code_sha256": "8cb9e8373b51571b32fdbb0c6e1115274366b339371c59b1711ab166da7874ce",
        "certificate_sha256": "c80dbfab3d375ac63b12c46dc2aaedc9718c21be0d8768d6e682c292619ddeeb",
        "schema": "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_COUNT_REPLAY",
        "count": 2048, "origins": (1300001, 1308021, 1316041)},
    "TPC381": {
        "code": ROOT / "papers/tpc-381-c1-origin-family-replay/code/tpc381_c1_origin_family_replay.py",
        "certificate": ROOT / "papers/tpc-381-c1-origin-family-replay/results/tpc381_certificate.json",
        "code_sha256": "107932b1671c12baaabad0a53ff68a4944f6f54d45e88cfa4212468db0b7b354",
        "certificate_sha256": "c217a475d0e0a0aa440840e02f2e73bd0e0ba52f478143540dcd8772c4742c2b",
        "schema": "TPC381_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY",
        "count": 2048, "origins": (1400001, 1408021, 1416041)},
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def sha(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 5e-12) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
    need(math.isfinite(target) and math.isfinite(actual) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual),
                                                  abs(target)),
         label + " mismatch")


def load(label: str) -> tuple[dict[str, Any], bytes]:
    spec = SPECS[label]
    need(spec["code"].is_file() and spec["certificate"].is_file(),
         label + " files")
    need(sha(spec["code"].read_bytes()) == spec["code_sha256"],
         label + " code hash")
    raw = spec["certificate"].read_bytes()
    need(sha(raw) == spec["certificate_sha256"], label + " certificate hash")
    doc = json.loads(raw)
    need(raw == canonical(doc), label + " canonical")
    need(doc.get("certificate_version") == 1 and
         doc.get("claim_status") == spec["status"], label + " header")
    payload = doc.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == spec["schema"]
         and payload.get("status") == spec["status"], label + " schema")
    need(doc.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), label + " payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("window_count") == spec["count"] and
         protocol.get("origins") == list(spec["origins"]) and
         protocol.get("q_anchors") == list(QS) and
         protocol.get("laws") == list(LAWS), label + " protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 36, label + " rows")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), label + " row hash")
    keys = {(row.get("origin"), row.get("Q"), row.get("law"))
            for row in rows}
    need(keys == {(o, q, law) for o in spec["origins"]
                  for q in QS for law in LAWS}, label + " row keys")
    return payload, raw


def parent_lock_check(payload: dict[str, Any]) -> None:
    locks = payload.get("parent_locks")
    need(isinstance(locks, list) and len(locks) == 3, "parent lock list")
    for lock, label in zip(locks, ("TPC379", "TPC380", "TPC381")):
        spec = SPECS[label]
        need(lock.get("label") == label and
             lock.get("code_sha256") == spec["code_sha256"] and
             lock.get("certificate_sha256") == spec["certificate_sha256"] and
             lock.get("schema") == spec["schema"] and
             lock.get("status") == spec["status"] and
             lock.get("count") == spec["count"] and
             lock.get("origins") == list(spec["origins"]),
             label + " embedded lock")


def rows(payload: dict[str, Any], law: str, q0: int) -> list[dict[str, Any]]:
    selected = [row for row in payload["rows"]
                if row.get("law") == law and row.get("Q") == q0]
    selected.sort(key=lambda row: row["origin"])
    need(len(selected) == 3, "origin cardinality")
    return selected


def calculate(values: list[float]) -> tuple[float, float, float, float, bool]:
    need(values and all(math.isfinite(x) and x >= 0.0 for x in values),
         "finite metric values")
    lo, hi = min(values), max(values)
    mean = sum(values) / len(values)
    spread = hi - lo
    relative = spread / mean if mean else float("inf")
    return lo, hi, mean, relative, relative <= CAP


def verify_cell(item: dict[str, Any], values: list[float], label: str) -> None:
    lo, hi, mean, relative, stable = calculate(values)
    need(item.get("value_count") == len(values), label + " count")
    close(lo, item.get("minimum"), label + " min")
    close(hi, item.get("maximum"), label + " max")
    close(mean, item.get("mean"), label + " mean")
    close(hi - lo, item.get("absolute_spread"), label + " spread")
    close(relative, item.get("relative_spread"), label + " relative")
    need(item.get("within_one_percent") is stable, label + " flag")


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        target, _ = load_certificate_only()
        parent_lock_check(target)
        payloads = {label: load(label)[0] for label in SPECS}
        same_items = {(item["law"], item["Q"]): item
                      for item in target["same_count_cells"]}
        scale_items = {(item["law"], item["Q"]): item
                       for item in target["scale_control_cells"]}
        contrast_items = {(item["law"], item["Q"]): item
                          for item in target["scale_contrasts"]}
        need(len(same_items) == 12 and len(scale_items) == 12 and
             len(contrast_items) == 12, "cell census")
        stable = 0
        over = 0
        for law in LAWS:
            for q0 in QS:
                values = []
                for label in ("TPC380", "TPC381"):
                    values.extend(float(row["band"]["spectral"])
                                  for row in rows(payloads[label], law, q0))
                item = same_items[(law, q0)]
                verify_cell(item, values, "same " + law + str(q0))
                stable += int(item["within_one_percent"])
                if law != "all_plus":
                    over += int(not item["within_one_percent"])
                scale_values = [float(row["band"]["spectral"])
                                for row in rows(payloads["TPC379"], law, q0)]
                scale_item = scale_items[(law, q0)]
                verify_cell(scale_item, scale_values, "scale " + law + str(q0))
                scale_mean = sum(scale_values) / len(scale_values)
                same_mean = sum(values) / len(values)
                change = (same_mean - scale_mean) / scale_mean
                citem = contrast_items[(law, q0)]
                close(scale_mean, citem.get("scale_mean"), "scale mean")
                close(same_mean, citem.get("same_count_mean"), "same mean")
                close(change, citem.get("relative_change"), "contrast")
                close(abs(change), citem.get("absolute_relative_change"),
                      "absolute contrast")
                need(citem.get("within_one_percent") is
                     (abs(change) <= CAP), "contrast flag")
        summary = target["phase_summary"]
        need(summary.get("same_count_cells_within_one_percent") == stable == 8,
             "stable census")
        need(summary.get("signed_cells_over_one_percent") == over == 4,
             "signed spread census")
        high = same_items[("all_plus", 8192)]
        need(high["within_one_percent"] is True and
             float(high["relative_spread"]) < 1e-3,
             "all-plus high-Q stability")
        high_contrast = contrast_items[("all_plus", 8192)]
        need(high_contrast["within_one_percent"] is False and
             float(high_contrast["absolute_relative_change"]) > CAP,
             "scale contrast")
        firewall = target.get("claim_firewall", {})
        need(firewall.get("TPC382_ARITHMETIC_ADVANCE") == "NO" and
             firewall.get("TPC382_FIXED_POWER_CREDIT") == 0 and
             firewall.get("TPC382_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC382_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
        need(target.get("round2_clue") ==
             "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN", "clue")
        print("TPC382_INDEPENDENT_CHECK=PASS cells=12 same_values=72 "
              "stable_cells=8 signed_over_1pct=4 scale_refuted=True")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC382_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


def load_certificate_only() -> tuple[dict[str, Any], bytes]:
    raw = CERTIFICATE.read_bytes()
    need(sha(raw) ==
         "1bd35889f40e911aa2faa4f2f5a636583f905a388b0dda0417c1ed031f492b6e",
         "certificate self hash")
    doc = json.loads(raw)
    need(raw == canonical(doc), "target canonical")
    return doc["payload"], raw


if __name__ == "__main__":
    raise SystemExit(main())
