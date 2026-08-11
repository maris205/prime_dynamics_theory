from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

import pytest

import build_result as result


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


@pytest.fixture(scope="module")
def stored() -> dict[str, object]:
    value = result.loads_strict(result.OUTPUT.read_text(encoding="utf-8"))
    require(result.validate_result_payload(value, compare_fresh=False) is True)
    return value


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_stored_pretty_and_canonical_identities(stored: dict[str, object]) -> None:
    pretty = result.OUTPUT.read_bytes()
    canonical = result.canonical_bytes(stored)
    require(len(pretty) == 148331)
    require(sha256(pretty).hexdigest() == "7557bcc78811b29d7ac9f155fd8553c75d70b659748a37cf2fef427af4958f27")
    require(len(canonical) == 101772)
    require(sha256(canonical).hexdigest() == "9377280e97c1c92f92f492abb10edb72ae2b4b08b90b2ded1c30cf57e2904c9b")
    require(stored["all_pass"] is True)


def test_fresh_payload_matches_stored(stored: dict[str, object]) -> None:
    fresh = result.build_payload()
    require(result.exact_equal(fresh, stored) is True)
    require(result.validate_result_payload(stored, compare_fresh=True) is True)


def test_source_and_core_seals(stored: dict[str, object]) -> None:
    identities = stored["identities"]
    require(identities["core_file"] == {
        "bytes": 127045,
        "sha256": "4abb5e4c61a9b71370d2e02c36a474655719740b91fdd247f64ed0af0b90509e",
    })
    require(identities["certificate"]["canonical_sha256"] == "31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9")
    require(identities["source_closure"]["git"] == 148)
    require(identities["source_closure"]["remote"] == 4)
    require(identities["source_closure"]["logical"] == 152)
    source = stored["source_closure"]
    require(source["remote"]["network_fetch_performed"] is False)
    require(source["remote"]["external_payload_hash_hits"] == [])
    require(source["remote"]["redistributable_in_release"] == [False, False, True, False])


def test_theorem_is_self_contained_and_q2_is_full8(stored: dict[str, object]) -> None:
    theorem = stored["theorem_contracts"]
    model = theorem["model_and_quantifiers"]
    require(model["phase_table_type"] == "F_r:T^3->{-1,+1}, r in Z/qZ")
    require("for every r and a,b,c,d,e in T" in model["safety"])
    require("finite maximum" in model["capacity"])
    density = theorem["phase_densities"]
    require("p||q" in density["Theta"] and "p^2|q" in density["Theta"])
    require(density["Pi_mass"] == "sum_(U subset {L,C,R})Pi_(q,r)(U)=1/q")
    tropical = theorem["tropical_capacity"]
    require(tropical["all_q_state_count"] == 8)
    require(tropical["q_ge_3"].endswith("only for q>=3"))
    require(tropical["compressed_coefficients"].startswith("(a_r,b_r,c_r,d_r)="))
    require(theorem["positive_projection_and_relation"]["projected_terminal_limit"].startswith("L_q(F_proj)="))
    require(theorem["small_clocks"]["C2"] == "(3K2-K3)/4")
    require(theorem["small_clocks"]["q2_forbidden_old_four_state_value"] == "K2-K3")
    require("K2/K1>1/2" in theorem["small_clocks"]["ratio_inequalities"])


def test_reflection_endpoint_and_source_firewall(stored: dict[str, object]) -> None:
    theorem = stored["theorem_contracts"]
    require(theorem["reflection_and_absolute_value"]["terminal_sign"] == "L_q(F^rho)=-L_q(F)")
    require(theorem["reflection_and_absolute_value"]["capacity_identity"] == "max_safe |L_q|=max_safe L_q")
    require(theorem["all_clock_rigidity"]["strict_nonattainment"] == "C(q)<B_infinity for every finite q")
    require(theorem["all_clock_rigidity"]["conclusion"].endswith("not attained at finite q"))
    require(theorem["divisibility_and_square_support"]["square_clock"].startswith("p_y is the y-th odd prime"))
    require(theorem["divisibility_and_square_support"]["phase_contribution"] == "W_r:=K_r(Y_(r-2),Y_r)")
    roles = theorem["analytic_and_finite_roles"]
    require(roles["RH375_terminal_clock_analytic_input"] is False)
    require("sole terminal-log analytic input" in roles["RH394"])


