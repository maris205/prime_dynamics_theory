import numpy as np

from adaptive_cloud import first_admissible_prefix


def test_first_admissible_shell_prefix():
    roots = [np.asarray([0.5, -0.5]), np.asarray([0.1j, -0.1j])]
    all_roots = np.concatenate(roots)
    full = np.asarray([np.sum(all_roots**n) for n in range(1, 5)])
    result = first_admissible_prefix(
        roots, full, 0.0, 0.0, tolerance=1e-14, minimum_rank=2
    )
    assert result["selected"] is not None
    assert result["selected"]["cloud"].size == 4
    assert result["selected"]["jet_norm"] < 1e-14
