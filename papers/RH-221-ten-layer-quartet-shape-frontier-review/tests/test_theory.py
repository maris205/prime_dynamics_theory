from shape_review import review_coordinate, strict_gate_vector


def test_review_coordinate_and_strict_gates():
    statuses = {key: True for key in (
        "normalization_negative",
        "shape_manifold_exact",
        "finite_clock_positive",
        "prediction_law_open",
        "boundary_theorem_exact",
        "transverse_quenching_exact",
        "recurrence_identification_negative",
        "fixed_degree_counting_negative",
        "gauge_completion_exact",
    )}
    statuses["rank_growing_divisor_constructed"] = False
    assert review_coordinate(statuses) == "finite_gauge_complete_shape_flow_open_rank_growing_divisor"
    assert not any(strict_gate_vector().values())
