#!/usr/bin/env python3
"""Fail-closed schema and algebra stress tests for TPC-332.

The expensive numerical replay is intentionally kept in the independent
checker.  This companion attacks the serialized certificate: it rejects
missing source-L2 fields, changed growth geometry, altered censuses, broken
provenance, exact-anchor mutations, and any attempt to upgrade the finite
result into an arithmetic theorem.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-332-growing-control-average-ensemble"
CERTIFICATE = PROJECT / "results/tpc332_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-331-control-average-centered-response-decomposition/code/"
    "tpc331_control_average_centered_response_decomposition.py")
PARENT_CERTIFICATE = ROOT / (
    "papers/tpc-331-control-average-centered-response-decomposition/results/"
    "tpc331_certificate.json")
V59_CODE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/code/"
    "tpc267_literal_residual_radius_certificate.py")
V59_CERTIFICATE = ROOT / (
    "papers/tpc-267-literal-v59-residual-radius-census/results/"
    "tpc267_certificate.json")

SCHEMA = "TPC332_GROWING_CONTROL_AVERAGE_ENSEMBLE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
HEIGHT = 66
TAIL_CUTOFF = 50000
RATIO_GUARD = 5.0e-8
CONTROL_NAMES = ("identity", "affine_3_11", "affine_5_17",
                 "affine_7_29", "reversal")
PLACEMENT_RULE = (
    "five_predeclared_bijections: identity, affine_3_11, affine_5_17, "
    "affine_7_29, reversal")
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
COMPONENTS = ("average", "coherent", "centered")
LABELS = ("NEGATIVE_OFF_DIAGONAL", "POSITIVE_OFF_DIAGONAL", "UNRESOLVED")
PARENT_CODE_SHA256 = (
    "c96095bd951d80e9147eeba99241761ba31a78b04a6b01bfcd120397f7e0eebc")
PARENT_CERT_SHA256 = (
    "eacd8b5e508956b362cbc0bb3c8da2b245a2155f91d8f48e794121f3e7a4997c")
V59_CODE_SHA256 = (
    "d7e36a243b9acc4cbc65297e1d497053b350892cdb7c7c5b2d8f7ac7f917f750")
V59_CERT_SHA256 = (
    "adf6aef58ec6701db0f000545ead11c8a7642b1f0ab7ec4b8d42822d32e90ce9")

EXPECTED_CENSUS = {
    "all_plus": {
        "average": {"NEGATIVE_OFF_DIAGONAL": 0,
                    "POSITIVE_OFF_DIAGONAL": 48, "UNRESOLVED": 0},
        "coherent": {"NEGATIVE_OFF_DIAGONAL": 1,
                      "POSITIVE_OFF_DIAGONAL": 47, "UNRESOLVED": 0},
        "centered": {"NEGATIVE_OFF_DIAGONAL": 0,
                     "POSITIVE_OFF_DIAGONAL": 48, "UNRESOLVED": 0},
    },
    "alternating_index": {
        "average": {"NEGATIVE_OFF_DIAGONAL": 31,
                    "POSITIVE_OFF_DIAGONAL": 17, "UNRESOLVED": 0},
        "coherent": {"NEGATIVE_OFF_DIAGONAL": 38,
                      "POSITIVE_OFF_DIAGONAL": 10, "UNRESOLVED": 0},
        "centered": {"NEGATIVE_OFF_DIAGONAL": 29,
                     "POSITIVE_OFF_DIAGONAL": 19, "UNRESOLVED": 0},
    },
    "mod4_character": {
        "average": {"NEGATIVE_OFF_DIAGONAL": 48,
                    "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "coherent": {"NEGATIVE_OFF_DIAGONAL": 44,
                      "POSITIVE_OFF_DIAGONAL": 4, "UNRESOLVED": 0},
        "centered": {"NEGATIVE_OFF_DIAGONAL": 47,
                     "POSITIVE_OFF_DIAGONAL": 1, "UNRESOLVED": 0},
    },
    "half_split": {
        "average": {"NEGATIVE_OFF_DIAGONAL": 48,
                    "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
        "coherent": {"NEGATIVE_OFF_DIAGONAL": 39,
                      "POSITIVE_OFF_DIAGONAL": 9, "UNRESOLVED": 0},
        "centered": {"NEGATIVE_OFF_DIAGONAL": 48,
                     "POSITIVE_OFF_DIAGONAL": 0, "UNRESOLVED": 0},
    },
}


class Failure(RuntimeError):
    pass


class DuplicateKey(ValueError):
    pass


def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(key)
        result[key] = value
    return result


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def read_certificate() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    document = json.loads(raw, object_pairs_hook=no_duplicates)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    return payload


def finite_gram_identity() -> None:
    """Exercise exact Gram algebra and make two mutations observable."""
    values = list(range(44001, 44013))
    matrix = [[Fraction(0) for _ in values] for _ in values]
    for ui, u in enumerate(values):
        for ti, t in enumerate(values):
            if ui == ti:
                continue
            matrix[ui][ti] = Fraction(int((u - t) % 5 == 0), 1)
    vector = [Fraction((i % 5) - 2, 3) for i in range(len(values))]
    output = [sum((matrix[u][t] * vector[t]
                   for t in range(len(values))), Fraction(0))
              for u in range(len(values))]
    energy = sum((x * x for x in output), Fraction(0))
    diagonal = sum((vector[t] * vector[t] *
                    sum((matrix[u][t] * matrix[u][t]
                         for u in range(len(values))), Fraction(0))
                    for t in range(len(values))), Fraction(0))
    off = sum((vector[t] * vector[v] *
               sum((matrix[u][t] * matrix[u][v]
                    for u in range(len(values))), Fraction(0))
              for t in range(len(values))
              for v in range(len(values)) if t != v), Fraction(0))
    need(energy == diagonal + off and energy > 0 and diagonal > 0,
         "exact Gram identity")
    changed = list(vector)
    changed[3] += Fraction(1, 7)
    changed_output = [sum((matrix[u][t] * changed[t]
                           for t in range(len(values))), Fraction(0))
                      for u in range(len(values))]
    need(sum((x * x for x in changed_output), Fraction(0)) != energy,
         "source mutation is invisible")
    flipped = [[-entry for entry in row] for row in matrix]
    flipped_output = [sum((flipped[u][t] * vector[t]
                           for t in range(len(values))), Fraction(0))
                      for u in range(len(values))]
    need(sum((x * x for x in flipped_output), Fraction(0)) == energy,
         "Gram sign invariance sanity")


def validate_payload(payload: dict[str, Any]) -> None:
    protocol = payload.get("protocol")
    controls = [
        {"name": name, "multiplier": multiplier, "offset": offset,
         "rule": rule}
        for name, multiplier, offset, rule in (
            ("identity", 1, 0, "pi_0(i)=i"),
            ("affine_3_11", 3, 11,
             "pi_3,11(i)=(3*i+11) mod source_count"),
            ("affine_5_17", 5, 17,
             "pi_5,17(i)=(5*i+17) mod source_count"),
            ("affine_7_29", 7, 29,
             "pi_7,29(i)=(7*i+29) mod source_count"),
            ("reversal", -1, -1,
             "pi_rev(i)=source_count-1-i"))]
    need(isinstance(protocol, dict) and
         protocol.get("origins") == list(ORIGINS) and
         protocol.get("scales") == list(SCALES) and
         protocol.get("source_counts") == [x // 2 for x in SCALES] and
         protocol.get("Q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("height") == HEIGHT and
         protocol.get("euler_tail_cutoff") == TAIL_CUTOFF and
         protocol.get("placement_rule") == PLACEMENT_RULE and
         protocol.get("controls") == controls and
         protocol.get("laws") == list(LAW_NAMES), "protocol")
    need(payload.get("parent_lock") == {
        "TPC331_producer_sha256": PARENT_CODE_SHA256,
        "TPC331_certificate_sha256": PARENT_CERT_SHA256,
    }, "parent lock")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 48, "row count")
    keys = {(row.get("origin"), row.get("scale"), row.get("Q"),
             row.get("kernel_exponent")) for row in rows}
    need(keys == {(o, n, q, s) for o in ORIGINS for n in SCALES
                  for q in Q_ANCHORS for s in EXPONENTS}, "row keys")
    counts = {law: {component: {label: 0 for label in LABELS}
                    for component in COMPONENTS} for law in LAW_NAMES}
    for row in rows:
        source = row.get("source_l2")
        need(isinstance(source, dict), "source L2 field")
        for key in ("lambda_l2", "comparison_l2", "residual_l2",
                    "lambda_comparison_inner_product",
                    "lambda_l2_per_source", "comparison_l2_per_source",
                    "residual_l2_per_source",
                    "normalized_cross_correlation"):
            value = float(source[key])
            need(math.isfinite(value), "source L2 finiteness")
        need(float(source["residual_identity_error"]) < 1.0e-8,
             "source identity error")
        decomposition = row.get("control_average_decomposition")
        need(isinstance(decomposition, dict), "decomposition field")
        for law in LAW_NAMES:
            law_record = decomposition.get(law)
            need(isinstance(law_record, dict) and
                 law_record.get("control_count") == 5, "decomposition shape")
            for component in COMPONENTS:
                record = law_record.get(component)
                need(isinstance(record, dict) and
                     record.get("classification") in LABELS,
                     "component record")
                ratio = float(record["ratio"])
                lo, hi = map(float, record["ratio_interval"])
                need(math.isfinite(ratio) and lo == ratio - RATIO_GUARD and
                     hi == ratio + RATIO_GUARD, "component guard")
                counts[law][component][record["classification"]] += 1
            coherent = float(law_record["energy_fraction_coherent"])
            centered = float(law_record["energy_fraction_centered"])
            need(math.isfinite(coherent) and math.isfinite(centered) and
                 abs(coherent + centered - 1.0) < 1.0e-10,
                 "component fractions")
    need(counts == EXPECTED_CENSUS, "decomposition census")
    finite = payload.get("finite_audit")
    need(isinstance(finite, dict) and finite.get("rows") == 48 and
         finite.get("origins") == 2 and finite.get("scales") == 3 and
         finite.get("laws") == 4 and
         finite.get("decomposition_observations") == 192 and
         finite.get("control_count") == 5 and
         finite.get("decomposition_census") == EXPECTED_CENSUS and
         finite.get("arithmetic_advance") == "NO" and
         finite.get("fixed_power_credit") == 0, "finite audit")
    source_audit = payload.get("source_ensemble_audit")
    need(isinstance(source_audit, dict) and
         source_audit.get("source_l2_observations") == 6 and
         len(source_audit.get("windows", [])) == 6 and
         len(source_audit.get("growth_pairs", [])) == 4 and
         source_audit.get("all_plus_actual_census") == {
             "NEGATIVE_OFF_DIAGONAL": 27,
             "POSITIVE_OFF_DIAGONAL": 21,
             "UNRESOLVED": 0}, "source ensemble audit")
    anchor = payload.get("exact_anchor")
    need(isinstance(anchor, dict) and anchor.get("interval") == [44001, 44016]
         and anchor.get("Q") == 4 and anchor.get("shell") == [5, 7]
         and anchor.get("exponent") == 1 and
         anchor.get("mean_centered_identity_exact") is True,
         "exact anchor")
    expected_anchor = {
        "identity": (
            "2ac54aca8cad770b1eec2d250d3cb4d00e92d25a7facdc05eac7882d0ca4f082",
            "e9375cfdc17673d47b8afcc2c93df974dad942cada2bd266a5ba6ac334f16ac0",
            "352cf00142ecc3af964b221f673e4c0b913437291952fce22eb0da7185ecf8f6"),
        "control_average": (
            "66fd985e2aa210907d412b63baa3007bef8ff7d0dab3d57fd18cbf6454fdc336",
            "93881b878a40e2bbaabe8585b4bdff9b3c22775c5579fb1f041073493a2450e4",
            "953d4cd59e73d7806b6f2c086684a54fb3ed829b5276b30e15fd06da567b8f3f"),
        "coherent": (
            "c2446d91c735edbf677f659e834f6be16b80123f825c0454007c24b3af7d0ca2",
            "25383f4e91009f5c3eb03d626e2785b4429071e116554f958e1b4e5bcf42655b",
            "73a2661c8e4f9556ab0de7f7b48282aa3ae1d871b233a7a6ae08285d618dd3a2"),
        "centered": (
            "efeb18b8fc93bfbcbcbc93f3dc7da104dcb3e2ccc3f280c645ce303b433eda7b",
            "2b87b62a58fc24495ab6e1391c07fdc2bb5d9670444e1c4d0f82775b6122f1ed",
            "072cc8379690d8c63d8f9122db23f8bb8586dc2d411d6000f81f8a2100fed056"),
    }
    for component, digests in expected_anchor.items():
        record = anchor.get(component)
        need(isinstance(record, dict) and
             (record.get("energy_digest"),
              record.get("coordinate_diagonal_digest"),
              record.get("off_diagonal_digest")) == digests,
             "exact anchor digest")
    firewall = payload.get("claim_firewall")
    need(firewall == {
        "TPC332_EXACT_MEAN_CENTERED_DECOMPOSITION":
            "PROVED_EXACT_FINITE",
        "TPC332_SOURCE_NATIVE_VECTOR":
            "PROVED_EXACT_FINITE_DECLARED_MODEL",
        "TPC332_SOURCE_L2_IDENTITY":
            "PROVED_EXACT_FINITE_FLOAT64_REPLAY",
        "TPC332_GROWING_ENSEMBLE":
            "NUMERICALLY_CERTIFIED_FINITE_48_ROWS",
        "TPC332_CONTROL_AVERAGE_CENSUS":
            "NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
        "TPC332_CENTERED_POSITION_CENSUS":
            "NUMERICALLY_CERTIFIED_FINITE_48_OF_48",
        "TPC332_COHERENT_CENSUS":
            "NUMERICALLY_CERTIFIED_FINITE_47_OF_48",
        "TPC332_SOURCE_L2_GROWTH":
            "NUMERICALLY_CERTIFIED_FINITE_OBSERVATION",
        "TPC332_ARITHMETIC_ADVANCE": "NO",
        "TPC332_FIXED_POWER_CREDIT": 0,
        "TPC332_GROWING_SOURCE_NATIVE_L2": "OPEN",
        "TPC332_FULL_GATE_B": "OPEN",
        "TPC332_TWIN_PRIME_RESULT": "NONE",
    }, "claim firewall")


def check() -> None:
    payload = read_certificate()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERTIFICATE.read_bytes()) == PARENT_CERT_SHA256 and
         digest(V59_CODE.read_bytes()) == V59_CODE_SHA256 and
         digest(V59_CERTIFICATE.read_bytes()) == V59_CERT_SHA256,
         "provenance locks")
    validate_payload(payload)
    mutations: list[dict[str, Any]] = []
    bad = json.loads(json.dumps(payload))
    del bad["rows"][0]["source_l2"]
    mutations.append(bad)
    bad = json.loads(json.dumps(payload))
    bad["finite_audit"]["rows"] = 47
    mutations.append(bad)
    bad = json.loads(json.dumps(payload))
    bad["protocol"]["origins"][0] += 2
    mutations.append(bad)
    bad = json.loads(json.dumps(payload))
    bad["exact_anchor"]["identity"]["energy_digest"] = "0" * 64
    mutations.append(bad)
    bad = json.loads(json.dumps(payload))
    bad["claim_firewall"]["TPC332_ARITHMETIC_ADVANCE"] = "YES"
    mutations.append(bad)
    rejected = 0
    for mutation in mutations:
        try:
            validate_payload(mutation)
        except (Failure, KeyError, TypeError, ValueError):
            rejected += 1
    need(rejected == len(mutations), "mutation accepted")
    finite_gram_identity()
    print("TPC332_STRESS=PASS rows=48 decomposition_observations=192 "
          "source_windows=6 growth_pairs=4 control_count=5 "
          "exact_gram_identity=1 mutations=5 firewall=fail_closed")


def main() -> int:
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    try:
        check()
    except (Failure, DuplicateKey, OSError, json.JSONDecodeError, KeyError,
            TypeError, ValueError) as error:
        print("TPC332_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
