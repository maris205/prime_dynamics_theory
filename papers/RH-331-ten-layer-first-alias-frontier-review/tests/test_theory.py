from first_alias_review import ROUTE_COORDINATE, batch_status


def test_ten_typed_layers_have_scoped_conclusions_only():
    status = batch_status()
    assert status["paper_numbers"] == list(range(322, 332))
    assert status["layer_count"] == 10
    assert status["proved_scoped_conclusion_count"] == 10
    assert status["discharged_actual_bridge_obligation_count"] == 0
    assert all(layer["conclusion_proved"] for layer in status["layers"])
    assert not any(layer["actual_bridge_obligation_discharged"] for layer in status["layers"])


def test_exact_transfer_architecture_remains_inactive():
    status = batch_status()
    assert status["route_coordinate"] == ROUTE_COORDINATE
    assert status["exact_actual_model_transfer_identity_proved"] is True
    assert status["observable_shell_gauge_invariance_proved"] is True
    assert status["open_actual_bridge_obligation_count"] == 9
    assert not any(status["actual_bridge_obligations"].values())
    assert status["actual_full_trace_replacement_proved"] is False
    assert status["determinant_gluing_activated"] is False


def test_branch_ledgers_and_gates_do_not_close():
    status = batch_status()
    assert status["ledger_coordinates"] == ["head", "bridge", "tail", "target", "boundary"]
    assert status["spectral_score"] == 4
    assert status["counterloop_score"] == 4
    assert status["weighted_cross_branch_glue_proved"] is False
    assert status["complete_count"] == 0
    assert not any(status["gates"].values())
