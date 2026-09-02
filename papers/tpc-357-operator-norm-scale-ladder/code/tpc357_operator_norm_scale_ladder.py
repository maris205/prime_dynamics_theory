#!/usr/bin/env python3
"""TPC-357: finite operator-norm scale ladder for TPC-355 normalization.

The experiment freezes the TPC-356 geometry-adversarial origins and extends
the count ladder to 2048.  Every signed matrix receives Schur and Frobenius
envelopes; the all-plus family additionally receives a full symmetric
eigenvalue computation.  This is an operator-only finite audit.  It supplies
neither a growing estimate nor an arithmetic/twin-prime conclusion.
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
    raise SystemExit("TPC357 requires numpy: " + str(error))

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc357_certificate.json"
BASE_CODE = ROOT / (
    "papers/tpc-355-position-aware-mask-energy-normalization/code/"
    "tpc355_position_aware_mask_energy_normalization.py")
PARENT_CODE = ROOT / (
    "papers/tpc-356-geometry-adversarial-normalization-holdout/code/"
    "tpc356_geometry_adversarial_normalization_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-356-geometry-adversarial-normalization-holdout/results/"
    "tpc356_certificate.json")
BASE_CODE_SHA256 = (
    "b54883cbc2e9e19dd8cf6fbece69ff7752ba805678e0b5b2fcf82949dd42fde9")
PARENT_CODE_SHA256 = (
    "1e36e0417fbc6a3f76f459205cd519f9c2420f960c9b17133f27b70de1940244")
PARENT_CERT_SHA256 = (
    "76afe58c8cf13c0cf122c9e167e031fa831335d0ff1cf2597efed9f130ca0ad6")

SCHEMA = "TPC357_OPERATOR_NORM_SCALE_LADDER_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_OPERATOR_NORM_SCALE_LADDER"
ROUND2_CLUE = (
    "ATTACK_THE_FINITE_NORMALIZED_SPECTRAL_CAP_ON_A_PREREGISTERED_FRESH_"
    "ORIGIN_SCALE_HOLDOUT_BEFORE_ANY_UNIFORM_CLAIM")

ORIGINS = (38423, 42010, 45597)
COUNTS = (256, 512, 1024, 2048)
Q_ANCHORS = (24, 54, 80)
EXPONENTS = (1, 2)
LAW_NAMES = ("all_plus", "alternating_index", "mod4_character", "half_split")
HEIGHT = 66
SPECTRAL_LAWS = ("all_plus",)
SCALE_GUARD = 1.0e-6
SYMMETRY_TOL = 1.0e-12
BOUND_TOL = 2.0e-10
EXACT_INTERVAL = (38431, 38444)
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
    spec = importlib.util.spec_from_file_location("tpc355_base", BASE_CODE)
    need(spec is not None and spec.loader is not None, "base module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_base_module()


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "TPC356 certificate digest")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC356 certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict), "TPC356 payload")
    protocol = payload.get("protocol", {})
    need(protocol.get("selected_origins") == list(ORIGINS),
         "TPC356 selected origins")
    return payload


def matrix_metrics(matrix: np.ndarray, compute_spectrum: bool
                   ) -> dict[str, Any]:
    symmetry_error = float(np.max(np.abs(matrix - matrix.T)))
    need(math.isfinite(symmetry_error) and symmetry_error <= SYMMETRY_TOL,
         "matrix symmetry")
    absolute = np.abs(matrix)
    schur = float(np.max(np.sum(absolute, axis=1)))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(math.isfinite(schur) and math.isfinite(frobenius) and
         schur > 0 and frobenius > 0, "finite positive envelopes")
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
        lo = float(eigenvalues[0])
        hi = float(eigenvalues[-1])
        spectral = max(abs(lo), abs(hi))
        need(math.isfinite(spectral) and spectral > 0, "spectral norm")
        need(spectral <= schur + BOUND_TOL * max(1.0, schur),
             "Schur spectral envelope")
        need(spectral <= frobenius + BOUND_TOL * max(1.0, frobenius),
             "Frobenius spectral envelope")
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
                        normalized = matrices[law] / scale
                        spectral = law in SPECTRAL_LAWS
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
                            "spectrum_computed": spectral,
                            "raw_metrics": matrix_metrics(
                                matrices[law], spectral),
                            "normalized_metrics": matrix_metrics(
                                normalized, spectral),
                        })
    need(len(rows) == 288, "row census")
    return rows


def envelope_summaries(rows: list[dict[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for law in LAW_NAMES:
        selected = [row for row in rows if row["law"] == law]
        need(len(selected) == 72, "law census")
        output[law] = {}
        for metric_name in ("raw_metrics", "normalized_metrics"):
            schur = [float(row[metric_name]["schur_row_sum_bound"])
                     for row in selected]
            frob = [float(row[metric_name]["frobenius_bound"])
                    for row in selected]
            spectral = [float(row[metric_name]["spectral_norm"])
                        for row in selected
                        if row[metric_name]["spectral_norm"] is not None]
            output[law][metric_name] = {
                "rows": len(selected),
                "schur_min": show(min(schur)),
                "schur_max": show(max(schur)),
                "frobenius_min": show(min(frob)),
                "frobenius_max": show(max(frob)),
                "spectral_rows": len(spectral),
                "spectral_min": show(min(spectral)) if spectral else None,
                "spectral_max": show(max(spectral)) if spectral else None,
            }
    return output


def transition_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    all_plus = {(row["origin"], row["count"], row["Q"],
                 row["kernel_exponent"]): row
                for row in rows if row["law"] == "all_plus"}
    sequences: list[dict[str, Any]] = []
    counters = {name: {"increase": 0, "decrease": 0, "flat": 0}
                for name in ("raw_spectral", "normalized_spectral",
                             "raw_schur", "normalized_schur")}
    extrema = {name: {"largest_increase": -math.inf,
                      "largest_decrease": math.inf}
               for name in counters}
    fields = {
        "raw_spectral": ("raw_metrics", "spectral_norm"),
        "normalized_spectral": ("normalized_metrics", "spectral_norm"),
        "raw_schur": ("raw_metrics", "schur_row_sum_bound"),
        "normalized_schur": ("normalized_metrics", "schur_row_sum_bound"),
    }
    for origin in ORIGINS:
        for q0 in Q_ANCHORS:
            for exponent in EXPONENTS:
                selected = [all_plus[(origin, count, q0, exponent)]
                            for count in COUNTS]
                record: dict[str, Any] = {
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
                        counters[name][label] += 1
                        labels.append(label)
                        extrema[name]["largest_increase"] = max(
                            extrema[name]["largest_increase"], delta)
                        extrema[name]["largest_decrease"] = min(
                            extrema[name]["largest_decrease"], delta)
                    record["metrics"][name] = {
                        "values": [show(value) for value in values],
                        "deltas": [show(delta) for delta in deltas],
                        "classifications": labels,
                    }
                sequences.append(record)
    need(len(sequences) == 18, "sequence census")
    need(all(sum(item.values()) == 54 for item in counters.values()),
         "transition census")
    need(counters["normalized_spectral"]["increase"] > 0 and
         counters["normalized_spectral"]["decrease"] > 0,
         "normalized spectral nonmonotonicity witness")
    return {
        "guard": show(SCALE_GUARD),
        "sequences": sequences,
        "census": counters,
        "extrema": {name: {key: show(value) for key, value in data.items()}
                    for name, data in extrema.items()},
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(EXACT_INTERVAL[0], EXACT_INTERVAL[1] + 1))
    primes = BASE.shell_for(EXACT_Q)
    matrix = [[sum((BASE.exact_entry(prime, u, t, EXACT_EXPONENT)
                    for prime in primes), Fraction(0))
               for t in values] for u in values]
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "exact symmetry")
    row_sums = [sum((abs(value) for value in row), Fraction(0))
                for row in matrix]
    frobenius_sq = sum((value * value for row in matrix for value in row),
                       Fraction(0))
    geometry = [sum((BASE.exact_entry(prime, u, t, EXACT_EXPONENT) ** 2
                     for prime in primes for t in values), Fraction(0))
                for u in values]
    need(all(value > 0 for value in geometry), "exact geometry positivity")

    def fraction_text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    return {
        "interval": list(EXACT_INTERVAL),
        "Q": EXACT_Q,
        "shell": primes,
        "kernel_exponent": EXACT_EXPONENT,
        "matrix_symmetric": True,
        "geometry_positive": True,
        "raw_schur_bound": fraction_text(max(row_sums)),
        "raw_frobenius_square": fraction_text(frobenius_sq),
        "row_sums_digest": hashlib.sha256(canonical(
            [fraction_text(value) for value in row_sums])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [fraction_text(value) for value in geometry])).hexdigest(),
        "finite_schur_theorem": (
            "For every finite real symmetric matrix T, ||T||_2 is at most "
            "max_u sum_t |T(u,t)|; independently, ||T||_2<=||T||_F."),
    }


def build_payload() -> dict[str, Any]:
    for path, expected, label in (
            (BASE_CODE, BASE_CODE_SHA256, "TPC355 code"),
            (PARENT_CODE, PARENT_CODE_SHA256, "TPC356 code"),
            (PARENT_CERT, PARENT_CERT_SHA256, "TPC356 certificate")):
        need(path.is_file() and digest(path.read_bytes()) == expected,
             label + " provenance")
    load_parent_payload()
    rows = build_rows()
    summaries = envelope_summaries(rows)
    transitions = transition_audit(rows)
    all_metrics = [row[family] for row in rows
                   for family in ("raw_metrics", "normalized_metrics")]
    spectral_metrics = [item for item in all_metrics
                        if item["spectral_norm"] is not None]
    need(len(spectral_metrics) == 144, "spectral metric census")
    normalized_schur_max = max(float(row["normalized_metrics"]
                                     ["schur_row_sum_bound"])
                               for row in rows)
    normalized_spectral_max = max(float(row["normalized_metrics"]
                                        ["spectral_norm"])
                                  for row in rows
                                  if row["law"] == "all_plus")
    raw_spectral_max = max(float(row["raw_metrics"]["spectral_norm"])
                           for row in rows if row["law"] == "all_plus")
    need(normalized_schur_max < 0.83, "finite normalized Schur cap")
    need(normalized_spectral_max < 0.64, "finite normalized spectral cap")
    need(raw_spectral_max > 1500.0, "raw spectral growth witness")
    audit = {
        "rows": len(rows),
        "all_law_schur_rows": len(rows),
        "all_law_frobenius_rows": len(rows),
        "all_plus_spectral_rows": 72,
        "raw_and_normalized_spectral_metrics": len(spectral_metrics),
        "normalized_schur_max": show(normalized_schur_max),
        "normalized_schur_cap": "0.83",
        "normalized_all_plus_spectral_max": show(normalized_spectral_max),
        "normalized_all_plus_spectral_cap": "0.64",
        "raw_all_plus_spectral_max": show(raw_spectral_max),
        "raw_all_plus_spectral_growth_threshold": "1500",
        "finite_schur_violations": 0,
        "finite_frobenius_violations": 0,
        "normalized_spectral_increase_transitions":
            transitions["census"]["normalized_spectral"]["increase"],
        "normalized_spectral_decrease_transitions":
            transitions["census"]["normalized_spectral"]["decrease"],
        "fixed_power_credit": 0,
        "arithmetic_advance": "NO",
    }
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "parent_lock": {
            "TPC355_code_sha256": BASE_CODE_SHA256,
            "TPC356_code_sha256": PARENT_CODE_SHA256,
            "TPC356_certificate_sha256": PARENT_CERT_SHA256,
        },
        "protocol": {
            "origins": list(ORIGINS),
            "source_of_origins": "TPC-356 frozen geometry-adversarial selection",
            "counts": list(COUNTS),
            "q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "height": HEIGHT,
            "laws": list(LAW_NAMES),
            "spectral_laws": list(SPECTRAL_LAWS),
            "operator": "literal deleted-diagonal two-endpoint divisibility-masked shell operator",
            "normalization": "TPC-355 unsigned mask-energy symmetric congruence",
            "source_response_used": False,
        },
        "exact_theorem": {
            "schur": "For finite real symmetric T, ||T||_2 <= max_u sum_t |T(u,t)|.",
            "frobenius": "For finite real T, ||T||_2 <= ||T||_F.",
            "congruence": "Positive finite geometry defines a real symmetric normalized matrix.",
            "scope": "finite declared matrices only",
        },
        "finite_audit": audit,
        "envelope_summaries": summaries,
        "scale_transition_audit": transitions,
        "claim_firewall": {
            "TPC357_FINITE_SCHUR_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC357_FINITE_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC357_OPERATOR_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_288_ROWS",
            "TPC357_NORMALIZED_SCHUR_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC357_ALL_PLUS_SPECTRAL_CAP": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
            "TPC357_SCALE_MONOTONE_DECAY": "REFUTED_SCOPED_ON_DECLARED_LADDER",
            "TPC357_GROWING_OPERATOR_BOUND": "OPEN",
            "TPC357_SOURCE_UNIFORM_L2": "OPEN",
            "TPC357_ARITHMETIC_ADVANCE": "NO",
            "TPC357_FIXED_POWER_CREDIT": 0,
            "TPC357_FULL_GATE_B": "OPEN",
            "TPC357_TWIN_PRIME_RESULT": "NONE",
            "TPC357_STRONGEST_OBSTRUCTION": (
                "FINITE_CAP_HAS_NO_ORIGIN_UNIFORM_OR_GROWING_SCALE_PROOF_"
                "AND_NORMALIZED_SPECTRAL_DECAY_IS_NOT_MONOTONE"),
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
            print("TPC357_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            payload = json.loads(RESULT.read_bytes())["payload"]
            audit = payload["finite_audit"]
            print("TPC357_CERTIFICATE=PASS rows=288 spectral_rows=72 "
                  "normalized_schur_max=" + audit["normalized_schur_max"] +
                  " normalized_spectral_max=" +
                  audit["normalized_all_plus_spectral_max"])
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            TypeError, KeyError, np.linalg.LinAlgError) as error:
        print("TPC357_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
