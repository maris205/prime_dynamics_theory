"""Certified stored-factor graph for the quadratic band-merging operator."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix

from .enclosures import (
    FrobeniusBall,
    add,
    conjugate_transpose,
    dense_abs_operator_upper,
    dense_exact_matmul,
    frobenius_upper_array,
    magnitude_upper,
    matmul,
    negate,
    scalar_multiply,
    scale_rows,
    sparse_abs_operator_upper,
    sparse_exact_matmul,
    subtract,
)


@dataclass(frozen=True)
class StoredBlocks:
    """Enclosures of the exact stored-factor blocks ``D,C,E*``."""

    direct: FrobeniusBall
    forcing: FrobeniusBall
    observation_adjoint: FrobeniusBall

    @property
    def observation(self) -> FrobeniusBall:
        return conjugate_transpose(self.observation_adjoint)


@dataclass(frozen=True)
class NodeEnclosures:
    """All balls entering one primal-dual contour-node certificate."""

    primal_residual: FrobeniusBall
    dual_residual: FrobeniusBall
    base_consistency: FrobeniusBall
    primal_increment: FrobeniusBall
    primal_correction: FrobeniusBall
    dual_weighted_correction: FrobeniusBall
    total_computed_correction: FrobeniusBall


class StoredFactorGraph:
    r"""Exact finite operator built from stored binary64 factors.

    With

    ``U=M-R Lambda L*`` and ``Q=I-VW``, the external operator and blocks are

    ``B=Q U^2 Q``, ``C=Q U^2 V``, ``D=W U^2 V``, and ``E=W U^2 Q``.

    The floating centres follow the same operation graph as RH-24--RH-26;
    every method additionally propagates a global Frobenius radius.
    """

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
        self.right = np.asarray(right_modes)
        self.left = np.asarray(left_modes)
        self.values = np.asarray(peripheral_values)
        self.synthesis = np.asarray(synthesis)
        self.analysis = np.asarray(analysis)
        dimension = self.matrix.shape[0]
        if self.matrix.shape != (dimension, dimension):
            raise ValueError("matrix must be square")
        if self.right.shape != self.left.shape or self.right.shape[0] != dimension:
            raise ValueError("peripheral modes have incompatible shapes")
        if self.values.shape != (self.right.shape[1],):
            raise ValueError("peripheral values have incompatible shape")
        if self.synthesis.shape[0] != dimension:
            raise ValueError("synthesis has incompatible dimension")
        if self.analysis.shape != (self.synthesis.shape[1], dimension):
            raise ValueError("analysis and synthesis have incompatible shapes")

        self.matrix_abs_norm = sparse_abs_operator_upper(self.matrix)
        self.maximum_row_nonzeros = int(np.max(np.diff(self.matrix.indptr)))
        self.maximum_column_nonzeros = int(
            np.max(np.diff(self.matrix_adjoint.indptr))
        )
        self._dense_norms = {
            "right": dense_abs_operator_upper(self.right),
            "left_t": dense_abs_operator_upper(self.left.T),
            "right_h": dense_abs_operator_upper(self.right.conj().T),
            "left_conj": dense_abs_operator_upper(self.left.conj()),
            "synthesis": dense_abs_operator_upper(self.synthesis),
            "analysis": dense_abs_operator_upper(self.analysis),
            "synthesis_h": dense_abs_operator_upper(self.synthesis.conj().T),
            "analysis_h": dense_abs_operator_upper(self.analysis.conj().T),
        }

    def _dense(self, name: str, operator: np.ndarray, ball: FrobeniusBall) -> FrobeniusBall:
        bound = self._dense_norms[name]
        result = dense_exact_matmul(
            operator,
            ball,
            abs_operator_upper=bound,
        )
        return result

    def packet(self, source: FrobeniusBall) -> FrobeniusBall:
        coefficients = self._dense("analysis", self.analysis, source)
        return self._dense("synthesis", self.synthesis, coefficients)

    def external(self, source: FrobeniusBall) -> FrobeniusBall:
        return subtract(source, self.packet(source))

    def external_adjoint(self, source: FrobeniusBall) -> FrobeniusBall:
        coefficients = self._dense(
            "synthesis_h", self.synthesis.conj().T, source
        )
        correction = self._dense(
            "analysis_h", self.analysis.conj().T, coefficients
        )
        return subtract(source, correction)

    def one_step(self, source: FrobeniusBall) -> FrobeniusBall:
        matrix_part = sparse_exact_matmul(
            self.matrix,
            source,
            abs_operator_upper=self.matrix_abs_norm,
            maximum_row_nonzeros=self.maximum_row_nonzeros,
        )
        coefficients = self._dense("left_t", self.left.T, source)
        weighted = scale_rows(self.values, coefficients)
        correction = self._dense("right", self.right, weighted)
        return subtract(matrix_part, correction)

    def one_step_adjoint(self, source: FrobeniusBall) -> FrobeniusBall:
        matrix_part = sparse_exact_matmul(
            self.matrix_adjoint,
            source,
            abs_operator_upper=self.matrix_abs_norm,
            maximum_row_nonzeros=self.maximum_column_nonzeros,
        )
        coefficients = self._dense("right_h", self.right.conj().T, source)
        weighted = scale_rows(self.values.conj(), coefficients)
        correction = self._dense("left_conj", self.left.conj(), weighted)
        return subtract(matrix_part, correction)

    def two_step(self, source: FrobeniusBall) -> FrobeniusBall:
        return self.one_step(self.one_step(source))

    def two_step_adjoint(self, source: FrobeniusBall) -> FrobeniusBall:
        return self.one_step_adjoint(self.one_step_adjoint(source))

    def external_action(self, source: FrobeniusBall) -> FrobeniusBall:
        return self.external(self.two_step(self.external(source)))

    def external_action_adjoint(self, source: FrobeniusBall) -> FrobeniusBall:
        return self.external_adjoint(
            self.two_step_adjoint(self.external_adjoint(source))
        )

    def build_blocks(self) -> StoredBlocks:
        trial = FrobeniusBall.exact(self.synthesis)
        returned = self.two_step(trial)
        direct = self._dense("analysis", self.analysis, returned)
        forcing = self.external(returned)
        observation_adjoint = self.external_adjoint(
            self.two_step_adjoint(FrobeniusBall.exact(self.analysis.conj().T))
        )
        return StoredBlocks(
            direct=direct,
            forcing=forcing,
            observation_adjoint=observation_adjoint,
        )

    def primal_residual(
        self,
        blocks: StoredBlocks,
        solution: np.ndarray,
        spectral_parameter: complex,
    ) -> FrobeniusBall:
        state = FrobeniusBall.exact(np.asarray(solution))
        shifted = subtract(
            scalar_multiply(spectral_parameter, state),
            self.external_action(state),
        )
        return subtract(blocks.forcing, shifted)

    def dual_residual(
        self,
        blocks: StoredBlocks,
        solution: np.ndarray,
        spectral_parameter: complex,
    ) -> FrobeniusBall:
        state = FrobeniusBall.exact(np.asarray(solution))
        shifted = subtract(
            scalar_multiply(np.conj(spectral_parameter), state),
            self.external_action_adjoint(state),
        )
        return subtract(blocks.observation_adjoint, shifted)

    def node_enclosures(
        self,
        blocks: StoredBlocks,
        spectral_parameter: complex,
        base_feshbach: np.ndarray,
        base_solution: np.ndarray,
        deep_solution: np.ndarray,
        dual_solution: np.ndarray,
    ) -> NodeEnclosures:
        zeta = complex(spectral_parameter)
        base_state = FrobeniusBall.exact(np.asarray(base_solution))
        deep_state = FrobeniusBall.exact(np.asarray(deep_solution))
        dual_state = FrobeniusBall.exact(np.asarray(dual_solution))
        primal_residual = self.primal_residual(blocks, deep_solution, zeta)
        dual_residual = self.dual_residual(blocks, dual_solution, zeta)
        increment = subtract(deep_state, base_state)
        observation = blocks.observation
        primal_correction = negate(matmul(observation, increment))
        dual_weighted = negate(
            matmul(conjugate_transpose(dual_state), primal_residual)
        )

        rank = self.synthesis.shape[1]
        spectral_identity = scalar_multiply(
            zeta, FrobeniusBall.exact(np.eye(rank, dtype=np.complex128))
        )
        ideal_base = subtract(
            subtract(spectral_identity, blocks.direct),
            matmul(observation, base_state),
        )
        consistency = subtract(
            ideal_base, FrobeniusBall.exact(np.asarray(base_feshbach))
        )
        computed = add(consistency, add(primal_correction, dual_weighted))
        return NodeEnclosures(
            primal_residual=primal_residual,
            dual_residual=dual_residual,
            base_consistency=consistency,
            primal_increment=increment,
            primal_correction=primal_correction,
            dual_weighted_correction=dual_weighted,
            total_computed_correction=computed,
        )

    def statistics(self) -> dict[str, float | int]:
        """Return sparsity and stored-number diagnostics for the graph."""

        arrays = [
            self.matrix.data,
            self.right,
            self.left,
            self.values,
            self.synthesis,
            self.analysis,
        ]
        nonzero = np.concatenate(
            [np.abs(np.asarray(item)).reshape(-1) for item in arrays]
        )
        nonzero = nonzero[nonzero > 0.0]
        tiny = np.finfo(np.float64).tiny
        row_sums = np.asarray(self.matrix.sum(axis=1)).reshape(-1)
        return {
            "dimension": int(self.matrix.shape[0]),
            "matrix_nonzeros": int(self.matrix.nnz),
            "maximum_row_nonzeros": self.maximum_row_nonzeros,
            "maximum_column_nonzeros": self.maximum_column_nonzeros,
            "minimum_nonzero_stored_magnitude": float(np.min(nonzero)),
            "subnormal_stored_count": int(np.count_nonzero(nonzero < tiny)),
            "matrix_abs_operator_upper": self.matrix_abs_norm,
            "maximum_row_sum_defect": float(np.max(np.abs(row_sums - 1.0))),
            "synthesis_frobenius_upper": frobenius_upper_array(self.synthesis),
            "analysis_frobenius_upper": frobenius_upper_array(self.analysis),
        }
