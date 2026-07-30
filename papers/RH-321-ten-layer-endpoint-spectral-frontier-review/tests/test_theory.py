from endpoint_spectral_review import batch_status


def test_typed_ledgers_remain_separate():
    status = batch_status()
    assert status["spectral_score"] == 4
    assert status["counterloop_score"] == 4
    assert status["weighted_cross_branch_glue_proved"] is False


def test_synthetic_progress_does_not_set_actual_transport():
    status = batch_status()
    assert status["exact_finite_spectral_prefix_realization_proved"] is True
    assert status["actual_fixed_order_complement_transport_proved"] is False
    assert status["actual_endpoint_energy_tightness_proved"] is False


def test_complete_count_stays_zero():
    assert batch_status()["complete_count"] == 0
