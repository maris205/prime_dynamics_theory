from superloop_review import macro_gates, route_coordinate


def test_review_route_keeps_all_macro_gates_open():
    statuses = {gate: False for gate in "ABCDE"}
    statuses["complete_gluing_certificate"] = False
    assert macro_gates(statuses) == {gate: False for gate in "ABCDE"}
    assert route_coordinate(statuses).startswith("exact_superloop_quotient")
