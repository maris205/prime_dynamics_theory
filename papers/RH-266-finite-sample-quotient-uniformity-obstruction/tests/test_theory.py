import pytest
from uniformity_obstruction import finite_sample_uniformity_status, triangular_bump


def test_finite_samples_admit_an_unsampled_spike():
    samples = (0.1, 0.2, 0.4)
    bump = triangular_bump(samples, 0.3, 2.0)
    assert all(bump(value) == 0.0 for value in samples)
    assert bump(0.3) == pytest.approx(2.0)


def test_uniform_status_requires_both_inputs():
    status = finite_sample_uniformity_status(
        sample_count=23, missing_archived_count=9, continuum_modulus_available=False
    )
    assert status["uniform_conclusion_available"] is False
