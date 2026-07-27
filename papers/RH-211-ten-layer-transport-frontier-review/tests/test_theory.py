from transport_review import review_coordinate, strict_gate_vector


def test_review_coordinate():
    statuses = {
        "naive_haar_transport_rejected": True,
        "branch_correspondence_supported": True,
        "dual_channel_divisor_supported": True,
        "scalar_residue_renormalization_rejected": True,
        "expanded_cloud_rejected": True,
        "all_level_divisor_limit": False,
    }
    assert review_coordinate(statuses) == "finite_dual_channel_divisor_flow_open_renormalization"


def test_macro_gates_remain_strictly_closed():
    gates = strict_gate_vector()
    assert set(gates) == {"gate_A", "gate_B", "gate_C", "gate_D", "gate_E", "hilbert_polya_operator", "zeta_zero_identification", "riemann_hypothesis"}
    assert not any(gates.values())
