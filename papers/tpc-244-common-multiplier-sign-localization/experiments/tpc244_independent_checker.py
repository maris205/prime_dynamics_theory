#!/usr/bin/env python3
"""Independent strict checker for the TPC-244 certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]
CERTIFICATE = PROJECT / "results" / "tpc244_certificate.json"
STATUS = "PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION"
FINITE_CLASS = "NUMERICAL_FINITE_ILLUSTRATION_ONLY"
SOURCE_PATHS = {
    "TPC214_BRIDGE": REPO / "research/tpc-big-road/bridge_b_mobius_frequency_clusters.md",
    "TPC214_PROOF": REPO / "papers/tpc-214-mobius-frequency-clusters/PROOF_PACKAGE.md",
    "TPC228_DERIVATION": REPO / "papers/tpc-228-source-native-polarized-collision-compiler/DERIVATION_PACKAGE.md",
    "TPC228_PROOF": REPO / "papers/tpc-228-source-native-polarized-collision-compiler/PROOF_PACKAGE.md",
    "TPC236_SOURCE": REPO / "papers/tpc-236-physical-multiwrap-collision-envelope/notes/source_lock.md",
    "TPC237_SOURCE": REPO / "papers/tpc-237-collision-compressed-finite-window-reassembly/notes/source_lock.md",
    "TPC237_PROOF": REPO / "papers/tpc-237-collision-compressed-finite-window-reassembly/PROOF_PACKAGE.md",
    "TPC242_PROOF": REPO / "papers/tpc-242-phase-fourier-collision-separation/PROOF_PACKAGE.md",
    "TPC243_PROOF": REPO / "papers/tpc-243-hard-window-near-isometry-bilinear-transfer/PROOF_PACKAGE.md",
}
SOURCE_HASHES = {
    "TPC214_BRIDGE": "8779910e87c77df2b2c1efbd7caac9b03560b71089280b72c9d1e30a34874f69",
    "TPC214_PROOF": "eec983abf4d69fbb14d965872b11513d822df97f682f602c2e0ab35f1eac7c84",
    "TPC228_DERIVATION": "453d7eb8fb39f6af8c24e6e592d7ee5c732cd0e3e9adabeb6b0223c7f6ecdf0f",
    "TPC228_PROOF": "1b6f91f100b89222dc08a070623e6162539b8e88b17b807b2d4ccfb6338da61d",
    "TPC236_SOURCE": "039d9e6e8684eed34ede58b9491c3ddfc57e2097bd36cb930348d4cebc226272",
    "TPC237_SOURCE": "35b338da0a5c8e84c4189022f717e029f45dc1f644291f9748487b8e2bf81d9a",
    "TPC237_PROOF": "9464a698148f57c7b0ed57ad1f45760585d68b6b8d56969de2347833b6aee425",
    "TPC242_PROOF": "b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba",
    "TPC243_PROOF": "e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf",
}

Gaussian = tuple[Fraction, Fraction]
Vector = tuple[Gaussian, ...]


class CheckFailure(RuntimeError):
    """Fail-closed independent-check error."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


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

    value = json.loads(
        raw.decode("ascii"),
        object_pairs_hook=pairs_hook,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, "top-level object")
    require(raw == canonical(value) + b"\n", "canonical bytes")
    return value


def exact_keys(value: object, keys: set[str], label: str) -> dict[str, Any]:
    require(type(value) is dict and set(value.keys()) == keys, label + " keys")
    return value


def strict_int(value: object, label: str) -> int:
    require(type(value) is int, label + " int type")
    return value


def fraction(value: object, label: str) -> Fraction:
    record = exact_keys(value, {"numerator", "denominator"}, label)
    numerator = strict_int(record["numerator"], label + " numerator")
    denominator = strict_int(record["denominator"], label + " denominator")
    require(denominator > 0 and math.gcd(abs(numerator), denominator) == 1,
            label + " reduced fraction")
    return Fraction(numerator, denominator)


def gaussian(value: object, label: str) -> Gaussian:
    record = exact_keys(value, {"re", "im"}, label)
    return (fraction(record["re"], label + " re"), fraction(record["im"], label + " im"))


def z(real: int | Fraction = 0, imag: int | Fraction = 0) -> Gaussian:
    return (Fraction(real), Fraction(imag))


def add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def mul(left: Gaussian, right: Gaussian) -> Gaussian:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def scale(value: Gaussian, scalar: int | Fraction) -> Gaussian:
    factor = Fraction(scalar)
    return (factor * value[0], factor * value[1])


