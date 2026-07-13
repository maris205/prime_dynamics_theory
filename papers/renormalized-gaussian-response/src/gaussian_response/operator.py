"""Gaussian-smoothed quadratic transfer matrices and exact derivatives.

The matrix is row stochastic.  Its action on a column vector represents the
conditional expectation of an observable at the next step.  Sparse matrices
use a support pattern fixed at ``u_ref`` so that finite differences and
parameter derivatives do not acquire artificial cutoff discontinuities.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Iterable

import numpy as np
import scipy.sparse as sp


def grid_centers(d: int) -> np.ndarray:
    """Return midpoint centers of the uniform partition of [-1, 1]."""
    if d < 2:
        raise ValueError("d must be at least 2")
    h = 2.0 / d
    return -1.0 + h * (np.arange(d, dtype=np.float64) + 0.5)


def _validate_orders(orders: Iterable[int]) -> tuple[int, ...]:
    result = tuple(dict.fromkeys(int(order) for order in orders))
    if not result or any(order not in (0, 1, 2) for order in result):
        raise ValueError("orders must be a nonempty subset of (0, 1, 2)")
    return result


@dataclass(frozen=True)
class BuildStats:
    d: int
    nnz: int
    density: float
    elapsed_seconds: float
    bytes_per_matrix: int


class FixedSupportGaussianFamily:
    """Sparse Gaussian family on a support pattern fixed near ``u_ref``.

    Parameters
    ----------
    d:
        Number of uniform grid cells.
    sigma:
        Physical Gaussian width.
    u_ref:
        Parameter at which row supports are centered.
    cutoff:
        Number of Gaussian widths retained on each side.  ``None`` builds the
        full dense support in CSR form.
    parameter_radius:
        The support is padded by ``parameter_radius * c_i**2`` in row ``i``.
        It therefore contains the cutoff window for every
        ``abs(u-u_ref) <= parameter_radius``.
    """

    def __init__(
        self,
        d: int,
        sigma: float,
        u_ref: float,
        cutoff: float | None = 6.0,
        parameter_radius: float = 0.0,
    ) -> None:
        if sigma <= 0.0:
            raise ValueError("sigma must be positive")
        if cutoff is not None and cutoff <= 0.0:
            raise ValueError("cutoff must be positive or None")
        if parameter_radius < 0.0:
            raise ValueError("parameter_radius must be nonnegative")

        self.d = int(d)
        self.sigma = float(sigma)
        self.u_ref = float(u_ref)
        self.cutoff = None if cutoff is None else float(cutoff)
        self.parameter_radius = float(parameter_radius)
        self.centers = grid_centers(self.d)
        self.h = 2.0 / self.d
        self._c2 = self.centers * self.centers
        self._lo, self._hi, self.indptr, self.indices = self._build_support()

    def _build_support(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        if self.cutoff is None:
            lo = np.zeros(self.d, dtype=np.int64)
            hi = np.full(self.d, self.d, dtype=np.int64)
        else:
            means = 1.0 - self.u_ref * self._c2
            radii = self.cutoff * self.sigma + self.parameter_radius * self._c2
            lo = np.searchsorted(self.centers, means - radii, side="left")
            hi = np.searchsorted(self.centers, means + radii, side="right")
            lo = np.clip(lo, 0, self.d).astype(np.int64, copy=False)
            hi = np.clip(hi, 0, self.d).astype(np.int64, copy=False)

            empty = hi <= lo
            if np.any(empty):
                nearest = np.rint((means[empty] + 1.0) / self.h - 0.5).astype(np.int64)
                nearest = np.clip(nearest, 0, self.d - 1)
                lo[empty] = nearest
                hi[empty] = nearest + 1

        lengths = hi - lo
        indptr = np.empty(self.d + 1, dtype=np.int64)
        indptr[0] = 0
        np.cumsum(lengths, out=indptr[1:])
        indices = np.empty(int(indptr[-1]), dtype=np.int32)
        for i in range(self.d):
            start, end = int(indptr[i]), int(indptr[i + 1])
            indices[start:end] = np.arange(lo[i], hi[i], dtype=np.int32)
        return lo, hi, indptr, indices

    @property
    def nnz(self) -> int:
        return int(self.indptr[-1])

    def support_covers(self, u: float) -> bool:
        """Whether padding was declared large enough for the requested value."""
        return abs(float(u) - self.u_ref) <= self.parameter_radius + 8.0 * np.finfo(float).eps

    def matrices(
        self,
        u: float,
        orders: Iterable[int] = (0, 1, 2),
    ) -> tuple[sp.csr_matrix, ...]:
        """Build selected derivative orders using the exact softmax formulas."""
        requested = _validate_orders(orders)
        data = {order: np.empty(self.nnz, dtype=np.float64) for order in requested}
        sigma2 = self.sigma * self.sigma
        u = float(u)

        for i in range(self.d):
            start, end = int(self.indptr[i]), int(self.indptr[i + 1])
            cols = self.indices[start:end]
            z = self.centers[cols] - (1.0 - u * self._c2[i])
            log_weights = -(z * z) / (2.0 * sigma2)
            log_weights -= np.max(log_weights)
            weights = np.exp(log_weights)
            probabilities = weights / np.sum(weights)

            if 0 in data:
                data[0][start:end] = probabilities

            if 1 in data or 2 in data:
                score = -self._c2[i] * z / sigma2
                centered_score = score - np.dot(probabilities, score)
                if 1 in data:
                    data[1][start:end] = probabilities * centered_score
                if 2 in data:
                    variance = np.dot(probabilities, centered_score * centered_score)
                    data[2][start:end] = probabilities * (
                        centered_score * centered_score - variance
                    )

        shape = (self.d, self.d)
        return tuple(
            sp.csr_matrix(
                (data[order], self.indices, self.indptr),
                shape=shape,
                copy=False,
            )
            for order in requested
        )

    def matrix(self, u: float, order: int = 0) -> sp.csr_matrix:
        return self.matrices(u, (order,))[0]

    def build_with_stats(
        self,
        u: float,
        orders: Iterable[int] = (0, 1, 2),
    ) -> tuple[tuple[sp.csr_matrix, ...], BuildStats]:
        start = perf_counter()
        matrices = self.matrices(u, orders)
        elapsed = perf_counter() - start
        first = matrices[0]
        byte_count = first.data.nbytes + first.indices.nbytes + first.indptr.nbytes
        stats = BuildStats(
            d=self.d,
            nnz=self.nnz,
            density=self.nnz / float(self.d * self.d),
            elapsed_seconds=elapsed,
            bytes_per_matrix=byte_count,
        )
        return matrices, stats

    def tail_mass_diagnostic(self, u: float, reference_cutoff: float = 12.0) -> dict[str, float]:
        """Estimate omitted row mass against a wider Gaussian window.

        A 12-sigma reference leaves a continuous Gaussian tail below machine
        precision.  The returned quantity is a numerical diagnostic; the exact
        rowwise identity is ``||K_full-K_cut||_1 = 2*q_i`` where ``q_i`` is the
        full omitted probability.
        """
        if self.cutoff is None:
            return {"maximum_omitted_mass": 0.0, "maximum_l1_error": 0.0}
        if reference_cutoff <= self.cutoff:
            raise ValueError("reference_cutoff must exceed the support cutoff")

        sigma2 = self.sigma * self.sigma
        maximum = 0.0
        for i in range(self.d):
            mean = 1.0 - float(u) * self._c2[i]
            lo = int(np.searchsorted(self.centers, mean - reference_cutoff * self.sigma))
            hi = int(np.searchsorted(self.centers, mean + reference_cutoff * self.sigma, side="right"))
            lo = max(0, lo)
            hi = min(self.d, hi)
            cols = np.arange(lo, hi, dtype=np.int64)
            z = self.centers[cols] - mean
            log_weights = -(z * z) / (2.0 * sigma2)
            log_weights -= np.max(log_weights)
            weights = np.exp(log_weights)
            retained = (cols >= self._lo[i]) & (cols < self._hi[i])
            omitted = 1.0 - float(np.sum(weights[retained]) / np.sum(weights))
            maximum = max(maximum, omitted)
        return {
            "maximum_omitted_mass": maximum,
            "maximum_l1_error": 2.0 * maximum,
        }


def dense_gaussian_matrices(
    d: int,
    sigma: float,
    u: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Dense reference implementation of K, K', and K''."""
    centers = grid_centers(d)
    c2 = centers * centers
    means = 1.0 - float(u) * c2
    z = centers[np.newaxis, :] - means[:, np.newaxis]
    log_weights = -(z * z) / (2.0 * sigma * sigma)
    log_weights -= np.max(log_weights, axis=1, keepdims=True)
    weights = np.exp(log_weights)
    kernel = weights / np.sum(weights, axis=1, keepdims=True)

    score = -c2[:, np.newaxis] * z / (sigma * sigma)
    mean_score = np.sum(kernel * score, axis=1, keepdims=True)
    centered_score = score - mean_score
    variance = np.sum(kernel * centered_score * centered_score, axis=1, keepdims=True)
    first = kernel * centered_score
    second = kernel * (centered_score * centered_score - variance)
    return kernel, first, second
