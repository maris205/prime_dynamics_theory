from shell_transport import neumann_resolvent_bound, normalizer_lower


def test_positive_normalizer_on_archived_interval():
    assert normalizer_lower(0.04) > 0.499


def test_neumann_bound():
    assert neumann_resolvent_bound(10, 0.04) == 10 / 0.6
