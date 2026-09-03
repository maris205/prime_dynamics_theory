#!/usr/bin/env python3
"""Adversarial certificate mutations for TPC-372."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-372-full-window-offblock-decomposition/results/"
    "tpc372_certificate.json")
SCHEMA = "TPC372_FULL_WINDOW_OFFBLOCK_DECOMPOSITION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FULL_WINDOW_DECOMPOSITION"
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
           "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1" or
           lock.get("parent_block_phase") is not True, "parent lock")
    protocol = payload.get("protocol", {})
    reject(protocol.get("origins") != ORIGINS or
           protocol.get("window_count") != 2048 or
           protocol.get("block_count") != 256 or
           protocol.get("block_indices") != list(range(8)) or
           protocol.get("q_anchors") != Q_ANCHORS or
           protocol.get("kernel_exponents") != [1] or
           protocol.get("laws") != ["all_plus"] or
           protocol.get("betas") != BETAS or protocol.get("height") != 66 or
           protocol.get("common_normalization") is not True or
           protocol.get("source_response_used") is not False or
           protocol.get("origin_selection_used") is not False or
           protocol.get("component_selection_used") is not False, "protocol")
    rows = payload.get("rows")
    expected = {(o, q, 1, beta, "all_plus")
                for beta in BETAS for o in ORIGINS for q in Q_ANCHORS}
    reject(not isinstance(rows, list) or len(rows) != 18 or
           {(row.get("origin"), row.get("Q"), row.get("kernel_exponent"),
             row.get("beta"), row.get("law")) for row in rows} != expected,
           "rows")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap") != "0.64000000000000001" or
           phase.get("schur_cap") != "0.82999999999999996" or
           phase.get("cap_repair_betas") != [], "phase header")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        reject(item.get("rows") != 9 or
               item.get("full_spectral_cap_violations") != sum(
                   float(row["full"]["spectral"]) > .64
                   for row in selected) or
               item.get("full_schur_cap_violations") != sum(
                   float(row["full"]["schur"]) > .83
                   for row in selected) or
               item.get("block_diagonal_spectral_cap_violations") != sum(
                   float(row["block_diagonal"]["spectral"]) > .64
                   for row in selected) or
               item.get("off_block_spectral_cap_violations") != sum(
                   float(row["off_block"]["spectral"]) > .64
                   for row in selected), "phase beta")
        for q0 in Q_ANCHORS:
            selected_q = [row for row in selected if row["Q"] == q0]
            item_q = phase.get("by_beta_q", {}).get(f"{beta}:{q0}", {})
            reject(item_q.get("rows") != 3 or
                   item_q.get("full_spectral_cap_violations") != sum(
                       float(row["full"]["spectral"]) > .64
                       for row in selected_q) or
                   item_q.get("block_diagonal_spectral_cap_violations") != sum(
                       float(row["block_diagonal"]["spectral"]) > .64
                       for row in selected_q) or
                   item_q.get("off_block_spectral_cap_violations") != sum(
                       float(row["off_block"]["spectral"]) > .64
                       for row in selected_q), "phase q")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 18 or audit.get("beta2_rows") != 9 or
           audit.get("baseline_beta0_rows") != 9 or
           audit.get("origin_count") != 3 or audit.get("q_count") != 3 or
           audit.get("spectral_rows") != 18 or
           audit.get("beta2_full_spectral_cap_violations") != 6 or
           audit.get("beta2_full_schur_cap_violations") != 0 or
           audit.get("beta2_block_diagonal_spectral_cap_violations") != 0 or
           audit.get("beta2_block_diagonal_schur_cap_violations") != 0 or
           audit.get("beta2_off_block_spectral_cap_violations") != 0 or
           audit.get("baseline_beta0_full_spectral_cap_violations") != 9 or
           audit.get("baseline_beta0_full_schur_cap_violations") != 9 or
           audit.get("decomposition_max_error") != "0" or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    actual = [[row["origin"], row["count"], row["Q"],
               row["kernel_exponent"], row["law"]]
              for row in rows if row["beta"] == 2 and
              float(row["full"]["spectral"]) > .64]
    expected_full = [[1010001, 2048, 2048, 1, "all_plus"],
                     [1010001, 2048, 8192, 1, "all_plus"],
                     [1018021, 2048, 2048, 1, "all_plus"],
                     [1018021, 2048, 8192, 1, "all_plus"],
                     [1026041, 2048, 2048, 1, "all_plus"],
                     [1026041, 2048, 8192, 1, "all_plus"]]
    reject(actual != expected_full or audit.get("full_failure_keys") != actual or
           audit.get("block_diagonal_beta2_failure_keys") != [] or
           audit.get("required_off_block_keys") !=
           [[key[0], key[2]] for key in actual], "failure census")
    reject(payload.get("exact_theorem", {}).get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-371 block-local phase localization",
    }, "anchor")
    expected_firewall = {
        "TPC372_FULL_WINDOW_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC372_COMMON_NORMALIZATION": "PROVED_EXACT_FINITE",
        "TPC372_DECOMPOSITION_IDENTITY": "NUMERICALLY_CERTIFIED_FINITE",
        "TPC372_FULL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
        "TPC372_BETA2_FULL_FAILURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_BLOCK_DIAGONAL_PHASE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_OFF_BLOCK_NECESSITY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC372_CROSS_BLOCK_CAUSALITY": "OPEN",
        "TPC372_ORIGIN_UNIFORMITY": "OPEN",
        "TPC372_WINDOW_UNIFORMITY": "OPEN",
        "TPC372_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC372_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC372_SOURCE_UNIFORM_L2": "OPEN",
        "TPC372_ARITHMETIC_ADVANCE": "NO",
        "TPC372_FIXED_POWER_CREDIT": 0,
        "TPC372_FULL_GATE_B": "OPEN",
        "TPC372_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        reject(firewall.get(key) != value, "firewall " + key)
    reject(payload.get("round2_clue") != "TEST_EIGENMODE_BLOCK_SEPARATION",
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
            (("payload", "parent_lock", "parent_block_phase"), False),
            (("payload", "protocol", "window_count"), 1024),
            (("payload", "protocol", "block_count"), 128),
            (("payload", "protocol", "block_indices"), [0, 1]),
            (("payload", "protocol", "q_anchors"), [512, 2048]),
            (("payload", "protocol", "component_selection_used"), True),
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "laws"), ["invented"]),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "law"), "invented"),
            (("payload", "row_digest"), "0" * 64),
            (("payload", "finite_audit", "rows"), 17),
            (("payload", "finite_audit", "beta2_rows"), 8),
            (("payload", "finite_audit", "beta2_full_spectral_cap_violations"), 0),
            (("payload", "finite_audit", "beta2_block_diagonal_spectral_cap_violations"), 1),
            (("payload", "finite_audit", "required_off_block_keys"), []),
            (("payload", "finite_audit", "decomposition_max_error"), "1/10"),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "phase_summary", "by_beta", "2",
              "full_spectral_cap_violations"), 0),
            (("payload", "phase_summary", "by_beta_q", "2:2048",
              "full_spectral_cap_violations"), 0),
            (("payload", "exact_theorem", "anchor_inheritance", "Q"), 5),
            (("payload", "claim_firewall", "TPC372_OFF_BLOCK_NECESSITY"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC372_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC372_FIXED_POWER_CREDIT"), 1),
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
        print("TPC372_STRESS=PASS exact_baseline=1 mutations=" +
              str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC372_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
