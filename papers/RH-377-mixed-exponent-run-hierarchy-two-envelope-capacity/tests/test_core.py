from fractions import Fraction
from itertools import product

from mixed_run_hierarchy import (
    ENDPOINT,
    aggregate_layers,
    boolean_rank_certificate,
    countermodel_certificate,
    euler_diagnostic,
    mixed_layers,
    mobius_prefix,
    mobius_residual_certificate,
    signed_run_indicator,
    stationary_moment,
    transition_probability,
)


def test_mobius_and_small_boolean_layers():
    mu = mobius_prefix(12)
    assert mu[1:] == [1, -1, -1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
    for values in product((-1, 0, 1), repeat=3):
        layers = mixed_layers(values)
        even, odd = aggregate_layers(layers)
        for sigma in (-1, 1):
            assert 8 * signed_run_indicator(values, sigma) == (
                layers[0] + even + sigma * (layers[1] + odd)
            )


def test_exhaustive_boolean_and_formal_rank_certificate():
    result = boolean_rank_certificate()
    assert result["all_pass"]
    assert result["boolean_case_count"] == 19_680
    assert result["formal_coordinate_count"] == 466
    assert result["formal_rank"] == 13
    assert result["formal_kernel_dimension"] == 453
    assert result["formal_rank_not_arithmetic_minimal"]
    assert result["a_row_supports"] == [1, 3, 7, 15, 31, 63, 127]
    assert result["b_row_supports"] == [1, 4, 11, 26, 57, 120]


def test_stationary_countermodel_certificate():
    result = countermodel_certificate()
    assert result["all_pass"]
    assert result["transition_cells"] == 27
    assert result["stationarity_pair_cells"] == 9
    assert result["distinct_raw_moment_cases"] == 502
    assert result["square_only_moment_cases"] == 502
    assert result["one_sign_masked_moment_cases"] == 1_793
    assert result["directional_moments"]["E_A_B_C2"]["text"] == "8/81"
    assert result["triple_probabilities"]["plus_plus_plus"]["text"] == "4/81"
    assert result["synthetic_not_mobius"]
    assert result["does_not_match_mobius_squarefree"]
    assert transition_probability(1, 1, 0) == Fraction(1, 9)
    assert stationary_moment((1, 1, 2)) == Fraction(8, 81)


def test_full_mobius_residual_ledger():
    result = mobius_residual_certificate()
    assert result["all_pass"]
    assert result["endpoint"] == ENDPOINT
    assert result["window_updates"] == 1_048_548
    assert result["cumulative_sign_identity_count"] == 4_194_304
    assert result["path_capacity_prefix_count"] == 262_144
    endpoint = result["frozen_rows"]["262144"]
    assert endpoint["H0"] == [106237, 84569, 65768, 49604, 35783, 24127, 14429, 6449]
    assert endpoint["H1"] == [3, -56, -174, -146, 115, -54, -111, -14]
    assert endpoint["K_N"] == 129080
    assert endpoint["capacity_residual_scaled_256"] == 2560
    assert endpoint["capacity_bound_scaled_256"] == 14848


def test_conditional_euler_diagnostic():
    result = euler_diagnostic()
    assert result["finite_not_asymptotic"]
    assert result["prime_cutoff"] == 1_048_576
    assert result["prime_count"] == 82_025
    assert result["odd_prime_count"] == 82_024
    assert result["conditional_capacity_partial"] == "0.4920202775829839485"
    assert result["decimal_reproduction_pass"]
