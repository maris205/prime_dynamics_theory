import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontier_archive_boundary():
    payload = json.loads((ROOT / "results" / "r_frontier_audit.json").read_text(encoding="utf-8"))
    assert payload["finite_matrix_case_count"] == 3584
    assert payload["rank_change_witness_count"] == 63
    assert payload["aggregate_failure_count"] == 0
    assert payload["physical_R_status"] == "open"
    assert payload["current_first_missing_interface"] == "X_phys"
    assert not payload["theorem_boundary"]["riemann_hypothesis"]


def test_publication_archive_verification():
    payload = json.loads((ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8"))
    assert payload["status"] == "all_rh162_171_hashes_pdfs_audits_and_claim_boundaries_verified"
    assert payload["pdf_pair_count"] == 10
    assert payload["aggregate_failure_count"] == 0
