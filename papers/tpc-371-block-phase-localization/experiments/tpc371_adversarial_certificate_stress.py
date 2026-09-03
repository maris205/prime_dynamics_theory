#!/usr/bin/env python3
"""Adversarial certificate mutations for TPC-371."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-371-block-phase-localization/results/tpc371_certificate.json")
SCHEMA = "TPC371_COUNT_2048_BLOCK_PHASE_LOCALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_BLOCK_PHASE_LOCALIZATION"
ORIGINS = [1010001, 1018021, 1026041]
Q_ANCHORS = [512, 2048, 8192]
EXPONENTS = [1]
BETAS = [0, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]
BLOCK_INDICES = list(range(8))


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
    origin = payload.get("origin_protocol", {})
    reject(origin.get("candidate_count") != 41 or
           origin.get("grid_start") != 1010001 or
           origin.get("grid_step") != 401 or
           origin.get("grid_indices") != [0, 20, 40] or
           origin.get("selected_origins") != ORIGINS or
           origin.get("response_used") is not False or
           origin.get("geometry_used_for_selection") is not False or
           origin.get("source_used") is not False, "origin protocol")
    protocol = payload.get("protocol", {})
    reject(protocol.get("origins") != ORIGINS or
           protocol.get("window_count") != 2048 or
           protocol.get("block_count") != 256 or
           protocol.get("block_indices") != BLOCK_INDICES or
           protocol.get("q_anchors") != Q_ANCHORS or
           protocol.get("kernel_exponents") != EXPONENTS or
           protocol.get("laws") != LAWS or protocol.get("betas") != BETAS or
           protocol.get("height") != 66 or
           protocol.get("spectra_for_all_laws") is not True or
           protocol.get("source_response_used") is not False or
           protocol.get("origin_selection_used") is not False or
           protocol.get("block_selection_used") is not False, "protocol")
    rows = payload.get("rows")
    expected = {(o, b, q, e, beta, law)
                for beta in BETAS for o in ORIGINS for b in BLOCK_INDICES
                for q in Q_ANCHORS for e in EXPONENTS for law in LAWS}
    reject(not isinstance(rows, list) or len(rows) != 576, "rows")
    reject({(row.get("origin"), row.get("block_index"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows} != expected, "row keys")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap_repair_betas") != [] or
           phase.get("cap") != "0.64000000000000001" or
           phase.get("schur_cap") != "0.82999999999999996", "phase header")
    for beta in BETAS:
        selected = [row for row in rows if row["beta"] == beta]
        item = phase.get("by_beta", {}).get(str(beta), {})
        reject(item.get("rows") != 288 or item.get("blocks") != 24 or
               item.get("spectral_cap_violations") != sum(
                   float(row["normalized"]["spectral"]) > .64
                   for row in selected) or
               item.get("schur_cap_violations") != sum(
                   float(row["normalized"]["schur"]) > .83
                   for row in selected), "phase beta")
        for q0 in Q_ANCHORS:
            selected_q = [row for row in selected if row["Q"] == q0]
            item_q = phase.get("by_beta_q", {}).get(f"{beta}:{q0}", {})
            reject(item_q.get("rows") != 96 or
                   item_q.get("spectral_cap_violations") != sum(
                       float(row["normalized"]["spectral"]) > .64
                       for row in selected_q) or
                   item_q.get("schur_cap_violations") != sum(
                       float(row["normalized"]["schur"]) > .83
                       for row in selected_q), "phase q")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 576 or
           audit.get("settings_per_beta") != 288 or
           audit.get("origin_count") != 3 or audit.get("block_count") != 8 or
           audit.get("rows_per_origin") != 96 or
           audit.get("beta_count") != 2 or audit.get("spectral_rows") != 576 or
           audit.get("beta2_rows") != 288 or
           audit.get("window_count") != 2048 or
           audit.get("block_count_fixed") != 256 or
           audit.get("q_min") != 512 or audit.get("q_max") != 8192 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    for beta, prefix in ((2, "beta2"), (0, "baseline_beta0")):
        item = phase["by_beta"][str(beta)]
        reject(audit.get(prefix + "_spectral_cap_violations") !=
               item["spectral_cap_violations"] or
               audit.get(prefix + "_schur_cap_violations") !=
               item["schur_cap_violations"], "audit phase")
    actual = [[row["origin"], row["block_index"], row["Q"],
               row["kernel_exponent"], row["law"]]
              for row in rows if row["beta"] == 2 and
              float(row["normalized"]["spectral"]) > .64]
    reject(audit.get("beta2_failure_keys") != actual or
           audit.get("beta2_all_declared_blocks_pass") != (not actual) or
           audit.get("beta2_failure_block_count") !=
           len({(key[0], key[1]) for key in actual}), "failure keys")
    reject(payload.get("exact_theorem", {}).get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4, "kernel_exponent": 1,
        "source_project": "TPC-370 count-2048 finite-window audit",
    }, "anchor inheritance")
    expected_firewall = {
        "TPC371_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC371_BLOCK_PARTITION": "PROVED_EXACT_FINITE_PREDECLARED",
        "TPC371_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC371_BLOCK_LOCAL_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_576_ROWS",
        "TPC371_BETA2_BLOCK_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC371_BETA2_LOCAL_FAILURE": "REFUTED_SCOPED",
        "TPC371_CROSS_BLOCK_COHERENCE": "OPEN",
        "TPC371_ORIGIN_UNIFORMITY": "OPEN",
        "TPC371_WINDOW_UNIFORMITY": "OPEN",
        "TPC371_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC371_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC371_SOURCE_UNIFORM_L2": "OPEN",
        "TPC371_ARITHMETIC_ADVANCE": "NO",
        "TPC371_FIXED_POWER_CREDIT": 0,
        "TPC371_FULL_GATE_B": "OPEN",
        "TPC371_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        reject(firewall.get(key) != value, "firewall " + key)
    reject(payload.get("round2_clue") !=
           "TEST_OFF_BLOCK_COHERENCE_DECOMPOSITION", "clue")


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
            (("payload", "origin_protocol", "grid_indices"), [0, 1, 40]),
            (("payload", "origin_protocol", "response_used"), True),
            (("payload", "origin_protocol", "source_used"), True),
            (("payload", "protocol", "window_count"), 1024),
            (("payload", "protocol", "block_count"), 128),
            (("payload", "protocol", "block_indices"), [0, 1]),
            (("payload", "protocol", "block_selection_used"), True),
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "protocol", "q_anchors"), [512, 2048]),
            (("payload", "protocol", "kernel_exponents"), [1, 2]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "spectra_for_all_laws"), False),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "block_index"), 8),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "block_count"), 128),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "law"), "invented"),
            (("payload", "row_digest"), "0" * 64),
            (("payload", "finite_audit", "rows"), 575),
            (("payload", "finite_audit", "block_count"), 7),
            (("payload", "finite_audit", "beta2_spectral_cap_violations"), 1),
            (("payload", "finite_audit", "beta2_all_declared_blocks_pass"), False),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 1),
            (("payload", "exact_theorem", "anchor_inheritance", "Q"), 5),
            (("payload", "claim_firewall", "TPC371_BETA2_LOCAL_FAILURE"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC371_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC371_FIXED_POWER_CREDIT"), 1),
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
        print("TPC371_STRESS=PASS exact_baseline=1 mutations=" +
              str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC371_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
