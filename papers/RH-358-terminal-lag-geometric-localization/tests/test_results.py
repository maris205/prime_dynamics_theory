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


def test_uniform_profile_keeps_every_full_range_factor():
    payload = _strict_load(ROOT / "results/result.json")
    profile = payload["uniform_terminal_profile"]
    assert profile["relative_errors_uniform"] is True
    assert profile["x_minus_q_alone_uniform"] is False
    assert "C_M^(q/k)" in profile["source_locked"]
    assert "(2k-1)/(2k-1-q)" in profile["source_locked"]
    assert "1-x^(-(k-1-q))" in profile["source_locked"]


def test_lag_regimes_and_geometric_limits_are_locked():
    payload = _strict_load(ROOT / "results/result.json")
    regimes = payload["lag_regimes"]
    assert regimes["sublinear"].startswith("q=o(k)")
    assert "2*C_M^theta/(2-theta)" in regimes["linear"]
    assert "1-x^(-ell)" in regimes["fixed_residual_depth"]
    geometric = payload["geometric_localization"]
    assert geometric["ell1_convergence"] is True
    assert geometric["total_variation_convergence"] is True
    assert geometric["mean_limit"] == "1/(x-1)"
    assert geometric["variance_limit"] == "x/(x-1)^2"
    assert geometric["vanishing_truncation_iff"] == "q->infinity"


def test_actual_scope_gates_and_forbidden_claims_stay_closed():
    payload = _strict_load(ROOT / "results/result.json")
    actual = payload["conditional_actual_head"]
    assert actual["hypothesis_proved_here"] is False
    assert actual["uniform_coordinatewise_lag_ratio_inherited"] is True
    assert actual["first_two_lag_moments_inherited"] is True
    assert actual["moment_transfer_uses_tv_alone"] is False
    assert actual["root_rank_spectrum_or_determinant_transfer"] is False
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())


def test_rows_are_reproduction_only_and_next_route_is_read_only():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["finite_rows_are_formula_reproduction_only"] is True
    assert len(payload["exact_profile_rows"]) == 4
    assert len(payload["uniform_error_envelope_rows"]) == 4
    assert len(payload["distribution_metric_rows"]) == 4
    assert len(payload["linear_diagnostic_rows"]) == 4
    assert len(payload["fixed_residual_diagnostic_rows"]) == 4
    assert payload["next_candidate"]["paper"] == "RH-359"
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
        ROOT / "terminal-lag-geometric-localization.pdf"
    ).read_bytes()
