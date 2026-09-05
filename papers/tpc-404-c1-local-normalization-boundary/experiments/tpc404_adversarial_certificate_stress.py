#!/usr/bin/env python3
"""Strict mutation tests for the TPC-404 certificate contract."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-404-c1-local-normalization-boundary/results/tpc404_certificate.json"
STATUS = "PROVED_EXACT_FINITE_LOCAL_NORMALIZATION_BOUNDARY_AUDIT"
SCHEMA = "TPC404_C1_LOCAL_NORMALIZATION_BOUNDARY_V1"


class Failure(ValueError):
    pass


def canonical(v: object) -> bytes:
    return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


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
    if p.get("normalization") != "local_diagonal":
        raise Failure("normalization")
    identities = p.get("identities")
    expected = {
        "G_origin": "P_minus_sq*S0",
        "G_next": "P_minus_sq*S1+P_plus_sq*(S1-T1^2)",
        "normalized_square": "(T1*P_minus)^2/(G_origin*G_next)",
    }
    if identities != expected:
        raise Failure("identities")
    cases = p.get("cases")
    if type(cases) is not list or len(cases) != 4 or [c.get("m") for c in cases] != [1, 2, 3, 4]:
        raise Failure("case census")
    if any(c.get("exact_geometry_identity") is not True for c in cases):
        raise Failure("identity")
    firewall = p.get("claim_firewall")
    if type(firewall) is not dict or firewall.get("NORMALIZED_GROWING_THEOREM") != "OPEN":
        raise Failure("firewall")


def main() -> None:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    original = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants)
    validate(original)
    mutations = ("normalization", "identities", "case_count", "exact_geometry_identity", "firewall")
    rejected = 0
    for mutation in mutations:
        d = copy.deepcopy(original)
        if mutation == "normalization":
            d["payload"][mutation] = "global_diagonal"
        elif mutation == "identities":
            d["payload"][mutation]["G_next"] = "P_minus_sq*S1"
        elif mutation == "case_count":
            d["payload"]["cases"] = d["payload"]["cases"][:3]
        elif mutation == "exact_geometry_identity":
            d["payload"]["cases"][0][mutation] = False
        else:
            d["payload"]["claim_firewall"]["NORMALIZED_GROWING_THEOREM"] = "PROVED"
        d["payload_sha256"] = hashlib.sha256(canonical(d["payload"])).hexdigest()
        try:
            validate(d)
        except Failure:
            rejected += 1
    if rejected != len(mutations):
        raise Failure("mutation escaped")
    print(f"TPC404_STRESS=PASS mutations={len(mutations)} strict_contract=PASS")


if __name__ == "__main__":
    main()
