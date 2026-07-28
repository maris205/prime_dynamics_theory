from determinant_review import macro_gates, route_coordinate


def test_route_requires_uniform_complement_and_local_counts():
    statuses = {
        "rank_growing_cloud": True,
        "shell_complete_selection": True,
        "empirical_tightness": True,
        "direct_divisor_rejected": True,
        "reciprocal_dictionary": True,
        "resolved_tail_control": True,
        "dual_channel_coherence": True,
    }
    assert route_coordinate(statuses) == "rank_growing_reciprocal_cloud_open_uniform_complement_ideal_limit"
    statuses["uniform_complement_ideal_control"] = True
    statuses["local_count_stability"] = True
    assert route_coordinate(statuses) == "relative_det2_family_open_dynamical_limit"


def test_macro_gates_default_closed():
    assert not any(macro_gates({}).values())
