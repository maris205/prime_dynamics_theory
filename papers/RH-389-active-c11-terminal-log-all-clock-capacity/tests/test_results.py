from __future__ import annotations

from copy import deepcopy
import json
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
import verify_tao_source  # noqa: E402
from terminal_log_capacity import core  # noqa: E402


def _stored(name: str) -> object:
    return verify_tao_source.loads_strict((ROOT / "results" / name).read_text(encoding="utf-8"))


def test_result_is_fresh_exact_and_all_pass() -> None:
    stored = _stored("result.json")
    fresh = build_result.build_payload()
    assert verify_tao_source.exact_equal(stored, fresh)
    assert stored["all_pass"] is True
    assert stored["certificate_fixture"] == {
        "canonical_bytes": 208648,
        "field_verified": True,
        "fresh_verified": True,
        "pass": True,
        "sha256": "b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020",
    }


def test_result_theorem_quantifiers_capacity_and_reflection_are_exact() -> None:
    theorem = build_result.build_payload()["theorem"]
    assert theorem["absolute_capacity"] == "for every fixed q>=1, G_log(q)=6/pi^2-kappa2/2"
    assert theorem["terminal_score"].startswith("S_X^omega(q,f):=")
    assert "with mu0(m)=mu(m) for m>=1 and 0 for m<=0" in theorem["terminal_score"]
    assert theorem["limit_theorem"].startswith("for every fixed q>=1, every fixed f in A_q")
    assert "every 1<=omega(X)<=X with omega(X)->infinity" in theorem["limit_theorem"]
    assert theorem["capacity_definition"].startswith("G_log(q):=max_(f in A_q)|L_q(f)|")
    assert theorem["all_clock_order"].endswith("no lim_X sup_q claim")
    assert theorem["fixed_data_quantifier"].startswith("q and the safe q-periodic table family are fixed")
    assert theorem["normalization"].startswith("1<=omega(X)<=X,omega(X)->infinity")
    assert theorem["limit_order"].startswith("take each fixed-table terminal-log limit")
    assert theorem["optimizer"].endswith("for every fixed q")
    assert "c02,c11,c22 negate" in theorem["reflection"]
    assert theorem["active_c11_input"].startswith("D(n)=n-2,V(n)=n,determinant=2")


def test_global_projection_charge_and_reflection_are_hard_gates() -> None:
    certificate = build_result.build_payload()["certificate"]
    projection = certificate["contracts"]["projection_global_contract"]
    charge = certificate["analytic_rows"][4]["charge_contract"]
    reflection = certificate["analytic_rows"][5]["global_reflection_contract"]
    assert projection["pass"] is True and projection["projection_compatibility_failures"] == 0
    assert charge["pass"] is True
    assert charge["self_loop_moduli_for_offset_minus_two"] == [1, 2]
    assert charge["baseline_attains_for_every_fixed_q"] is True
    assert reflection["pass"] is True
    assert reflection["coefficient_sign_pattern"] == ["+", "-", "-", "+", "+", "-"]
    assert reflection["reflection_compatibility_failure_count"] == 0


def test_source_closure_is_exact_95_plus_three() -> None:
    locks = build_result.build_payload()["source_locks"]
    assert (locks["git_count"], locks["remote_count"], locks["logical_count"]) == (95, 3, 98)
    assert locks["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert locks["logical_digest_pass"] is True
    assert locks["pass"] is True
    assert locks["remote"]["source_keys"] == [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
        "tao-cambridge-2016-logarithmic-chowla",
    ]


def test_mutation_result_is_exact_24_of_24() -> None:
    mutations = build_result.build_payload()["mutations"]
    assert mutations["count"] == 24
    assert mutations["all_pass"] is True
    assert [row["name"] for row in mutations["rows"]] == list(core.MUTATION_NAMES)
    assert all(row["changed"] is True and row["rejected"] is True for row in mutations["rows"])
    assert "without certificate/group builders" in mutations["verification_mode"]


def test_certificate_and_logical_digest_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
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


def test_remote_canonical_rebinding_is_a_top_level_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(source_locks, "TAO_CANONICAL_SHA256", "0" * 64)
    payload = build_result.build_payload()
    assert payload["source_locks"]["remote"]["pass"] is False
    assert payload["source_locks"]["pass"] is False
    assert payload["all_pass"] is False


def test_malformed_sealed_constants_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "CERTIFICATE_FIXTURE_SHA256", "not-a-sha")
    with pytest.raises(ValueError, match="malformed"):
        build_result.build_payload()
    monkeypatch.undo()
    monkeypatch.setattr(source_locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", "not-a-sha")
    with pytest.raises(ValueError, match="malformed"):
        build_result.build_payload()


def test_gates_firewalls_declarations_and_source_roles_are_exact() -> None:
    payload = build_result.build_payload()
    assert payload["gates"] == build_result.GATES
    assert not any(payload["gates"].values())
    assert payload["forbidden_claims"] == build_result.FORBIDDEN
    assert not any(payload["forbidden_claims"].values())
    declarations = payload["declarations"]
    assert declarations["active_c11_is_in_scope"] is True
    assert declarations["network_fetch_performed_by_build"] is False
    assert declarations["external_payload_vendored"] is False
    assert declarations["certificate_rows_are_analytic_proof"] is False
    assert declarations["inherited_Johnston_Yang_and_Maynard_are_RH389_proof_inputs"] is False
    assert declarations["analytic_source_for_full_mobius_correlation"].startswith("TPC-137")
    assert declarations["Tao_role"].endswith("only")


def test_schema_is_fresh_closed_and_officially_valid() -> None:
    stored = _stored("result.schema.json")
    fresh = build_schema.build_schema()
    assert verify_tao_source.exact_equal(stored, fresh)
    assert stored["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert stored["additionalProperties"] is False
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft202012Validator.check_schema(stored)
    assert list(jsonschema.Draft202012Validator(stored).iter_errors(build_result.build_payload())) == []


def test_schema_rejects_bool_for_int_extra_list_drift_and_nonfinite() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = build_schema.build_schema()
    candidate = build_result.build_payload()
    candidate["certificate"]["truth_rows"][0]["table_id"] = False
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["extra"] = 1
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["certificate"]["scope_rows"].append(deepcopy(candidate["certificate"]["scope_rows"][0]))
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    with pytest.raises(ValueError):
        verify_tao_source.loads_strict('{"x":Infinity}')
    with pytest.raises(ValueError):
        verify_tao_source.loads_strict('{"x":1,"x":2}')


def test_full_remote_object_and_result_type_mutations_are_distinguished() -> None:
    payload = build_result.build_payload()
    tao = payload["source_locks"]["remote"]["objects"][2]
    for path, bad in (
        ("doi", "10.0/wrong"),
        ("bytes", 534085),
        ("pdf_final_url", "https://example.invalid/source.pdf"),
        ("redistributable_in_release", False),
    ):
        candidate = deepcopy(tao)
        candidate[path] = bad
        assert not core.exact_equal(candidate, tao)
    candidate = deepcopy(payload)
    candidate["declarations"]["git_source_rows"] = True
    assert not core.exact_equal(candidate, payload)


def test_optimized_builder_matches_stored_result() -> None:
    code = (
        "import json,sys;sys.path[:0]=['src','experiments'];"
        "from build_result import build_payload;"
        "print(json.dumps(build_payload(),sort_keys=True,separators=(',',':'),allow_nan=False))"
    )
    completed = subprocess.run(
        [sys.executable, "-B", "-OO", "-c", code],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert core.exact_equal(verify_tao_source.loads_strict(completed.stdout), build_result.build_payload())
