import numpy as np

from dyadic_packet_gauge import dyadic_polar_alignment, exact_gram_metric_lift, tail_inflation_factor


def test_dyadic_alignment_and_metric_lift():
    embedding = np.array([[2**-0.5, 0.0], [2**-0.5, 0.0], [0.0, 2**-0.5], [0.0, 2**-0.5]])
    source = np.eye(2)
    target = embedding.copy()
    alignment = dyadic_polar_alignment(source, target, embedding)
    assert np.allclose(alignment["principal_cosines"], 1.0)
    source_gram = np.diag([4.0, 1.0])
    target_gram = np.diag([1.0, 9.0])
    lift = exact_gram_metric_lift(source_gram, target_gram, alignment["target_to_source"])
    assert lift["gram_alignment_error"] < 1e-12


def test_natural_tail_inflation_and_geometry_tail_obstruction():
    source_gram = np.eye(2)
    target_gram = np.eye(2)
    lift = exact_gram_metric_lift(source_gram, target_gram, np.eye(2))
    source_tail = np.diag([1.0, 1e-6])
    target_tail = np.diag([1e-6, 1.0])
    factor = tail_inflation_factor(source_tail, target_tail, lift["gauge"])
    assert abs(factor - 1e6) < 1e-4