def abs_sq(value: Gaussian) -> Fraction:
    return value[0] * value[0] + value[1] * value[1]


def inner(first: Vector, second: Vector) -> Gaussian:
    require(len(first) == len(second), "independent vector dimension")
    total = z()
    for left, right in zip(first, second):
        total = add(total, mul(conj(left), right))
    return total


def norm_sq(value: Vector) -> Fraction:
    result = inner(value, value)
    require(result[1] == 0 and result[0] >= 0, "independent norm")
    return result[0]


def vector_add(left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "independent vector add")
    return tuple(add(a, b) for a, b in zip(left, right))


def vector_scale(value: Vector, scalar: int | Fraction) -> Vector:
    return tuple(scale(entry, scalar) for entry in value)


def phase(exponent: int) -> Gaussian:
    return (z(1), z(0, 1), z(-1), z(0, -1))[exponent % 4]


def signs(size: int) -> list[tuple[int, ...]]:
    return list(itertools.product((-1, 1), repeat=size))


def synthesize(coefficients: Vector, frequencies: tuple[int, ...], start: int, length: int) -> Vector:
    output: list[Gaussian] = []
    for n_value in range(start, start + length):
        total = z()
        for coefficient, frequency in zip(coefficients, frequencies):
            total = add(total, mul(coefficient, phase(n_value * frequency)))
        output.append(total)
    return tuple(output)


def validate_direct(record: object) -> None:
    item = exact_keys(record, {
        "block_count", "blocks", "common_multipliers", "covariance",
        "b_norm_sq", "w_norm_sq", "pattern_count",
        "all_common_sign_patterns_invariant", "classification",
    }, "direct fixture")
    require(item["blocks"] == ["h5", "h7", "h35"], "direct block labels")
    require(item["common_multipliers"] == [2, -3, 5], "direct multipliers")
    require(strict_int(item["block_count"], "direct block count") == 3, "direct block count value")
    require(strict_int(item["pattern_count"], "direct pattern count") == 8, "direct pattern count value")
    require(item["all_common_sign_patterns_invariant"] is True, "direct invariant marker")
    require(item["classification"] == FINITE_CLASS, "direct classification")

    multipliers = (2, -3, 5)
    b_blocks: tuple[Vector, ...] = (
        (z(1, 1), z(2)),
        (z(-1), z(1, 1)),
        (z(Fraction(1, 2), -1), z(2, 1)),
    )
    w_blocks: tuple[Vector, ...] = (
        (z(2, -1), z(-1, 2)),
        (z(3), z(0, 1)),
        (z(-2), z(1, -1)),
    )
    covariance = z()
    bn = Fraction(0)
    wn = Fraction(0)
    for scalar, b_value, w_value in zip(multipliers, b_blocks, w_blocks):
        covariance = add(covariance, scale(inner(w_value, b_value), scalar * scalar))
        bn += scalar * scalar * norm_sq(b_value)
        wn += scalar * scalar * norm_sq(w_value)
    require(gaussian(item["covariance"], "direct covariance") == covariance, "direct covariance value")
    require(fraction(item["b_norm_sq"], "direct b norm") == bn, "direct b norm value")
    require(fraction(item["w_norm_sq"], "direct w norm") == wn, "direct w norm value")


def validate_overlap(record: object) -> None:
    item = exact_keys(record, {
        "blocks", "common_multipliers", "diagonal_D", "symmetrized_edges",
        "q_by_sign_pattern", "pattern_count", "cut_identity_all_patterns",
        "sign_sensitive", "classification",
    }, "overlap fixture")
    require(item["blocks"] == ["h5", "h7", "h35"], "overlap blocks")
    require(item["common_multipliers"] == [2, -3, 5], "overlap multipliers")
    require(item["classification"] == FINITE_CLASS, "overlap classification")
    require(item["cut_identity_all_patterns"] is True and item["sign_sensitive"] is True,
            "overlap markers")
    require(strict_int(item["pattern_count"], "overlap pattern count") == 8,
            "overlap pattern count value")
    require(gaussian(item["diagonal_D"], "overlap D") == z(-12), "overlap D value")
    edges = exact_keys(item["symmetrized_edges"], {"h5--h7", "h5--h35", "h7--h35"},
                      "overlap edges")
    expected_edges = {"h5--h7": z(-12), "h5--h35": z(20), "h7--h35": z(-15)}
    for key, expected in expected_edges.items():
        require(gaussian(edges[key], "overlap edge " + key) == expected,
                "overlap edge value " + key)

    values = exact_keys(item["q_by_sign_pattern"], {
        "---", "--+", "-+-", "-++", "+--", "+-+", "++-", "+++",
    }, "overlap q patterns")
    for pattern in signs(3):
        key = "".join("+" if sign == 1 else "-" for sign in pattern)
        expected = z(-12)
        for (h, k), edge_key in (((0, 1), "h5--h7"), ((0, 2), "h5--h35"), ((1, 2), "h7--h35")):
            expected = add(expected, scale(expected_edges[edge_key], pattern[h] * pattern[k]))
        require(gaussian(values[key], "overlap q " + key) == expected,
                "overlap q value " + key)


