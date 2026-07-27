import numpy as np

from divisor_first import rotating_similarity_example, route_coordinate


def test_rotating_projector_leaves_divisor_fixed():
    reference = rotating_similarity_example(0.0)
    terminal = rotating_similarity_example(np.pi / 2)
    assert np.linalg.norm(reference["characteristic_coefficients"] - terminal["characteristic_coefficients"]) < 1e-12
    assert terminal["projector_distance"] > 0.999


def test_route_coordinate():
    statuses = {
        "finite_branch_correspondence": True,
        "finite_dual_channel_divisor": True,
        "naive_state_transport_rejected": True,
        "scalar_residue_renormalization_rejected": True,
        "all_level_divisor_limit": False,
    }
    assert route_coordinate(statuses) == "finite_dual_channel_divisor_flow_open_renormalization"
    statuses["all_level_divisor_limit"] = True
    assert route_coordinate(statuses) == "intrinsic_divisor_open_fredholm_assembly"
