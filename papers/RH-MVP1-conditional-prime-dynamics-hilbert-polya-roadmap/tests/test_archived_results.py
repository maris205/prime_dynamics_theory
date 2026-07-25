import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def data() -> dict:
    return json.loads((ROOT / "results/mvp_audit.json").read_text())


def test_complete_numbered_inventory() -> None:
    summary = data()["audit_summary"]
    assert summary["numbered_paper_count"] == 160
    assert summary["consecutive_numbering"]
    assert summary["readme_count"] == 160
    assert summary["main_tex_count"] == 160
    assert summary["pdf_directory_count"] == 160
    assert summary["summary_archive_count"] == 131
    assert summary["verification_archive_count"] == 131


def test_declared_archives_and_milestones() -> None:
    summary = data()["audit_summary"]
    assert summary["declared_publication_hash_count"] == 1717
    assert summary["declared_publication_hash_failure_count"] == 0
    assert summary["milestone_input_count"] == 17
    assert summary["review_anchor_count"] == 10


def test_macro_debt_is_not_promoted() -> None:
    payload = data()
    summary = payload["audit_summary"]
    assert summary["proved_macro_gate_count"] == 1
    assert summary["conditional_macro_gate_count"] == 0
    assert summary["open_macro_gate_count"] == 5
    assert summary["full_mvp_completion_bundle"] == ["A", "B", "C", "D", "E"]
    assert summary["hilbert_polya_completion_bundle"] == ["A", "B", "C"]
    assert summary["current_unconditional_claim_level"] == "foundation"
    assert summary["current_first_missing_gate"] == "A"


def test_claim_boundary() -> None:
    boundary = data()["theorem_boundary"]
    assert boundary["conditional_macro_implication"]
    assert boundary["all_160_numbered_papers_present"]
    assert not boundary["all_macro_assumptions_proved"]
    assert not boundary["canonical_self_adjoint_operator_constructed"]
    assert not boundary["prime_power_trace_formula_proved"]
    assert not boundary["zeta_spectral_identity_proved"]
    assert not boundary["riemann_hypothesis_proved"]


def test_shortcuts_remain_rejected() -> None:
    payload = data()
    assert payload["audit_summary"]["rejected_shortcut_count"] == 9
    texts = " ".join(item["shortcut"] for item in payload["rejected_shortcuts"])
    assert "topological conjugacy" in texts
    assert "contemporaneous spectral reset" in texts
    assert "prime-power trace formula" in texts
