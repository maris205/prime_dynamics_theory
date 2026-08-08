from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
import subprocess
import sys

import pytest

from vk_prime_tail import (
    MUTATION_NAMES,
    R_FIXTURES,
    apply_mutation,
    auxiliary_attack_results,
    build_certificate,
    canonical_json_bytes,
    loads_strict,
    mutation_results,
    payload_sha256,
    verify_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
RH384_RESULT = REPOSITORY / "papers" / "RH-384-prime-tail-scale-separation" / "results" / "result.json"


def test_exact_96_row_certificate_and_digest() -> None:
    certificate = verify_certificate()
    assert certificate["counts"] == {
        "analytic_source_rows": 16,
        "r_fixtures": 8,
        "partition_rows": 66,
        "envelope_sharpness_rows": 6,
        "oracle_rows_total": 96,
    }
    assert len(canonical_json_bytes(certificate)) == 29_717
    assert payload_sha256(certificate) == "64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710"
    assert certificate["epistemic_role"] == "reproduction_not_analytic_proof"
    assert certificate["all_pass"] is True


def test_source_lock_file_is_exact_core_object() -> None:
    loaded = loads_strict((ROOT / "results" / "external_source_lock.json").read_text())
    assert canonical_json_bytes(loaded) == canonical_json_bytes(build_certificate()["remote_source_lock"])
    assert loaded["redistributable_in_release"] is False
    assert loaded["pdf_vendored"] is False
    assert loaded["network_verification"]["default"] == "disabled"


def test_r_fixture_contract() -> None:
    rows = build_certificate()["r_fixtures"]
    assert tuple(row["r"] for row in rows) == R_FIXTURES
    assert all(type(row["r"]) is int for row in rows)
    assert [row["two_r_minus_one"] for row in rows] == [2 * r - 1 for r in R_FIXTURES]


def test_rh384_partition_regression_is_reproduced_not_promoted() -> None:
    inherited = loads_strict(RH384_RESULT.read_text())["certificate"]["partitions"]
    current = build_certificate()["partitions"]
    assert len(inherited) == len(current) == 66
    inherited_projection = [
        (
            row["partition"],
            row["degree"],
            row["length"],
            row["constant"],
            row["p_exponent"],
        )
        for row in inherited
    ]
    current_projection = [
        (
            row["partition"],
            row["degree_d"],
            row["length"],
            row["leading_constant"],
            row["p_exponent"],
        )
        for row in current
    ]
    assert current_projection == inherited_projection
    assert all(row["rh384_regression_role"] == "reproduction_only" for row in current)


def test_canonical_kernel_and_partition_ledgers() -> None:
    contracts = build_certificate()["contracts"]
    assert contracts["kernel_ledger"]["canonical_exact_to_power"].endswith("r/(x^2-1)")
    assert contracts["kernel_ledger"]["optional_coarse"].endswith("when r/x^2<=3/8")
    assert contracts["partition_ledger"] == {
        "exact_kernel": "14*d*eta",
        "power_kernel_addition": "d/(x^2-1)",
        "leading_addition": "H/L",
        "refined_leading_sign": "-H/L",
        "refined_remainder": "2*H2/L^2",
    }


def test_twenty_four_genuine_mutations_fail_field_level_verification() -> None:
    rows = mutation_results()
    assert [row["name"] for row in rows] == list(MUTATION_NAMES)
    assert len(rows) == 24
    assert all(row["payload_changed"] is True for row in rows)
    assert all(row["rejected"] is True for row in rows)
    assert rows[-1]["name"] == "redistributable_true"


def test_auxiliary_source_type_and_strict_json_attacks_are_rejected() -> None:
    rows = auxiliary_attack_results()
    assert [row["name"] for row in rows] == [
        "source_url", "source_bytes", "source_DOI", "source_MIME", "source_pages_type",
        "nonfinite_JSON", "duplicate_JSON",
    ]
    assert all(row["rejected"] is True for row in rows)


@pytest.mark.parametrize("name", MUTATION_NAMES)
def test_each_object_mutation_changes_payload_and_is_rejected(name: str) -> None:
    fresh = build_certificate()
    mutated = apply_mutation(fresh, name)
    assert canonical_json_bytes(mutated) != canonical_json_bytes(fresh)
    with pytest.raises((TypeError, ValueError)):
        verify_certificate(mutated, compare_fresh=False)


@pytest.mark.parametrize("bad", [0, 1, "false", None])
def test_compare_fresh_requires_exact_bool(bad: object) -> None:
    with pytest.raises(TypeError):
        verify_certificate(compare_fresh=bad)  # type: ignore[arg-type]


def test_field_level_verifier_never_calls_fresh_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    import vk_prime_tail.core as core

    candidate = core.build_certificate()

    def forbidden() -> dict[str, object]:
        raise RuntimeError("fresh called")

    monkeypatch.setattr(core, "build_certificate", forbidden)
    assert core.verify_certificate(candidate, compare_fresh=False) is candidate
    for name in core.MUTATION_NAMES:
        mutated = core.apply_mutation(candidate, name)
        with pytest.raises((TypeError, ValueError)):
            core.verify_certificate(mutated, compare_fresh=False)


@pytest.mark.parametrize(
    ("row_index", "field", "bad_value"),
    [
        (2, "bound", "FALSE"),
        (5, "obstruction", "none"),
    ],
)
def test_envelope_text_attacks_are_rejected(row_index: int, field: str, bad_value: str) -> None:
    candidate = build_certificate()
    candidate["envelopes"][row_index][field] = bad_value
    with pytest.raises(ValueError):
        verify_certificate(candidate, compare_fresh=False)


def test_envelope_extra_key_is_rejected() -> None:
    candidate = build_certificate()
    candidate["envelopes"][0]["unexpected"] = "escape"
    with pytest.raises(ValueError):
        verify_certificate(candidate, compare_fresh=False)


def test_every_scalar_leaf_is_field_level_fail_closed() -> None:
    candidate = build_certificate()
    leaves: list[tuple[tuple[object, ...], object]] = []

    def walk(value: object, path: tuple[object, ...] = ()) -> None:
        if type(value) is dict:
            for key, item in value.items():
                walk(item, (*path, key))
        elif type(value) is list:
            for index, item in enumerate(value):
                walk(item, (*path, index))
        else:
            leaves.append((path, value))

    def replace(value: dict[str, object], path: tuple[object, ...], replacement: object) -> None:
        cursor: object = value
        for part in path[:-1]:
            cursor = cursor[part]  # type: ignore[index]
        cursor[path[-1]] = replacement  # type: ignore[index]

    walk(candidate)
    assert len(leaves) == 1522
    for path, value in leaves:
        if type(value) is bool:
            replacement = not value
        elif type(value) is int:
            replacement = value + 1
        elif type(value) is str:
            replacement = value + "#"
        elif value is None:
            replacement = "not-null"
        else:  # pragma: no cover - the certificate has only strict JSON primitives
            raise AssertionError(type(value))
        mutated = deepcopy(candidate)
        replace(mutated, path, replacement)
        with pytest.raises((TypeError, ValueError)):
            verify_certificate(mutated, compare_fresh=False)


def test_strict_json_rejects_duplicate_nonfinite_and_nonobject() -> None:
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "[]"):
        with pytest.raises(ValueError):
            loads_strict(text)


def test_optimized_python_certificate_is_identical() -> None:
    code = (
        "from vk_prime_tail import build_certificate,canonical_json_bytes,payload_sha256;"
        "c=build_certificate();print(len(canonical_json_bytes(c)),payload_sha256(c))"
    )
    completed = subprocess.run(
        [sys.executable, "-OO", "-B", "-c", code],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"},
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.stdout.strip() == "29717 64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710"
