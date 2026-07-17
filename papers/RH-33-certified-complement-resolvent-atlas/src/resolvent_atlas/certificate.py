"""All-column componentwise certificate for one direct complement inverse."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import time

import numpy as np
from scipy.sparse.linalg import splu


@dataclass(frozen=True)
class DirectInverseCertificate:
    center_inverse_two_norm_upper: float
    approximate_inverse_frobenius_upper: float
    residual_frobenius_upper: float
    residual_center_frobenius_upper: float
    residual_radius_frobenius_upper: float
    inverse_sha256: str
    residual_center_sha256: str
    residual_radius_sha256: str
    factor_nnz: int
    factor_seconds: float
    certificate_seconds: float
    admissible: bool


def certify_direct_inverse(
    system,
    graph,
    spectral_parameter: complex,
    *,
    chunk_size: int = 256,
) -> DirectInverseCertificate:
    """Certify the exact stored A(z)^-1 using an arbitrary sparse right inverse."""

    from outward_residuals import (
        ComponentwiseBall,
        componentwise_scalar_multiply,
        componentwise_subtract,
        frobenius_upper_array,
    )
    from sparse_grushin import combine_frobenius_bounds, neumann_inverse_certificate

    factor_started = time.perf_counter()
    factor = splu(
        system.matrix,
        permc_spec="COLAMD",
        diag_pivot_thresh=1.0,
        options={"Equil": False, "IterRefine": "DOUBLE"},
    )
    factor_seconds = time.perf_counter() - factor_started
    dimension = int(system.physical_dimension)
    total_dimension = int(system.bordered_dimension)
    inverse_bounds: list[float] = []
    residual_bounds: list[float] = []
    residual_center_bounds: list[float] = []
    residual_radius_bounds: list[float] = []
    inverse_hash = hashlib.sha256()
    center_hash = hashlib.sha256()
    radius_hash = hashlib.sha256()
    certificate_started = time.perf_counter()
    for start in range(0, dimension, int(chunk_size)):
        stop = min(start + int(chunk_size), dimension)
        width = stop - start
        source = np.zeros((total_dimension, width), dtype=np.complex128)
        source[np.arange(start, stop), np.arange(width)] = 1.0
        solution = factor.solve(source)
        approximate = np.ascontiguousarray(solution[:dimension, :])
        inverse_hash.update(approximate.view(np.uint8))
        inverse_bounds.append(frobenius_upper_array(approximate))

        approximate_ball = ComponentwiseBall.exact(approximate)
        shifted = componentwise_subtract(
            componentwise_scalar_multiply(spectral_parameter, approximate_ball),
            graph.action(approximate_ball),
        )
        identity = np.zeros((dimension, width), dtype=np.complex128)
        identity[np.arange(start, stop), np.arange(width)] = 1.0
        residual = componentwise_subtract(
            ComponentwiseBall.exact(identity), shifted
        )
        center = np.ascontiguousarray(residual.center)
        radius = np.ascontiguousarray(residual.radius)
        center_hash.update(center.view(np.uint8))
        radius_hash.update(radius.view(np.uint8))
        residual_bounds.append(residual.norm_upper)
        residual_center_bounds.append(frobenius_upper_array(center))
        residual_radius_bounds.append(frobenius_upper_array(radius))
        print(
            f"  certified columns {stop}/{dimension}: "
            f"R_F={inverse_bounds[-1]:.3e}, E_F={residual_bounds[-1]:.3e}",
            flush=True,
        )
    approximate_upper = combine_frobenius_bounds(inverse_bounds)
    residual_upper = combine_frobenius_bounds(residual_bounds)
    center_upper = combine_frobenius_bounds(residual_center_bounds)
    radius_upper = combine_frobenius_bounds(residual_radius_bounds)
    certificate = neumann_inverse_certificate(approximate_upper, residual_upper)
    return DirectInverseCertificate(
        center_inverse_two_norm_upper=certificate.inverse_two_norm_upper,
        approximate_inverse_frobenius_upper=approximate_upper,
        residual_frobenius_upper=residual_upper,
        residual_center_frobenius_upper=center_upper,
        residual_radius_frobenius_upper=radius_upper,
        inverse_sha256=inverse_hash.hexdigest(),
        residual_center_sha256=center_hash.hexdigest(),
        residual_radius_sha256=radius_hash.hexdigest(),
        factor_nnz=int(factor.L.nnz + factor.U.nnz),
        factor_seconds=factor_seconds,
        certificate_seconds=time.perf_counter() - certificate_started,
        admissible=certificate.admissible,
    )
