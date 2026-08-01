import hashlib
import json
from pathlib import Path

from experiments.build_result import result_payload


ROOT = Path(__file__).resolve().parents[1]


def _json(name: str):
    return json.loads((ROOT / "results" / name).read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def test_result_file_is_deterministic():
    assert _json("result.json") == result_payload()


def test_source_lock_uses_actual_head_and_strict_prefix():
    data = _json("result.json")
    source = data["source_lock"]
    assert source["actual_head"].startswith("algebraic_nonperipheral")
    assert source["counterloop_rank"] == "m_k=2k-2"
    assert source["strict_prefix"] == "2<=n<4k_contains_2k_excludes_4k"
    assert source["endpoint_singular_rank_identified_with_head_rank"] is False


def test_rank_lock_and_shifted_uniqueness_are_exactly_scoped():
    data = _json("result.json")
    rank = data["rank_lock"]
    assert rank["o1_matching_forces_eventual_exact_rank"] is True
    assert rank["actual_rank_law_available"] is False
    shifted = data["shifted_moment_uniqueness"]
    assert shifted["numerator_degree_bound"] == "2N-1"
    assert shifted["zero_order"] == "2N"
    assert shifted["conclusion"] == "X=Y_as_multisets"


def test_hidden_shell_counterexample_keeps_physical_firewall():
    shell = _json("result.json")["hidden_shell_counterexample"]
    assert shell["strict_prefix_moments_equal"] is True
    assert shell["D_4k"] == "0_exactly"
    assert shell["padded_distance_lower_bound"] == "4kq=2k"
    assert shell["added_genus_one_factor"] == "1-(3z/4)^(4k)"
    assert shell["actual_noisy_operator"] is False


def test_rh299_threshold_and_route_verdict():
    data = _json("result.json")
    bridge = data["rh299_specialization"]
    assert bridge["global_threshold"].startswith("1.926813889034")
    assert bridge["local_threshold"].startswith("0.926813889034")
    assert bridge["actual_matching_theorem_available"] is False
    verdict = data["route_verdict"]
    assert verdict["rh299_without_rank_law_cap_rate"] == "STOP_SCOPED"
    assert verdict["aggregate_moment_fourier_hardy"] == "NOT_TESTABLE_open"
    assert verdict["direct_annular"] == "NOT_TESTABLE_open"


def test_claim_firewall_and_gates_are_strict_booleans():
    data = _json("result.json")
    assert len(data["false_claims"]) == 22
    assert all(type(value) is bool and value is False for value in data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert all(type(value) is bool and value is False for value in data["gates"].values())


def test_publication_manifest_has_exact_15_file_scope_and_valid_hashes():
    manifest = _json("dependency_manifest.json")
    assert manifest["file_count"] == 15
    assert len(manifest["files"]) == 15
    assert "results/dependency_manifest.json" not in manifest["files"]
    assert "results/archive_verification.json" not in manifest["files"]
    assert not any(name.endswith((".aux", ".log", ".fls", ".fdb_latexmk", ".bbl", ".blg")) for name in manifest["files"])
    for relative, expected in manifest["files"].items():
        assert _sha256(ROOT / relative) == expected


def test_archive_verification_is_closed():
    verification = _json("archive_verification.json")
    assert verification["file_count"] == 15
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["status"].endswith("_archive_verified")
