from __future__ import annotations

from copy import deepcopy
import json

import pytest

import growing_rank_filtration.core as core


def test_certificate_shape_hash_and_exact_verification() -> None:
    certificate = core.build_certificate()
    assert certificate["counts"] == {
        "kernel_rows": 12,
        "channel_rows": 7,
        "gamma_rows": 15,
        "factorial_rows": 12,
        "growing_rows": 10,
        "necessity_rows": 10,
        "contract_rows": 6,
        "oracle_rows_total": 72,
    }
    assert certificate["all_pass"] is True
    assert core.verify_certificate(certificate)
    assert len(core.canonical_json_bytes(certificate)) == 17571
    assert core.payload_sha256(certificate) == "e2116abd4aeb910c24ee470a520623f29f1f454bb9b5293840875da091682b3b"


def test_normalized_master_uses_safe_power_exponent() -> None:
    certificate = core.build_certificate()
    kernel = certificate["kernel_rows"]
    assert kernel[7]["A"] == "1/((1-x^-2)^s*(1-c/(x^2-1)))"
    assert kernel[10]["B"] == "1/((1-x^-2)^(s+1)*(1-c/(x^2-1)))"
    assert kernel[11]["coordinate_terms"] == [
        "c^s*(4-1/s)*A*epsilon",
        "c^s*((2s-1)/(2s+1))*B/x^2",
        "c^s*C*K!/(s*((2s-1)*L)^K)",
    ]
    assert kernel[11]["endpoint_multiplier"] == 126


def test_growing_window_and_full_K_are_symbolic_contracts() -> None:
    certificate = core.build_certificate()
    factorial = certificate["factorial_rows"]
    growing = certificate["growing_rows"]
    assert factorial[9]["D_domain"] == "positive real"
    assert factorial[9]["K_integer"] is True
    assert factorial[9]["index_domain"] == "exact integers 1<=k<floor(D)"
    assert factorial[9]["floor_D_le_D"] is True
    assert factorial[9]["ratio_numerator_le_D"] is True
    assert factorial[10]["chain"] == "j+1<=K-1<D<=(2r-1)*L"
    assert growing[0]["S_y"] == "floor((1-delta)*log(L)/log(7))"
    assert growing[3]["A_uniform_upper"] == 4
    assert growing[4]["B_uniform_upper"] == 4
    assert growing[5]["C_uniform_upper"] == 2
    assert growing[9]["limit_variable"] == "y->infinity"


def test_gamma_all_r_and_fixed_s_necessity_are_consumed() -> None:
    certificate = core.build_certificate()
    gamma = certificate["gamma_rows"]
    necessity = certificate["necessity_rows"]
    assert all(gamma[index]["positive"] is True for index in range(1, 6))
    assert gamma[13]["ratio_threshold_exponents"] == [1, 2, 6]
    assert gamma[14]["pass"] is True
    assert necessity[7]["two_point_bound"].startswith("|F(H+A)-F(H+B)")
    assert necessity[8]["gamma_source"] == "gamma_all_r row"
    assert necessity[9]["J_bridge"] == "sum_(j>=r)c^j*(J_j-I_(2j))/j=O(x^(-2r-1)/L)=o(x^(-2r))"
    assert necessity[9]["scope"] == "fixed s only in frozen P/J/I hierarchy"


def test_source_and_firewall_contracts() -> None:
    contracts = core.build_certificate()["contract_rows"]
    assert contracts[2]["git_rows"] == 87
    assert contracts[2]["remote_rows"] == 2
    assert contracts[2]["logical_rows"] == 89
    assert contracts[2]["all87_digest"] == "b86cb21288fe9c48304d90ae812829f5e44f4fac0a2b725a09e5c1512ca60cab"
    assert contracts[2]["logical89_digest"] == "2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922"
    assert contracts[3]["excluded"] == ["RH-389", "TPC-137", "Tao active-log source"]
    assert contracts[5]["gates_A_to_E"] == [False] * 5
    assert contracts[5]["pass"] is True


