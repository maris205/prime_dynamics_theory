from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import json

import pytest

import moving_rank_necessity.core as core


def test_positive_baseline_passes_false_and_fresh_modes() -> None:
    certificate = core.build_certificate()
    assert core.verify_certificate(certificate, compare_fresh=False)
    assert core.verify_certificate(certificate, compare_fresh=True)


def test_exact_semantic_row_count() -> None:
    certificate = core.build_certificate()
    assert certificate["counts"] == {
        "definition_rows": 10, "edge_rows": 12, "gamma_rows": 12,
        "vector_rows": 12, "profile_rows": 8, "contract_rows": 6,
        "semantic_rows_total": 60,
    }


def test_frozen_certificate_fixture() -> None:
    certificate = core.build_certificate()
    assert len(core.canonical_json_bytes(certificate)) == 10_062
    assert core.payload_sha256(certificate) == "cc2874435e62205a3e969e841d80d37243d95826855bd242f0eff3478dccf367"


def test_false_mode_invokes_no_builders(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden() -> list[dict[str, object]]:
        raise AssertionError("builder invoked")

    for name in core.GROUP_BUILDERS:
        monkeypatch.setitem(core.GROUP_BUILDERS, name, forbidden)
    assert core.verify_certificate(certificate, compare_fresh=False)
    with pytest.raises(AssertionError, match="builder invoked"):
        core.verify_certificate(certificate, compare_fresh=True)


@pytest.mark.parametrize("name", core.MUTATION_NAMES)
def test_each_genuine_mutation_is_rejected(name: str) -> None:
    certificate = core.build_certificate()
    mutated = core.apply_mutation(certificate, name)
    with pytest.raises((TypeError, ValueError, RuntimeError, KeyError, IndexError)):
        core.verify_certificate(mutated, compare_fresh=False)


def test_mutation_report_is_exactly_24_of_24() -> None:
    rows = core.mutation_results()
    assert [row["name"] for row in rows] == list(core.MUTATION_NAMES)
    assert len(rows) == 24
    assert all(row == {"name": row["name"], "rejected": True} for row in rows)


def _leaf_paths(value: object, prefix: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    if type(value) is dict:
        return [path for key, item in value.items() for path in _leaf_paths(item, prefix + (key,))]
    if type(value) is list:
        return [path for index, item in enumerate(value) for path in _leaf_paths(item, prefix + (index,))]
    return [prefix]


def _mutate_leaf(value: object, path: tuple[object, ...]) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    key = path[-1]
    original = cursor[key]
    if type(original) is bool:
        cursor[key] = not original
    elif type(original) is int:
        cursor[key] = original + 1
    elif type(original) is str:
        cursor[key] = original + "#"
    else:
        raise AssertionError(f"unexpected scalar type: {type(original).__name__}")


def test_every_certificate_scalar_leaf_is_closed() -> None:
    certificate = core.build_certificate()
    paths = _leaf_paths(certificate)
    assert len(paths) >= 300
    for path in paths:
        mutated = deepcopy(certificate)
        _mutate_leaf(mutated, path)
        with pytest.raises((TypeError, ValueError, RuntimeError, KeyError, IndexError)):
            core.verify_certificate(mutated, compare_fresh=False)


def test_exact_types_reject_bool_for_integer_leaf() -> None:
    certificate = core.build_certificate()
    certificate["counts"]["semantic_rows_total"] = True
    with pytest.raises(ValueError):
        core.verify_certificate(certificate, compare_fresh=False)


def test_membership_rejects_extra_and_missing_groups() -> None:
    extra = core.build_certificate()
    extra["surprise"] = False
    with pytest.raises(ValueError):
        core.verify_certificate(extra, compare_fresh=False)
    missing = core.build_certificate()
    del missing["edge_rows"]
    with pytest.raises(ValueError):
        core.verify_certificate(missing, compare_fresh=False)


def test_strict_json_rejects_duplicate_keys_nan_and_non_object() -> None:
    with pytest.raises(ValueError, match="duplicate JSON key"):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError, match="non-finite"):
        core.loads_strict('{"a":NaN}')
    with pytest.raises(TypeError, match="top-level"):
        core.loads_strict("[]")


def test_fraction_text_round_trip_and_canonical_rejections() -> None:
    for value in (Fraction(0), Fraction(3, 7), Fraction(-9, 5), Fraction(12)):
        assert core.fraction_from_text(core.fraction_text(value), "fixture") == value
    for bad in ("2/4", "+1", "1/0", "1/-2", "1/2/3", ""):
        with pytest.raises((TypeError, ValueError)):
            core.fraction_from_text(bad, "bad")


def test_canonical_json_forbids_nonfinite() -> None:
    with pytest.raises(ValueError):
        core.canonical_json_bytes({"x": float("inf")})


def test_apply_mutation_rejects_unknown_and_bad_container() -> None:
    with pytest.raises(ValueError):
        core.apply_mutation(core.build_certificate(), "unknown")
    with pytest.raises(ValueError):
        core.apply_mutation([], core.MUTATION_NAMES[0])


def test_gamma_constant_is_exact_positive_fraction() -> None:
    row = core.build_certificate()["gamma_rows"][8]
    value = core.fraction_from_text(row["exact"], "kappa")
    assert value > 0
    assert row["decimal_prefix"] == "0.0347017856545"
