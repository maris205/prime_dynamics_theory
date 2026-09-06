#!/usr/bin/env python3
"""Exact pooled two-shell CRT replay for the TPC local proxy entry."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc411_certificate.json"
SCHEMA = "TPC411_C1_POOLED_ODD_COMPLETE_SHELLS_V1"
STATUS = "PROVED_EXACT_FINITE_POOLED_ODD_COMPLETE_SHELLS"
QS, H, N, B = (65536, 131072), 66, 264, 1_000_000
COUNTS = (5709, 10749)


class Failure(ValueError):
    pass


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise Failure("non-finite JSON constant")


def primes(limit):
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def crt(residues, moduli):
    period = math.prod(moduli)
    residue = sum(r * (period // p) * pow(period // p, -1, p)
                  for r, p in zip(residues, moduli)) % period
    return residue, period


def txt(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def shells():
    out = []
    for Q, expected in zip(QS, COUNTS):
        shell = [p for p in primes(2 * Q) if p > Q]
        need(len(shell) == expected, "shell census")
        out.extend((p, Q) for p in shell)
    return out


def row(items):
    primes_all = [p for p, _ in items]
    q_for = [q for _, q in items]
    need(len(primes_all) % 2 == 0 and min(primes_all) > N, "pooled domain")
    residues = [0 if i % 2 == 0 else -N for i in range(len(primes_all))]
    residue, period = crt(residues, primes_all)
    origin = residue + ((B - residue) // period + 1) * period
    t = lambda d: Fraction(H * H, H * H + d * d)
    S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
    S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    amplitudes = [Fraction(p ** 3, q * q * (p - 1)) for p, q in items]
    minus, plus = amplitudes[1::2], amplitudes[::2]
    Vminus = sum((a * a for a in minus), Fraction(0))
    Vplus = sum((a * a for a in plus), Fraction(0))
    Pminus = sum(minus, Fraction(0))
    amin = min(amplitudes)
    G0 = Vminus * S0
    G1 = Vminus * S1 + Vplus * (S1 - t(1) ** 2)
    direct = t(1) * Pminus
    z2 = direct * direct / (G0 * G1)
    sharp2 = t(1) ** 2 / (amin * amin * S0 * S1)
    coarse2 = Fraction(16, H * H)
    need(origin > B and G0 > 0 and G1 > 0 and z2 <= sharp2 <= coarse2, "bound")
    return {
        "H": H, "N": N, "m_minus": len(minus), "m_plus": len(plus),
        "shell_count": len(items), "shell_counts": list(COUNTS), "Q_scales": list(QS),
        "origin_lower_bound": B, "selected_primes": primes_all, "prime_shell_Q": q_for,
        "residues": residues, "crt_residue": residue, "crt_period": period, "origin": origin,
        "S0": txt(S0), "S1": txt(S1), "a_min": txt(amin), "P_minus": txt(Pminus),
        "V_minus": txt(Vminus), "V_plus": txt(Vplus), "G0": txt(G0), "G1": txt(G1),
        "direct": txt(direct), "normalized_square": txt(z2),
        "sharp_bound_square": txt(sharp2), "coarse_bound_square_4_over_H": txt(coarse2),
        "uniform_bound_exact": True,
        "normalized_float64_observation": f"{math.sqrt(float(z2)):.15f}",
        "H_times_normalized_float64_observation": f"{H * math.sqrt(float(z2)):.15f}",
    }


def payload():
    items = shells()
    return {
        "schema": SCHEMA, "status": STATUS, "Q_scales": list(QS), "H": H, "N": N,
        "origin_lower_bound": B, "shell_rule": "pooled full shells Q<p<=2Q",
        "shell_counts": list(COUNTS), "shell_sha256": {
            str(Q): hashlib.sha256(canonical([p for p, q in items if q == Q])).hexdigest()
            for Q in QS}, "window_rule": "N=264=4H", "normalization": "pooled complete-shell local diagonal",
        "theorem_domain": {
            "H_and_N": "fixed integers H=66,N=264 with N=4H",
            "Q_and_shell": "two full odd shells Q=65536 and Q=131072, pooled without deletion",
            "profile": "pooled primes ordered increasingly; even i residue 0, odd i residue -N",
            "amplitude": "a_i=p_i^3/[Q_i^2(p_i-1)] using each prime's declared shell Q_i",
            "parity": "pooled cardinality r=16458 is even, with m_minus=m_plus=8229",
            "origin": "o is a CRT solution above the declared origin lower bound",
            "proxy": "complete-shell masked local geometry from TPC-404",
        },
        "theorem": {
            "exact_sharp_bound": "0<=z<=t1/(a_min*sqrt(S0*S1))",
            "coarse_uniform_bound": "z<=4/(a_min*H)<=4/H",
            "proof_steps": ["P_minus^2<=m_minus*V_minus", "G1>=V_minus*S1",
                            "V_minus>=m_minus*a_min^2", "S0>=H/4", "S1>=H/4", "a_min>=1"],
            "scope": "one pooled adjacent normalized proxy entry, not the full operator",
        },
        "cases": [row(items)],
        "claim_firewall": {
            "POOLED_ODD_COMPLETE_SHELLS": "PROVED_EXACT_FINITE",
            "POOLED_DECIMAL": "NUMERICAL_OBSERVATION", "FULL_OPERATOR_NORM": "OPEN",
            "NORMALIZED_GROWING_THEOREM": "OPEN", "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN",
            "ARITHMETIC_ADVANCE": "NO", "FIXED_POWER_CREDIT": 0, "FULL_GATE_B": "OPEN",
            "TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_C1_POOLED_COMPLETE_SHELL_EXTENSION",
    }


def write():
    p = payload()
    RESULT.write_bytes(canonical({"certificate_version": 1, "claim_status": STATUS,
                                  "payload": p,
                                  "payload_sha256": hashlib.sha256(canonical(p)).hexdigest()}))


def check_document(document):
    need(type(document) is dict and set(document) ==
         {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "claim status")
    need(document["payload_sha256"] == hashlib.sha256(canonical(document["payload"])).hexdigest(), "digest")
    need(canonical(document["payload"]) == canonical(payload()), "exact pooled certificate")


def main():
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write(); print("TPC411_CERTIFICATE=WRITTEN")
    elif args.check:
        check_document(json.loads(RESULT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants)); print("TPC411_CERTIFICATE=PASS cases=1 pooled_shells=2 literal_domain=PASS")
    else:
        raise SystemExit("explicit --check or --write required")


if __name__ == "__main__":
    main()
