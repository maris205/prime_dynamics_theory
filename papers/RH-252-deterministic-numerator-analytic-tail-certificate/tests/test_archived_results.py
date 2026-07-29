import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_archived_tail_certificate():
    payload = json.loads((ROOT / "results/analytic_tail_audit.json").read_text())
    assert payload["scaled_zero_free_radius"] > 1.42
    assert payload["unit_disk_all_order_target_tail_exists"] is True
    assert payload["finite_boundary_supremum_available"] is False
    assert payload["coefficient_orders_used_for_diagnostics"] == list(range(2, 13))
    assert payload["theorem_boundary"]["analytic_all_order_target_tail"] is True
    assert payload["theorem_boundary"]["numerical_uniform_target_tail_constant"] is False
    assert payload["theorem_boundary"]["gate_A"] is False
