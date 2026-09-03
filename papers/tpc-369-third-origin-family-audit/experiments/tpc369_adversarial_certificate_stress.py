#!/usr/bin/env python3
"""Adversarial mutation test for the TPC-369 third-family certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-369-third-origin-family-audit/results/"
    "tpc369_certificate.json")
SCHEMA = "TPC369_THIRD_ORIGIN_FAMILY_AUDIT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_THIRD_ORIGIN_FAMILY_AUDIT"
ORIGINS = [1010001, 1018021, 1026041]
COUNTS = [512, 1024]
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
    reject(not isinstance(rows, list) or len(rows) != 144, "rows")
    reject({(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows} != expected, "row keys")
    reject(payload.get("row_digest") != hashlib.sha256(
        canonical(rows)).hexdigest(), "row digest")
    phase = payload.get("phase_summary", {})
    reject(phase.get("cap_repair_betas") != [], "repair beta")
    for beta, spectral, schur in ((0, 18, 18), (2, 6, 0)):
        item = phase.get("by_beta", {}).get(str(beta), {})
        reject(item.get("rows") != 72 or
               item.get("spectral_cap_violations") != spectral or
               item.get("schur_cap_violations") != schur, "phase")
    audit = payload.get("finite_audit", {})
    reject(audit.get("rows") != 144 or
           audit.get("settings_per_beta") != 72 or
           audit.get("beta_count") != 2 or
           audit.get("spectral_rows") != 144 or
           audit.get("beta2_rows") != 72 or
           audit.get("beta2_spectral_cap_violations") != 6 or
           audit.get("beta2_schur_cap_violations") != 0 or
           audit.get("baseline_beta0_spectral_cap_violations") != 18 or
           audit.get("baseline_beta0_schur_cap_violations") != 18 or
           audit.get("q_min") != 512 or audit.get("q_max") != 8192 or
           audit.get("count_min") != 512 or audit.get("count_max") != 1024 or
           audit.get("fixed_power_credit") != 0 or
           audit.get("arithmetic_advance") != "NO", "audit")
    expected_failure_keys = [
        [origin, 1024, q0, 1, "all_plus"]
        for origin in ORIGINS for q0 in (2048, 8192)]
    reject(audit.get("expected_parent_failure_pattern") != expected_failure_keys or
           audit.get("replicated_failure_keys") != expected_failure_keys or
           audit.get("failure_pattern_matches_parent") is not True,
           "failure pattern comparison")
    reject(payload.get("exact_theorem", {}).get("anchor_repair") != {
        "initial_interval": [1010342, 1010355],
        "initial_geometry_positive_beta0": False,
        "initial_geometry_positive_beta2": False,
        "selected_interval": [1010346, 1010359],
        "selected_offset": 4,
    }, "anchor repair")
    expected_firewall = {
        "TPC369_ORIGIN_FAMILY_PROTOCOL": "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
        "TPC369_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC369_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_144_ROWS",
        "TPC369_THIRD_ORIGIN_FAMILY": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_BETA2_PHASE_AUDIT": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_BETA2_FAILURE_PATTERN": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC369_INITIAL_ANCHOR_POSITIVITY": "REFUTED_SCOPED",
        "TPC369_REPAIRED_ANCHOR_RULE": "PROVED_EXACT_FINITE",
        "TPC369_ORIGIN_UNIFORMITY": "OPEN",
        "TPC369_WINDOW_UNIFORMITY": "OPEN",
        "TPC369_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC369_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC369_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC369_SOURCE_UNIFORM_L2": "OPEN",
        "TPC369_ARITHMETIC_ADVANCE": "NO",
        "TPC369_FIXED_POWER_CREDIT": 0,
        "TPC369_FULL_GATE_B": "OPEN",
        "TPC369_TWIN_PRIME_RESULT": "NONE",
    }
    firewall = payload.get("claim_firewall", {})
    for key, value in expected_firewall.items():
        reject(firewall.get(key) != value, "firewall " + key)
    reject(payload.get("round2_clue") !=
           "TEST_COUNT_2048_ORIGIN_PHASE_OR_RESIDUE_PHASE", "clue")


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
            (("payload", "protocol", "counts"), [512]),
            (("payload", "protocol", "q_anchors"), [512, 2048]),
            (("payload", "protocol", "kernel_exponents"), [1, 2]),
            (("payload", "protocol", "betas"), [0, 1, 2]),
            (("payload", "protocol", "spectra_for_all_laws"), False),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "Q"), 1024),
            (("payload", "rows", 0, "count"), 2048),
            (("payload", "rows", 0, "beta"), 1),
            (("payload", "rows", 0, "law"), "invented"),
            (("payload", "row_digest"), "0" * 64),
            (("payload", "finite_audit", "rows"), 143),
            (("payload", "finite_audit", "count_max"), 2048),
            (("payload", "finite_audit", "beta2_spectral_cap_violations"), 0),
            (("payload", "phase_summary", "cap_repair_betas"), [2]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 0),
            (("payload", "exact_theorem", "anchor_repair",
              "selected_offset"), 3),
            (("payload", "claim_firewall", "TPC369_BETA2_PHASE_AUDIT"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC369_ARITHMETIC_ADVANCE"), "YES"),
            (("payload", "claim_firewall", "TPC369_FIXED_POWER_CREDIT"), 1),
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
        print("TPC369_STRESS=PASS exact_baseline=1 mutations=30")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC369_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
