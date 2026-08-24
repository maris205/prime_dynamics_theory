#!/usr/bin/env python3
"""Independent exact checker for the TPC-231 local law and finite scan."""

from __future__ import annotations

import json
from bisect import bisect_left, bisect_right
from fractions import Fraction
from hashlib import sha256
from math import gcd
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


class IndependentFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise IndependentFailure(message)


def primes_to(limit: int) -> tuple[tuple[bool, ...], tuple[int, ...], tuple[int, ...]]:
    flags = [True] * (limit + 1)
    flags[0] = flags[1] = False
    p = 2
    while p * p <= limit:
        if flags[p]:
            multiple = p * p
            while multiple <= limit:
                flags[multiple] = False
                multiple += p
        p += 1
    primes = tuple(i for i, value in enumerate(flags) if value)
    prefix = [0]
    for value in flags:
        prefix.append(prefix[-1] + (1 if value else 0))
    return tuple(flags), primes, tuple(prefix)


def form_pair(Q: int, k: int) -> tuple[int, int]:
    t, a = divmod(Q, 3)
    require(a in (1, 2), "primitive residue")
    return 3 * k + a, 16 * t + 3 * a - 7 * k


def direct_roots(Q: int, ell: int) -> int:
    return len({k for k in range(ell) if (form_pair(Q, k)[0] * form_pair(Q, k)[1]) % ell == 0})


def edge_count_by_parameter(Q: int, flags: tuple[bool, ...]) -> int:
    if gcd(Q, 21) != 1:
        return 0
    _, a = divmod(Q, 3)
    lower = ((10 * Q - 7 * a) // 21) + 1
    upper = (8 * Q - 1 - 5 * a) // 15
    count = 0
    for k in range(lower, upper + 1):
        p, r = form_pair(Q, k)
        if Q < p < r < 2 * Q and flags[p] and flags[r]:
            count += 1
    return count


def ftext(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def independent_scan(Q_max: int) -> dict[str, object]:
    flags, _, prefix = primes_to(2 * Q_max)
    windows = ((8, 31), (32, 127), (128, 511), (512, 2047), (2048, 8191), (8192, Q_max))
    lines = []
    summaries = []
    total_edges = total_rows = edge_scales = 0
    for lower, upper in windows:
        w_edges = w_rows = w_scales = 0
        max_ratio = Fraction(-1)
        max_Q = None
        for Q in range(lower, upper + 1):
            E = edge_count_by_parameter(Q, flags)
            P = prefix[2 * Q] - prefix[Q + 1]
            require(P > 0, "prime shell")
            ratio = Fraction(E, P)
            if ratio > max_ratio:
                max_ratio, max_Q = ratio, Q
            if E:
                w_scales += 1
                edge_scales += 1
            w_edges += E
            w_rows += P
            total_edges += E
            total_rows += P
            lines.append(f"{Q}|{P}|{E}|{ftext(ratio)}")
        summaries.append(
            {
                "Q_min": lower,
                "Q_max": upper,
                "scales": upper - lower + 1,
                "edge_bearing_scales": w_scales,
                "total_edges": w_edges,
                "total_prime_rows": w_rows,
                "aggregate_edge_to_row_ratio": ftext(Fraction(w_edges, w_rows)),
                "maximum_edge_to_row_ratio": ftext(max_ratio),
                "first_maximum_Q": max_Q,
            }
        )
    return {
        "Q_min": 8,
        "Q_max": Q_max,
        "scales_checked": Q_max - 7,
        "edge_bearing_scales": edge_scales,
        "total_edges": total_edges,
        "total_prime_rows": total_rows,
        "aggregate_edge_to_row_ratio": ftext(Fraction(total_edges, total_rows)),
        "windows": summaries,
        "scan_sha256": sha256("\n".join(lines).encode("utf-8")).hexdigest(),
    }


def no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key")
        output[key] = value
    return output


def main() -> int:
    data = json.loads((PROJECT / "results" / "certificate.json").read_text(), object_pairs_hook=no_duplicate_pairs)
    require(data["schema"] == "tpc231-finite-resonance-sieve-obstruction-v1", "schema")
    require(data["claim_level"] == "PROVED_ARITHMETIC_OBSTRUCTION_L1", "claim")
    for Q in (10, 11, 13, 17, 19, 23, 25, 29, 31, 32, 37, 41, 101, 125):
        if gcd(Q, 21) == 1:
            for ell in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31):
                expected = 1 if ell in (2, 3, 7) or Q % ell == 0 else 2
                require(direct_roots(Q, ell) == expected, "local root law")
    require(data["finite_scan"] == independent_scan(32768), "independent finite scan")
    require(data["q25_edges"] == [[37, 47]], "Q25 edge")
    firewall = data["firewall"]
    require(firewall["arithmetic_advance"] == "NO", "arithmetic promotion")
    require(firewall["strict_1_over_400"] == "UNPAID_GLOBAL_STOP_SCOPED_FOR_FIRST_RESONANCE", "firewall")
    print("TPC231_INDEPENDENT_CHECK=PASS")
    print("local_root_law=PASS")
    print("finite_scan=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
