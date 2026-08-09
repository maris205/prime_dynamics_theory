from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "experiments", ROOT / "src"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import build_result  # noqa: E402
import build_schema  # noqa: E402
import source_locks  # noqa: E402
from growing_rank_filtration import exact_equal, loads_strict  # noqa: E402


def _stored(name: str) -> dict[str, object]:
    return loads_strict((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_result_is_fresh_byte_exact_and_all_pass() -> None:
    stored_path = ROOT / "results" / "result.json"
    stored = _stored("result.json")
    fresh = build_result.build_payload()
    assert exact_equal(stored, fresh)
    assert stored_path.read_bytes() == build_result.pretty_json_bytes(fresh)
    assert stored["all_pass"] is True
    assert stored["certificate_fixture"] == {
        "canonical_bytes": 17_571,
        "sha256": "e2116abd4aeb910c24ee470a520623f29f1f454bb9b5293840875da091682b3b",
        "pass": True,
    }


def test_theorem_contract_has_exact_growing_and_fixed_rank_quantifiers() -> None:
    theorem = build_result.build_payload()["theorem"]
    assert theorem["rank_window"] == "exact integers 2<=s<=S_y=floor((1-delta)*log(L)/log(7))"
    assert theorem["factorial_window"] == "exact integers 1<=K<=floor((2s-1)*L)"
    assert theorem["B_s_c"] == "1/((1-x^-2)^(s+1)*(1-c/(x^2-1)))"
    assert theorem["normalized_coordinate_bound"].startswith("|PhiP_c-Psi_(c;s,K)|/K_s<=")
    assert theorem["endpoint_bound"].startswith("pi^2*")
    assert theorem["uniform_window"].startswith("as y->infinity,max_(2<=s<=S_y")
    assert theorem["eventual_nonempty"] == "eventually S_y>=2"
    assert theorem["gamma_positivity"] == "gamma_(r)>0 for every exact integer r>=1"
    assert theorem["fixed_s_scalar_necessity"].startswith("for fixed exact integer s>=2")
    assert theorem["fixed_s_scalar_necessity"].endswith(">=1/2")
    assert theorem["GapI_less_r_definition"].startswith("F((sum_(j<r)c^j*P_j/j")
    assert theorem["GapJ_less_r_definition"].startswith("F((sum_(j<r)c^j*P_j/j")
    assert theorem["fixed_s_endpoint_necessity_I"].endswith(">=gamma_(r)/2")
    assert theorem["fixed_s_endpoint_necessity_J"].endswith(">=gamma_(r)/2")
    assert theorem["necessity_scope"] == "fixed s only in the frozen P/J/I hierarchy"


def test_source_closure_and_roles_are_exact_87_plus_two() -> None:
    payload = build_result.build_payload()
    locks = payload["source_locks"]
    assert (locks["git_count"], locks["remote_count"], locks["logical_count"]) == (87, 2, 89)
    assert locks["git"]["all_git_source_digest"] == source_locks.EXPECTED_ALL_GIT_SOURCE_DIGEST
    assert locks["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert locks["logical_digest_pass"] is True
    assert locks["pass"] is True
    assert payload["source_roles"] == {
        "johnston_yang": "prime-counting envelope inherited through the RH-386/RH-388 closure",
        "maynard": "fixed-s consecutive bounded-gap necessity",
        "excluded_as_irrelevant": ["RH-389", "TPC-137", "Tao active-log source"],
    }


def test_twenty_four_mutations_are_hard_gated() -> None:
    mutations = build_result.build_payload()["mutations"]
    assert mutations["count"] == 24
    assert len(mutations["names"]) == 24
    assert len(mutations["results"]) == 24
    assert all(row["rejected"] is True for row in mutations["results"])
    assert mutations["all_pass"] is True


def test_certificate_source_and_logical_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "CERTIFICATE_FIXTURE_SHA256", "0" * 64)
    payload = build_result.build_payload()
    assert payload["certificate_fixture"]["pass"] is False
    assert payload["all_pass"] is False
    monkeypatch.undo()

    monkeypatch.setattr(source_locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", "0" * 64)
    payload = build_result.build_payload()
    assert payload["source_locks"]["logical_digest_pass"] is False
    assert payload["source_locks"]["pass"] is False
    assert payload["all_pass"] is False
    monkeypatch.undo()

    monkeypatch.setattr(build_result, "EXPECTED_LOGICAL_SOURCE_DIGEST", "0" * 64)
    assert build_result.build_payload()["all_pass"] is False


def test_mutation_gate_rebinding_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    rows = deepcopy(build_result.mutation_results())
    rows[0]["rejected"] = False
    monkeypatch.setattr(build_result, "mutation_results", lambda: rows)
    payload = build_result.build_payload()
    assert payload["mutations"]["all_pass"] is False
    assert payload["all_pass"] is False


def test_malformed_constants_and_bool_aliases_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "CERTIFICATE_FIXTURE_SHA256", "not-a-sha")
    with pytest.raises(ValueError, match="malformed"):
        build_result.build_payload()
    monkeypatch.undo()

    attacked_gates = dict(build_result.GATES)
    attacked_gates["A_intrinsic_determinant"] = 0
    monkeypatch.setattr(build_result, "GATES", attacked_gates)
    with pytest.raises(TypeError, match="exact booleans"):
        build_result.build_payload()


def test_forbidden_membership_deletion_and_empty_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    attacked = dict(build_result.FORBIDDEN)
    del attacked["growing_s_necessity"]
    monkeypatch.setattr(build_result, "FORBIDDEN", attacked)
    with pytest.raises(ValueError, match="firewall membership"):
        build_result.build_payload()
    monkeypatch.undo()
    monkeypatch.setattr(build_result, "FORBIDDEN", {})
    with pytest.raises(ValueError, match="firewall membership"):
        build_result.build_payload()


def test_gates_firewalls_and_declarations_are_exact() -> None:
    payload = build_result.build_payload()
    assert payload["gates"] == build_result.GATES
    assert not any(payload["gates"].values())
    assert payload["forbidden_claims"] == build_result.FORBIDDEN
    assert not any(payload["forbidden_claims"].values())
    assert payload["declarations"] == {
        "network_fetch_performed_by_build": False,
        "external_payload_vendored": False,
        "finite_rows_are_analytic_proof": False,
        "effective_least_y_computed": False,
        "git_source_rows": 87,
        "remote_logical_objects": 2,
        "logical_source_rows": 89,
    }


def _assert_recursively_closed(node: object) -> None:
    if type(node) is not dict:
        return
    if node.get("type") == "object":
        assert node["additionalProperties"] is False
        assert node["required"] == sorted(node["properties"])
        for child in node["properties"].values():
            _assert_recursively_closed(child)
    elif node.get("type") == "array":
        assert node["items"] is False
        assert node["minItems"] == node["maxItems"]
        for child in node.get("prefixItems", []):
            _assert_recursively_closed(child)


def test_schema_is_fresh_byte_exact_and_recursively_closed() -> None:
    stored_path = ROOT / "results" / "result.schema.json"
    stored = _stored("result.schema.json")
    fresh = build_schema.build_schema()
    assert exact_equal(stored, fresh)
    assert stored_path.read_bytes() == build_result.pretty_json_bytes(fresh)
    assert stored["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert stored["$id"] == "https://example.invalid/schemas/RH-390-result.schema.json"
    _assert_recursively_closed(stored)


def test_official_draft202012_schema_and_instance() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = build_schema.build_schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(build_result.build_payload())) == []


def test_schema_rejects_bool_for_int_extra_member_and_remote_rebinding() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = build_schema.build_schema()
    candidate = build_result.build_payload()
    candidate["certificate_fixture"]["canonical_bytes"] = True
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["extra"] = 1
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["source_locks"]["remote"]["objects"][1]["redistributable_in_release"] = True
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))


def test_strict_stored_json_rejects_duplicates_nonfinite_and_nonobjects() -> None:
    for text in ('{"a":1,"a":2}', '{"x":NaN}', '{"x":Infinity}', '[]', '1', 'null'):
        with pytest.raises((TypeError, ValueError)):
            loads_strict(text)


def test_optimized_builders_match_stored_result_and_schema() -> None:
    code = (
        "import json,sys;sys.path[:0]=['src','experiments'];"
        "from build_result import build_payload;from build_schema import build_schema;"
        "print(json.dumps({'result':build_payload(),'schema':build_schema()},sort_keys=True,separators=(',',':'),allow_nan=False))"
    )
    completed = subprocess.run(
        [sys.executable, "-B", "-OO", "-c", code],
        cwd=ROOT,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    optimized = loads_strict(completed.stdout)
    assert exact_equal(optimized["result"], _stored("result.json"))
    assert exact_equal(optimized["schema"], _stored("result.schema.json"))


def test_no_cache_artifacts_exist() -> None:
    assert list(ROOT.rglob("__pycache__")) == []
    assert list(ROOT.rglob(".pytest_cache")) == []
