#!/usr/bin/env python3
"""Mutation stress test for the TPC-364 finite certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CERTIFICATE = ROOT / (
    "papers/tpc-364-shell-tilt-phase-diagram/results/"
    "tpc364_certificate.json")
SCHEMA = "TPC364_SHELL_TILT_PHASE_DIAGRAM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SHELL_TILT_PHASE_DIAGRAM"
BETAS = [-2, -1, 0, 1, 2]
LAWS = ["all_plus", "alternating_index", "mod4_character", "half_split"]


class Rejected(Exception):
    pass


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def validate(document: dict[str, Any]) -> None:
    if (document.get("certificate_version") != 1 or
            document.get("claim_status") != STATUS):
        raise Rejected("header")
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise Rejected("schema")
    if document.get("payload_sha256") != hashlib.sha256(
            canonical(payload)).hexdigest():
        raise Rejected("payload hash")
    protocol = payload.get("protocol", {})
    if (protocol.get("origins") != [313030, 311166, 321651] or
            protocol.get("counts") != [256, 512] or
            protocol.get("q_anchors") != [80, 128, 256, 512] or
            protocol.get("kernel_exponents") != [1, 2] or
            protocol.get("laws") != LAWS or
            protocol.get("betas") != BETAS or
            protocol.get("spectra_for_all_laws") is not True or
            protocol.get("source_response_used") is not False):
        raise Rejected("protocol")
    rows = payload.get("rows")
    if not isinstance(rows, list) or len(rows) != 960:
        raise Rejected("rows")
    keys = {(row.get("origin"), row.get("count"), row.get("Q"),
             row.get("kernel_exponent"), row.get("beta"), row.get("law"))
            for row in rows}
    if len(keys) != 960:
        raise Rejected("row keys")
    if payload.get("row_digest") != hashlib.sha256(
            canonical(rows)).hexdigest():
        raise Rejected("row digest")
    phase = payload.get("phase_summary", {})
    if phase.get("cap_repair_betas") != [2]:
        raise Rejected("repair beta")
    by_beta = phase.get("by_beta", {})
    expected = {-2: 63, -1: 36, 0: 30, 1: 30, 2: 0}
    for beta, violations in expected.items():
        item = by_beta.get(str(beta), {})
        if (item.get("rows") != 192 or
                item.get("spectral_cap_violations") != violations):
            raise Rejected("phase " + str(beta))
    audit = payload.get("finite_audit", {})
    if (audit.get("rows") != 960 or
            audit.get("settings_per_beta") != 48 or
            audit.get("beta_count") != 5 or
            audit.get("spectral_rows") != 960 or
            audit.get("beta2_cap_repair_rows") != 192 or
            audit.get("beta2_total_rows") != 192 or
            audit.get("baseline_beta0_cap_violations") != 30 or
            audit.get("fixed_power_credit") != 0 or
            audit.get("arithmetic_advance") != "NO"):
        raise Rejected("audit")
    firewall = payload.get("claim_firewall", {})
    expected_firewall = {
        "TPC364_WEIGHTED_BLOCK_DEFINITION": "PROVED_EXACT_FINITE",
        "TPC364_WEIGHTED_GEOMETRY_POSITIVITY": "PROVED_EXACT_FINITE",
        "TPC364_FINITE_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_960_ROWS",
        "TPC364_PHASE_DIAGRAM": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_PANEL_CAP_REPAIR": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
        "TPC364_BETA2_ASYMPTOTIC_REPAIR": "OPEN",
        "TPC364_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
        "TPC364_GROWING_OPERATOR_BOUND": "OPEN",
        "TPC364_SOURCE_UNIFORM_L2": "OPEN",
        "TPC364_ARITHMETIC_ADVANCE": "NO",
        "TPC364_FIXED_POWER_CREDIT": 0,
        "TPC364_FULL_GATE_B": "OPEN", "TPC364_TWIN_PRIME_RESULT": "NONE",
    }
    for key, value in expected_firewall.items():
        if firewall.get(key) != value:
            raise Rejected("firewall " + key)


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("--check is the only argument")
    try:
        document = json.loads(CERTIFICATE.read_bytes())
        validate(document)
        baseline = hashlib.sha256(canonical(document)).hexdigest()
        mutations = [
            (("payload", "schema"), "MUTATED"),
            (("payload", "protocol", "betas"), [-1, 0, 1]),
            (("payload", "protocol", "q_anchors"), [80, 128, 256]),
            (("payload", "protocol", "source_response_used"), True),
            (("payload", "rows"), []),
            (("payload", "rows", 0, "beta"), 99),
            (("payload", "finite_audit", "rows"), 959),
            (("payload", "finite_audit", "beta2_cap_repair_rows"), 191),
            (("payload", "phase_summary", "cap_repair_betas"), [1]),
            (("payload", "phase_summary", "by_beta", "2",
              "spectral_cap_violations"), 1),
            (("payload", "phase_summary", "by_beta", "0",
              "spectral_cap_violations"), 0),
            (("payload", "phase_summary", "cap"), "0.5"),
            (("payload", "claim_firewall", "TPC364_BETA2_ASYMPTOTIC_REPAIR"),
             "PROVED"),
            (("payload", "claim_firewall", "TPC364_ARITHMETIC_ADVANCE"),
             "YES"),
            (("payload", "claim_firewall", "TPC364_FIXED_POWER_CREDIT"), 1),
            (("payload", "claim_firewall", "TPC364_FULL_GATE_B"), "PASS"),
            (("payload", "row_digest"), "0" * 64),
            (("payload_sha256",), "0" * 64),
        ]
        rejected = 0
        for path, value in mutations:
            item = copy.deepcopy(document)
            target: Any = item
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            try:
                validate(item)
            except Rejected:
                rejected += 1
        if (rejected != len(mutations) or
                hashlib.sha256(canonical(document)).hexdigest() != baseline):
            raise Rejected("mutation census")
        print("TPC364_STRESS=PASS exact_baseline=1 mutations=18")
        return 0
    except (Rejected, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC364_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
