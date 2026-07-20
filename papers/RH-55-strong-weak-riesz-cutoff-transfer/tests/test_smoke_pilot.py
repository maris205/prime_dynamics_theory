from experiments.run_riesz_cutoff_pilot import build_payload


def test_smoke_pilot_replays_both_mechanisms() -> None:
    payload = build_payload(smoke=True)
    assert len(payload["midpoint_ulam_audit"]) == 2
    assert len(payload["archived_intrinsic_factor_audit"]) == 15
    extrema = payload["extrema"]
    assert extrema["maximum_midpoint_row_scaled_ratio"] < 0.42
    assert extrema["maximum_five_sigma_actual_riesz_sum"] < 6.6e-8
    assert extrema["kappa_two_shape_ratio_strictly_decreases"]
