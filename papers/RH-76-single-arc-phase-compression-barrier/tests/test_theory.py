import math

import pytest

from phase_compression import (
    arc_chord_radius,
    binomial_arc_remainder,
    coherence_residual_lower,
)


def test_zero_arc_is_rank_one() -> None:
    assert arc_chord_radius(0.0) == 0.0
    assert binomial_arc_remainder(20, 1, 0.0) == 0.0


def test_full_degree_is_exact() -> None:
    assert binomial_arc_remainder(12, 13, 2.0) == 0.0


def test_narrower_arc_improves_bound() -> None:
    assert binomial_arc_remainder(20, 8, 0.1) < binomial_arc_remainder(20, 8, 1.0)


def test_fourier_coherence_forces_unit_residual() -> None:
    assert coherence_residual_lower(8, 0.0) == 1.0


@pytest.mark.parametrize("call", [lambda: arc_chord_radius(-1.0), lambda: binomial_arc_remainder(4, 6, 0.1), lambda: coherence_residual_lower(0, 0.1)])
def test_invalid_inputs_fail(call) -> None:
    with pytest.raises(ValueError):
        call()
