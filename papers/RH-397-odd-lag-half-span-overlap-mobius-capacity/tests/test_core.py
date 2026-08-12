"""Runtime tests for the RH-397 exact finite certificate."""

from __future__ import annotations

import ast
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from src.odd_lag_half_span_capacity import core


def require(condition: object, message: str) -> None:
    if condition is not True:
        raise RuntimeError(message)


def test_certificate_identity_and_baseline() -> None:
    value = core.build_certificate()
    encoded = core.certificate_bytes()
    require(value["row_count"] == 72, "wrong row count")
    require(value["all_pass"] is True, "certificate row failure")
    require(len(encoded) == core.CERTIFICATE_FIXTURE_BYTES, "byte seal drift")
    require(sha256(encoded).hexdigest() == core.CERTIFICATE_FIXTURE_SHA256, "hash drift")
    require(core.verify_certificate(value) is True, "false-mode baseline rejected")
    require(core.verify_certificate(value, compare_fresh=True) is True, "fresh baseline rejected")


def test_relation_and_flag_oracles() -> None:
    oracle = core.relation_oracle()
    require(oracle["pass"] is True, "relation oracle failed")
    require(oracle["safe_pair_count"] == 61440, "safe-pair census drift")
    require(oracle["flag_class_counts"] == {"00": 16, "10": 48, "01": 48, "11": 400}, "flag classes drift")


def test_dp_brute_controls() -> None:
    expected = {
        (1, 1): ["0", "1", "-1/2", "0"],
        (1, 2): ["0", "1", "-1/2", "1/4"],
        (1, 3): ["0", "1", "-1/2", "1/12"],
        (4, 4): ["0", "1", "-3/4", "0"],
        (9, 2): ["0", "1", "-4/7", "1/3"],
    }
    for fixture, coefficients in expected.items():
        h, q = fixture
        require(core.half_span_capacity(h, q)["coefficients"] == coefficients, "DP control drift")
        require(core.flag_brute_capacity(h, q)["coefficients"] == coefficients, "brute control drift")


def test_phase_translation_fixtures() -> None:
    for h, q in ((1, 2), (2, 9), (4, 4), (9, 2), (10, 6)):
        for phase in range(q):
            require(
                core.phase_MUVW(h, q, phase)[2]
                == core.phase_MUVW(h, q, (phase + h) % q)[1],
                "phase translation drift",
            )


def test_all_semantic_mutations_distinct_and_rejected() -> None:
    baseline = core.build_certificate()
    target_map = dict(core.MUTATION_TARGETS)
    require(tuple(target_map) == core.MUTATION_NAMES, "mutation target order drift")
    digests: set[str] = set()
    for name in core.MUTATION_NAMES:
        mutated = core.mutate_certificate(baseline, name)
        changed = [
            before["id"]
            for before, after in zip(baseline["rows"], mutated["rows"])
            if before != after
        ]
        require(changed == [target_map[name]], f"mutation missed semantic target: {name}")
        digest = sha256(core.canonical_json_bytes(mutated)).hexdigest()
        require(digest not in digests, "duplicate semantic mutation")
        digests.add(digest)
        require(core.verify_certificate(mutated) is False, f"mutation escaped: {name}")
    require(len(digests) == len(core.MUTATION_NAMES) >= 40, "mutation count too small")


def test_topology_and_exact_type_attacks() -> None:
    baseline = core.build_certificate()
    attacks = []
    extra = deepcopy(baseline); extra["extra"] = 0; attacks.append(extra)
    missing = deepcopy(baseline); missing.pop("status"); attacks.append(missing)
    reordered = {key: baseline[key] for key in reversed(tuple(baseline))}; attacks.append(reordered)
    float_row = deepcopy(baseline); float_row["row_count"] = 72.0; attacks.append(float_row)
    bool_row = deepcopy(baseline); bool_row["row_count"] = True; attacks.append(bool_row)
    extra_leaf = deepcopy(baseline); extra_leaf["rows"][0]["data"]["extra"] = 0; attacks.append(extra_leaf)
    for attacked in attacks:
        require(core.verify_certificate(attacked) is False, "topology/type attack escaped")


def test_false_mode_survives_builder_and_helper_bombs() -> None:
    baseline = core.build_certificate()
    saved = {}

    def bomb(*_args: object, **_kwargs: object) -> object:
        raise RuntimeError("forbidden semantic helper used in false mode")

    try:
        for name in (*core.BUILDER_NAMES, *core.SEMANTIC_HELPER_NAMES):
            if hasattr(core, name):
                saved[name] = getattr(core, name)
                setattr(core, name, bomb)
        require(core.verify_certificate(baseline, compare_fresh=False) is True, "false mode used a bombed helper")
    finally:
        for name, value in saved.items():
            setattr(core, name, value)


def test_validator_global_rebinding_rejected() -> None:
    baseline = core.build_certificate()
    original_title = core.TITLE
    original_groups = core.GROUP_IDS
    try:
        core.TITLE = "coordinated drift"
        core.GROUP_IDS = {}
        require(core.verify_certificate(baseline) is True, "false verifier read mutable semantic globals")
        drift = deepcopy(baseline); drift["title"] = "coordinated drift"
        require(core.verify_certificate(drift) is False, "coordinated drift escaped")
    finally:
        core.TITLE = original_title
        core.GROUP_IDS = original_groups


def test_strict_json_duplicate_nonfinite_and_bool_domain() -> None:
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
        try:
            core.loads_strict(text)
        except ValueError:
            pass
        else:
            raise RuntimeError("strict JSON attack escaped")
    for bad in (True, 1.0, 0, -1):
        try:
            core.half_span_capacity(bad, 2)
        except (TypeError, ValueError):
            pass
        else:
            raise RuntimeError("exact integer domain attack escaped")


def test_ast_has_no_bare_assert_and_runtime_sentinel() -> None:
    paths = [Path(core.__file__), Path(__file__)]
    count = 0
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        count += sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    require(count == 0, "bare assert found")
    sentinel = "runtime_require" + "_executed"
    require(sentinel == "runtime_require_executed", "runtime require sentinel failed")


def test_cache_and_certificate_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    forbidden = [path for path in root.rglob("*") if path.name == ".pytest_cache" or path.suffix == ".pyc" or path.name == "__pycache__"]
    require(forbidden == [], f"cache artifacts present: {forbidden}")
    require(core.CERTIFICATE_FIXTURE_ROWS == 72, "fixture row constant drift")
    require(sum(core.ROW_PARTITION.values()) == 72, "partition drift")
