from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

import pytest

import fixed_lag_centered_capacity.core as core


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
    require(len(encoded) == core.CERTIFICATE_FIXTURE_BYTES == 83309)
    require(
        sha256(encoded).hexdigest()
        == core.CERTIFICATE_FIXTURE_SHA256
        == "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba"
    )
    require(certificate["row_count"] == core.CERTIFICATE_FIXTURE_ROWS == 96)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)
    require(core.verify_certificate(certificate, compare_fresh=True) is True)


def test_exact_partition_order_and_ids(certificate: dict[str, object]) -> None:
    require(certificate["row_partition"] == core.ROW_PARTITION)
    expected = [
        (group, identifier)
        for group, identifiers in core.GROUP_IDS.items()
        for identifier in identifiers
    ]
    actual = [(row["group"], row["id"]) for row in certificate["rows"]]
    require(actual == expected)
    require(len(actual) == len(set(actual)) == 96)
    require(list(certificate["row_ids"]) == list(core.GROUP_IDS))


def test_density_empty_support_mass_and_prime_domain(certificate: dict[str, object]) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    require(by_id["B07_theta_empty"]["data"]["coefficients"] == ["1/36", "0", "0", "0"])
    require(
        by_id["B11_Pi_phase_mass"]["data"]["sum_over_8_exact_supports"]
        == by_id["B11_Pi_phase_mass"]["data"]["theta_empty"]
    )
    require(core.theta_coefficients(9, 36, 17, ()) == (
        core.Fraction(1, 36), core.Fraction(0), core.Fraction(0), core.Fraction(0)
    ))
    with pytest.raises(ValueError):
        core.residue_set(1, 4, ("L", "C"))
    with pytest.raises(ValueError):
        core.nu_support(1, 1, ("L", "C"))


def test_relation_full8_and_selfloop_exception(certificate: dict[str, object]) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    oracle = by_id["C16_dynamic_relation_oracle"]["data"]
    require(oracle["ordered_pair_count"] == 262144)
    require(oracle["safe_pair_count"] == 3375)
    require(all(oracle[key] == 0 for key in (
        "compatibility_failure_count", "inclusion_failure_count",
        "saturation_failure_count", "reflection_failure_count",
    )))
    selfloop = by_id["D02_selfloop_full8_required"]["data"]
    require(selfloop["full8"] == ["0", "0", "1/2", "-1/2"])
    require(selfloop["forbidden_four"] == ["0", "0", "1", "-2"])
    require(selfloop["full8_strictly_larger"] is True)
    brute = by_id["D12_full8_vs_four_bruteforce_and_forbidden_allq_claim"]["data"]
    require(all(row["dp"] == row["brute"] for row in brute["brute_rows"]))
    require(brute["four_state_all_q"] is False)


def test_square_fixtures_cover_domain_and_marginal_charge(
    certificate: dict[str, object],
) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    fixtures = by_id["E12_exact_fixtures"]["data"]["fixtures"]
    expected = {
        (1, 36): (24, 16), (1, 900): (576, 392),
        (2, 36): (24, 12), (2, 900): (576, 300),
        (3, 900): (576, 386), (6, 36): (24, 9),
        (6, 72): (48, 24), (6, 900): (576, 291),
        (6, 1800): (1152, 582),
    }
    require({(row["h"], row["q"]): (row["positive"], row["mwis"]) for row in fixtures} == expected)
    require(by_id["E06_same_support_domain"]["data"]["pre_p0_counterexample"]["equal"] is False)
    covers = by_id["E11_same_support_scaling"]["data"]["fixture_rows"]
    require(all(row["pass"] is True for row in covers))
    require(all(row["gcd_multiplier_step"] > 1 for row in covers))
    require(by_id["E08_shared_coordinate_marginal_all_t"]["data"]["marginal_failures"] == 0)
    require(by_id["E09_pair_charge"]["data"]["mask_triple_failure_count"] == 0)


def test_run_endpoint_strict_lift_and_landscape(certificate: dict[str, object]) -> None:
    by_id = {row["id"]: row for row in certificate["rows"]}
    require(all(row["pass"] is True for row in by_id["F08_finite_run_MWIS_identity"]["data"]["fixtures"]))
    numerical = by_id["F12_numeric_intervals"]["data"]["rows"]
    require([row["quoted_orientation_only"] for row in numerical] == [
        "0.421926446", "0.328926097", "0.416224610"
    ])
    require(all(row["quoted_value_inside"] is True for row in numerical))
    strict = by_id["G06_normalized_gain_E"]["data"]["fixture"]
    require(strict["old_positive"] == 576)
    require(strict["new_positive"] == strict["predicted_positive"] == 27648)
    require(strict["new_mwis"] == strict["predicted_mwis"] == 14253)
    require(strict["even_excess"] == 285)
    require(by_id["G01_fresh_p_domain"]["data"]["pre_p0_counterexample"] == {
        "h": 1, "q": 4, "P": 3,
        "old_all_positive_cycles": [2],
        "actual_new_M": 16, "naive_path_formula_M": 17,
    })
    require(by_id["G07_CRT_exact_length2_run"]["data"]["pass"] is True)
    require(all(row["pass"] is True for row in by_id["H01_CRT_exact_length1_run"]["data"]["fixtures"]))
    require("outside-prime Euler tail" in by_id["H02_each_h_strict_baseline"]["data"]["analytic_proof_obligation"])
    require(by_id["H07_inf_unattained"]["data"]["attained"] is False)


