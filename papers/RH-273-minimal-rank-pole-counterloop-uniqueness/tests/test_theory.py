from minrank import equality_roots, minimal_rank, prefix_moments


def test_rank_lower_bound_interface():
    assert minimal_rank(15) == 30


def test_equality_shell_has_prefix_moments():
    beta = 0.9
    for N in range(1, 8):
        roots = equality_roots(N, beta)
        for n in range(1, 2 * N + 1):
            assert abs(sum(z**n for z in roots) - prefix_moments(N, beta, n)) < 1e-12
