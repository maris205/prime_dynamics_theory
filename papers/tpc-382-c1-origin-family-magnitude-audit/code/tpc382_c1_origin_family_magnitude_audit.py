#!/usr/bin/env python3
"""TPC-382: a finite magnitude audit over the sealed c=1 panels.

The experiment is deliberately a certificate-level aggregation.  It does not
select new origins or read a response.  Two N=2048 parent panels are merged
under a predeclared one-percent spread rule, while the N=1024 panel is kept as
an explicitly labelled scale control.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-382-c1-origin-family-magnitude-audit"
RESULT = PROJECT / "results/tpc382_certificate.json"

LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
QS = (512, 2048, 8192)
RELATIVE_SPREAD_CAP = 0.01
SCALE_CONTRAST_CAP = 0.01
HIGH_Q = 8192

PARENTS = (
    {
        "label": "TPC379",
        "code": ROOT / (
            "papers/tpc-379-c1-crossholdout-law-control/code/"
            "tpc379_c1_crossholdout_law_control.py"),
        "certificate": ROOT / (
            "papers/tpc-379-c1-crossholdout-law-control/results/"
            "tpc379_certificate.json"),
        "code_sha256":
            "5f4a32af562127a158dcb9232ecc6e380717c27145857b1f814734c5d0597b82",
        "certificate_sha256":
            "a41800cb32f59b2d025a808b92fb52567fbef661181f89889074b861c40504c7",
        "schema": "TPC379_C1_CROSSHOLDOUT_LAW_CONTROL_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL",
        "count": 1024,
        "origins": [1200001, 1208021, 1216041],
    },
    {
        "label": "TPC380",
        "code": ROOT / (
            "papers/tpc-380-c1-law-control-count-replay/code/"
            "tpc380_c1_law_control_count_replay.py"),
        "certificate": ROOT / (
            "papers/tpc-380-c1-law-control-count-replay/results/"
            "tpc380_certificate.json"),
        "code_sha256":
            "8cb9e8373b51571b32fdbb0c6e1115274366b339371c59b1711ab166da7874ce",
        "certificate_sha256":
            "c80dbfab3d375ac63b12c46dc2aaedc9718c21be0d8768d6e682c292619ddeeb",
        "schema": "TPC380_C1_LAW_CONTROL_COUNT_REPLAY_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_COUNT_REPLAY",
        "count": 2048,
        "origins": [1300001, 1308021, 1316041],
    },
    {
        "label": "TPC381",
        "code": ROOT / (
            "papers/tpc-381-c1-origin-family-replay/code/"
            "tpc381_c1_origin_family_replay.py"),
        "certificate": ROOT / (
            "papers/tpc-381-c1-origin-family-replay/results/"
            "tpc381_certificate.json"),
        "code_sha256":
            "107932b1671c12baaabad0a53ff68a4944f6f54d45e88cfa4212468db0b7b354",
        "certificate_sha256":
            "c217a475d0e0a0aa440840e02f2e73bd0e0ba52f478143540dcd8772c4742c2b",
        "schema": "TPC381_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY",
        "count": 2048,
        "origins": [1400001, 1408021, 1416041],
    },
)

CLAIM_FIREWALL = {
    "TPC382_PARENT_LOCKS": "PROVED_EXACT_FINITE_HASHED",
    "TPC382_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_CERTIFICATE_BLIND",
    "TPC382_SAME_N_ORIGIN_MAGNITUDE_AUDIT":
        "NUMERICALLY_CERTIFIED_FINITE_72_VALUES",
    "TPC382_ALL_PLUS_HIGH_Q_STABILITY_1PCT":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC382_LAW_DEPENDENT_MAGNITUDE_SPREAD":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC382_CROSS_COUNT_MAGNITUDE_INVARIANCE": "REFUTED_FINITE_SCOPED",
    "TPC382_ORIGIN_UNIFORMITY": "OPEN",
    "TPC382_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC382_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC382_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC382_SOURCE_UNIFORM_L2": "OPEN",
    "TPC382_ARITHMETIC_ADVANCE": "NO",
    "TPC382_FIXED_POWER_CREDIT": 0,
    "TPC382_FULL_GATE_B": "OPEN",
    "TPC382_TWIN_PRIME_RESULT": "NONE",
}


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


def show(value: float) -> str:
    return format(float(value), ".17g")


def finite_tree(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and finite_tree(v)
                   for k, v in value.items())
    if isinstance(value, list):
        return all(finite_tree(v) for v in value)
    return True


def load_parent(spec: dict[str, Any]) -> dict[str, Any]:
    need(spec["code"].is_file() and spec["certificate"].is_file(),
         spec["label"] + " files")
    need(digest(spec["code"].read_bytes()) == spec["code_sha256"],
         spec["label"] + " code provenance")
    raw = spec["certificate"].read_bytes()
    need(digest(raw) == spec["certificate_sha256"],
         spec["label"] + " certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), spec["label"] + " canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == spec["status"],
         spec["label"] + " header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == spec["schema"]
         and payload.get("status") == spec["status"],
         spec["label"] + " payload header")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), spec["label"] + " payload hash")
    protocol = payload.get("protocol", {})
    need(protocol.get("window_count") == spec["count"] and
         protocol.get("origins") == spec["origins"] and
         protocol.get("q_anchors") == list(QS) and
         protocol.get("laws") == list(LAWS), spec["label"] + " protocol")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 36,
         spec["label"] + " row count")
    need(payload.get("row_digest") == hashlib.sha256(
        canonical(rows)).hexdigest(), spec["label"] + " row digest")
    expected = {(origin, q0, law) for origin in spec["origins"]
                for q0 in QS for law in LAWS}
    need({(row.get("origin"), row.get("Q"), row.get("law"))
          for row in rows} == expected, spec["label"] + " row keys")
    for row in rows:
        value = float(row["band"]["spectral"])
        need(math.isfinite(value) and value >= 0.0,
             spec["label"] + " finite spectral row")
    return payload


def stats(values: list[float]) -> dict[str, Any]:
    need(len(values) > 0 and all(math.isfinite(x) and x >= 0.0
                                 for x in values), "finite values")
    minimum, maximum = min(values), max(values)
    mean = sum(values) / len(values)
    spread = maximum - minimum
    relative = spread / mean if mean else float("inf")
    return {
        "value_count": len(values),
        "minimum": show(minimum),
        "maximum": show(maximum),
        "mean": show(mean),
        "absolute_spread": show(spread),
        "relative_spread": show(relative),
        "within_one_percent": bool(relative <= RELATIVE_SPREAD_CAP),
    }


def rows_for(payload: dict[str, Any], law: str, q0: int) -> list[dict[str, Any]]:
    rows = [row for row in payload["rows"]
            if row["law"] == law and row["Q"] == q0]
    rows.sort(key=lambda row: row["origin"])
    need(len(rows) == 3, "three origin rows")
    return rows


def cell(label: str, payload: dict[str, Any], law: str, q0: int,
         cohort: str) -> dict[str, Any]:
    rows = rows_for(payload, law, q0)
    values = [float(row["band"]["spectral"]) for row in rows]
    result = stats(values)
    result.update({
        "cohort": cohort,
        "panel": label,
        "count": int(payload["protocol"]["window_count"]),
        "Q": q0,
        "law": law,
        "origins": [int(row["origin"]) for row in rows],
        "values": [show(value) for value in values],
    })
    return result


def combined_cell(payloads: list[tuple[str, dict[str, Any]]], law: str,
                  q0: int) -> dict[str, Any]:
    values: list[float] = []
    provenance: list[dict[str, Any]] = []
    for label, payload in payloads:
        rows = rows_for(payload, law, q0)
        values.extend(float(row["band"]["spectral"]) for row in rows)
        provenance.append({
            "panel": label,
            "origins": [int(row["origin"]) for row in rows],
        })
    result = stats(values)
    result.update({
        "cohort": "same_count_N2048",
        "panel_count": len(payloads),
        "count": 2048,
        "Q": q0,
        "law": law,
        "provenance": provenance,
        "values": [show(value) for value in values],
    })
    return result


def contrast(scale: dict[str, Any], same: dict[str, Any], law: str,
             q0: int) -> dict[str, Any]:
    scale_mean = float(scale["mean"])
    same_mean = float(same["mean"])
    change = (same_mean - scale_mean) / scale_mean
    return {
        "law": law,
        "Q": q0,
        "scale_panel": "TPC379_N1024",
        "same_count_panel": "TPC380_TPC381_N2048",
        "scale_mean": show(scale_mean),
        "same_count_mean": show(same_mean),
        "relative_change": show(change),
        "absolute_relative_change": show(abs(change)),
        "within_one_percent": bool(abs(change) <= SCALE_CONTRAST_CAP),
    }


def build_payload() -> dict[str, Any]:
    loaded = {spec["label"]: load_parent(spec) for spec in PARENTS}
    same_parents = [("TPC380", loaded["TPC380"]),
                    ("TPC381", loaded["TPC381"])]
    same_cells = [combined_cell(same_parents, law, q0)
                  for law in LAWS for q0 in QS]
    scale_cells = [cell("TPC379", loaded["TPC379"], law, q0,
                         "scale_control_N1024")
                   for law in LAWS for q0 in QS]
    same_by_key = {(item["law"], item["Q"]): item for item in same_cells}
    scale_by_key = {(item["law"], item["Q"]): item for item in scale_cells}
    contrasts = [contrast(scale_by_key[(law, q0)],
                          same_by_key[(law, q0)], law, q0)
                 for law in LAWS for q0 in QS]
    all_plus_high_q = same_by_key[("all_plus", HIGH_Q)]
    signed_over_cap = [item for item in same_cells
                       if item["law"] != "all_plus" and
                       not item["within_one_percent"]]
    scale_refutation = [item for item in contrasts
                        if item["law"] == "all_plus" and
                        item["Q"] == HIGH_Q][0]
    parent_locks = []
    for spec in PARENTS:
        parent_locks.append({
            "label": spec["label"],
            "code_sha256": spec["code_sha256"],
            "certificate_sha256": spec["certificate_sha256"],
            "schema": spec["schema"],
            "status": spec["status"],
            "count": spec["count"],
            "origins": spec["origins"],
        })
    return {
        "schema": "TPC382_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT_V1",
        "status": "NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT",
        "parent_locks": parent_locks,
        "selection_protocol": {
            "parent_panels_fixed_before_metric_read": True,
            "parent_hashes_fixed_before_aggregation": True,
            "response_used_for_selection": False,
            "metric_used_for_selection": False,
            "same_count_labels": ["TPC380", "TPC381"],
            "scale_control_label": "TPC379",
            "laws": list(LAWS),
            "q_anchors": list(QS),
            "relative_spread_cap": show(RELATIVE_SPREAD_CAP),
            "scale_contrast_cap": show(SCALE_CONTRAST_CAP),
            "high_q": HIGH_Q,
        },
        "protocol": {
            "same_count": 2048,
            "same_count_panels": ["TPC380", "TPC381"],
            "scale_control_count": 1024,
            "scale_control_panel": "TPC379",
            "laws": list(LAWS),
            "q_anchors": list(QS),
            "cells_per_panel": 12,
            "same_count_value_count": 72,
            "scale_control_value_count": 36,
            "metric": "normalized c=1 band spectral value",
            "spread_definition": "(max-min)/mean across locked origin values",
            "scale_definition":
                "(mean_N2048 - mean_N1024)/mean_N1024 at matched law and Q",
        },
        "same_count_cells": same_cells,
        "scale_control_cells": scale_cells,
        "scale_contrasts": contrasts,
        "phase_summary": {
            "same_count_values": 72,
            "same_count_cells": len(same_cells),
            "same_count_cells_within_one_percent": sum(
                item["within_one_percent"] for item in same_cells),
            "all_plus_high_q_relative_spread":
                all_plus_high_q["relative_spread"],
            "all_plus_high_q_within_one_percent":
                all_plus_high_q["within_one_percent"],
            "signed_cells_over_one_percent": len(signed_over_cap),
            "signed_cells_over_one_percent_keys": [
                [item["law"], item["Q"]] for item in signed_over_cap],
            "all_plus_high_q_scale_absolute_relative_change":
                scale_refutation["absolute_relative_change"],
            "all_plus_high_q_scale_within_one_percent":
                scale_refutation["within_one_percent"],
        },
        "finite_audit": {
            "same_count_panel_count": 2,
            "same_count_origins": 6,
            "same_count_laws": len(LAWS),
            "same_count_q_anchors": len(QS),
            "same_count_values": 72,
            "scale_control_values": 36,
            "complete_cartesian_same_count": True,
            "parent_coordinates_already_disjoint": True,
            "one_percent_rule_predeclared": True,
            "arithmetic_advance": "NO",
            "fixed_power_credit": 0,
        },
        "claim_firewall": CLAIM_FIREWALL,
        "round2_clue": "TEST_C1_POOLED_NORMALIZATION_CROSS_ORIGIN",
        "exact_theorem": {
            "label": "FINITE_LOCKED_MAGNITUDE_AGGREGATION_IDENTITY",
            "statement":
                "For the locked parent rows, each reported min, max, mean, "
                "spread, and matched-count contrast is the prescribed finite "
                "arithmetic transform of those rows.",
            "status": "PROVED_EXACT_FINITE_DEFINITIONAL",
        },
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": payload["status"],
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
        "payload": payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        document = build_document()
        need(finite_tree(document), "non-finite document")
        if args.write:
            RESULT.write_bytes(canonical(document))
            print("TPC382_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "certificate replay mismatch")
            summary = document["payload"]["phase_summary"]
            print("TPC382_CERTIFICATE=PASS cells=12 same_values=72 "
                  "stable_cells=%d signed_over_1pct=%d scale_refuted=%s" % (
                      summary["same_count_cells_within_one_percent"],
                      summary["signed_cells_over_one_percent"],
                      not summary["all_plus_high_q_scale_within_one_percent"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC382_CERTIFICATE=FAIL " + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
