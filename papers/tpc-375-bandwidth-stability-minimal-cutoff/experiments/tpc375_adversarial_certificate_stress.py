#!/usr/bin/env python3
"""Adversarial certificate mutations for TPC-375."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-375-bandwidth-stability-minimal-cutoff/results/"
    "tpc375_certificate.json")
SCHEMA = "TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BANDWIDTH_STABILITY"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BAND_CUTOFFS = [0, 1, 2, 3]
EXPECTED_PARENT = [
    [1010001, 2048, 2048, 1, "all_plus"],
    [1010001, 2048, 8192, 1, "all_plus"],
    [1018021, 2048, 2048, 1, "all_plus"],
    [1018021, 2048, 8192, 1, "all_plus"],
    [1026041, 2048, 2048, 1, "all_plus"],
    [1026041, 2048, 8192, 1, "all_plus"],
]


class Rejected(Exception):
    pass


def reject(condition: bool, message: str) -> None:
    if condition:
        raise Rejected(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    reject(document.get("certificate_version") != 1 or
           document.get("claim_status") != STATUS, "header")
    payload = document.get("payload")
    reject(not isinstance(payload, dict) or payload.get("schema") != SCHEMA or
           payload.get("status") != STATUS, "schema/status")
    reject(document.get("payload_sha256") != hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    reject(payload.get("parent_lock") != {
        "base_code_sha256":
        "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9",
        "parent_code_sha256":
        "09851134f9c2d2444c42702b1649e49d259cb9316291ee5b7c275a92b96a9cd0",
        "parent_certificate_sha256":
        "c49310bd080f609f90ee03a74beeda7fbd7ebae0b5f25012a06235f42a047c40",
        "parent_schema": "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1",
        "parent_round2_clue": "TEST_BANDWIDTH_STABILITY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    reject(protocol != {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoffs": BAND_CUTOFFS,
        "band_definition": "sum of layers with block distance <= cutoff",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": [2], "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "component_selection_used": False,
        "panel_complete_before_cutoff_read": True,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
    }, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, 2, "all_plus")
                for o in ORIGINS for q in Q_ANCHORS}
    reject(not isinstance(rows, list) or len(rows) != 9 or
           {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
             r.get("beta"), r.get("law")) for r in rows} != expected,
           "row census")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        reject(row.get("count") != 2048 or row.get("height") != 66 or
               row.get("shell_cardinality", 0) <= 0, "row header")
        reject(set(row.get("bands", {})) != {str(c) for c in BAND_CUTOFFS},
               "band census")
        for component in ("full", "bands"):
            fields = row.get(component, {})
            if component == "bands":
                fields = {name: value for sub in fields.values()
                          for name, value in sub.items()}
            for name, value in fields.items():
                if name != "schur_row_index":
                    reject(not math.isfinite(float(value)), "nonfinite metric")
        mode = row.get("mode", {})
        reject(mode.get("mode_rule") !=
               "largest absolute eigenvalue; minimum mode wins ties" or
               set(mode.get("by_cutoff", {})) !=
               {str(c) for c in BAND_CUTOFFS} or
               float(mode.get("eigen_residual_inf")) > 1.0e-5 or
               float(mode.get("full_mode_norm_error")) > 1.0e-8,
               "mode")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cutoffs") != BAND_CUTOFFS or
           phase.get("band_definition") != "block distance <= cutoff" or
           phase.get("caps") != {"spectral": "0.64000000000000001",
                                  "schur": "0.82999999999999996"},
           "phase header")
    for cutoff in BAND_CUTOFFS:
        key = str(cutoff)
        item = phase.get("by_cutoff", {}).get(key, {})
        failures = [r for r in rows if r["band_failure_flags"][key]]
        schur_failures = [r for r in rows
                          if float(r["bands"][key]["schur"]) > .83]
        expected_failures = [[r["origin"], r["count"], r["Q"],
                              r["kernel_exponent"], r["law"]]
                             for r in failures]
        reject(item.get("cutoff") != cutoff or item.get("rows") != 9 or
               item.get("spectral_cap_violations") != len(failures) or
               item.get("schur_cap_violations") != len(schur_failures) or
               item.get("failure_keys") != expected_failures,
               "phase cutoff")
        for q0 in Q_ANCHORS:
            qitem = phase.get("by_cutoff_q", {}).get(f"{cutoff}:{q0}", {})
            setting = [r for r in rows if r["Q"] == q0]
            reject(qitem.get("cutoff") != cutoff or qitem.get("Q") != q0 or
                   qitem.get("rows") != 3 or
                   qitem.get("spectral_cap_violations") != sum(
                       r["band_failure_flags"][key] for r in setting) or
                   qitem.get("spectral_values") !=
                   [r["bands"][key]["spectral"] for r in setting],
                   "phase Q")
    first = [next((c for c in BAND_CUTOFFS
                   if r["band_failure_flags"][str(c)]), None) for r in rows]
    reject(phase.get("minimal_failure_cutoff_census") != {
        str(c): first.count(c) for c in BAND_CUTOFFS} or
           phase.get("never_failure_rows") != first.count(None),
           "minimal cutoff census")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 9 or audit.get("origin_count") != 3 or
           audit.get("q_count") != 3 or audit.get("cutoff_count") != 4 or
           audit.get("spectral_rows") != 9 or
           audit.get("spectral_cap_violations_by_cutoff") != {
               str(c): phase["by_cutoff"][str(c)][
                   "spectral_cap_violations"] for c in BAND_CUTOFFS} or
           audit.get("schur_cap_violations_by_cutoff") != {
               str(c): phase["by_cutoff"][str(c)][
                   "schur_cap_violations"] for c in BAND_CUTOFFS} or
           audit.get("failure_keys_by_cutoff") != {
               str(c): phase["by_cutoff"][str(c)]["failure_keys"]
               for c in BAND_CUTOFFS} or
           audit.get("parent_failure_keys") != EXPECTED_PARENT or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    reject(payload.get("exact_theorem", {}).get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-374 near-block band truncation",
    }, "anchor")
    reject(payload.get("claim_firewall") != {
        "TPC375_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC375_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC375_NESTED_BAND_MASKS": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC375_BANDWIDTH_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_9_ROWS",
        "TPC375_FAILURE_CUTOFF_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_PARENT_SUPPORT_REPRODUCTION":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_MINIMAL_CUTOFF": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC375_BANDWIDTH_UNIFORMITY": "OPEN",
        "TPC375_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC375_ORIGIN_UNIFORMITY": "OPEN",
        "TPC375_WINDOW_UNIFORMITY": "OPEN",
        "TPC375_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC375_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC375_SOURCE_UNIFORM_L2": "OPEN",
        "TPC375_ARITHMETIC_ADVANCE": "NO",
        "TPC375_FIXED_POWER_CREDIT": 0,
        "TPC375_FULL_GATE_B": "OPEN",
        "TPC375_TWIN_PRIME_RESULT": "NONE",
    }, "firewall")
    reject(payload.get("round2_clue") != "TEST_BANDWIDTH_HOLDOUT", "clue")


def mutate(document: dict[str, Any], path: tuple[Any, ...], value: Any,
           refresh: bool = True) -> dict[str, Any]:
    item = copy.deepcopy(document)
    target: Any = item
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    if refresh and path[0] == "payload":
        item["payload_sha256"] = hashlib.sha256(
            canonical(item["payload"])).hexdigest()
    return item


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        raw = CERTIFICATE.read_bytes()
        document = json.loads(raw)
        reject(raw != canonical(document), "certificate canonicality")
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("certificate_version",), 2),
            (("claim_status",), "PROVED"),
            (("payload", "schema"), "MUTATED"),
            (("payload", "parent_lock", "parent_round2_clue"), "NO"),
            (("payload", "protocol", "band_cutoffs"), [0, 2, 3]),
            (("payload", "protocol", "band_definition"), "all pairs"),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "row_selection_used"), True),
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "beta"), 0),
            (("payload", "rows", 0, "bands", "3", "spectral"), "0"),
            (("payload", "rows", 0, "mode", "mode_rule"), "adaptive"),
            (("payload", "finite_audit", "rows"), 8),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "phase_summary", "cutoffs"), [0, 1]),
            (("payload", "phase_summary", "by_cutoff", "3",
              "failure_keys"), []),
            (("payload", "exact_theorem", "anchor_inheritance", "Q"), 5),
            (("payload", "claim_firewall", "TPC375_BANDWIDTH_UNIFORMITY"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC375_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "round2_clue"), "CLAIM_TWIN_PRIMES"),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = mutate(document, path, value,
                          refresh=(path[0] == "payload"))
            try:
                validate(item)
            except Rejected:
                rejected += 1
        reject(rejected != len(mutations), "mutation census")
        reject(hashlib.sha256(canonical(document)).hexdigest() != baseline,
               "baseline changed")
        print("TPC375_STRESS=PASS exact_baseline=1 mutations=" +
              str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC375_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
