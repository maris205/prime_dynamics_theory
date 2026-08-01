import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic():
    assert _result() == result_payload()


def test_result_locks_information_class_scope():
    data = _result()
    theorem = data["abstract_completion_theorem"]
    assert theorem["information_class_only"] is True
    assert theorem["cancelling_completion_exists_algebraically"] is True
    assert theorem["noncancelling_completion_exists_algebraically"] is True
    assert theorem["physical_realizability_claimed"] is False
    assert theorem["aggregate_physical_verdict_determined"] is False
    assert data["two_order_compensation"]["separate_absolute_route"] == "STOP_SCOPED"
    assert data["two_order_compensation"]["signed_aggregate_verdict"] == "NOT_TESTABLE"


def test_all_nine_upstream_gate_ledgers_are_false():
    names = (
        "RH-332-sharp-physical-repelling-return-affine-leg-remainder",
        "RH-333-raw-forward-affine-tube-escape-obstruction",
        "RH-334-gauge-fixed-physical-first-alias-observation-map",
        "RH-335-projector-localized-parity-ledger-and-cellwise-extension-nonuniqueness",
        "RH-336-projector-mass-first-alias-threshold-and-isospectral-cell-obstruction",
        "RH-337-algebraic-clock-drift-and-parity-alias-replacement-obstruction",
        "RH-338-boundary-orbit-far-atom-and-signed-diffuse-compensation-obstruction",
        "RH-339-first-lower-sideband-orbit-atom-compensation-obstruction",
        "RH-340-synchronized-determinant-prefix-and-two-order-orbit-head-compensation-obstruction",
    )
    values = []
    for name in names:
        source = json.loads((PAPERS / name / "results/result.json").read_text())
        assert len(source["gates"]) == 5
        values.extend(source["gates"].values())
    assert len(values) == 45
    assert not any(values)
    assert _result()["batch_gate_values_expected_false"] == 50


def test_finite_rows_are_never_promoted_to_physical_evidence():
    data = _result()
    assert len(data["abstract_witness_rows"]) == 4
    assert data["finite_rows_are_abstract_algebra_checks_only"] is True
    assert all(not row["physical_operator_constructed"] for row in data["abstract_witness_rows"])
