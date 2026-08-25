#!/usr/bin/env python3
"""Independent strict checker for the TPC-245 certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
CERTIFICATE = PROJECT / "results/tpc245_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_SHARP_LONGITUDINAL_TRANSVERSE_COVARIANCE_DISKS"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
SOURCE_PATHS = {
    "TPC219_DERIVATION": REPO / "papers/tpc-219-prime-shell-longitudinal-ledger/DERIVATION_PACKAGE.md",
    "TPC219_PROOF": REPO / "papers/tpc-219-prime-shell-longitudinal-ledger/PROOF_PACKAGE.md",
    "TPC243_PROOF": REPO / "papers/tpc-243-hard-window-near-isometry-bilinear-transfer/PROOF_PACKAGE.md",
    "TPC244_BRIDGE": REPO / "research/tpc-big-road/bridge_b_common_multiplier_sign_localization.md",
    "TPC244_PROOF": REPO / "papers/tpc-244-common-multiplier-sign-localization/PROOF_PACKAGE.md",
}
SOURCE_HASHES = {
    "TPC219_DERIVATION": "b1c3795762f780625edab11fbe8543799eb121a33deb203b269fd6c338b6daca",
    "TPC219_PROOF": "c4954445bfb83bd4bbdb7674b3401c2327a6e4cd69d6d6ed9264f29a8f7e6f60",
    "TPC243_PROOF": "e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf",
    "TPC244_BRIDGE": "28d14c10c1e59a5d87c10508e974d776a641edb0075be4d569e256a0e6015439",
    "TPC244_PROOF": "f24de94c94db9dadf15727fb72cfd1b8c1ae596585ed99a0615ff13534109b49",
}

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class CheckFailure(RuntimeError):
    """Fail-closed independent-check error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def strict_load(raw: bytes) -> dict[str, Any]:
    require(raw.endswith(b"\n") and raw.count(b"\n") == 1, "newline discipline")

    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        output: dict[str, object] = {}
        for key, value in pairs:
            require(type(key) is str and key not in output, "duplicate JSON key")
            output[key] = value
        return output

    def reject_constant(value: str) -> object:
        raise CheckFailure("nonfinite constant: " + value)

    def reject_float(value: str) -> object:
        raise CheckFailure("floating number: " + value)

    value = json.loads(raw.decode("ascii"), object_pairs_hook=pairs_hook,
                       parse_constant=reject_constant, parse_float=reject_float)
    require(type(value) is dict, "top-level object")
    canonical = json.dumps(value, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True).encode("ascii") + b"\n"
    require(raw == canonical, "canonical bytes")
    return value


def exact_keys(value: object, keys: set[str], label: str) -> dict[str, Any]:
    require(type(value) is dict and set(value.keys()) == keys, label + " keys")
    return value


def strict_int(value: object, label: str) -> int:
    require(type(value) is int, label + " exact int")
    return value


def fraction(value: object, label: str) -> Fraction:
    record = exact_keys(value, {"denominator", "numerator"}, label)
    numerator = strict_int(record["numerator"], label + " numerator")
    denominator = strict_int(record["denominator"], label + " denominator")
    require(denominator > 0 and math.gcd(abs(numerator), denominator) == 1,
            label + " reduced")
    return Fraction(numerator, denominator)


def gaussian(value: object, label: str) -> Gaussian:
    record = exact_keys(value, {"im", "re"}, label)
    return (fraction(record["re"], label + " re"),
            fraction(record["im"], label + " im"))


