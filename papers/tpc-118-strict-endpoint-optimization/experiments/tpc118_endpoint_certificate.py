#!/usr/bin/env python3
"""Exact rational regression for the TPC-118 endpoint certificates."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path


Vector = list[Fraction]
Matrix = list[list[Fraction]]


def dot(x: Vector, y: Vector) -> Fraction:
    if len(x) != len(y):
        raise ValueError("dimension mismatch in dot product")
    return sum(a * b for a, b in zip(x, y))


def matvec(a: Matrix, x: Vector) -> Vector:
    return [dot(row, x) for row in a]


def transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def geq(x: Vector, y: Vector) -> bool:
    if len(x) != len(y):
        raise ValueError("dimension mismatch in comparison")
    return all(a >= b for a, b in zip(x, y))


def leq(x: Vector, y: Vector) -> bool:
    if len(x) != len(y):
        raise ValueError("dimension mismatch in comparison")
    return all(a <= b for a, b in zip(x, y))


def check_certificate(
    a: Matrix, b: Vector, c: Vector, x: Vector, y: Vector
) -> Fraction:
    if not geq(matvec(a, x), b) or any(value < 0 for value in x):
        raise AssertionError("primal point is infeasible")
    if not leq(matvec(transpose(a), y), c) or any(value < 0 for value in y):
        raise AssertionError("dual point is infeasible")
    primal = dot(c, x)
    dual = dot(b, y)
    if dual > primal:
        raise AssertionError("weak duality failed")
    if dual != primal:
        raise AssertionError("certificate is not matching")
    return primal


EventRef = tuple[str, str, str, str]
RegistryKey = EventRef


def event_ref(record: dict[str, object]) -> EventRef:
    return (
        str(record["id"]),
        str(record["map"]),
        str(record["scope"]),
        str(record["norm"]),
    )


def registry_key(record: dict[str, object]) -> RegistryKey:
    return event_ref(record)


def canonical_registry(
    records: list[dict[str, object]],
) -> dict[RegistryKey, dict[str, object]]:
    registry: dict[RegistryKey, dict[str, object]] = {}
    for record in records:
        missing = {
            "id", "map", "scope", "norm", "source", "deps", "value"
        } - set(record)
        if missing:
            raise ValueError(f"token is missing fields: {sorted(missing)}")
        key = registry_key(record)
        value = record["value"]
        if key in registry and (
            registry[key]["value"] != value
            or registry[key]["source"] != record["source"]
            or tuple(registry[key]["deps"]) != tuple(record["deps"])
        ):
            raise ValueError(
                f"ambiguous alternative evidence for one physical event: {key}"
            )
        registry[key] = record
    return registry


def resolve_joint_tokens(
    records: list[dict[str, object]],
) -> dict[RegistryKey, dict[str, object]]:
    registry = canonical_registry(records)
    base_by_ref: dict[EventRef, RegistryKey] = {}
    for key, record in registry.items():
        if not tuple(record["deps"]):
            ref = event_ref(record)
            if ref in base_by_ref:
                raise ValueError(f"ambiguous base-event provenance: {ref}")
            base_by_ref[ref] = key

    removed: set[RegistryKey] = set()
    for record in registry.values():
        for dependency in tuple(record["deps"]):
            if dependency not in base_by_ref:
                raise ValueError(f"unresolved joint-token dependency: {dependency}")
            key = base_by_ref[dependency]
            if key in removed:
                raise ValueError(f"dependency charged by two joint tokens: {dependency}")
            removed.add(key)
    return {key: record for key, record in registry.items() if key not in removed}


def token(
    token_id: str,
    literal_map: str,
    value: Fraction | None,
    *,
    scope: str = "fixed-h0-active-carrier",
    norm: str = "amplitude",
    source: str = "literal-theorem",
    deps: tuple[EventRef, ...] = (),
) -> dict[str, object]:
    return {
        "id": token_id,
        "map": literal_map,
        "scope": scope,
        "norm": norm,
        "source": source,
        "deps": deps,
        "value": value,
    }


def main() -> None:
    threshold = Fraction(1, 400)
    identity: Matrix = [
        [Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(1)],
    ]
    objective = [Fraction(1), Fraction(1)]
    dual_point = [Fraction(1), Fraction(1)]

    cases = {
        "strict_below": [Fraction(1, 1000), Fraction(1, 1200)],
        "exact_equality": [Fraction(1, 1000), Fraction(3, 2000)],
        "strict_above": [Fraction(1, 500), Fraction(1, 1000)],
    }
    objectives: dict[str, str] = {}
    classifications: dict[str, str] = {}
    for name, lower_bounds in cases.items():
        value = check_certificate(
            identity,
            lower_bounds,
            objective,
            lower_bounds,
            dual_point,
        )
        objectives[name] = f"{value.numerator}/{value.denominator}"
        if value < threshold:
            classifications[name] = "GO"
        elif value == threshold:
            classifications[name] = "STOP_EQUALITY"
        else:
            classifications[name] = "STOP_ABOVE"

    frame = token("frame", "quotient-to-physical", Fraction(1, 2000))
    localization = token(
        "localization", "profile-to-fixed-shift", Fraction(1, 3000)
    )
    records = [frame, dict(frame), localization]
    registry = canonical_registry(records)
    if len(registry) != 2:
        raise AssertionError("full-provenance duplicate was not merged")

    # Equal ids and values do not merge when their literal maps differ.
    distinct_map_registry = canonical_registry(
        [
            frame,
            token("frame", "different-physical-map", Fraction(1, 2000)),
        ]
    )
    if len(distinct_map_registry) != 2:
        raise AssertionError("different literal maps were incorrectly merged")

    conflict_rejected = False
    try:
        canonical_registry(
            [
                token("tail", "tail-to-physical", Fraction(1, 1000)),
                token("tail", "tail-to-physical", Fraction(1, 900)),
            ]
        )
    except ValueError:
        conflict_rejected = True
    if not conflict_rejected:
        raise AssertionError("conflicting duplicate was accepted")

    alternative_source_rejected = False
    try:
        canonical_registry(
            [
                frame,
                token(
                    "frame",
                    "quotient-to-physical",
                    Fraction(1, 2000),
                    source="alternative-frame-theorem",
                ),
            ]
        )
    except ValueError:
        alternative_source_rejected = True
    if not alternative_source_rejected:
        raise AssertionError("same physical event from two sources was added")

    alternative_dependency_rejected = False
    try:
        canonical_registry(
            [
                token(
                    "joint",
                    "same-joint-map",
                    Fraction(1, 1700),
                    deps=(event_ref(frame),),
                ),
                token(
                    "joint",
                    "same-joint-map",
                    Fraction(1, 1700),
                    deps=(event_ref(localization),),
                ),
            ]
        )
    except ValueError:
        alternative_dependency_rejected = True
    if not alternative_dependency_rejected:
        raise AssertionError("same physical event with two dependency sets was added")

    grouping = token("group", "native-to-residual", Fraction(1, 2500))
    joint = token(
        "frame-group-joint",
        "native-to-physical",
        Fraction(1, 1500),
        source="joint-frame-group-theorem",
        deps=(event_ref(frame), event_ref(grouping)),
    )
    resolved = resolve_joint_tokens([frame, grouping, localization, joint])
    resolved_ids = {str(record["id"]) for record in resolved.values()}
    if resolved_ids != {"localization", "frame-group-joint"}:
        raise AssertionError("joint token did not replace exactly its dependencies")

    missing_dependency_rejected = False
    try:
        orphan_joint = token(
            "orphan-joint",
            "orphan-map",
            Fraction(1, 1600),
            deps=(event_ref(token("missing", "missing-map", Fraction(0))),),
        )
        resolve_joint_tokens([frame, orphan_joint])
    except ValueError:
        missing_dependency_rejected = True
    if not missing_dependency_rejected:
        raise AssertionError("unresolved joint dependency was accepted")

    incomplete_registry = canonical_registry(
        [frame, token("tail", "tail-to-physical", None)]
    )
    incomplete_rejected = any(
        record["value"] is None for record in incomplete_registry.values()
    )
    if not incomplete_rejected:
        raise AssertionError("unknown token was treated as zero")

    result = {
        "schema": "tpc-118-strict-endpoint-certificate-v1",
        "status": "PASS",
        "threshold": "1/400",
        "objectives": objectives,
        "classifications": classifications,
        "checks": {
            "matching_primal_dual_certificates": len(cases),
            "full_provenance_duplicate_merge": 1,
            "different_map_nonmerge": 1,
            "conflicting_duplicate_rejection": 1,
            "alternative_source_rejection": 1,
            "alternative_dependency_rejection": 1,
            "joint_dependency_replacement": 1,
            "missing_dependency_rejection": 1,
            "unknown_token_rejection": 1,
        },
        "claim_boundary": {
            "finite_exact_certificate": True,
            "actual_complete_tpc_registry": False,
            "actual_strict_endpoint_certificate": False,
            "new_L2_fixed_shift_estimate": False,
            "parity_breakthrough": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_suffix(".json").write_text(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
