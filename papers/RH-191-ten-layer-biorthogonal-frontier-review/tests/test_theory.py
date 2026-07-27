from biorthogonal_frontier import current_frontier, macro_boundary, route_status


def test_frontier_classification():
    statuses = {"biorthogonal_local_candidate": "local_floating_candidate", "validated_physical_D": "open"}
    assert route_status(statuses) == "local_biorthogonal_candidate_with_open_DKH"
    assert "validated_physical_D" in current_frontier(statuses)
    assert not macro_boundary()["gate_A"]
