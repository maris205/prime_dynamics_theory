from __future__ import annotations

import ast
from copy import deepcopy
import hashlib
from pathlib import Path

import pytest

import build_result as result


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError, match="optimized sentinel"):
        require(False, "optimized sentinel")


def test_build_validate_and_frozen_fixtures() -> None:
    payload = result.build_payload()
    require(payload["all_pass"] is True)
    require(result.validate_result_payload(payload, compare_fresh=False) is True)
    require(result.validate_result_payload(payload, compare_fresh=True) is True)
    require(payload["certificate_fixture"] == {
        "canonical_bytes": 108_636,
        "sha256": "3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998",
        "pass": True,
    })
    require(payload["core_fixture"] == {
        "sha256": "3b24da1f1c54e69f98b2e1d07209d24928dbb3493a3fcc386c0bcf751dde4c85",
        "pass": True,
    })
    require(payload["source_fixture"] == {
        "canonical_bytes": 47_785,
        "sha256": "8028373a8e8d7f10061c70872a72dc9c55654f9730de9fe2de19b7a4b3696501",
        "builder_sha256": "2171aa240afbc8add45fec589545fc2e1490a971da3fc72cf772559e17de51e9",
        "pass": True,
    })


def test_result_file_is_exact_pretty_serialization() -> None:
    stored = result.loads_strict(result.OUTPUT.read_text(encoding="utf-8"))
    require(result.validate_result_payload(stored, compare_fresh=False) is True)
    require(result.OUTPUT.read_bytes() == result.pretty_json_bytes(stored))
    require(stored == result.build_payload())


def test_theorem_contract_is_self_contained_and_exact() -> None:
    payload = result.build_payload()
    theorems = payload["theorems"]
    require(theorems["odd_parity_compiler"]["admitted_support_sizes"] == (
        "|O(alpha)| is 0, 2, or a positive odd integer"
    ))
    require(theorems["phase_density"]["Theta"].startswith("Theta_(q,r)(E)=q^-1"))
    require(theorems["exact_support_table_law"]["probability"] == (
        "Pi_(q,r)(U)>=0 and sum_U Pi_(q,r)(U)=1/q"
    ))
    require("endpoint error O(1)" in theorems["proof_decomposition"]["phase_bridge"])
    require("harmonic denominator" in theorems["proof_decomposition"]["phase_bridge"])
    require(theorems["complete_three_shift_law"]["full_sign_table_phase_families"] == "2^(27q)")
    require(theorems["four_shift_boundary"]["q_phase_families"] == (
        "[binom(16,8)*2^65]^q"
    ))
    require(result.payload_sha256(theorems) == result.THEOREM_CONTRACT_SHA256)
    require(result.payload_sha256(payload["source_roles"]) == result.SOURCE_ROLE_SHA256)


def test_finite_contracts_consume_certificate() -> None:
    finite = result.build_payload()["finite_contracts"]
    require(finite["dimensions"]["m3"]["admitted"] == 27)
    require(finite["dimensions"]["m3"]["total"] == 27)
    require(finite["dimensions"]["m4"]["admitted"] == 80)
    require(finite["dimensions"]["m4"]["total"] == 81)
    require(finite["signed_four_cube"] == {
        "eligible_corner_patterns": 12_870,
        "ternary_truth_tables": 12_870 * 2**65,
        "free_noncorner_bits": 65,
    })
    require(finite["current_tables"]["M_0_through_4"] == [2, 4, 16, 70, 648])
    require(finite["current_tables"]["two_input"] == 512)
    require(finite["current_tables"]["three_input"] == 36_700_160)


def test_source_closure_rights_and_roles_are_consumed() -> None:
    payload = result.build_payload()
    source = payload["source_locks"]
    require((source["git_count"], source["remote_count"], source["logical_count"]) == (128, 4, 132))
    require(source["logical_source_digest"] == (
        "07c9ed6c0c79d77098e19d8102b4267ea4af637ae2d72148c412cc626af738ac"
    ))
    require(source["remote"]["redistributable_in_release"] == [False, False, True, False])
    require(source["remote"]["network_fetch_performed"] is False)
    require(source["remote"]["external_payload_hash_hits"] == [])
    require("TT is the fourth" in payload["source_roles"]["RH393"])


def test_every_result_mutation_fails_false_mode() -> None:
    payload = result.build_payload()
    require(len(result.RESULT_MUTATION_NAMES) == 32)
    require(len(set(result.RESULT_MUTATION_NAMES)) == 32)
    escaped = [
        name for name in result.RESULT_MUTATION_NAMES
        if result.validate_result_payload(
            result.mutate_result_payload(payload, name), compare_fresh=False
        )
    ]
    require(escaped == [], f"result mutations escaped: {escaped}")


def test_false_mode_uses_no_builder_or_public_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = result.build_payload()

    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden false-mode dependency")

    for name in result.RESULT_BUILDER_NAMES + result.RESULT_HELPER_NAMES:
        monkeypatch.setattr(result, name, bomb)
    require(result.validate_result_payload(payload, compare_fresh=False) is True)


def test_coordinated_constant_rebinding_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = result.build_payload()
    monkeypatch.setattr(result, "CERTIFICATE_FIXTURE_BYTES", 108_635)
    monkeypatch.setattr(result, "CERTIFICATE_FIXTURE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "CORE_FILE_SHA256", "1" * 64)
    monkeypatch.setattr(result, "THEOREM_CONTRACT_SHA256", result.payload_sha256({}))
    require(result.validate_result_payload(payload, compare_fresh=False) is False)
    with pytest.raises(ValueError, match="independent result hash contract"):
        result.build_payload()


def test_type_topology_and_firewall_attacks() -> None:
    baseline = result.build_payload()
    attacks = []
    changed = deepcopy(baseline)
    changed["mutations"]["count"] = 32.0
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["declarations"]["git_source_rows"] = True
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["gates"]["unexpected"] = False
    attacks.append(changed)
    changed = deepcopy(baseline)
    del changed["theorems"]
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["extra"] = None
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["dimensions"]["m3"]["m"] = 99
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["dimensions"]["m3"]["all_even"] = 999
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["dimensions"]["extra"] = {}
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["dimensions"]["m3"]["extra"] = 0
    attacks.append(changed)
    changed = deepcopy(baseline)
    del changed["finite_contracts"]["dimensions"]["m4"]["positive_odd"]
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["dimensions"]["m4"]["two_odd"] = True
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["signed_four_cube"]["eligible_corner_patterns"] = 12_870.0
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["current_tables"]["two_input"] = 512.0
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["current_tables"]["M_0_through_4"][0] = 2.0
    attacks.append(changed)
    changed = deepcopy(baseline)
    changed["finite_contracts"]["phase_fixture"]["rows"] = 8.0
    attacks.append(changed)
    require(all(result.validate_result_payload(item, compare_fresh=False) is False for item in attacks))
    require(result.validate_result_payload([], compare_fresh=False) is False)
    require(result.validate_result_payload(baseline, compare_fresh="false") is False)


def test_strict_json_and_no_bare_asserts() -> None:
    with pytest.raises(ValueError, match="duplicate JSON key"):
        result.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError, match="non-finite"):
        result.loads_strict('{"a":NaN}')
    with pytest.raises(TypeError):
        result.loads_strict(b"{}")
    require(result.exact_equal(1, True) is False)
    require(result.exact_equal(1, 1.0) is False)
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
    require(len(hashlib.sha256(result.OUTPUT.read_bytes()).hexdigest()) == 64)
