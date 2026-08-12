"""Runtime and adversarial tests for the RH-397 Stage-1 result."""

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
    require(type(value) is dict)
    require(result.validate_result_payload(value, compare_fresh=False) is True)
    return value


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_stored_and_fresh_identities(stored: dict[str, object]) -> None:
    pretty = result.OUTPUT.read_bytes()
    canonical = result.canonical_bytes(stored)
    require(len(pretty) == 151768)
    require(sha256(pretty).hexdigest() == "d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f")
    require(len(canonical) == 105495)
    require(sha256(canonical).hexdigest() == "d2445cc883371ccfd96eeb09f908d62d232fcb5cde5ea9170aa2029956047c2a")
    require(stored["all_pass"] is True)
    require(result.exact_equal(result.build_payload(), stored) is True)
    require(result.validate_result_payload(stored, compare_fresh=True) is True)


def test_frozen_core_source_and_roles(stored: dict[str, object]) -> None:
    identities = stored["identities"]
    require(identities["core_file"] == {"bytes": 75206, "sha256": result.CORE_FILE_SHA256})
    require(identities["core_test"] == {"bytes": 6648, "sha256": result.CORE_TEST_SHA256})
    require(identities["certificate"]["canonical_sha256"] == result.CERTIFICATE_FIXTURE_SHA256)
    require(identities["certificate"]["rows"] == 72)
    require(identities["source_closure"] == {
        "canonical_bytes": 61297, "canonical_sha256": result.SOURCE_CLOSURE_SHA256,
        "git": 172, "remote": 4, "logical": 176,
        "group_sizes": result.SOURCE_GROUP_SIZES,
        "group_digests": result.SOURCE_GROUP_DIGESTS,
        "all_git_sha256": result.ALL_GIT_SOURCE_SHA256,
        "logical_sha256": result.LOGICAL_SOURCE_SHA256,
    })
    require(stored["source_closure"]["pass"] is True)
    require(stored["source_closure"]["direct_predecessor"]["commit"] == "cd57086fa90939d56656c3f952a08ffad9aabefe")
    require(stored["source_roles"]["RH394"]["analytic_input"] is True)
    require(stored["source_roles"]["RH396"].startswith("direct_collision"))
    require(stored["declarations"]["remote_redistributable_in_release"] == [False, False, True, False])
    require(stored["declarations"]["external_payload_hash_hits"] == [])


def test_exact_theorem_contract(stored: dict[str, object]) -> None:
    theorem = stored["theorem_contracts"]
    model = theorem["model_and_quantifiers"]
    require(model["phase_domain"] == "q>=1 is a finite integer and r lies in Z/qZ; r+h is read modulo q")
    require("for every r in Z/qZ and x,z,y,w in T" in model["safety"])
    require("every admissible terminal clock omega" in model["fixed_table_limit"])
    require("same value for all omega" in model["fixed_table_limit"])
    require("max_(F universally half-span safe)|L_hq(F)|" in model["capacity_definition"])
    require(theorem["collision_aware_densities"]["coordinate_shifts"] == ["L=+h", "C=0", "R=-h"])
    require(theorem["collision_aware_densities"]["K1"] == "K1=product_p(1-1/p^2)=6/pi^2")
    require(theorem["collision_aware_densities"]["unconditional_K2_K3_substitution"] is False)
    projection = theorem["projection_flags_rectangles_reflection"]
    require(projection["safe_pairs"] == 61440)
    require(projection["flag_order"] == ["00", "10", "01", "11"])
    require(projection["flag_class_counts"] == [16, 48, 48, 400])
    require(projection["rectangle_sizes"] == [4, 6, 6, 9])
    weights = theorem["phase_weights_and_edge_saturation"]
    require(weights["rectangle_value"].endswith("+(1-s)(1-t)W"))
    require(weights["translation"] == "V_r=U_(r+h)")
    require("t_(r+h)" in weights["addition_gain"])
    capacity = theorem["weighted_independent_set_capacity"]
    require(capacity["weighted_not_cardinality"] is True)
    require("max_(J subset Z/qZ, J intersect (J+h)=empty)" in capacity["formula"])
    odd = theorem["odd_lag_all_clock_attainment"]
    require(odd["scope"] == "each fixed odd integer h>=1")
    require(odd["clock_maximum"] == "max_(finite q>=1)C_h^hs(q)=C_h^hs(2)=K1-kappa2(h)/2+kappa3(h)/4")
    require("iff the declared finite phase clock q is even" in odd["attainment_classification"])
    require(odd["q2_attains"] is True)
    require(odd["controls"]["h9q2"] == ["0", "1", "-4/7", "1/3"])
    ceiling = theorem["analytic_source_roles_and_claim_ceiling"]
    require(ceiling["analytic_shift_count"] == 3)
    require(ceiling["c1111_invoked"] is False)