def test_every_named_semantic_mutation_is_distinct_and_rejected(
    certificate: dict[str, object],
) -> None:
    require(len(core.MUTATION_NAMES) == len(set(core.MUTATION_NAMES)) == 32)
    digests = []
    for name in core.MUTATION_NAMES:
        mutated = core.mutate_certificate(certificate, name)
        require(core.verify_certificate(mutated, compare_fresh=False) is False, name)
        digests.append(sha256(core.canonical_json_bytes(mutated)).hexdigest())
    require(len(set(digests)) == 32)
    with pytest.raises(ValueError):
        core.mutate_certificate(certificate, "not_a_mutation")


def test_false_mode_uses_no_builder_semantic_helper_or_rebindable_global(
    certificate: dict[str, object], monkeypatch: pytest.MonkeyPatch,
) -> None:
    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden global called")

    for name in core.BUILDER_NAMES + core.SEMANTIC_HELPER_NAMES:
        monkeypatch.setattr(core, name, bomb)
    for name in ("Fraction", "sha256", "json", "math", "deepcopy"):
        monkeypatch.setattr(core, name, bomb)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)


def test_coordinated_constants_comparators_and_pass_edits_fail_closed(
    certificate: dict[str, object], monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(core, "TITLE", "wrong")
    monkeypatch.setattr(core, "PACKAGE", "wrong")
    monkeypatch.setattr(core, "GROUP_IDS", {"fake": ("fake",)})
    monkeypatch.setattr(core, "ROW_PARTITION", {"fake": 96})
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_ROWS", 1)
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_BYTES", 1)
    monkeypatch.setattr(core, "CERTIFICATE_FIXTURE_SHA256", "0" * 64)
    monkeypatch.setattr(core, "MUTATION_NAMES", ("fake",))
    monkeypatch.setattr(core, "exact_equal", lambda _left, _right: True)
    monkeypatch.setattr(core, "canonical_json_bytes", lambda _value: b"{}")
    require(core.verify_certificate(certificate, compare_fresh=False) is True)

    coordinated = deepcopy(certificate)
    row = next(item for item in coordinated["rows"] if item["id"] == "G02_positive_count_Nprime")
    row["data"]["predicted_N"] = row["data"]["old_N"] * 49
    row["pass"] = True
    coordinated["all_pass"] = True
    require(core.verify_certificate(coordinated, compare_fresh=False) is False)


def test_type_shape_order_and_literal_attacks(certificate: dict[str, object]) -> None:
    attacks: list[dict[str, object]] = []
    item = deepcopy(certificate)
    item["row_count"] = 96.0
    attacks.append(item)
    item = deepcopy(certificate)
    item["all_pass"] = 1
    attacks.append(item)
    item = deepcopy(certificate)
    item["extra"] = 0
    attacks.append(item)
    item = dict(reversed(list(deepcopy(certificate).items())))
    attacks.append(item)
    item = deepcopy(certificate)
    item["rows"] = list(reversed(item["rows"]))
    attacks.append(item)
    item = deepcopy(certificate)
    item["rows"][0]["data"]["boundary_extension_only"] = 1
    attacks.append(item)
    item = deepcopy(certificate)
    item["row_ids"]["strict_lift_CRT"] = list(reversed(item["row_ids"]["strict_lift_CRT"]))
    attacks.append(item)
    for attack in attacks:
        require(core.verify_certificate(attack, compare_fresh=False) is False)


def test_strict_json_exact_equality_and_roundtrip(certificate: dict[str, object]) -> None:
    require(core.loads_strict('{"a":1}') == {"a": 1})
    with pytest.raises(ValueError):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        core.loads_strict('{"a":NaN}')
    require(core.exact_equal(1, True) is False)
    require(core.exact_equal(1, 1.0) is False)
    encoded = core.canonical_json_bytes(certificate)
    require(core.exact_equal(core.loads_strict(encoded.decode("utf-8")), certificate) is True)
    require(json.loads(encoded)["schema_version"] == 1)


def test_no_bare_asserts_float_literals_or_cache_artifacts() -> None:
    package_root = Path(__file__).resolve().parents[1]
    paths = (
        Path(__file__),
        package_root / "src" / "fixed_lag_centered_capacity" / "core.py",
    )
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
        if path.name == "core.py":
            require(not any(
                isinstance(node, ast.Constant) and type(node.value) is float
                for node in ast.walk(tree)
            ))
    require(not any(path.name == "__pycache__" for path in package_root.rglob("__pycache__")))
    require(not any(path.suffix == ".pyc" for path in package_root.rglob("*.pyc")))
    require(not (package_root / ".pytest_cache").exists())
