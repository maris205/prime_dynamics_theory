#!/usr/bin/env python3
"""Strict contract mutation tests for TPC-403."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-403-c1-crt-origin-proxy-obstruction/results/tpc403_certificate.json"
STATUS = "PROVED_EXACT_FINITE_CRT_PROXY_OBSTRUCTION"
SCHEMA = "TPC403_C1_CRT_ORIGIN_PROXY_OBSTRUCTION_V1"


class Failure(ValueError):
    pass


def canonical(v: object) -> bytes:
    return (json.dumps(v, sort_keys=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise Failure("duplicate key")
        d[k] = v
    return d


def no_constants(v):
    raise Failure("non-finite constant")


def validate(d: dict) -> None:
    if type(d) is not dict or set(d) != {"certificate_version", "claim_status", "payload", "payload_sha256"}:
        raise Failure("document")
    if type(d["certificate_version"]) is not int or d["certificate_version"] != 1 or d["claim_status"] != STATUS:
        raise Failure("header")
    p = d["payload"]
    if type(p) is not dict or d["payload_sha256"] != hashlib.sha256(canonical(p)).hexdigest():
        raise Failure("digest")
    if p.get("schema") != SCHEMA or p.get("status") != STATUS:
        raise Failure("payload header")
    if p.get("negative_congruence") != "o = -N (mod p_i) for odd i":
        raise Failure("congruence")
    cases = p.get("cases")
    if type(cases) is not list or len(cases) != 4 or [c.get("m") for c in cases] != [1, 2, 3, 4]:
        raise Failure("case census")
    if any(c.get("exact_identity") is not True for c in cases):
        raise Failure("identity")


def main() -> None:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants)
    validate(original)
    mutations = ("negative_congruence", "case_count", "exact_identity")
    rejected = 0
    for mutation in mutations:
        d = copy.deepcopy(original)
        if mutation == "negative_congruence":
            d["payload"][mutation] = "o = +N (mod p_i) for odd i"
        elif mutation == "case_count":
            d["payload"]["cases"] = d["payload"]["cases"][:3]
        else:
            d["payload"]["cases"][0]["exact_identity"] = False
        d["payload_sha256"] = hashlib.sha256(canonical(d["payload"])).hexdigest()
        try:
            validate(d)
        except Failure:
            rejected += 1
    if rejected != len(mutations):
        raise Failure("mutation escaped")
    print("TPC403_STRESS=PASS mutations=3 strict_contract=PASS")


if __name__ == "__main__":
    main()
