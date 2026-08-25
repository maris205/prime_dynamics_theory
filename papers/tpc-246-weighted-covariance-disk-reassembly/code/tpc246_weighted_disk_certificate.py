#!/usr/bin/env python3
"""Exact certificate producer/checker for TPC-246 weighted disks."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc246_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY"


class CheckFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def q(value: int, denominator: int = 1) -> Fraction:
    return Fraction(value, denominator)


def qs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def qp(value: str) -> Fraction:
    require(type(value) is str and value.count("/") == 1, "rational encoding")
    numerator, denominator = value.split("/")
    result = Fraction(int(numerator), int(denominator))
    require(qs(result) == value, "noncanonical rational")
    return result


Gaussian = tuple[Fraction, Fraction]


def g(re: Fraction | int, im: Fraction | int = 0) -> Gaussian:
    return Fraction(re), Fraction(im)


def gadd(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gneg(value: Gaussian) -> Gaussian:
    return -value[0], -value[1]


def gmul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def gconj(value: Gaussian) -> Gaussian:
    return value[0], -value[1]


def gscale(scale: Fraction, value: Gaussian) -> Gaussian:
    return scale * value[0], scale * value[1]


def gnorm2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def gj(value: Gaussian) -> dict[str, str]:
    return {"re": qs(value[0]), "im": qs(value[1])}


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_json_loads(text: str) -> Any:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise CheckFailure("duplicate JSON key: " + key)
            result[key] = value
        return result
    return json.loads(text, object_pairs_hook=pairs_hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          CheckFailure("nonfinite JSON token: " + token)))


def weighted_center(weights: list[Gaussian], centers: list[Gaussian]) -> Gaussian:
    total = g(0)
    for weight, center in zip(weights, centers):
        total = gadd(total, gmul(weight, center))
    return total


def weighted_value(weights: list[Gaussian], centers: list[Gaussian],
                   deviations: list[Gaussian]) -> Gaussian:
    total = g(0)
    for weight, center, deviation in zip(weights, centers, deviations):
        total = gadd(total, gmul(weight, gadd(center, deviation)))
    return total


def reverse_deviations(weights: list[Gaussian], moduli: list[Fraction],
                       radii: list[Fraction], radius: Fraction,
                       target_deviation: Gaussian) -> list[Gaussian]:
    require(radius > 0, "reverse construction radius")
    output: list[Gaussian] = []
    for weight, modulus, local_radius in zip(weights, moduli, radii):
        if modulus == 0:
            require(weight == g(0), "zero modulus weight")
            output.append(g(0))
        else:
            output.append(gscale(local_radius / (modulus * radius),
                                 gmul(gconj(weight), target_deviation)))
    return output


def exact_fixture() -> dict[str, Any]:
    centers = [g(2, 1), g(-1, 2), g(1, -1)]
    radii = [q(1), q(1, 2), q(1, 4)]
    weights = [g(q(3, 5), q(4, 5)), g(q(-5, 13), q(12, 13)), g(2)]
    moduli = [q(1), q(1), q(2)]
    for weight, modulus in zip(weights, moduli):
        require(gnorm2(weight) == modulus * modulus, "declared weight modulus")
    center = weighted_center(weights, centers)
    radius = sum((modulus * local_radius
                  for modulus, local_radius in zip(moduli, radii)), q(0))
    require(center == g(q(61, 65), q(-97, 65)), "fixture center")
    require(radius == 2, "fixture radius")
    require(gnorm2(center) <= radius * radius, "fixture cancellation condition")

    zero_deviations = reverse_deviations(weights, moduli, radii, radius,
                                           gneg(center))
    require(weighted_value(weights, centers, zero_deviations) == g(0),
            "explicit zero realization")
    for deviation, local_radius in zip(zero_deviations, radii):
        require(gnorm2(deviation) <= local_radius * local_radius,
                "zero realization leaves local disk")

    boundary_delta = g(radius)
    boundary_deviations = reverse_deviations(weights, moduli, radii, radius,
                                               boundary_delta)
    boundary_target = gadd(center, boundary_delta)
    require(weighted_value(weights, centers, boundary_deviations) == boundary_target,
            "boundary realization")

    return {
        "centers": [gj(value) for value in centers],
        "radii": [qs(value) for value in radii],
        "weights": [gj(value) for value in weights],
        "weight_moduli": [qs(value) for value in moduli],
        "aggregate_center": gj(center),
        "aggregate_radius": qs(radius),
        "zero_feasible": True,
        "zero_local_deviations": [gj(value) for value in zero_deviations],
        "zero_aggregate": gj(weighted_value(weights, centers, zero_deviations)),
        "boundary_target": gj(boundary_target),
        "boundary_local_deviations": [gj(value) for value in boundary_deviations],
    }


def robust_fixture() -> dict[str, Any]:
    weights = [q(2), q(1)]
    centers = [g(3), g(1)]
    radii = [q(1, 4), q(1, 4)]
    aggregate_center = sum((weight * center[0]
                            for weight, center in zip(weights, centers)), q(0))
    aggregate_radius = sum((weight * radius
                            for weight, radius in zip(weights, radii)), q(0))
    epsilon = q(1, 20)
    norm_w = q(2)
    norm_b = q(5, 2)
    leakage = epsilon * norm_w * norm_b
    inflated_radius = aggregate_radius + leakage
    margin = aggregate_center - inflated_radius
    require(aggregate_center == 7, "robust center")
    require(aggregate_radius == q(3, 4), "robust radius")
    require(leakage == q(1, 4), "robust leakage")
    require(inflated_radius == 1 and margin == 6, "robust margin")
    return {
        "common_multiplier_weights": [qs(value) for value in weights],
        "local_centers": [gj(value) for value in centers],
        "local_radii": [qs(value) for value in radii],
        "aggregate_center": gj(g(aggregate_center)),
        "aggregate_radius": qs(aggregate_radius),
        "epsilon": qs(epsilon),
        "norm_w": qs(norm_w),
        "norm_b": qs(norm_b),
        "window_leakage": qs(leakage),
        "inflated_radius": qs(inflated_radius),
        "uniform_lower_margin": qs(margin),
        "robust_nonvanishing": True,
    }


def build_payload() -> dict[str, Any]:
    return {
        "theorem": {
            "coupled_family_containment": "PROVED_WITHOUT_PRODUCT_REALIZABILITY",
            "weighted_disk_identity": "EXACT",
            "aggregate_center": "SUM_LAMBDA_H_C_H",
            "aggregate_radius": "SUM_ABS_LAMBDA_H_R_H",
            "reverse_realization": "EXPLICIT_FOR_EVERY_POINT",
            "zero_criterion": "ABS_CENTER_LE_RADIUS",
            "minimum_modulus": "MAX_ABS_CENTER_MINUS_RADIUS_0",
        },
        "complex_weight_fixture": exact_fixture(),
        "hard_window_fixture": robust_fixture(),
        "exclusions": {
            "arbitrary_complex_weight_is_common_multiplier": False,
            "positive_radius_circle_is_disk": False,
            "independent_product_is_automatic_for_source": False,
            "inflated_physical_disk_is_exact_image": False,
        },
        "scope_firewall": {
            "ARITHMETIC_ADVANCE": "NO",
            "ARITHMETIC_L2": "NONE",
            "CANONICAL_BLOCK_DIRECTIONS": "OPEN",
            "FIXED_ATOM_CREDIT": 0,
            "FULL_GATE_B": "OPEN",
            "INDEPENDENT_SOURCE_REALIZABILITY": "OPEN",
            "LITERAL_V59_TWO_LANE_ATTACHMENT": "OPEN",
            "PAYABLE_ARITHMETIC_MARGIN": "OPEN",
            "STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TWIN_PRIME_RESULT": "NONE",
        },
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    digest = hashlib.sha256(canonical_json(payload)).hexdigest()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": digest,
    }


def same_typed(candidate: Any, expected: Any) -> bool:
    if type(candidate) is not type(expected):
        return False
    if type(expected) is dict:
        return candidate.keys() == expected.keys() and all(
            same_typed(candidate[key], expected[key]) for key in expected
        )
    if type(expected) is list:
        return len(candidate) == len(expected) and all(
            same_typed(left, right) for left, right in zip(candidate, expected)
        )
    return candidate == expected


def validate(document: Any) -> None:
    expected = build_document()
    require(same_typed(document, expected), "certificate does not match recomputation")
    require(type(document["certificate_version"]) is int, "certificate version type")
    payload = document["payload"]
    require(hashlib.sha256(canonical_json(payload)).hexdigest()
            == document["payload_sha256"], "payload digest")
    fixture = payload["complex_weight_fixture"]
    require(fixture["zero_feasible"] is True, "zero feasibility exact bool")
    require(qp(fixture["aggregate_radius"]) == 2, "aggregate radius parse")
    hard = payload["hard_window_fixture"]
    require(qp(hard["uniform_lower_margin"]) == 6, "robust margin parse")
    require(hard["robust_nonvanishing"] is True, "robust verdict exact bool")
    firewall = payload["scope_firewall"]
    require(firewall["ARITHMETIC_ADVANCE"] == "NO", "arithmetic firewall")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed atom type")


def write_certificate() -> None:
    document = build_document()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_bytes(canonical_json(document) + b"\n")


def check_certificate() -> None:
    require(CERTIFICATE.is_file(), "certificate missing")
    raw = CERTIFICATE.read_bytes()
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1,
            "certificate line format")
    document = strict_json_loads(raw.decode("ascii"))
    require(raw == canonical_json(document) + b"\n", "canonical JSON bytes")
    validate(document)
    print("TPC246_CERTIFICATE=PASS")
    print("claim=" + STATUS)
    print("complex_weights=3")
    print("aggregate_center=61/65-97/65i")
    print("aggregate_radius=2/1")
    print("explicit_zero_realization=PASS")
    print("hard_window_uniform_margin=6/1")
    print("arithmetic_L2=NONE")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("TPC246_CERTIFICATE=FAIL: choose exactly one mode")
    try:
        if args.write:
            write_certificate()
            check_certificate()
        else:
            check_certificate()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit("TPC246_CERTIFICATE=FAIL: " + str(error))


if __name__ == "__main__":
    main()
