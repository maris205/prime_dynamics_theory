from trace_review import macro_gates, route_coordinate


def test_route_coordinate_requires_the_full_finite_chain():
    statuses = {
        "riesz_wall_identified": True,
        "radial_gap_insufficient": True,
        "projection_free_factor": True,
        "trace_hs_separation": True,
        "trace_moment_atlas": True,
        "dual_channel_jet_coherence": True,
        "adaptive_selector": True,
        "finite_jet_contraction_bound": True,
        "trace_envelope_criterion": True,
    }
    assert route_coordinate(statuses) == "projection_free_relative_det2_open_uniform_trace_envelope"
    assert not any(macro_gates(statuses).values())