def test_core_and_result_mutations(stored: dict[str, object]) -> None:
    rows = stored["core_mutation_audit"]
    require(len(rows) == 60)
    require([row["name"] for row in rows] == list(result.MUTATION_NAMES))
    require([row["target_id"] for row in rows] == [target for _name, target in result.MUTATION_TARGETS])
    require(all(row["existing_leaf_changed"] is True and row["false_validator_rejected"] is True for row in rows))
    require(len(result.RESULT_MUTATION_NAMES) == 78)
    require(len(set(result.RESULT_MUTATION_NAMES)) == 78)
    digests = []
    for name in result.RESULT_MUTATION_NAMES:
        changed = result.mutate_result(stored, name)
        require(result.validate_result_payload(changed, compare_fresh=False) is False, name)
        digests.append(sha256(result.canonical_bytes(changed)).hexdigest())
    require(len(set(digests)) == 78)


def test_topology_types_and_strict_json(stored: dict[str, object]) -> None:
    attacks = []
    extra = deepcopy(stored); extra["extra"] = 0; attacks.append(extra)
    missing = deepcopy(stored); missing.pop("status"); attacks.append(missing)
    reordered = {key: stored[key] for key in reversed(tuple(stored))}; attacks.append(reordered)
    float_version = deepcopy(stored); float_version["schema_version"] = 1.0; attacks.append(float_version)
    bool_version = deepcopy(stored); bool_version["schema_version"] = True; attacks.append(bool_version)
    for attack in attacks:
        require(result.validate_result_payload(attack, compare_fresh=False) is False)
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        with pytest.raises(ValueError):
            result.loads_strict(text)


def test_false_mode_survives_bombs(stored: dict[str, object]) -> None:
    saved = {}
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("false mode called a public helper")
    try:
        for name in (*result.RESULT_BUILDER_NAMES, *result.RESULT_HELPER_NAMES):
            if hasattr(result, name):
                saved[name] = getattr(result, name); setattr(result, name, bomb)
        require(result.validate_result_payload(stored, compare_fresh=False) is True)
    finally:
        for name, value in saved.items():
            setattr(result, name, value)


def test_validator_factory_rejects_wrong_producer(stored: dict[str, object]) -> None:
    wrong = deepcopy(stored)
    wrong["summary"]["safe_relation_pairs"] = 61439

    def wrong_builder() -> dict[str, object]:
        return deepcopy(wrong)

    with pytest.raises(RuntimeError, match="independent canonical seal"):
        result._make_result_validator(wrong_builder)

    reordered = deepcopy(stored)
    model = reordered["theorem_contracts"]["model_and_quantifiers"]
    reordered["theorem_contracts"]["model_and_quantifiers"] = {
        key: model[key] for key in reversed(tuple(model))
    }

    def reordered_builder() -> dict[str, object]:
        return deepcopy(reordered)

    with pytest.raises(RuntimeError, match="independent ordered seal"):
        result._make_result_validator(reordered_builder)

    wrong_type = deepcopy(stored)
    wrong_type["theorem_contracts"]["odd_lag_all_clock_attainment"]["control_basis"] = (
        "K0", "K1", "K2", "K3",
    )

    def wrong_type_builder() -> dict[str, object]:
        return deepcopy(wrong_type)

    with pytest.raises(RuntimeError, match="non-exact JSON type"):
        result._make_result_validator(wrong_type_builder)


def test_ast_and_cache_hygiene() -> None:
    paths = [Path(result.__file__), Path(__file__)]
    trees = [ast.parse(path.read_text(encoding="utf-8")) for path in paths]
    count = sum(isinstance(node, ast.Assert) for tree in trees for node in ast.walk(tree))
    require(count == 0)
    for tree in trees:
        for node in ast.walk(tree):
            if not isinstance(node, ast.Dict):
                continue
            keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and type(key.value) is str]
            require(len(keys) == len(set(keys)), "duplicate literal dict key")
    root = Path(__file__).resolve().parents[1]
    forbidden = [path for path in root.rglob("*") if path.name in ("__pycache__", ".pytest_cache") or path.suffix == ".pyc"]
    require(forbidden == [], f"cache artifacts present: {forbidden}")
