import hashlib
import json
from pathlib import Path

from experiments.build_result import result_status


ROOT = Path(__file__).resolve().parents[1]


def _strict_load(path: Path):
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


def test_uniform_theorem_and_linear_constants_are_locked():
    payload = _strict_load(ROOT / "results/result.json")
    uniform = payload["uniform_endpoint_theorem"]
    assert uniform["relative_errors_uniform"] is True
    assert "1-y_k^(-L)" in uniform["finite_radius"]
    assert "C_M^(1+L/k)" in uniform["source_locked"]
    linear = payload["linear_depth"]
    assert "C_M^(1+alpha)" in linear["post"]
    assert "C_M^alpha" in linear["ratio"]
    assert linear["post_kth_root"] == "x^(1+alpha)"
    assert linear["ratio_kth_root"] == "x^alpha"


def test_boundary_and_phase_firewalls_are_explicit():
    payload = _strict_load(ROOT / "results/result.json")
    boundary = payload["boundary_stitching"]
    assert boundary["bounded_L"] == "retain_1-x^(-L)"
    assert boundary["alpha_zero"].startswith("delete_1-x^(-L)_only_if")
    phase = payload["integer_phase"]
    assert phase["universal_single_limit"] is False
    assert phase["rational_alpha"] == "finite_periodic_phase_orbit"
    assert phase["irrational_alpha"].startswith("phase_limit_set_[0,1]")


def test_actual_scope_gates_and_forbidden_claims_stay_closed():
    payload = _strict_load(ROOT / "results/result.json")
    actual = payload["conditional_actual_head"]
    assert actual["hypothesis_proved_here"] is False
    assert actual["root_or_rank_transfer"] is False
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())


def test_rows_are_reproduction_only_and_next_route_is_read_only():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["finite_rows_are_formula_reproduction_only"] is True
    assert len(payload["exact_fixture_rows"]) == 4
    assert len(payload["uniform_error_envelope_rows"]) == 4
    assert len(payload["linear_diagnostic_rows"]) == 4
    assert len(payload["rational_phase_orbits"]) == 3
    assert payload["next_candidate"]["paper"] == "RH-358"
    assert payload["next_candidate"]["status"].startswith("read_only")


def test_dependency_manifest_rehashes_all_publication_files():
    manifest = _strict_load(ROOT / "results/dependency_manifest.json")
    assert manifest["file_count"] == 17
    assert len(manifest["files"]) == 17
    for relative, expected in manifest["files"].items():
        actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert actual == expected


def test_archive_verification_is_clean():
    verification = _strict_load(ROOT / "results/archive_verification.json")
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["file_count"] == 17


def test_semantic_pdf_is_byte_identical_to_main_pdf():
    assert (ROOT / "main.pdf").read_bytes() == (
        ROOT / "uniform-linear-depth-upper-counterloop-profile.pdf"
    ).read_bytes()
