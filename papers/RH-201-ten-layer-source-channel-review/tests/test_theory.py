from source_channel_review import macro_boundary, next_frontier, route_coordinate


def test_route_and_boundaries():
    statuses = {"source_cyclic_quotient": True, "canonical_packet_exact": True, "edge_quartet_selected": True, "cross_scale_transport": False}
    assert route_coordinate(statuses) == "finite_canonical_edge_quartet_open_transport"
    boundary = macro_boundary()
    assert boundary["finite_source_channel_quartet"]
    assert not boundary["gate_A"]
    assert next_frontier(boundary)[0] == "validated_interval_quartet"
