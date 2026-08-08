from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from terminal_log_capacity import core  # noqa: E402


def test_certificate_has_exact_602_row_partition_and_hash() -> None:
    certificate = core.build_certificate()
    assert certificate["all_pass"] is True
    assert certificate["counts"] == core.EXPECTED_COUNTS
    assert certificate["contracts"]["row_partition"] == [512, 8, 64, 8, 6, 4]
    assert sum(certificate["contracts"]["row_partition"]) == 602
    assert core.verify_certificate(certificate, compare_fresh=False)
    assert core.verify_certificate(certificate, compare_fresh=True)
    assert len(core.canonical_json(certificate).encode("utf-8")) == 208648
    assert core.payload_sha256(certificate) == "b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020"


def test_projection_is_exact_pointwise_and_has_eight_equal_fibres() -> None:
    certificate = core.build_certificate()
    truth = certificate["truth_rows"]
    assert len(truth) == 512
    assert all(row["projected_table_id"] in core.ACTION_MASKS for row in truth)
    assert all(row["projected_plus_subset"] is True for row in truth)
    assert all(row["projected_only_z_plus"] is True for row in truth)
    assert all(row["all_pointwise_gains_nonnegative"] is True for row in truth)
    assert all(len(row["pointwise_zf_gains"]) == 9 for row in truth)
    assert [row["preimage_count"] for row in certificate["projected_action_rows"]] == [64] * 8
    assert [row["projected_mask"] for row in certificate["projected_action_rows"]] == list(core.ACTION_MASKS)


def test_projected_action_weights_are_independently_interpolated() -> None:
    rows = core.build_certificate()["projected_action_rows"]
    expected = [
        ("0", "0"), ("0", "1/2"), ("1", "-1"), ("1", "-1/2"),
        ("0", "1/2"), ("0", "1"), ("1", "-1/2"), ("1", "0"),
    ]
    assert [(row["c02_delta_coefficient"], row["c22_theta_coefficient"]) for row in rows] == expected
    for row in rows:
        coefficients = tuple(core.parse_fraction(value) for value in row["coefficients"])
        assert coefficients == core.coefficient_vector(row["projected_mask"])
    assert any(core.parse_fraction(row["coefficients"][2]) != 0 for row in rows)


def test_directed_compatibility_is_eight_then_four_targets() -> None:
    certificate = core.build_certificate()
    rows = certificate["compatibility_rows"]
    assert len(rows) == 64
    assert [row["compatible_target_count"] for row in certificate["projected_action_rows"]] == [8, 4, 4, 4, 4, 4, 4, 4]
    for row in rows:
        expected = row["left_empty"] or not row["right_contains_plus_one"]
        assert row["compatible"] is expected
        assert row["edge_triple_recomputed"] is True
    assert certificate["contracts"]["projection_global_contract"] == {
        "compatible_original_pair_count": 3375,
        "ordered_table_pair_count": 262144,
        "pass": True,
        "projection_compatibility_failures": 0,
        "table_count": 512,
    }


def test_charge_cones_predecessor_identity_and_small_q_disjointness_are_exact() -> None:
    rows = core.build_certificate()["charge_rows"]
    for row in rows:
        relative_delta = core.parse_fraction(row["relative_delta_coefficient"])
        relative_theta = core.parse_fraction(row["relative_theta_coefficient"])
        cap = core.parse_fraction(row["cap_theta_coefficient"])
        cone_a, cone_b = (core.parse_fraction(value) for value in row["gain_cap_cone_coefficients"])
        assert cone_a == -relative_delta >= 0
        assert cone_b == cap - relative_theta - relative_delta >= 0
        if row["contains_plus_one"]:
            assert row["forced_predecessor_action_id"] == 0
            assert row["predecessor_offset_mod_q"] == -2
            assert row["predecessor_loss_decomposition"] == ["1/2", "1/2"]
            assert row["predecessor_pair_inclusions"] == [
                "theta_(r-2)<=delta_(r-2)", "theta_r<=delta_(r-2)",
            ]
            assert row["allowed_predecessor_action_ids"] == [0]
            assert row["composition_offset_mod_q"] == 0
            assert row["injective_predecessor_map"] is True
            assert row["plus_phase_disjointness"] is True
            assert "q in {1,2} implies P=empty" in row["plus_phase_disjointness_statement"]
        else:
            assert cap == 0


