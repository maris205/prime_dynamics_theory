from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

import build_result
import two_odd_compiler.core as core


def require(condition: bool, message: str = "test requirement failed") -> None:
    if condition is not True:
        raise AssertionError(message)


def test_stored_result_is_strict_fresh_and_byte_identical() -> None:
    raw = build_result.OUTPUT.read_bytes()
    stored = core.loads_strict(raw.decode("utf-8"))
    fresh = build_result.build_payload()
    require(core.exact_equal(stored, fresh))
    require(raw == build_result.pretty_json_bytes(fresh))
    require(build_result.validate_result_payload(stored, compare_fresh=False))
    require(build_result.validate_result_payload(stored, compare_fresh=True))


def test_result_consumes_all_frozen_gates() -> None:
    payload = build_result.build_payload()
    require(payload["all_pass"] is True)
    require(payload["paper"] == "RH-393")
    require(payload["certificate_fixture"] == {
        "canonical_bytes": 117096,
        "sha256": "f109da241722796418f39708b16fa162cce0b85a6e448998d3ede593b7bd697b",
        "pass": True,
    })
    require(payload["core_fixture"] == {
        "sha256": "f92c4f21cd487bff84f40cdc20ca3605d986acfe132fd7e493b126936024a342",
        "pass": True,
    })
    require(payload["finite_contracts"]["truth_census"] == {
        "eligible": 192, "outside": 320,
    })
    require(payload["finite_contracts"]["m3_dimension"]["allowed_dimension"] == 26)
    require(payload["source_locks"]["pass"] is True)
    require((
        payload["source_locks"]["git_count"],
        payload["source_locks"]["remote_count"],
        payload["source_locks"]["logical_count"],
    ) == (117, 3, 120))


def test_theorem_contract_is_self_contained() -> None:
    theorem = build_result.build_payload()["theorems"]
    require(theorem["terminal_clock"]["mobius_extension"].startswith("mu_0(t)=mu(t)"))
    compiler = theorem["two_odd_factor_compiler"]
    density = theorem["phase_density"]
    landscape = theorem["squarefree_landscape"]
    corollary = theorem["distinguished_current_corollary"]
    require("every fixed integer m>=1" in compiler["quantifiers"])
    require("every admissible terminal clock" in compiler["quantifiers"])
    require("Theta_(q,r)(E(alpha))" in compiler["limit"])
    require("c111(f)=2^-3" in compiler["m3_table_criterion"])
    require("covered iff c111(f)=0" in compiler["m3_table_criterion"])
    require("distinct set" in density["B_p"])
    require("counting distinct mod-p^2 classes" in density["tau_p_r"])
    require("sum_(r mod q)" in density["phase_sum"])
    require("not attained" in landscape["upper"])
    require("Q_y=product_(p<=y)p^2" in landscape["approach"])
    require("exactly 192 of 512" in corollary["census"])
    require(corollary["outside"] == "the remaining 320 tables are outside the theorem only")


def test_all_core_mutations_are_consumed() -> None:
    mutation = build_result.build_payload()["mutations"]
    require(mutation["count"] == len(core.MUTATION_NAMES) == 32)
    require(mutation["names"] == list(core.MUTATION_NAMES))
    require(all(row["rejected"] is True for row in mutation["results"]))


