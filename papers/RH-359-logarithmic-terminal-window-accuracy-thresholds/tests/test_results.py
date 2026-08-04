import hashlib
import json
from pathlib import Path

from experiments.build_result import result_status


ROOT = Path(__file__).resolve().parents[1]


def _strict_load(path):
    def hook(pairs):
        output = {}
        for key, value in pairs:
            if key in output:
                raise ValueError(f"duplicate key: {key}")
            output[key] = value
        return output

    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=hook,
        parse_constant=lambda value: (_ for _ in ()).throw(
            ValueError(f"nonfinite JSON constant: {value}")
        ),
    )


def test_result_artifact_matches_generator():
    assert _strict_load(ROOT / "results/result.json") == result_status()


def test_phase_and_minimal_window_claims_are_locked():
    payload = _strict_load(ROOT / "results/result.json")
    phase = payload["polynomial_phase"]
    assert phase["phase_limit_set"] == "[0,1]"
    assert phase["normalized_error_limit_set"] == "[x^(-c),x^(1-c)]"
    assert phase["unique_constant"] is False
    window = payload["minimal_window"]
    assert window["correction_limit_set"] == "[0,1]"
    assert window["universal_exact_integer_selection"] is False


def test_accuracy_exponents_and_conditional_scope_are_typed():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["accuracy_exponents"]["superlog_sublinear_is_superpolynomial"] is True
    actual = payload["conditional_actual_head"]
    assert actual["hypothesis_proved_here"] is False
    assert actual["phase_exponent_and_minimal_width_inherited"] is True
    assert actual["root_rank_spectrum_or_determinant_transfer"] is False


def test_forbidden_claims_and_gates_stay_false():
    payload = _strict_load(ROOT / "results/result.json")
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())


def test_rows_are_reproduction_only_and_next_route_is_read_only():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["finite_rows_are_formula_reproduction_only"] is True
    assert len(payload["exact_minimal_width_rows"]) == 4
    assert len(payload["phase_diagnostic_rows"]) == 4
    assert len(payload["finite_phase_cover_rows"]) == 3
    assert payload["next_candidate"]["paper"] == "RH-360"
    assert payload["next_candidate"]["status"].startswith("read_only")


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = _strict_load(ROOT / "results/dependency_manifest.json")
    assert manifest["file_count"] == 18
    assert len(manifest["files"]) == 18
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_archive_verification_is_clean():
    verification = _strict_load(ROOT / "results/archive_verification.json")
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["file_count"] == 18


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "logarithmic-terminal-window-accuracy-thresholds.pdf"
    ).read_bytes()
