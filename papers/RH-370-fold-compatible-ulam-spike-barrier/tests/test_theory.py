from __future__ import annotations

from fractions import Fraction

from fold_ulam import ROOT_U, finite_checks, mirror_extension, spike_jump
from fold_ulam.core import cyclic_folded_matrix


def test_exact_folding_checks() -> None:
    checks = finite_checks()
    assert checks["all_pass"] is True
    assert len(checks["rows"]) == 4


def test_characteristic_factor_and_kernel() -> None:
    folded = cyclic_folded_matrix(5)
    audit = mirror_extension(folded, 2)
    assert all(value == 0 for row in audit["observable_residual"] for value in row)
    assert all(value == 0 for vector in audit["kernel_images"] for value in vector)
    assert audit["char_full"] == audit["char_folded"] + (Fraction(0),) * 2


def test_spike_jump_has_exact_half_power() -> None:
    values = []
    for h in (1 / 4, 1 / 16, 1 / 64):
        values.append(spike_jump(ROOT_U, h) * h**0.5)
    assert max(values) - min(values) < 1e-12
    expected = (2.0 - 2.0**0.5) / ROOT_U**0.5
    assert abs(values[0] - expected) < 1e-12
