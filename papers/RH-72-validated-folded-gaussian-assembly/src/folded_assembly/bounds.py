"""Deterministic bounds for stochastic repair and Haar compression."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

import numpy as np


def full_sparse_row_l1(omitted_mass: float, full_mass: float) -> float:
    """Exact L1 distance between full and support-renormalized rows."""

    omitted = float(omitted_mass)
    total = float(full_mass)
    if omitted < 0.0 or total <= 0.0 or omitted > total:
        raise ValueError("invalid full/sparse masses")
    return 2.0 * omitted / total


def induced_two_norm_bound(one_norm: float, infinity_norm: float) -> float:
    """Return sqrt(||A||_1 ||A||_infinity)."""

    one = float(one_norm)
    infinity = float(infinity_norm)
    if one < 0.0 or infinity < 0.0:
        raise ValueError("induced norm bounds must be nonnegative")
    return math.sqrt(one * infinity)


def exact_stochastic_repair(
    row: np.ndarray,
) -> tuple[int, Fraction, tuple[Fraction, ...]]:
    """Repair one nonnegative binary64 row as exact dyadic rationals.

    All entries except the largest are left unchanged. The largest entry is
    replaced by one minus the exact dyadic sum of the others.
    """

    values = np.asarray(row, dtype=np.float64)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("row must be a nonempty vector")
    if np.any(values < 0.0) or not np.all(np.isfinite(values)):
        raise ValueError("row must be finite and nonnegative")
    pivot = int(np.argmax(values))
    fractions = [Fraction.from_float(float(value)) for value in values]
    replacement = Fraction(1, 1) - sum(
        fraction
        for index, fraction in enumerate(fractions)
        if index != pivot
    )
    if replacement <= 0:
        raise ValueError("stochastic repair destroyed positivity")
    correction = replacement - fractions[pivot]
    fractions[pivot] = replacement
    if sum(fractions, Fraction(0, 1)) != 1:
        raise ArithmeticError("exact stochastic repair failed")
    return pivot, correction, tuple(fractions)


@dataclass(frozen=True)
class CompressedAssemblyBound:
    matrix_two_norm_defect: float
    embedding_two_norm_defect: float
    frozen_matrix_two_norm_upper: float
    frozen_embedding_two_norm_upper: float
    compressed_two_norm_defect_upper: float


def compressed_assembly_defect(
    matrix_two_norm_defect: float,
    embedding_two_norm_defect: float,
    frozen_matrix_two_norm_upper: float,
    frozen_embedding_two_norm_upper: float,
) -> CompressedAssemblyBound:
    """Bound E* P D - E0* F D0 for exact/frozen Haar isometries.

    The exact left and right embeddings have norm one. Both frozen
    embeddings have the same supplied norm upper.
    """

    matrix_defect = float(matrix_two_norm_defect)
    embedding_defect = float(embedding_two_norm_defect)
    matrix_upper = float(frozen_matrix_two_norm_upper)
    embedding_upper = float(frozen_embedding_two_norm_upper)
    if min(matrix_defect, embedding_defect, matrix_upper, embedding_upper) < 0:
        raise ValueError("assembly bounds must be nonnegative")
    total = (
        matrix_defect
        + embedding_defect * matrix_upper
        + embedding_upper * matrix_upper * embedding_defect
    )
    return CompressedAssemblyBound(
        matrix_two_norm_defect=matrix_defect,
        embedding_two_norm_defect=embedding_defect,
        frozen_matrix_two_norm_upper=matrix_upper,
        frozen_embedding_two_norm_upper=embedding_upper,
        compressed_two_norm_defect_upper=total,
    )
