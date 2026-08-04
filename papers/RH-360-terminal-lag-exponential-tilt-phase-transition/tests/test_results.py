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


def test_three_transform_regimes_are_locked():
    payload = _strict_load(ROOT / "results/result.json")
    transform = payload["generating_function"]
    assert "0<=z<x" in transform["subcritical"]
    assert "tau+log(C_M)" in transform["critical"]
    assert "C_M" in transform["supercritical"]
    assert "max(0,log(z/x))" in transform["free_energy"]


def test_tilted_phase_diagram_is_not_spectral():
    payload = _strict_load(ROOT / "results/result.json")
    diagram = payload["tilted_phase_diagram"]
    assert "geometric_ratio_z/x" in diagram["subcritical"]
    assert "density" in diagram["critical"]
    assert "geometric_ratio_x/z" in diagram["supercritical"]
    assert diagram["spectral_probability_interpretation"] is False


def test_conditional_scope_and_gates_stay_closed():
    payload = _strict_load(ROOT / "results/result.json")
    actual = payload["conditional_actual_head"]
    assert actual["hypothesis_proved_here"] is False
    assert actual["all_nonnegative_tilt_sequences_inherited"] is True
    assert actual["root_rank_spectrum_or_determinant_transfer"] is False
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())


def test_rows_and_review_trigger_are_typed():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["finite_rows_are_formula_reproduction_only"] is True
    assert len(payload["subcritical_transform_rows"]) == 4
    assert len(payload["critical_rows"]) == 4
    assert len(payload["supercritical_transform_rows"]) == 4
    assert len(payload["subcritical_tilt_rows"]) == 4
    assert len(payload["supercritical_tilt_rows"]) == 4
    assert payload["next_paper"]["paper"] == "RH-361"
    assert payload["next_paper"]["status"].endswith("not_proved_here")


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
        ROOT / "terminal-lag-exponential-tilt-phase-transition.pdf"
    ).read_bytes()
