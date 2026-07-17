from __future__ import annotations

from fractions import Fraction

import numpy as np

from resolvent_atlas import (
    build_direct_grushin_system,
    certify_arc_coverage,
    merge_circular_gap_components,
    turn_center_id,
)


def test_arc_coverage_closes_local_disc() -> None:
    row = {
        "arc": "3",
        "center_real": "0.0",
        "center_imag": "0.0",
        "disc_radius": "0.01",
        "resolvent_budget_lower": "1000.0",
    }
    result = certify_arc_coverage(0.0j, 10.0, row)
    assert result.closed
    assert result.neumann_product_upper < 1.0


def test_arc_coverage_rejects_remote_disc() -> None:
    row = {
        "arc": "4",
        "center_real": "0.2",
        "center_imag": "0.0",
        "disc_radius": "0.01",
        "resolvent_budget_lower": "1000.0",
    }
    result = certify_arc_coverage(0.0j, 10.0, row)
    assert not result.closed
    assert result.neumann_product_upper > 1.0


def test_exact_gap_components_merge_across_dyadic_levels() -> None:
    leaves = [
        {
            "parent_arc": 2,
            "start_numerator": 1,
            "end_numerator": 2,
            "turn_denominator": 8,
        },
        {
            "parent_arc": 3,
            "start_numerator": 4,
            "end_numerator": 6,
            "turn_denominator": 16,
        },
    ]
    components = merge_circular_gap_components(leaves)
    assert len(components) == 1
    assert components[0].start_turn == Fraction(1, 8)
    assert components[0].end_turn == Fraction(3, 8)
    assert components[0].midpoint_turn == Fraction(1, 4)
    assert components[0].parent_arcs == (2, 3)


def test_gap_components_merge_at_turn_seam() -> None:
    leaves = [
        {
            "parent_arc": 0,
            "start_numerator": 0,
            "end_numerator": 1,
            "turn_denominator": 16,
        },
        {
            "parent_arc": 15,
            "start_numerator": 15,
            "end_numerator": 16,
            "turn_denominator": 16,
        },
    ]
    components = merge_circular_gap_components(leaves)
    assert len(components) == 1
    assert components[0].start_turn == Fraction(15, 16)
    assert components[0].end_turn == Fraction(17, 16)
    assert components[0].midpoint_turn == Fraction(0)
    assert turn_center_id(components[0].midpoint_turn) == "turn_00000000_of_00000001"


def test_unlifted_grushin_leading_block_is_exact_complement_inverse() -> None:
    generator = np.random.default_rng(20260716)
    dimension = 6
    packet_rank = 2
    peripheral_rank = 1
    matrix = generator.normal(size=(dimension, dimension)) / 8.0
    right = generator.normal(size=(dimension, peripheral_rank))
    left = generator.normal(size=(dimension, peripheral_rank))
    values = np.asarray([0.17])
    synthesis = generator.normal(size=(dimension, packet_rank)) / 3.0
    analysis = generator.normal(size=(packet_rank, dimension)) / 3.0
    zeta = 1.7 + 0.2j
    system = build_direct_grushin_system(
        matrix,
        right,
        left,
        values,
        synthesis,
        analysis,
        zeta,
    )
    one_step = matrix - (right * values[None, :]) @ left.T
    external = np.eye(dimension) - synthesis @ analysis
    target = zeta * np.eye(dimension) - external @ one_step @ one_step @ external
    leading = np.linalg.inv(system.matrix.toarray())[:dimension, :dimension]
    assert np.allclose(leading, np.linalg.inv(target), rtol=2.0e-11, atol=2.0e-11)


def test_stored_block_schur_determinant_without_projector_assumption() -> None:
    generator = np.random.default_rng(33)
    dimension = 5
    packet_rank = 2
    block = generator.normal(size=(dimension, dimension)) / 5.0
    forcing = generator.normal(size=(dimension, packet_rank)) / 4.0
    observation = generator.normal(size=(packet_rank, dimension)) / 4.0
    direct = generator.normal(size=(packet_rank, packet_rank)) / 5.0
    zeta = 1.3 - 0.4j
    complement = zeta * np.eye(dimension) - block
    feshbach = (
        zeta * np.eye(packet_rank)
        - direct
        - observation @ np.linalg.solve(complement, forcing)
    )
    augmented = np.block([[direct, observation], [forcing, block]])
    left_value = np.linalg.det(zeta * np.eye(dimension + packet_rank) - augmented)
    right_value = np.linalg.det(complement) * np.linalg.det(feshbach)
    assert np.allclose(left_value, right_value, rtol=2.0e-12, atol=2.0e-12)
