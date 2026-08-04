import hashlib
import json
from pathlib import Path

from experiments.build_result import result_payload
from signed_counterloop_review import DIRECTORY_NAMES, UPSTREAM_FALSE_CLAIM_COUNTS


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent


def _result():
    return json.loads((ROOT / "results" / "result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "actual_direct_layer_numbers",
        "batch_false_claim_values_expected_false",
        "batch_gate_values_expected_false",
        "conditional_actual_head_layer_count",
        "deterministic_counterloop_layer_numbers",
        "directory_names",
        "expected_batch_publication_files",
        "expected_batch_tree_files",
        "expected_review_publication_files",
        "expected_upstream_publication_files",
        "false_claims",
        "finite_rows_are_coefficient_ledger_reproduction_only",
        "finite_typed_fiber_rows",
        "gates",
        "layer_count",
        "layers",
        "open_obligation_count",
        "open_obligations",
        "paper_numbers",
        "review_false_claim_values_expected_false",
        "review_gate_values_expected_false",
        "review_layer_number",
        "rh241_frontier",
        "rh288_status",
        "scope",
        "source_anchors",
        "status",
        "terminal_lag_route",
        "typed_identities",
        "typed_separation_theorem",
        "unconditional_scoped_conclusion_count",
        "upstream_audit",
        "upstream_false_claim_values_expected_false",
        "upstream_gate_values_expected_false",
        "verdict",
    }


def test_nine_upstream_result_ledgers_have_exact_false_counts():
    gate_values = []
    false_claim_values = []
    observed_counts = []
    for name in DIRECTORY_NAMES[:-1]:
        source = json.loads((PAPERS / name / "results/result.json").read_text(encoding="utf-8"))
        assert len(source["gates"]) == 5
        gate_values.extend(source["gates"].values())
        observed_counts.append(len(source["false_claims"]))
        false_claim_values.extend(source["false_claims"].values())
    assert observed_counts == list(UPSTREAM_FALSE_CLAIM_COUNTS)
    assert len(gate_values) == 45
    assert not any(gate_values)
    assert len(false_claim_values) == 129
    assert not any(false_claim_values)


def test_upstream_audit_rows_match_source_counts_exactly():
    rows = _result()["upstream_audit"]
    assert [row["paper"] for row in rows] == list(range(352, 361))
    assert [row["false_claim_count"] for row in rows] == list(UPSTREAM_FALSE_CLAIM_COUNTS)
    assert sum(row["gate_count"] for row in rows) == 45
    assert sum(row["false_claim_count"] for row in rows) == 129
    assert not any(row["gate_true_count"] for row in rows)
    assert not any(row["false_claim_true_count"] for row in rows)


def test_result_locks_typed_nonpromotion_and_open_bridge():
    data = _result()
    identities = data["typed_identities"]
    assert set(identities) == {
        "direct",
        "fiber",
        "head_defect",
        "p_to_q_promotion_requires_same_clock_defect_control",
    }
    assert identities["direct"] == "p=tau-a=q-d"
    assert identities["head_defect"] == "d=h-s"
    assert identities["fiber"] == "q=p+d_and_h=s+d"
    assert identities["p_to_q_promotion_requires_same_clock_defect_control"] is True
    theorem = data["typed_separation_theorem"]
    assert theorem["only_named_actual_head_bridge"] == "same_clock_unnormalized_D_(4k)(R)->0"
    assert theorem["bridge_proved_in_batch"] is False
    assert theorem["physical_counterexample_constructed"] is False


def test_finite_rows_are_never_promoted_to_physical_evidence():
    data = _result()
    assert data["finite_rows_are_coefficient_ledger_reproduction_only"] is True
    for row in data["finite_typed_fiber_rows"]:
        assert row["physical_operator_constructed"] is False
        assert row["spectral_submultiset_claimed"] is False


def test_dependency_manifest_rehashes_all_review_publication_files():
    manifest = json.loads(
        (ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["file_count"] == 20
    assert len(manifest["files"]) == 20
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_individual_and_batch_archive_verification_are_exact():
    individual = json.loads(
        (ROOT / "results/archive_verification.json").read_text(encoding="utf-8")
    )
    batch = json.loads(
        (ROOT / "results/batch_archive_verification.json").read_text(encoding="utf-8")
    )
    assert individual["failure_count"] == 0
    assert individual["failures"] == []
    assert individual["file_count"] == 20
    assert batch["failure_count"] == 0
    assert batch["failures"] == []
    assert batch["paper_numbers"] == list(range(352, 362))
    assert batch["file_count"] == 176


def test_batch_manifest_rehashes_all_176_publication_files():
    manifest = json.loads(
        (ROOT / "results/batch_dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["status"] == "rh352_361_batch_publication_manifest"
    assert manifest["paper_numbers"] == list(range(352, 362))
    assert manifest["file_count"] == 176
    assert len(manifest["files"]) == 176
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((PAPERS / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "ten-layer-signed-completion-and-upper-counterloop-review.pdf"
    ).read_bytes()
