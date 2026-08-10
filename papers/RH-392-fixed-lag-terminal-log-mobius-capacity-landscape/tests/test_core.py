from copy import deepcopy
import math

import pytest

import fixed_lag_capacity.core as core


EXPECTED_BYTES = 220832
EXPECTED_SHA256 = "614297795d4d4dfeadfb5667d3e0d405d04fbe8e07e9d87a743faed9cb267a96"


def test_baseline_false_and_fresh_verification() -> None:
    certificate = core.build_certificate()
    assert certificate["all_pass"] is True
    assert certificate["counts"]["total_rows"] == 640
    assert core.verify_certificate(certificate, compare_fresh=False)
    assert core.verify_certificate(certificate, compare_fresh=True)
    payload = core.canonical_json_bytes(certificate)
    assert len(payload) == EXPECTED_BYTES
    assert core.payload_sha256(certificate) == EXPECTED_SHA256


def test_false_mode_calls_no_group_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("a certificate builder was called in false mode")

    for name in core.BUILDER_NAMES:
        monkeypatch.setattr(core, name, forbidden)
    assert core.verify_certificate(certificate, compare_fresh=False)
    with pytest.raises(AssertionError, match="builder was called"):
        core.verify_certificate(certificate, compare_fresh=True)


def test_corrupt_shared_constructors_cannot_self_certify(monkeypatch: pytest.MonkeyPatch) -> None:
    original_truth = core._truth_semantics

    def corrupt_truth(table_id: int) -> dict[str, object]:
        row = original_truth(table_id)
        row["projected_table_id"] = 1
        row["pass"] = True
        return row

    monkeypatch.setattr(core, "_truth_semantics", corrupt_truth)
    corrupted_truth_certificate = core.build_certificate()
    assert corrupted_truth_certificate["all_pass"] is True
    monkeypatch.setattr(core, "_truth_semantics", original_truth)
    assert not core.verify_certificate(corrupted_truth_certificate, compare_fresh=False)

    original_determinant = core._determinant_contracts

    def corrupt_determinant() -> list[dict[str, object]]:
        rows = original_determinant()
        rows[0]["determinant_hypothesis"] = "Delta may equal zero"
        rows[0]["pass"] = True
        return rows

    monkeypatch.setattr(core, "_determinant_contracts", corrupt_determinant)
    corrupted_determinant_certificate = core.build_certificate()
    assert corrupted_determinant_certificate["all_pass"] is True
    monkeypatch.setattr(core, "_determinant_contracts", original_determinant)
    assert not core.verify_certificate(corrupted_determinant_certificate, compare_fresh=False)


def test_all_24_mutations_are_genuine_semantic_rejections() -> None:
    certificate = core.build_certificate()
    rejected = {
        name for name in core.MUTATION_NAMES
        if not core.verify_certificate(core.mutate_certificate(certificate, name), compare_fresh=False)
    }
    assert len(core.MUTATION_NAMES) == 24
    assert rejected == set(core.MUTATION_NAMES)
    assert core.verify_certificate(certificate, compare_fresh=False)


def test_projection_and_compatibility_exhaustive() -> None:
    for table_id in range(512):
        projected = core.projected_table_id(table_id)
        assert set(core.plus_point_indices(projected)) <= set(core.plus_point_indices(table_id))
        assert all(
            z == 1
            for index, (_, z) in enumerate(core.POINTS)
            if projected & (1 << index)
        )
        assert all(gain >= 0 for gain in core.pointwise_zf_gains(table_id))
        assert core.reflected_table_id(core.reflected_table_id(table_id)) == table_id
    assert [sum(core.action_id_from_table(table_id) == action for table_id in range(512)) for action in range(8)] == [64] * 8
    for left in range(8):
        for right in range(8):
            expected = not core.action_values(left) or 1 not in core.action_values(right)
            assert core.action_compatible(left, right) is expected


def test_collision_multiplicity_distinguishes_mod_p_and_mod_p2() -> None:
    assert core.square_collision_count(2, 2) == 2
    assert core.tau_collision_multiplicity(2, 2, 0) == 2
    assert core.square_collision_count(2, 4) == 1
    assert core.tau_collision_multiplicity(2, 4, 0) == 1
    assert core.square_collision_count(3, 6) == 2
    assert core.tau_collision_multiplicity(3, 6, 0) == 2
    assert core.square_collision_count(3, 9) == 1
    assert core.tau_collision_multiplicity(3, 9, 0) == 1
    assert core.theta_local_factor(2, 4, 2, 0) == core.Fraction(1, 2)
    assert core.theta_local_factor(2, 2, 2, 0) == 0
    assert core.theta_local_factor(3, 6, 3, 0) == core.Fraction(1, 3)
    assert core.theta_local_factor(2, 2, 4, 1) == 1
    with pytest.raises(ValueError, match="prime"):
        core.theta_local_factor(4, 2, 1, 0)


