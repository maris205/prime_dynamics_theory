from frontier_review import PAPER_NUMBERS, counterloop_vector, spectral_vector


def test_ten_layers_and_dual_vectors():
    assert PAPER_NUMBERS == tuple(range(272, 282))
    assert sum(spectral_vector()) == 2
    assert sum(counterloop_vector()) == 4
