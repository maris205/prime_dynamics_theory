"""Arcwise conditional Feshbach budgets from certified Arnoldi relations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from outward_residuals import (
    ComponentwiseBall,
    componentwise_dense_exact_matmul,
    componentwise_scalar_multiply,
    componentwise_subtract,
    gamma,
    inverse_certificate,
    lower_divide,
    magnitude_upper,
    upper_add,
    upper_divide,
    upper_multiply,
)

from .coordinates import (
    CoordinateDisc,
    coordinate_extension_sum,
    enclose_coordinate_increment,
    enclose_shifted_coordinates,
)
from .geometry import ArcDisc
from .relations import StaticArcCertificate


def _column_frobenius_upper(bounds: list[float]) -> float:
    """Outward upper bound for the Frobenius norm of column 2-norm bounds."""

    if not bounds:
        return 0.0
    values = np.asarray(bounds, dtype=np.float64)
    if np.any(values < 0.0) or np.any(~np.isfinite(values)):
        raise ValueError("column bounds must be finite and nonnegative")
    scale = float(np.max(values))
    if scale == 0.0:
        return 0.0
    scale_lower = float(np.nextafter(scale, 0.0))
    scaled = np.nextafter(values / scale_lower, np.inf)
    scaled[values == 0.0] = 0.0
    squares = np.nextafter(scaled * scaled, np.inf)
    raw = float(np.sum(squares, dtype=np.float64))
    denominator = float(
        np.nextafter(1.0 - gamma(2 * values.size + 8), 0.0)
    )
    sum_upper = upper_divide(raw, denominator)
    root_upper = float(np.nextafter(np.sqrt(sum_upper), np.inf))
    return upper_multiply(scale, root_upper)


def _coordinate(
    model,
    column: int,
    depth: int,
    center: complex,
    radius: float,
) -> CoordinateDisc:
    selected = int(depth)
    hessenberg = np.asarray(model.hessenbergs[int(column)])[
        :selected, :selected
    ]
    right_hand_side = np.zeros(selected, dtype=np.complex128)
    right_hand_side[0] = float(model.forcing_norms[int(column)])
    return enclose_shifted_coordinates(
        hessenberg,
        right_hand_side,
        center,
        radius,
    )


def _weighted_coordinate_upper(
    column_norms: np.ndarray, coordinate: CoordinateDisc
) -> float:
    r"""Bound ``sum_j column_norms[j] * |coordinate[j]|`` outwardly."""

    weights = np.asarray(column_norms, dtype=np.float64).reshape(-1)
    if weights.shape != coordinate.center.shape:
        raise ValueError("column weights and coordinates have incompatible shapes")
    magnitudes = np.nextafter(
        magnitude_upper(coordinate.center) + coordinate.radius,
        np.inf,
    )
    total = 0.0
    for weight, value in zip(weights, magnitudes):
        total = upper_add(
            total, upper_multiply(float(weight), float(value))
        )
    return total


def projected_feshbach_ball(
    model,
    coordinates: list[CoordinateDisc],
    center: complex,
    radius: float,
    *,
    depth: int,
) -> ComponentwiseBall:
    """Enclose the exact stored projected Feshbach rational matrix."""

    rank = int(model.packet_rank)
    if len(coordinates) != rank:
        raise ValueError("one coordinate disc is required per packet column")
    selected = int(depth)
    if selected < 1 or selected > int(model.maximum_depth):
        raise ValueError("depth is outside the Arnoldi model")
    identity = ComponentwiseBall.exact(
        np.eye(rank, dtype=np.complex128)
    )
    spectral = componentwise_scalar_multiply(center, identity)
    parameter_radius = np.zeros((rank, rank), dtype=np.float64)
    np.fill_diagonal(parameter_radius, float(radius))
    spectral = ComponentwiseBall(
        spectral.center,
        np.nextafter(spectral.radius + parameter_radius, np.inf),
    )
    self_energy_center = np.empty((rank, rank), dtype=np.complex128)
    self_energy_radius = np.empty((rank, rank), dtype=np.float64)
    for column, coordinate in enumerate(coordinates):
        if np.asarray(coordinate.center).shape != (selected,):
            raise ValueError("coordinate disc has incompatible depth")
        coupling = np.asarray(model.output_couplings[column])[
            :, :selected
        ]
        contribution = componentwise_dense_exact_matmul(
            coupling,
            coordinate.ball,
        )
        self_energy_center[:, column] = np.asarray(contribution.center).reshape(-1)
        self_energy_radius[:, column] = np.asarray(contribution.radius).reshape(-1)
    self_energy = ComponentwiseBall(
        self_energy_center, self_energy_radius
    )
    return componentwise_subtract(
        componentwise_subtract(
            spectral,
            ComponentwiseBall.exact(np.asarray(model.reduced)),
        ),
        self_energy,
    )


def family_inverse_norm_upper(ball: ComponentwiseBall) -> tuple[float, float, float]:
    """Bound every inverse in a Frobenius ball around a small matrix."""

    center_certificate = inverse_certificate(np.asarray(ball.center))
    uncertainty = ball.radius_frobenius_upper
    product = upper_multiply(
        center_certificate.inverse_norm_upper, uncertainty
    )
    if product >= 1.0:
        raise RuntimeError("the projected Feshbach family failed its Neumann test")
    denominator = float(np.nextafter(1.0 - product, 0.0))
    family_upper = upper_divide(
        center_certificate.inverse_norm_upper, denominator
    )
    return family_upper, product, center_certificate.defect_norm_upper


@dataclass(frozen=True)
class ArcBudget:
    index: int
    angle: float
    center: complex
    radius: float
    correction_ratio_upper: float
    remainder_coefficient_upper: float
    resolvent_budget_lower: float
    primal_residual_norm_upper: float
    dual_residual_norm_upper: float
    base_consistency_norm_upper: float
    primal_increment_norm_upper: float
    dual_solution_norm_upper: float
    computed_correction_norm_upper: float
    projected_inverse_norm_upper: float
    projected_family_neumann_product: float
    projected_center_inverse_defect: float
    maximum_coordinate_contraction: float
    maximum_coordinate_iterations: int


def evaluate_arc_budget(
    arc: ArcDisc,
    primal_model,
    dual_model,
    static: StaticArcCertificate,
    *,
    base_depth: int,
    maximum_depth: int,
) -> ArcBudget:
    """Return one full-subarc conditional budget."""

    rank = primal_model.packet_rank
    base_coordinates = [
        _coordinate(
            primal_model,
            column,
            base_depth,
            arc.center,
            arc.radius,
        )
        for column in range(rank)
    ]

    # The small projected family is the dominant adaptive rejection test.
    # Certify it before constructing the more expensive deep and dual solves,
    # so failed parent arcs can be bisected with minimal wasted work.
    feshbach = projected_feshbach_ball(
        primal_model,
        base_coordinates,
        arc.center,
        arc.radius,
        depth=base_depth,
    )
    inverse_upper, family_product, inverse_defect = family_inverse_norm_upper(
        feshbach
    )

    dual_coordinates: list[CoordinateDisc] = []
    increment_coordinates: list[CoordinateDisc] = []
    deep_coordinates: list[CoordinateDisc] = []
    for column, base_coordinate in enumerate(base_coordinates):
        dual_coordinates.append(
            _coordinate(
                dual_model,
                column,
                maximum_depth,
                np.conj(arc.center),
                arc.radius,
            )
        )
        deep_hessenberg = np.asarray(primal_model.hessenbergs[column])[
            : int(maximum_depth), : int(maximum_depth)
        ]
        increment = enclose_coordinate_increment(
            deep_hessenberg,
            base_coordinate,
            arc.center,
            arc.radius,
            base_depth=base_depth,
        )
        increment_coordinates.append(increment)
        deep_coordinates.append(
            coordinate_extension_sum(base_coordinate, increment)
        )

    primal_column_bounds: list[float] = []
    dual_column_bounds: list[float] = []
    increment_column_bounds: list[float] = []
    dual_solution_column_bounds: list[float] = []
    consistency_column_bounds: list[float] = []
    primal_correction_column_bounds: list[float] = []
    contractions: list[float] = []
    iterations: list[int] = []
    for column in range(rank):
        primal_static = static.primal[column]
        dual_static = static.dual[column]
        base_coordinate = base_coordinates[column]
        deep_coordinate = deep_coordinates[column]
        dual_coordinate = dual_coordinates[column]
        difference = increment_coordinates[column]
        primal_column_bounds.append(
            upper_add(
                primal_static.source_defect_norm_upper,
                _weighted_coordinate_upper(
                    primal_static.relation_column_norm_uppers,
                    deep_coordinate,
                ),
            )
        )
        dual_column_bounds.append(
            upper_add(
                dual_static.source_defect_norm_upper,
                _weighted_coordinate_upper(
                    dual_static.relation_column_norm_uppers,
                    dual_coordinate,
                ),
            )
        )
        increment_column_bounds.append(
            upper_multiply(
                primal_static.basis_norm_upper,
                difference.norm_upper,
            )
        )
        dual_solution_column_bounds.append(
            upper_multiply(
                dual_static.basis_norm_upper,
                dual_coordinate.norm_upper,
            )
        )
        consistency_column_bounds.append(
            _weighted_coordinate_upper(
                primal_static.base_coupling_column_norm_uppers,
                base_coordinate,
            )
        )
        primal_correction_column_bounds.append(
            _weighted_coordinate_upper(
                primal_static.deep_physical_coupling_column_norm_uppers,
                difference,
            )
        )
        contractions.extend(
            (
                base_coordinate.contraction_upper,
                deep_coordinate.contraction_upper,
                dual_coordinate.contraction_upper,
            )
        )
        iterations.extend(
            (
                base_coordinate.fixed_point_iterations,
                deep_coordinate.fixed_point_iterations,
                dual_coordinate.fixed_point_iterations,
            )
        )

    primal_residual = _column_frobenius_upper(primal_column_bounds)
    dual_residual = _column_frobenius_upper(dual_column_bounds)
    primal_increment = _column_frobenius_upper(increment_column_bounds)
    dual_solution = _column_frobenius_upper(dual_solution_column_bounds)
    consistency = upper_add(
        static.direct_defect_norm_upper,
        _column_frobenius_upper(consistency_column_bounds),
    )
    primal_correction = _column_frobenius_upper(
        primal_correction_column_bounds
    )
    dual_weighted = upper_multiply(dual_solution, primal_residual)
    computed_correction = upper_add(
        consistency, primal_correction, dual_weighted
    )
    eta = upper_multiply(inverse_upper, computed_correction)
    coefficient = upper_multiply(
        inverse_upper,
        upper_multiply(dual_residual, primal_residual),
    )
    numerator = float(max(0.0, np.nextafter(1.0 - eta, 0.0)))
    budget = lower_divide(numerator, coefficient)
    return ArcBudget(
        index=arc.index,
        angle=arc.angle,
        center=arc.center,
        radius=arc.radius,
        correction_ratio_upper=eta,
        remainder_coefficient_upper=coefficient,
        resolvent_budget_lower=budget,
        primal_residual_norm_upper=primal_residual,
        dual_residual_norm_upper=dual_residual,
        base_consistency_norm_upper=consistency,
        primal_increment_norm_upper=primal_increment,
        dual_solution_norm_upper=dual_solution,
        computed_correction_norm_upper=computed_correction,
        projected_inverse_norm_upper=inverse_upper,
        projected_family_neumann_product=family_product,
        projected_center_inverse_defect=inverse_defect,
        maximum_coordinate_contraction=max(contractions),
        maximum_coordinate_iterations=max(iterations),
    )
