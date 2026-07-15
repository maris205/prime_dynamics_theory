"""Independent 80-bit reevaluation of the stored-factor graph.

This module is a diagnostic, not part of the proof layer.  It casts every
stored binary64 factor to the platform long-double type and reevaluates the
same graph with explicit CSR row reductions.  On x86-64 this supplies a
63-bit significand, ten bits beyond binary64, and is useful for checking how
much of each outward radius is actually consumed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.sparse import csr_matrix

from .enclosures import FrobeniusBall


LD = np.longdouble
CLD = np.clongdouble


def longdouble_frobenius(values: np.ndarray) -> np.longdouble:
    """Return a scaled long-double Frobenius norm."""

    array = np.asarray(values, dtype=CLD)
    magnitudes = np.abs(array).astype(LD, copy=False).reshape(-1)
    if magnitudes.size == 0:
        return LD(0.0)
    scale = np.max(magnitudes)
    if scale == 0.0:
        return LD(0.0)
    return scale * np.sqrt(
        np.sum((magnitudes / scale) ** 2, dtype=LD), dtype=LD
    )


def ball_utilization(reference: np.ndarray, ball: FrobeniusBall) -> float:
    """Fraction of a global Frobenius radius consumed by an 80-bit value."""

    difference = np.asarray(reference, dtype=CLD) - np.asarray(
        ball.center, dtype=CLD
    )
    defect = float(longdouble_frobenius(difference))
    if ball.radius == 0.0:
        return 0.0 if defect == 0.0 else float("inf")
    return float(defect / ball.radius)


@dataclass(frozen=True)
class LongDoubleBlocks:
    direct: np.ndarray
    forcing: np.ndarray
    observation_adjoint: np.ndarray


@dataclass(frozen=True)
class LongDoubleNode:
    primal_residual: np.ndarray
    dual_residual: np.ndarray
    base_consistency: np.ndarray
    primal_increment: np.ndarray
    primal_correction: np.ndarray
    dual_weighted_correction: np.ndarray
    total_computed_correction: np.ndarray


class LongDoubleFactorGraph:
    """Long-double counterpart of :class:`StoredFactorGraph`."""

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
        self.right = np.asarray(right_modes, dtype=CLD)
        self.left = np.asarray(left_modes, dtype=CLD)
        self.values = np.asarray(peripheral_values, dtype=CLD)
        self.synthesis = np.asarray(synthesis, dtype=CLD)
        self.analysis = np.asarray(analysis, dtype=CLD)

    @staticmethod
    def _sparse_apply(matrix: csr_matrix, source: np.ndarray) -> np.ndarray:
        sparse = matrix.tocsr(copy=False)
        values = np.asarray(source, dtype=CLD)
        was_vector = values.ndim == 1
        if was_vector:
            values = values[:, None]
        result = np.zeros((sparse.shape[0], values.shape[1]), dtype=CLD)
        data = np.asarray(sparse.data, dtype=CLD)
        for row in range(sparse.shape[0]):
            start = int(sparse.indptr[row])
            stop = int(sparse.indptr[row + 1])
            if start != stop:
                products = data[start:stop, None] * values[
                    sparse.indices[start:stop], :
                ]
                result[row, :] = np.sum(products, axis=0, dtype=CLD)
        return result[:, 0] if was_vector else result

    def external(self, source: np.ndarray) -> np.ndarray:
        values = np.asarray(source, dtype=CLD)
        return values - self.synthesis @ (self.analysis @ values)

    def external_adjoint(self, source: np.ndarray) -> np.ndarray:
        values = np.asarray(source, dtype=CLD)
        return values - self.analysis.conj().T @ (
            self.synthesis.conj().T @ values
        )

    def one_step(self, source: np.ndarray) -> np.ndarray:
        values = np.asarray(source, dtype=CLD)
        coefficients = self.left.T @ values
        if values.ndim == 1:
            correction = self.right @ (self.values * coefficients)
        else:
            correction = self.right @ (self.values[:, None] * coefficients)
        return self._sparse_apply(self.matrix, values) - correction

    def one_step_adjoint(self, source: np.ndarray) -> np.ndarray:
        values = np.asarray(source, dtype=CLD)
        coefficients = self.right.conj().T @ values
        if values.ndim == 1:
            correction = self.left.conj() @ (
                self.values.conj() * coefficients
            )
        else:
            correction = self.left.conj() @ (
                self.values.conj()[:, None] * coefficients
            )
        return self._sparse_apply(self.matrix_adjoint, values) - correction

    def two_step(self, source: np.ndarray) -> np.ndarray:
        return self.one_step(self.one_step(source))

    def two_step_adjoint(self, source: np.ndarray) -> np.ndarray:
        return self.one_step_adjoint(self.one_step_adjoint(source))

    def action(self, source: np.ndarray) -> np.ndarray:
        return self.external(self.two_step(self.external(source)))

    def action_adjoint(self, source: np.ndarray) -> np.ndarray:
        return self.external_adjoint(
            self.two_step_adjoint(self.external_adjoint(source))
        )

    def build_blocks(self) -> LongDoubleBlocks:
        returned = self.two_step(self.synthesis)
        return LongDoubleBlocks(
            direct=self.analysis @ returned,
            forcing=self.external(returned),
            observation_adjoint=self.external_adjoint(
                self.two_step_adjoint(self.analysis.conj().T)
            ),
        )

    def node(
        self,
        blocks: LongDoubleBlocks,
        spectral_parameter: complex,
        base_feshbach: np.ndarray,
        base_solution: np.ndarray,
        deep_solution: np.ndarray,
        dual_solution: np.ndarray,
    ) -> LongDoubleNode:
        zeta = CLD(spectral_parameter)
        base = np.asarray(base_solution, dtype=CLD)
        deep = np.asarray(deep_solution, dtype=CLD)
        dual = np.asarray(dual_solution, dtype=CLD)
        observation = blocks.observation_adjoint.conj().T
        primal_residual = blocks.forcing - (
            zeta * deep - self.action(deep)
        )
        dual_residual = blocks.observation_adjoint - (
            np.conj(zeta) * dual - self.action_adjoint(dual)
        )
        increment = deep - base
        primal_correction = -observation @ increment
        dual_weighted = -dual.conj().T @ primal_residual
        rank = self.synthesis.shape[1]
        ideal_base = (
            zeta * np.eye(rank, dtype=CLD)
            - blocks.direct
            - observation @ base
        )
        consistency = ideal_base - np.asarray(base_feshbach, dtype=CLD)
        total = consistency + primal_correction + dual_weighted
        return LongDoubleNode(
            primal_residual=primal_residual,
            dual_residual=dual_residual,
            base_consistency=consistency,
            primal_increment=increment,
            primal_correction=primal_correction,
            dual_weighted_correction=dual_weighted,
            total_computed_correction=total,
        )
