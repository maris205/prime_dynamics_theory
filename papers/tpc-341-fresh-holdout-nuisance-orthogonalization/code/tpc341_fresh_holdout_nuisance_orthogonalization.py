#!/usr/bin/env python3
"""TPC-341: fresh holdout test for nuisance orthogonalization.

The parent operator and source are fixed.  This release moves to three
non-overlapping, cutoff-safe windows and asks whether a twin-prime response
that is mostly removed by an all-control nuisance projection remains removed
on a held-out control.  The held-out statistic is deliberately descriptive;
it is not an arithmetic cancellation theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc341_certificate.json"
PARENT_PROJECT = ROOT / "papers/tpc-340-schur-frobenius-hybrid-envelope"
PARENT_CODE = PARENT_PROJECT / "code/tpc340_schur_frobenius_hybrid_envelope.py"
PARENT_CERT = PARENT_PROJECT / "results/tpc340_certificate.json"
PARENT_CODE_SHA256 = "218c16d63061f075e580ea3e90b8bc5d07a7bdb925cc7d67540a191f80ab5a8f"
PARENT_CERT_SHA256 = "0dd344ef91a6bc52ea311542223d6f12925b0ccb5322ccdc92ffaaad414be30d"

SCHEMA = "TPC341_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION"
ORIGINS = (48097, 48609, 49217)
SCALES = (1024,)
Q = 54
EXPONENT = 1
HEIGHT = 66
CUTOFF = 50_000
CATEGORIES = ("twin_prime", "non_twin_prime_shift",
               "prime_power_shift", "zero_support")
NUISANCE_CATEGORIES = ("non_twin_prime_shift", "prime_power_shift",
                        "zero_support")
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
NUMERIC_TOL = 8.0e-6
RANK_TOL_FACTOR = 1.0


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


def load_parent() -> Any:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC340 producer provenance")
    need(digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256,
         "TPC340 certificate provenance")
    raw = PARENT_CERT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document) and document.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE",
         "TPC340 certificate header")
    spec = importlib.util.spec_from_file_location("tpc340_parent", PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent import spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.load_parent()


def classify(source: Any, value: int, lam: float, comparison: float) -> str:
    if lam * comparison == 0.0:
        return "zero_support"
    power = source.prime_power(value + 2)
    need(power is not None, "prime-power support")
    if power[1] == 1:
        return "twin_prime" if source.is_prime_small(value) else \
            "non_twin_prime_shift"
    return "prime_power_shift"


def control_indices(size: int, multiplier: int, offset: int) -> np.ndarray:
    if multiplier == -1:
        result = np.arange(size - 1, -1, -1, dtype=np.int64)
    else:
        result = np.asarray([(multiplier * i + offset) % size
                             for i in range(size)], dtype=np.int64)
    need(len(set(int(item) for item in result)) == size, "control bijection")
    return result


def projection_metrics(target: np.ndarray,
                        columns: list[np.ndarray]) -> dict[str, Any]:
    need(len(columns) > 0, "nuisance columns")
    matrix = np.column_stack(columns)
    need(matrix.ndim == 2 and matrix.shape[0] == len(target),
         "nuisance matrix shape")
    basis_all, singular, _ = np.linalg.svd(matrix, full_matrices=False)
    if len(singular) == 0 or singular[0] == 0.0:
        rank = 0
        basis = np.zeros((len(target), 0), dtype=np.float64)
    else:
        tolerance = (RANK_TOL_FACTOR * max(matrix.shape) *
                     np.finfo(np.float64).eps * singular[0])
        rank = int(np.sum(singular > tolerance))
        basis = basis_all[:, :rank]
    projected = basis @ (basis.T @ target) if rank else np.zeros_like(target)
    residual = target - projected
    target_energy = float(target @ target)
    projected_energy = float(projected @ projected)
    residual_energy = float(residual @ residual)
    need(math.isfinite(target_energy) and target_energy > 0.0,
         "nonzero projection target")
    need(math.isfinite(projected_energy) and math.isfinite(residual_energy),
         "projection energy")
    decomposition_gap = target_energy - projected_energy - residual_energy
    need(abs(decomposition_gap) <= NUMERIC_TOL * max(1.0, target_energy),
         "projection Pythagorean identity")
    condition = (float(singular[0] / singular[rank - 1])
                 if rank else math.inf)
    return {
        "target_energy": show(target_energy),
        "projected_energy": show(projected_energy),
        "residual_energy": show(residual_energy),
        "residual_retention": show(residual_energy / target_energy),
        "removed_fraction": show(1.0 - residual_energy / target_energy),
        "decomposition_gap": show(decomposition_gap),
        "nuisance_rank": rank,
        "nuisance_singular_values": [show(item) for item in singular],
        "nuisance_condition": show(condition),
        "identity_holds": True,
    }


def row_record(source: Any, origin: int, scale: int) -> dict[str, Any]:
    lo, hi = origin, origin + scale // 2 - 1
    need(hi + 2 < CUTOFF, "fresh row exceeds parent cutoff")
    values = np.arange(lo, hi + 1, dtype=np.int64)
    lam, comparison, beta, _width = source.source_vectors(lo, hi)
    masks = {name: np.zeros(len(beta), dtype=bool) for name in CATEGORIES}
    for i, value in enumerate(range(lo, hi + 1)):
        masks[classify(source, value, float(lam[i]), float(comparison[i]))][i] = True
    _, matrices = source.coherent_matrices(values, Q, EXPONENT)
    matrix = matrices["all_plus"]
    vectors = {name: beta * masks[name] for name in CATEGORIES}
    outputs = {name: [] for name in CATEGORIES}
    raw_records: list[dict[str, Any]] = []
    for control_name, multiplier, offset, rule in CONTROLS:
        permutation = control_indices(len(beta), multiplier, offset)
        for category in CATEGORIES:
            placed = vectors[category][permutation]
            source_l2 = float(placed @ placed)
            output = matrix @ placed
            response_energy = float(output @ output)
            response_gain = response_energy / source_l2 if source_l2 else 0.0
            outputs[category].append(output)
            raw_records.append({
                "control": control_name, "category": category,
                "support_size": int(np.count_nonzero(placed)),
                "source_l2": show(source_l2),
                "response_energy": show(response_energy),
                "response_gain": show(response_gain),
            })
    means = {category: np.mean(np.stack(outputs[category]), axis=0)
             for category in CATEGORIES}
    nuisance_means = [means[category] for category in NUISANCE_CATEGORIES]
    in_sample = projection_metrics(means["twin_prime"], nuisance_means)
    expected_rank = sum(float(np.linalg.norm(item)) > 0.0
                        for item in nuisance_means)
    need(in_sample["nuisance_rank"] == expected_rank,
         "in-sample nuisance rank")
    holdout: list[dict[str, Any]] = []
    control_names = [item[0] for item in CONTROLS]
    for omitted, (control_name, _, _, _) in enumerate(CONTROLS):
        training = [index for index in range(len(CONTROLS)) if index != omitted]
        training_means = [np.mean(np.stack([outputs[category][index]
                                             for index in training]), axis=0)
                          for category in NUISANCE_CATEGORIES]
        metrics = projection_metrics(outputs["twin_prime"][omitted],
                                     training_means)
        need(metrics["nuisance_rank"] == expected_rank,
             "held-out nuisance rank")
        metrics.update({
            "omitted_control": control_name,
            "training_controls": [control_names[index] for index in training],
        })
        holdout.append(metrics)
    nonempty = [item for item in raw_records if float(item["source_l2"]) > 0.0]
    need(len(raw_records) == 36 and bool(nonempty), "raw record census")
    return {
        "origin": origin, "scale": scale,
        "source_interval": [lo, hi], "source_count": len(beta),
        "cutoff_safe": hi + 2 < CUTOFF,
        "operator": {"law": "all_plus", "Q": Q,
                     "kernel_exponent": EXPONENT, "height": HEIGHT},
        "mask_counts": {name: int(masks[name].sum()) for name in CATEGORIES},
        "raw_records": raw_records,
        "nonempty_raw_record_count": len(nonempty),
        "mean_energies": {name: show(float(means[name] @ means[name]))
                          for name in CATEGORIES},
        "expected_nuisance_rank": expected_rank,
        "in_sample": in_sample,
        "holdout": holdout,
    }


def exact_anchor() -> dict[str, Any]:
    # The orthogonal decomposition is exact for the coordinate nuisance span.
    target = np.asarray([1.0, 1.0, 1.0])
    columns = [np.asarray([1.0, 0.0, 0.0]),
               np.asarray([0.0, 1.0, 0.0])]
    metrics = projection_metrics(target, columns)
    need(metrics["target_energy"] == "3" and
         metrics["projected_energy"] == "2" and
         metrics["residual_energy"] == "1" and
         metrics["residual_retention"] == show(1.0 / 3.0),
         "exact projection anchor")
    return {"target": ["1", "1", "1"],
            "nuisance_columns": [["1", "0", "0"], ["0", "1", "0"]],
            "target_energy": "3", "projected_energy": "2",
            "residual_energy": "1", "residual_retention": show(1.0 / 3.0),
            "identity_exact": True}


def build_payload() -> dict[str, Any]:
    source = load_parent()
    rows = [row_record(source, origin, scale)
            for origin in ORIGINS for scale in SCALES]
    raw = [item for row in rows for item in row["raw_records"]]
    nonempty = [item for item in raw if float(item["source_l2"]) > 0.0]
    in_sample = [row["in_sample"] for row in rows]
    holdout = [item for row in rows for item in row["holdout"]]
    ranks = [row["in_sample"]["nuisance_rank"] for row in rows]
    rank_failures = sum(row["in_sample"]["nuisance_rank"] !=
                        row["expected_nuisance_rank"] for row in rows)
    rank_failures += sum(item["nuisance_rank"] !=
                         row["expected_nuisance_rank"]
                         for row in rows for item in row["holdout"])
    need(len(rows) == 3 and len(raw) == 108 and len(nonempty) == 90 and
         len(in_sample) == 3 and len(holdout) == 27 and rank_failures == 0,
         "global fresh holdout census")
    in_retention = [float(item["residual_retention"]) for item in in_sample]
    hold_retention = [float(item["residual_retention"]) for item in holdout]
    in_condition = [float(item["nuisance_condition"]) for item in in_sample]
    hold_condition = [float(item["nuisance_condition"]) for item in holdout]
    need(max(in_retention) < 0.30 and min(hold_retention) > 0.40,
         "predeclared stability obstruction")
    return {
        "schema": SCHEMA,
        "parent_lock": {"TPC340_producer_sha256": PARENT_CODE_SHA256,
                         "TPC340_certificate_sha256": PARENT_CERT_SHA256},
        "protocol": {
            "origins": list(ORIGINS), "scales": list(SCALES),
            "source_intervals": [[origin, origin + SCALES[0] // 2 - 1]
                                  for origin in ORIGINS],
            "parent_cutoff": CUTOFF,
            "operator": {"law": "all_plus", "Q": Q,
                          "kernel_exponent": EXPONENT, "height": HEIGHT},
            "categories": list(CATEGORIES),
            "nuisance_categories": list(NUISANCE_CATEGORIES),
            "controls": [{"name": name, "multiplier": multiplier,
                          "offset": offset, "rule": rule}
                         for name, multiplier, offset, rule in CONTROLS],
            "in_sample_projection":
                "project nine-control twin mean onto nuisance mean span",
            "holdout_projection":
                "omit one control; train nuisance means on other eight; test omitted twin output",
            "rank_rule": "SVD singular values above max(shape)*eps*sigma_max",
        },
        "exact_theorem": {
            "orthogonal_decomposition":
                "||y||^2=||P_N y||^2+||(I-P_N)y||^2",
            "projection": "P_N is the Euclidean orthogonal projector onto span(N)",
            "finite_scope": "valid for every finite vector and finite nuisance span",
            "arithmetic_interpretation": "none without a growing independent estimate",
        },
        "finite_audit": {
            "rows": 3, "origins": 3, "scales": 1, "controls": 9,
            "categories": 4, "raw_records": 108,
            "nonempty_raw_records": 90,
            "in_sample_projection_records": 3,
            "leave_one_control_out_records": 27,
            "rank_failures": 0,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "summary": {
            "in_sample_retention_min": show(min(in_retention)),
            "in_sample_retention_max": show(max(in_retention)),
            "in_sample_removed_min": show(min(1.0 - value for value in in_retention)),
            "in_sample_removed_max": show(max(1.0 - value for value in in_retention)),
            "holdout_retention_min": show(min(hold_retention)),
            "holdout_retention_max": show(max(hold_retention)),
            "holdout_removed_min": show(min(1.0 - value for value in hold_retention)),
            "holdout_removed_max": show(max(1.0 - value for value in hold_retention)),
            "in_sample_condition_min": show(min(in_condition)),
            "in_sample_condition_max": show(max(in_condition)),
            "holdout_condition_min": show(min(hold_condition)),
            "holdout_condition_max": show(max(hold_condition)),
            "rank_values": sorted(set(ranks)),
            "rank_failures": rank_failures,
            "raw_records": len(raw), "nonempty_raw_records": len(nonempty),
            "holdout_records": len(holdout),
            "in_sample_guard": "retention < 0.30",
            "holdout_guard": "retention > 0.40",
        },
        "exact_anchor": exact_anchor(),
        "claim_firewall": {
            "TPC341_PROJECTION_IDENTITY":
                "PROVED_EXACT_FINITE_DECLARED_MODEL",
            "TPC341_FRESH_HOLDOUT_REPLAY":
                "NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS",
            "TPC341_IN_SAMPLE_PROJECTION":
                "NUMERICALLY_CERTIFIED_FINITE_3_ROWS",
            "TPC341_HOLDOUT_OBSTRUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_27_RECORDS",
            "TPC341_IN_SAMPLE_RETENTION":
                "NUMERICAL_OBSERVATION_0.201_TO_0.256",
            "TPC341_HOLDOUT_RETENTION":
                "NUMERICAL_OBSERVATION_0.444_TO_0.890",
            "TPC341_CONTROL_STABILITY": "REFUTED_SCOPED",
            "TPC341_ARITHMETIC_ADVANCE": "NO",
            "TPC341_FIXED_POWER_CREDIT": 0,
            "TPC341_SOURCE_UNIFORM_L2": "OPEN",
            "TPC341_UNIFORM_MASKED_OPERATOR_BOUND": "OPEN",
            "TPC341_FULL_GATE_B": "OPEN",
            "TPC341_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": "INDEPENDENT_REPRODUCTION_OR_FREEZE_NUISANCE_PROJECTION",
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
            print("TPC341_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            need(stored == document, "TPC341 certificate does not replay")
            print("TPC341_CERTIFICATE=PASS rows=3 controls=9 raw_records=108 "
                  "holdout_records=27 rank_failures=0 exact_anchor=1")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC341_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