def validate_hard_window(record: object) -> None:
    item = exact_keys(record, {
        "frequency_quarters", "block_index", "interval_M", "interval_N",
        "row_bound_R", "epsilon", "coefficient_covariance", "b_norm_sq",
        "w_norm_sq", "individual_bound_sq", "pairwise_bound_sq",
        "maximum_error_abs_sq", "maximum_pair_difference_abs_sq", "patterns",
        "pattern_count", "individual_transfer_all_patterns",
        "pairwise_factor_two_all_ordered_pairs", "ordered_pair_count", "classification",
    }, "hard-window fixture")
    require(item["frequency_quarters"] == [0, 1, 2, 3], "hard frequencies")
    require(item["block_index"] == [0, 0, 1, 2], "hard block index")
    require(strict_int(item["interval_M"], "hard M") == -3, "hard M value")
    require(strict_int(item["interval_N"], "hard N") == 17, "hard N value")
    require(fraction(item["row_bound_R"], "hard row bound") == 6, "hard row bound value")
    require(fraction(item["epsilon"], "hard epsilon") == Fraction(6, 17), "hard epsilon value")
    require(item["individual_transfer_all_patterns"] is True, "hard individual marker")
    require(item["pairwise_factor_two_all_ordered_pairs"] is True, "hard pair marker")
    require(strict_int(item["pattern_count"], "hard pattern count") == 8, "hard pattern count value")
    require(strict_int(item["ordered_pair_count"], "hard pair count") == 64, "hard pair count value")
    require(item["classification"] == FINITE_CLASS, "hard classification")

    frequencies = (0, 1, 2, 3)
    block_index = (0, 0, 1, 2)
    multipliers = (2, -3, 5)
    b_local: Vector = (z(1, 1), z(2, -1), z(-1, 2), z(Fraction(1, 2), 1))
    w_local: Vector = (z(2, -1), z(-1, 1), z(1), z(-2, 1))
    epsilon = Fraction(6, 17)
    patterns = exact_keys(item["patterns"], {
        "---", "--+", "-+-", "-++", "+--", "+-+", "++-", "+++",
    }, "hard patterns")
    physical_values: list[Gaussian] = []
    covariance0: Gaussian | None = None
    bn0: Fraction | None = None
    wn0: Fraction | None = None
    max_error = Fraction(0)
    for pattern in signs(3):
        key = "".join("+" if sign == 1 else "-" for sign in pattern)
        b_coeff = tuple(scale(value, pattern[block] * multipliers[block])
                        for value, block in zip(b_local, block_index))
        w_coeff = tuple(scale(value, pattern[block] * multipliers[block])
                        for value, block in zip(w_local, block_index))
        covariance = inner(w_coeff, b_coeff)
        bn = norm_sq(b_coeff)
        wn = norm_sq(w_coeff)
        if covariance0 is None:
            covariance0, bn0, wn0 = covariance, bn, wn
        require(covariance == covariance0 and bn == bn0 and wn == wn0,
                "hard coefficient invariance")
        physical = scale(inner(synthesize(w_coeff, frequencies, -3, 17),
                               synthesize(b_coeff, frequencies, -3, 17)), Fraction(1, 17))
        error_sq = abs_sq(add(physical, scale(covariance, -1)))
        entry = exact_keys(patterns[key], {"physical_covariance", "error_abs_sq"},
                           "hard pattern " + key)
        require(gaussian(entry["physical_covariance"], "hard physical " + key) == physical,
                "hard physical value " + key)
        require(fraction(entry["error_abs_sq"], "hard error " + key) == error_sq,
                "hard error value " + key)
        max_error = max(max_error, error_sq)
        physical_values.append(physical)

    require(covariance0 is not None and bn0 is not None and wn0 is not None,
            "hard nonempty")
    individual_bound = epsilon * epsilon * bn0 * wn0
    pair_bound = 4 * individual_bound
    max_pair = max(abs_sq(add(left, scale(right, -1)))
                   for left in physical_values for right in physical_values)
    require(gaussian(item["coefficient_covariance"], "hard covariance") == covariance0,
            "hard covariance value")
    require(fraction(item["b_norm_sq"], "hard b norm") == bn0, "hard b norm value")
    require(fraction(item["w_norm_sq"], "hard w norm") == wn0, "hard w norm value")
    require(fraction(item["individual_bound_sq"], "hard individual bound") == individual_bound,
            "hard individual bound value")
    require(fraction(item["pairwise_bound_sq"], "hard pair bound") == pair_bound,
            "hard pair bound value")
    require(fraction(item["maximum_error_abs_sq"], "hard max error") == max_error,
            "hard max error value")
    require(fraction(item["maximum_pair_difference_abs_sq"], "hard max pair") == max_pair,
            "hard max pair value")
    require(max_error <= individual_bound and max_pair <= pair_bound, "hard exact inequalities")


