"""Integer checks for the parity-factor Möbius capacity theorem.

The admissible sign words have all ``+1`` positions in one parity class.
All routines are integer-only; the asymptotic theorem is stated and proved
in the manuscript from standard Möbius and squarefree-density inputs.
"""

from __future__ import annotations

from itertools import product
from math import isqrt


def mobius_prefix(n: int) -> list[int]:
    """Return ``[mu(1), ..., mu(n)]`` by a linear sieve."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    mu = [0] * (n + 1)
    primes: list[int] = []
    composite = [False] * (n + 1)
    if n >= 1:
        mu[1] = 1
    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            v = i * p
            if v > n:
                break
            composite[v] = True
            if i % p == 0:
                mu[v] = 0
                break
            mu[v] = -mu[i]
    return mu[1:]


def parity_statistics(values: list[int]) -> dict[str, object]:
    """Return exact signed and squarefree counts by parity.

    Residue ``0`` is even and residue ``1`` is odd.  ``P_r`` and ``N_r`` are
    the counts of ``+1`` and ``-1`` Möbius values in that class.
    """
    total = sum(values)
    rows: dict[int, dict[str, int]] = {}
    for r in (0, 1):
        row = {"squarefree": 0, "positive": 0, "negative": 0, "mertens": 0}
        for n, value in enumerate(values, start=1):
            if n % 2 != r:
                continue
            row["mertens"] += value
            if value == 1:
                row["squarefree"] += 1
                row["positive"] += 1
            elif value == -1:
                row["squarefree"] += 1
                row["negative"] += 1
        rows[r] = row
    return {"total_mertens": total, "residues": rows}


def capacity_formula(values: list[int]) -> dict[str, object]:
    """Evaluate the exact parity-factor capacity and witnesses.

    A witness is encoded as a list of signs.  The four candidates are the two
    parity classes, with either positive or negative Möbius entries flipped
    from the all-negative baseline.
    """
    stats = parity_statistics(values)
    total = int(stats["total_mertens"])
    candidates: dict[str, int] = {}
    witnesses: dict[str, list[int]] = {}
    for r in (0, 1):
        row = stats["residues"][r]
        key = f"positive_{r}"
        candidates[key] = -total + 2 * int(row["positive"])
        witness = [-1] * len(values)
        for n, value in enumerate(values, start=1):
            if n % 2 == r and value == 1:
                witness[n - 1] = 1
        witnesses[key] = witness
        key = f"negative_{r}"
        candidates[key] = -total - 2 * int(row["negative"])
        witness = [-1] * len(values)
        for n, value in enumerate(values, start=1):
            if n % 2 == r and value == -1:
                witness[n - 1] = 1
        witnesses[key] = witness
    best_key = max(candidates, key=lambda key: abs(candidates[key]))
    return {
        "capacity": abs(candidates[best_key]),
        "best_key": best_key,
        "candidates": candidates,
        "witness": witnesses[best_key],
        "statistics": stats,
    }


def _admissible_a2(word: tuple[int, ...]) -> bool:
    """A_{\{2\}} factor rule: all plus positions use one parity class."""
    plus = [i % 2 for i, value in enumerate(word, start=1) if value == 1]
    return not plus or len(set(plus)) == 1


def finite_checks(max_n: int = 12) -> dict[str, object]:
    """Brute-force the factor constraint against the closed formula."""
    rows = []
    for n in range(1, max_n + 1):
        values = mobius_prefix(n)
        formula = capacity_formula(values)
        brute = max(
            abs(sum(value * sign for value, sign in zip(values, word)))
            for word in product((-1, 1), repeat=n)
            if _admissible_a2(word)
        )
        witness = formula["witness"]
        rows.append(
            {
                "N": n,
                "formula_capacity": formula["capacity"],
                "brute_capacity": brute,
                "witness_admissible": _admissible_a2(tuple(witness)),
                "pass": formula["capacity"] == brute
                and _admissible_a2(tuple(witness)),
            }
        )
    return {"max_n": max_n, "rows": rows, "all_pass": all(r["pass"] for r in rows)}
