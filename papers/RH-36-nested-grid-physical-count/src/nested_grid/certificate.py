"""Rigorous low-rank and Schur-continuation bounds for RH-36."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math

import numpy as np


@dataclass(frozen=True)
class BlockNormCertificate:
    """A certified spectral-norm upper bound for one stored coordinate block."""

    name: str
    dimension: int
    approximation_rank: int
    left_gram_defect_frobenius_upper: float
    right_gram_defect_frobenius_upper: float
    left_factor_two_norm_upper: float
    right_factor_two_norm_upper: float
    singular_scale_upper: float
    low_rank_two_norm_upper: float
    residual_frobenius_upper: float
    residual_center_frobenius_upper: float
    residual_radius_frobenius_upper: float
    block_two_norm_upper: float
    residual_center_sha256: str
    residual_radius_sha256: str


@dataclass(frozen=True)
class ContinuationGate:
    """Global constants in the nested-grid Feshbach continuation theorem."""

    contour_origin_distance_lower: float
    detail_norm_upper: float
    detail_resolvent_upper: float
    coarse_consistency_upper: float
    coarse_to_detail_upper: float
    detail_to_coarse_upper: float
    self_energy_upper: float
    effective_perturbation_upper: float
    admissible_coarse_resolvent_upper: float
    detail_spectrum_outside_counting_circle: bool


def _up(value: float) -> float:
    return float(np.nextafter(float(value), np.inf))


def _down(value: float) -> float:
    return float(np.nextafter(float(value), -np.inf))


def _up_add(left: float, right: float) -> float:
    return _up(float(left) + float(right))


def _up_mul(left: float, right: float) -> float:
    return _up(float(left) * float(right))


def _up_sqrt(value: float) -> float:
    return _up(math.sqrt(float(value)))


def _slice_ball(ball, selector):
    from outward_residuals import ComponentwiseBall

    return ComponentwiseBall(
        np.asarray(ball.center)[selector],
        np.asarray(ball.radius)[selector],
    )


def _join_pair(even, odd):
    from outward_residuals import ComponentwiseBall

    center = np.empty(
        (2 * even.center.shape[0],) + even.center.shape[1:],
        dtype=np.result_type(even.center, odd.center),
    )
    radius = np.empty(center.shape, dtype=np.float64)
    center[0::2] = even.center
    center[1::2] = odd.center
    radius[0::2] = even.radius
    radius[1::2] = odd.radius
    return ComponentwiseBall(center, radius)


def prolong_ball(ball):
    """Apply the exact replication map J x = (x_i,x_i)."""

    return _join_pair(ball, ball)


def detail_injection_ball(ball):
    """Apply the exact alternating map K y = (y_i,-y_i)."""

    from outward_residuals import componentwise_negate

    return _join_pair(ball, componentwise_negate(ball))


def restrict_ball(ball):
    """Apply R x = (x_{2i}+x_{2i+1})/2 with outward arithmetic."""

    from outward_residuals import (
        componentwise_add,
        componentwise_scalar_multiply,
    )

    return componentwise_scalar_multiply(
        0.5,
        componentwise_add(
            _slice_ball(ball, slice(0, None, 2)),
            _slice_ball(ball, slice(1, None, 2)),
        ),
    )


def detail_restriction_ball(ball):
    """Apply S x = (x_{2i}-x_{2i+1})/2 with outward arithmetic."""

    from outward_residuals import (
        componentwise_scalar_multiply,
        componentwise_subtract,
    )

    return componentwise_scalar_multiply(
        0.5,
        componentwise_subtract(
            _slice_ball(ball, slice(0, None, 2)),
            _slice_ball(ball, slice(1, None, 2)),
        ),
    )


def coordinate_block_action(name: str, coarse_graph, fine_graph, source):
    """Evaluate one exact stored Haar-coordinate block on a ball."""

    from outward_residuals import componentwise_subtract

    if name == "coarse_consistency":
        fine_value = restrict_ball(
            fine_graph.two_step(prolong_ball(source))
        )
        return componentwise_subtract(
            fine_value, coarse_graph.two_step(source)
        )
    if name == "coarse_to_detail":
        return detail_restriction_ball(
            fine_graph.two_step(prolong_ball(source))
        )
    if name == "detail_to_coarse":
        return restrict_ball(
            fine_graph.two_step(detail_injection_ball(source))
        )
    if name == "detail_block":
        return detail_restriction_ball(
            fine_graph.two_step(detail_injection_ball(source))
        )
    raise ValueError(f"unknown coordinate block: {name}")


def coordinate_block_adjoint_action(
    name: str, coarse_graph, fine_graph, source
):
    """Evaluate the Euclidean adjoint of one coordinate block."""

    from outward_residuals import componentwise_subtract

    if name == "coarse_consistency":
        fine_value = restrict_ball(
            fine_graph.two_step_adjoint(prolong_ball(source))
        )
        return componentwise_subtract(
            fine_value, coarse_graph.two_step_adjoint(source)
        )
    if name == "coarse_to_detail":
        return restrict_ball(
            fine_graph.two_step_adjoint(detail_injection_ball(source))
        )
    if name == "detail_to_coarse":
        return detail_restriction_ball(
            fine_graph.two_step_adjoint(prolong_ball(source))
        )
    if name == "detail_block":
        return detail_restriction_ball(
            fine_graph.two_step_adjoint(detail_injection_ball(source))
        )
    raise ValueError(f"unknown coordinate block: {name}")


def _gram_factor_norm_upper(factor: np.ndarray, *, columns: bool) -> tuple[float, float]:
    from outward_residuals import (
        ComponentwiseBall,
        componentwise_dense_exact_matmul,
        componentwise_subtract,
    )

    values = np.asarray(factor)
    if values.ndim != 2:
        raise ValueError("low-rank factor must be a matrix")
    if columns:
        left = values.conj().T
        right = values
        rank = values.shape[1]
    else:
        left = values
        right = values.conj().T
        rank = values.shape[0]
    gram = componentwise_dense_exact_matmul(
        left,
        ComponentwiseBall.exact(right),
    )
    defect = componentwise_subtract(
        gram, ComponentwiseBall.exact(np.eye(rank, dtype=gram.center.dtype))
    )
    defect_upper = defect.norm_upper
    norm_upper = _up_sqrt(_up_add(1.0, defect_upper))
    return defect_upper, norm_upper


def certify_low_rank_block(
    name: str,
    coarse_graph,
    fine_graph,
    left_factor: np.ndarray,
    singular_values: np.ndarray,
    right_factor_adjoint: np.ndarray,
    *,
    chunk_size: int = 128,
) -> BlockNormCertificate:
    """Certify ``||E||_2`` from a stored low-rank center and residual."""

    from outward_residuals import (
        ComponentwiseBall,
        componentwise_dense_exact_matmul,
        componentwise_scale_rows,
        componentwise_subtract,
        frobenius_upper_array,
    )
    from sparse_grushin import combine_frobenius_bounds

    left = np.asarray(left_factor)
    scales = np.asarray(singular_values).reshape(-1)
    right_h = np.asarray(right_factor_adjoint)
    dimension = int(left.shape[0])
    rank = int(scales.size)
    if left.shape != (dimension, rank):
        raise ValueError("left factor has an incompatible shape")
    if right_h.shape != (rank, dimension):
        raise ValueError("right factor has an incompatible shape")

    left_defect, left_norm = _gram_factor_norm_upper(left, columns=True)
    right_defect, right_norm = _gram_factor_norm_upper(
        right_h, columns=False
    )
    scale_upper = _up(float(np.max(np.abs(scales))))
    low_rank_upper = _up_mul(
        _up_mul(left_norm, scale_upper), right_norm
    )

    residual_bounds: list[float] = []
    center_bounds: list[float] = []
    radius_bounds: list[float] = []
    center_hash = hashlib.sha256()
    radius_hash = hashlib.sha256()
    for start in range(0, dimension, int(chunk_size)):
        stop = min(start + int(chunk_size), dimension)
        width = stop - start
        source = np.zeros((dimension, width), dtype=np.float64)
        source[np.arange(start, stop), np.arange(width)] = 1.0
        target = coordinate_block_action(
            name,
            coarse_graph,
            fine_graph,
            ComponentwiseBall.exact(source),
        )
        right_chunk = ComponentwiseBall.exact(right_h[:, start:stop])
        scaled = componentwise_scale_rows(scales, right_chunk)
        approximation = componentwise_dense_exact_matmul(left, scaled)
        residual = componentwise_subtract(target, approximation)
        center = np.ascontiguousarray(residual.center)
        radius = np.ascontiguousarray(residual.radius)
        center_hash.update(center.view(np.uint8))
        radius_hash.update(radius.view(np.uint8))
        residual_bounds.append(residual.norm_upper)
        center_bounds.append(frobenius_upper_array(center))
        radius_bounds.append(frobenius_upper_array(radius))

    residual_upper = combine_frobenius_bounds(residual_bounds)
    center_upper = combine_frobenius_bounds(center_bounds)
    radius_upper = combine_frobenius_bounds(radius_bounds)
    block_upper = _up_add(low_rank_upper, residual_upper)
    return BlockNormCertificate(
        name=name,
        dimension=dimension,
        approximation_rank=rank,
        left_gram_defect_frobenius_upper=left_defect,
        right_gram_defect_frobenius_upper=right_defect,
        left_factor_two_norm_upper=left_norm,
        right_factor_two_norm_upper=right_norm,
        singular_scale_upper=scale_upper,
        low_rank_two_norm_upper=low_rank_upper,
        residual_frobenius_upper=residual_upper,
        residual_center_frobenius_upper=center_upper,
        residual_radius_frobenius_upper=radius_upper,
        block_two_norm_upper=block_upper,
        residual_center_sha256=center_hash.hexdigest(),
        residual_radius_sha256=radius_hash.hexdigest(),
    )


def continuation_gate(
    contour_center: complex,
    contour_radius: float,
    *,
    coarse_consistency_upper: float,
    coarse_to_detail_upper: float,
    detail_to_coarse_upper: float,
    detail_norm_upper: float,
) -> ContinuationGate:
    """Compose the global detail and self-energy bounds outward."""

    center_modulus_lower = _down(abs(complex(contour_center)))
    origin_distance = _down(center_modulus_lower - float(contour_radius))
    denominator = _down(origin_distance - float(detail_norm_upper))
    if denominator <= 0.0:
        detail_resolvent = float("inf")
        detail_outside = False
    else:
        detail_resolvent = _up(1.0 / denominator)
        detail_outside = bool(detail_norm_upper < origin_distance)
    self_energy = _up_mul(
        _up_mul(coarse_to_detail_upper, detail_resolvent),
        detail_to_coarse_upper,
    )
    effective = _up_add(coarse_consistency_upper, self_energy)
    admissible = float("inf") if effective == 0.0 else _down(1.0 / effective)
    return ContinuationGate(
        contour_origin_distance_lower=origin_distance,
        detail_norm_upper=float(detail_norm_upper),
        detail_resolvent_upper=detail_resolvent,
        coarse_consistency_upper=float(coarse_consistency_upper),
        coarse_to_detail_upper=float(coarse_to_detail_upper),
        detail_to_coarse_upper=float(detail_to_coarse_upper),
        self_energy_upper=self_energy,
        effective_perturbation_upper=effective,
        admissible_coarse_resolvent_upper=admissible,
        detail_spectrum_outside_counting_circle=detail_outside,
    )
