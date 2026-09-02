#!/usr/bin/env python3
"""TPC-337: control covariance of masked signed-Gram responses.

TPC-336 showed that source-mask gains do not transfer through the fixed
all-plus operator.  Here every source mask is transported by the same five
predeclared coordinate bijections before the operator is applied.  The
certificate records the exact finite mean/centered covariance decomposition
of each masked output and the resulting four-by-four covariance Gram matrix.
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
RESULT = PROJECT / "results/tpc337_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-336-masked-signed-gram-response"
PARENT_CODE = PARENT_PROJECT / "code/tpc336_masked_signed_gram_response.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc336_certificate.json"
PARENT_CODE_SHA256 = "0c2febd76d6bfdc5af4b58145739bcc04b435303f15c66b31e2d0b2e63497442"
PARENT_CERT_SHA256 = "926859be38cc601ef728363328899d4e9ab2001f77e7e1106ab028d64cf2814a"

SCHEMA = "TPC337_CONTROL_COVARIANCE_MASKED_RESPONSE_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE"
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
)
CONTROL_NAMES = tuple(item[0] for item in CONTROLS)
PAIR_NAMES = tuple(CATEGORIES[i] + "__" + CATEGORIES[j]
                   for i in range(len(CATEGORIES))
                   for j in range(i + 1, len(CATEGORIES)))
NUMERIC_TOL = 5.0e-6
SIGN_GUARD = 1.0e-7


class Failure(RuntimeError):
    """Fail-closed certificate error."""


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
         "TPC336 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC336 certificate provenance")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE",
         "TPC336 certificate header")
    spec = importlib.util.spec_from_file_location("tpc336_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.parent_source_module(), document


def permutation(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        indices = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        indices = np.asarray([(multiplier * i + offset) % size
                              for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in indices)) == size,
         "control is not bijective")
    return indices


def classify(source: Any, value: int, lam: float, comp: float) -> str:
    """Reapply the TPC-334 support partition at the physical coordinate."""
    if lam * comp == 0.0:
        return "zero_support"
    prime_power = source.prime_power(value + 2)
    need(prime_power is not None, "prime-power support")
    if prime_power[1] == 1:
        return ("twin_prime" if source.is_prime_small(value)
                else "non_twin_prime_shift")
    return "prime_power_shift"


def scalar_record(average: float, coherent: float, centered: float,
                  error: float) -> dict[str, Any]:
    need(all(math.isfinite(item) and item >= -NUMERIC_TOL
             for item in (average, coherent, centered, error)),
         "finite covariance scalar")
    average = max(0.0, average)
    coherent = max(0.0, coherent)
    centered = max(0.0, centered)
    return {
        "average_energy": show(average),
        "coherent_energy": show(coherent),
        "centered_energy": show(centered),
        "identity_error": show(error),
        "coherent_fraction": show(coherent / average) if average else "0",
        "centered_fraction": show(centered / average) if average else "0",
    }


def exact_anchor() -> dict[str, Any]:
    # Two class-labelled output orbits.  The average cross covariance is zero,
    # while the coherent and centered cross terms cancel exactly.
    twin = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    background = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(-1)]]

    def mean(vectors: list[list[Fraction]]) -> list[Fraction]:
        return [sum(row[k] for row in vectors) / len(vectors)
                for k in range(len(vectors[0]))]

    def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
        return sum((a * b for a, b in zip(left, right)), Fraction(0))

    twin_mean = mean(twin)
    background_mean = mean(background)
    twin_centered = [[a - b for a, b in zip(row, twin_mean)] for row in twin]
    background_centered = [[a - b for a, b in zip(row, background_mean)]
                           for row in background]
    avg_cross = sum((dot(a, b) for a, b in zip(twin, background)), Fraction(0)) / 2
    coherent_cross = dot(twin_mean, background_mean)
    centered_cross = sum((dot(a, b) for a, b in zip(
        twin_centered, background_centered)), Fraction(0)) / 2
    need(avg_cross == coherent_cross + centered_cross,
         "exact covariance anchor")
    return {
        "twin_orbit": [["1", "0"], ["0", "1"]],
        "background_orbit": [["1", "1"], ["1", "-1"]],
        "average_cross": str(avg_cross),
        "coherent_cross": str(coherent_cross),
        "centered_cross": str(centered_cross),
        "identity_exact": True,
    }


def row_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comp, beta, width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(beta), dtype=bool) for name in CATEGORIES}
    for index, value in enumerate(range(lo, hi + 1)):
        name = classify(source, value, float(lam[index]), float(comp[index]))
        masks[name][index] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]

    outputs = np.zeros((len(CATEGORIES), len(CONTROLS), len(beta)),
                       dtype=np.float64)
    control_records: list[dict[str, Any]] = []
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    for control_index, (name, multiplier, offset, rule) in enumerate(CONTROLS):
        indices = permutation(len(beta), multiplier, offset)
        placed = {category: vectors[category][indices]
                  for category in CATEGORIES}
        for category_index, category in enumerate(CATEGORIES):
            outputs[category_index, control_index] = matrix @ placed[category]
        control_records.append({"name": name, "rule": rule,
                                "multiplier": multiplier, "offset": offset,
                                "bijection": True})

    means = outputs.mean(axis=1)
    centered = outputs - means[:, None, :]
    average_class = np.mean(np.sum(outputs * outputs, axis=2), axis=1)
    coherent_class = np.sum(means * means, axis=1)
    centered_class = np.mean(np.sum(centered * centered, axis=2), axis=1)
    class_records: dict[str, Any] = {}
    class_identity_errors: list[float] = []
    for index, category in enumerate(CATEGORIES):
        error = abs(float(average_class[index] - coherent_class[index] -
                          centered_class[index]))
        class_identity_errors.append(error)
        class_records[category] = {
            "coordinate_count": int(masks[category].sum()),
            "source_l2": show(float(np.dot(vectors[category],
                                             vectors[category]))),
            **scalar_record(float(average_class[index]),
                            float(coherent_class[index]),
                            float(centered_class[index]), error),
        }

    full_outputs = outputs.sum(axis=0)
    full_mean = means.sum(axis=0)
    full_centered = centered.sum(axis=0)
    full_average = float(np.mean(np.sum(full_outputs * full_outputs, axis=1)))
    full_coherent = float(np.dot(full_mean, full_mean))
    full_centered_energy = float(np.mean(np.sum(full_centered * full_centered,
                                                axis=1)))
    full_error = abs(full_average - full_coherent - full_centered_energy)

    average_gram = np.einsum("cjn,djn->cd", outputs, outputs) / len(CONTROLS)
    coherent_gram = means @ means.T
    covariance_gram = np.einsum("cjn,djn->cd", centered, centered) / len(CONTROLS)
    covariance_gram = (covariance_gram + covariance_gram.T) / 2.0
    eigenvalues = np.linalg.eigvalsh(covariance_gram)
    need(bool(np.all(np.isfinite(eigenvalues))), "covariance spectrum")

    def matrix_strings(matrix_value: np.ndarray) -> list[list[str]]:
        return [[show(float(matrix_value[i, j]))
                 for j in range(len(CATEGORIES))]
                for i in range(len(CATEGORIES))]

    pair_average = {}
    pair_coherent = {}
    pair_covariance = {}
    for i, left in enumerate(CATEGORIES):
        for j in range(i + 1, len(CATEGORIES)):
            key = left + "__" + CATEGORIES[j]
            pair_average[key] = show(float(average_gram[i, j]))
            pair_coherent[key] = show(float(coherent_gram[i, j]))
            pair_covariance[key] = show(float(covariance_gram[i, j]))

    need(full_error <= NUMERIC_TOL * max(1.0, full_average),
         "full mean-centered identity")
    need(all(error <= NUMERIC_TOL * max(1.0, average_class[i])
             for i, error in enumerate(class_identity_errors)),
         "class mean-centered identity")
    need(float(full_centered_energy / full_average) > 0.75 and
         float(full_coherent / full_average) < 0.25,
         "control covariance dominance")

    return {
        "origin": origin,
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": len(beta),
        "operator": {"law": "all_plus", "Q": Q,
                      "kernel_exponent": EXPONENT, "height": HEIGHT},
        "controls": control_records,
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "class_response": class_records,
        "full_response": scalar_record(full_average, full_coherent,
                                        full_centered_energy, full_error),
        "average_gram": matrix_strings(average_gram),
        "coherent_gram": matrix_strings(coherent_gram),
        "covariance_gram": matrix_strings(covariance_gram),
        "covariance_eigenvalues": [show(float(item)) for item in eigenvalues],
        "covariance_trace": show(float(np.trace(covariance_gram))),
        "full_centered_minus_class_trace": show(
            full_centered_energy - float(np.trace(covariance_gram))),
        "pair_average": pair_average,
        "pair_coherent": pair_coherent,
        "pair_covariance": pair_covariance,
        "source_weight_max_interval_width": show(width),
    }


def build_payload(parent_document: dict[str, Any]) -> dict[str, Any]:
    source, _ = load_parent()
    rows = [row_record(source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    coherent_fractions = [float(row["full_response"]["coherent_fraction"])
                          for row in rows]
    centered_fractions = [float(row["full_response"]["centered_fraction"])
                          for row in rows]
    eigen_minima = [min(float(item) for item in row["covariance_eigenvalues"])
                    for row in rows]
    pair_signs = {}
    for key in PAIR_NAMES:
        values = [float(row["pair_covariance"][key]) for row in rows]
        pair_signs[key] = {
            "negative": sum(item < -SIGN_GUARD for item in values),
            "positive": sum(item > SIGN_GUARD for item in values),
            "zero_or_unresolved": sum(abs(item) <= SIGN_GUARD
                                       for item in values),
        }
    need(all(item["positive"] == 6 for key, item in pair_signs.items()
             if key == "twin_prime__non_twin_prime_shift"),
         "twin-background covariance sign")
    need(all(item["negative"] == 6 for key, item in pair_signs.items()
             if key in ("twin_prime__zero_support",
                        "non_twin_prime_shift__zero_support")),
         "background covariance signs")
    need(min(coherent_fractions) > 0.0 and max(coherent_fractions) < 0.25,
         "coherent fraction range")
    need(min(centered_fractions) > 0.75, "centered fraction range")
    need(min(eigen_minima) >= -1.0e-4, "finite PSD guard")
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC336_producer_sha256": PARENT_CODE_SHA256,
                         "TPC336_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "source_counts": [scale // 2 for scale in SCALES],
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "controls": [
                {"name": name, "multiplier": multiplier, "offset": offset,
                 "rule": rule}
                for name, multiplier, offset, rule in CONTROLS],
            "output_definition": "y_C,j=C P_j beta_C",
            "covariance_definition":
                "K_CD=(1/m) sum_j <y_C,j-ybar_C,y_D,j-ybar_D>",
            "source_interval_rule": "I_{o,N}={o,...,o+N/2-1}",
        },
        "exact_theorem": {
            "mean_output": "ybar_C=(1/m) sum_j y_C,j",
            "centered_output": "z_C,j=y_C,j-ybar_C",
            "zero_sum": "sum_j z_C,j=0",
            "class_identity":
                "mean_j ||y_C,j||^2=||ybar_C||^2+mean_j ||z_C,j||^2",
            "pair_identity":
                "mean_j <y_C,j,y_D,j>=<ybar_C,ybar_D>+K_CD",
            "full_identity":
                "mean_j ||sum_C y_C,j||^2=||sum_C ybar_C||^2+"
                "mean_j ||sum_C z_C,j||^2",
            "covariance_psd": "K is a Gram matrix of centered outputs",
            "finite_scope": "all identities are finite bilinear identities",
        },
        "finite_audit": {
            "rows": 6, "origins": 2, "scales": 3, "controls": 5,
            "categories": 4, "class_decomposition_observations": 24,
            "pair_covariance_observations": 36,
            "full_decomposition_observations": 6,
            "covariance_spectrum_observations": 6,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "summary": {
            "full_coherent_fraction_min": show(min(coherent_fractions)),
            "full_coherent_fraction_max": show(max(coherent_fractions)),
            "full_centered_fraction_min": show(min(centered_fractions)),
            "full_centered_fraction_max": show(max(centered_fractions)),
            "covariance_eigenvalue_min": show(min(eigen_minima)),
            "covariance_pair_signs": pair_signs,
            "twin_background_covariance_positive_rows": 6,
            "twin_zero_covariance_negative_rows": 6,
            "background_zero_covariance_negative_rows": 6,
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC337_MEAN_CENTERED_OUTPUT_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC337_COVARIANCE_GRAM_PSD":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC337_MASKED_CONTROL_REPLAY":
                "NUMERICALLY_CERTIFIED_FINITE_6_ROWS_5_CONTROLS",
            "TPC337_FULL_CENTERED_COVARIANCE_DOMINANCE":
                "NUMERICALLY_CERTIFIED_FINITE_6_OF_6",
            "TPC337_TWIN_BACKGROUND_COVARIANCE_SIGN":
                "NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6",
            "TPC337_ZERO_BACKGROUND_COVARIANCE_SIGN":
                "NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6",
            "TPC337_SOURCE_SHARE_TRANSFER": "REFUTED_SCOPED",
            "TPC337_ARITHMETIC_ADVANCE": "NO",
            "TPC337_FIXED_POWER_CREDIT": 0,
            "TPC337_SOURCE_UNIFORM_L2": "OPEN",
            "TPC337_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC337_FULL_GATE_B": "OPEN",
            "TPC337_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue":
            "GROW_THE_CONTROL_ORBIT_AND_TEST_COVARIANCE_SPECTRUM_STABILITY",
        "rows": rows,
    }


def build_document() -> dict[str, Any]:
    _, parent_document = load_parent()
    payload = build_payload(parent_document)
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
            print("TPC337_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC337 certificate does not replay")
            print("TPC337_CERTIFICATE=PASS rows=6 controls=5 categories=4 "
                  "centered_dominance=6 covariance_psd=1 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC337_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
