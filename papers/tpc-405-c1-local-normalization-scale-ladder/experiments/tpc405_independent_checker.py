#!/usr/bin/env python3
"""Independent exact replay of the TPC-405 scale ladder and CRT masks."""
from __future__ import annotations
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-405-c1-local-normalization-scale-ladder/results/tpc405_certificate.json"
SCHEMA = "TPC405_C1_LOCAL_NORMALIZATION_SCALE_LADDER_V1"
STATUS = "PROVED_UNIFORM_FINITE_CRT_PROXY_ADJACENT_ENTRY_BOUND"
Q, B = 8192, 1_000_000
HEIGHTS, MULTIPLICITIES = (16, 32, 66, 128, 256), (1, 2, 3, 4)


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise ValueError("non-finite JSON constant")


def primes(limit):
    f = bytearray(b"\1") * (limit + 1)
    f[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if f[p]:
            f[p*p : limit+1 : p] = b"\0" * (((limit-p*p)//p)+1)
    return [p for p in range(2, limit+1) if f[p]]


def txt(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def replay():
    shell = [p for p in primes(2*Q) if p > Q]
    need(len(shell) == 872, "shell")
    result = []
    for H in HEIGHTS:
        N = 4*H
        t = lambda d: Fraction(H*H, H*H+d*d)
        S0 = sum((t(d)**2 for d in range(1,N)), Fraction(0))
        S1 = sum((t(d)**2 for d in range(1,N-1)), Fraction(0)) + t(1)**2
        for m in MULTIPLICITIES:
            selected = shell[:2*m]
            residues = [0 if i % 2 == 0 else -N for i in range(2*m)]
            period = math.prod(selected)
            residue = sum(r*(period//p)*pow(period//p,-1,p)
                          for r,p in zip(residues,selected)) % period
            origin = residue + ((B-residue)//period+1)*period
            aa = [Fraction(p**3,Q*Q*(p-1)) for p in selected]
            vm = sum((a*a for a in aa[1::2]), Fraction(0))
            vp = sum((a*a for a in aa[::2]), Fraction(0))
            pm = sum(aa[1::2], Fraction(0))
            amin = min(aa)
            g0 = vm*S0
            g1 = vm*S1 + vp*(S1-t(1)**2)
            direct = t(1)*pm
            z2 = direct*direct/(g0*g1)
            sharp2 = t(1)**2/(amin*amin*S0*S1)
            coarse2 = Fraction(16,H*H)
            # Literal masked row-energy replay, not a formula import.
            literal = []
            for offset in (0,1):
                energy = Fraction(0)
                for p,a in zip(selected,aa):
                    if (origin+offset) % p == 0:
                        continue
                    energy += a*a*sum((t(offset-j)**2 for j in range(N)
                                      if j != offset and (origin+j) % p != 0),
                                     Fraction(0))
                literal.append(energy)
            signed_direct = sum((-(-1)**i*aa[i]*t(1) for i,p in enumerate(selected)
                                 if origin % p and (origin+1) % p), Fraction(0))
            need(literal == [g0,g1] and signed_direct == direct, "literal masks")
            need(z2 <= sharp2 <= coarse2, "bound")
            result.append({
                "H":H,"N":N,"m":m,"Q":Q,"origin_lower_bound":B,
                "selected_primes":selected,"residues":residues,
                "crt_residue":residue,"crt_period":period,"origin":origin,
                "S0":txt(S0),"S1":txt(S1),"a_min":txt(amin),
                "P_minus":txt(pm),"V_minus":txt(vm),"V_plus":txt(vp),
                "G0":txt(g0),"G1":txt(g1),"direct":txt(direct),
                "normalized_square":txt(z2),"sharp_bound_square":txt(sharp2),
                "coarse_bound_square_4_over_H":txt(coarse2),
                "uniform_bound_exact":True,
                "normalized_float64_observation":f"{math.sqrt(float(z2)):.15f}",
                "H_times_normalized_float64_observation":f"{H*math.sqrt(float(z2)):.15f}",
            })
    return result


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    d = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates,
                   parse_constant=no_constants)
    need(type(d) is dict and set(d) == {"certificate_version","claim_status","payload","payload_sha256"}, "document")
    need(type(d["certificate_version"]) is int and d["certificate_version"] == 1, "version")
    need(d["claim_status"] == STATUS, "status")
    need(d["payload_sha256"] == hashlib.sha256(canonical(d["payload"])).hexdigest(), "digest")
    p = d["payload"]
    need(p["schema"] == SCHEMA and p["cases"] == replay(), "independent replay")
    need(p["theorem_domain"]["H_and_N"] == "integers H,N with H>=1 and N>=H+2", "integer domain")
    need(p["claim_firewall"]["LOCAL_PROXY_ENTRY_BOUND"] == "PROVED_UNIFORM", "firewall")
    print("TPC405_INDEPENDENT_CHECK=PASS cases=20 literal_crt_masks=PASS uniform_bound=PASS")


if __name__ == "__main__":
    main()
