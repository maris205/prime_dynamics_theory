from __future__ import annotations

import ast
from copy import deepcopy
from itertools import product as standard_product
import json
from pathlib import Path

import pytest

import odd_parity_compiler.core as core


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_baseline_false_and_fresh() -> None:
    certificate = core.build_certificate()
    require(certificate["all_pass"] is True)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)
    require(core.verify_certificate(certificate, compare_fresh=True) is True)
    require(len(core.certificate_bytes()) > 50_000)


def test_exact_main_formulas() -> None:
    require([core.admitted_dimension(m) for m in range(1, 5)] == [3, 9, 27, 80])
    require([core.current_stratum_count(k) for k in range(5)] == [2, 4, 16, 70, 648])
    require([core.brute_stratum_count(k) for k in range(5)] == [2, 4, 16, 70, 648])
    require(core.current_table_count(2) == 512)
    require(core.current_table_count(3) == 36_700_160)


def test_current_interpolation_and_phase_mass_are_dynamic() -> None:
    certificate = core.build_certificate()
    require(all(row["disallowed_nonzero_count"] == 0 for row in certificate["current_table_rows"]))
    require(all(row["eligible"] is True for row in certificate["current_table_rows"]))
    for row in certificate["phase_rows"]:
        require(row["pi_numerators"] == row["recovered_pi_numerators"])
        require(row["phase_mass_numerator"] * row["q"] == row["common_denominator"])


def test_every_semantic_mutation_is_rejected() -> None:
    certificate = core.build_certificate()
    require(len(core.MUTATION_NAMES) == 32)
    for name in core.MUTATION_NAMES:
        mutated = core.mutate_certificate(certificate, name)
        require(core.verify_certificate(mutated, compare_fresh=False) is False, name)


def test_false_mode_uses_no_builder_or_semantic_helper(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden helper called")

    for name in core.BUILDER_NAMES + core.SEMANTIC_HELPER_NAMES:
        monkeypatch.setattr(core, name, bomb)
    require(core.verify_certificate(certificate, compare_fresh=False) is True)


def test_coordinated_global_rebinding_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(core, "TITLE", "wrong")
    monkeypatch.setattr(core, "EPISTEMIC_ROLE", "analytic_proof")
    monkeypatch.setattr(core, "ROW_PARTITION", (80, 17, 512, 8, 8, 8, 8, 8, 9))
    monkeypatch.setattr(core, "ROW_COUNT", 658)
    corrupted = core.build_certificate()
    require(core.verify_certificate(corrupted, compare_fresh=False) is False)


def test_rebound_validator_and_cartesian_product_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    baseline = core.build_certificate()
    monkeypatch.setattr(core, "_local_semantic_verify", lambda _value: True)
    require(core.verify_certificate([], compare_fresh=False) is False)
    require(core.verify_certificate(baseline, compare_fresh=False) is True)

    def reversed_product(*args: object, **kwargs: object) -> object:
        return reversed(tuple(standard_product(*args, **kwargs)))

    monkeypatch.setattr(core, "product", reversed_product)
    corrupted = core.build_certificate()
    require(corrupted["all_pass"] is True)
    require(core.verify_certificate(corrupted, compare_fresh=False) is False)


def test_type_shape_and_order_attacks() -> None:
    certificate = core.build_certificate()
    attacks = []
    item = deepcopy(certificate)
    item["row_count"] = 658.0
    attacks.append(item)
    item = deepcopy(certificate)
    item["summary"]["m3_admitted"] = True
    attacks.append(item)
    item = deepcopy(certificate)
    item["extra"] = 0
    attacks.append(item)
    item = deepcopy(certificate)
    item["monomial_rows"] = list(reversed(item["monomial_rows"]))
    attacks.append(item)
    item = deepcopy(certificate)
    del item["analytic_rows"]
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
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
