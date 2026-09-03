#!/usr/bin/env python3
"""Adversarial mutation test for the TPC-370 count-2048 certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-370-count-2048-window-audit/results/"
    "tpc370_certificate.json")
SCHEMA = "TPC370_COUNT_2048_WINDOW_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_COUNT_2048_WINDOW_AUDIT"
ORIGINS = [1010001, 1018021, 1026041]
COUNTS = [2048]
Q_ANCHORS = [512, 2048, 8192]
EXPONENTS = [1]
BETAS = [0, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]


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
           origin.get("grid_start") != 1010001 or origin.get("grid_step") != 401 or
           origin.get("grid_indices") != [0, 20, 40] or
           origin.get("selected_origins") != ORIGINS or
           origin.get("response_used") is not False or
           origin.get("geometry_used_for_selection") is not False or
           origin.get("source_used") is not False, "origin protocol")
    protocol = payload.get("protocol", {})
    reject(protocol.get("origins") != ORIGINS or
           protocol.get("counts") != COUNTS or
           protocol.get("q_anchors") != Q_ANCHORS or
           protocol.get("kernel_exponents") != EXPONENTS or
           protocol.get("laws") != LAWS or protocol.get("betas") != BETAS or
           protocol.get("height") != 66 or
           protocol.get("spectra_for_all_laws") is not True or
           protocol.get("source_response_used") is not False or
           protocol.get("origin_selection_used") is not False, "protocol")
    rows = payload.get("rows")
    expected = {(o, n, q, e, b, law)
                for b in BETAS for o in ORIGINS for n in COUNTS
                for q in Q_ANCHORS for e in EXPONENTS for law in LAWS}
    reject(not isinstance(rows, list) or len(rows) != 72, "rows")
    reject({(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows} != expected, "row keys")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap_repair_betas") != [], "repair beta")
    for beta in BETAS:
        spectral = sum(
            float(row["normalized"]["spectral"]) > 0.64
            for row in rows if row["beta"] == beta)
        schur = sum(
            float(row["normalized"]["schur"]) > 0.83
            for row in rows if row["beta"] == beta)
        item = phase.get("by_beta", {}).get(str(beta), {})
        reject(item.get("rows") != 36 or
               item.get("spectral_cap_violations") != spectral or
               item.get("schur_cap_violations") != schur, "phase")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 72 or
           audit.get("settings_per_beta") != 36 or
           audit.get("beta_count") != 2 or
           audit.get("spectral_rows") != 72 or
           audit.get("beta2_rows") != 36 or
           audit.get("q_min") != 512 or audit.get("q_max") != 8192 or
           audit.get("count_min") != 2048 or audit.get("count_max") != 2048 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    for beta in BETAS:
        item = phase["by_beta"][str(beta)]
        reject(audit.get(
            "beta2_spectral_cap_violations" if beta == 2 else
            "baseline_beta0_spectral_cap_violations") !=
               item["spectral_cap_violations"], "spectral audit")
        reject(audit.get(
            "beta2_schur_cap_violations" if beta == 2 else
            "baseline_beta0_schur_cap_violations") !=
               item["schur_cap_violations"], "schur audit")
    actual_failure_keys = [
        [row["origin"], row["count"], row["Q"], row["kernel_exponent"],
         row["law"]]
        for row in rows if row["beta"] == 2 and
        float(row["normalized"]["spectral"]) > 0.64
    ]
    actual_signature = sorted([[key[0], key[2], key[3], key[4]]
                                for key in actual_failure_keys])
    parent_keys = audit.get("parent_failure_keys")
    parent_signature = audit.get("parent_failure_signature")
    reject(not isinstance(parent_keys, list) or
           parent_signature != sorted([[key[0], key[2], key[3], key[4]]
                                       for key in parent_keys]) or
           audit.get("replicated_failure_keys") != actual_failure_keys or
           audit.get("replicated_failure_signature") != actual_signature or
           audit.get("failure_signature_matches_parent") !=
           (actual_signature == parent_signature),
           "failure signature comparison")
    reject(payload.get("exact_theorem", {}).get("anchor_inheritance") != {
        "interval": [1010346, 1010359], "Q": 4,
        "kernel_exponent": 1,
        "source_project": "TPC-369 third predeclared origin-family audit",
    }, "anchor inheritance")
    expected_firewall = {
        "TPC370_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND",
        "TPC370_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC370_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
        "TPC370_COUNT_2048_WINDOW": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_BETA2_PARENT_SIGNATURE": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC370_ORIGIN_UNIFORMITY": "OPEN",
        "TPC370_WINDOW_UNIFORMITY": "OPEN",
        "TPC370_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC370_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC370_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC370_SOURCE_UNIFORM_L2": "OPEN",
        "TPC370_ARITHMETIC_ADVANCE": "NO",
        "TPC370_FIXED_POWER_CREDIT": 0,
        "TPC370_FULL_GATE_B": "OPEN",
        "TPC370_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        reject(firewall.get(key) != value, "firewall " + key)
    reject(payload.get("round2_clue") !=
           "TEST_COUNT_2048_PHASE_LOCALIZATION", "clue")


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
            (("payload", "protocol", "origins"), [ORIGINS[0]]),
            (("payload", "protocol", "counts"), [1024]),
            (("payload", "protocol", "q_anchors"), [512, 2048]),
            (("payload", "protocol", "kernel_exponents"), [1, 2]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "spectra_for_all_laws"), False),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "count"), 1024),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "law"), "invented"),
            (("payload", "row_digest"), "0" * 64),
            (("payload", "finite_audit", "rows"), 143),
            (("payload", "finite_audit", "count_max"), 1024),
            (("payload", "finite_audit", "beta2_spectral_cap_violations"), 0),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 0),
            (("payload", "exact_theorem", "anchor_inheritance",
              "Q"), 5),
            (("payload", "finite_audit", "parent_failure_signature"),
             []),
            (("payload", "claim_firewall", "TPC370_BETA2_PHASE_AUDIT"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC370_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC370_FIXED_POWER_CREDIT"), 1),
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
        print("TPC370_STRESS=PASS exact_baseline=1 mutations=" + str(len(mutations)))
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC370_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
