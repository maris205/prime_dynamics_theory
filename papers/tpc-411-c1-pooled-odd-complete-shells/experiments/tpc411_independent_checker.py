#!/usr/bin/env python3
"""Independent literal replay for the pooled TPC-411 profile."""
from __future__ import annotations
import hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-411-c1-pooled-odd-complete-shells/results/tpc411_certificate.json"
SCHEMA = "TPC411_C1_POOLED_ODD_COMPLETE_SHELLS_V1"
STATUS = "PROVED_EXACT_FINITE_POOLED_ODD_COMPLETE_SHELLS"
QS, COUNTS, H, N, B = (65536, 131072), (5709, 10749), 66, 264, 1_000_000


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key"); out[key] = value
    return out


def no_constants(value):
    raise ValueError("non-finite JSON constant")


def primes(limit):
    flags = bytearray(b"\1") * (limit + 1); flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]: flags[p * p:limit + 1:p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def txt(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def replay():
    items = []
    for Q, count in zip(QS, COUNTS):
        shell = [p for p in primes(2 * Q) if p > Q]; need(len(shell) == count, "shell census")
        items.extend((p, Q) for p in shell)
    ps, q_for = [p for p, _ in items], [q for _, q in items]
    residues = [0 if i % 2 == 0 else -N for i in range(len(ps))]
    period = math.prod(ps)
    residue = sum(r * (period // p) * pow(period // p, -1, p) for r, p in zip(residues, ps)) % period
    origin = residue + ((B - residue) // period + 1) * period
    t = lambda d: Fraction(H * H, H * H + d * d)
    S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0)); S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    aa = [Fraction(p ** 3, Q * Q * (p - 1)) for p, Q in items]; minus, plus = aa[1::2], aa[::2]
    vm = sum((a * a for a in minus), Fraction(0)); vp = sum((a * a for a in plus), Fraction(0)); pm = sum(minus, Fraction(0)); amin = min(aa)
    g0 = vm * S0; g1 = vm * S1 + vp * (S1 - t(1) ** 2); direct = t(1) * pm; z2 = direct * direct / (g0 * g1); sharp2 = t(1) ** 2 / (amin * amin * S0 * S1); coarse2 = Fraction(16, H * H)
    origin_mod = [origin % p for p in ps]; weights = [t(d) ** 2 for d in range(N)]; literal = []
    for offset in (0, 1):
        energy = Fraction(0)
        for p, a, r in zip(ps, aa, origin_mod):
            if (r + offset) % p == 0: continue
            inner = Fraction(0)
            for j in range(N):
                if j == offset or (r + j) % p == 0: continue
                inner += weights[abs(offset - j)]
            energy += a * a * inner
        literal.append(energy)
    signed = sum((-(-1) ** i * a * t(1) for i, a in enumerate(aa) if origin_mod[i] and (origin_mod[i] + 1) % ps[i]), Fraction(0))
    need(literal == [g0, g1] and signed == direct, "literal pooled masks"); need(z2 <= sharp2 <= coarse2, "bound")
    return {"H": H, "N": N, "m_minus": len(minus), "m_plus": len(plus), "shell_count": len(ps), "shell_counts": list(COUNTS), "Q_scales": list(QS), "origin_lower_bound": B, "selected_primes": ps, "prime_shell_Q": q_for, "residues": residues, "crt_residue": residue, "crt_period": period, "origin": origin, "S0": txt(S0), "S1": txt(S1), "a_min": txt(amin), "P_minus": txt(pm), "V_minus": txt(vm), "V_plus": txt(vp), "G0": txt(g0), "G1": txt(g1), "direct": txt(direct), "normalized_square": txt(z2), "sharp_bound_square": txt(sharp2), "coarse_bound_square_4_over_H": txt(coarse2), "uniform_bound_exact": True, "normalized_float64_observation": f"{math.sqrt(float(z2)):.15f}", "H_times_normalized_float64_observation": f"{H * math.sqrt(float(z2)):.15f}"}


def main():
    if sys.argv[1:] != ["--check"]: raise SystemExit("explicit --check required")
    d = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants); need(d["claim_status"] == STATUS, "status"); need(d["payload_sha256"] == hashlib.sha256(canonical(d["payload"])).hexdigest(), "digest")
    p = d["payload"]; need(p["schema"] == SCHEMA and p["cases"] == [replay()], "independent replay"); need(p["Q_scales"] == list(QS) and p["shell_counts"] == list(COUNTS), "scales"); need(p["claim_firewall"]["POOLED_ODD_COMPLETE_SHELLS"] == "PROVED_EXACT_FINITE", "firewall")
    print("TPC411_INDEPENDENT_CHECK=PASS cases=1 pooled_shells=2 literal_crt_masks=PASS")


if __name__ == "__main__": main()
