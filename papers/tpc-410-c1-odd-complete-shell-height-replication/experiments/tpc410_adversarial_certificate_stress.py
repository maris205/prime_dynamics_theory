#!/usr/bin/env python3
"""Strict mutation tests for the TPC-410 height-replication contract."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-410-c1-odd-complete-shell-height-replication/results/tpc410_certificate.json"
SCHEMA = "TPC410_C1_ODD_COMPLETE_SHELL_HEIGHT_REPLICATION_V1"
STATUS = "PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_REPLICATION"


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":")) + "\n").encode()


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise ValueError("non-finite constant")


def validate(document):
    need(type(document) is dict and set(document) ==
         {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "header")
    payload = document["payload"]
    need(document["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(), "digest")
    need(payload.get("schema") == SCHEMA and payload.get("status") == STATUS, "status")
    need(payload.get("Q") == 131072 and payload.get("heights") == [16, 32, 66, 128], "scales")
    need(payload.get("shell_count") == 10749, "shell count")
    need(payload.get("window_rule") == "N=4H", "window")
    need(payload.get("theorem", {}).get("coarse_uniform_bound") == "z<=4/(a_min*H)<=4/H", "bound")
    need(payload.get("theorem_domain", {}).get("parity", "").startswith("r odd"), "parity")
    need(payload.get("claim_firewall", {}).get("FULL_OPERATOR_NORM") == "OPEN", "operator firewall")
    cases = payload.get("cases")
    need(type(cases) is list and len(cases) == 4, "case census")
    need([c.get("H") for c in cases] == [16, 32, 66, 128], "case order")
    need(all(c.get("N") == 4 * c.get("H") and c.get("uniform_bound_exact") is True and
             c.get("m_minus") + c.get("m_plus") == 10749 and
             c.get("m_plus") == c.get("m_minus") + 1 for c in cases), "cases")


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates,
                          parse_constant=no_constants)
    validate(original)
    mutations = ("height_list", "shell_count", "window", "bound", "parity",
                 "operator", "case_count", "height_case", "exact_flag")
    rejected = 0
    for mutation in mutations:
        document = copy.deepcopy(original)
        payload = document["payload"]
        if mutation == "height_list":
            payload["heights"] = [16, 32]
        elif mutation == "shell_count":
            payload["shell_count"] = 10748
        elif mutation == "window":
            payload["window_rule"] = "N=H"
        elif mutation == "bound":
            payload["theorem"]["coarse_uniform_bound"] = "z<=8/H"
        elif mutation == "parity":
            payload["theorem_domain"]["parity"] = "even shell only"
        elif mutation == "operator":
            payload["claim_firewall"]["FULL_OPERATOR_NORM"] = "PROVED"
        elif mutation == "case_count":
            payload["cases"] = payload["cases"][:-1]
        elif mutation == "height_case":
            payload["cases"][0]["H"] = 8
        else:
            payload["cases"][0]["uniform_bound_exact"] = False
        document["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        try:
            validate(document)
        except ValueError:
            rejected += 1
    need(rejected == len(mutations), "mutation escaped")
    print(f"TPC410_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")


if __name__ == "__main__":
    main()
