#!/usr/bin/env python3
"""Adversarial certificate mutations for TPC-374."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-374-near-block-band-truncation/results/"
    "tpc374_certificate.json")
SCHEMA = "TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_NEAR_BLOCK_BAND_TRUNCATION"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BETAS = [0, 2]
EXPECTED_FAILURES = [
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
    lock = payload.get("parent_lock", {})
    reject(lock != {
        "base_code_sha256":
        "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9",
        "parent_code_sha256":
        "770877d4375f65b5eae61101e3bc8c8340737a19e3e2f22defc4f75c1640df49",
        "parent_certificate_sha256":
        "7f54603589c49085ec6f35bf7752a505e85f2f2e9f979d448f42a8e7776a80e5",
        "parent_schema": "TPC373_EIGENMODE_BLOCK_SEPARATION_V1",
        "parent_round2_clue": "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
    }, "parent lock")
    protocol = payload.get("protocol", {})
    reject(protocol != {
        "origins": ORIGINS, "window_count": 2048, "block_count": 256,
        "block_indices": list(range(8)),
        "partition": "fixed eight contiguous 256-point blocks",
        "band_cutoff": 3,
        "band_definition": "sum of layers with block distance <= 3",
        "q_anchors": Q_ANCHORS, "kernel_exponents": [1],
        "laws": ["all_plus"], "betas": BETAS, "height": 66,
        "common_normalization": True, "source_response_used": False,
        "origin_selection_used": False, "row_selection_used": False,
        "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        "component_selection_used": False,
        "panel_complete_before_mode_read": True,
    }, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    reject(not isinstance(rows, list) or len(rows) != 18 or
           {(r.get("origin"), r.get("Q"), r.get("kernel_exponent"),
             r.get("beta"), r.get("law")) for r in rows} != expected,
           "row census")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        reject(row.get("count") != 2048 or row.get("height") != 66 or
               row.get("shell_cardinality", 0) <= 0 or
               row.get("parent_failure") not in (True, False), "row header")
        for component in ("full", "band"):
            metrics = row.get(component, {})
            for key in ("spectral", "schur", "frobenius",
                        "minimum_eigenvalue", "maximum_eigenvalue"):
                reject(key not in metrics, component + " metric")
        tail = row.get("tail", {})
        reject(any(key not in tail for key in
                   ("schur", "frobenius", "symmetry_error")), "tail")
        mode = row.get("mode", {})
        reject(mode.get("mode_rule") !=
               "largest absolute eigenvalue; minimum mode wins ties" or
               mode.get("selected_mode") != "minimum_eigenvalue" or
               float(mode.get("eigen_residual_inf")) > 1.0e-5 or
               float(mode.get("full_mode_norm_error")) > 1.0e-8 or
               float(mode.get("rayleigh_sum_error")) > 1.0e-8,
               "mode")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap") != "0.64000000000000001" or
           phase.get("schur_cap") != "0.82999999999999996" or
           phase.get("band_cutoff") != 3 or
           phase.get("band_definition") !=
           "sum of layers with block distance <= 3" or
           phase.get("cap_repair_betas") != [], "phase header")
    expected_phase = {"0": (9, 9, 9, 9, 9), "2": (9, 6, 0, 6, 0)}
    for beta_text, values in expected_phase.items():
        item = phase.get("by_beta", {}).get(beta_text, {})
        reject((item.get("rows"), item.get("full_spectral_cap_violations"),
                item.get("full_schur_cap_violations"),
                item.get("band_spectral_cap_violations"),
                item.get("band_schur_cap_violations")) != values or
               item.get("minimum_mode_rows") != 9, "phase beta")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 18 or audit.get("beta2_rows") != 9 or
           audit.get("baseline_beta0_rows") != 9 or
           audit.get("origin_count") != 3 or audit.get("q_count") != 3 or
           audit.get("spectral_rows") != 18 or
           audit.get("beta2_full_spectral_cap_violations") != 6 or
           audit.get("beta2_full_schur_cap_violations") != 0 or
           audit.get("beta2_band_spectral_cap_violations") != 6 or
           audit.get("beta2_band_schur_cap_violations") != 0 or
           audit.get("baseline_beta0_full_spectral_cap_violations") != 9 or
           audit.get("baseline_beta0_full_schur_cap_violations") != 9 or
           audit.get("full_failure_keys") != EXPECTED_FAILURES or
           audit.get("band_failure_keys") != EXPECTED_FAILURES or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    reject(payload.get("exact_theorem", {}).get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-373 eigenmode block separation",
    }, "anchor")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC374_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC374_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC374_NEAR_BLOCK_BAND": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC374_BAND_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC374_BAND_FAILURE_CENSUS": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_PARENT_FAILURE_REPRODUCTION":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_RAYLEIGH_RETENTION": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_TAIL_PROFILE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC374_BAND_OPERATOR_UNIFORMITY": "OPEN",
        "TPC374_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC374_ORIGIN_UNIFORMITY": "OPEN",
        "TPC374_WINDOW_UNIFORMITY": "OPEN",
        "TPC374_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC374_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC374_SOURCE_UNIFORM_L2": "OPEN",
        "TPC374_ARITHMETIC_ADVANCE": "NO",
        "TPC374_FIXED_POWER_CREDIT": 0,
        "TPC374_FULL_GATE_B": "OPEN",
        "TPC374_TWIN_PRIME_RESULT": "NONE",
    }
    reject(firewall != expected_firewall, "firewall")
    reject(payload.get("round2_clue") != "TEST_BANDWIDTH_STABILITY", "clue")


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
            (("payload", "protocol", "window_count"), 1024),
            (("payload", "protocol", "band_cutoff"), 2),
            (("payload", "protocol", "band_definition"), "all pairs"),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "row_selection_used"), True),
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "band", "spectral"), "0"),
            (("payload", "rows", 0, "mode", "selected_mode"),
             "maximum_eigenvalue"),
            (("payload", "rows", 0, "mode", "eigen_residual_inf"), "1"),
            (("payload", "finite_audit", "rows"), 17),
            (("payload", "finite_audit", "band_failure_keys"), []),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "phase_summary", "band_cutoff"), 1),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "exact_theorem", "anchor_inheritance", "Q"), 5),
            (("payload", "claim_firewall", "TPC374_BAND_OPERATOR_UNIFORMITY"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC374_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "claim_firewall", "TPC374_FIXED_POWER_CREDIT"), 1),
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
        print("TPC374_STRESS=PASS exact_baseline=1 mutations=" +
              str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC374_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
