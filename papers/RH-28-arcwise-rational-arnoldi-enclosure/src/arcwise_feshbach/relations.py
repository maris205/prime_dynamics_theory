"""Static certified Arnoldi source, relation, and observation defects."""

from __future__ import annotations

import gc
import time
from dataclasses import dataclass

import numpy as np

from outward_residuals import (
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_adjoint,
    componentwise_dense_exact_matmul,
    componentwise_matmul,
    componentwise_scalar_multiply,
    componentwise_subtract,
    gamma,
    magnitude_upper,
)


def _ball_column(ball: ComponentwiseBall, column: int) -> ComponentwiseBall:
    return ComponentwiseBall(
        np.asarray(ball.center)[:, int(column) : int(column) + 1],
        np.asarray(ball.radius)[:, int(column) : int(column) + 1],
    )


def _column_norm_uppers(ball: ComponentwiseBall) -> np.ndarray:
    """Return one outward Euclidean-norm bound per matrix column."""

    center = np.asarray(ball.center)
    if center.ndim != 2:
        raise ValueError("column norms require a matrix ball")
    return np.asarray(
        [_ball_column(ball, column).norm_upper for column in range(center.shape[1])],
        dtype=np.float64,
    )


def _magnitude_ball(ball: ComponentwiseBall) -> np.ndarray:
    raw = magnitude_upper(ball.center) + np.asarray(ball.radius)
    return np.nextafter(raw, np.inf)


def _row_sum_upper(values: np.ndarray) -> float:
    matrix = np.asarray(values, dtype=np.float64)
    raw = np.sum(matrix, axis=1, dtype=np.float64)
    denominator = float(
        np.nextafter(1.0 - gamma(2 * matrix.shape[1] + 8), 0.0)
    )
    return float(np.nextafter(np.max(raw) / denominator, np.inf))


def basis_two_norm_upper(basis: np.ndarray) -> float:
    """Certify ``||Q||_2`` from an outward Gram matrix."""

    values = np.asarray(basis, dtype=np.complex128)
    gram = componentwise_matmul(
        ComponentwiseBall.exact(values.conj().T),
        ComponentwiseBall.exact(values),
    )
    gram_infinity = _row_sum_upper(_magnitude_ball(gram))
    return float(np.nextafter(np.sqrt(gram_infinity), np.inf))


@dataclass(frozen=True)
class RelationSummary:
    source_defect_norm_upper: float
    source_center_norm: float
    source_radius: float
    relation_norm_upper: float
    relation_center_norm: float
    relation_radius: float
    relation_column_norm_uppers: np.ndarray
    basis_norm_upper: float


@dataclass(frozen=True)
class PrimalRelationSummary(RelationSummary):
    base_coupling_defect_norm_upper: float
    base_coupling_center_norm: float
    base_coupling_radius: float
    base_coupling_column_norm_uppers: np.ndarray
    deep_physical_coupling_column_norm_uppers: np.ndarray


@dataclass(frozen=True)
class StaticArcCertificate:
    direct_defect_norm_upper: float
    direct_center_norm: float
    direct_radius: float
    observation_norm_upper: float
    primal: tuple[PrimalRelationSummary, ...]
    dual: tuple[RelationSummary, ...]
    elapsed_seconds: float


def _relation_summary(
    source: ComponentwiseBall,
    beta: float,
    basis: np.ndarray,
    hessenberg: np.ndarray,
    action,
) -> tuple[RelationSummary, ComponentwiseBall]:
    values = np.asarray(basis, dtype=np.complex128)
    projected = np.asarray(hessenberg, dtype=np.complex128)
    normalized_source = componentwise_scalar_multiply(
        float(beta), ComponentwiseBall.exact(values[:, :1])
    )
    source_defect = componentwise_subtract(source, normalized_source)
    applied = action(ComponentwiseBall.exact(values))
    reconstructed = componentwise_dense_exact_matmul(
        values,
        ComponentwiseBall.exact(projected),
    )
    relation = componentwise_subtract(applied, reconstructed)
    return (
        RelationSummary(
            source_defect_norm_upper=source_defect.norm_upper,
            source_center_norm=float(np.linalg.norm(source_defect.center)),
            source_radius=source_defect.radius_frobenius_upper,
            relation_norm_upper=relation.norm_upper,
            relation_center_norm=float(np.linalg.norm(relation.center)),
            relation_radius=relation.radius_frobenius_upper,
            relation_column_norm_uppers=_column_norm_uppers(relation),
            basis_norm_upper=basis_two_norm_upper(values),
        ),
        relation,
    )


