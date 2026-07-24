import math
import numpy as np

from singular_support_rayleigh import (
    outward_support_rayleigh_upper,
    support_rayleigh_constant,
    support_volume_lower,
)


def test_kernel_criterion_and_pseudoinverse_formula():
    gram = np.diag([4.0, 1.0, 0.0])
    tail = np.diag([1.0, 0.25, 0.0])
    result = support_rayleigh_constant(gram, tail, support_tolerance=1e-12, compatibility_tolerance=1e-12)
    assert result["support_rank"] == 2
    assert result["kernel_compatible"]
    assert abs(result["support_gamma"] - 0.5) < 1e-12
    assert abs(result["pseudovolume"] - 2.0) < 1e-12
    obstructed = support_rayleigh_constant(
        gram, tail + np.diag([0.0, 0.0, 1e-4]),
        support_tolerance=1e-12, compatibility_tolerance=1e-12,
    )
    assert math.isinf(obstructed["full_space_gamma"])


def test_sharp_volume_and_outward_guard():
    assert abs(support_volume_lower(6.0, 0.25, 2) - 3.375) < 1e-12
    gram = np.diag([2.0, 1.0, 0.0])
    tail = np.diag([0.2, 0.2, 0.0])
    basis = np.eye(3)[:, :2]
    bound = outward_support_rayleigh_upper(gram, tail, basis, 1e-6, 2e-6)
    exact = support_rayleigh_constant(gram, tail, support_tolerance=1e-12)
    assert bound["outward_gamma_squared_upper"] >= exact["support_gamma_squared"]
