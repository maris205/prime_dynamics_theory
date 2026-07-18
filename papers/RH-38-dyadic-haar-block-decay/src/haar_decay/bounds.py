"""Scalar bounds behind the dyadic quarter/half law."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class DerivativeEnvelope:
    """Uniform derivative bounds for a normalized kernel on the unit square."""

    x: float
    y: float
    xx: float
    xy: float
    yy: float


@dataclass(frozen=True)
class HaarBlockBounds:
    """Spectral-norm uppers for the four unnormalized Haar blocks."""

    coarse_consistency: float
    coarse_to_detail: float
    detail_to_coarse: float
    detail_block: float


def _nonnegative(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0.0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return result


def ideal_midpoint_haar_bounds(
    coarse_mesh: float, envelope: DerivativeEnvelope
) -> HaarBlockBounds:
    """Return the exact Taylor/Schur bounds for ``h k(x_i,y_j)`` matrices."""

    h = _nonnegative(coarse_mesh, "coarse_mesh")
    if h == 0.0:
        raise ValueError("coarse_mesh must be positive")
    x = _nonnegative(envelope.x, "envelope.x")
    y = _nonnegative(envelope.y, "envelope.y")
    xx = _nonnegative(envelope.xx, "envelope.xx")
    xy = _nonnegative(envelope.xy, "envelope.xy")
    yy = _nonnegative(envelope.yy, "envelope.yy")
    return HaarBlockBounds(
        coarse_consistency=h * h * (xx + 2.0 * xy + yy) / 32.0,
        coarse_to_detail=h * x / 4.0,
        detail_to_coarse=h * y / 4.0,
        detail_block=h * h * xy / 16.0,
    )


def discrete_normalization_defect(
    mesh: float,
    *,
    raw_kernel_upper: float,
    raw_yy_upper: float,
    continuum_normalizer_lower: float,
) -> float:
    """Bound discrete row normalization relative to continuum normalization."""

    h = _nonnegative(mesh, "mesh")
    raw = _nonnegative(raw_kernel_upper, "raw_kernel_upper")
    raw_yy = _nonnegative(raw_yy_upper, "raw_yy_upper")
    lower = _nonnegative(
        continuum_normalizer_lower, "continuum_normalizer_lower"
    )
    if h == 0.0 or lower == 0.0:
        raise ValueError("mesh and continuum normalizer lower must be positive")
    midpoint_error = h * h * raw_yy / 24.0
    if midpoint_error >= lower:
        raise ValueError("midpoint normalizer error is not smaller than its lower bound")
    return raw * midpoint_error / (lower * (lower - midpoint_error))


def discretely_normalized_haar_bounds(
    coarse_mesh: float,
    envelope: DerivativeEnvelope,
    *,
    raw_kernel_upper: float,
    raw_yy_upper: float,
    continuum_normalizer_lower: float,
) -> HaarBlockBounds:
    """Add the quotient-midpoint normalization defects to the ideal rates."""

    ideal = ideal_midpoint_haar_bounds(coarse_mesh, envelope)
    coarse_defect = discrete_normalization_defect(
        coarse_mesh,
        raw_kernel_upper=raw_kernel_upper,
        raw_yy_upper=raw_yy_upper,
        continuum_normalizer_lower=continuum_normalizer_lower,
    )
    fine_defect = discrete_normalization_defect(
        0.5 * float(coarse_mesh),
        raw_kernel_upper=raw_kernel_upper,
        raw_yy_upper=raw_yy_upper,
        continuum_normalizer_lower=continuum_normalizer_lower,
    )
    return HaarBlockBounds(
        coarse_consistency=(
            ideal.coarse_consistency + coarse_defect + fine_defect
        ),
        coarse_to_detail=ideal.coarse_to_detail + fine_defect,
        detail_to_coarse=ideal.detail_to_coarse + fine_defect,
        detail_block=ideal.detail_block + fine_defect,
    )


def square_block_bounds(
    coarse_operator_upper: float, one_step: HaarBlockBounds
) -> HaarBlockBounds:
    """Propagate one-step Haar bounds through exact block squaring."""

    m = _nonnegative(coarse_operator_upper, "coarse_operator_upper")
    e = _nonnegative(one_step.coarse_consistency, "coarse_consistency")
    c = _nonnegative(one_step.coarse_to_detail, "coarse_to_detail")
    b = _nonnegative(one_step.detail_to_coarse, "detail_to_coarse")
    d = _nonnegative(one_step.detail_block, "detail_block")
    return HaarBlockBounds(
        coarse_consistency=2.0 * m * e + e * e + b * c,
        coarse_to_detail=c * (m + e + d),
        detail_to_coarse=b * (m + e + d),
        detail_block=b * c + d * d,
    )


def renormalized_constants(
    bounds: HaarBlockBounds, coarse_mesh: float
) -> HaarBlockBounds:
    """Divide consistency/detail by ``h^2`` and cross channels by ``h``."""

    h = _nonnegative(coarse_mesh, "coarse_mesh")
    if h == 0.0:
        raise ValueError("coarse_mesh must be positive")
    return HaarBlockBounds(
        coarse_consistency=bounds.coarse_consistency / (h * h),
        coarse_to_detail=bounds.coarse_to_detail / h,
        detail_to_coarse=bounds.detail_to_coarse / h,
        detail_block=bounds.detail_block / (h * h),
    )
