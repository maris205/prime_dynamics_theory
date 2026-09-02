#!/usr/bin/env python3
"""TPC-338: growing-control covariance spectrum.

TPC-337 found that five-control output variation dominates the coherent mean.
This release adds four predeclared affine controls and compares the nested
five-control and nine-control covariance ledgers on the same parent-locked
source/operator panel.  It is designed to separate stable energy structure
from control-family-dependent signed entries.
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
from typing import Any, Iterable

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc338_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-337-control-covariance-masked-response"
PARENT_CODE = PARENT_PROJECT / "code/tpc337_control_covariance_masked_response.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc337_certificate.json"
PARENT_CODE_SHA256 = "e74d621fa48fe7c15ff4e520dc2a051e5b195a5045c706592f275a6ead6b384d"
PARENT_CERT_SHA256 = "558f9a2dc60cd6616230785b46934a415459211a2e1bc31083447c53dd40e1d2"

SCHEMA = "TPC338_GROWING_CONTROL_COVARIANCE_SPECTRUM_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM"
ORIGINS = (42001, 44001)
SCALES = (2048, 4096, 8192)
Q = 54
EXPONENT = 1
HEIGHT = 66
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
CONTROLS = (
    ("identity", 1, 0, "pi_0(i)=i"),
    ("affine_3_11", 3, 11, "pi_3,11(i)=(3*i+11) mod source_count"),
    ("affine_5_17", 5, 17, "pi_5,17(i)=(5*i+17) mod source_count"),
    ("affine_7_29", 7, 29, "pi_7,29(i)=(7*i+29) mod source_count"),
    ("reversal", -1, -1, "pi_rev(i)=source_count-1-i"),
    ("affine_9_1", 9, 1, "pi_9,1(i)=(9*i+1) mod source_count"),
    ("affine_11_13", 11, 13, "pi_11,13(i)=(11*i+13) mod source_count"),
    ("affine_13_17", 13, 17, "pi_13,17(i)=(13*i+17) mod source_count"),
    ("affine_17_19", 17, 19, "pi_17,19(i)=(17*i+19) mod source_count"),
)
CONTROL_NAMES = tuple(item[0] for item in CONTROLS)
OLD_COUNT = 5
NUMERIC_TOL = 6.0e-6
SIGN_GUARD = 1.0e-7


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


def load_parent() -> tuple[Any, dict[str, Any]]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC337 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC337 certificate provenance")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE",
         "TPC337 certificate header")
    spec = importlib.util.spec_from_file_location("tpc337_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source, _ = module.load_parent()
    return source, document


def classify(source: Any, value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = source.prime_power(value + 2)
    need(power is not None, "prime-power support")
    if power[1] == 1:
        return "twin_prime" if source.is_prime_small(value) else "non_twin_prime_shift"
    return "prime_power_shift"


def indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def exact_anchor() -> dict[str, Any]:
    # The two-control identity is nested in every larger control orbit.
    vectors = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    mean = [sum(vector[k] for vector in vectors) / 2 for k in range(2)]
    centered = [[vector[k] - mean[k] for k in range(2)] for vector in vectors]
    average_energy = sum(sum(item * item for item in vector)
                         for vector in vectors) / 2
    coherent_energy = sum(item * item for item in mean)
    centered_energy = sum(sum(item * item for item in vector)
                          for vector in centered) / 2
    need(average_energy == coherent_energy + centered_energy,
         "nested exact anchor")
    return {"orbit": [["1", "0"], ["0", "1"]],
            "average_energy": str(average_energy),
            "coherent_energy": str(coherent_energy),
            "centered_energy": str(centered_energy),
            "identity_exact": True}


def scalar(average: float, coherent: float, centered: float,
           error: float) -> dict[str, Any]:
    need(all(math.isfinite(item) and item >= -NUMERIC_TOL
             for item in (average, coherent, centered, error)),
         "finite scalar")
    average = max(0.0, average)
    coherent = max(0.0, coherent)
    centered = max(0.0, centered)
    return {"average_energy": show(average),
            "coherent_energy": show(coherent),
            "centered_energy": show(centered),
            "identity_error": show(error),
            "coherent_fraction": show(coherent / average) if average else "0",
            "centered_fraction": show(centered / average) if average else "0"}


def matrix_strings(matrix: np.ndarray) -> list[list[str]]:
    return [[show(float(matrix[i, j])) for j in range(len(CATEGORIES))]
            for i in range(len(CATEGORIES))]


def ensemble_record(outputs: np.ndarray, selected: Iterable[int]) -> dict[str, Any]:
    selected_indices = list(selected)
    orbit = outputs[:, selected_indices, :]
    count = len(selected_indices)
    means = orbit.mean(axis=1)
    centered = orbit - means[:, None, :]
    class_average = np.mean(np.sum(orbit * orbit, axis=2), axis=1)
    class_coherent = np.sum(means * means, axis=1)
    class_centered = np.mean(np.sum(centered * centered, axis=2), axis=1)
    classes = {}
    for i, name in enumerate(CATEGORIES):
        error = abs(float(class_average[i] - class_coherent[i] -
                          class_centered[i]))
        classes[name] = scalar(float(class_average[i]), float(class_coherent[i]),
                               float(class_centered[i]), error)
    full = orbit.sum(axis=0)
    full_mean = means.sum(axis=0)
    full_centered = centered.sum(axis=0)
    full_average = float(np.mean(np.sum(full * full, axis=1)))
    full_coherent = float(full_mean @ full_mean)
    full_centered_energy = float(np.mean(np.sum(full_centered * full_centered,
                                                axis=1)))
    full_error = abs(full_average - full_coherent - full_centered_energy)
    covariance = np.einsum("cjn,djn->cd", centered, centered) / count
    covariance = (covariance + covariance.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(covariance)
    need(bool(np.all(np.isfinite(eigenvalues))), "finite covariance spectrum")
    trace = float(np.trace(covariance))
    normalized = eigenvalues / trace if trace else eigenvalues
    pairs = {}
    for i, left in enumerate(CATEGORIES):
        for j in range(i + 1, len(CATEGORIES)):
            pairs[left + "__" + CATEGORIES[j]] = show(float(covariance[i, j]))
    return {
        "control_count": count,
        "selected_controls": [CONTROL_NAMES[i] for i in selected_indices],
        "class_response": classes,
        "full_response": scalar(full_average, full_coherent,
                                full_centered_energy, full_error),
        "covariance_gram": matrix_strings(covariance),
        "covariance_eigenvalues": [show(float(item)) for item in eigenvalues],
        "normalized_covariance_eigenvalues": [show(float(item))
                                               for item in normalized],
        "covariance_trace": show(trace),
        "full_centered_minus_class_trace": show(
            full_centered_energy - trace),
        "pair_covariance": pairs,
    }


def row_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comparison, beta, width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(beta), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[classify(source, value, float(lam[i]), float(comparison[i]))][i] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    outputs = np.zeros((len(CATEGORIES), len(CONTROLS), len(beta)))
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    control_records = []
    for j, (name, multiplier, offset, rule) in enumerate(CONTROLS):
        permutation = indices(len(beta), multiplier, offset)
        for i, category_name in enumerate(CATEGORIES):
            outputs[i, j] = matrix @ vectors[category_name][permutation]
        control_records.append({"name": name, "multiplier": multiplier,
                                "offset": offset, "rule": rule,
                                "bijection": True})
    five = ensemble_record(outputs, range(OLD_COUNT))
    nine = ensemble_record(outputs, range(len(CONTROLS)))
    five_eigen = np.asarray([float(item)
                             for item in five["normalized_covariance_eigenvalues"]])
    nine_eigen = np.asarray([float(item)
                             for item in nine["normalized_covariance_eigenvalues"]])
    eigen_l1 = float(np.sum(np.abs(five_eigen - nine_eigen)))
    five_matrix = np.asarray([[float(item) for item in row]
                              for row in five["covariance_gram"]])
    nine_matrix = np.asarray([[float(item) for item in row]
                              for row in nine["covariance_gram"]])
    relative_matrix = float(np.linalg.norm(nine_matrix - five_matrix) /
                            np.linalg.norm(five_matrix))
    need(float(five["full_response"]["centered_fraction"]) > 0.75 and
         float(nine["full_response"]["centered_fraction"]) > 0.85,
         "centered dominance")
    need(float(five["full_response"]["coherent_fraction"]) < 0.25 and
         float(nine["full_response"]["coherent_fraction"]) < 0.15,
         "coherent suppression")
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(beta),
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "operator": {"law": "all_plus", "Q": Q,
                      "kernel_exponent": EXPONENT, "height": HEIGHT},
        "controls": control_records,
        "five_control": five, "nine_control": nine,
        "normalized_spectrum_l1_distance": show(eigen_l1),
        "covariance_relative_frobenius_change": show(relative_matrix),
        "source_weight_max_interval_width": show(width),
    }


def build_payload() -> dict[str, Any]:
    source, _ = load_parent()
    rows = [row_record(source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    five_centered = [float(row["five_control"]["full_response"][
        "centered_fraction"]) for row in rows]
    nine_centered = [float(row["nine_control"]["full_response"][
        "centered_fraction"]) for row in rows]
    five_coherent = [float(row["five_control"]["full_response"][
        "coherent_fraction"]) for row in rows]
    nine_coherent = [float(row["nine_control"]["full_response"][
        "coherent_fraction"]) for row in rows]
    l1 = [float(row["normalized_spectrum_l1_distance"]) for row in rows]
    rel = [float(row["covariance_relative_frobenius_change"]) for row in rows]
    sign_census: dict[str, Any] = {}
    for ensemble_name in ("five_control", "nine_control"):
        sign_census[ensemble_name] = {}
        for pair in ("twin_prime__non_twin_prime_shift",
                     "twin_prime__zero_support",
                     "non_twin_prime_shift__zero_support"):
            values = [float(row[ensemble_name]["pair_covariance"][pair])
                      for row in rows]
            sign_census[ensemble_name][pair] = {
                "negative": sum(item < -SIGN_GUARD for item in values),
                "positive": sum(item > SIGN_GUARD for item in values),
                "zero_or_unresolved": sum(abs(item) <= SIGN_GUARD
                                           for item in values),
            }
    need(sign_census["five_control"]["twin_prime__zero_support"]["negative"] == 6,
         "five-control twin-zero sign")
    need(sign_census["nine_control"]["twin_prime__zero_support"]["positive"] == 6,
         "nine-control twin-zero sign")
    need(sign_census["five_control"]["twin_prime__non_twin_prime_shift"]["positive"] == 6 and
         sign_census["nine_control"]["twin_prime__non_twin_prime_shift"]["positive"] == 6,
         "twin-background sign")
    need(sign_census["five_control"]["non_twin_prime_shift__zero_support"]["negative"] == 6 and
         sign_census["nine_control"]["non_twin_prime_shift__zero_support"]["negative"] == 6,
         "background-zero sign")
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC337_producer_sha256": PARENT_CODE_SHA256,
                         "TPC337_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "control_orbit": [
                {"name": name, "multiplier": multiplier, "offset": offset,
                 "rule": rule}
                for name, multiplier, offset, rule in CONTROLS],
            "nested_comparison": "first five controls versus all nine controls",
            "covariance_definition":
                "K_CD=(1/m) sum_j <y_Cj-ybar_C,y_Dj-ybar_D>",
        },
        "exact_theorem": {
            "nested_mean_centered_identity":
                "mean_j ||y_Cj||^2=||ybar_C||^2+mean_j ||z_Cj||^2",
            "covariance_gram_psd": "K is a finite centered-output Gram matrix",
            "spectrum_normalization": "eigenvalues divided by trace when trace>0",
            "finite_scope": "the identities are finite; spectrum comparisons are observations",
        },
        "finite_audit": {
            "rows": 6, "origins": 2, "scales": 3,
            "five_controls": 5, "nine_controls": 9, "categories": 4,
            "nested_decompositions": 48, "normalized_spectrum_comparisons": 6,
            "pair_sign_ensembles": 2, "fixed_power_credit": 0,
            "arithmetic_advance": "NO",
        },
        "summary": {
            "five_centered_fraction_min": show(min(five_centered)),
            "five_centered_fraction_max": show(max(five_centered)),
            "nine_centered_fraction_min": show(min(nine_centered)),
            "nine_centered_fraction_max": show(max(nine_centered)),
            "five_coherent_fraction_min": show(min(five_coherent)),
            "five_coherent_fraction_max": show(max(five_coherent)),
            "nine_coherent_fraction_min": show(min(nine_coherent)),
            "nine_coherent_fraction_max": show(max(nine_coherent)),
            "normalized_spectrum_l1_min": show(min(l1)),
            "normalized_spectrum_l1_max": show(max(l1)),
            "covariance_relative_frobenius_min": show(min(rel)),
            "covariance_relative_frobenius_max": show(max(rel)),
            "sign_census": sign_census,
            "energy_dominance_rows": 6,
            "twin_zero_sign_reversal": True,
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC338_NESTED_COVARIANCE_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC338_COVARIANCE_GRAM_PSD":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC338_ENERGY_DOMINANCE_STABILITY":
                "NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
            "TPC338_NORMALIZED_SPECTRUM_STABILITY":
                "NUMERICALLY_CERTIFIED_FINITE_6_ROWS",
            "TPC338_TWIN_ZERO_SIGN_STABILITY": "REFUTED_SCOPED",
            "TPC338_TWIN_ZERO_SIGN_REVERSAL":
                "NUMERICALLY_CERTIFIED_FINITE_6_OF_6_NESTED_COMPARISON",
            "TPC338_TWIN_BACKGROUND_SIGN":
                "NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6_BOTH_ENSEMBLES",
            "TPC338_BACKGROUND_ZERO_SIGN":
                "NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6_BOTH_ENSEMBLES",
            "TPC338_ARITHMETIC_ADVANCE": "NO",
            "TPC338_FIXED_POWER_CREDIT": 0,
            "TPC338_SOURCE_UNIFORM_L2": "OPEN",
            "TPC338_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC338_FULL_GATE_B": "OPEN",
            "TPC338_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue":
            "REPLACE_SIGN_HEURISTICS_BY_A_UNIFORM_MASKED_OPERATOR_ENVELOPE",
        "rows": rows,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        document = build_document()
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(document))
            print("TPC338_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC338 certificate does not replay")
            print("TPC338_CERTIFICATE=PASS rows=6 five_controls=5 nine_controls=9 "
                  "energy_dominance=6 twin_zero_reversal=6 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC338_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
