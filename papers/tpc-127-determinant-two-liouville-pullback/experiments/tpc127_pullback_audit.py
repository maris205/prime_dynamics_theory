#!/usr/bin/env python3
"""Deterministic finite audit for the TPC-127 pullback."""

from __future__ import annotations

import argparse
import difflib
import json
from pathlib import Path
import sys


def mobius(n: int) -> int:
    if n <= 0:
        raise ValueError("mobius is used only on positive integers")
    value = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            value = -value
            if n % p == 0:
                return 0
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        value = -value
    return value


def liouville(n: int) -> int:
    if n <= 0:
        raise ValueError("liouville is used only on positive integers")
    value = 1
    p = 2
    while p * p <= n:
        while n % p == 0:
            n //= p
            value = -value
        p += 1
    if n > 1:
        value = -value
    return value


def audit() -> dict:
    # 5*1 - 3*1 = 2; a and s are coprime and odd.
    a, s, d, u = 3, 5, 1, 1
    # Deliberately do not use [1,N]: prefixes must be indexed by T in I.
    interval = list(range(7, 37))
    q = a * s
    n0 = s * u

    determinant_ok = s * u - a * d == 2
    frame_ok = all(
        s * (u + a * z) == a * (d + s * z) + 2 == n0 + q * z
        for z in interval
    )
    progression_ok = all(
        (n0 + q * z) % s == 0 and (n0 + q * z - 2) % a == 0
        for z in interval
    )

    identity_ok = True
    for z in interval:
        D = d + s * z
        V = u + a * z
        n = s * V
        lhs = mobius(D) * mobius(V)
        rhs = (
            (mobius(D) ** 2)
            * (mobius(V) ** 2)
            * liouville(q)
            * liouville(n - 2)
            * liouville(n)
        )
        identity_ok &= lhs == rhs

    # Gaussian-integer weights and fourth-root phases make this transport
    # check exact rather than tolerance based.
    weights = {
        z: complex((3 * z) % 11 - 5, (5 * z) % 13 - 6)
        for z in interval
    }
    original = sum(
        mobius(d + s * z)
        * mobius(u + a * z)
        * weights[z]
        * quarter_turn(-z)
        for z in interval
    )
    pulled = liouville(q) * sum(
        (mobius((n - 2) // a) ** 2)
        * (mobius(n // s) ** 2)
        * liouville(n - 2)
        * liouville(n)
        * weights[(n - n0) // q]
        * quarter_turn(-((n - n0) // q))
        for n in (n0 + q * z for z in interval)
    )
    sum_ok = original == pulled

    prefixes_original = []
    prefixes_pulled = []
    prefix_endpoints = []
    left = 0
    right = 0
    for z in interval:
        n = n0 + q * z
        left += mobius(d + s * z) * mobius(u + a * z)
        right += (
            liouville(q)
            * (mobius((n - 2) // a) ** 2)
            * (mobius(n // s) ** 2)
            * liouville(n - 2)
            * liouville(n)
        )
        prefix_endpoints.append(z)
        prefixes_original.append(left)
        prefixes_pulled.append(right)
    prefix_ok = prefixes_original == prefixes_pulled
    interval_prefix_indexing_ok = (
        prefix_endpoints == interval
        and interval[0] != 1
        and interval[-1] != len(interval)
    )

    # If D and V were both even and squarefree, D/2 and V/2 would be
    # odd and s(V/2)-a(D/2)=1.  The left side is even because a,s are odd.
    parity_obstruction_ok = all(
        (s * v_half - a * d_half) % 2 == 0
        for d_half in range(1, 40, 2)
        for v_half in range(1, 40, 2)
    )
    support_scan = list(range(0, 500))
    squarefree_support = [
        z
        for z in support_scan
        if mobius(d + s * z) != 0 and mobius(u + a * z) != 0
    ]
    squarefree_even_even_absent = parity_obstruction_ok and all(
        not (
            (d + s * z) % 2 == 0
            and (u + a * z) % 2 == 0
        )
        for z in squarefree_support
    )

    result = {
        "determinant_two": determinant_ok,
        "n_frame": frame_ok,
        "progression_congruences": progression_ok,
        "mobius_liouville_identity": identity_ok,
        "weighted_sum_transport": sum_ok,
        "all_prefixes_preserved": prefix_ok,
        "interval_prefix_indexing": interval_prefix_indexing_ok,
        "squarefree_even_even_parity_obstruction": parity_obstruction_ok,
        "squarefree_even_even_absent": squarefree_even_even_absent,
        "sample": {
            "interval_first": interval[0],
            "interval_last": interval[-1],
            "interval_length": len(interval),
            "prefix_endpoints_are_actual_interval_points": interval_prefix_indexing_ok,
            "squarefree_support_points_scanned": len(squarefree_support),
            "weighted_sum_gaussian_integer": [
                int(original.real),
                int(original.imag),
            ],
        },
        "level": {
            "finite_algebra": "L0",
            "actual_branch_attachment": "L1",
            "growing_cancellation": "not proved",
        },
    }
    result["all_checks_passed"] = all(
        result[key]
        for key in (
            "determinant_two",
            "n_frame",
            "progression_congruences",
            "mobius_liouville_identity",
            "weighted_sum_transport",
            "all_prefixes_preserved",
            "interval_prefix_indexing",
            "squarefree_even_even_parity_obstruction",
            "squarefree_even_even_absent",
        )
    )
    return result


def quarter_turn(power: int) -> complex:
    """Return i**power exactly as a Gaussian integer."""
    return (1 + 0j, 0 + 1j, -1 + 0j, 0 - 1j)[power % 4]


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
