"""Matching and shell diagnostics for an expanded resolved spectrum."""

from __future__ import annotations

import numpy as np
from scipy.optimize import linear_sum_assignment


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"], dtype=float) + 1j * np.asarray(payload["imag"], dtype=float)


def complex_payload(values_array: np.ndarray) -> dict[str, list[float]]:
    roots = np.asarray(values_array, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in roots],
        "imag": [float(value.imag) for value in roots],
    }


def match_reference_roots(reference: np.ndarray, expanded: np.ndarray) -> dict[str, object]:
    """Match every reference root to a distinct expanded root."""

    old = np.asarray(reference, dtype=complex).reshape(-1)
    new = np.asarray(expanded, dtype=complex).reshape(-1)
    if old.size == 0 or new.size < old.size:
        raise ValueError("expanded spectrum must contain the nonempty reference spectrum")
    cost = np.abs(old[:, None] - new[None, :])
    rows, columns = linear_sum_assignment(cost)
    if rows.size != old.size:
        raise RuntimeError("root matching did not cover the reference spectrum")
    matched_error = cost[rows, columns]
    used = set(int(index) for index in columns)
    unmatched = np.asarray([new[index] for index in range(new.size) if index not in used])
    return {
        "maximum_matching_error": float(np.max(matched_error)),
        "mean_matching_error": float(np.mean(matched_error)),
        "matched_columns": [int(index) for index in columns],
        "unmatched": unmatched,
    }


def shell_count_and_rank(shells: list[np.ndarray]) -> tuple[int, int]:
    return len(shells), int(sum(np.asarray(shell).size for shell in shells))
