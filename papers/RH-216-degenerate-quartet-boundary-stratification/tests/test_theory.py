import numpy as np

from shape_boundary import (
    boundary_root_distance,
    canonical_roots,
    degeneracy_labels,
    discriminant_formula,
    root_discriminant,
)


def test_discriminant_formula():
    u, eta = 0.37, -0.28
    assert abs(root_discriminant(canonical_roots(u, eta)) - discriminant_formula(u, eta)) < 1e-10


def test_axial_boundary_is_double_pm_one():
    assert boundary_root_distance(1.0, 0.7) == 0.0
    assert "axial_double_pair" in degeneracy_labels(1.0, 0.7)
    assert discriminant_formula(1.0, 0.7) == 0.0
