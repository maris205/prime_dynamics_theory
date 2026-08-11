from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import centered_three_window_capacity.core as core


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


@pytest.fixture(scope="module")
def certificate() -> dict[str, object]:
    value = core.build_certificate()
    require(value["all_pass"] is True)
    return value


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_baseline_fixture_false_and_fresh(certificate: dict[str, object]) -> None:
    encoded = core.canonical_json_bytes(certificate)
    require(len(encoded) == core.CERTIFICATE_FIXTURE_BYTES)
    require(sha256(encoded).hexdigest() == core.CERTIFICATE_FIXTURE_SHA256)
    require(certificate["row_count"] == core.CERTIFICATE_FIXTURE_ROWS == 72)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)
    require(core.verify_certificate(certificate, compare_fresh=True) is True)


def test_exact_finite_audits(certificate: dict[str, object]) -> None:
    projection = certificate["projection_audit"]
    require(projection["pointwise_case_count"] == 54)
    require(projection["deleted_coordinate_count"] == 18)
    require(projection["pointwise_projection_pass"] is True)
    relation = certificate["relation_pair_audit"]
    require(relation["ordered_relation_pair_count"] == 262144)
    require(relation["safe_pair_count"] == 3375)
    require(relation["criterion_failure_count"] == 0)
    require(relation["saturation_failure_count"] == 0)
    reflection = certificate["reflection_audit"]
    require(reflection["ordered_safe_pair_count"] == 3375)
    require(reflection["lambda_sign_cell_case_count"] == 495)
    require(reflection["terminal_sign_identity"] == "L_q(F^rho)=-L_q(F)")
    require(reflection["both_signs_attained"] is True)


def test_q2_exception_and_exact_small_clocks(certificate: dict[str, object]) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    expected = {
        1: ["0", "1", "-1"],
        2: ["0", "3/4", "-1/4"],
        3: ["3/8", "0", "0"],
        4: ["2/3", "0", "0"],
        6: ["1/8", "1/2", "0"],
    }
    for q, coefficients in expected.items():
        require(by_id[f"clock_{q}"]["data"]["full8_coefficients"] == coefficients)
    require(by_id["clock_2"]["data"]["four_state_coefficients"] == ["0", "1", "-1"])
    require(by_id["q2_witness_summary"]["data"]["even_contribution"] == ["0", "1/4", "-1/4"])
    require(by_id["q2_witness_summary"]["data"]["odd_contribution"] == ["0", "1/2", "0"])
    q2_rows = [row for row in certificate["rows"] if row["kind"] == "q2_selfloop"]
    require(len(q2_rows) == 16)
    require(all(type(row["data"]["selfloop_coefficients"]) is list for row in q2_rows))


def test_generic_compression_and_square_interface(certificate: dict[str, object]) -> None:
    multi = certificate["multi_affinity_audit"]
    require(multi["context_count"] == 72)
    require(multi["second_difference_failure_count"] == 0)
    require(multi["state_variable_self_identification_q_1_to_10"] == {
        str(q): q in (1, 2) for q in range(1, 11)
    })
    square = certificate["square_marginal_interface_audit"]
    require(square["pass"] is True)
    require(square["forced_reset_moduli"] == [4, 9])
    require(square["path_bound"]["charges_L_0_to_12"] == [
        (length + 1) // 2 for length in range(13)
    ])
    require(all(row["left_right_per_t_equal"] is True for row in square["local_branches"]))
    marginal_rows = [row for row in certificate["rows"] if row["kind"] == "marginal_charge"]
    require(len(marginal_rows) == 12)
    require({row["data"]["shared_value"] for row in marginal_rows} == {-1, 0, 1})


