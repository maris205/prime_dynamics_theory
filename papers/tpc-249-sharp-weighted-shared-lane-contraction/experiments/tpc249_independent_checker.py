#!/usr/bin/env python3
"""Independent exact replay for TPC-249; imports no producer code."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc249_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARP_WEIGHTED_SHARED_LANE_CONTRACTION"


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("ascii")


def strict(text: str) -> Any:
    def hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            if key in output:
                raise Failure("duplicate key")
            output[key] = value
        return output
    return json.loads(text, object_pairs_hook=hook,
                      parse_constant=lambda token: (_ for _ in ()).throw(
                          Failure("nonfinite token: " + token)))


def q(value: Any) -> Fraction:
    need(type(value) is str and value.count("/") == 1, "rational")
    result = Fraction(*(int(part) for part in value.split("/")))
    need(f"{result.numerator}/{result.denominator}" == value, "canonical rational")
    return result


def replay(document: Any) -> None:
    need(type(document) is dict and set(document) == {
        "certificate_version", "claim_status", "payload", "payload_sha256"
    }, "schema")
    need(type(document["certificate_version"]) is int and
         document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "status")
    body = document["payload"]
    need(hashlib.sha256(canonical(body)).hexdigest() == document["payload_sha256"],
         "digest")
    need(body["source"] == {
        "affine_domain": "MODELING_CHOICE",
        "contraction": "g_c=sum_b lambda_cb v_cb",
        "probe": "v_cb=A_cb beta_b",
        "same_weights_no_conjugation": True,
    }, "source")
    groups = body["fixtures"]["groups"]
    need(type(groups) is list and len(groups) == 3, "groups")
    radii = []
    tagged = Fraction(0)
    for record in groups:
        probes = [[q(value) for value in row] for row in record["probes"]]
        weights = [q(value) for value in record["weights"]]
        rho = q(record["rho"])
        g = [sum((weight * probe[j] for weight, probe in zip(weights, probes)),
                 Fraction(0)) for j in range(len(probes[0]))]
        need([q(value) for value in record["contracted_probe"]] == g, "contracted probe")
        g2 = sum((value * value for value in g), Fraction(0))
        need(q(record["contracted_norm_squared"]) == g2, "Gram norm")
        tagged += q(record["tagged_radius"])
        radii.append((record["name"], rho, g2))
    need(radii == [("orthogonal", Fraction(2), Fraction(1)),
                   ("cancellation", Fraction(3), Fraction(0)),
                   ("aligned", Fraction(1), Fraction(4))], "fixture radii")
    fixture = body["fixtures"]
    need(q(fixture["independent_exact_radius"]) == 4 and
         q(fixture["independent_tagged_radius"]) == tagged == Fraction(54, 5),
         "aggregate radii")
    need(q(fixture["explicit_target"]) ==
         sum((q(value) for value in fixture["explicit_local_targets"]), Fraction(0)),
         "target allocation")
    need(q(fixture["affine_scalar_center"]) == Fraction(1, 5) and
         fixture["affine_zero_feasible"] is True and
         q(fixture["positive_margin_minimum"]) == 1, "affine calculus")
    need(q(fixture["global_radius_squared"]) == 20, "global radius")
    orientation = fixture["complex_orientation"]
    need(orientation["weighted_scalar"] ==
         orientation["inner_product_with_contracted_probe"], "complex orientation")
    firewall = body["scope_firewall"]
    need(firewall["ACTUAL_GRAM_ASYMPTOTIC"] == "OPEN" and
         firewall["ARITHMETIC_L2"] == "NONE" and
         type(firewall["FIXED_ATOM_CREDIT"]) is int and
         firewall["FIXED_ATOM_CREDIT"] == 0, "firewall")


def rejected(mutator: Callable[[dict[str, Any]], None], original: dict[str, Any]) -> bool:
    candidate = deepcopy(original)
    mutator(candidate)
    try:
        replay(candidate)
    except (Failure, KeyError, TypeError, ValueError, ZeroDivisionError):
        return True
    return False


def check() -> None:
    raw = CERTIFICATE.read_bytes()
    document = strict(raw.decode("ascii"))
    need(raw == canonical(document) + b"\n", "canonical bytes")
    replay(document)
    attacks: list[Callable[[dict[str, Any]], None]] = [
        lambda d: d.__setitem__("certificate_version", True),
        lambda d: d.__setitem__("claim_status", "PROVED_ARITHMETIC_L2"),
        lambda d: d["payload"]["source"].__setitem__("same_weights_no_conjugation", False),
        lambda d: d["payload"]["fixtures"].__setitem__("independent_exact_radius", "54/5"),
        lambda d: d["payload"]["fixtures"]["groups"][1].__setitem__("contracted_norm_squared", "1/1"),
        lambda d: d["payload"]["fixtures"].__setitem__("global_radius_squared", "16/1"),
        lambda d: d["payload"]["scope_firewall"].__setitem__("ARITHMETIC_L2", "PASS"),
        lambda d: d.__setitem__("payload_sha256", "0" * 64),
    ]
    need(all(rejected(attack, document) for attack in attacks), "mutation accepted")
    rebound = deepcopy(document)
    rebound["payload"]["fixtures"]["independent_exact_radius"] = "54/5"
    rebound["payload_sha256"] = hashlib.sha256(canonical(rebound["payload"])).hexdigest()
    need(rejected(lambda d: d.update(rebound), document), "digest rebound")
    print("TPC249_INDEPENDENT_CHECK=PASS")
    print("mutations_rejected=9/9")
    print("weighted_contraction=EXACT")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC249_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        check()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, ZeroDivisionError) as error:
        raise SystemExit("TPC249_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
