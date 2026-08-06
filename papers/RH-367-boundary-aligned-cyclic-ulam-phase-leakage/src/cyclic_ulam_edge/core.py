"""Exact finite ledgers for RH-367.

The source theorem is finite-dimensional: an exactly aligned cell-overlap
Ulam matrix inherits the two-band sign mode.  This module deliberately keeps
that statement separate from any continuum spectral claim.  The phase scan
is read from the frozen external source and is a diagnostic, not an
asymptotic theorem.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable


U_C = 1.5436890126920764
R = U_C - 1.0
INTERVAL_LEFT = -R
INTERVAL_RIGHT = 1.0


def polynomial_residual(u: float = U_C) -> float:
    """Residual of u^3-2u^2+2u-2=0 at the frozen decimal root."""

    return u**3 - 2.0 * u**2 + 2.0 * u - 2.0


def map_value(x: float, u: float = U_C) -> float:
    return 1.0 - u * x * x


def geometry_residuals(u: float = U_C) -> dict[str, float]:
    r = u - 1.0
    return {
        "parameter_polynomial": polynomial_residual(u),
        "critical_0_to_1": map_value(0.0, u) - 1.0,
        "critical_1_to_minus_r": map_value(1.0, u) + r,
        "critical_minus_r_to_r": map_value(-r, u) - r,
        "critical_r_fixed": map_value(r, u) - r,
        "lrl_boundary_f2_zero": map_value(map_value(0.3555443332295785, u), u),
    }


def aligned_block(n0: int, n1: int) -> list[list[float]]:
    """A row-stochastic anti-diagonal block witness.

    Each source cell in band zero sends all mass uniformly to band one, and
    conversely.  It is an exact finite model of the only property needed by
    the block theorem; no continuum discretization is inferred from it.
    """

    if n0 < 1 or n1 < 1:
        raise ValueError("both band sizes must be positive")
    rows: list[list[float]] = []
    for _ in range(n0):
        rows.append([0.0] * n0 + [1.0 / n1] * n1)
    for _ in range(n1):
        rows.append([1.0 / n0] * n0 + [0.0] * n1)
    return rows


def sign_vector(n0: int, n1: int) -> tuple[float, ...]:
    if n0 < 1 or n1 < 1:
        raise ValueError("both band sizes must be positive")
    return tuple([1.0] * n0 + [-1.0] * n1)


def matvec(matrix: list[list[float]], vector: Iterable[float]) -> tuple[float, ...]:
    values = tuple(vector)
    if any(len(row) != len(values) for row in matrix):
        raise ValueError("matrix/vector dimensions do not match")
    return tuple(sum(a * b for a, b in zip(row, values)) for row in matrix)


def sign_mode_residual(n0: int, n1: int) -> float:
    matrix = aligned_block(n0, n1)
    signs = sign_vector(n0, n1)
    image = matvec(matrix, signs)
    return max(abs(value + sign) for value, sign in zip(image, signs))


def crossing_projection(theta: float) -> float:
    """Squared-sign projection defect for a crossing cell fraction theta."""

    if not 0.0 <= theta <= 1.0:
        raise ValueError("theta must lie in [0,1]")
    return 1.0 - (2.0 * theta - 1.0) ** 2


def local_defect(width: float, theta: float) -> float:
    """Lebesgue-weighted local defect 4 h theta(1-theta)."""

    if width < 0.0:
        raise ValueError("width must be nonnegative")
    return width * crossing_projection(theta)


def aligned_projection_mass() -> float:
    """The exact projected same-band mass for an aligned partition."""

    return 0.0


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def phase_summary(payload: dict[str, object]) -> dict[str, object]:
    rows = payload["rows"]
    assert isinstance(rows, list)
    aligned = [row for row in rows if row.get("band_aligned_phase")]
    crossing = [row for row in rows if not row.get("band_aligned_phase")]
    return {
        "cells": payload["cells"],
        "phase_count": payload["phase_count"],
        "row_count": len(rows),
        "aligned_rows": len(aligned),
        "crossing_rows": len(crossing),
        "aligned_projected_mass_max": max(
            (float(row["projected_same_band_mass"]) for row in aligned),
            default=0.0,
        ),
        "crossing_projected_mass_min": min(
            (float(row["projected_same_band_mass"]) for row in crossing),
            default=0.0,
        ),
        "crossing_projected_mass_max": max(
            (float(row["projected_same_band_mass"]) for row in crossing),
            default=0.0,
        ),
        "crossing_distance_to_minus_one_max": max(
            (float(row["distance_to_minus_one"]) for row in crossing),
            default=0.0,
        ),
        "max_row_sum_error": max(
            (float(row["row_sum_error"]) for row in rows), default=0.0
        ),
        "max_stationary_l1_residual": max(
            (float(row["stationary_l1_residual"]) for row in rows), default=0.0
        ),
    }


def finite_checks() -> dict[str, object]:
    matrix = aligned_block(3, 5)
    signs = sign_vector(3, 5)
    image = matvec(matrix, signs)
    theta_rows = [
        {"theta": theta, "identity": crossing_projection(theta),
         "local_defect": local_defect(0.25, theta)}
        for theta in (0.0, 0.25, 0.5, 0.75, 1.0)
    ]
    return {
        "geometry_residuals": geometry_residuals(),
        "geometry_max_abs_residual": max(abs(x) for x in geometry_residuals().values()),
        "aligned_block_shape": [len(matrix), len(matrix[0])],
        "aligned_row_sums": [sum(row) for row in matrix],
        "sign_mode_image": list(image),
        "sign_mode_residual": sign_mode_residual(3, 5),
        "aligned_projected_same_band_mass": aligned_projection_mass(),
        "crossing_identity_rows": theta_rows,
        "crossing_identity_pass": all(
            abs(row["identity"] - 4.0 * row["theta"] * (1.0 - row["theta"])) < 1.0e-15
            for row in theta_rows
        ),
    }
