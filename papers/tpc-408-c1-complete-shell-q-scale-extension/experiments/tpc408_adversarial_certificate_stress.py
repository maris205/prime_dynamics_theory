#!/usr/bin/env python3
"""Strict fail-closed mutation tests for the TPC-408 certificate contract."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-408-c1-complete-shell-q-scale-extension/results/tpc408_certificate.json"
SCHEMA = "TPC408_C1_COMPLETE_SHELL_Q_SCALE_EXTENSION_V1"
STATUS = "PROVED_EXACT_FINITE_COMPLETE_SHELL_Q_SCALE_EXTENSION"


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
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1,
         "version")
    need(document["claim_status"] == STATUS, "header")
    payload = document["payload"]
    need(document["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(), "digest")
    need(payload.get("schema") == SCHEMA and payload.get("status") == STATUS, "status")
    need(payload.get("Q_scales") == [65536, 131072], "scales")
    need(payload.get("shell_counts") == [5709, 10749], "counts")
    need(payload.get("window_rule") == "N=264=4H", "window")
    need(payload.get("theorem", {}).get("coarse_uniform_bound") == "z<=4/(a_min*H)<=4/H", "bound")
    need(payload.get("theorem_domain", {}).get("parity", "").startswith("r may be odd"), "parity")
    need(payload.get("claim_firewall", {}).get("FULL_OPERATOR_NORM") == "OPEN", "operator firewall")
    cases = payload.get("cases")
    need(type(cases) is list and len(cases) == 2, "case census")
    need([c.get("Q") for c in cases] == [65536, 131072], "case order")
    need(all(c.get("uniform_bound_exact") is True and
             c.get("m_minus") + c.get("m_plus") == c.get("shell_count") and
             c.get("m_plus") == c.get("m_minus") + 1 for c in cases), "cases")


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates,
                          parse_constant=no_constants)
    validate(original)
    mutations = ("q_scales", "shell_counts", "window", "bound", "parity",
                 "operator", "case_count", "q_case", "exact_flag")
    rejected = 0
    for mutation in mutations:
        document = copy.deepcopy(original)
        payload = document["payload"]
        if mutation == "q_scales":
            payload["Q_scales"] = [65536]
        elif mutation == "shell_counts":
            payload["shell_counts"][0] = 5708
        elif mutation == "window":
            payload["window_rule"] = "N=H"
        elif mutation == "bound":
            payload["theorem"]["coarse_uniform_bound"] = "z<=8/H"
        elif mutation == "parity":
            payload["theorem_domain"]["parity"] = "even shells only"
        elif mutation == "operator":
            payload["claim_firewall"]["FULL_OPERATOR_NORM"] = "PROVED"
        elif mutation == "case_count":
            payload["cases"] = payload["cases"][:-1]
        elif mutation == "q_case":
            payload["cases"][0]["Q"] = 32768
        else:
            payload["cases"][0]["uniform_bound_exact"] = False
        document["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        try:
            validate(document)
        except ValueError:
            rejected += 1
    need(rejected == len(mutations), "mutation escaped")
    print(f"TPC408_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")


if __name__ == "__main__":
    main()
