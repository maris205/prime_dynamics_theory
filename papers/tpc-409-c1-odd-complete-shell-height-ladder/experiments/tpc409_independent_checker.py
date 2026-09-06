#!/usr/bin/env python3
"""Independent exact literal replay for TPC-409's odd-shell height ladder."""
from __future__ import annotations
import hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-409-c1-odd-complete-shell-height-ladder/results/tpc409_certificate.json"
SCHEMA = "TPC409_C1_ODD_COMPLETE_SHELL_HEIGHT_LADDER_V1"
STATUS = "PROVED_EXACT_FINITE_ODD_COMPLETE_SHELL_HEIGHT_LADDER"
Q, HEIGHTS, B = 65536, (16, 32, 66, 128), 1_000_000


def need(condition, message):
    if type(condition) is not bool or not condition:
        raise ValueError(message)


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
    raise ValueError("non-finite JSON constant")


def primes(limit):
    flags = bytearray(b"\1") * (limit + 1)
    flags[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def txt(value):
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def replay():
    shell = [p for p in primes(2 * Q) if p > Q]
    need(len(shell) == 5709, "shell census")
    amplitudes = [Fraction(p ** 3, Q * Q * (p - 1)) for p in shell]
    rows = []
    for H in HEIGHTS:
        N = 4 * H
        residues = [0 if i % 2 == 0 else -N for i in range(len(shell))]
        period = math.prod(shell)
        residue = sum(r * (period // p) * pow(period // p, -1, p)
                      for r, p in zip(residues, shell)) % period
        origin = residue + ((B - residue) // period + 1) * period
        t = lambda d: Fraction(H * H, H * H + d * d)
        S0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
        S1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
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
        origin_residues = [origin % p for p in shell]
        weights = [t(d) ** 2 for d in range(N)]
        literal = []
        for offset in (0, 1):
            energy = Fraction(0)
            for p, a, origin_mod_p in zip(shell, amplitudes, origin_residues):
                if (origin_mod_p + offset) % p == 0:
                    continue
                inner = Fraction(0)
                for j in range(N):
                    if j == offset or (origin_mod_p + j) % p == 0:
                        continue
                    inner += weights[abs(offset - j)]
                energy += a * a * inner
            literal.append(energy)
        signed = sum((-(-1) ** i * a * t(1) for i, a in enumerate(amplitudes)
                      if origin_residues[i] and (origin_residues[i] + 1) % shell[i]),
                     Fraction(0))
        need(literal == [G0, G1], "literal energies")
        need(signed == direct, "literal adjacent coefficient")
        need(z2 <= sharp2 <= coarse2, "exact bound")
        rows.append({
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
        })
    return rows


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    document = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates,
                          parse_constant=no_constants)
    need(type(document) is dict and set(document) ==
         {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(document["claim_status"] == STATUS, "status")
    need(document["payload_sha256"] == hashlib.sha256(canonical(document["payload"])).hexdigest(), "digest")
    payload = document["payload"]
    need(payload["schema"] == SCHEMA and payload["cases"] == replay(), "independent literal replay")
    need(payload["heights"] == list(HEIGHTS) and payload["shell_count"] == 5709, "height census")
    need(payload["theorem_domain"]["parity"].startswith("r odd"), "odd-shell domain")
    need(payload["claim_firewall"]["ODD_COMPLETE_SHELL_HEIGHT_LADDER"] == "PROVED_EXACT_FINITE", "firewall")
    print("TPC409_INDEPENDENT_CHECK=PASS cases=4 heights=4 literal_crt_masks=PASS odd_shell=PASS")


if __name__ == "__main__":
    main()
