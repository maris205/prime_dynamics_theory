import numpy as np

from periodic_superloops import (
    HARDY_RADIUS,
    atomic_power_trace,
    closed_loop_sum,
    cloud_extracted_trace,
    folded_gaussian_kernel,
    folded_gaussian_matrix,
    graded_supertrace,
    matrix_power_trace,
)


def test_closed_loop_and_graded_counterloop_identities():
    raw = folded_gaussian_matrix(4, 0.08)
    scaled = raw / HARDY_RADIUS
    roots = np.linalg.eigvals(scaled)
    selected = roots[np.argsort(-np.abs(roots))[:3]]
    omitted = roots[np.argsort(-np.abs(roots))[3:]]
    for order in range(2, 6):
        direct = matrix_power_trace(scaled, order)
        loops = closed_loop_sum(scaled, order)
        residual = cloud_extracted_trace(scaled, selected, order)
        assert abs(direct - loops) < 2.0e-13
        assert abs(residual - graded_supertrace(scaled, selected, order)) < 1.0e-14
        assert abs(residual - atomic_power_trace(omitted, order)) < 2.0e-13


def test_folded_continuum_kernel_is_row_normalized():
    nodes, weights = np.polynomial.legendre.leggauss(256)
    destinations = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    for source in (0.05, 0.3, 0.7, 0.98):
        mass = np.dot(weights, folded_gaussian_kernel(source, destinations, 0.06))
        assert abs(mass - 1.0) < 2.0e-12
