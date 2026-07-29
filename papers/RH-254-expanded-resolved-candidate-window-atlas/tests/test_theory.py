import numpy as np

from expanded_window import match_reference_roots, shell_count_and_rank


def test_matching_covers_reference_and_returns_new_roots():
    reference = np.asarray([1.0 + 0j, 0.5 + 0.2j])
    expanded = np.asarray([1.0 + 1e-9j, 0.5 + 0.2j, 0.1 - 0.1j])
    result = match_reference_roots(reference, expanded)
    assert result["maximum_matching_error"] < 2e-9
    assert result["unmatched"].size == 1


def test_shell_count_and_rank():
    shells = [np.asarray([1.0]), np.asarray([0.2 + 0.1j, 0.2 - 0.1j])]
    assert shell_count_and_rank(shells) == (2, 3)
