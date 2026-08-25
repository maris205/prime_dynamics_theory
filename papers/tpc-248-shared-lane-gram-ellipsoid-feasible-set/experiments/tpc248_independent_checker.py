#!/usr/bin/env python3
"""Independent exact replay for TPC-248; imports no producer code."""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


PROJECT = Path(__file__).resolve().parents[1]
CERTIFICATE = PROJECT / "results/tpc248_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET"


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
    need(type(value) is str and value.count("/") == 1, "rational type")
    left, right = value.split("/")
    result = Fraction(int(left), int(right))
    need(f"{result.numerator}/{result.denominator}" == value, "rational canonical")
    return result


def matrix(value: Any) -> list[list[Fraction]]:
    need(type(value) is list and bool(value), "matrix type")
    output = [[q(entry) for entry in row] for row in value]
    need(all(type(row) is list and len(row) == len(output[0]) for row in value),
         "matrix rectangular")
    return output


def mm(a: list[list[Fraction]], b: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Fraction(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a: list[list[Fraction]]) -> list[list[Fraction]]:
    return [list(column) for column in zip(*a)]


def verify_pair(record: dict[str, Any]) -> None:
    gram = matrix(record["gram"])
    dagger = matrix(record["gram_dagger"])
    need(mm(mm(gram, dagger), gram) == gram, "first MP identity")
    need(mm(mm(dagger, gram), dagger) == dagger, "second MP identity")
    need(mm(gram, dagger) == tr(mm(gram, dagger)), "third MP identity")
    need(mm(dagger, gram) == tr(mm(dagger, gram)), "fourth MP identity")


def replay(document: Any) -> None:
    need(type(document) is dict and set(document) == {
        "certificate_version", "claim_status", "payload", "payload_sha256"
    }, "document schema")
    need(type(document["certificate_version"]) is int and
         document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "status")
    body = document["payload"]
    need(hashlib.sha256(canonical(body)).hexdigest() == document["payload_sha256"],
         "payload hash")
    source = body["source_object"]
    need(source == {
        "cartesian_promotion_from_tagged_copies": False,
        "fixed_c_shared_lane": True,
        "output_lane": "w_c=P_cw",
        "probe": "v_cb=A_cb beta_b",
    }, "source object")
    theorem = body["theorem"]
    need(theorem["ball_image"] == "RANGE_G_AND_Y_STAR_G_DAGGER_Y_LE_RHO_SQUARED",
         "ball theorem")
    need(theorem["sphere_with_kernel_slack"] == "SOLID_ELLIPSOID" and
         theorem["sphere_without_kernel_slack"] == "BOUNDARY_SHELL",
         "sphere theorem")
    fixtures = body["real_fixtures"]
    for name in ("rank_one_repeated_probe", "full_rank_orthogonal_probe",
                 "tilted_full_rank_probe"):
        verify_pair(fixtures[name])
    rank_one = fixtures["rank_one_repeated_probe"]
    need(rank_one["range_equation"] == "y_1=y_2" and
         rank_one["boundary_energy"] == "1/1" and
         rank_one["polydisk_promotion"] == "REFUTED_SCOPED",
         "rank-one obstruction")
    slack = fixtures["sphere_slack"]
    no_slack = fixtures["sphere_no_slack"]
    need(q(slack["minimum_energy"]) == Fraction(9, 25) and
         q(slack["slack_norm"]) == Fraction(4, 5) and
         slack["kernel_dimension_positive"] is True, "slack fixture")
    need(type(no_slack["kernel_dimension"]) is int and
         no_slack["kernel_dimension"] == 0 and
         no_slack["sphere_membership"] is False, "no-slack fixture")
    global_budget = fixtures["global_budget"]
    need(global_budget["local_product_membership"] is True and
         q(global_budget["global_energy"]) == 2 and
         global_budget["global_membership"] is False, "global budget")
    complex_fixture = body["complex_fixture"]
    need(complex_fixture["z_equals_conjugate_y"] is True and
         q(complex_fixture["quadratic_energy"]) == 5, "complex orientation")
    y = complex_fixture["y_vstar_w"]
    z = complex_fixture["z_physical"]
    need(y == [{"im": "1/1", "re": "2/1"},
               {"im": "-2/1", "re": "1/1"}], "complex y")
    need(z == [{"im": "-1/1", "re": "2/1"},
               {"im": "2/1", "re": "1/1"}], "complex z")
    firewall = body["scope_firewall"]
    need(firewall["ARITHMETIC_ADVANCE"] == "NO" and
         firewall["ARITHMETIC_L2"] == "NONE" and
         type(firewall["FIXED_ATOM_CREDIT"]) is int and
         firewall["FIXED_ATOM_CREDIT"] == 0 and
         firewall["TWIN_PRIME_RESULT"] == "NONE", "firewall")


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
        lambda d: d["payload"]["source_object"].__setitem__("fixed_c_shared_lane", False),
        lambda d: d["payload"]["real_fixtures"]["rank_one_repeated_probe"].__setitem__("range_equation", "ALL"),
        lambda d: d["payload"]["real_fixtures"]["sphere_no_slack"].__setitem__("sphere_membership", True),
        lambda d: d["payload"]["real_fixtures"]["global_budget"].__setitem__("global_membership", True),
        lambda d: d["payload"]["complex_fixture"].__setitem__("z_equals_conjugate_y", False),
        lambda d: d["payload"]["scope_firewall"].__setitem__("ARITHMETIC_L2", "PASS"),
        lambda d: d.__setitem__("payload_sha256", "0" * 64),
    ]
    need(all(rejected(attack, document) for attack in attacks), "mutation accepted")
    rebound = deepcopy(document)
    rebound["payload"]["source_object"]["fixed_c_shared_lane"] = False
    rebound["payload_sha256"] = hashlib.sha256(canonical(rebound["payload"])).hexdigest()
    need(rejected(lambda d: d.update(rebound), document), "digest-rebound mutation")
    print("TPC248_INDEPENDENT_CHECK=PASS")
    print("mutations_rejected=10/10")
    print("shared_lane_joint_set=GRAM_ELLIPSOID")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC248_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        check()
    except (Failure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, ZeroDivisionError) as error:
        raise SystemExit("TPC248_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
