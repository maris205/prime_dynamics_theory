from complement_budget import norm_only_complement_budget, root_half_spacing, validated_inverse_bound


def test_half_spacing():
    assert abs(root_half_spacing(4, 2.0) - 2.0 ** 0.5) < 1e-12


def test_norm_only_budget_can_succeed_or_fail():
    good = norm_only_complement_budget(0.1, 1.0, 2.0, 0.2, 1.0, 0.1, 0.1)
    assert good["norm_only_resolvent_available"]
    assert good["full_norm_only_certificate"]
    bad = norm_only_complement_budget(1.0, 10.0, 1.0, 0.1, 1.0, 0.1, 0.1)
    assert not bad["norm_only_resolvent_available"]


def test_complement_bound_is_linear_in_oblique_condition():
    result = norm_only_complement_budget(2.0, 3.0, 10.0, 1.0, 1.0, 0.1, 0.1)
    assert result["complement_operator_norm_bound"] == 6.0


def test_mesh_and_operator_ball_inverse_bound():
    good = validated_inverse_bound(2.0, 0.1, 0.05, 0.05)
    assert good["validated_inverse_available"]
    assert abs(good["validated_inverse_bound"] - 2.0 / 0.7) < 1e-12
    bad = validated_inverse_bound(5.0, 0.2, 0.1, 0.1)
    assert not bad["validated_inverse_available"]
