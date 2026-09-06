#!/usr/bin/env python3
"""Exact odd complete-shell height ladder for the TPC local proxy entry."""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc409_certificate.json"
SCHEMA = "TPC409_C1_ODD_COMPLETE_SHELL_HEIGHT_LADDER_V1"
STATUS = "PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_LADDER"
Q, HEIGHTS, B = 65536, (16, 32, 66, 128), 1_000_000
EXPECTED_SHELL_COUNT = 5709


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


def shell_primes():
    shell = [p for p in primes(2 * Q) if p > Q]
    need(len(shell) == EXPECTED_SHELL_COUNT, "complete shell census")
    return shell


def row(H, shell):
    N = 4 * H
    need(Q > N, "window below shell")
    residues = [0 if i % 2 == 0 else -N for i in range(len(shell))]
    residue, period = crt(residues, shell)
    origin = residue + ((B - residue) // period + 1) * period
    t = lambda d: Fraction(H * H, H * H + d * d)
    S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
    S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    amplitudes = [Fraction(p ** 3, Q * Q * (p - 1)) for p in shell]
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
        "H": H, "N": N, "Q": Q, "m_minus": len(minus), "m_plus": len(plus),
        "shell_count": len(shell), "origin_lower_bound": B,
        "selected_primes": shell, "residues": residues,
        "crt_residue": residue, "crt_period": period, "origin": origin,
        "S0": txt(S0), "S1": txt(S1), "a_min": txt(amin),
        "P_minus": txt(Pminus), "V_minus": txt(Vminus), "V_plus": txt(Vplus),
        "G0": txt(G0), "G1": txt(G1), "direct": txt(direct),
        "normalized_square": txt(z2), "sharp_bound_square": txt(sharp2),
        "coarse_bound_square_4_over_H": txt(coarse2), "uniform_bound_exact": True,
        "normalized_float64_observation": f"{math.sqrt(float(z2)):.15f}",
        "H_times_normalized_float64_observation": f"{H * math.sqrt(float(z2)):.15f}",
    }


def payload():
    shell = shell_primes()
    return {
        "schema": SCHEMA, "status": STATUS, "Q": Q,
        "heights": list(HEIGHTS), "window_rule": "N=4H",
        "origin_lower_bound": B, "shell_rule": "all primes Q<p<=2Q",
        "shell_count": EXPECTED_SHELL_COUNT,
        "shell_sha256": hashlib.sha256(canonical(shell)).hexdigest(),
        "normalization": "complete-shell local diagonal",
        "theorem_domain": {
            "H_and_N": "fixed integer heights H in {16,32,66,128} with N=4H",
            "Q_and_shell": "Q=65536>N and the complete odd shell Q<p<=2Q with r=5709 primes",
            "profile": "all shell primes, indexed increasingly; even i residue 0, odd i residue -N",
            "parity": "r odd; m_plus=ceil(r/2)=2855 and m_minus=floor(r/2)=2854",
            "origin": "o is a CRT solution above the declared origin lower bound",
            "proxy": "complete-shell masked local geometry from TPC-404",
        },
        "theorem": {
            "exact_sharp_bound": "0<=z<=t1/(a_min*sqrt(S0*S1))",
            "coarse_uniform_bound": "z<=4/(a_min*H)<=4/H",
            "proof_steps": ["P_minus^2<=m_minus*V_minus", "G1>=V_minus*S1",
                            "V_minus>=m_minus*a_min^2", "S0>=H/4", "S1>=H/4", "a_min>=1"],
            "scope": "one adjacent normalized proxy entry across a finite odd-shell height ladder, not the full operator",
        },
        "cases": [row(H, shell) for H in HEIGHTS],
        "claim_firewall": {
            "ODD_COMPLETE_SHELL_HEIGHT_LADDER": "PROVED_EXACT_FINITE",
            "HEIGHT_LADDER_DECIMALS": "NUMERICAL_OBSERVATION",
            "FULL_OPERATOR_NORM": "OPEN", "NORMALIZED_GROWING_THEOREM": "OPEN",
            "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN", "ARITHMETIC_ADVANCE": "NO",
            "FIXED_POWER_CREDIT": 0, "FULL_GATE_B": "OPEN", "TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "TEST_C1_ODD_COMPLETE_SHELL_HEIGHT_EXTENSION",
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
    need(canonical(document["payload"]) == canonical(payload()), "exact height ladder")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write:
        write(); print("TPC409_CERTIFICATE=WRITTEN")
    elif args.check:
        check_document(json.loads(RESULT.read_bytes(), object_pairs_hook=no_duplicates,
                                  parse_constant=no_constants))
        print("TPC409_CERTIFICATE=PASS cases=4 heights=4 odd_complete_shell=PASS")
    else:
        raise SystemExit("explicit --check or --write required")


if __name__ == "__main__":
    main()