def build_static_arc_certificate(
    graph: ComponentwiseStoredFactorGraph,
    blocks,
    primal_model,
    dual_model,
    *,
    base_depth: int,
    maximum_depth: int,
) -> StaticArcCertificate:
    """Build all ambient defects needed for cheap rational arc evaluation."""

    if primal_model.retained_bases is None or dual_model.retained_bases is None:
        raise ValueError("both Arnoldi models must retain their ambient bases")
    begun = time.time()
    rank = primal_model.packet_rank
    if dual_model.packet_rank != rank:
        raise ValueError("primal and dual packet ranks differ")

    direct_defect = componentwise_subtract(
        ComponentwiseBall.exact(np.asarray(primal_model.reduced)),
        blocks.direct,
    )
    observation = blocks.observation
    observation_norm = observation.norm_upper
    primal_rows: list[PrimalRelationSummary] = []
    dual_rows: list[RelationSummary] = []

    for column in range(rank):
        print(
            f"  certify primal relation {column + 1}/{rank}", flush=True
        )
        basis = np.asarray(primal_model.retained_bases[column])[
            :, : int(maximum_depth)
        ]
        hessenberg = np.asarray(primal_model.hessenbergs[column])[
            : int(maximum_depth), : int(maximum_depth)
        ]
        summary, _ = _relation_summary(
            _ball_column(blocks.forcing, column),
            float(primal_model.forcing_norms[column]),
            basis,
            hessenberg,
            graph.action,
        )
        physical_coupling = componentwise_matmul(
            observation,
            ComponentwiseBall.exact(basis),
        )
        base_physical_coupling = ComponentwiseBall(
            np.asarray(physical_coupling.center)[:, : int(base_depth)],
            np.asarray(physical_coupling.radius)[:, : int(base_depth)],
        )
        model_coupling = np.asarray(primal_model.output_couplings[column])[
            :, : int(base_depth)
        ]
        coupling_defect = componentwise_subtract(
            ComponentwiseBall.exact(model_coupling),
            base_physical_coupling,
        )
        primal_rows.append(
            PrimalRelationSummary(
                **summary.__dict__,
                base_coupling_defect_norm_upper=coupling_defect.norm_upper,
                base_coupling_center_norm=float(
                    np.linalg.norm(coupling_defect.center)
                ),
                base_coupling_radius=coupling_defect.radius_frobenius_upper,
                base_coupling_column_norm_uppers=_column_norm_uppers(
                    coupling_defect
                ),
                deep_physical_coupling_column_norm_uppers=_column_norm_uppers(
                    physical_coupling
                ),
            )
        )
        gc.collect()

    for column in range(rank):
        print(f"  certify dual relation {column + 1}/{rank}", flush=True)
        basis = np.asarray(dual_model.retained_bases[column])[
            :, : int(maximum_depth)
        ]
        hessenberg = np.asarray(dual_model.hessenbergs[column])[
            : int(maximum_depth), : int(maximum_depth)
        ]
        summary, _ = _relation_summary(
            _ball_column(blocks.observation_adjoint, column),
            float(dual_model.forcing_norms[column]),
            basis,
            hessenberg,
            graph.action_adjoint,
        )
        dual_rows.append(summary)
        gc.collect()

    return StaticArcCertificate(
        direct_defect_norm_upper=direct_defect.norm_upper,
        direct_center_norm=float(np.linalg.norm(direct_defect.center)),
        direct_radius=direct_defect.radius_frobenius_upper,
        observation_norm_upper=observation_norm,
        primal=tuple(primal_rows),
        dual=tuple(dual_rows),
        elapsed_seconds=time.time() - begun,
    )
