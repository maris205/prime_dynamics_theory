from __future__ import annotations

from euclidean_contour import (
    HilbertEnvelope,
    adaptive_multiple,
    continuum_galerkin_defect,
    discrete_normalization_defect,
    hilbert_haar_bounds,
    hilbert_schur_step,
    midpoint_galerkin_defect,
    neumann_transfer,
    relaxed_cutoff_defect,
)


ENVELOPE = HilbertEnvelope(
    kernel=5.49855,
    source_first=669.465,
    target_first=382.571,
    source_second=196078.0,
    source_target=82004.0,
    target_second=47447.0,
    source_second_target_second=1.445e10,
)


def test_midpoint_peano_defect_is_second_order() -> None:
    first = midpoint_galerkin_defect(4096, ENVELOPE)
    second = midpoint_galerkin_defect(8192, ENVELOPE)
    assert first < 8.2e-4
    assert second < first / 3.99


def test_hilbert_schur_chain_closes() -> None:
    resolvent = 90.3
    modulus = 0.9365
    for dimension in (4096, 8192, 16384, 32768):
        step = hilbert_schur_step(
            resolvent,
            modulus,
            hilbert_haar_bounds(dimension, ENVELOPE),
        )
        assert step.count_transfers
        resolvent = step.fine_resolvent_upper
    continuum = neumann_transfer(
        max(resolvent, 1.0 / modulus),
        continuum_galerkin_defect(65536, ENVELOPE),
    )
    assert continuum.admissible
    assert continuum.neumann_product_upper < 0.59


def test_normalization_and_cutoff_are_tiny_at_threshold() -> None:
    dimension = 131072
    midpoint = midpoint_galerkin_defect(dimension, ENVELOPE)
    normalization = discrete_normalization_defect(
        dimension,
        0.01,
        0.012533141373155,
        ENVELOPE.kernel,
        midpoint,
    )
    cutoff = relaxed_cutoff_defect(
        dimension, 0.01, adaptive_multiple(dimension, 8.0)
    )
    assert normalization.spectral_norm_defect_upper < 1.6e-6
    assert cutoff.spectral_norm_upper < 2.0e-13