def test_endpoint_rows_and_firewalls(certificate: dict[str, object]) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    require(by_id["q36_B1"]["data"]["capacity_coefficients"] == ["2/3", "0", "0"])
    require(by_id["q900_B2"]["data"]["capacity_coefficients"] == ["49/72", "0", "0"])
    require(by_id["one_site_q6"]["data"]["coefficients"] == ["3/8", "0", "0"])
    require(by_id["q6_strict_gain"]["data"]["difference_coefficients"] == ["-1/4", "1/2", "0"])
    require(by_id["q_divides_Q_lift"]["data"]["direction"] == "C(q)<=C(Q)")
    require(by_id["finite_nonattainment"]["data"]["finite_attainment"] is False)
    require(by_id["source_role_split"]["data"]["RH375_terminal_clock_analytic_input"] is False)
    ceiling = by_id["claim_ceiling"]["data"]
    require(ceiling["fixed_q_and_tables_only"] is True)
    require(all(ceiling[key] is False for key in (
        "growing_q", "rate", "ordinary_Cesaro", "prelimit_or_adaptive_max",
        "generic_graph_capacity", "even_odd_support_at_least_four",
        "operator_trace_zero_RH_or_Gates",
    )))


def test_every_named_semantic_mutation_is_rejected(certificate: dict[str, object]) -> None:
    require(len(core.MUTATION_NAMES) == 57)
    require(len(set(core.MUTATION_NAMES)) == len(core.MUTATION_NAMES))
    for name in core.MUTATION_NAMES:
        mutated = core.mutate_certificate(certificate, name)
        require(core.verify_certificate(mutated, compare_fresh=False) is False, name)


def test_false_mode_uses_no_global_builder_or_semantic_helper(
    certificate: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global helper called")

    for name in core.BUILDER_NAMES + core.SEMANTIC_HELPER_NAMES:
        monkeypatch.setattr(core, name, bomb)
    monkeypatch.setattr(core, "Fraction", bomb)
    monkeypatch.setattr(core, "sha256", bomb)
    monkeypatch.setattr(core, "json", bomb)
    monkeypatch.setattr(core, "math", bomb)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)


def test_coordinated_constants_seals_and_comparator_rebinding_fails_closed(
    certificate: dict[str, object], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(core, "TITLE", "wrong")
    monkeypatch.setattr(core, "ROW_PARTITION", {"subset_state": 72})
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_ROWS", 1)
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_BYTES", 1)
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_SHA256", "0" * 64)
    monkeypatch.setattr(core, "MUTATION_NAMES", ("fake",))
    monkeypatch.setattr(core, "exact_equal", lambda _left, _right: True)
    monkeypatch.setattr(core, "canonical_json_bytes", lambda _value: b"{}")
    require(core.verify_certificate(certificate, compare_fresh=False) is True)
    corrupted = deepcopy(certificate)
    corrupted["title"] = "wrong"
    require(core.verify_certificate(corrupted, compare_fresh=False) is False)


def test_type_shape_order_and_literal_attacks(certificate: dict[str, object]) -> None:
    attacks: list[dict[str, object]] = []
    item = deepcopy(certificate)
    item["row_count"] = 72.0
    attacks.append(item)
    item = deepcopy(certificate)
    item["all_pass"] = 1
    attacks.append(item)
    item = deepcopy(certificate)
    item["extra"] = 0
    attacks.append(item)
    item = deepcopy(certificate)
    item["rows"] = list(reversed(item["rows"]))
    attacks.append(item)
    item = deepcopy(certificate)
    del item["density_contract"]["pi"]
    attacks.append(item)
    item = deepcopy(certificate)
    item["rows"][0]["data"]["mask"] = True
    attacks.append(item)
    for attack in attacks:
        require(core.verify_certificate(attack, compare_fresh=False) is False)


def test_strict_json_and_exact_equality() -> None:
    require(core.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        core.loads_strict('{"a":NaN}')
    require(core.exact_equal(1, True) is False)
    require(core.exact_equal(1, 1.0) is False)


def test_no_bare_asserts_or_cache_contract() -> None:
    package_root = Path(__file__).resolve().parents[1]
    for path in (
        Path(__file__),
        package_root / "src" / "centered_three_window_capacity" / "core.py",
    ):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
    require(not any(path.name == "__pycache__" for path in package_root.rglob("__pycache__")))
    require(not any(path.suffix == ".pyc" for path in package_root.rglob("*.pyc")))


def test_certificate_is_strict_json_roundtrip(certificate: dict[str, object]) -> None:
    encoded = core.canonical_json_bytes(certificate)
    decoded = core.loads_strict(encoded.decode("utf-8"))
    require(core.exact_equal(decoded, certificate) is True)
    require(json.loads(encoded)["schema_version"] == 1)
