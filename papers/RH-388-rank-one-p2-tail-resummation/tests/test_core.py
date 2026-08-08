from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import rank_one_p2.core as core  # noqa: E402


def test_certificate_has_exact_56_rows_and_frozen_constants() -> None:
    certificate = core.build_certificate()
    assert core.verify_certificate(certificate)
    assert certificate["counts"] == {
        "analytic_rows": 12,
        "coordinate_rows": 7,
        "factorial_rows": 12,
        "endpoint_rows": 7,
        "necessity_rows": 10,
        "ledger_rows": 8,
        "oracle_rows_total": 56,
    }
    assert certificate["all_pass"] is True
    master = certificate["ledger_rows"][4]
    assert master["coordinate_coefficients"] == [60, 13, "28/3"]
    assert master["gap_coefficients"] == [7560, 1638, 1176]
    assert certificate["necessity_rows"][6]["sharp_lower_constant"] == "1/2"
    assert certificate["necessity_rows"][8]["entry_l1_Hessian_bound"] == 224
    assert certificate["necessity_rows"][8]["Taylor_remainder_coefficient"] == 112
    assert certificate["necessity_rows"][9]["endpoint_lower_constant"] == "X_infinity"


def test_coordinate_oracles_recompute_all_seven_channels() -> None:
    rows = core.build_certificate()["coordinate_rows"]
    assert [row["c"] for row in rows] == list(range(1, 8))
    assert all(row["source_under_60"] is True for row in rows)
    assert all(row["power_under_13"] is True for row in rows)
    assert all(row["factorial_under_4c_over_3"] is True for row in rows)
    assert all(row["positive_cube"] is True for row in rows)
    assert core.fraction_from_text(rows[-1]["factorial_total_coefficient"], "factorial") > 8
    assert core.fraction_from_text(rows[-1]["factorial_total_coefficient"], "factorial") < core.Fraction(28, 3)


def test_K_fixture_rows_lock_factorial_monotonicity() -> None:
    rows = core.build_certificate()["factorial_rows"]
    assert [row["K"] for row in rows] == list(range(1, 13))
    assert all(row["within_window"] is True for row in rows)
    assert all(row["step_not_above_one"] is True for row in rows)
    assert all(row["under_first_term"] is True for row in rows)


def test_field_verifier_does_not_call_fresh_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("row/fresh builder called")

    monkeypatch.setattr(core, "build_certificate", forbidden)
    for name in (
        "_analytic_rows",
        "_coordinate_rows",
        "_factorial_rows",
        "_endpoint_rows",
        "_necessity_rows",
        "_ledger_rows",
    ):
        monkeypatch.setattr(core, name, forbidden)
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
    candidate["ledger_rows"][0]["gradient_bound"] = True
    with pytest.raises(ValueError):
        core.verify_certificate(candidate, compare_fresh=False)
    candidate = core.build_certificate()
    candidate["contracts"]["source_contract"]["git_rows"] = True
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


def test_optimized_mode_matches_direct_build() -> None:
    code = (
        "import json,sys;"
        f"sys.path.insert(0,{str(ROOT / 'src')!r});"
        "import rank_one_p2.core as c;"
        "x=c.build_certificate();"
        "print(json.dumps({'sha':c.payload_sha256(x),'ok':c.verify_certificate(x),'m':c.mutation_results()},sort_keys=True,separators=(',',':')))"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-c", code],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0, completed.stderr
    result = json.loads(completed.stdout)
    certificate = core.build_certificate()
    assert result["sha"] == core.payload_sha256(certificate)
    assert result["ok"] is True
    assert result["m"]["all_pass"] is True


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
