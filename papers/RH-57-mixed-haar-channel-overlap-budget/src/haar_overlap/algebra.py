"""Invariant-block algebra for directional Hardy energies.

The operator passed to the Gramian routines is already divided by the Hardy
radius.  Thus stability means ``spectral_radius(operator) < 1``.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import numpy as np
from scipy.linalg import eig


def _square_matrix(value: np.ndarray, name: str) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be square")
    return result


def _source_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[:, None]
    if result.ndim != 2 or result.shape[0] != dimension:
        raise ValueError("source has incompatible shape")
    return result


def _observation_matrix(value: np.ndarray, dimension: int) -> np.ndarray:
    result = np.asarray(value, dtype=np.complex128)
    if result.ndim == 1:
        result = result[None, :]
    if result.ndim != 2 or result.shape[1] != dimension:
        raise ValueError("observation has incompatible shape")
    return result


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


@dataclass(frozen=True)
class RadialRieszPartition:
    """Binary64 grouped spectral projectors and residual diagnostics."""

    eigenvalues: np.ndarray
    physical_moduli: np.ndarray
    cuts: tuple[float, ...]
    names: tuple[str, ...]
    counts: tuple[int, ...]
    projectors: tuple[np.ndarray, ...]
    projector_norms: tuple[float, ...]
    overlap_condition_numbers: tuple[float | None, ...]
    idempotence_defects: tuple[float, ...]
    commutator_defects: tuple[float, ...]
    partition_defect: float
    pairwise_product_defect: float
    minimum_boundary_gap: float


def radial_riesz_partition(
    operator: np.ndarray,
    cuts: Sequence[float],
    *,
    physical_scale: float = 1.0,
    names: Sequence[str] | None = None,
) -> RadialRieszPartition:
    r"""Construct grouped Riesz projectors for fixed radial annuli.

    Noncentral groups are formed from paired left/right invariant subspaces.
    The central projector is the complement of their sum, so tiny clustered
    eigenvalues are never diagonalized one by one in the final projector.
    This is still a binary64 eigensolver diagnostic, not an interval contour
    construction.
    """

    a = _square_matrix(operator, "operator")
    boundaries = tuple(float(value) for value in cuts)
    if any(not math.isfinite(value) or value <= 0.0 for value in boundaries):
        raise ValueError("cuts must be finite and positive")
    if any(right <= left for left, right in zip(boundaries, boundaries[1:])):
        raise ValueError("cuts must be strictly increasing")
    scale = float(physical_scale)
    if not math.isfinite(scale) or scale <= 0.0:
        raise ValueError("physical_scale must be finite and positive")

    group_count = len(boundaries) + 1
    if names is None:
        labels = ("central",) + tuple(
            f"annulus_{index}" for index in range(1, group_count - 1)
        ) + (("edge",) if group_count > 1 else ())
    else:
        labels = tuple(str(value) for value in names)
        if len(labels) != group_count:
            raise ValueError("names must have len(cuts)+1 entries")

    values, left, right = eig(a, left=True, right=True, check_finite=False)
    moduli = np.abs(values) * scale
    assignments = np.digitize(moduli, boundaries, right=True)
    identity = np.eye(a.shape[0], dtype=np.complex128)

    outer: dict[int, tuple[np.ndarray, float]] = {}
    for group in range(1, group_count):
        indices = np.flatnonzero(assignments == group)
        if not indices.size:
            continue
        right_block = right[:, indices]
        left_block = left[:, indices]
        overlap = left_block.conjugate().T @ right_block
        condition = float(np.linalg.cond(overlap))
        projector = right_block @ np.linalg.solve(
            overlap, left_block.conjugate().T
        )
        outer[group] = (projector, condition)

    central = identity.copy()
    for projector, _ in outer.values():
        central -= projector

    active_names: list[str] = []
    active_counts: list[int] = []
    projectors: list[np.ndarray] = []
    conditions: list[float | None] = []
    central_count = int(np.count_nonzero(assignments == 0))
    if central_count:
        active_names.append(labels[0])
        active_counts.append(central_count)
        projectors.append(central)
        conditions.append(None)
    for group in range(1, group_count):
        if group not in outer:
            continue
        projector, condition = outer[group]
        active_names.append(labels[group])
        active_counts.append(int(np.count_nonzero(assignments == group)))
        projectors.append(projector)
        conditions.append(condition)

    scale_a = max(1.0, float(np.linalg.norm(a, 2)))
    projector_norms = tuple(float(np.linalg.norm(p, 2)) for p in projectors)
    idempotence = tuple(float(np.linalg.norm(p @ p - p, 2)) for p in projectors)
    commutators = tuple(
        float(np.linalg.norm(a @ p - p @ a, 2)) / scale_a for p in projectors
    )
    partition = float(np.linalg.norm(sum(projectors, start=np.zeros_like(a)) - identity, 2))
    pairwise = 0.0
    for left_index, left_projector in enumerate(projectors):
        for right_index, right_projector in enumerate(projectors):
            if left_index == right_index:
                continue
            pairwise = max(
                pairwise,
                float(np.linalg.norm(left_projector @ right_projector, 2)),
            )
    boundary_gap = min(
        (float(np.min(np.abs(moduli - boundary))) for boundary in boundaries),
        default=math.inf,
    )
    return RadialRieszPartition(
        eigenvalues=values,
        physical_moduli=moduli,
        cuts=boundaries,
        names=tuple(active_names),
        counts=tuple(active_counts),
        projectors=tuple(projectors),
        projector_norms=projector_norms,
        overlap_condition_numbers=tuple(conditions),
        idempotence_defects=idempotence,
        commutator_defects=commutators,
        partition_defect=partition,
        pairwise_product_defect=pairwise,
        minimum_boundary_gap=boundary_gap,
    )


def block_gram_from_gramian(
    gramian: np.ndarray,
    observation: np.ndarray,
    projectors: Sequence[np.ndarray],
) -> np.ndarray:
    r"""Return the Riesz-block response Gram matrix.

    If ``G=sum_m A^m X X^* (A^*)^m`` and the projectors commute with ``A``,
    then entry ``(j,k)`` is

    ``tr(Y P_j G P_k^* Y^*)``.

    It is the time-domain inner product of the two complete block responses.
    """

    g = _square_matrix(gramian, "gramian")
    y = _observation_matrix(observation, g.shape[0])
    blocks = tuple(_square_matrix(value, "projector") for value in projectors)
    if any(value.shape != g.shape for value in blocks):
        raise ValueError("projector has incompatible shape")
    images = tuple(y @ value for value in blocks)
    result = np.empty((len(blocks), len(blocks)), dtype=np.complex128)
    for row, left_image in enumerate(images):
        for column, right_image in enumerate(images):
            result[row, column] = np.trace(
                left_image @ g @ right_image.conjugate().T
            )
    return _hermitian(result)


def hardy_cauchy_gram(
    eigenvalues: Sequence[complex],
    channel_overlaps: Sequence[np.ndarray | complex],
    radius: float,
) -> np.ndarray:
    r"""Return the exact simple-mode Hardy Gram matrix.

    For ``N=sum_j mu_j P_j`` and ``Z_j=Y P_j X``, the convention used here is

    ``K_jk = tr(Z_j Z_k^*) / (1-mu_j conjugate(mu_k)/r^2)``.
    """

    values = np.asarray(tuple(eigenvalues), dtype=np.complex128)
    overlaps = tuple(np.asarray(value, dtype=np.complex128) for value in channel_overlaps)
    if len(values) != len(overlaps):
        raise ValueError("eigenvalues and overlaps must have equal length")
    hardy_radius = float(radius)
    if not math.isfinite(hardy_radius) or hardy_radius <= 0.0:
        raise ValueError("radius must be finite and positive")
    if np.max(np.abs(values), initial=0.0) >= hardy_radius:
        raise ValueError("all modal radii must be below the Hardy radius")
    shapes = {value.shape for value in overlaps}
    if len(shapes) > 1:
        raise ValueError("all channel overlaps must have the same shape")
    result = np.empty((len(values), len(values)), dtype=np.complex128)
    for row, (left_value, left_overlap) in enumerate(zip(values, overlaps)):
        for column, (right_value, right_overlap) in enumerate(zip(values, overlaps)):
            spatial = np.vdot(right_overlap, left_overlap)
            result[row, column] = spatial / (
                1.0 - left_value * np.conjugate(right_value) / hardy_radius**2
            )
    return _hermitian(result)


@dataclass(frozen=True)
class BlockGramBudget:
    """Exact reconstruction and sufficient block-fusion bounds."""

    exact_energy: float
    square_sum_energy: float
    signed_fusion_ratio: float
    absolute_block_upper: float
    coherence_constant: float
    coherence_upper: float
    gershgorin_constant: float
    gershgorin_upper: float
    block_energies: np.ndarray
    normalized_gram: np.ndarray
    minimum_gram_eigenvalue: float


def gram_budget(gram: np.ndarray, *, tolerance: float = 1.0e-12) -> BlockGramBudget:
    r"""Evaluate square-summed and coherence-weighted Hardy bounds."""

    value = _square_matrix(gram, "gram")
    hermitian = _hermitian(value)
    diagonal = np.real(np.diag(hermitian))
    scale = max(1.0, float(np.max(np.abs(diagonal), initial=0.0)))
    tol = float(tolerance)
    if np.min(diagonal, initial=0.0) < -tol * scale:
        raise ValueError("gram has a negative diagonal beyond tolerance")
    energies = np.sqrt(np.maximum(diagonal, 0.0))
    active = energies > math.sqrt(tol * scale)
    normalized = np.zeros_like(hermitian)
    if np.any(active):
        active_indices = np.flatnonzero(active)
        denominator = np.outer(energies[active], energies[active])
        active_gram = hermitian[np.ix_(active_indices, active_indices)] / denominator
        active_gram = _hermitian(active_gram)
        normalized[np.ix_(active_indices, active_indices)] = active_gram
        coherence = float(np.max(np.linalg.eigvalsh(active_gram)).real)
        gershgorin = float(np.max(np.sum(np.abs(active_gram), axis=1)))
    else:
        coherence = 0.0
        gershgorin = 0.0
    square_sum_squared = float(np.sum(np.maximum(diagonal, 0.0)))
    exact_squared = float(np.real(np.sum(hermitian)))
    if exact_squared < -tol * max(1.0, square_sum_squared):
        raise ValueError("reconstructed energy square is negative beyond tolerance")
    exact_squared = max(exact_squared, 0.0)
    return BlockGramBudget(
        exact_energy=math.sqrt(exact_squared),
        square_sum_energy=math.sqrt(square_sum_squared),
        signed_fusion_ratio=(
            exact_squared / square_sum_squared
            if square_sum_squared > 0.0
            else 0.0
        ),
        absolute_block_upper=float(np.sum(energies)),
        coherence_constant=coherence,
        coherence_upper=math.sqrt(max(0.0, coherence * square_sum_squared)),
        gershgorin_constant=gershgorin,
        gershgorin_upper=math.sqrt(max(0.0, gershgorin * square_sum_squared)),
        block_energies=energies,
        normalized_gram=normalized,
        minimum_gram_eigenvalue=float(np.min(np.linalg.eigvalsh(hermitian)).real),
    )
