from fractions import Fraction
from itertools import product

from safe_window_transducers import (
    causal_policy_count,
    current_zero_basis_dimension,
    exhaustive_extrema_certificate,
    graph_lift_certificate,
    lag_table_certificate,
    mealy_certificate,
    mobius_certificate,
    online_obstruction_certificate,
    score_coefficients,
    truncated_window_certificate,
    window_safety_cases,
)


def test_lag_census_rank_and_witnesses() -> None:
    certificate = lag_table_certificate()
    assert certificate["all_pass"]
    assert certificate["safe_table_count"] == 13
    assert certificate["coefficient_rank"] == 5
    assert score_coefficients(frozenset({(0, 1)})) == (0, 1, 0, 0, -1, -1)
    assert score_coefficients(frozenset({(-1, 1), (0, 1)})) == (
        0,
        1,
        Fraction(-1, 2),
        Fraction(-1, 2),
        Fraction(-1, 2),
        Fraction(-1, 2),
    )


def test_basis_and_mealy_minimality() -> None:
    assert current_zero_basis_dimension(1, 15) == 2 * 3**14
    ell_one = {(0, window): -1 for window in product((-1, 0, 1), repeat=1)}
    assert window_safety_cases(ell_one, 1, 1) == (True, 27)
    ell_two = {
        (phase, window): -1
        for phase in range(2)
        for window in product((-1, 0, 1), repeat=2)
    }
    assert window_safety_cases(ell_two, 2, 2) == (True, 162)
    assert mealy_certificate()["all_pass"]


def test_online_obstruction() -> None:
    assert [causal_policy_count(horizon) for horizon in range(1, 5)] == [
        8,
        256,
        65536,
        0,
    ]
    certificate = online_obstruction_certificate()
    assert certificate["adversarial_branch_replay_pass"]
    assert certificate["if_first_output_plus_scores"] == [1, 2, 1]
    assert certificate["if_first_output_minus_scores"] == [-1, -2, -3, -2]
    assert certificate["if_first_output_plus_choice_rows"][-1][
        "safe_prefix_optimal_choices"
    ] == []
    assert certificate["if_first_output_minus_choice_rows"][-1][
        "safe_prefix_optimal_choices"
    ] == []
    assert certificate["all_pass"]


def test_truncated_window() -> None:
    assert truncated_window_certificate()["all_pass"]


def test_full_graph_exhaustion_and_mobius_stream() -> None:
    graph = graph_lift_certificate()
    assert graph["total_cases"] == 486
    assert graph["all_pass"]
    exhaustive = exhaustive_extrema_certificate()
    assert exhaustive["word_count"] == 88_572
    assert exhaustive["extrema_equality_count"] == 177_144
    assert exhaustive["all_pass"]
    mobius = mobius_certificate()
    assert mobius["endpoint"] == 1 << 20
    assert mobius["prefix_extrema_equality_count"] == 2_097_152
    assert mobius["lag_ledger_prefix_count"] == 1_048_576
    assert mobius["recursive_window_equality_count"] == 2_097_152
    assert mobius["all_pass"]