def vector(value: object, label: str) -> Vector:
    require(type(value) is list, label + " list")
    return tuple(gaussian(entry, label + " coordinate") for entry in value)


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] * right[0] - left[1] * right[1],
            left[0] * right[1] + left[1] * right[0])


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def inner(first: Vector, second: Vector) -> Gaussian:
    require(len(first) == len(second), "independent vector dimension")
    total = z()
    for left, right in zip(first, second):
        total = add(total, mul(conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    answer = inner(value, value)
    require(answer[1] == 0 and answer[0] >= 0, "independent norm")
    return answer[0]


def validate_vector_record(record: object, label: str) -> None:
    item = exact_keys(record, {
        "B", "E_B", "E_W", "W", "cauchy_residual", "center",
        "covariance", "transverse_covariance",
    }, label)
    b_vector = vector(item["B"], label + " B")
    w_vector = vector(item["W"], label + " W")
    require(len(b_vector) == len(w_vector) and len(b_vector) >= 1,
            label + " dimensions")
    b = b_vector[0]
    w = w_vector[0]
    bp = b_vector[1:]
    wp = w_vector[1:]
    eb = norm_sq(bp)
    ew = norm_sq(wp)
    center = mul(conj(w), b)
    transverse = inner(wp, bp)
    covariance = inner(w_vector, b_vector)
    require(fraction(item["E_B"], label + " E_B") == eb, label + " E_B value")
    require(fraction(item["E_W"], label + " E_W") == ew, label + " E_W value")
    require(gaussian(item["center"], label + " center") == center, label + " center value")
    require(gaussian(item["transverse_covariance"], label + " transverse") == transverse,
            label + " transverse value")
    require(gaussian(item["covariance"], label + " covariance") == covariance,
            label + " covariance value")
    require(covariance == add(center, transverse), label + " decomposition")
    require(fraction(item["cauchy_residual"], label + " residual") ==
            eb * ew - abs_sq(transverse), label + " residual value")
    require(abs_sq(transverse) <= eb * ew, label + " Cauchy")


def validate_document(stored: dict[str, Any]) -> None:
    top = exact_keys(stored, {"certificate_version", "payload", "payload_sha256", "schema"},
                     "top")
    require(strict_int(top["certificate_version"], "version") == 1, "version value")
    require(top["schema"] == "tpc245-longitudinal-transverse-covariance-disks-v1",
            "schema")
    payload = exact_keys(top["payload"], {
        "baseline", "classification", "fixtures", "scope_firewall", "status", "theorem",
    }, "payload")
    canonical_payload = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                                   ensure_ascii=True).encode("ascii")
    require(top["payload_sha256"] == hashlib.sha256(canonical_payload).hexdigest(),
            "payload digest")
    require(payload["classification"] == FINITE_CLASS and payload["status"] == STATUS,
            "status and classification")

    baseline = exact_keys(payload["baseline"], {"handoff_sha256", "head", "source_hashes"},
                          "baseline")
    require(baseline["head"] == "edc6f6ee80249a6c29f96acdc2a47e088f533474",
            "baseline head")
    require(baseline["handoff_sha256"] ==
            "cdeb66efabdbe32814c8f1a69d04dbba0b06d7b010b4835519d1c7fcc76a33df",
            "handoff hash")
    require(baseline["source_hashes"] == SOURCE_HASHES, "stored source hashes")
    for key, path in SOURCE_PATHS.items():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == SOURCE_HASHES[key],
                "source lock " + key)

    theorem = exact_keys(payload["theorem"], {
        "decomposition", "dimension_at_least_two", "dimension_one", "dimension_zero",
        "minimum_modulus_disk", "orientation", "phase_sector", "zero_feasibility_disk",
    }, "theorem")
    require(theorem["decomposition"] ==
            "<W,B>=conjugate(w)b+<W_perp,B_perp>", "decomposition marker")
    require(theorem["dimension_at_least_two"] ==
            "CLOSED_DISK_CENTER_C_RADIUS_SQRT_EB_EW", "disk marker")
    require(theorem["dimension_one"] ==
            "BOUNDARY_CIRCLE_IF_R_POSITIVE_ELSE_SINGLETON", "circle marker")
    require(theorem["dimension_zero"] ==
            "SINGLETON_IF_ZERO_ENERGIES_ELSE_UNREALIZABLE", "dimension-zero marker")
    require(theorem["minimum_modulus_disk"] == "max(|c|-r,0)",
            "minimum-modulus marker")
    require(theorem["orientation"] ==
            "CONJUGATE_LINEAR_FIRST_SLOT_CENTER_CONJUGATE_W_TIMES_B",
            "orientation marker")
    require(theorem["phase_sector"] ==
            "SHARP_HALF_ANGLE_ARCSIN_R_OVER_ABS_C_WHEN_R_LT_ABS_C",
            "phase-sector marker")
    require(theorem["zero_feasibility_disk"] == "IFF_ABS_C_LE_R",
            "zero-feasibility marker")

    fixtures = exact_keys(payload["fixtures"], {
        "dimension_at_least_two_disk", "dimension_one_circle",
        "low_dimension_singletons", "sharp_phase_tangent",
    }, "fixtures")
    disk = exact_keys(fixtures["dimension_at_least_two_disk"], {
        "classification", "dimension_transverse", "fixed_E_B", "fixed_E_W",
        "radius_squared", "sample_count", "samples",
    }, "disk fixture")
    require(strict_int(disk["dimension_transverse"], "disk dimension") == 2,
            "disk dimension value")
    require(strict_int(disk["sample_count"], "disk count") == 3, "disk count value")
    require(type(disk["samples"]) is list and len(disk["samples"]) == 3, "disk samples")
    for index, sample in enumerate(disk["samples"]):
        require(type(sample) is dict and "label" in sample, "disk sample label")
        copy = dict(sample)
        copy.pop("label")
        validate_vector_record(copy, "disk sample " + str(index))
    transverses = [gaussian(sample["transverse_covariance"], "disk transverse")
                   for sample in disk["samples"]]
    require(transverses == [z(), z(0, 6), z(Fraction(18, 5))], "disk sample values")

    circle = exact_keys(fixtures["dimension_one_circle"], {
        "classification", "dimension_transverse", "interior_zero_feasible",
        "phase_count", "radius_squared", "samples",
    }, "circle fixture")
    require(strict_int(circle["dimension_transverse"], "circle dimension") == 1,
            "circle dimension value")
    require(strict_int(circle["phase_count"], "circle phases") == 4, "circle phase value")
    require(circle["interior_zero_feasible"] is False, "circle interior firewall")
    for index, sample in enumerate(circle["samples"]):
        validate_vector_record(sample, "circle sample " + str(index))
        require(abs_sq(gaussian(sample["covariance"], "circle covariance")) == 36,
                "circle radius value")

    low = exact_keys(fixtures["low_dimension_singletons"], {
        "classification", "dimension_one_radius_zero", "dimension_zero_energy_zero",
        "dimension_zero_positive_energy_realizable",
    }, "low dimension")
    require(low["dimension_zero_positive_energy_realizable"] is False,
            "zero-dimensional realizability firewall")
    validate_vector_record(low["dimension_one_radius_zero"], "dimension-one singleton")
    validate_vector_record(low["dimension_zero_energy_zero"], "dimension-zero singleton")

    tangent = exact_keys(fixtures["sharp_phase_tangent"], {
        "center_modulus", "classification", "radius", "sharp_sine_ratio",
        "tangent_covariance", "tangent_modulus", "vector_record",
    }, "tangent")
    validate_vector_record(tangent["vector_record"], "tangent vector")
    require(fraction(tangent["center_modulus"], "center modulus") == 5, "center modulus value")
    require(fraction(tangent["radius"], "radius") == 3, "radius value")
    require(fraction(tangent["tangent_modulus"], "tangent modulus") == 4,
            "tangent modulus value")
    require(fraction(tangent["sharp_sine_ratio"], "sine ratio") == Fraction(3, 5),
            "sine ratio value")

    firewall = exact_keys(payload["scope_firewall"], {
        "ARITHMETIC_ADVANCE", "ARITHMETIC_L2", "CANONICAL_BLOCK_DIRECTION",
        "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE", "FIXED_ATOM_CREDIT", "FULL_GATE_B",
        "LITERAL_V59_TWO_LANE_ATTACHMENT", "STRICT_1_OVER_400", "TPC219_RELATION",
        "TWIN_PRIME_RESULT",
    }, "firewall")
    require(firewall["ARITHMETIC_ADVANCE"] == "NO" and
            firewall["ARITHMETIC_L2"] == "NONE", "arithmetic firewall")
    require(firewall["CANONICAL_BLOCK_DIRECTION"] == "OPEN" and
            firewall["LITERAL_V59_TWO_LANE_ATTACHMENT"] == "OPEN", "attachment firewall")
    require(type(firewall["FIXED_ATOM_CREDIT"]) is int and
            firewall["FIXED_ATOM_CREDIT"] == 0, "fixed atom exact type")
    require(firewall["FULL_GATE_B"] == "OPEN" and
            firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL",
            "Gate-B endpoint firewall")
    require(firewall["TPC219_RELATION"] ==
            "PROJECTION_LINEAGE_ONLY_NOT_LITERAL_OBJECT_IDENTITY",
            "TPC219 type firewall")
    require(firewall["TWIN_PRIME_RESULT"] == "NONE",
            "twin-prime firewall")
    require(firewall["FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE"] is False,
            "finite evidence firewall")