def validate_document(document: object) -> None:
    doc = exact_keys(document, {
        "certificate_version", "task", "status", "source_lock", "object_lock",
        "theorem", "fixtures", "scope_firewall", "route_evaluation",
        "mutation_firewalls", "payload_sha256",
    }, "document")
    require(strict_int(doc["certificate_version"], "certificate version") == 1,
            "certificate version value")
    require(doc["task"] == "TPC-244" and doc["status"] == STATUS, "task/status")
    digest = doc["payload_sha256"]
    require(type(digest) is str and len(digest) == 64, "payload digest type")
    payload = dict(doc)
    del payload["payload_sha256"]
    require(hashlib.sha256(canonical(payload)).hexdigest() == digest, "payload digest value")

    source = exact_keys(doc["source_lock"], {"baseline_head", "tpc_handoff_sha256", "files"},
                        "source lock")
    require(source["baseline_head"] == "ba1aa9ddb12f42ae390a6d709f40225b2562c009",
            "baseline head")
    require(source["tpc_handoff_sha256"] ==
            "46704f3f8b61a469799deb6a568451ff8e1298677b57cd4359851dce9d6d74f0",
            "handoff source hash")
    require(source["files"] == SOURCE_HASHES, "source-lock registry")
    for key, path in SOURCE_PATHS.items():
        require(path.is_file(), "missing source " + key)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == SOURCE_HASHES[key], "source hash mismatch " + key)

    object_lock = exact_keys(doc["object_lock"], {
        "inner_product", "coefficient_space", "common_multiplier",
        "literal_cluster", "physical_covariance_orientation",
    }, "object lock")
    require(object_lock == {
        "inner_product": "CONJUGATE_LINEAR_FIRST_LINEAR_SECOND",
        "coefficient_space": "FINITE_ORTHOGONAL_DIRECT_SUM_OF_BLOCKS",
        "common_multiplier": "SAME_C_H_ON_BOTH_LANES",
        "literal_cluster": "C_h=sum_(d_in_D_x,h|d)mu(d)log(d)/d",
        "physical_covariance_orientation": "Q_I=N^(-1)<T_W,T_B>=F_1",
    }, "object-lock values")

    theorem = exact_keys(doc["theorem"], {
        "classification", "direct_sum_covariance", "common_unit_phase_invariance",
        "internal_mobius_signs", "overlap_polynomial", "sign_cut_identity",
        "all_sign_invariance", "hard_window_pairwise_transfer",
    }, "theorem")
    require(theorem["classification"] == "PROVED_STRUCTURAL_L1_ONLY", "theorem class")
    require(theorem["direct_sum_covariance"] == "<W,B>=sum_h|C_h|^2<w_h,b_h>",
            "direct theorem")
    require(theorem["internal_mobius_signs"] == "PRESERVED_INSIDE_ABS_C_H",
            "internal Möbius firewall")
    require(theorem["sign_cut_identity"] == "Q(s)-Q(1)=-2sum_(cut_edges)S_hk",
            "cut orientation")
    require(theorem["all_sign_invariance"] ==
            "IFF_EVERY_SYMMETRIZED_EDGE_S_HK_IS_ZERO", "iff theorem")
    require(theorem["hard_window_pairwise_transfer"] == "<=2epsilon||W||_2||B||_2",
            "factor-two theorem")

    fixtures = exact_keys(doc["fixtures"], {"direct_sum", "overlap", "hard_window"},
                          "fixtures")
    validate_direct(fixtures["direct_sum"])
    validate_overlap(fixtures["overlap"])
    validate_hard_window(fixtures["hard_window"])

    firewall = exact_keys(doc["scope_firewall"], {
        "LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT", "PHYSICAL_SPECIALIZATION",
        "COEFFICIENT_NORM_PAYMENT", "SIGNED_C_H_CANCELLATION", "ARITHMETIC_L2",
        "ARITHMETIC_ADVANCE", "FIXED_ATOM_CREDIT", "STRICT_1_OVER_400",
        "FULL_GATE_B", "TWIN_PRIME_RESULT", "FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE",
    }, "firewall")
    require(firewall["LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT"] == "OPEN",
            "literal attachment firewall")
    require(firewall["PHYSICAL_SPECIALIZATION"] ==
            "CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT",
            "conditional specialization")
    require(firewall["SIGNED_C_H_CANCELLATION"] == "NONE", "signed C_h firewall")
    require(firewall["ARITHMETIC_L2"] == "NONE" and firewall["ARITHMETIC_ADVANCE"] == "NO",
            "arithmetic firewall")
    require(strict_int(firewall["FIXED_ATOM_CREDIT"], "fixed atom") == 0,
            "fixed atom value")
    require(firewall["STRICT_1_OVER_400"] == "UNPAID_GLOBAL"
            and firewall["FULL_GATE_B"] == "OPEN", "Gate B firewall")
    require(firewall["FINITE_CERTIFICATE_IS_THEOREM_EVIDENCE"] is False,
            "finite evidence firewall")

    route = exact_keys(doc["route_evaluation"], {
        "strongest_positive_result", "strongest_obstruction", "open_theorem",
        "reusable_structure", "ROUND2_CLUE",
    }, "route evaluation")
    require(route["strongest_obstruction"] ==
            "OUTER_C_H_SIGN_CANNOT_CONTROL_SAME_BLOCK_MAIN_COVARIANCE",
            "route obstruction")
    mutations = exact_keys(doc["mutation_firewalls"], {"rejected", "rejected_count"},
                           "mutations")
    require(type(mutations["rejected"]) is list
            and strict_int(mutations["rejected_count"], "mutation count") == 12,
            "mutation registry")


