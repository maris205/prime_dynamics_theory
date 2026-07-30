import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["clock_intersection_empty_for_current_methods"] is True
    assert data["actual_trace_nonconvergence_proved"] is False
    assert data["new_boundary_layer_route_excluded"] is False
    assert not any(data["gates"].values())
