#!/usr/bin/env python3
"""TPC-358: fresh-origin transfer of the finite normalized operator audit.

The three origins are fixed by an arithmetic spacing rule before any matrix
or spectral value is read.  The experiment then replays the TPC-357 protocol
on this disjoint origin-scale panel.  It is finite operator evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC358 requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc358_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-357-operator-norm-scale-ladder/code/"
    "tpc357_operator_norm_scale_ladder.py")
PARENT_CERT = ROOT / (
    "papers/tpc-357-operator-norm-scale-ladder/results/"
    "tpc357_certificate.json")
BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "44217207664b8bf08218458f102dacbdb03cf48c85a6fa0d72e7f23fe84a36a1")
PARENT_CERT_SHA256 = (
    "9eda189321af2233b6ff39eed97f8ead46ebe6853556b6baf3614e752a6e5fee")

SCHEMA = "TPC358_FRESH_ORIGIN_SPECTRAL_HOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FRESH_ORIGIN_SPECTRAL_HOLDOUT"
ROUND2_CLUE = (
    "TEST_A_GEOMETRY_ADVERSARIAL_FRESH_ORIGIN_OR_SCHUR_TIGHTNESS_HOLDOUT_"
    "BEFORE_ANY_SOURCE_UNIFORM_OPERATOR_CLAIM")

# Fixed before reading any matrix.  The spacing is deliberately much larger
# than the preceding panel, and none of these origins is a TPC-356 origin.
ORIGINS = (52_001, 120_001, 220_001)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
SPECTRAL_LAWS = ("all_plus",)
HEIGHT = 66
SCALE_GUARD = 1.0e-6
BOUND_TOL = 2.0e-10
PARENT_TRANSFER_TOL = 1.0e-3
EXACT_INTERVAL = (52_031, 52_044)
EXACT_Q = 4
EXACT_EXPONENT = 1


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def show(value: float, digits: int = 17) -> str:
    return format(float(value), f".{digits}g")


def load_base_module():
    spec = importlib.util.spec_from_file_location("tpc355_base_358", BASE_CODE)
    need(spec is not None and spec.loader is not None, "base module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base_module()


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "TPC357 certificate digest")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC357 certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), "TPC357 payload")
    protocol = payload.get("protocol", {})
    need(protocol.get("origins") == [38423, 42010, 45597] and
         protocol.get("counts") == list(COUNTS) and
         protocol.get("q_anchors") == list(Q_ANCHORS) and
         protocol.get("kernel_exponents") == list(EXPONENTS) and
         protocol.get("laws") == list(LAW_NAMES),
         "TPC357 protocol compatibility")
    return payload


def matrix_metrics(matrix: np.ndarray, compute_spectrum: bool
                   ) -> dict[str, Any]:
    symmetry_error = float(np.max(np.abs(matrix - matrix.T)))
    need(math.isfinite(symmetry_error) and symmetry_error <= 1.0e-12,
         "matrix symmetry")
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(schur) and math.isfinite(frobenius) and
         schur > 0 and frobenius > 0, "finite envelope")
    result: dict[str, Any] = {
        "schur_row_sum_bound": show(schur),
        "frobenius_bound": show(frobenius),
        "symmetry_error": show(symmetry_error),
        "spectral_norm": None,
        "minimum_eigenvalue": None,
        "maximum_eigenvalue": None,
        "spectral_over_schur": None,
        "spectral_over_frobenius": None,
    }
    if compute_spectrum:
        eigenvalues = np.linalg.eigvalsh(matrix)
        lo, hi = float(eigenvalues[0]), float(eigenvalues[-1])
        spectral = max(abs(lo), abs(hi))
        need(math.isfinite(spectral) and spectral > 0, "spectrum")
        need(spectral <= schur + BOUND_TOL * max(1.0, schur) and
             spectral <= frobenius + BOUND_TOL * max(1.0, frobenius),
             "finite spectral envelope")
        result.update({
            "spectral_norm": show(spectral),
            "minimum_eigenvalue": show(lo),
            "maximum_eigenvalue": show(hi),
            "spectral_over_schur": show(spectral / schur),
            "spectral_over_frobenius": show(spectral / frobenius),
        })
    return result


def build_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for count in COUNTS:
            values = np.arange(origin, origin + count, dtype=np.int64)
            for q0 in Q_ANCHORS:
                for exponent in EXPONENTS:
                    primes, matrices, geometry = BASE.component_matrices(
                        values, q0, exponent)
                    scale = np.sqrt(geometry[:, None] * geometry[None, :])
                    for law in LAW_NAMES:
                        spectrum = law in SPECTRAL_LAWS
                        normalized = matrices[law] / scale
                        rows.append({
                            "origin": origin,
                            "count": count,
                            "interval": [origin, origin + count - 1],
                            "Q": q0,
                            "kernel_exponent": exponent,
                            "height": HEIGHT,
                            "law": law,
                            "shell": primes,
                            "shell_cardinality": len(primes),
                            "operator_shape": [count, count],
                            "unsigned_geometry_energy_min": show(
                                float(np.min(geometry))),
                            "unsigned_geometry_energy_max": show(
                                float(np.max(geometry))),
                            "unsigned_geometry_spread": show(
                                float(np.max(geometry) / np.min(geometry))),
                            "spectrum_computed": spectrum,
                            "raw_metrics": matrix_metrics(
                                matrices[law], spectrum),
                            "normalized_metrics": matrix_metrics(
                                normalized, spectrum),
                        })
    need(len(rows) == 288, "row census")
    return rows


def summaries(rows: list[dict[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for law in LAW_NAMES:
        selected = [row for row in rows if row["law"] == law]
        need(len(selected) == 72, "law census")
        result[law] = {}
        for family in ("raw_metrics", "normalized_metrics"):
            schur = [float(row[family]["schur_row_sum_bound"])
                     for row in selected]
            frob = [float(row[family]["frobenius_bound"])
                    for row in selected]
            spectral = [float(row[family]["spectral_norm"])
                        for row in selected
                        if row[family]["spectral_norm"] is not None]
            result[law][family] = {
                "rows": len(selected),
                "schur_min": show(min(schur)),
                "schur_max": show(max(schur)),
                "frobenius_min": show(min(frob)),
                "frobenius_max": show(max(frob)),
                "spectral_rows": len(spectral),
                "spectral_min": show(min(spectral)) if spectral else None,
                "spectral_max": show(max(spectral)) if spectral else None,
            }
    return result


def transition_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    source = {(row["origin"], row["count"], row["Q"],
               row["kernel_exponent"]): row
             for row in rows if row["law"] == "all_plus"}
    fields = {
        "raw_spectral": ("raw_metrics", "spectral_norm"),
        "normalized_spectral": ("normalized_metrics", "spectral_norm"),
        "raw_schur": ("raw_metrics", "schur_row_sum_bound"),
        "normalized_schur": ("normalized_metrics", "schur_row_sum_bound"),
    }
    census = {name: {"increase": 0, "decrease": 0, "flat": 0}
              for name in fields}
    extrema = {name: {"largest_increase": -math.inf,
                      "largest_decrease": math.inf}
               for name in fields}
    sequences: list[dict[str, Any]] = []
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                selected = [source[(origin, count, q0, exponent)]
                            for count in COUNTS]
                item: dict[str, Any] = {
                    "origin": origin, "Q": q0,
                    "kernel_exponent": exponent,
                    "counts": list(COUNTS), "metrics": {},
                }
                for name, (family, field) in fields.items():
                    values = [float(row[family][field]) for row in selected]
                    deltas = [values[index + 1] - values[index]
                              for index in range(len(values) - 1)]
                    labels = []
                    for delta in deltas:
                        if delta > SCALE_GUARD:
                            label = "increase"
                        elif delta < -SCALE_GUARD:
                            label = "decrease"
                        else:
                            label = "flat"
                        census[name][label] += 1
                        labels.append(label)
                        extrema[name]["largest_increase"] = max(
                            extrema[name]["largest_increase"], delta)
                        extrema[name]["largest_decrease"] = min(
                            extrema[name]["largest_decrease"], delta)
                    item["metrics"][name] = {
                        "values": [show(value) for value in values],
                        "deltas": [show(delta) for delta in deltas],
                        "classifications": labels,
                    }
                sequences.append(item)
    need(len(sequences) == 18, "sequence census")
    need(all(sum(value.values()) == 54 for value in census.values()),
         "transition census")
    need(census["normalized_spectral"]["increase"] > 0 and
         census["normalized_spectral"]["decrease"] > 0,
         "fresh spectral nonmonotonicity")
    return {
        "guard": show(SCALE_GUARD), "sequences": sequences,
        "census": census,
        "extrema": {name: {key: show(value) for key, value in data.items()}
                    for name, data in extrema.items()},
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = BASE.shell_for(EXACT_Q)
    matrix = [[sum((BASE.exact_entry(prime, u, t, EXACT_EXPONENT)
                    for prime in primes), Fraction(0))
               for t in values] for u in values]
    row_sums = [sum((abs(value) for value in row), Fraction(0))
                for row in matrix]
    geometry = [sum((BASE.exact_entry(prime, u, t, EXACT_EXPONENT) ** 2
                     for prime in primes for t in values), Fraction(0))
                for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "exact symmetry")
    need(all(value > 0 for value in geometry), "exact geometry")

    def text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "shell": primes, "kernel_exponent": EXACT_EXPONENT,
        "matrix_symmetric": True, "geometry_positive": True,
        "row_sums_digest": hashlib.sha256(canonical(
            [text(value) for value in row_sums])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [text(value) for value in geometry])).hexdigest(),
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "TPC355 code"),
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC357 code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC357 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    parent = load_parent_payload()
    rows = build_rows()
    envelope = summaries(rows)
    transitions = transition_audit(rows)
    spectra = [row[family]["spectral_norm"] for row in rows
               for family in ("raw_metrics", "normalized_metrics")
               if row[family]["spectral_norm"] is not None]
    need(len(spectra) == 144, "spectral census")
    normalized_schur_max = max(float(row["normalized_metrics"]
                                     ["schur_row_sum_bound"])
                               for row in rows)
    normalized_spectral_max = max(float(row["normalized_metrics"]
                                        ["spectral_norm"])
                                  for row in rows if row["law"] == "all_plus")
    raw_spectral_max = max(float(row["raw_metrics"]["spectral_norm"])
                           for row in rows if row["law"] == "all_plus")
    parent_audit = parent["finite_audit"]
    parent_schur = float(parent_audit["normalized_schur_max"])
    parent_spectral = float(parent_audit["normalized_all_plus_spectral_max"])
    need(normalized_schur_max < 0.83 and normalized_spectral_max < 0.64,
         "fresh finite caps")
    need(raw_spectral_max > 1500.0, "fresh raw scale witness")
    need(abs(normalized_schur_max - parent_schur) <= PARENT_TRANSFER_TOL and
         abs(normalized_spectral_max - parent_spectral) <= PARENT_TRANSFER_TOL,
         "parent finite cap transfer")
    audit = {
        "rows": len(rows), "origins": len(ORIGINS),
        "all_law_schur_rows": len(rows),
        "all_law_frobenius_rows": len(rows),
        "all_plus_spectral_rows": 72,
        "raw_and_normalized_spectral_metrics": len(spectra),
        "origin_span": ORIGINS[-1] - ORIGINS[0],
        "normalized_schur_max": show(normalized_schur_max),
        "normalized_schur_cap": "0.83",
        "normalized_all_plus_spectral_max": show(normalized_spectral_max),
        "normalized_all_plus_spectral_cap": "0.64",
        "raw_all_plus_spectral_max": show(raw_spectral_max),
        "raw_all_plus_spectral_growth_threshold": "1500",
        "parent_normalized_schur_max": show(parent_schur),
        "parent_normalized_spectral_max": show(parent_spectral),
        "parent_transfer_tolerance": show(PARENT_TRANSFER_TOL),
        "finite_schur_violations": 0,
        "finite_frobenius_violations": 0,
        "normalized_spectral_increase_transitions":
            transitions["census"]["normalized_spectral"]["increase"],
        "normalized_spectral_decrease_transitions":
            transitions["census"]["normalized_spectral"]["decrease"],
        "fixed_power_credit": 0, "arithmetic_advance": "NO",
    }
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "TPC355_code_sha256": BASE_CODE_SHA256,
            "TPC357_code_sha256": PARENT_CODE_SHA256,
            "TPC357_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "origin_rule": "fixed arithmetic spacing: 52001+100000j, j=0,1,2",
            "disjoint_from_tpc356": True,
            "counts": list(COUNTS), "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS), "height": HEIGHT,
            "laws": list(LAW_NAMES), "spectral_laws": list(SPECTRAL_LAWS),
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
            "source_response_used": False,
        },
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "congruence": "Positive finite geometry defines a real symmetric normalized matrix.",
            "scope": "finite declared matrices and parent comparison only",
        },
        "finite_audit": audit,
        "envelope_summaries": envelope,
        "scale_transition_audit": transitions,
        "claim_firewall": {
            "TPC358_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC358_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC358_FRESH_ORIGIN_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC358_PARENT_CAP_TRANSFER": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_NORMALIZED_SCHUR_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_ALL_PLUS_SPECTRAL_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC358_SCALE_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
            "TPC358_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC358_SOURCE_UNIFORM_L2": "OPEN",
            "TPC358_ARITHMETIC_ADVANCE": "NO",
            "TPC358_FIXED_POWER_CREDIT": 0,
            "TPC358_FULL_GATE_B": "OPEN",
            "TPC358_TWIN_PRIME_RESULT": "NONE",
            "TPC358_STRONGEST_OBSTRUCTION": (
                "FINITE_PARENT_CAP_TRANSFER_DOES_NOT_SUPPLY_ORIGIN_UNIFORMITY_"
                "AND_SPECTRAL_DECAY_REMAINS_NONMONOTONE"),
        },
        "exact_anchor": exact_anchor(),
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write_certificate() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored.get("certificate_version") == 1 and
         stored.get("claim_status") == STATUS, "certificate header")
    payload = stored.get("payload")
    need(isinstance(payload, dict) and
         stored.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "payload hash")
    need(payload == build_payload(), "certificate replay")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC358_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            payload = json.loads(RESULT.read_bytes())["payload"]
            audit = payload["finite_audit"]
            print("TPC358_CERTIFICATE=PASS rows=288 spectral_rows=72 "
                  "normalized_schur_max=" + audit["normalized_schur_max"] +
                  " normalized_spectral_max=" +
                  audit["normalized_all_plus_spectral_max"])
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC358_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
