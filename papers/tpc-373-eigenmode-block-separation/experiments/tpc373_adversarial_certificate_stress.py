#!/usr/bin/env python3
"""Adversarial certificate mutations for TPC-373."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-373-eigenmode-block-separation/results/"
    "tpc373_certificate.json")
SCHEMA = "TPC373_EIGENMODE_BLOCK_SEPARATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_EIGENMODE_BLOCK_SEPARATION"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
BETAS = [0, 2]


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
    reject(lock.get("parent_schema") !=
           "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1" or
           lock.get("parent_round2_clue") !=
           "TEST_EIGENMODE_BLOCK_SEPARATION", "parent lock")
    protocol = payload.get("protocol", {})
    reject(protocol.get("origins") != ORIGINS or
           protocol.get("window_count") != 2048 or
           protocol.get("block_count") != 256 or
           protocol.get("block_indices") != list(range(8)) or
           protocol.get("partition") !=
           "fixed eight contiguous 256-point blocks" or
           protocol.get("layer_definition") !=
           "absolute block-index distance 0..7" or
           protocol.get("q_anchors") != Q_ANCHORS or
           protocol.get("kernel_exponents") != [1] or
           protocol.get("laws") != ["all_plus"] or
           protocol.get("betas") != BETAS or protocol.get("height") != 66 or
           protocol.get("common_normalization") is not True or
           protocol.get("source_response_used") is not False or
           protocol.get("origin_selection_used") is not False or
           protocol.get("row_selection_used") is not False or
           protocol.get("component_selection_used") is not False or
           protocol.get("panel_complete_before_mode_read") is not True or
           protocol.get("mode_rule") !=
           "largest absolute eigenvalue; minimum mode wins ties", "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    reject(not isinstance(rows, list) or len(rows) != 18 or
           {(row.get("origin"), row.get("Q"), row.get("kernel_exponent"),
             row.get("beta"), row.get("law")) for row in rows} != expected,
           "rows")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    for row in rows:
        reject(row.get("count") != 2048 or row.get("height") != 66 or
               row.get("shell_cardinality", 0) <= 0 or
               row.get("parent_failure") not in (True, False), "row header")
        metrics = row.get("full", {})
        for key in ("spectral", "schur", "frobenius", "minimum_eigenvalue",
                    "maximum_eigenvalue"):
            reject(key not in metrics, "metric " + key)
        mode = row.get("eigenmode", {})
        reject(mode.get("mode_rule") !=
               "largest absolute eigenvalue; minimum mode wins ties" or
               mode.get("layer_count") != 8 or
               mode.get("selected_mode") not in
               ("minimum_eigenvalue", "maximum_eigenvalue") or
               len(mode.get("layers", [])) != 8, "mode header")
        reject([layer.get("block_distance") for layer in mode["layers"]] !=
               list(range(8)), "layer census")
        reject(float(mode.get("layer_reconstruction_error")) > 1.0e-12 or
               float(mode.get("rayleigh_sum_error")) > 1.0e-8 or
               float(mode.get("eigen_residual_inf")) > 1.0e-5, "errors")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap") != "0.64000000000000001" or
           phase.get("schur_cap") != "0.82999999999999996" or
           phase.get("mode_selection") !=
           "largest absolute eigenvalue; min wins ties" or
           phase.get("layer_partition") !=
           "absolute block-index distance 0..7" or
           phase.get("cap_repair_betas") != [], "phase header")
    for beta in BETAS:
        item = phase.get("by_beta", {}).get(str(beta), {})
        reject(item.get("rows") != 9 or
               item.get("minimum_mode_rows", -1) < 0 or
               item.get("maximum_mode_rows", -1) < 0 or
               item.get("minimum_mode_rows", -1) +
               item.get("maximum_mode_rows", -1) != 9 or
               sum(item.get("dominant_distance_histogram", {}).values()) != 9,
               "phase beta")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 18 or audit.get("beta2_rows") != 9 or
           audit.get("baseline_beta0_rows") != 9 or
           audit.get("origin_count") != 3 or audit.get("q_count") != 3 or
           audit.get("spectral_rows") != 18 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    theorem = payload.get("exact_theorem", {})
    reject(theorem.get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-372 full-window off-block decomposition",
    }, "anchor")
    expected_firewall = {
        "TPC373_FULL_WINDOW_PROTOCOL":
            "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC373_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC373_BLOCK_DISTANCE_PARTITION":
            "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC373_EIGENMODE_SELECTION_RULE":
            "PROVED_EXACT_FINITE_DETERMINISTIC",
        "TPC373_EIGENMODE_REPLAY":
            "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC373_LAYER_RECONSTRUCTION": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC373_RAYLEIGH_PROFILE":
            "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC373_CROSS_BLOCK_DECAY": "OPEN",
        "TPC373_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC373_ORIGIN_UNIFORMITY": "OPEN",
        "TPC373_WINDOW_UNIFORMITY": "OPEN",
        "TPC373_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC373_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC373_SOURCE_UNIFORM_L2": "OPEN",
        "TPC373_ARITHMETIC_ADVANCE": "NO",
        "TPC373_FIXED_POWER_CREDIT": 0,
        "TPC373_FULL_GATE_B": "OPEN",
        "TPC373_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        reject(payload.get("claim_firewall", {}).get(key) != value,
               "firewall " + key)
    reject(payload.get("round2_clue") != "TEST_LAYERWISE_CROSS_BLOCK_DECAY",
           "clue")


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
            (("payload", "status"), "PROVED"),
            (("payload", "parent_lock", "parent_round2_clue"), "NO"),
            (("payload", "protocol", "window_count"), 1024),
            (("payload", "protocol", "block_count"), 128),
            (("payload", "protocol", "block_indices"), [0, 1]),
            (("payload", "protocol", "layer_definition"), "all pairs"),
            (("payload", "protocol", "q_anchors"), [512, 2048]),
            (("payload", "protocol", "mode_rule"), "largest positive"),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "protocol", "row_selection_used"), True),
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "laws"), ["invented"]),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "law"), "invented"),
            (("payload", "row_digest"), "0" * 64),
            (("payload", "rows", 0, "eigenmode", "selected_mode"),
             "claimed_positive"),
            (("payload", "rows", 0, "eigenmode", "layers"), []),
            (("payload", "rows", 0, "eigenmode", "layer_count"), 7),
            (("payload", "rows", 0, "eigenmode",
              "layer_reconstruction_error"), "1/10"),
            (("payload", "finite_audit", "rows"), 17),
            (("payload", "finite_audit", "beta2_rows"), 8),
            (("payload", "finite_audit", "fixed_power_credit"), 1),
            (("payload", "finite_audit", "arithmetic_advance"), "YES"),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "phase_summary", "mode_selection"), "adaptive"),
            (("payload", "phase_summary", "by_beta", "2", "rows"), 8),
            (("payload", "phase_summary", "by_beta", "2",
              "minimum_mode_rows"), 10),
            (("payload", "exact_theorem", "anchor_inheritance", "Q"), 5),
            (("payload", "claim_firewall", "TPC373_CROSS_BLOCK_DECAY"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC373_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "claim_firewall", "TPC373_FIXED_POWER_CREDIT"), 1),
            (("payload", "round2_clue"), "CLAIM_TWIN_PRIMES"),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = mutate(document, path, value, refresh=(path[0] == "payload"))
            try:
                validate(item)
            except Rejected:
                rejected += 1
        reject(rejected != len(mutations), "mutation census")
        reject(hashlib.sha256(canonical(document)).hexdigest() != baseline,
               "baseline changed")
        print("TPC373_STRESS=PASS exact_baseline=1 mutations=" +
              str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC373_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