def test_false_validator_invokes_no_result_or_source_builder(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = build_result.build_payload()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("false validator invoked a forbidden builder")

    monkeypatch.setattr(build_result, "build_payload", forbidden)
    monkeypatch.setattr(build_result, "build_certificate", forbidden)
    monkeypatch.setattr(build_result, "build_source_closure", forbidden)
    monkeypatch.setattr(build_result, "exact_equal", forbidden)
    monkeypatch.setattr(build_result, "payload_sha256", forbidden)
    monkeypatch.setattr(build_result, "canonical_json_bytes", forbidden)
    require(build_result.validate_result_payload(payload, compare_fresh=False))


def test_forbidden_and_gate_membership_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    original = build_result.FORBIDDEN
    deleted = dict(original)
    deleted.pop("odd_support_at_least_3")
    monkeypatch.setattr(build_result, "FORBIDDEN", deleted)
    with pytest.raises(ValueError, match="membership"):
        build_result.build_payload()
    monkeypatch.undo()
    extra = dict(original)
    extra["invented"] = False
    monkeypatch.setattr(build_result, "FORBIDDEN", extra)
    with pytest.raises(ValueError, match="membership"):
        build_result.build_payload()
    monkeypatch.undo()
    gates = dict(build_result.GATES)
    gates.pop("A_intrinsic_determinant")
    monkeypatch.setattr(build_result, "GATES", gates)
    with pytest.raises(ValueError, match="membership"):
        build_result.build_payload()


def test_theorem_and_source_role_rebinding_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    theorem = deepcopy(build_result.THEOREM_CONTRACTS)
    theorem["two_odd_factor_compiler"]["vanishing_channels"] = "all channels"
    monkeypatch.setattr(build_result, "THEOREM_CONTRACTS", theorem)
    with pytest.raises(ValueError, match="theorem"):
        build_result.build_payload()
    monkeypatch.undo()
    roles = deepcopy(build_result.SOURCE_ROLES)
    roles["Mirsky"] = "black box"
    monkeypatch.setattr(build_result, "SOURCE_ROLES", roles)
    with pytest.raises(ValueError, match="source-role"):
        build_result.build_payload()


def test_coordinated_contract_and_seal_rebinding_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theorem = deepcopy(build_result.THEOREM_CONTRACTS)
    theorem["two_odd_factor_compiler"]["vanishing_channels"] = "all channels"
    monkeypatch.setattr(build_result, "THEOREM_CONTRACTS", theorem)
    monkeypatch.setattr(
        build_result, "THEOREM_CONTRACT_SHA256", build_result.payload_sha256(theorem)
    )
    with pytest.raises(ValueError, match="independent title/hash seal"):
        build_result.build_payload()
    monkeypatch.undo()

    roles = deepcopy(build_result.SOURCE_ROLES)
    roles["Mirsky"] = "unlocked black box"
    monkeypatch.setattr(build_result, "SOURCE_ROLES", roles)
    monkeypatch.setattr(
        build_result, "SOURCE_ROLE_SHA256", build_result.payload_sha256(roles)
    )
    with pytest.raises(ValueError, match="independent title/hash seal"):
        build_result.build_payload()
    monkeypatch.undo()

    monkeypatch.setattr(build_result, "SOURCE_CLOSURE_SHA256", "0" * 64)
    monkeypatch.setattr(build_result, "EXPECTED_ALL_GIT_SOURCE_DIGEST", "1" * 64)
    monkeypatch.setattr(build_result, "EXPECTED_LOGICAL_SOURCE_DIGEST", "2" * 64)
    with pytest.raises(ValueError, match="independent title/hash seal"):
        build_result.build_payload()


def test_title_fixture_and_remote_seals_are_literal(monkeypatch: pytest.MonkeyPatch) -> None:
    attacks = (
        ("TITLE", "changed title"),
        ("CERTIFICATE_FIXTURE_SHA256", "0" * 64),
        ("CORE_FILE_SHA256", "1" * 64),
        ("SOURCE_RELEASE", "0" * 40),
        ("JY_CANONICAL_SHA256", "2" * 64),
        ("MAYNARD_CANONICAL_SHA256", "3" * 64),
        ("TAO_CANONICAL_SHA256", "4" * 64),
    )
    for name, value in attacks:
        monkeypatch.setattr(build_result, name, value)
        with pytest.raises(ValueError):
            build_result.build_payload()
        monkeypatch.undo()


def test_mutation_names_and_exact_comparator_rebinding_fail_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(build_result, "MUTATION_NAMES", ("title",) * 32)
    with pytest.raises(ValueError, match="mutation-name"):
        build_result.build_payload()
    monkeypatch.undo()

    payload = build_result.build_payload()
    payload["theorems"]["two_odd_factor_compiler"]["limit"] = "0"
    monkeypatch.setattr(build_result, "exact_equal", lambda *_args: True)
    require(not build_result.validate_result_payload(payload, compare_fresh=False))


def test_hash_helper_rebinding_cannot_bypass_contract_or_source_seals(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theorem = deepcopy(build_result.THEOREM_CONTRACTS)
    theorem["two_odd_factor_compiler"]["limit"] = "0"
    monkeypatch.setattr(build_result, "THEOREM_CONTRACTS", theorem)
    monkeypatch.setattr(
        build_result, "payload_sha256",
        lambda *_args: build_result.THEOREM_CONTRACT_SHA256,
    )
    with pytest.raises(ValueError, match="theorem contract seal"):
        build_result.build_payload()
    monkeypatch.undo()

    payload = build_result.build_payload()
    payload["source_locks"]["remote"]["network_fetch_performed"] = True
    monkeypatch.setattr(
        build_result, "payload_sha256",
        lambda *_args: build_result.SOURCE_CLOSURE_SHA256,
    )
    require(not build_result.validate_result_payload(payload, compare_fresh=False))


def test_nested_result_attacks_are_rejected() -> None:
    payload = build_result.build_payload()
    variants: list[dict[str, object]] = []
    extra = deepcopy(payload)
    extra["extra"] = False
    variants.append(extra)
    missing = deepcopy(payload)
    del missing["theorems"]["phase_density"]
    variants.append(missing)
    wrong_limit = deepcopy(payload)
    wrong_limit["theorems"]["two_odd_factor_compiler"]["limit"] = "0"
    variants.append(wrong_limit)
    bool_count = deepcopy(payload)
    bool_count["mutations"]["count"] = True
    variants.append(bool_count)
    source_rebind = deepcopy(payload)
    source_rebind["source_locks"]["logical_count"] = 119
    variants.append(source_rebind)
    payload_hit = deepcopy(payload)
    payload_hit["source_locks"]["remote"]["external_payload_hash_hits"] = ["x"]
    variants.append(payload_hit)
    require(all(not build_result.validate_result_payload(item, compare_fresh=False) for item in variants))


def test_compare_fresh_requires_exact_boolean() -> None:
    with pytest.raises(TypeError, match="exact bool"):
        build_result.validate_result_payload({}, compare_fresh=1)


def test_no_unsealed_predecessor_or_payload_language() -> None:
    text = Path(build_result.__file__).read_text(encoding="utf-8")
    sentinel = "TO_" + "BE_" + "SEALED"
    require(sentinel not in text)
    require("RH390" in text and "RH391" in text)
    require("vendored_external_payload" in text)
