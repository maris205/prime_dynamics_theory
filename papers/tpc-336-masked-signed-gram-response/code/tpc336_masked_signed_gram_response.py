#!/usr/bin/env python3
"""TPC-336: signed-Gram response of twin and background masks.

TPC-335 found a non-dominant but non-negligible twin residual component.  This
release feeds the four source masks through one fixed all-plus signed-Gram
operator (Q=54, s=1).  It records self responses and output cross terms, so
the full response identity is auditable rather than inferred from component
energies.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc336_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-335-twin-isolated-source-norm"
PARENT_CODE = PARENT_PROJECT / "code/tpc335_twin_isolated_source_norm.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc335_certificate.json"
PARENT_CODE_SHA256 = "e6d66a3963f974c9d3f03b20441b327a34dd9e684fabb72e0777d31082c4e608"
PARENT_CERT_SHA256 = "cee2aee00208cbfe8331abc80e066c7a736824414f4d8208a73e4c545bfa4934"
SCHEMA = "TPC336_MASKED_SIGNED_GRAM_RESPONSE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q = 54
EXPONENT = 1
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
              "prime_power_shift", "zero_support")


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC335 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC335 certificate provenance")
    raw = PARENT_CERT.read_bytes(); document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM",
         "TPC335 header")
    return document


def parent_source_module() -> Any:
    spec = importlib.util.spec_from_file_location("tpc335_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.parent_source_module()


def classify(source: Any, t: int, lam: float, comp: float) -> str:
    if lam * comp == 0.0:
        return "zero_support"
    pp = source.prime_power(t + 2)
    need(pp is not None, "support prime power")
    if pp[1] == 1:
        return "twin_prime" if source.is_prime_small(t) else "non_twin_prime_shift"
    return "prime_power_shift"


def metric(matrix: Any, vector: Any, column_energy: Any) -> dict[str, Any]:
    output = matrix @ vector
    energy = float(output @ output)
    diagonal = float(np.sum(column_energy * vector * vector))
    need(energy > 0 and diagonal > 0 and math.isfinite(energy),
         "positive response metric")
    return {"energy": show(energy), "coordinate_diagonal": show(diagonal),
            "off_diagonal": show(energy - diagonal),
            "ratio": show(energy / diagonal)}


def exact_anchor() -> dict[str, Any]:
    # A rational output-Gram identity for two disjoint labeled components.
    matrix = [[Fraction(2), Fraction(1)], [Fraction(1), Fraction(-1)]]
    twin = [Fraction(1), Fraction(0)]; background = [Fraction(0), Fraction(2)]
    full = [a + b for a, b in zip(twin, background)]
    def energy(vector: list[Fraction]) -> Fraction:
        out = [sum(matrix[i][j] * vector[j] for j in range(2))
               for i in range(2)]
        return sum(x * x for x in out)
    et, eb, ef = energy(twin), energy(background), energy(full)
    cross = sum((sum(matrix[i][j] * twin[j] for j in range(2)) *
                 sum(matrix[i][j] * background[j] for j in range(2))
                 for i in range(2)), Fraction(0))
    need(ef == et + eb + 2 * cross, "exact output Gram anchor")
    return {"matrix": [["2", "1"], ["1", "-1"]],
            "twin": ["1", "0"], "background": ["0", "2"],
            "full": ["1", "2"], "twin_energy": str(et),
            "background_energy": str(eb), "cross_inner_product": str(cross),
            "full_energy": str(ef), "identity_exact": True}


def source_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, beta, width = source.source_vectors(lo, hi)
    masks = {c: np.zeros(len(beta), dtype=bool) for c in CATEGORIES}
    for i, t in enumerate(range(lo, hi + 1)):
        masks[classify(source, t, float(lam[i]), float(comp[i]))][i] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    column_energy = np.sum(matrix * matrix, axis=0, dtype=np.float64)
    vectors = {c: beta * masks[c] for c in CATEGORIES}
    outputs = {c: matrix @ vectors[c] for c in CATEGORIES}
    source_norms = {c: float(v @ v) for c, v in vectors.items()}
    self_metrics = {}
    for c in CATEGORIES:
        e = float(outputs[c] @ outputs[c])
        d = float(np.sum(column_energy * vectors[c] * vectors[c]))
        if source_norms[c] == 0.0:
            need(e == 0.0 and d == 0.0, "empty response metric")
            gain = 0.0
        else:
            need(e > 0 and d > 0 and math.isfinite(e), "response metric")
            gain = e / source_norms[c]
        self_metrics[c] = {
            "coordinate_count": int(masks[c].sum()),
            "source_l2": show(source_norms[c]),
            "response_energy": show(e),
            "coordinate_diagonal": show(d),
            "off_diagonal": show(e - d),
            "response_gain": show(gain),
        }
    pairwise: dict[str, str] = {}
    for i, left in enumerate(CATEGORIES):
        for right in CATEGORIES[i:]:
            pairwise[left + "__" + right] = show(
                float(outputs[left] @ outputs[right]))
    full_output = matrix @ beta
    full_energy = float(full_output @ full_output)
    full_source_l2 = float(beta @ beta)
    self_sum = sum(float(self_metrics[c]["response_energy"]) for c in CATEGORIES)
    pair_twice = 2.0 * sum(float(pairwise[left + "__" + right])
                            for i, left in enumerate(CATEGORIES)
                            for right in CATEGORIES[i + 1:])
    identity_error = abs(full_energy - self_sum - pair_twice)
    gains = {c: float(self_metrics[c]["response_gain"]) for c in CATEGORIES}
    ordering = sorted(CATEGORIES, key=lambda c: (-gains[c], c))
    need(ordering == ["zero_support", "non_twin_prime_shift", "twin_prime",
                      "prime_power_shift"], "response gain ordering")
    return {
        "origin": origin, "scale": scale, "source_interval": [lo, hi],
        "source_count": scale // 2, "operator": {"law": "all_plus", "Q": Q,
        "kernel_exponent": EXPONENT, "height": 66},
        "self_metrics": self_metrics, "output_pairwise_gram": pairwise,
        "full_source_l2": show(full_source_l2),
        "full_response_energy": show(full_energy),
        "full_response_gain": show(full_energy / full_source_l2),
        "self_response_energy_sum": show(self_sum),
        "twice_pair_interaction_sum": show(pair_twice),
        "response_identity_error": show(identity_error),
        "self_to_full_energy_ratio": show(self_sum / full_energy),
        "destructive_interaction": bool(full_energy < self_sum),
        "response_gain_order": ordering,
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    source = parent_source_module()
    rows = [source_record(source, o, s) for o in ORIGINS for s in SCALES]
    category_ranges = {}
    for c in CATEGORIES:
        values = [float(r["self_metrics"][c]["response_gain"]) for r in rows]
        category_ranges[c] = {"gain_min": show(min(values)),
                              "gain_max": show(max(values))}
    ratios = [float(r["self_to_full_energy_ratio"]) for r in rows]
    errors = [float(r["response_identity_error"]) for r in rows]
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC335_producer_sha256": PARENT_CODE_SHA256,
                         "TPC335_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {"origins": list(ORIGINS), "scales": list(SCALES),
                      "source_counts": [s // 2 for s in SCALES],
                      "operator_law": "all_plus", "Q": Q,
                      "kernel_exponent": EXPONENT, "height": 66,
                      "categories": list(CATEGORIES),
                      "response_identity": "full=sum self+2 sum output cross"},
        "finite_audit": {"rows": 6, "operator_rows": 6, "categories": 4,
                          "response_identity_observations": 6,
                          "gain_ordering_census": 6,
                          "arithmetic_advance": "NO", "fixed_power_credit": 0},
        "rows": rows,
        "summary": {"gain_ranges": category_ranges,
                     "self_to_full_energy_ratio_min": show(min(ratios)),
                     "self_to_full_energy_ratio_max": show(max(ratios)),
                     "destructive_interaction_rows": sum(
                         r["destructive_interaction"] for r in rows),
                     "max_response_identity_error": show(max(errors))},
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC336_MASK_RESPONSE_IDENTITY": "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC336_FIXED_OPERATOR_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
            "TPC336_GAIN_ORDERING": "NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
            "TPC336_DESTRUCTIVE_OUTPUT_INTERACTION": "NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
            "TPC336_TWIN_RESPONSE_DOMINANCE": "REFUTED_SCOPED_FINITE_PANEL",
            "TPC336_ARITHMETIC_ADVANCE": "NO",
            "TPC336_FIXED_POWER_CREDIT": 0,
            "TPC336_SOURCE_UNIFORM_L2": "OPEN",
            "TPC336_FULL_GATE_B": "OPEN",
            "TPC336_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "RETURN_TO_CONTROL_COVARIANCE_OR_SEEK_UNIFORM_MASKED_OPERATOR_BOUND",
    }


def build_document() -> dict[str, Any]:
    load_parent(); payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def check_document(document: dict[str, Any]) -> None:
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "header")
    payload = document.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA,
         "schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload digest")
    need(payload.get("parent_lock") == {
        "TPC335_producer_sha256": PARENT_CODE_SHA256,
        "TPC335_certificate_sha256": PARENT_CERT_SHA256}, "parent lock")
    need(payload.get("finite_audit") == {
        "rows": 6, "operator_rows": 6, "categories": 4,
        "response_identity_observations": 6, "gain_ordering_census": 6,
        "arithmetic_advance": "NO", "fixed_power_credit": 0}, "audit")
    rows = payload.get("rows"); need(isinstance(rows, list) and len(rows) == 6,
                                        "rows")
    source = parent_source_module()
    rebuilt = [source_record(source, o, s) for o in ORIGINS for s in SCALES]
    for actual, recorded in zip(rebuilt, rows):
        need(actual.keys() == recorded.keys(), "row fields")
        for key, value in actual.items():
            if isinstance(value, str):
                need(abs(float(value) - float(recorded[key])) <=
                     4.0e-10 * max(1.0, abs(float(value))), "row " + key)
            elif isinstance(value, dict):
                if key == "self_metrics":
                    for c in CATEGORIES:
                        for field, item in value[c].items():
                            if isinstance(item, str):
                                need(abs(float(item) - float(recorded[key][c][field])) <=
                                     4.0e-10 * max(1.0, abs(float(item))),
                                     "metric " + c + " " + field)
                            else:
                                need(item == recorded[key][c][field],
                                     "metric field")
                elif key == "operator":
                    need(value == recorded[key], "operator protocol")
                else:
                    for field, item in value.items():
                        need(abs(float(item) - float(recorded[key][field])) <=
                             4.0e-10 * max(1.0, abs(float(item))),
                             "pair " + field)
            elif isinstance(value, list):
                need(value == recorded[key], "list " + key)
            else:
                need(value == recorded[key], "field " + key)
    need(payload["summary"]["destructive_interaction_rows"] == 6,
         "destructive census")
    need(payload["exact_anchor"]["identity_exact"] is True, "anchor")
    fw = payload["claim_firewall"]
    need(fw["TPC336_ARITHMETIC_ADVANCE"] == "NO" and
         fw["TPC336_SOURCE_UNIFORM_L2"] == "OPEN" and
         fw["TPC336_FIXED_POWER_CREDIT"] == 0, "firewall")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true"); args = parser.parse_args()
    try:
        if args.write:
            RESULT.write_bytes(canonical(build_document()))
        if args.check:
            raw = RESULT.read_bytes(); document = json.loads(raw)
            need(raw == canonical(document), "canonicality")
            load_parent(); check_document(document)
            print("TPC336_CERTIFICATE=PASS rows=6 categories=4 "
                  "gain_ordering=6 destructive_interaction=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC336_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