def test_charge_cones_and_reflection_witnesses() -> None:
    certificate = core.build_certificate()
    nonplus_rows = certificate["charge_rows"][:4]
    plus_rows = certificate["charge_rows"][4:]
    assert [row["direct_loss_cone_coefficients"] for row in nonplus_rows] == [
        ["1", "1/2"], ["1", "0"], ["0", "1/2"], ["0", "0"]
    ]
    assert [row["gain_cone_coefficients"] for row in plus_rows] == [
        ["1", "1/2"], ["1", "0"], ["0", "1/2"], ["0", "0"]
    ]
    assert all(row["forced_predecessor_empty"] is True for row in plus_rows)
    assert core.reflected_table_id(36) == 72
    assert core.reflected_table_id(72) == 36


def test_global_closure_translation_and_capacity_definition() -> None:
    certificate = core.build_certificate()
    closure = certificate["contracts"]["global_closure"]
    assert closure == {
        "ordered_table_pair_count": 262144,
        "compatible_pair_count": 3375,
        "projection_compatibility_failures": 0,
        "reflection_compatibility_failures": 0,
        "reflection_involution_failures": 0,
        "coefficient_parity": ["+", "-", "-", "+", "+", "-"],
        "coefficient_parity_failures": 0,
        "coefficient_interpolation_failures": 0,
        "table_36_self_compatible": True,
        "table_72_self_compatible": True,
        "plus_action_self_compatible_count": 0,
        "pass": True,
    }
    oracle = {(row["q"], row["h"]): row for row in certificate["contracts"]["translation_oracle"]}
    assert (oracle[(4, 2)]["gcd"], oracle[(4, 2)]["cycle_count"], oracle[(4, 2)]["cycle_length"]) == (2, 2, 2)
    assert oracle[(6, 3)]["cycles"] == [[0, 3], [1, 4], [2, 5]]
    assert oracle[(2, 2)]["self_loop"] is True
    assert oracle[(2, 2)]["self_loop_forces_empty_plus_set"] is True
    capacity = certificate["landscape_rows"][5]
    assert capacity["definition"] == "G_log(q,h)=max_(f in finite safe A_(q,h)) |L_(q,h)(f)|"
    assert certificate["landscape_rows"][7]["witnesses"] == {
        "positive_table": 36, "positive_value": "+G_log(q,h)",
        "negative_table": 72, "negative_value": "-G_log(q,h)",
    }


def test_additional_semantic_leaf_attacks_rejected() -> None:
    certificate = core.build_certificate()
    attacks = []
    wrong_nu = deepcopy(certificate)
    wrong_nu["theta_rows"][2]["nu"] = 2
    attacks.append(wrong_nu)
    wrong_capacity = deepcopy(certificate)
    wrong_capacity["landscape_rows"][5]["formula"] = "G_log(q,h)=6/pi^2+kappa_h/2"
    attacks.append(wrong_capacity)
    wrong_c22 = deepcopy(certificate)
    wrong_c22["monomial_rows"][8]["limit_channel"] = "0"
    attacks.append(wrong_c22)
    wrong_global = deepcopy(certificate)
    wrong_global["contracts"]["global_closure"]["compatible_pair_count"] = 3374
    attacks.append(wrong_global)
    wrong_bridge = deepcopy(certificate)
    wrong_bridge["determinant_rows"][1]["mobius_liouville_identity"] = "mu=lambda"
    attacks.append(wrong_bridge)
    assert all(not core.verify_certificate(attack, compare_fresh=False) for attack in attacks)


def test_strict_types_membership_and_json_parser() -> None:
    certificate = core.build_certificate()
    wrong_bool_id = deepcopy(certificate)
    wrong_bool_id["truth_rows"][0]["table_id"] = False
    assert not core.verify_certificate(wrong_bool_id, compare_fresh=False)
    missing = deepcopy(certificate)
    del missing["theta_rows"][0]["nu_p"]
    assert not core.verify_certificate(missing, compare_fresh=False)
    extra = deepcopy(certificate)
    extra["landscape_rows"][0]["extra"] = 0
    assert not core.verify_certificate(extra, compare_fresh=False)
    assert core.loads_strict('{"a":1}') == {"a": 1}
    with pytest.raises(ValueError, match="duplicate JSON key"):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError, match="non-finite"):
        core.loads_strict('{"a":NaN}')
    with pytest.raises(ValueError, match="non-finite"):
        core.loads_strict('{"a":Infinity}')
    with pytest.raises(ValueError):
        core.canonical_json({"a": math.nan})


def test_exact_input_guards() -> None:
    with pytest.raises(TypeError):
        core.truth_values(True)
    with pytest.raises(TypeError):
        core.action_values(False)
    with pytest.raises(TypeError):
        core.verify_certificate(core.build_certificate(), compare_fresh=1)
    with pytest.raises(ValueError):
        core.mutate_certificate(core.build_certificate(), "unknown")
