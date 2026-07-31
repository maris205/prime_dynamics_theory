import math

import pytest

from joint_matching import (
    BETA,
    MULTIPLIER_CONSTANT,
    TARGET_RADIUS,
    distance_to_unit_interval,
    duhamel_majorant,
    exchange_shell,
    fixed_reference_reachability,
    hardy_target,
    joint_demand,
    joint_matching_decomposition,
    joint_residual,
    leading_alias_model,
    matching_power,
    normalized_required_power,
    power_radius_comparison,
    reachability_false_positive,
    target_contrast_radius,
    typed_interface,
    uncertainty_interval,
)


def test_exact_joint_matching_decomposition():
    row = joint_matching_decomposition(
        k=5,
        alias_defect=4.0,
        parity_packet=0.6,
        boundary_packet=0.9,
        scale=2.5,
        contrast=0.85,
        reference_contrast=0.7,
        observation_error=-0.03,
        remainder=0.02,
    )
    assert abs(row["identity_error"]) < 1e-14
    assert row["demand"] == pytest.approx(2.5)
    assert row["residual"] == pytest.approx(row["decomposed_residual"])


def test_raw_sign_ledger_and_shell_model():
    shell = exchange_shell(4, 3.0, -0.9, 0.8)
    residual = joint_residual(0.4, shell, -0.1, 0.2, 0.7)
    assert residual == pytest.approx(0.4 + shell - 0.1 + 0.2 - 0.7)
    assert joint_demand(0.7, 0.2, 0.4) == pytest.approx(0.1)


def test_required_power_and_reachability_distance():
    k = 6
    scale = 4.0
    reference = 0.8
    demand = 1.5
    y = matching_power(k, demand, scale, reference)
    row = fixed_reference_reachability(k, demand, scale, reference)
    assert row["required_power"] == pytest.approx(y)
    assert row["reachable"] is True
    assert row["best_absolute_residual"] == 0.0
    assert row["target_contrast_radius"] ** (2 * k) == pytest.approx(y)

    out = fixed_reference_reachability(k, 8.0, scale, reference)
    assert out["reachable"] is False
    assert out["best_absolute_residual"] == pytest.approx(
        scale * distance_to_unit_interval(out["required_power"])
    )


def test_alias_normalized_required_power():
    q = 0.2
    b = 0.3
    ell = 1.25
    z = 0.1
    y = normalized_required_power(
        parity_to_alias=q,
        boundary_to_alias=b,
        shell_to_alias=ell,
        reference_power=z,
    )
    assert y == pytest.approx(z + (1.0 - q - b) / ell)


def test_power_radius_mean_value_bounds():
    row = power_radius_comparison(16, 0.55, 0.97)
    assert row["mean_value_lower_bound"] <= row["power_mismatch"]
    assert row["power_mismatch"] <= row["mean_value_upper_bound"]
    assert row["target_radius"] ** 32 == pytest.approx(0.55)


def test_unit_edge_expansion():
    y = 0.4
    limit = -math.log(y)
    values = [
        2.0 * k * (1.0 - target_contrast_radius(k, y))
        for k in (16, 32, 64, 128)
    ]
    assert abs(values[-1] - limit) < abs(values[0] - limit)
    assert values[-1] == pytest.approx(limit, rel=0.01)


def test_alias_target_precision_scale():
    for k in (8, 16, 32):
        alias = leading_alias_model(k)
        target = hardy_target(k)
        expected = (
            MULTIPLIER_CONSTANT
            / 2.0
            * (BETA * TARGET_RADIUS) ** (-2 * k)
        )
        assert target / alias == pytest.approx(expected)


def test_sharp_uncertainty_interval():
    row = uncertainty_interval(-2.0, 0.25, 0.1)
    assert row == {
        "lower": pytest.approx(-2.35),
        "upper": pytest.approx(-1.65),
        "best_absolute_residual": pytest.approx(1.65),
        "worst_absolute_residual": pytest.approx(2.35),
    }
    centered = uncertainty_interval(0.2, 0.25, 0.1)
    assert centered["best_absolute_residual"] == 0.0


def test_duhamel_majorant_retains_all_weights():
    assert duhamel_majorant([2.0, 3.0, 5.0], [0.1, 0.2, 0.4]) == pytest.approx(
        2.8
    )
    with pytest.raises(ValueError):
        duhamel_majorant([1.0], [1.0, 2.0])


def test_reachability_false_positive():
    row = reachability_false_positive(theta=0.25, scale=100.0, target=0.01)
    assert row["best_case_reachability_residual"] == 0.0
    assert row["physical_model_mismatch"] == -25.0
    assert row["absolute_mismatch_to_target"] == 2500.0


def test_even_order_sign_ambiguity():
    assert exchange_shell(9, 2.0, 0.91, 0.7) == pytest.approx(
        exchange_shell(9, 2.0, -0.91, 0.7)
    )


def test_typed_interface_and_validation():
    interface = typed_interface()
    assert interface["joint_ledger"] == "e=B+S+R+P-A"
    assert interface["exact_matching_equation"] == (
        "e=L*(c_phys^(2k)-y)+E_obs+R"
    )
    assert interface["physical_contrast_identified"] is False
    with pytest.raises(ValueError):
        target_contrast_radius(4, 1.1)
    with pytest.raises(ValueError):
        exchange_shell(4, 1.0, 1.1, 0.0)
