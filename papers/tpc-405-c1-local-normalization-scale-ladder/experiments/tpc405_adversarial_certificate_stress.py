#!/usr/bin/env python3
"""Strict contract mutation tests for TPC-405."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-405-c1-local-normalization-scale-ladder/results/tpc405_certificate.json"
SCHEMA = "TPC405_C1_LOCAL_NORMALIZATION_SCALE_LADDER_V1"
STATUS = "PROVED_UNIFORM_FINITE_CRT_PROXY_ADJACENT_ENTRY_BOUND"


class Failure(ValueError):
    pass


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise Failure("duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise Failure("non-finite constant")


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise Failure(message)


def validate(d):
    need(type(d) is dict and set(d) == {"certificate_version","claim_status","payload","payload_sha256"}, "document")
    need(type(d["certificate_version"]) is int and d["certificate_version"] == 1 and d["claim_status"] == STATUS, "header")
    p = d["payload"]
    need(type(p) is dict and d["payload_sha256"] == hashlib.sha256(canonical(p)).hexdigest(), "digest")
    need(p.get("schema") == SCHEMA and p.get("status") == STATUS, "payload status")
    need(p.get("window_rule") == "N=4H", "window rule")
    need(p.get("theorem_domain", {}).get("H_and_N") == "integers H,N with H>=1 and N>=H+2", "integer domain")
    need(p.get("theorem", {}).get("coarse_uniform_bound") == "z<=4/(a_min*H)<=4/H", "bound")
    need(p.get("claim_firewall", {}).get("FULL_OPERATOR_NORM") == "OPEN", "full operator firewall")
    cases = p.get("cases")
    need(type(cases) is list and len(cases) == 20, "case census")
    need([(c.get("H"),c.get("m")) for c in cases] ==
         [(H,m) for H in (16,32,66,128,256) for m in (1,2,3,4)], "case order")
    need(all(c.get("uniform_bound_exact") is True for c in cases), "exact bound flags")


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates,
                          parse_constant=no_constants)
    validate(original)
    mutations = ("window_rule","integer_domain","bound","full_operator",
                 "case_count","exact_flag","height")
    rejected = 0
    for mutation in mutations:
        d = copy.deepcopy(original)
        if mutation == "window_rule":
            d["payload"]["window_rule"] = "N=H"
        elif mutation == "integer_domain":
            d["payload"]["theorem_domain"]["H_and_N"] = "real H,N"
        elif mutation == "bound":
            d["payload"]["theorem"]["coarse_uniform_bound"] = "z<=8/H"
        elif mutation == "full_operator":
            d["payload"]["claim_firewall"]["FULL_OPERATOR_NORM"] = "PROVED"
        elif mutation == "case_count":
            d["payload"]["cases"] = d["payload"]["cases"][:-1]
        elif mutation == "exact_flag":
            d["payload"]["cases"][0]["uniform_bound_exact"] = False
        else:
            d["payload"]["cases"][0]["H"] = 15
        d["payload_sha256"] = hashlib.sha256(canonical(d["payload"])).hexdigest()
        try:
            validate(d)
        except Failure:
            rejected += 1
    need(rejected == len(mutations), "mutation escaped")
    print(f"TPC405_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")


if __name__ == "__main__":
    main()
