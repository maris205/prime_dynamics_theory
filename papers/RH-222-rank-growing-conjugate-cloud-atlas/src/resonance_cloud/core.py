"""Shell-complete spectral clouds for the folded Gaussian operator."""

from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs


HARDY_RADIUS = 0.85


@dataclass(frozen=True)
class BulkResolution:
    perron: complex
    parity: complex
    bulk: np.ndarray
    full_frobenius_squared: float


def deterministic_start(dimension: int) -> np.ndarray:
    index = np.arange(int(dimension), dtype=float)
    vector = np.sin((index + 0.5) * math.sqrt(2.0))
    vector += 0.37 * np.cos((index + 0.5) * math.sqrt(3.0))
    return vector / np.linalg.norm(vector)


def haar_coarse_embedding(dimension: int) -> sparse.csr_matrix:
    size = int(dimension)
    if size < 4 or size % 2:
        raise ValueError("an even dimension at least four is required")
    rows = np.arange(size)
    columns = np.repeat(np.arange(size // 2), 2)
    data = np.full(size, 1.0 / math.sqrt(2.0))
    return sparse.coo_matrix(
        (data, (rows, columns)), shape=(size, size // 2)
    ).tocsr()


def resolve_bulk(
    matrix: sparse.spmatrix,
    candidate_count: int,
    *,
    hardy_radius: float = HARDY_RADIUS,
) -> BulkResolution:
    """Resolve leading eigenvalues, remove Perron/parity, and Hardy-scale."""

    operator = sparse.csr_matrix(matrix, dtype=float)
    if operator.shape[0] != operator.shape[1]:
        raise ValueError("a square operator is required")
    radius = float(hardy_radius)
    if not 0.0 < radius < 1.0:
        raise ValueError("the Hardy radius must lie in (0,1)")
    count = min(int(candidate_count), operator.shape[0] - 2)
    if count < 8:
        raise ValueError("at least eight candidate eigenvalues are required")
    values = eigs(
        operator,
        k=count,
        which="LM",
        return_eigenvectors=False,
        tol=3.0e-11,
        maxiter=max(20000, 40 * operator.shape[0]),
        ncv=min(operator.shape[0], max(2 * count + 1, 48)),
        v0=deterministic_start(operator.shape[0]),
    )
    values = np.asarray(values, dtype=complex)
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    available = [index for index in range(values.size) if index != perron_index]
    negative_real = [
        index
        for index in available
        if abs(values[index].imag) <= 2.0e-8 and values[index].real < -1.0e-8
    ]
    if not negative_real:
        raise RuntimeError("the negative parity resonance was not resolved")
    parity_index = min(negative_real, key=lambda index: values[index].real)
    bulk = np.delete(values, (perron_index, parity_index)) / radius
    bulk = bulk[np.argsort(-np.abs(bulk))]
    frobenius_squared = float(operator.multiply(operator).sum()) / radius**2
    return BulkResolution(
        perron=complex(values[perron_index] / radius),
        parity=complex(values[parity_index] / radius),
        bulk=bulk,
        full_frobenius_squared=frobenius_squared,
    )


def conjugate_shells(
    values: np.ndarray,
    *,
    real_tolerance: float = 2.0e-8,
    pair_tolerance: float = 2.0e-7,
) -> list[np.ndarray]:
    """Partition a resolved real-operator spectrum into real or conjugate shells."""

    roots = np.asarray(values, dtype=complex).reshape(-1)
    unused = set(range(roots.size))
    shells: list[np.ndarray] = []
    for index in np.argsort(-np.abs(roots)):
        current = int(index)
        if current not in unused:
            continue
        value = roots[current]
        unused.remove(current)
        if abs(value.imag) <= float(real_tolerance):
            shells.append(np.asarray([complex(value.real, 0.0)]))
            continue
        if not unused:
            continue
        partner = min(unused, key=lambda candidate: abs(roots[candidate] - np.conj(value)))
        error = abs(roots[partner] - np.conj(value))
        scale = max(1.0, abs(value), abs(roots[partner]))
        if error > float(pair_tolerance) * scale:
            continue
        unused.remove(partner)
        pair = np.asarray([value, roots[partner]], dtype=complex)
        pair = pair[np.argsort(-pair.imag)]
        shells.append(pair)
    shells.sort(key=lambda shell: -float(np.max(np.abs(shell))))
    return shells


def select_shell_complete_cloud(
    shells: list[np.ndarray], target_rank: int
) -> tuple[np.ndarray, list[np.ndarray]]:
    target = int(target_rank)
    if target < 1:
        raise ValueError("target rank must be positive")
    selected: list[np.ndarray] = []
    count = 0
    for shell in shells:
        selected.append(np.asarray(shell, dtype=complex))
        count += int(np.asarray(shell).size)
        if count >= target:
            break
    if count < target:
        raise RuntimeError("the resolved candidate cloud is too small")
    return np.concatenate(selected), selected


def conjugacy_error(values: np.ndarray) -> float:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    return float(max(np.min(np.abs(roots - np.conj(value))) for value in roots))


def cloud_gauge(values: np.ndarray) -> dict[str, complex | float | np.ndarray]:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    if roots.size < 2:
        raise ValueError("at least two roots are required")
    center = complex(np.mean(roots))
    centered = roots - center
    radius = float(np.sqrt(np.mean(np.abs(centered) ** 2)))
    if radius <= np.finfo(float).tiny:
        raise ValueError("the cloud RMS radius is zero")
    normalized = centered / radius
    return {"center": center, "radius": radius, "normalized": normalized}


def shell_gap(shells: list[np.ndarray], selected_shell_count: int) -> float:
    count = int(selected_shell_count)
    if count < 1 or count > len(shells):
        raise ValueError("invalid selected shell count")
    if count == len(shells):
        return float("inf")
    inner_selected = min(abs(value) for shell in shells[:count] for value in shell)
    outer_omitted = max(abs(value) for value in shells[count])
    return float(inner_selected - outer_omitted)


def reciprocal_zeros(values: np.ndarray) -> np.ndarray:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    if np.min(np.abs(roots)) <= np.finfo(float).tiny:
        raise ValueError("zero resonances have no finite reciprocal zero")
    return 1.0 / roots


def complex_payload(values: np.ndarray) -> dict[str, list[float]]:
    roots = np.asarray(values, dtype=complex).reshape(-1)
    return {
        "real": [float(value.real) for value in roots],
        "imag": [float(value.imag) for value in roots],
    }
