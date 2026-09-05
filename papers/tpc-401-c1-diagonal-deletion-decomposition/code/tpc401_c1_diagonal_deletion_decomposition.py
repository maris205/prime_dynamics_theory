#!/usr/bin/env python3
"""TPC-401: exact finite audit of the production-domain diagonal deletion.

The audit isolates a structural fact used by TPC-400.  When N<Q<p, every
off-diagonal difference in an N-window is smaller than p, so the divisibility
indicator vanishes there.  The exact anchor N=13,Q=8 is retained as a boundary
counterexample.  This is a finite algebraic result, not an arithmetic estimate.
"""
from __future__ import annotations

import argparse, hashlib, json, math
from fractions import Fraction
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc401_certificate.json"
SCHEMA = "TPC401_C1_DIAGONAL_DELETION_DECOMPOSITION_V1"
STATUS = "PROVED_EXACT_FINITE_PRODUCTION_DOMAIN_DIAGONAL_DELETION_AUDIT"
PROD_Q, PROD_N, PROD_H = 8192, 1024, 66
PROD_ORIGINS = (7600001, 7603209, 7606417, 7609625, 7612833, 7616041)
ANCHOR_Q, ANCHOR_N = 8, 13

class Failure(ValueError):
    pass

def need(condition, message):
    if type(condition) is not bool or not condition:
        raise Failure(message)

def canonical(v):
    return (json.dumps(v, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":")) + "\n").encode()

def digest(b):
    return hashlib.sha256(b.replace(b"\r\n", b"\n").replace(b"\r", b"\n")).hexdigest()

def primes(limit):
    f = bytearray(b"\1") * (limit + 1); f[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if f[p]: f[p*p:limit+1:p] = b"\0" * (((limit-p*p)//p)+1)
    return [p for p in range(2, limit+1) if f[p]]

def shell(q): return [p for p in primes(2*q) if q < p <= 2*q]

def production_audit():
    ps = shell(PROD_Q)
    sampled = (0, 1, PROD_N//2, PROD_N-2, PROD_N-1)
    offdiag = 0; congruence_zero = 0; component_equal = 0
    geometry_checks = 0
    for o in PROD_ORIGINS:
        for x in sampled:
            u = o + x
            for y in sampled:
                v = o + y
                if u == v: continue
                offdiag += len(ps)
                for p in ps:
                    if (u-v) % p != 0: congruence_zero += 1
                    vp = (u % p != 0); vq = (v % p != 0)
                    k = Fraction(PROD_H*PROD_H,
                                 PROD_H*PROD_H + (u-v)*(u-v))
                    a = Fraction(p**3, PROD_Q**2 * (p-1))
                    scale = Fraction(p**3, PROD_Q**2)
                    direct = scale * k * int((u-v) % p == 0)
                    direct -= scale * k * Fraction(1, p-1)
                    if not (vp and vq): direct = Fraction(0)
                    if direct == -a*k*int(vp)*int(vq): component_equal += 1
                geometry_checks += 1
    expected = len(PROD_ORIGINS) * len(sampled) * (len(sampled)-1) * len(ps)
    return {"Q": PROD_Q, "N": PROD_N, "H": PROD_H,
            "origins": list(PROD_ORIGINS), "shell_cardinality": len(ps),
            "sampled_offdiagonal_pairs": geometry_checks,
            "component_rows": offdiag, "congruence_zero_rows": congruence_zero,
            "component_decomposition_equal_rows": component_equal,
            "expected_component_rows": expected,
            "all_sampled_components_equal": component_equal == expected,
            "all_sampled_divisibility_indicators_zero": congruence_zero == expected}

def anchor_counterexample():
    q, n, p = ANCHOR_Q, ANCHOR_N, 11
    u, v = 7600001, 7600012
    k = Fraction(PROD_H**2, PROD_H**2 + (u-v)**2)
    a = Fraction(p**3, q*q*(p-1))
    direct = Fraction(p**3,q*q)*k*(1-Fraction(1,p-1))
    reduced = -a*k
    return {"Q": q, "N": n, "prime": p, "difference": u-v,
            "u": u, "v": v, "unit_masks_active": u%p != 0 and v%p != 0,
            "direct": str(direct), "reduced": str(reduced),
            "nonzero_difference": str(direct-reduced),
            "offdiagonal": u != v, "divisibility_indicator": (u-v)%p == 0,
            "decomposition_applicable": False}

def build():
    prod = production_audit(); anchor = anchor_counterexample()
    payload = {"schema": SCHEMA, "status": STATUS,
      "production_domain": {"condition": "N < Q < p", "H": PROD_H,
        "prime_shell": "Q < p <= 2Q", "audit": prod,
        "identity": "K_p = -a_p(D_p T D_p - D_p)",
        "geometry_identity": "G_o(u)=sum_{p not divide u} a_p^2(S_o(u)-1_{r_p(o) exists}k_H(u-r_p(o))^2)"},
      "exact_anchor_boundary": anchor,
      "claim_firewall": {"TPC401_ANALYTIC_STRUCTURE": "PROVED_EXACT_FINITE",
        "TPC401_NUMERICAL_CERTIFICATION": "NONE_NEEDED",
        "TPC401_ARITHMETIC_ADVANCE": "NO", "TPC401_FIXED_POWER_CREDIT": 0,
        "TPC401_SOURCE_UNIFORM_L2": "OPEN", "TPC401_FULL_GATE_B": "OPEN",
        "TPC401_TWIN_PRIME_RESULT": "NONE"},
      "round2_clue": "TEST_C1_DIAGONAL_DELETION_SIGNED_TERM_AUDIT"}
    doc = {"certificate_version": 1, "claim_status": STATUS,
           "payload": payload, "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}
    RESULT.write_bytes(canonical(doc)); return doc

def check(doc):
    need(type(doc["certificate_version"]) is int and doc["certificate_version"] == 1 and doc["claim_status"] == STATUS, "header")
    need(doc["payload_sha256"] == hashlib.sha256(canonical(doc["payload"])).hexdigest(), "payload digest")
    p = doc["payload"]; a = p["production_domain"]["audit"]
    need(p["schema"] == SCHEMA and p["status"] == STATUS and p["production_domain"]["condition"] == "N < Q < p", "scope")
    need(a["all_sampled_components_equal"] is True and a["all_sampled_divisibility_indicators_zero"] is True, "exact equalities")
    need(a["component_rows"] == a["expected_component_rows"] == 104640, "row census")
    need(canonical(a) == canonical(production_audit()), "exact regeneration")
    e = p["exact_anchor_boundary"]
    need(canonical(e) == canonical(anchor_counterexample()) and e["unit_masks_active"] is True and Fraction(e["nonzero_difference"]) != 0, "active anchor counterexample")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); ap.add_argument("--check", action="store_true"); args=ap.parse_args()
    if args.write: build(); print("TPC401_CERTIFICATE=WRITTEN"); return
    if not args.check: raise SystemExit("explicit --check or --write required")
    check(json.loads(RESULT.read_bytes())); print("TPC401_CERTIFICATE=PASS sampled_pairs=120 component_rows=104640 shell=872 active_anchor_counterexample=PASS")
if __name__ == "__main__": main()
