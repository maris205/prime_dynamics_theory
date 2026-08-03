import hashlib
import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _result():
    return json.loads((ROOT / "results/result.json").read_text(encoding="utf-8"))


def test_result_file_is_deterministic_and_schema_is_strict():
    data = _result()
    assert data == result_payload()
    assert set(data) == {
        "band_corollary",
        "clock",
        "constants",
        "false_claims",
        "finite_rows",
        "finite_rows_are_formula_reproduction_only",
        "gates",
        "linear_frontiers",
        "raw_method_boundary",
        "scope",
        "source_anchors",
        "source_types",
        "status",
        "tail_theorem",
        "verdict",
    }


def test_tail_and_band_theorems_are_explicit():
    data = _result()
    assert data["tail_theorem"]["all_orders_included"] is True
    assert data["tail_theorem"]["sublinear_root_ceiling"].endswith("<1")
    assert data["band_corollary"]["near_alias_band"].startswith("x^(-k)")
    assert data["band_corollary"]["full_log_tail"].startswith("x^(-k)")


def test_finite_rows_cover_odd_and_even_lower_cuts():
    rows = _result()["finite_rows"]
    assert len(rows) == 4
    assert {row["N_parity"] for row in rows} == {"odd", "even"}
    assert all(row["finite_formula_only"] for row in rows)


def test_threshold_decimals_are_diagnostic_only():
    frontiers = _result()["linear_frontiers"]
    assert frontiers["alpha_natural_exact"].startswith("log(")
    assert frontiers["alpha_alias_exact"].startswith("log(")
    assert frontiers["diagnostics_are_not_interval_certificates"] is True


def test_raw_boundary_is_method_only():
    boundary = _result()["raw_method_boundary"]
    assert boundary["strict_global_lower"] == "9604/7225"
    assert boundary["global_lower_is_superunit"] is True
    assert boundary["method_boundary_only"] is True


def test_all_gates_and_forbidden_claims_remain_false():
    data = _result()
    assert len(data["gates"]) == 5
    assert not any(data["gates"].values())
    assert len(data["false_claims"]) == 13
    assert not any(data["false_claims"].values())


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = json.loads(
        (ROOT / "results/dependency_manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["file_count"] == 17
    assert len(manifest["files"]) == 17
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_individual_archive_verification_is_exact():
    verification = json.loads(
        (ROOT / "results/archive_verification.json").read_text(encoding="utf-8")
    )
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["file_count"] == 17


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "parity-free-near-alias-direct-tail-envelope.pdf"
    ).read_bytes()
