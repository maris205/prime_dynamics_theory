import json
from pathlib import Path

from first_alias_review import batch_status


def test_result_firewall():
    root = Path(__file__).parents[1]
    data = json.loads((root / "results/result.json").read_text())
    expected = batch_status()
    assert data["layers"] == expected["layers"]
    assert data["ledger_coordinates"] == expected["ledger_coordinates"]
    assert data["route_coordinate"] == "first_alias_transfer_criterion_exact_actual_replacement_open"
    assert data["paper_numbers"] == list(range(322, 332))
    assert data["discharged_actual_bridge_obligation_count"] == 0
    assert data["actual_full_trace_replacement_proved"] is False
    assert data["actual_full_trace_divergence_proved"] is False
    assert data["actual_weighted_full_trace_prefix_vanishing_proved"] is False
    assert data["reopening_trigger_supplied"] is False
    assert data["scoped_first_alias_route_stop"] is True
    assert data["complete_count"] == 0
    assert data["hilbert_polya_constructed"] is False
    assert data["riemann_zeros_identified"] is False
    assert data["von_mangoldt_trace_proved"] is False
    assert data["zeta_divisor_equality"] is False
    assert data["riemann_hypothesis_proved"] is False
    assert not any(data["gates"].values())

    upstream = (
        "RH-322-certified-critical-folded-row-half-line-profile",
        "RH-323-oriented-paired-affine-gaussian-chain",
        "RH-324-sharp-physical-endpoint-affine-leg-remainder",
        "RH-325-moving-order-duhamel-composition-criterion",
        "RH-326-parity-renormalized-first-alias-packet-identity",
        "RH-327-neighboring-shell-coupling-cancellation-budget",
        "RH-328-joint-alias-parity-shell-matching-equation",
        "RH-329-validated-isolated-exchange-model-audit",
        "RH-330-joint-cancellation-full-trace-transfer-criterion",
    )
    gate_values = []
    for name in upstream:
        source = json.loads((root.parent / name / "results/result.json").read_text())
        assert len(source["gates"]) == 5
        gate_values.extend(source["gates"].values())
    assert len(gate_values) == 45
    assert not any(gate_values)
