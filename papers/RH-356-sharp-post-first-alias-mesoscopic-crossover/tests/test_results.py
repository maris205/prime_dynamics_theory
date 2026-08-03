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


def test_result_keeps_claim_firewall_closed():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["verdict"] == "GO_SCOPED"
    assert all(value is False for value in payload["gates"].values())
    assert all(value is False for value in payload["false_claims"].values())
    assert payload["conditional_actual_head"]["hypothesis_proved_here"] is False
    assert payload["conditional_actual_head"]["root_or_rank_transfer"] is False


def test_result_records_the_integer_phase_ceiling():
    payload = _strict_load(ROOT / "results/result.json")
    phase = payload["integer_phase"]
    assert phase["single_limit"] is False
    assert phase["phase_limit_set"] == "[0,1]"
    assert phase["liminf"] == "x^c/(x-1)"
    assert phase["limsup"] == "x^(c+1)/(x-1)"


def test_result_keeps_mesoscopic_and_linear_depth_separate():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["uniform_law"]["domain"] == "1<=L<=ell_k_with_ell_k=o(k)"
    assert payload["uniform_law"]["growing_depth_only"].startswith("L->infinity")
    assert "x^L-1" in payload["uniform_law"]["fixed_depth"]
    assert payload["uniform_law"]["C_M_cancels"] is True
    assert payload["false_claims"]["mesoscopic_formula_extended_to_linear_depth"] is False


def test_result_retains_floor_phase_and_conditional_actual_scope():
    payload = _strict_load(ROOT / "results/result.json")
    assert payload["integer_phase"]["single_limit"] is False
    actual = payload["conditional_actual_head"]
    assert actual["hypothesis_proved_here"] is False
    assert actual["odd_post_budget_tends_to_zero"] is True
    assert actual["inherits_mesoscopic_ratio_only_conditionally"] is True


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
