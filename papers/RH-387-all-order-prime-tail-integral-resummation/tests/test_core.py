from __future__ import annotations

from copy import deepcopy
import json

import pytest

import integral_resummation.core as core


def test_certificate_has_exact_42_rows_and_master_constants() -> None:
    certificate = core.build_certificate()
    assert core.verify_certificate(certificate)
    assert certificate["counts"] == {
        "analytic_rows": 12,
        "channel_rows": 7,
        "endpoint_rows": 7,
        "resummation_rows": 14,
        "ledger_rows": 2,
        "oracle_rows_total": 42,
    }
    master = certificate["ledger_rows"][1]
    assert (master["gradient"], master["source_gap_coefficient"], master["power_gap_coefficient"]) == (126, 3528, 588)
    assert certificate["analytic_rows"][1]["bridge_pass"] is True
    assert all(row["pass"] is True for row in certificate["channel_rows"])
    assert certificate["ledger_rows"][0]["derivative_terms"] == [2, 4, 4]
    assert certificate["ledger_rows"][0]["cube_exp_upper"] == "exp(1/2)<2"


def test_field_verifier_does_not_call_fresh_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden() -> dict[str, object]:
        raise RuntimeError("fresh builder called")

    monkeypatch.setattr(core, "build_certificate", forbidden)
    assert core.verify_certificate(certificate, compare_fresh=False)


def test_twenty_four_genuine_mutations_fail_field_verification() -> None:
    results = core.mutation_results()
    assert results["count"] == results["rejected"] == 24
    assert results["all_pass"] is True
    assert len({row["name"] for row in results["rows"]}) == 24


@pytest.mark.parametrize("bad", [0, 1, "false", None])
def test_compare_fresh_requires_exact_bool(bad: object) -> None:
    with pytest.raises(TypeError):
        core.verify_certificate(core.build_certificate(), compare_fresh=bad)  # type: ignore[arg-type]


def test_bool_for_int_and_unexpected_members_fail() -> None:
    candidate = core.build_certificate()
    candidate["ledger_rows"][0]["l1_gradient_bound"] = True
    with pytest.raises(ValueError):
        core.verify_certificate(candidate, compare_fresh=False)
    candidate = core.build_certificate()
    candidate["unexpected"] = 1
    with pytest.raises(ValueError):
        core.verify_certificate(candidate, compare_fresh=False)


def test_strict_json_rejects_duplicate_nonfinite_and_nonobject() -> None:
    with pytest.raises(ValueError):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        core.loads_strict('{"a":NaN}')
    with pytest.raises(TypeError):
        core.loads_strict('[]')


def test_canonical_round_trip_and_digest_are_stable() -> None:
    certificate = core.build_certificate()
    blob = core.canonical_json_bytes(certificate)
    loaded = core.loads_strict(blob.decode("utf-8"))
    assert core.exact_equal(loaded, certificate)
    assert core.payload_sha256(loaded) == core.payload_sha256(certificate)


def test_every_scalar_leaf_is_fail_closed() -> None:
    original = core.build_certificate()
    paths: list[tuple[object, ...]] = []

    def visit(value: object, path: tuple[object, ...]) -> None:
        if type(value) is dict:
            for key, item in value.items():
                visit(item, path + (key,))
        elif type(value) is list:
            for index, item in enumerate(value):
                visit(item, path + (index,))
        else:
            paths.append(path)

    visit(original, ())
    for path in paths:
        candidate = deepcopy(original)
        parent: object = candidate
        for key in path[:-1]:
            parent = parent[key]  # type: ignore[index]
        key = path[-1]
        old = parent[key]  # type: ignore[index]
        if type(old) is bool:
            new = not old
        elif type(old) is int:
            new = old + 1
        elif type(old) is str:
            new = old + "!"
        elif old is None:
            new = "not-null"
        else:
            raise AssertionError(type(old))
        parent[key] = new  # type: ignore[index]
        with pytest.raises((TypeError, ValueError)):
            core.verify_certificate(candidate, compare_fresh=False)
