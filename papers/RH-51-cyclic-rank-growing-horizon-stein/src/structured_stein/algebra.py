"""Finite-dimensional algebra for RH-51 structured Stein certificates.

The operator passed to this module is already the scaled bulk operator
``A=N/r``.  Thus its controllability Gramian solves

    G - A G A^* = X X^*.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


def _square_matrix(operator: np.ndarray) -> np.ndarray:
    value = np.asarray(operator, dtype=np.complex128)
    if value.ndim != 2 or value.shape[0] != value.shape[1]:
        raise ValueError("operator must be square")
    return value


def _source_matrix(source: np.ndarray, dimension: int) -> np.ndarray:
    value = np.asarray(source, dtype=np.complex128)
    if value.ndim == 1:
        value = value[:, None]
    if value.ndim != 2 or value.shape[0] != dimension:
        raise ValueError("source has incompatible shape")
    return value


def _hermitian(value: np.ndarray) -> np.ndarray:
    return 0.5 * (value + value.conjugate().T)


def _positive_horizon(horizon: int) -> int:
    value = int(horizon)
    if value < 1:
        raise ValueError("horizon must be positive")
    return value


def finite_horizon_gramian(
    operator: np.ndarray, source: np.ndarray, horizon: int
) -> np.ndarray:
    r"""Return ``sum_(j=0)^(M-1) A^j X X^* (A^*)^j``."""

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    count = _positive_horizon(horizon)
    state = x.copy()
    result = np.zeros_like(a)
    for _ in range(count):
        result += state @ state.conjugate().T
        state = a @ state
    return _hermitian(result)


def controllability_gramian(
    operator: np.ndarray, source: np.ndarray
) -> np.ndarray:
    r"""Solve ``G-A G A^*=X X^*`` for a stable finite matrix."""

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    return _hermitian(
        solve_discrete_lyapunov(a, x @ x.conjugate().T)
    )


def observability_gramian(
    operator: np.ndarray, observation: np.ndarray
) -> np.ndarray:
    r"""Solve ``O-A^* O A=Y^*Y`` for a stable finite matrix."""

    a = _square_matrix(operator)
    y = np.asarray(observation, dtype=np.complex128)
    if y.ndim == 1:
        y = y[None, :]
    if y.ndim != 2 or y.shape[1] != a.shape[0]:
        raise ValueError("observation has incompatible shape")
    return _hermitian(
        solve_discrete_lyapunov(
            a.conjugate().T, y.conjugate().T @ y
        )
    )


def stein_defect(
    operator: np.ndarray, candidate: np.ndarray, source: np.ndarray
) -> np.ndarray:
    r"""Return ``H-A H A^*-X X^*``."""

    a = _square_matrix(operator)
    h = np.asarray(candidate, dtype=np.complex128)
    x = _source_matrix(source, a.shape[0])
    if h.shape != a.shape:
        raise ValueError("candidate has incompatible shape")
    return _hermitian(h - a @ h @ a.conjugate().T - x @ x.conjugate().T)


def block_stein_defect(
    operator: np.ndarray,
    candidate: np.ndarray,
    source: np.ndarray,
    horizon: int,
) -> np.ndarray:
    r"""Return ``H-A^M H(A^*)^M-S_M``."""

    a = _square_matrix(operator)
    h = np.asarray(candidate, dtype=np.complex128)
    x = _source_matrix(source, a.shape[0])
    count = _positive_horizon(horizon)
    if h.shape != a.shape:
        raise ValueError("candidate has incompatible shape")
    power = np.linalg.matrix_power(a, count)
    partial = finite_horizon_gramian(a, x, count)
    return _hermitian(
        h - power @ h @ power.conjugate().T - partial
    )


@dataclass(frozen=True)
class GramianSpectrum:
    """Eigenvalue-based complexity ledger for a positive Gramian."""

    eigenvalues: np.ndarray
    trace: float
    participation_rank: float
    rank_for_99_percent_trace: int
    numerical_rank: int


def gramian_spectrum(
    gramian: np.ndarray, *, relative_tolerance: float = 1.0e-12
) -> GramianSpectrum:
    """Return descending eigenvalues and standard effective-rank summaries."""

    g = _square_matrix(gramian)
    tolerance = float(relative_tolerance)
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("relative_tolerance must be positive")
    eigenvalues = np.linalg.eigvalsh(_hermitian(g)).real[::-1]
    scale = max(float(eigenvalues[0]), 0.0) if eigenvalues.size else 0.0
    clipped = np.maximum(eigenvalues, 0.0)
    total = float(np.sum(clipped))
    square_total = float(np.dot(clipped, clipped))
    participation = total * total / square_total if square_total > 0.0 else 0.0
    if total > 0.0:
        rank99 = int(np.searchsorted(np.cumsum(clipped), 0.99 * total) + 1)
    else:
        rank99 = 0
    numerical_rank = int(np.count_nonzero(clipped > tolerance * scale))
    return GramianSpectrum(
        eigenvalues=clipped,
        trace=total,
        participation_rank=float(participation),
        rank_for_99_percent_trace=rank99,
        numerical_rank=numerical_rank,
    )


def cyclic_rank_profile(
    operator: np.ndarray,
    source: np.ndarray,
    maximum_power: int,
    *,
    relative_tolerance: float = 1.0e-10,
) -> list[dict[str, float | int]]:
    r"""Numerically rank ``[X,AX,...,A^mX]`` for ``m=0,...,maximum_power``.

    The reported rank is explicitly floating and threshold dependent; the
    exact theorem uses the algebraic dimension of the same cyclic span.
    """

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    last = int(maximum_power)
    tolerance = float(relative_tolerance)
    if last < 0:
        raise ValueError("maximum_power must be nonnegative")
    if not math.isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("relative_tolerance must be positive")
    blocks = []
    state = x.copy()
    rows: list[dict[str, float | int]] = []
    for power in range(last + 1):
        blocks.append(state)
        krylov = np.concatenate(blocks, axis=1)
        singular = np.linalg.svd(krylov, compute_uv=False)
        scale = float(singular[0]) if singular.size else 0.0
        rank = int(np.count_nonzero(singular > tolerance * scale))
        rows.append(
            {
                "maximum_power": power,
                "block_count": power + 1,
                "numerical_rank": rank,
                "rank_fraction": rank / a.shape[0],
                "largest_singular_value": scale,
                "smallest_retained_singular_value": (
                    float(singular[rank - 1]) if rank else 0.0
                ),
            }
        )
        state = a @ state
    return rows


@dataclass(frozen=True)
class SupersolutionAudit:
    """Floating audit of one positive Stein supersolution."""

    positive_minimum_eigenvalue: float
    defect_minimum_eigenvalue: float
    dominates_exact_gramian_minimum_eigenvalue: float
    admissible: bool


def supersolution_audit(
    operator: np.ndarray,
    source: np.ndarray,
    candidate: np.ndarray,
    *,
    tolerance: float = 1.0e-10,
) -> SupersolutionAudit:
    """Check positivity, the Stein defect, and domination of the Gramian."""

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    h = _hermitian(np.asarray(candidate, dtype=np.complex128))
    if h.shape != a.shape:
        raise ValueError("candidate has incompatible shape")
    exact = controllability_gramian(a, x)
    positive = float(np.min(np.linalg.eigvalsh(h)).real)
    defect = float(np.min(np.linalg.eigvalsh(stein_defect(a, h, x))).real)
    domination = float(np.min(np.linalg.eigvalsh(_hermitian(h - exact))).real)
    tol = float(tolerance)
    return SupersolutionAudit(
        positive_minimum_eigenvalue=positive,
        defect_minimum_eigenvalue=defect,
        dominates_exact_gramian_minimum_eigenvalue=domination,
        admissible=(positive >= -tol and defect >= -tol and domination >= -tol),
    )


@dataclass(frozen=True)
class BlockCompletion:
    """Finite-horizon Gramian plus an isotropic rigorous tail floor."""

    horizon: int
    power_norm: float
    contraction_margin: float
    tail_residual_norm: float
    isotropic_floor: float
    candidate: np.ndarray
    block_defect_minimum_eigenvalue: float


def isotropic_block_completion(
    operator: np.ndarray, source: np.ndarray, horizon: int
) -> BlockCompletion:
    r"""Construct ``H=S_M+alpha I`` from one contracting block power.

    If ``q=||A^M||_2<1``, then

    ``alpha=||A^M S_M (A^*)^M||_2/(1-q^2)``

    makes ``H-A^M H(A^*)^M >= S_M``.  The construction is exact in exact
    arithmetic; the returned eigenvalue is a binary64 audit.
    """

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    count = _positive_horizon(horizon)
    partial = finite_horizon_gramian(a, x, count)
    power = np.linalg.matrix_power(a, count)
    q = float(np.linalg.norm(power, 2))
    margin = 1.0 - q * q
    if margin <= 0.0:
        raise ValueError("selected block power is not a Euclidean contraction")
    tail_residual = _hermitian(
        power @ partial @ power.conjugate().T
    )
    residual_norm = float(np.linalg.norm(tail_residual, 2))
    alpha = residual_norm / margin
    candidate = _hermitian(partial + alpha * np.eye(a.shape[0]))
    defect = block_stein_defect(a, candidate, x, count)
    minimum = float(np.min(np.linalg.eigvalsh(defect)).real)
    return BlockCompletion(
        horizon=count,
        power_norm=q,
        contraction_margin=margin,
        tail_residual_norm=residual_norm,
        isotropic_floor=alpha,
        candidate=candidate,
        block_defect_minimum_eigenvalue=minimum,
    )


def low_rank_isotropic_floor(gramian: np.ndarray, rank: int) -> float:
    r"""Necessary ``alpha`` for ``Z Z^*+alpha I >= G`` with ``rank(Z)<=k``."""

    g = _square_matrix(gramian)
    k = int(rank)
    if k < 0:
        raise ValueError("rank must be nonnegative")
    if k >= g.shape[0]:
        return 0.0
    values = np.linalg.eigvalsh(_hermitian(g)).real[::-1]
    return float(max(values[k], 0.0))


@dataclass(frozen=True)
class ConicWitness:
    """Rank-one dual witness against a finitely generated metric cone."""

    generator_quadratic_forms: tuple[float, ...]
    source_quadratic_form: float
    obstructs_cone: bool


def conic_vector_witness(
    operator: np.ndarray,
    source: np.ndarray,
    generators: Iterable[np.ndarray],
    vector: np.ndarray,
    *,
    tolerance: float = 1.0e-12,
) -> ConicWitness:
    r"""Audit the rank-one dual obstruction for ``H=sum h_j W_j``.

    If every ``v^*(W_j-AW_jA^*)v`` is nonpositive while
    ``v^*XX^*v`` is positive, no nonnegative conic combination can be a
    Stein supersolution.
    """

    a = _square_matrix(operator)
    x = _source_matrix(source, a.shape[0])
    v = np.asarray(vector, dtype=np.complex128).reshape(-1)
    if v.shape != (a.shape[0],):
        raise ValueError("vector has incompatible shape")
    norm = float(np.linalg.norm(v))
    if norm == 0.0:
        raise ValueError("vector must be nonzero")
    v = v / norm
    forms = []
    for generator in generators:
        w = np.asarray(generator, dtype=np.complex128)
        if w.shape != a.shape:
            raise ValueError("generator has incompatible shape")
        defect = _hermitian(w - a @ w @ a.conjugate().T)
        forms.append(float(np.vdot(v, defect @ v).real))
    source_form = float(np.linalg.norm(x.conjugate().T @ v) ** 2)
    tol = float(tolerance)
    return ConicWitness(
        generator_quadratic_forms=tuple(forms),
        source_quadratic_form=source_form,
        obstructs_cone=(all(value <= tol for value in forms) and source_form > tol),
    )
