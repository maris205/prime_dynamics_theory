import json
from pathlib import Path


def test_result_scope():
    data = json.loads((Path(__file__).parents[1] / "results/result.json").read_text())
    assert data["fixed_order_bulk_leakage_law"] is True
    assert data["separate_parity_majorant_diverges"] is True
    assert data["combined_full_trace_error_diverges_proved"] is False
    assert data["moving_order_cancellation_excluded"] is False
    assert not any(data["gates"].values())
