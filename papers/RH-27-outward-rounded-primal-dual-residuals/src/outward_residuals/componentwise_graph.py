"""Componentwise refinement of the stored quadratic-map factor graph."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix

from .componentwise import (
    ComponentwiseBall,
    componentwise_add,
    componentwise_adjoint,
    componentwise_dense_exact_matmul,
    componentwise_matmul,
    componentwise_negate,
    componentwise_scalar_multiply,
    componentwise_scale_rows,
    componentwise_sparse_exact_matmul,
    componentwise_subtract,
)
from .enclosures import magnitude_upper


@dataclass(frozen=True)
class ComponentwiseBlocks:
    direct: ComponentwiseBall
    forcing: ComponentwiseBall
    observation_adjoint: ComponentwiseBall

    @property
    def observation(self) -> ComponentwiseBall:
        return componentwise_adjoint(self.observation_adjoint)


@dataclass(frozen=True)
class ComponentwiseNode:
    primal_residual: ComponentwiseBall
    dual_residual: ComponentwiseBall
    base_consistency: ComponentwiseBall
    primal_increment: ComponentwiseBall
    primal_correction: ComponentwiseBall
    dual_weighted_correction: ComponentwiseBall
    total_computed_correction: ComponentwiseBall


class ComponentwiseStoredFactorGraph:
    """Stored-factor graph retaining one radius for every output entry."""

    def __init__(
        self,
        matrix: csr_matrix,
        right_modes: np.ndarray,
        left_modes: np.ndarray,
        peripheral_values: np.ndarray,
        synthesis: np.ndarray,
        analysis: np.ndarray,
    ) -> None:
        self.matrix = matrix.tocsr(copy=False)
        self.matrix_adjoint = self.matrix.conj().T.tocsr()
        self.matrix_absolute = self.matrix.copy()
        self.matrix_absolute.data = magnitude_upper(self.matrix.data)
        self.matrix_adjoint_absolute = self.matrix_adjoint.copy()
        self.matrix_adjoint_absolute.data = magnitude_upper(
            self.matrix_adjoint.data
        )
        self.right = np.asarray(right_modes)
        self.left = np.asarray(left_modes)
        self.values = np.asarray(peripheral_values)
        self.synthesis = np.asarray(synthesis)
        self.analysis = np.asarray(analysis)
        self.maximum_row_nonzeros = int(np.max(np.diff(self.matrix.indptr)))
        self.maximum_column_nonzeros = int(
            np.max(np.diff(self.matrix_adjoint.indptr))
        )
        self._absolute = {
            "right": magnitude_upper(self.right),
            "left_t": magnitude_upper(self.left.T),
            "right_h": magnitude_upper(self.right.conj().T),
            "left_conj": magnitude_upper(self.left.conj()),
            "synthesis": magnitude_upper(self.synthesis),
            "analysis": magnitude_upper(self.analysis),
            "synthesis_h": magnitude_upper(self.synthesis.conj().T),
            "analysis_h": magnitude_upper(self.analysis.conj().T),
        }

    def _dense(
        self, name: str, operator: np.ndarray, ball: ComponentwiseBall
    ) -> ComponentwiseBall:
        return componentwise_dense_exact_matmul(
            operator, ball, absolute_matrix=self._absolute[name]
        )

    def packet(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return self._dense(
            "synthesis",
            self.synthesis,
            self._dense("analysis", self.analysis, source),
        )

    def external(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return componentwise_subtract(source, self.packet(source))

    def external_adjoint(self, source: ComponentwiseBall) -> ComponentwiseBall:
        coefficients = self._dense(
            "synthesis_h", self.synthesis.conj().T, source
        )
        correction = self._dense(
            "analysis_h", self.analysis.conj().T, coefficients
        )
        return componentwise_subtract(source, correction)

    def one_step(self, source: ComponentwiseBall) -> ComponentwiseBall:
        matrix_part = componentwise_sparse_exact_matmul(
            self.matrix,
            source,
            absolute_matrix=self.matrix_absolute,
            maximum_row_nonzeros=self.maximum_row_nonzeros,
        )
        coefficients = self._dense("left_t", self.left.T, source)
        correction = self._dense(
            "right",
            self.right,
            componentwise_scale_rows(self.values, coefficients),
        )
        return componentwise_subtract(matrix_part, correction)

    def one_step_adjoint(self, source: ComponentwiseBall) -> ComponentwiseBall:
        matrix_part = componentwise_sparse_exact_matmul(
            self.matrix_adjoint,
            source,
            absolute_matrix=self.matrix_adjoint_absolute,
            maximum_row_nonzeros=self.maximum_column_nonzeros,
        )
        coefficients = self._dense("right_h", self.right.conj().T, source)
        correction = self._dense(
            "left_conj",
            self.left.conj(),
            componentwise_scale_rows(self.values.conj(), coefficients),
        )
        return componentwise_subtract(matrix_part, correction)

    def two_step(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return self.one_step(self.one_step(source))

    def two_step_adjoint(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return self.one_step_adjoint(self.one_step_adjoint(source))

    def action(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return self.external(self.two_step(self.external(source)))

    def action_adjoint(self, source: ComponentwiseBall) -> ComponentwiseBall:
        return self.external_adjoint(
            self.two_step_adjoint(self.external_adjoint(source))
        )

    def build_blocks(self) -> ComponentwiseBlocks:
        returned = self.two_step(ComponentwiseBall.exact(self.synthesis))
        return ComponentwiseBlocks(
            direct=self._dense("analysis", self.analysis, returned),
            forcing=self.external(returned),
            observation_adjoint=self.external_adjoint(
                self.two_step_adjoint(
                    ComponentwiseBall.exact(self.analysis.conj().T)
                )
            ),
        )

    def node(
        self,
        blocks: ComponentwiseBlocks,
        spectral_parameter: complex,
        base_feshbach: np.ndarray,
        base_solution: np.ndarray,
        deep_solution: np.ndarray,
        dual_solution: np.ndarray,
    ) -> ComponentwiseNode:
        zeta = complex(spectral_parameter)
        base = ComponentwiseBall.exact(np.asarray(base_solution))
        deep = ComponentwiseBall.exact(np.asarray(deep_solution))
        dual = ComponentwiseBall.exact(np.asarray(dual_solution))
        primal_residual = componentwise_subtract(
            blocks.forcing,
            componentwise_subtract(
                componentwise_scalar_multiply(zeta, deep),
                self.action(deep),
            ),
        )
        dual_residual = componentwise_subtract(
            blocks.observation_adjoint,
            componentwise_subtract(
                componentwise_scalar_multiply(np.conj(zeta), dual),
                self.action_adjoint(dual),
            ),
        )
        increment = componentwise_subtract(deep, base)
        observation = blocks.observation
        primal_correction = componentwise_negate(
            componentwise_matmul(observation, increment)
        )
        dual_weighted = componentwise_negate(
            componentwise_matmul(
                componentwise_adjoint(dual), primal_residual
            )
        )
        rank = self.synthesis.shape[1]
        ideal_base = componentwise_subtract(
            componentwise_subtract(
                componentwise_scalar_multiply(
                    zeta,
                    ComponentwiseBall.exact(
                        np.eye(rank, dtype=np.complex128)
                    ),
                ),
                blocks.direct,
            ),
            componentwise_matmul(observation, base),
        )
        consistency = componentwise_subtract(
            ideal_base, ComponentwiseBall.exact(np.asarray(base_feshbach))
        )
        total = componentwise_add(
            consistency,
            componentwise_add(primal_correction, dual_weighted),
        )
        return ComponentwiseNode(
            primal_residual=primal_residual,
            dual_residual=dual_residual,
            base_consistency=consistency,
            primal_increment=increment,
            primal_correction=primal_correction,
            dual_weighted_correction=dual_weighted,
            total_computed_correction=total,
        )
