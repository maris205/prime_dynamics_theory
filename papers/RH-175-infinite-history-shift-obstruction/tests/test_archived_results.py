import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_shift_archive():
    payload = json.loads((ROOT / "results/shift_obstruction_audit.json").read_text())
    assert payload["resolvent_case_count"] == 15
    assert payload["maximum_relative_formula_error"] < 1e-12
    assert payload["all_finite_shift_spectra_zero"]
    assert payload["all_singular_floor_counts_match"]
    assert not payload["theorem_boundary"]["direct_fredholm_determinant_route"]
