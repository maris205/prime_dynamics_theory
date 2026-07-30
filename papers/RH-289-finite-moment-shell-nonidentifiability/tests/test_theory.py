import math

from moment_no_go import shell_factor, shell_moment


def test_hidden_shell_moments():
    order, radius = 11, 0.8
    for power in range(1, order):
        assert abs(shell_moment(order, radius, power)) < 1e-12
    assert abs(shell_moment(order, radius, order) - order * radius**order) < 1e-11


def test_exact_genus_one_factor():
    order, radius, z = 7, 0.6, 0.4 + 0.2j
    assert abs(shell_factor(order, radius, z) - (1 - (radius * z) ** order)) < 1e-12
