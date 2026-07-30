from annular_review import batch_status


def test_ledgers_remain_typed_and_incomplete():
    data = batch_status()
    assert data["spectral_ledger"] == [True, False, True, True, True]
    assert data["counterloop_ledger"] == [True, True, False, True, True]
    assert data["spectral_score"] == 4
    assert data["counterloop_score"] == 4
    assert data["weighted_cross_branch_glue_proved"] is False
    assert data["complete_count"] == 0


def test_all_gates_remain_open():
    assert not any(batch_status()["gates"].values())
