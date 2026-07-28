import numpy as np
from scipy import sparse

from trace_atlas import extracted_trace_moments, sparse_power_traces, weighted_jet_norm


def test_sparse_power_traces_on_a_diagonal_matrix():
    matrix = sparse.diags([0.5, -0.25]).tocsr()
    traces = sparse_power_traces(matrix, 4)
    expected = np.asarray([0.5**n + (-0.25) ** n for n in range(1, 5)])
    assert np.max(np.abs(traces - expected)) < 1e-14


def test_extraction_removes_listed_eigenvalues():
    roots = np.asarray([0.5, -0.25])
    traces = np.asarray([np.sum(roots**n) for n in range(1, 5)])
    residual = extracted_trace_moments(traces, 0.5, -0.25, np.asarray([]))
    assert np.max(np.abs(residual)) < 1e-14
    assert weighted_jet_norm(residual) < 1e-14
