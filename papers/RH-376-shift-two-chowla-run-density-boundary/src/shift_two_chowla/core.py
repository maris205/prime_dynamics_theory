"""Exact integer audit for the RH-376 two-site Möbius identities.

The finite computations reproduce algebraic identities and frozen rows.  They
are not used as evidence for any asymptotic correlation statement.
"""

from __future__ import annotations

from functools import lru_cache
import importlib.util
from pathlib import Path
from types import ModuleType


ENDPOINT = 1 << 20
ROW_LIMITS = (1 << 10, 1 << 16, 1 << 20)
RH371_ALIGNMENT_LIMIT = 1 << 10


def mobius_prefix(limit: int) -> list[int]:
    """Return ``mu(0),...,mu(limit)`` using an exact linear sieve."""

    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive integer")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            composite[product] = True
            if value % prime == 0:
                mu[product] = 0
                break
            mu[product] = -mu[value]
    return mu


def pointwise_terms(left: int, right: int) -> dict[str, int]:
    """Return the six pointwise terms for one shift-two pair."""

    if left not in (-1, 0, 1) or right not in (-1, 0, 1):
        raise ValueError("Möbius values must lie in {-1,0,1}")
    return {
        "C_plus": int(left == 1 and right == 1),
        "C_minus": int(left == -1 and right == -1),
        "Q2": left * left * right * right,
        "U2": left * right * right,
        "V2": left * left * right,
        "D2": left * right,
    }


def _empty_totals() -> dict[str, int]:
    return {key: 0 for key in ("C_plus", "C_minus", "Q2", "U2", "V2", "D2")}


def two_site_totals(mu: list[int], limit: int) -> dict[str, int]:
    """Sum over the common endpoint ``1 <= n <= limit-2``."""

    if type(limit) is not int or limit < 1 or limit >= len(mu):
        raise ValueError("limit must index the supplied Möbius prefix")
    totals = _empty_totals()
    for start in range(1, max(1, limit - 1)):
        row = pointwise_terms(mu[start], mu[start + 2])
        for key, value in row.items():
            totals[key] += value
    return totals


def _identity_pass(row: dict[str, int]) -> bool:
    return (
        4 * row["C_plus"]
        == row["Q2"] + row["U2"] + row["V2"] + row["D2"]
        and 4 * row["C_minus"]
        == row["Q2"] - row["U2"] - row["V2"] + row["D2"]
    )


def _load_rh371_core() -> ModuleType:
    root = Path(__file__).resolve().parents[4]
    path = (
        root
        / "papers"
        / "RH-371-eight-run-distance-two-capacity-obstruction"
        / "src"
        / "distance_capacity"
        / "core.py"
    )
    spec = importlib.util.spec_from_file_location("rh371_locked_core", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load frozen RH-371 core: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def verify_certificate() -> dict[str, object]:
    """Run all exact finite checks declared by RH-376."""

    mu = mobius_prefix(ENDPOINT)
    totals = _empty_totals()
    pointwise_pass = True
    cumulative_pass = True
    even_zero_pass = True
    pointwise_count = 0
    even_start_count = 0
    rows: dict[int, dict[str, int]] = {}

    # Prefix N acquires the single new start n=N-2.  This convention checks
    # every common endpoint 1 <= n <= N-2 without an off-by-one conversion.
    for limit in range(1, ENDPOINT + 1):
        if limit >= 3:
            start = limit - 2
            row = pointwise_terms(mu[start], mu[start + 2])
            pointwise_count += 1
            pointwise_pass = pointwise_pass and _identity_pass(row)
            if start % 2 == 0:
                even_start_count += 1
                even_zero_pass = even_zero_pass and all(value == 0 for value in row.values())
            for key, value in row.items():
                totals[key] += value
        cumulative_pass = cumulative_pass and _identity_pass(totals)
        if limit in ROW_LIMITS:
            rows[limit] = dict(totals)

    expected_rows = {
        1024: {"C_plus": 66, "C_minus": 82, "Q2": 330, "U2": -18, "V2": -14, "D2": -34},
        65536: {"C_plus": 5293, "C_minus": 5301, "Q2": 21155, "U2": -51, "V2": 35, "D2": 33},
        1048576: {"C_plus": 84630, "C_minus": 84346, "Q2": 338334, "U2": 130, "V2": 438, "D2": -382},
    }
    frozen_rows_pass = rows == expected_rows

    rh371 = _load_rh371_core()
    alignment_pass = True
    for limit in range(1, RH371_ALIGNMENT_LIMIT + 1):
        current = two_site_totals(mu, limit)
        plus = rh371.run_counts(mu, 1, limit, max_length=2)[1]
        minus = rh371.run_counts(mu, -1, limit, max_length=2)[1]
        if current["C_plus"] != plus or current["C_minus"] != minus:
            alignment_pass = False
            break

    all_pass = all((
        pointwise_pass,
        cumulative_pass,
        even_zero_pass,
        frozen_rows_pass,
        alignment_pass,
    ))
    return {
        "label": "finite_exact_reproduction_only_not_asymptotic_evidence",
        "endpoint": ENDPOINT,
        "common_endpoint": "1<=n<=N-2",
        "pointwise_identity_count": pointwise_count,
        "pointwise_identities_pass": pointwise_pass,
        "cumulative_prefix_count": ENDPOINT,
        "cumulative_identities_pass": cumulative_pass,
        "even_start_count": even_start_count,
        "even_start_zero_pass": even_zero_pass,
        "rh371_alignment_prefix_count": RH371_ALIGNMENT_LIMIT,
        "rh371_alignment_sign_cells": 2 * RH371_ALIGNMENT_LIMIT,
        "rh371_alignment_pass": alignment_pass,
        "frozen_rows": {str(limit): rows[limit] for limit in ROW_LIMITS},
        "frozen_rows_pass": frozen_rows_pass,
        "all_pass": all_pass,
    }
