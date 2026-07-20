from experiments.run_hardy_barrier_pilot import build_payload


def test_smoke_pilot_replays_scalar_and_inherited_clocks() -> None:
    payload = build_payload(smoke=True)
    assert len(payload["all_column_dense_audit"]) == 2
    assert len(payload["production_directional_audit"]) == 2
    assert len(payload["deterministic_tail_audit"]) == 2
    assert payload["extrema"]["common_strong_rate_threshold"] < 0.28