def test_optimizer_witness_and_input_reflection_are_exact() -> None:
    certificate = core.build_certificate()
    optimizer = certificate["analytic_rows"][4]
    reflection = certificate["analytic_rows"][5]
    assert optimizer["signed_capacity"] == "6/pi^2-kappa2/2"
    assert optimizer["attained_by"] == {"action_id": 3, "projected_mask": 36, "q": "every fixed q>=1", "set": [-1, 0], "table_id": 36}
    assert optimizer["charge_contract"]["self_loop_moduli_for_offset_minus_two"] == [1, 2]
    assert optimizer["charge_contract"]["plus_actions_self_incompatible"] is True
    assert optimizer["charge_contract"]["baseline_attains_for_every_fixed_q"] is True
    assert core.reflected_table_id(36) == 72
    assert core.coefficient_vector(36) == tuple(Fraction(value) for value in (0, 1, Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(-1, 2)))
    assert core.coefficient_vector(72) == tuple(Fraction(value) for value in (0, -1, Fraction(1, 2), Fraction(-1, 2), Fraction(-1, 2), Fraction(1, 2)))
    assert reflection["witness_coefficient_reflection"]["table_72"] == ["0", "-1", "1/2", "-1/2", "-1/2", "1/2"]
    assert "c02,c11,c22 negate" in reflection["input_reflection"]
    assert reflection["negative_witness"] == {"q": "every fixed q>=1", "table_id": 72}
    assert reflection["global_reflection_contract"] == {
        "coefficient_parity_failure_count": 0,
        "coefficient_sign_pattern": ["+", "-", "-", "+", "+", "-"],
        "compatible_original_pair_count": 3375,
        "involution_failure_count": 0,
        "ordered_table_pair_count": 262144,
        "pass": True,
        "reflection_compatibility_failure_count": 0,
        "table_count": 512,
    }


def test_analytic_source_roles_quantifiers_and_firewalls_are_exact() -> None:
    certificate = core.build_certificate()
    terminal, active, abel, density, _, absolute = certificate["analytic_rows"]
    assert terminal["omega_range"] == "1<=omega(X)<=X"
    assert terminal["omega_limit"] == "omega(X)->infinity"
    assert terminal["clock_quantifier"].startswith("q is fixed")
    assert active["active_c11"] is True
    assert active["D"] == {"intercept": -2, "slope": 1}
    assert active["V"] == {"intercept": 0, "slope": 1}
    assert active["determinant"] == 2
    assert active["source_role"].startswith("TPC-137")
    assert "upstream Liouville input" in active["source_role"]
    assert "johnston" not in active["source_role"].lower()
    assert "maynard" not in active["source_role"].lower()
    assert abel["mobius_zero_channels"] == ["c01", "c12", "c21"]
    assert density["single_density_total"].endswith("6/pi^2")
    assert density["pair_density_total"].endswith("kappa2")
    assert absolute["limit_order"].startswith("first take")
    forbidden = sum((row["forbidden"] for row in certificate["scope_rows"]), [])
    for phrase in ("ordinary Cesaro average", "q=q(X)", "max before limit", "K_N", "operator", "Riemann Hypothesis"):
        assert phrase in forbidden
    assert certificate["scope_rows"][3]["gates"] == {"A": False, "B": False, "C": False, "D": False, "E": False}


def test_twenty_four_genuine_mutations_fail_field_level_verification() -> None:
    certificate = core.build_certificate()
    rejected = []
    for name in core.MUTATION_NAMES:
        candidate = core.apply_mutation(certificate, name)
        assert not core.exact_equal(candidate, certificate), name
        if not core.verify_certificate(candidate, compare_fresh=False):
            rejected.append(name)
    assert rejected == list(core.MUTATION_NAMES)


def test_field_level_verifier_does_not_call_any_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("a builder was called by field-level verification")

    for name in (
        "build_certificate", "_truth_rows", "_action_rows", "_compatibility_rows",
        "_charge_rows", "_analytic_rows", "_scope_rows", "_contracts",
    ):
        monkeypatch.setattr(core, name, forbidden)
    assert core.verify_certificate(certificate, compare_fresh=False)


def test_exact_types_bool_alias_and_compare_flag_fail_closed() -> None:
    certificate = core.build_certificate()
    for value in (0, 1, "false", None):
        with pytest.raises(TypeError, match="exact Boolean"):
            core.verify_certificate(certificate, compare_fresh=value)  # type: ignore[arg-type]
    attacks = []
    candidate = json.loads(json.dumps(certificate))
    candidate["counts"]["truth_rows"] = True
    attacks.append(candidate)
    candidate = json.loads(json.dumps(certificate))
    candidate["truth_rows"][0]["table_id"] = False
    attacks.append(candidate)
    candidate = json.loads(json.dumps(certificate))
    candidate["scope_rows"][3]["gates"]["A"] = 0
    attacks.append(candidate)
    candidate = json.loads(json.dumps(certificate))
    candidate["unexpected"] = None
    attacks.append(candidate)
    assert all(not core.verify_certificate(candidate, compare_fresh=False) for candidate in attacks)


def test_optimized_mode_is_byte_identical() -> None:
    code = (
        "import sys;"
        f"sys.path.insert(0,{str(ROOT / 'src')!r});"
        "from terminal_log_capacity import core;"
        "c=core.build_certificate();"
        "print(len(core.canonical_json(c).encode()),core.payload_sha256(c),core.verify_certificate(c,compare_fresh=False))"
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
    assert completed.stdout.strip() == "208648 b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020 True"
