from __future__ import annotations

from fractions import Fraction

import numpy as np

from packet_pair import (
    certify_leaf_transfer,
    exact_real_gram,
    pair_correction_majorant,
)


def test_exact_real_gram_uses_binary64_values_as_exact_dyadics() -> None:
    left = np.asarray([[0.5, -0.25], [1.0, 0.125]])
    right = np.asarray([[2.0, 0.5], [4.0, -2.0]])
    result = exact_real_gram(left, right)
    assert result.entries[0][0] == Fraction(0)
    assert result.entries[0][1] == Fraction(3, 4)
    assert result.entries[1][0] == Fraction(5, 2)
    assert result.entries[1][1] == Fraction(1, 4)
    assert result.frobenius_upper >= np.linalg.norm(left @ right, ord="fro")


def test_structured_majorant_contains_small_exact_pair_correction() -> None:
    rng = np.random.default_rng(73)
    dimension = 8
    rank = 2
    physical = rng.normal(size=(dimension, dimension)) / 5.0
    synthesis = rng.normal(size=(dimension, rank)) / 3.0
    base_analysis = np.linalg.solve(
        synthesis.T @ synthesis, synthesis.T
    )
    analysis = (np.eye(rank) + 2.0e-7 * rng.normal(size=(rank, rank))) @ (
        base_analysis
    )
    gram = analysis @ synthesis
    defect = gram - np.eye(rank)
    corrected_analysis = np.linalg.solve(gram, analysis)
    delta_analysis = corrected_analysis - analysis
    external = np.eye(dimension) - synthesis @ analysis
    corrected_external = np.eye(dimension) - synthesis @ corrected_analysis
    direct = analysis @ physical @ synthesis
    forcing = external @ physical @ synthesis
    observation = analysis @ physical @ external
    complement = external @ physical @ external
    corrected_direct = corrected_analysis @ physical @ synthesis
    corrected_forcing = corrected_external @ physical @ synthesis
    corrected_observation = (
        corrected_analysis @ physical @ corrected_external
    )
    corrected_complement = (
        corrected_external @ physical @ corrected_external
    )
    pad = 1.0 + 1.0e-12
    majorant = pair_correction_majorant(
        pair_defect_upper=pad * np.linalg.norm(defect, ord=2),
        synthesis_upper=pad * np.linalg.norm(synthesis, ord=2),
        analysis_upper=pad * np.linalg.norm(analysis, ord=2),
        physical_on_packet_upper=pad
        * np.linalg.norm(physical @ synthesis, ord=2),
        physical_on_external_upper=pad
        * np.linalg.norm(physical @ external, ord=2),
        stored_direct_upper=pad * np.linalg.norm(direct, ord=2),
        stored_forcing_upper=pad * np.linalg.norm(forcing, ord=2),
        stored_observation_upper=pad * np.linalg.norm(observation, ord=2),
    )
    assert np.linalg.norm(delta_analysis, ord=2) <= (
        majorant.analysis_correction_upper
    )
    assert np.linalg.norm(corrected_direct - direct, ord=2) <= (
        majorant.direct_correction_upper
    )
    assert np.linalg.norm(corrected_forcing - forcing, ord=2) <= (
        majorant.forcing_correction_upper
    )
    assert np.linalg.norm(corrected_observation - observation, ord=2) <= (
        majorant.observation_correction_upper
    )
    assert np.linalg.norm(corrected_complement - complement, ord=2) <= (
        majorant.complement_correction_upper
    )


def test_leaf_certificate_includes_the_full_inherited_remainder() -> None:
    majorant = pair_correction_majorant(
        pair_defect_upper=1.0e-8,
        synthesis_upper=1.2,
        analysis_upper=1.3,
        physical_on_packet_upper=1.4,
        physical_on_external_upper=1.5,
        stored_direct_upper=1.1,
        stored_forcing_upper=0.9,
        stored_observation_upper=1.0,
    )
    result = certify_leaf_transfer(
        majorant,
        stored_complement_inverse_upper=10.0,
        projected_feshbach_inverse_upper=4.0,
        stored_feshbach_computed_ratio_upper=0.1,
        stored_feshbach_remainder_coefficient_upper=0.02,
    )
    assert result.stored_feshbach_full_ratio_upper >= 0.3
    assert result.stored_feshbach_inverse_upper >= 4.0 / 0.7
    assert result.complement_homotopy_certified
    assert result.feshbach_homotopy_certified


def test_exact_corrected_block_is_physical_plus_zero_block() -> None:
    rng = np.random.default_rng(91)
    dimension = 7
    rank = 2
    physical = rng.normal(size=(dimension, dimension))
    synthesis = rng.normal(size=(dimension, rank))
    analysis = np.linalg.solve(synthesis.T @ synthesis, synthesis.T)
    corrected_external = np.eye(dimension) - synthesis @ analysis
    injection = np.vstack((analysis, corrected_external))
    extraction = np.hstack((synthesis, corrected_external))
    augmented = injection @ physical @ extraction
    assert np.linalg.norm(extraction @ injection - np.eye(dimension)) < 1.0e-12
    zeta = 2.3 + 0.7j
    left = np.linalg.det(
        zeta * np.eye(dimension + rank) - augmented
    )
    right = zeta**rank * np.linalg.det(
        zeta * np.eye(dimension) - physical
    )
    assert abs(left - right) <= 1.0e-9 * max(abs(left), abs(right), 1.0)
