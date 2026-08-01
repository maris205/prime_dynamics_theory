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


def test_construction_and_equal_invariants_are_exactly_scoped():
    data = _json("result.json")
    assert data["verdict"] == "GO_SCOPED_finite_normal_spectral_information_class"
    assert data["construction"]["model_spectra_only"] is True
    invariants = data["rank_and_mass"]
    assert invariants["common_rank"] == "6k-2"
    assert invariants["common_squared_spectral_mass"] == "(2k-2)beta_k^2+481k/200"
    assert invariants["common_maximum_modulus"] == "beta_k"


def test_moment_split_and_weighted_budget_keep_strict_endpoint():
    data = _json("result.json")
    moments = data["moment_ledger"]
    assert moments["both_equal_Y"] == "2<=n<2k"
    assert moments["not_equal_on_entire_strict_prefix"] is True
    assert moments["first_split_order"] == "n=2k"
    budget = data["weighted_budget"]
    assert budget["invisible_D_4k"] == "0_exactly"
    assert budget["visible_D_4k"] == "(21/20)^(2k)+(28/25)^(2k)"
    assert budget["one_over_n_cancellation_retained"] is True


def test_genus_one_factors_and_rank_cap_boundary():
    data = _json("result.json")
    assert data["genus_one_quotients"]["invisible"] == "1-(c*z)^(4k)"
    assert data["genus_one_quotients"]["visible"] == "[1-(a*z)^(2k)][1-(b*z)^(2k)]"
    assert data["underdetermination_corollary"][
        "future_actual_rank_cap_2k_minus_2_excludes_both_examples"
    ] is True


def test_coarse_physical_compatibility_is_not_realization():
    data = _json("result.json")["clock_and_coarse_compatibility"]
    assert data["rank_scale"].endswith("=o(1/sigma)")
    assert data["squared_mass_scale"].endswith("=o(1/sigma)")
    assert data["compatible_only_not_realized"] is True


def test_route_boundary_keeps_actual_transport_open():
    route = _json("result.json")["route_boundary"]
    assert route["actual_alias_inclusive_head_transport"] == "NOT_TESTABLE_open"
    assert route["equal_rank_mass_fixed_order_inference"].startswith("STOP_SCOPED")
    assert route["determinant_gluing"] == "OPEN_not_activated"


def test_claim_firewall_and_gates_are_strict_booleans():
    data = _json("result.json")
    assert len(data["false_claims"]) == 19
    assert all(type(value) is bool and value is False for value in data["false_claims"].values())
    assert set(data["gates"]) == set("ABCDE")
    assert all(type(value) is bool and value is False for value in data["gates"].values())


def test_publication_manifest_has_exact_15_file_scope_and_valid_hashes():
    manifest = _json("dependency_manifest.json")
    assert manifest["file_count"] == 15
    assert len(manifest["files"]) == 15
    assert "results/dependency_manifest.json" not in manifest["files"]
    assert "results/archive_verification.json" not in manifest["files"]
    assert not any(
        name.endswith((".aux", ".log", ".fls", ".fdb_latexmk", ".bbl", ".blg"))
        for name in manifest["files"]
    )
    for relative, expected in manifest["files"].items():
        assert _sha256(ROOT / relative) == expected


def test_archive_verification_is_closed():
    verification = _json("archive_verification.json")
    assert verification["file_count"] == 15
    assert verification["failure_count"] == 0
    assert verification["failures"] == []
    assert verification["status"].endswith("_archive_verified")
