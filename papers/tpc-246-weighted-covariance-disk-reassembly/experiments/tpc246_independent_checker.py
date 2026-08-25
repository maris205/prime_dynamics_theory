#!/usr/bin/env python3
"""Independent fail-closed checker for the TPC-246 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc246_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_WEIGHTED_COVARIANCE_DISK_REASSEMBLY"


class CheckFailure(RuntimeError):
    """Fail-closed validation error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict_load(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise CheckFailure("duplicate key: " + key)
            out[key] = value
        return out
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          CheckFailure("nonfinite token: " + token)))


def rat(text: Any) -> Fraction:
    require(type(text) is str and text.count("/") == 1, "rational type")
    left, right = text.split("/")
    value = Fraction(int(left), int(right))
    require(f"{value.numerator}/{value.denominator}" == text,
            "noncanonical rational")
    return value


Gaussian = tuple[Fraction, Fraction]


def gauss(value: Any) -> Gaussian:
    require(type(value) is dict and list(value.keys()) == ["im", "re"],
            "Gaussian schema/order")
    return rat(value["re"]), rat(value["im"])


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def norm2(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(type(value) is dict and set(value.keys()) == keys, label + " keys")


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
    exact_keys(document, {"certificate_version", "claim_status", "payload",
                          "payload_sha256"}, "document")
    require(type(document["certificate_version"]) is int and
            document["certificate_version"] == 1, "version")
    require(document["claim_status"] == STATUS, "claim status")
    payload = document["payload"]
    require(type(payload) is dict, "payload type")
    require(hashlib.sha256(canonical(payload)).hexdigest()
            == document["payload_sha256"], "payload digest")
    exact_keys(payload, {"theorem", "complex_weight_fixture",
                         "hard_window_fixture", "exclusions",
                         "scope_firewall"}, "payload")

    theorem = payload["theorem"]
    require(same_typed(theorem, {
        "aggregate_center": "SUM_LAMBDA_H_C_H",
        "aggregate_radius": "SUM_ABS_LAMBDA_H_R_H",
        "coupled_family_containment": "PROVED_WITHOUT_PRODUCT_REALIZABILITY",
        "minimum_modulus": "MAX_ABS_CENTER_MINUS_RADIUS_0",
        "reverse_realization": "EXPLICIT_FOR_EVERY_POINT",
        "weighted_disk_identity": "EXACT",
        "zero_criterion": "ABS_CENTER_LE_RADIUS",
    }), "theorem declaration")

    fixture = payload["complex_weight_fixture"]
    exact_keys(fixture, {"centers", "radii", "weights", "weight_moduli",
                         "aggregate_center", "aggregate_radius", "zero_feasible",
                         "zero_local_deviations", "zero_aggregate",
                         "boundary_target", "boundary_local_deviations"},
               "complex fixture")
    centers = [gauss(value) for value in fixture["centers"]]
    radii = [rat(value) for value in fixture["radii"]]
    weights = [gauss(value) for value in fixture["weights"]]
    moduli = [rat(value) for value in fixture["weight_moduli"]]
    require(centers == [(Fraction(2), Fraction(1)),
                        (Fraction(-1), Fraction(2)),
                        (Fraction(1), Fraction(-1))], "centers")
    require(radii == [Fraction(1), Fraction(1, 2), Fraction(1, 4)], "radii")
    require(weights == [(Fraction(3, 5), Fraction(4, 5)),
                        (Fraction(-5, 13), Fraction(12, 13)),
                        (Fraction(2), Fraction(0))], "weights")
    require(moduli == [Fraction(1), Fraction(1), Fraction(2)], "moduli")
    for weight, modulus in zip(weights, moduli):
        require(norm2(weight) == modulus * modulus, "weight modulus")
    center = (Fraction(0), Fraction(0))
    for weight, local_center in zip(weights, centers):
        center = add(center, mul(weight, local_center))
    radius = sum((modulus * local_radius
                  for modulus, local_radius in zip(moduli, radii)), Fraction(0))
    require(center == (Fraction(61, 65), Fraction(-97, 65)), "computed center")
    require(radius == Fraction(2), "computed radius")
    require(gauss(fixture["aggregate_center"]) == center, "stored center")
    require(rat(fixture["aggregate_radius"]) == radius, "stored radius")
    require(fixture["zero_feasible"] is True and norm2(center) <= radius * radius,
            "zero criterion")

    zero_deviations = [gauss(value) for value in fixture["zero_local_deviations"]]
    boundary_deviations = [gauss(value)
                           for value in fixture["boundary_local_deviations"]]
    require(len(zero_deviations) == 3 and len(boundary_deviations) == 3,
            "deviation lengths")
    zero_total = (Fraction(0), Fraction(0))
    boundary_total = (Fraction(0), Fraction(0))
    for weight, local_center, local_radius, zero_dev, boundary_dev in zip(
            weights, centers, radii, zero_deviations, boundary_deviations):
        require(norm2(zero_dev) <= local_radius * local_radius,
                "zero deviation outside disk")
        require(norm2(boundary_dev) <= local_radius * local_radius,
                "boundary deviation outside disk")
        zero_total = add(zero_total, mul(weight, add(local_center, zero_dev)))
        boundary_total = add(boundary_total,
                             mul(weight, add(local_center, boundary_dev)))
    require(zero_total == (Fraction(0), Fraction(0)), "zero realization")
    require(gauss(fixture["zero_aggregate"]) == zero_total, "stored zero")
    expected_boundary = add(center, (radius, Fraction(0)))
    require(boundary_total == expected_boundary, "boundary realization")
    require(gauss(fixture["boundary_target"]) == expected_boundary,
            "stored boundary")

    hard = payload["hard_window_fixture"]
    exact_keys(hard, {"common_multiplier_weights", "local_centers", "local_radii",
                      "aggregate_center", "aggregate_radius", "epsilon", "norm_w",
                      "norm_b", "window_leakage", "inflated_radius",
                      "uniform_lower_margin", "robust_nonvanishing"}, "hard fixture")
    common_weights = [rat(value) for value in hard["common_multiplier_weights"]]
    local_centers = [gauss(value) for value in hard["local_centers"]]
    local_radii = [rat(value) for value in hard["local_radii"]]
    require(common_weights == [Fraction(2), Fraction(1)], "common weights")
    require(local_centers == [(Fraction(3), Fraction(0)),
                              (Fraction(1), Fraction(0))], "hard centers")
    require(local_radii == [Fraction(1, 4), Fraction(1, 4)], "hard radii")
    hard_center = sum((weight * value[0]
                       for weight, value in zip(common_weights, local_centers)),
                      Fraction(0))
    hard_radius = sum((weight * value
                       for weight, value in zip(common_weights, local_radii)),
                      Fraction(0))
    epsilon = rat(hard["epsilon"])
    norm_w = rat(hard["norm_w"])
    norm_b = rat(hard["norm_b"])
    leakage = epsilon * norm_w * norm_b
    inflated = hard_radius + leakage
    margin = hard_center - inflated
    require(gauss(hard["aggregate_center"]) == (hard_center, Fraction(0)),
            "hard center")
    require(rat(hard["aggregate_radius"]) == hard_radius == Fraction(3, 4),
            "hard radius")
    require(rat(hard["window_leakage"]) == leakage == Fraction(1, 4),
            "leakage")
    require(rat(hard["inflated_radius"]) == inflated == Fraction(1),
            "inflated radius")
    require(rat(hard["uniform_lower_margin"]) == margin == Fraction(6),
            "uniform margin")
    require(hard["robust_nonvanishing"] is True and margin > 0,
            "robust verdict")

    require(same_typed(payload["exclusions"], {
        "arbitrary_complex_weight_is_common_multiplier": False,
        "independent_product_is_automatic_for_source": False,
        "inflated_physical_disk_is_exact_image": False,
        "positive_radius_circle_is_disk": False,
    }), "exclusions")
    require(same_typed(payload["scope_firewall"], {
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
    }), "scope firewall")


def rebound(candidate: dict[str, Any]) -> None:
    candidate["payload_sha256"] = hashlib.sha256(
        canonical(candidate["payload"])).hexdigest()


def mutation_count(document: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("claim promotion", lambda d: d.__setitem__("claim_status", "ARITHMETIC")),
        ("radius formula", lambda d: d["payload"]["theorem"].__setitem__(
            "aggregate_radius", "SUM_LAMBDA_H_R_H")),
        ("stored center", lambda d: d["payload"]["complex_weight_fixture"].__setitem__(
            "aggregate_center", {"im": "0/1", "re": "0/1"})),
        ("stored radius", lambda d: d["payload"]["complex_weight_fixture"].__setitem__(
            "aggregate_radius", "3/1")),
        ("zero verdict", lambda d: d["payload"]["complex_weight_fixture"].__setitem__(
            "zero_feasible", False)),
        ("zero deviation", lambda d: d["payload"]["complex_weight_fixture"]
            ["zero_local_deviations"][0].__setitem__("re", "99/1")),
        ("boundary target", lambda d: d["payload"]["complex_weight_fixture"]
            ["boundary_target"].__setitem__("re", "0/1")),
        ("hard center", lambda d: d["payload"]["hard_window_fixture"]
            ["aggregate_center"].__setitem__("re", "8/1")),
        ("window leakage", lambda d: d["payload"]["hard_window_fixture"].__setitem__(
            "window_leakage", "1/5")),
        ("margin", lambda d: d["payload"]["hard_window_fixture"].__setitem__(
            "uniform_lower_margin", "7/1")),
        ("robust verdict", lambda d: d["payload"]["hard_window_fixture"].__setitem__(
            "robust_nonvanishing", False)),
        ("circle promotion", lambda d: d["payload"]["exclusions"].__setitem__(
            "positive_radius_circle_is_disk", True)),
        ("complex common multiplier", lambda d: d["payload"]["exclusions"].__setitem__(
            "arbitrary_complex_weight_is_common_multiplier", True)),
        ("source independence", lambda d: d["payload"]["exclusions"].__setitem__(
            "independent_product_is_automatic_for_source", True)),
        ("arithmetic promotion", lambda d: d["payload"]["scope_firewall"].__setitem__(
            "ARITHMETIC_ADVANCE", "YES")),
        ("bool-int", lambda d: d["payload"]["scope_firewall"].__setitem__(
            "FIXED_ATOM_CREDIT", False)),
    ]
    rejected = 0
    for label, mutate in mutations:
        candidate = deepcopy(document)
        mutate(candidate)
        rebound(candidate)
        try:
            validate(candidate)
        except CheckFailure:
            rejected += 1
        else:
            raise CheckFailure("digest-rebound mutation accepted: " + label)
    return rejected


def run() -> None:
    raw = CERTIFICATE.read_bytes()
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "line format")
    document = strict_load(raw.decode("ascii"))
    require(raw == canonical(document) + b"\n", "canonical bytes")
    validate(document)
    rejected = mutation_count(document)
    require(rejected == 16, "mutation census")
    print("TPC246_INDEPENDENT_CHECK=PASS")
    print("direct_algebra_recomputation=PASS")
    print("explicit_zero_reconstruction=PASS")
    print("hard_window_margin_recomputation=PASS")
    print("digest_rebound_mutations_rejected=16/16")
    print("arithmetic_promotion=REJECTED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC246_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit("TPC246_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