def test_all_core_mutations_are_real_and_rejected(stored: dict[str, object]) -> None:
    rows = stored["core_mutation_audit"]
    require(len(rows) == 57)
    require(len({row["name"] for row in rows}) == 57)
    require(all(row["existing_leaf_changed"] is True for row in rows))
    require(all(row["false_validator_rejected"] is True for row in rows))


def test_every_result_mutation_is_rejected(stored: dict[str, object]) -> None:
    require(len(result.RESULT_MUTATION_NAMES) == 45)
    require(len(set(result.RESULT_MUTATION_NAMES)) == 45)
    for name in result.RESULT_MUTATION_NAMES:
        changed = result.mutate_result(stored, name)
        require(result.validate_result_payload(changed, compare_fresh=False) is False, name)


def test_false_mode_uses_no_global_builder_or_helper(
    stored: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global called")

    for name in result.RESULT_BUILDER_NAMES + result.RESULT_HELPER_NAMES:
        monkeypatch.setattr(result, name, bomb)
    monkeypatch.setattr(result, "sha256", bomb)
    monkeypatch.setattr(result, "json", bomb)
    require(result.validate_result_payload(stored, compare_fresh=False) is True)


def test_coordinated_constant_and_seal_rebinding_fails_closed(
    stored: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(result, "PAPER", "wrong")
    monkeypatch.setattr(result, "TITLE", "wrong")
    monkeypatch.setattr(result, "CORE_FILE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "SOURCE_CLOSURE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "THEOREM_CONTRACT_SHA256", "0" * 64)
    monkeypatch.setattr(result, "SOURCE_ROLE_SHA256", "0" * 64)
    monkeypatch.setattr(result, "RESULT_MUTATION_NAMES", ("fake",))
    monkeypatch.setattr(result, "FORBIDDEN", {"fake": False})
    require(result.validate_result_payload(stored, compare_fresh=False) is True)
    changed = deepcopy(stored)
    changed["identities"]["core_file"]["sha256"] = "0" * 64
    changed["identities"]["certificate"]["canonical_sha256"] = "0" * 64
    changed["identities"]["source_closure"]["canonical_sha256"] = "0" * 64
    require(result.validate_result_payload(changed, compare_fresh=False) is False)
    coordinated = deepcopy(stored)
    coordinated["forbidden"] = {"fake": False}
    coordinated["result_mutation_names"] = ["fake"]
    require(result.validate_result_payload(coordinated, compare_fresh=False) is False)


def test_exact_types_membership_and_order_attacks(stored: dict[str, object]) -> None:
    attacks: list[dict[str, object]] = []
    changed = deepcopy(stored)
    changed["schema_version"] = 1.0
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["summary"]["certificate_rows"] = True
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["core_mutation_audit"] = list(reversed(changed["core_mutation_audit"]))
    attacks.append(changed)
    changed = deepcopy(stored)
    changed["extra"] = 0
    attacks.append(changed)
    changed = deepcopy(stored)
    del changed["theorem_contracts"]["phase_densities"]["Pi"]
    attacks.append(changed)
    for attack in attacks:
        require(result.validate_result_payload(attack, compare_fresh=False) is False)


def test_strict_json_and_no_bare_asserts() -> None:
    require(result.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        result.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        result.loads_strict('{"a":Infinity}')
    package_root = Path(__file__).resolve().parents[1]
    for path in (Path(__file__), package_root / "experiments" / "build_result.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
