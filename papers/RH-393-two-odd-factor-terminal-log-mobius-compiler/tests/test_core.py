from __future__ import annotations

from copy import deepcopy
import hashlib

import pytest

import two_odd_compiler.core as core


def require(condition: bool, message: str = "test requirement failed") -> None:
    if condition is not True:
        raise AssertionError(message)


def test_baseline_and_deterministic_certificate() -> None:
    first = core.build_certificate()
    second = core.build_certificate()
    require(first["all_pass"] is True)
    require(core.verify_certificate(first, compare_fresh=False))
    require(core.verify_certificate(first, compare_fresh=True))
    require(core.canonical_json_bytes(first) == core.canonical_json_bytes(second))
    require(first["row_partition"] == [512, 27, 8, 12, 9, 8])
    require(first["row_count"] == 576)
    require(len(hashlib.sha256(core.canonical_json_bytes(first)).hexdigest()) == 64)


def test_truth_census_and_dimension_ledger() -> None:
    certificate = core.build_certificate()
    truth = certificate["truth_rows"]
    require(sum(row["eligible"] for row in truth) == 192)
    require(sum(row["outside_theorem"] for row in truth) == 320)
    patterns: dict[tuple[int, ...], int] = {}
    for row in truth:
        if row["eligible"]:
            key = tuple(row["corner_values"])
            patterns[key] = patterns.get(key, 0) + 1
    require(len(patterns) == 6)
    require(set(patterns.values()) == {32})
    dimension = certificate["dimension_rows"][2]
    require(dimension["odd_count_0"] == 8)
    require(dimension["odd_count_1"] == 12)
    require(dimension["odd_count_2"] == 6)
    require(dimension["allowed_dimension"] == 26)
    require(dimension["missing_dimension"] == 1)


def test_exact_finite_crt_vectors() -> None:
    vectors = [
        [[1, 1]],
        [[16, 25]],
        [[7, 18]],
        [[0, 1], [7, 18]],
        [[7, 36], [7, 18]],
        [[0, 1], [7, 36], [0, 1], [7, 36]],
        [[0, 1], [1, 6]],
        [[1, 18], [1, 18], [1, 18]],
        [[0, 1], [1, 12], [1, 12]],
        [[1, 9], [1, 6], [1, 6]],
        [[0, 1], [0, 1], [0, 1], [0, 1]],
        [
            [0, 1], [11, 225], [0, 1], [0, 1], [0, 1], [11, 150],
            [0, 1], [0, 1], [0, 1], [11, 450], [0, 1], [0, 1],
        ],
    ]
    masses = [
        [1, 1], [16, 25], [7, 18], [7, 18], [7, 12], [7, 18],
        [1, 6], [1, 6], [1, 6], [4, 9], [0, 1], [11, 75],
    ]
    rows = core.build_certificate()["theta_rows"]
    require([row["phase_densities"] for row in rows] == vectors)
    require([[
        row["phase_mass_numerator"], row["phase_mass_denominator"]
    ] for row in rows] == masses)
    require(all(row["phase_densities"] == row["predicted_phase_densities"] for row in rows))


def test_landscape_oracles_are_consumed() -> None:
    rows = core.build_certificate()["landscape_rows"]
    require([row.get("oracle_failures", 0) for row in rows] == [0] * 9)
    require(rows[3]["covered_residues"] == [0, 1, 2, 3])
    require(rows[7]["sample_Q"] == 900)
    require(rows[7]["small_prime_nu"] == [1, 1, 1])
    require(rows[7]["sample_tail_nu"] == 4)
    require(rows[8]["sample_phase_vector"] == [[0, 1], [7, 18]])
    require(rows[8]["sample_global_kappa"] == [7, 18])


def test_every_existing_leaf_mutation_is_rejected() -> None:
    baseline = core.build_certificate()
    require(len(core.MUTATION_NAMES) >= 24)
    escapes = [
        mutation
        for mutation in core.MUTATION_NAMES
        if core.verify_certificate(core.mutate_certificate(baseline, mutation))
    ]
    require(escapes == [], f"semantic mutation escapes: {escapes}")


def test_false_mode_forbids_all_builders_and_shared_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    baseline = core.build_certificate()

    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("false verifier invoked a forbidden helper")

    for name in core.BUILDER_NAMES + core.SEMANTIC_HELPER_NAMES:
        monkeypatch.setattr(core, name, forbidden)
    require(core.verify_certificate(baseline, compare_fresh=False))


def test_coordinated_constructor_corruption_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    with monkeypatch.context() as context:
        original = core.build_truth_rows

        def corrupt_truth() -> list[dict[str, object]]:
            rows = original()
            rows[257]["c11_numerator"] = 2
            return rows

        context.setattr(core, "build_truth_rows", corrupt_truth)
        corrupt = core.build_certificate()
        require(corrupt["all_pass"] is True)
        require(not core.verify_certificate(corrupt, compare_fresh=False))
    with monkeypatch.context() as context:
        original = core._build_landscape_contracts

        def corrupt_landscape() -> list[dict[str, object]]:
            rows = original()
            rows[5]["value"] = "1"
            return rows

        context.setattr(core, "_build_landscape_contracts", corrupt_landscape)
        corrupt = core.build_certificate()
        require(corrupt["all_pass"] is True)
        require(not core.verify_certificate(corrupt, compare_fresh=False))
    with monkeypatch.context() as context:
        original = core._build_analytic_contracts

        def corrupt_analytic() -> list[dict[str, object]]:
            rows = original()
            rows[0]["functional"] = "1"
            return rows

        context.setattr(core, "_build_analytic_contracts", corrupt_analytic)
        corrupt = core.build_certificate()
        require(corrupt["all_pass"] is True)
        require(not core.verify_certificate(corrupt, compare_fresh=False))
    with monkeypatch.context() as context:
        changed_cases = list(core.THETA_CASES)
        changed_cases[0] = ((0,), (2, 3), 1, 0)
        context.setattr(core, "THETA_CASES", tuple(changed_cases))
        corrupt = core.build_certificate()
        require(not core.verify_certificate(corrupt, compare_fresh=False))


def test_malformed_topology_and_exact_types_are_rejected() -> None:
    baseline = core.build_certificate()
    variants: list[dict[str, object]] = []
    missing = deepcopy(baseline)
    del missing["analytic_rows"]
    variants.append(missing)
    extra = deepcopy(baseline)
    extra["unexpected"] = False
    variants.append(extra)
    reordered = deepcopy(baseline)
    reordered["truth_rows"][0], reordered["truth_rows"][1] = (
        reordered["truth_rows"][1], reordered["truth_rows"][0]
    )
    variants.append(reordered)
    boolean_count = deepcopy(baseline)
    boolean_count["row_count"] = True
    variants.append(boolean_count)
    float_partition = deepcopy(baseline)
    float_partition["row_partition"][2] = 8.0
    variants.append(float_partition)
    require(all(not core.verify_certificate(item) for item in variants))
    require(not core.verify_certificate([]))


def test_strict_json_and_public_prime_domain() -> None:
    with pytest.raises(ValueError):
        core.loads_strict('{"a":1,"a":2}')
    with pytest.raises(ValueError):
        core.loads_strict('{"a":NaN}')
    with pytest.raises(TypeError):
        core.loads_strict(b"{}")
    with pytest.raises(ValueError):
        core.local_theta_data((0, 1), 4, 0, 0)
    with pytest.raises(ValueError):
        core.local_theta_data((0, 1), True, 0, 0)


def test_unknown_mutation_is_rejected() -> None:
    with pytest.raises(ValueError):
        core.mutate_certificate(core.build_certificate(), "unknown")
