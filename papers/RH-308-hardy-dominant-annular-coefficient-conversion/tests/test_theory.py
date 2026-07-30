import math

import pytest

from hardy_conversion import (
    cauchy_constant,
    hardy_constant,
    rudin_shapiro_block_lower,
    shrinking_hardy_scale,
)


def test_hardy_improves_cauchy_at_rho_1p41():
    assert hardy_constant(1.4, 1.41) < cauchy_constant(1.4, 1.41)
    assert math.isclose(hardy_constant(1.4, 1.41), 8.292467894275969)


def test_square_root_gap_asymptotic():
    eta = 1e-6
    assert math.isclose(
        shrinking_hardy_scale(eta) * math.sqrt(2.0 * eta), 1.0, rel_tol=5e-6
    )


def test_rudin_shapiro_block_has_square_root_scale():
    eta = 1e-3
    lower = rudin_shapiro_block_lower(eta, 1024)
    assert lower * math.sqrt(eta) > 0.1


def test_rudin_shapiro_length_must_be_dyadic():
    with pytest.raises(ValueError):
        rudin_shapiro_block_lower(0.1, 10)
