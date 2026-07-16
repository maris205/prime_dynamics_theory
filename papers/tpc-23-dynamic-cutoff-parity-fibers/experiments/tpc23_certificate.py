#!/usr/bin/env python3
"""Exact structural certificate for TPC-23.

The certificate uses integers and Fraction only.  Logarithms are stored
formally as prime-basis vectors, so no floating-point arithmetic enters
the divisor identities.  It is an audit of exact formulas and exponent
bookkeeping, not numerical evidence for any asymptotic statement.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


def factor(n: int) -> dict[int, int]:
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors(n: int) -> list[int]:
    ds = [1]
    for p, e in factor(n).items():
        ds = [d * p**j for d in ds for j in range(e + 1)]
    return sorted(ds)


def mobius(n: int) -> int:
    fs = factor(n)
    if any(e > 1 for e in fs.values()):
        return 0
    return -1 if len(fs) % 2 else 1


def liouville(n: int) -> int:
    return -1 if sum(factor(n).values()) % 2 else 1


def add_vec(dst: defaultdict[int, int], src: dict[int, int], scale: int = 1) -> None:
    for p, c in src.items():
        dst[p] += scale * c
        if dst[p] == 0:
            del dst[p]


def log_vec(n: int) -> dict[int, int]:
    return {p: e for p, e in factor(n).items()}


def a_vec(n: int) -> dict[int, int]:
    mu = mobius(n)
    if mu == 0:
        return {}
    return {p: -mu * e for p, e in factor(n).items()}


def tail_vec(n: int, y: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for u in divisors(n):
        if u > y:
            add_vec(out, a_vec(u))
    return dict(out)


def complement_vec(n: int, y: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for r in divisors(n):
        if r * y < n:
            add_vec(out, a_vec(n // r))
    return dict(out)


def liouville_cocycle_vec(n: int, y: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for r in divisors(n):
        if r * y >= n:
            continue
        q = n // r
        mu2 = mobius(q) ** 2
        coeff = -liouville(n) * liouville(r) * mu2
        add_vec(out, log_vec(q), coeff)
    return dict(out)


def balanced_split_vec(n: int, y: int) -> dict[int, int]:
    out: defaultdict[int, int] = defaultdict(int)
    for r in divisors(n):
        if r <= y or (r > y and r * y < n):
            add_vec(out, a_vec(n // r))
    return dict(out)


def crt_solutions(m1: int, m2: int, h: int, r: int, s: int) -> tuple[int, list[int]]:
    q = math.lcm(r, s)
    sols = [j for j in range(q) if (m1 * j + h) % r == 0 and (m2 * j + h) % s == 0]
    return q, sols


def exponent_checks() -> int:
    checks = 0
    for bi in range(4, 15):
        beta = Fraction(bi, 20)
        for si in range(1, 13):
            s = Fraction(si, 20)
            eta_star = min(
                1 - Fraction(3, 2) * beta,
                (beta + 1 - 4 * s) / 2,
                (3 - beta - 6 * s) / 4,
            )
            for f1i in range(si + 1):
                f1 = Fraction(f1i, 20)
                for f2i in range(si + 1):
                    f2 = Fraction(f2i, 20)
                    k1 = max(f1, beta - f1)
                    k2 = max(f2, beta - f2)
                    for y in (Fraction(0), s, 2 * s):
                        eta_a = (beta + 1 - y - k1 - k2) / 2
                        eta_b = 1 - f1 - f2 - (k1 + k2) / 2
                        if max(eta_a, eta_b) < eta_star:
                            raise AssertionError((beta, s, f1, f2, y, eta_a, eta_b, eta_star))
                        checks += 1
    return checks


def profile_checks() -> int:
    """Verify each affine profile identity at three noncollinear points."""

    points = (
        (Fraction(1, 2000), Fraction(1, 200)),
        (Fraction(1, 3000), Fraction(1, 100)),
        (Fraction(1, 4000), Fraction(3, 200)),
    )
    (s1, t1), (s2, t2), (s3, t3) = points
    if (s2 - s1) * (t3 - t1) == (s3 - s1) * (t2 - t1):
        raise AssertionError("profile test points are collinear")

    checks = 0
    for sigma, t in points:
        if not (0 < sigma < Fraction(1, 1000)):
            raise AssertionError(("inadmissible sigma", sigma))

        delta_p = Fraction(19, 126) - Fraction(2, 3) * sigma + t
        bmin_p = Fraction(11, 21) - 2 * sigma
        bmax_p = Fraction(61, 84) - sigma - delta_p / 2
        pub = (
            Fraction(1, 2) + delta_p - bmax_p,
            (bmin_p + 4 * delta_p - 1) / 4,
            (6 * delta_p - bmax_p) / 6,
        )
        pub_expected = (
            3 * t / 2,
            Fraction(2, 63) - Fraction(7, 6) * sigma + t,
            Fraction(8, 189) - Fraction(5, 9) * sigma + Fraction(13, 12) * t,
        )
        if pub != pub_expected:
            raise AssertionError(("published profile", sigma, t, pub, pub_expected))
        checks += 1

        delta_l = Fraction(5, 34) - Fraction(2, 3) * sigma + t
        bmin_l = Fraction(9, 17) - sigma / 2
        bmax_l = Fraction(49, 68) - sigma - delta_l / 2
        li = (
            Fraction(1, 2) + delta_l - bmax_l,
            (bmin_l + 4 * delta_l - 1) / 4,
            (6 * delta_l - bmax_l) / 6,
        )
        li_expected = (
            3 * t / 2,
            Fraction(1, 34) - Fraction(19, 24) * sigma + t,
            Fraction(2, 51) - Fraction(5, 9) * sigma + Fraction(13, 12) * t,
        )
        if li != li_expected:
            raise AssertionError(("Li profile", sigma, t, li, li_expected))
        checks += 1

    return checks


def main() -> None:
    checks = 0

    # Exact divisor reflection, including nonsquarefree targets.
    for n in range(2, 401):
        for y in range(1, 25):
            lhs = tail_vec(n, y)
            if lhs != complement_vec(n, y):
                raise AssertionError(("complement", n, y))
            checks += 1
            if lhs != liouville_cocycle_vec(n, y):
                raise AssertionError(("cocycle", n, y))
            checks += 1
            if n > y * y:
                if lhs != balanced_split_vec(n, y):
                    raise AssertionError(("balanced", n, y))
                checks += 1

    # General CRT compatibility and affine determinant.  This includes
    # moduli sharing primes with h, not only the primitive-orbit case.
    crt_triples = ((1, 2, 3), (2, 5, 11), (6, 5, 7), (6, 5, 11), (10, 3, 7))
    for h, m1, m2 in crt_triples:
        if math.gcd(m1 * m2, h) != 1 or m1 == m2:
            raise AssertionError(("bad CRT test triple", h, m1, m2))
        for r in range(1, 31):
            for s in range(1, 31):
                if math.gcd(r, m1) != 1 or math.gcd(s, m2) != 1:
                    continue
                q, sols = crt_solutions(m1, m2, h, r, s)
                predicted = (h * (m1 - m2)) % math.gcd(r, s) == 0
                if bool(sols) != predicted:
                    raise AssertionError(("compatibility", h, m1, m2, r, s, sols))
                checks += 1
                if predicted:
                    if len(sols) != 1:
                        raise AssertionError(("CRT uniqueness", h, m1, m2, r, s, sols))
                    j0 = sols[0]
                    a1 = m1 * q // r
                    b1 = (m1 * j0 + h) // r
                    a2 = m2 * q // s
                    b2 = (m2 * j0 + h) // s
                    det = a1 * b2 - a2 * b1
                    expected = h * (m1 - m2) // math.gcd(r, s)
                    if det != expected or det == 0:
                        raise AssertionError(
                            ("determinant", h, m1, m2, r, s, det, expected)
                        )
                    checks += 1

    # The h-factor in compatibility is genuine: d=4 does not divide
    # m1-m2=-6, but it divides h(m1-m2)=-12.
    h, m1, m2 = 2, 5, 11
    _, h_factor_solutions = crt_solutions(m1, m2, h, 4, 4)
    if len(h_factor_solutions) != 1:
        raise AssertionError("compatibility requires the h factor")
    checks += 1

    # A hard-failure variant omitting the gcd denominator must fail.
    q, sols = crt_solutions(m1, m2, h, 3, 3)
    if len(sols) != 1:
        raise AssertionError("hard-failure setup")
    j0 = sols[0]
    actual = (m1 * q // 3) * ((m2 * j0 + h) // 3) - (m2 * q // 3) * ((m1 * j0 + h) // 3)
    false_formula = h * (m1 - m2)
    if actual == false_formula:
        raise AssertionError("omitting complement gcd did not fail")
    checks += 1

    ledger_checks = exponent_checks()
    checks += ledger_checks

    # Exact affine profile collar identities.
    checks += profile_checks()

    source_path = Path(__file__).resolve()
    source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
    payload = {
        "certificate": "TPC-23 dynamic cutoff and parity fibers",
        "exact_checks": checks,
        "ledger_checks": ledger_checks,
        "source_sha256": source_hash,
        "hard_failure_omitted_gcd_detected": True,
        "asymptotic_evidence": False,
        "full_residual_closure": False,
        "hardy_littlewood_asymptotic": False,
        "twin_prime_result": False,
        "general_parity_breakthrough": False,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_digest"] = hashlib.sha256(canonical).hexdigest()

    output_path = source_path.with_suffix(".json")
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
