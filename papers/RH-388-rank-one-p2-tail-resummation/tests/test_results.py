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
from rank_one_p2 import exact_equal, loads_strict  # noqa: E402


def test_result_is_fresh_exact_and_all_pass() -> None:
    stored = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    fresh = build_result.build_payload()
    assert exact_equal(stored, fresh)
    assert stored["all_pass"] is True
    assert stored["certificate_fixture"] == {
        "canonical_bytes": build_result.CERTIFICATE_FIXTURE_BYTES,
        "sha256": build_result.CERTIFICATE_FIXTURE_SHA256,
        "pass": True,
    }


def test_result_theorem_contract_retains_pi_squared_and_sharp_scope() -> None:
    payload = build_result.build_payload()
    theorem = payload["theorem"]
    assert theorem["finite_bound"].startswith("pi^2*")
    assert theorem["uniform_window"] == "as y->infinity,max_(1<=K<=floor(3L))|GapP-GapK|/P_2 -> 0"
    assert theorem["limit_variable"] == "y->infinity"
    assert theorem["bounded_gap_scalar_necessity"].endswith(">=1/2")
    assert theorem["bounded_gap_endpoint_necessity_I"].endswith(">=X_infinity")
    assert theorem["necessity_scope"] == "the frozen P/J/I smooth-surrogate hierarchy only"


def test_source_closure_is_exact_77_plus_two() -> None:
    payload = build_result.build_payload()
    locks = payload["source_locks"]
    assert (locks["git_count"], locks["remote_count"], locks["logical_count"]) == (77, 2, 79)
    assert locks["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert locks["logical_digest_pass"] is True
    assert locks["pass"] is True
    assert locks["remote"]["source_keys"] == [
        "johnston-yang-arxiv-2204.01980v2",
        "maynard-annals-2015-small-gaps",
    ]


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


def test_malformed_sealed_constants_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(build_result, "CERTIFICATE_FIXTURE_SHA256", "not-a-sha")
    with pytest.raises(ValueError, match="malformed"):
        build_result.build_payload()
    monkeypatch.undo()
    monkeypatch.setattr(source_locks, "EXPECTED_LOGICAL_SOURCE_DIGEST", "not-a-sha")
    with pytest.raises(ValueError, match="malformed"):
        build_result.build_payload()


def test_gates_firewalls_and_declarations_are_exact() -> None:
    payload = build_result.build_payload()
    assert payload["gates"] == build_result.GATES
    assert not any(payload["gates"].values())
    assert payload["forbidden_claims"] == build_result.FORBIDDEN
    assert not any(payload["forbidden_claims"].values())
    assert payload["declarations"]["network_fetch_performed_by_build"] is False
    assert payload["declarations"]["external_payload_vendored"] is False


def test_schema_is_fresh_closed_and_validates_exact_result() -> None:
    stored = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    fresh = build_schema.build_schema()
    assert exact_equal(stored, fresh)
    assert stored["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert stored["additionalProperties"] is False
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.Draft202012Validator.check_schema(stored)
    assert list(jsonschema.Draft202012Validator(stored).iter_errors(build_result.build_payload())) == []


def test_schema_rejects_bool_for_int_extra_and_nonfinite() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = build_schema.build_schema()
    candidate = build_result.build_payload()
    candidate["certificate"]["ledger_rows"][0]["gradient_bound"] = True
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    candidate = build_result.build_payload()
    candidate["extra"] = 1
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(candidate))
    with pytest.raises(ValueError):
        loads_strict('{"x":Infinity}')


def test_full_object_remote_mutations_are_distinguished() -> None:
    payload = build_result.build_payload()
    maynard = payload["source_locks"]["remote"]["objects"][1]
    for path, bad in (
        ("doi", "10.0/wrong"),
        ("bytes", 528114),
        ("pdf_final_url", "https://example.invalid/source.pdf"),
        ("redistributable_in_release", True),
    ):
        candidate = deepcopy(maynard)
        candidate[path] = bad
        assert not exact_equal(candidate, maynard)


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
    assert exact_equal(loads_strict(completed.stdout), build_result.build_payload())
