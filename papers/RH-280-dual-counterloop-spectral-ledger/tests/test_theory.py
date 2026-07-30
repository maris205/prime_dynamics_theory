from dual_ledger import COUNTERLOOP_VECTOR, SPECTRAL_VECTOR, complete


def test_vectors_are_distinct_and_incomplete():
    assert sum(SPECTRAL_VECTOR) == 2
    assert sum(COUNTERLOOP_VECTOR) == 4
    assert not complete(SPECTRAL_VECTOR)
    assert not complete(COUNTERLOOP_VECTOR)