def reject_mutations(stored: dict[str, Any]) -> int:
    def rebind(candidate: dict[str, Any]) -> dict[str, Any]:
        payload_bytes = json.dumps(
            candidate["payload"], sort_keys=True, separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
        candidate["payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
        return candidate

    count = 0
    mutations = []
    item = deepcopy(stored)
    item["certificate_version"] = True
    mutations.append(item)
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["ARITHMETIC_ADVANCE"] = "YES"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["theorem"]["dimension_one"] = "CLOSED_DISK"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["theorem"]["orientation"] = "CONJUGATE_B_TIMES_W"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["fixtures"]["low_dimension_singletons"][
        "dimension_zero_positive_energy_realizable"] = True
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["theorem"]["phase_sector"] = "NONE"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["theorem"]["minimum_modulus_disk"] = "0"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["theorem"]["zero_feasibility_disk"] = "ALWAYS"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["FULL_GATE_B"] = "CLOSED"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["STRICT_1_OVER_400"] = "PAID"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["TPC219_RELATION"] = "LITERAL_OBJECT_IDENTITY"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["TWIN_PRIME_RESULT"] = "PROVED"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["CANONICAL_BLOCK_DIRECTION"] = "PROVED"
    mutations.append(rebind(item))
    item = deepcopy(stored)
    item["payload"]["scope_firewall"]["LITERAL_V59_TWO_LANE_ATTACHMENT"] = "PROVED"
    mutations.append(rebind(item))
    for mutation in mutations:
        try:
            validate_document(mutation)
        except CheckFailure:
            count += 1
    require(count == len(mutations), "hostile mutations rejected")
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC245_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        stored = strict_load(CERTIFICATE.read_bytes())
        validate_document(stored)
        rejected = reject_mutations(stored)
        print("TPC245_INDEPENDENT_CHECK=PASS")
        print("source_locks=" + str(len(SOURCE_PATHS)))
        print("disk_samples=3")
        print("circle_phases=4")
        print("hostile_mutations_rejected=" + str(rejected))
        print("status=" + STATUS)
        print("canonical_block_direction=OPEN")
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            UnicodeError, json.JSONDecodeError) as error:
        raise SystemExit("TPC245_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
