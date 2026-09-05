#!/usr/bin/env python3
"""Independent exact replay of the TPC-404 local geometry formulas."""
from __future__ import annotations
import hashlib, json, math, sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)

ROOT = Path(__file__).resolve().parents[3]
CERT = ROOT / "papers/tpc-404-c1-local-normalization-boundary/results/tpc404_certificate.json"
STATUS = "PROVED_EXACT_FINITE_LOCAL_NORMALIZATION_BOUNDARY_AUDIT"
Q, N, H = 8192, 1024, 66


def canon(v):
    return (json.dumps(v, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode()


def need(c, m):
    if type(c) is not bool or not c:
        raise ValueError(m)


def ps(limit):
    f = bytearray(b"\1") * (limit + 1)
    f[:2] = b"\0\0"
    for p in range(2, math.isqrt(limit) + 1):
        if f[p]:
            f[p * p : limit + 1 : p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if f[p]]


def ft(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def no_duplicates(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, "duplicate key")
        out[key] = value
    return out


def no_constants(value):
    raise ValueError("non-finite JSON constant")


def replay():
    shell = [p for p in ps(2 * Q) if p > Q][:8]
    t = lambda d: Fraction(H * H, H * H + d * d)
    s0 = sum((t(d) ** 2 for d in range(1, N)), Fraction(0))
    s1 = sum((t(d) ** 2 for d in range(1, N - 1)), Fraction(0)) + t(1) ** 2
    out = []
    for m in range(1, 5):
        aa = [Fraction(p**3, Q**2 * (p - 1)) for p in shell[: 2 * m]]
        pp2 = sum((x * x for x in aa[::2]), Fraction(0))
        pm2 = sum((x * x for x in aa[1::2]), Fraction(0))
        pm = sum(aa[1::2], Fraction(0))
        g0 = pm2 * s0
        g1 = pm2 * s1 + pp2 * (s1 - t(1) ** 2)
        direct = t(1) * pm
        ns = direct * direct / (g0 * g1)
        need(g0 > 0 and g1 > 0 and ns > 0, "positive geometry")
        # Independently reconstruct an actual CRT origin and literal masked rows.
        selected = shell[:2*m]
        period = math.prod(selected)
        origin = sum((0 if i % 2 == 0 else -N) * (period // p)
                     * pow(period // p, -1, p) for i, p in enumerate(selected)) % period
        origin += ((1000000-origin)//period+1)*period
        literal = []
        for offset in (0, 1):
            energy = Fraction(0)
            for p, amplitude in reversed(tuple(zip(selected, aa))):
                if (origin+offset) % p == 0:
                    continue
                energy += amplitude**2 * sum((t(offset-j)**2 for j in range(N)
                          if j != offset and (origin+j) % p != 0), Fraction(0))
            literal.append(energy)
        literal_direct = sum((-(-1)**i * aa[i] * t(1)
                              for i, p in enumerate(selected)
                              if origin % p and (origin+1) % p), Fraction(0))
        need(literal == [g0, g1] and literal_direct == direct, "literal CRT masked row energies")
        out.append({"m": m, "selected_primes": shell[: 2 * m], "origin_lower_bound": 1000000,
                    "S_offset_0": ft(s0), "S_offset_1": ft(s1), "P_minus": ft(pm),
                    "P_plus_sq": ft(pp2), "P_minus_sq": ft(pm2), "direct": ft(direct),
                    "G_origin": ft(g0), "G_next": ft(g1), "normalized_square": ft(ns),
                    "normalized_float64_observation": f"{math.sqrt(float(ns)):.15f}",
                    "exact_geometry_identity": True})
    return out


def main():
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check required")
    d = json.loads(CERT.read_bytes(), object_pairs_hook=no_duplicates, parse_constant=no_constants)
    need(type(d) is dict and set(d) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "document")
    need(type(d["certificate_version"]) is int and d["certificate_version"] == 1, "version")
    p = d["payload"]
    need(d["claim_status"] == STATUS, "status")
    need(d["payload_sha256"] == hashlib.sha256(canon(p)).hexdigest(), "digest")
    need(canon(p["cases"]) == canon(replay()), "typed replay")
    need(p["normalization"] == "local_diagonal", "normalization")
    print("TPC404_INDEPENDENT_CHECK=PASS cases=4 local_diagonal=PASS literal_crt_geometry=PASS")


if __name__ == "__main__":
    main()
