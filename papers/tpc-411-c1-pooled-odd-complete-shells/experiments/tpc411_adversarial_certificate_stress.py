#!/usr/bin/env python3
"""Strict mutation tests for the TPC-411 pooled certificate."""
from __future__ import annotations
import copy, hashlib, json, sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-411-c1-pooled-odd-complete-shells/results/tpc411_certificate.json"
SCHEMA = "TPC411_C1_POOLED_ODD_COMPLETE_SHELLS_V1"; STATUS = "PROVED_EXACT_FINITE_POOLED_ODD_COMPLETE_SHELLS"


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def need(condition, message):
    if type(condition) is not bool or not condition: raise ValueError(message)


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key"); out[key] = value
    return out


def no_constants(value): raise ValueError("non-finite constant")


def validate(d):
    need(type(d) is dict and set(d) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(d["certificate_version"] == 1 and d["claim_status"] == STATUS, "header")
    p = d["payload"]; need(d["payload_sha256"] == hashlib.sha256(canonical(p)).hexdigest(), "digest")
    need(p.get("schema") == SCHEMA and p.get("status") == STATUS, "status")
    need(p.get("Q_scales") == [65536, 131072] and p.get("shell_counts") == [5709, 10749], "scales")
    need(p.get("window_rule") == "N=264=4H" and p.get("shell_rule") == "pooled full shells Q<p<=2Q", "domain")
    need(p.get("theorem", {}).get("coarse_uniform_bound") == "z<=4/(a_min*H)<=4/H", "bound")
    need(p.get("claim_firewall", {}).get("FULL_OPERATOR_NORM") == "OPEN", "firewall")
    cs = p.get("cases"); need(type(cs) is list and len(cs) == 1, "case census")
    labels = cs[0].get("prime_shell_Q", [])
    need(cs[0].get("shell_count") == 16458 and cs[0].get("m_minus") == 8229 and cs[0].get("m_plus") == 8229 and cs[0].get("uniform_bound_exact") is True, "case")
    need(labels == [65536] * 5709 + [131072] * 10749, "shell labels")


def main():
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants); validate(original)
    mutations = ("q_scales", "shell_counts", "window", "bound", "prime_q", "operator", "case_count", "shell_count", "exact_flag"); rejected = 0
    for mutation in mutations:
        d = copy.deepcopy(original); p = d["payload"]
        if mutation == "q_scales": p["Q_scales"] = [65536]
        elif mutation == "shell_counts": p["shell_counts"][1] = 10748
        elif mutation == "window": p["window_rule"] = "N=H"
        elif mutation == "bound": p["theorem"]["coarse_uniform_bound"] = "z<=8/H"
        elif mutation == "prime_q": p["cases"][0]["prime_shell_Q"][0] = 131072
        elif mutation == "operator": p["claim_firewall"]["FULL_OPERATOR_NORM"] = "PROVED"
        elif mutation == "case_count": p["cases"] = []
        elif mutation == "shell_count": p["cases"][0]["shell_count"] = 16457
        else: p["cases"][0]["uniform_bound_exact"] = False
        d["payload_sha256"] = hashlib.sha256(canonical(p)).hexdigest()
        try: validate(d)
        except ValueError: rejected += 1
    need(rejected == len(mutations), "mutation escaped"); print(f"TPC411_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")


if __name__ == "__main__": main()