def test_field_verifier_never_calls_any_builder(monkeypatch: pytest.MonkeyPatch) -> None:
    certificate = core.build_certificate()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("fresh builder called")

    monkeypatch.setattr(core, "build_certificate", forbidden)
    for name in (
        "_kernel_rows",
        "_channel_rows",
        "_gamma_rows",
        "_factorial_rows",
        "_growing_rows",
        "_necessity_rows",
        "_contract_rows",
    ):
        monkeypatch.setattr(core, name, forbidden)
    monkeypatch.setattr(core, "GROUP_BUILDERS", {name: forbidden for name in core.GROUP_BUILDERS})
    assert core.verify_certificate(certificate, compare_fresh=False)


def test_twenty_four_genuine_mutations_fail_field_verification() -> None:
    certificate = core.build_certificate()
    assert len(core.MUTATION_NAMES) == 24
    results = core.mutation_results()
    assert [row["name"] for row in results] == list(core.MUTATION_NAMES)
    assert all(row["rejected"] is True for row in results)
    for name in core.MUTATION_NAMES:
        with pytest.raises((TypeError, ValueError, KeyError, IndexError)):
            core.verify_certificate(core.apply_mutation(certificate, name), compare_fresh=False)


def test_strict_json_rejects_duplicates_nonfinite_and_nonobjects() -> None:
    parsed = core.loads_strict('{"a":1,"b":[true,false]}')
    assert parsed == {"a": 1, "b": [True, False]}
    for text in ('{"a":1,"a":2}', '{"x":NaN}', '{"x":Infinity}', '[]', '1', 'null'):
        with pytest.raises((TypeError, ValueError)):
            core.loads_strict(text)


def test_exact_types_reject_bool_aliases_and_compare_mode_aliases() -> None:
    certificate = core.build_certificate()
    attacked = deepcopy(certificate)
    attacked["contract_rows"][2]["git_rows"] = True
    with pytest.raises((TypeError, ValueError)):
        core.verify_certificate(attacked, compare_fresh=False)
    for value in (0, 1, "false", None):
        with pytest.raises(TypeError):
            core.verify_certificate(certificate, compare_fresh=value)


def test_fresh_comparison_uses_canonical_bytes_not_python_bool_int_equality() -> None:
    certificate = core.build_certificate()
    attacked = deepcopy(certificate)
    attacked["counts"]["kernel_rows"] = True
    assert core.canonical_json_bytes(attacked) != core.canonical_json_bytes(certificate)
    with pytest.raises((TypeError, ValueError)):
        core.verify_certificate(attacked)


def _scalar_paths(value: object, prefix: tuple[object, ...] = ()) -> list[tuple[object, ...]]:
    if type(value) is dict:
        output: list[tuple[object, ...]] = []
        for key, item in value.items():
            output.extend(_scalar_paths(item, prefix + (key,)))
        return output
    if type(value) is list:
        output = []
        for index, item in enumerate(value):
            output.extend(_scalar_paths(item, prefix + (index,)))
        return output
    return [prefix]


def _mutate_scalar(value: object) -> object:
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if type(value) is str:
        return value + "__MUT"
    raise TypeError(f"unsupported scalar type {type(value).__name__}")


def _replace_path(value: object, path: tuple[object, ...]) -> None:
    target = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = _mutate_scalar(target[path[-1]])


def test_every_scalar_leaf_is_fail_closed_under_field_verification() -> None:
    certificate = core.build_certificate()
    paths = _scalar_paths(certificate)
    assert len(paths) > 250
    escaped: list[tuple[object, ...]] = []
    for path in paths:
        attacked = deepcopy(certificate)
        _replace_path(attacked, path)
        try:
            core.verify_certificate(attacked, compare_fresh=False)
        except (TypeError, ValueError, KeyError, IndexError):
            continue
        escaped.append(path)
    assert escaped == []


def test_canonical_json_round_trip_is_exact() -> None:
    certificate = core.build_certificate()
    text = core.canonical_json_bytes(certificate).decode("utf-8")
    assert core.loads_strict(text) == certificate
    assert json.loads(text) == certificate
