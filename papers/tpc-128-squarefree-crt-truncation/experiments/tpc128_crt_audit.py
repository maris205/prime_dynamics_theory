#!/usr/bin/env python3
"""Finite audit of the TPC-128 CRT and truncation identities."""

from __future__ import annotations

import argparse
import difflib
from fractions import Fraction
import json
import math
from pathlib import Path
import sys


def mobius(n: int) -> int:
    value = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            value = -value
            if n % p == 0:
                return 0
        p += 1
    if n > 1:
        value = -value
    return value


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def q_r(n: int, cutoff: int) -> int:
    return sum(
        mobius(k)
        for k in range(1, cutoff + 1)
        if n % (k * k) == 0
    )


def tau(n: int) -> int:
    return len(divisors(n))


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def ceil_sqrt(n: int) -> int:
    root = math.isqrt(n)
    return root if root * root == n else root + 1


def positive_saving(value: Fraction) -> Fraction | None:
    """Only a strictly positive exponent may be advertised as a saving."""
    return value if value > 0 else None


def audit() -> dict:
    a, s, d, u = 3, 5, 1, 1
    interval = list(range(0, 120))
    cutoff = 7
    q = a * s

    compatibility_ok = True
    crt_expansion_ok = True
    n_congruence_ok = True

    compatible_pairs: list[tuple[int, int, int]] = []
    for k in range(1, cutoff + 1):
        for ell in range(1, cutoff + 1):
            allowed = (
                math.gcd(k, s) == 1
                and math.gcd(ell, a) == 1
                and math.gcd(k, ell) == 1
            )
            residues = [
                z
                for z in range(k * k * ell * ell)
                if (d + s * z) % (k * k) == 0
                and (u + a * z) % (ell * ell) == 0
            ]
            compatibility_ok &= bool(residues) == allowed
            if allowed:
                compatibility_ok &= len(residues) == 1
                compatible_pairs.append((k, ell, residues[0]))
                n = s * (u + a * residues[0])
                n_congruence_ok &= (
                    n % (s * ell * ell) == 0
                    and (n - 2) % (a * k * k) == 0
                )

    for z in interval:
        lhs = q_r(d + s * z, cutoff) * q_r(u + a * z, cutoff)
        rhs = sum(
            mobius(k) * mobius(ell)
            for k, ell, residue in compatible_pairs
            if z % (k * k * ell * ell) == residue
        )
        crt_expansion_ok &= lhs == rhs

    y = max(max(d + s * z, u + a * z) for z in interval)
    tau_star = max(tau(n) for n in range(1, y + 1))
    actual_tail = sum(
        abs(
            (mobius(d + s * z) ** 2) * (mobius(u + a * z) ** 2)
            - q_r(d + s * z, cutoff) * q_r(u + a * z, cutoff)
        )
        for z in interval
    )
    # An integer majorant for (1+tau_*(Y))(N/R+sqrt(Y)+1).
    tail_bound = (1 + tau_star) * (
        ceil_div(len(interval), cutoff) + ceil_sqrt(y) + 1
    )
    tail_bound_ok = actual_tail <= tail_bound

    # Once R >= sqrt(Y), every possible square divisor is included and
    # the truncation is identically exact on the full sampled block.
    exact_cutoff = ceil_sqrt(y)
    exact_tail = sum(
        abs(
            (mobius(d + s * z) ** 2) * (mobius(u + a * z) ** 2)
            - q_r(d + s * z, exact_cutoff)
            * q_r(u + a * z, exact_cutoff)
        )
        for z in interval
    )
    exact_tail_above_sqrt_y = exact_tail == 0
    effective_cutoff_cap = all(
        q_r(value, exact_cutoff + 5) == q_r(value, exact_cutoff)
        for z in interval
        for value in (d + s * z, u + a * z)
    )

    census = sum(
        sum(
            1
            for z in interval
            if z % (k * k * ell * ell) == residue
        )
        for k, ell, residue in compatible_pairs
    )
    # zeta(2)^2 < 3, so this is an exact integer majorant for the
    # displayed N*zeta(2)^2+R^2 census bound.
    census_bound = 3 * len(interval) + cutoff**2
    census_ok = census <= census_bound

    # Guard the word "saving": the elementary tail regime must be
    # strictly positive, and the correlation exponent must beat the
    # census loss.  The exact-tail regime is recorded separately.
    nu = Fraction(1, 1)
    rho = Fraction(1, 5)
    upsilon_positive = Fraction(1, 1)
    upsilon_nonpositive = Fraction(3, 1)
    tail_positive = min(rho, nu - upsilon_positive / 2)
    tail_nonpositive = min(rho, nu - upsilon_nonpositive / 2)
    eta_corr = Fraction(3, 20)
    census_loss = Fraction(1, 10)
    corr_net = eta_corr - census_loss
    positive_saving_guard = (
        positive_saving(tail_positive) == Fraction(1, 5)
        and positive_saving(tail_nonpositive) is None
        and positive_saving(corr_net) == Fraction(1, 20)
        and exact_tail_above_sqrt_y
    )

    result = {
        "compatibility_iff": compatibility_ok,
        "crt_expansion": crt_expansion_ok,
        "n_frame_congruences": n_congruence_ok,
        "tail_bound": tail_bound_ok,
        "exact_tail_at_or_above_sqrt_y": exact_tail_above_sqrt_y,
        "effective_cutoff_capped_by_sqrt_y": effective_cutoff_cap,
        "component_census": census_ok,
        "positive_saving_guard": positive_saving_guard,
        "sample": {
            "a": a,
            "s": s,
            "determinant": s * u - a * d,
            "cutoff": cutoff,
            "max_affine_value": y,
            "actual_tail": actual_tail,
            "tail_upper_bound_integer_majorant": tail_bound,
            "exact_cutoff_ceil_sqrt_y": exact_cutoff,
            "exact_regime_tail": exact_tail,
            "census": census,
            "census_upper_bound_integer_majorant": census_bound,
            "max_n_modulus": q * cutoff**4,
            "saving_guard": {
                "positive_tail_candidate": str(tail_positive),
                "nonpositive_tail_candidate_rejected": str(
                    tail_nonpositive
                ),
                "correlation_minus_census_loss": str(corr_net),
                "requires_eta_corr_gt_census_loss": True,
                "exact_tail_regime": "zero",
            },
        },
        "level": {
            "finite_and_tail_results": "L0",
            "actual_attachment": "L1",
            "signed_correlation": "not proved",
        },
    }
    result["all_checks_passed"] = all(
        result[key]
        for key in (
            "compatibility_iff",
            "crt_expansion",
            "n_frame_congruences",
            "tail_bound",
            "exact_tail_at_or_above_sqrt_y",
            "effective_cutoff_capped_by_sqrt_y",
            "component_census",
            "positive_saving_guard",
        )
    )
    return result


def serialized(output: dict) -> str:
    return json.dumps(output, indent=2, sort_keys=True) + "\n"


def check_or_write(path: Path, rendered: str, check: bool) -> bool:
    if not check:
        path.write_text(rendered, encoding="utf-8")
        return True
    if not path.exists():
        print(f"{path}: missing audit artifact", file=sys.stderr)
        return False
    current = path.read_text(encoding="utf-8")
    if current == rendered:
        return True
    print(f"{path}: stale audit artifact", file=sys.stderr)
    sys.stderr.writelines(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            rendered.splitlines(keepends=True),
            fromfile=str(path),
            tofile="generated",
        )
    )
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed JSON without rewriting it",
    )
    args = parser.parse_args()
    output = audit()
    path = Path(__file__).with_suffix(".json")
    rendered = serialized(output)
    artifact_ok = check_or_write(path, rendered, args.check)
    print(rendered, end="")
    if not output["all_checks_passed"] or not artifact_ok:
        raise SystemExit(1)