def rebound(document: dict[str, Any]) -> None:
    cases: list[tuple[str, dict[str, Any]]] = []
    arithmetic = deepcopy(document)
    arithmetic["scope_firewall"]["ARITHMETIC_ADVANCE"] = "YES"
    cases.append(("arithmetic promotion", arithmetic))
    attachment = deepcopy(document)
    attachment["scope_firewall"]["LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT"] = "PROVED"
    cases.append(("attachment promotion", attachment))
    orientation = deepcopy(document)
    orientation["object_lock"]["physical_covariance_orientation"] = "Q_I=N^(-1)<T_B,T_W>"
    cases.append(("orientation reversal", orientation))
    factor = deepcopy(document)
    factor["theorem"]["hard_window_pairwise_transfer"] = "<=epsilon||W||_2||B||_2"
    cases.append(("factor two removal", factor))
    mobius = deepcopy(document)
    mobius["theorem"]["internal_mobius_signs"] = "ERASED"
    cases.append(("internal Möbius erasure", mobius))
    endpoint = deepcopy(document)
    endpoint["scope_firewall"]["STRICT_1_OVER_400"] = "PAID"
    cases.append(("endpoint promotion", endpoint))
    bool_type = deepcopy(document)
    bool_type["certificate_version"] = True
    cases.append(("bool/int confusion", bool_type))
    extra = deepcopy(document)
    extra["theorem"]["extra"] = "UNREGISTERED"
    cases.append(("extra nested key", extra))

    for label, candidate in cases:
        payload = dict(candidate)
        del payload["payload_sha256"]
        candidate["payload_sha256"] = hashlib.sha256(canonical(payload)).hexdigest()
        try:
            validate_document(candidate)
        except CheckFailure:
            continue
        raise CheckFailure("hostile rebound accepted: " + label)


def run() -> None:
    require(CERTIFICATE.is_file(), "missing certificate")
    document = strict_load(CERTIFICATE.read_bytes())
    validate_document(document)
    rebound(document)
    print("TPC244_INDEPENDENT_CHECK=PASS")
    print("source_locks=" + str(len(SOURCE_PATHS)))
    print("direct_sign_patterns=8")
    print("overlap_sign_patterns=8")
    print("hard_window_ordered_pairs=64")
    print("hostile_rebound_firewalls=8")
    print("status=" + STATUS)
    print("literal_v59_two_lane_attachment=OPEN")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC244_INDEPENDENT_CHECK=FAIL: use --check")
    try:
        run()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, UnicodeError) as error:
        raise SystemExit("TPC244_INDEPENDENT_CHECK=FAIL: " + str(error))


if __name__ == "__main__":
    main()
