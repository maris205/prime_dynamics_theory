from __future__ import annotations

import numpy as np
import pytest

from scale_law import (
    anchor_matching_extension,
    bounded_anchor_matching_extension,
    loglog_fit,
    smooth_cutoff,
)


def test_smooth_cutoff_endpoints() -> None:
    values = smooth_cutoff([0.1, 0.3, 0.5, 0.7], 0.2, 0.6)
    assert values[0] == 0.0
    assert values[-1] == 1.0
    assert 0.0 < values[1] < values[2] < 1.0


def test_positive_extension_matches_anchors_and_germ() -> None:
    scales = np.array([0.02, 0.04, 0.08])
    anchors = np.array([0.2, 0.1, 0.05])
    points = np.concatenate([scales, [1e-4]])
    values = anchor_matching_extension(scales, anchors, points, lambda x: x**2)
    assert values[:-1] == pytest.approx(anchors)
    assert values[-1] == pytest.approx(1e-8)


def test_bounded_extensions_have_incompatible_limits() -> None:
    scales = np.array([0.01, 0.02, 0.04])
    anchors = np.array([0.3, 0.2, 0.1])
    points = np.concatenate([scales, [1e-6]])
    germs = (lambda x: x, lambda x: np.full_like(x, 0.5), lambda x: 1.0 - x)
    probes = []
    for germ in germs:
        values = bounded_anchor_matching_extension(scales, anchors, points, germ)
        assert values[:-1] == pytest.approx(anchors)
        assert np.all((values > 0.0) & (values < 1.0))
        probes.append(values[-1])
    assert probes == pytest.approx([1e-6, 0.5, 1.0 - 1e-6])


def test_loglog_fit_recovers_exact_power() -> None:
    scales = np.array([0.01, 0.02, 0.04, 0.08])
    values = 3.0 * scales**1.75
    fit = loglog_fit(scales, values)
    assert fit["exponent"] == pytest.approx(1.75)
    assert fit["coefficient"] == pytest.approx(3.0)
    assert fit["r_squared"] == pytest.approx(1.0)


def test_validation() -> None:
    with pytest.raises(ValueError):
        loglog_fit([0.1, 0.2], [1.0, 2.0])
    with pytest.raises(ValueError):
        bounded_anchor_matching_extension([0.1], [1.0], [0.1], lambda x: x)
