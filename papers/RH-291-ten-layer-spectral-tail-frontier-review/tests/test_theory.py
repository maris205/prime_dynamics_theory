from tail_review import batch_status


def test_batch_frontier():
    status = batch_status()
    assert status["spectral_score"] == 4
    assert status["counterloop_score"] == 4
    assert status["complete_count"] == 0
    assert status["weighted_cross_branch_glue"] is False
    assert not any(status["gates"].values())
