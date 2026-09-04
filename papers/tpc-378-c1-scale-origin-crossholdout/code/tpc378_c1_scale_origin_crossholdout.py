#!/usr/bin/env python3
"""TPC-378: a coordinate-disjoint c=1 scale/origin cross-holdout."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc378_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-377-c1-window-scale-holdout/code/"
    "tpc377_c1_window_scale_holdout.py")
PARENT_CERT = ROOT / (
    "papers/tpc-377-c1-window-scale-holdout/results/"
    "tpc377_certificate.json")

PARENT_CODE_SHA256 = (
    "5200e29c0c26f61cb190de6dfcc186dd3ea80c9b7ebd0dc76b21f712b93ba966")
PARENT_CERT_SHA256 = (
    "2e3061e406a0bb6542b27789411b3518207024f92bcf943ef67afa37b200668c")

SCHEMA = "TPC378_C1_SCALE_ORIGIN_CROSSHOLDOUT_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_SCALE_ORIGIN_CROSSHOLDOUT"
ROUND2_CLUE = "TEST_C1_CROSSHOLDOUT_LAW_CONTROL"

GRID_START = 1_100_001
GRID_STEP = 401
GRID_COUNT = 41
ORIGIN_INDICES = (0, 20, 40)
ORIGINS = tuple(GRID_START + GRID_STEP * i for i in ORIGIN_INDICES)
COUNTS = (1024, 2048)
BLOCK_LENGTH = 256
BLOCK_COUNTS = tuple(n // BLOCK_LENGTH for n in COUNTS)
BAND_CUTOFF = 1
Q_ANCHORS = (512, 2048, 8192)
EXPONENT = 1
BETA = 2
LAW = "all_plus"
HEIGHT = 66
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
EXACT_INTERVAL = (ORIGINS[0], ORIGINS[0] + 13)
EXACT_Q = 4

CLAIM_FIREWALL = {
    "TPC378_SELECTION_PROTOCOL":
        "PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND",
    "TPC378_COORDINATE_DISJOINTNESS": "PROVED_EXACT_FINITE",
    "TPC378_COMMON_BAND_RULE": "PROVED_EXACT_FINITE_INHERITED",
    "TPC378_SCALE_ORIGIN_REPLAY":
        "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
    "TPC378_C1_PROFILE_TRANSFER":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_PARENT_PROFILE_REPLICATION":
        "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_RAYLEIGH_TAIL": "NUMERICALLY_CERTIFIED_FINITE_SCOPED",
    "TPC378_ORIGIN_UNIFORMITY": "OPEN",
    "TPC378_WINDOW_SCALE_UNIFORMITY": "OPEN",
    "TPC378_SPECTRAL_MAGNITUDE_UNIFORMITY": "OPEN",
    "TPC378_CROSS_BLOCK_CAUSALITY": "OPEN",
    "TPC378_NORMALIZATION_SOURCE_VALIDITY": "MODELING_CHOICE_OPEN",
    "TPC378_GROWING_OPERATOR_BOUND": "OPEN",
    "TPC378_SOURCE_UNIFORM_L2": "OPEN",
    "TPC378_ARITHMETIC_ADVANCE": "NO",
    "TPC378_FIXED_POWER_CREDIT": 0,
    "TPC378_FULL_GATE_B": "OPEN",
    "TPC378_TWIN_PRIME_RESULT": "NONE",
}


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


def show(value: float) -> str:
    return format(float(value), ".17g")


def load_parent_module():
    spec = importlib.util.spec_from_file_location("tpc377_parent_for_tpc378",
                                                  PARENT_CODE)
    need(spec is not None and spec.loader is not None, "parent module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PARENT = load_parent_module()


def load_parent_payload() -> dict[str, Any]:
    raw = PARENT_CERT.read_bytes()
    need(digest(raw) == PARENT_CERT_SHA256, "parent certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "parent certificate canonicality")
    payload = document.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") == "TPC377_C1_WINDOW_SCALE_HOLDOUT_V1" and
         payload.get("status") ==
         "NUMERICALLY_CERTIFIED_FINITE_C1_WINDOW_SCALE_HOLDOUT",
         "parent payload")
    return payload


def prior_intervals() -> list[tuple[int, int]]:
    # TPC-376 and TPC-377's largest declared windows, used only for an
    # exact finite coordinate-disjointness check.
    return [(1012006, 1012006 + 2048),
            (1016016, 1016016 + 2048),
            (1022031, 1022031 + 2048)]


def coordinate_disjointness() -> bool:
    current = [(o, o + max(COUNTS)) for o in ORIGINS]
    all_intervals = current + prior_intervals()
    return all(a[1] <= b[0] or b[1] <= a[0]
               for i, a in enumerate(all_intervals)
               for b in all_intervals[i + 1:])


def build_rows() -> list[dict[str, Any]]:
    jobs = [(origin, count, q0)
            for origin in ORIGINS for count in COUNTS for q0 in Q_ANCHORS]

    def one(job):
        # The inherited parent record is the literal c=1 operator.  The
        # origin/count panel is new; the independent checker reconstructs it
        # without importing this module.
        return PARENT.record(*job)

    with ThreadPoolExecutor(max_workers=3) as pool:
        rows = list(pool.map(one, jobs))
    need(len(rows) == 18, "row census")
    return rows


def phase_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_count: list[dict[str, Any]] = []
    for count in COUNTS:
        q_rows = []
        for q0 in Q_ANCHORS:
            setting = [r for r in rows
                       if r["count"] == count and r["Q"] == q0]
            q_rows.append({
                "Q": q0,
                "rows": len(setting),
                "spectral_cap_violations":
                    sum(bool(r["band_failure"]) for r in setting),
                "schur_cap_violations":
                    sum(bool(r["schur_failure"]) for r in setting),
                "spectral_values":
                    [r["band"]["spectral"] for r in setting],
            })
        by_count.append({
            "count": count,
            "block_count": count // BLOCK_LENGTH,
            "rows": sum(r["count"] == count for r in rows),
            "by_Q": q_rows,
            "failure_profile_by_Q": [
                q["spectral_cap_violations"] for q in q_rows],
        })
    retentions = [float(r["mode"]["band_rayleigh_abs_retention"])
                  for r in rows]
    tails = [float(r["mode"]["tail_rayleigh_abs_fraction"])
             for r in rows]
    return {
        "rows": len(rows),
        "band_cutoff": BAND_CUTOFF,
        "band_definition": "block distance <= 1",
        "caps": {"spectral": show(SPECTRAL_CAP),
                 "schur": show(SCHUR_CAP)},
        "spectral_cap_violations": sum(bool(r["band_failure"]) for r in rows),
        "schur_cap_violations": sum(bool(r["schur_failure"]) for r in rows),
        "by_count": by_count,
        "failure_profile_by_count_Q": [
            q["failure_profile_by_Q"] for q in by_count],
        "band_abs_retention_min": show(min(retentions)),
        "band_abs_retention_max": show(max(retentions)),
        "tail_abs_fraction_max": show(max(tails)),
    }


def exact_anchor() -> dict[str, Any]:
    values = list(range(*EXACT_INTERVAL))
    primes = PARENT.PARENT.ENGINE.BASE.shell_for(EXACT_Q)

    def as_text(value: Fraction) -> str:
        return f"{value.numerator}/{value.denominator}"

    matrix: list[list[Fraction]] = []
    geometry: list[Fraction] = []
    for u in values:
        row: list[Fraction] = []
        grow = Fraction(0)
        for t in values:
            total = Fraction(0)
            energy = Fraction(0)
            for prime in primes:
                if u == t or u % prime == 0 or t % prime == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % prime == 0), 1)
                    centered -= Fraction(1, prime - 1)
                    base = (prime * Fraction(HEIGHT * HEIGHT,
                                             HEIGHT * HEIGHT + (u - t) ** 2)
                            * centered)
                weighted = Fraction(prime, EXACT_Q) ** BETA * base
                total += weighted
                energy += weighted * weighted
            row.append(total)
            grow += energy
        matrix.append(row)
        geometry.append(grow)
    need(all(matrix[i][j] == matrix[j][i]
             for i in range(len(values)) for j in range(len(values))),
         "anchor symmetry")
    need(all(value > 0 for value in geometry), "anchor positivity")
    return {
        "interval": list(EXACT_INTERVAL), "Q": EXACT_Q,
        "kernel_exponent": EXPONENT, "beta": BETA, "shell": primes,
        "matrix_symmetric": True, "geometry_positive": True,
        "matrix_digest": hashlib.sha256(canonical([
            [as_text(value) for value in row] for row in matrix])).hexdigest(),
        "geometry_digest": hashlib.sha256(canonical(
            [as_text(value) for value in geometry])).hexdigest(),
    }


def build_payload() -> dict[str, Any]:
    need(PARENT_CODE.is_file() and
         digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    parent = load_parent_payload()
    need(coordinate_disjointness(), "coordinate disjointness")
    rows = build_rows()
    phase = phase_summary(rows)
    expected = [[0, 3, 3], [0, 3, 3]]
    need(phase["failure_profile_by_count_Q"] == expected,
         "crossholdout profile")
    need(phase["spectral_cap_violations"] == 12 and
         phase["schur_cap_violations"] == 0, "crossholdout census")
    return {
        "schema": SCHEMA, "status": STATUS,
        "parent_lock": {
            "parent_code_sha256": PARENT_CODE_SHA256,
            "parent_certificate_sha256": PARENT_CERT_SHA256,
            "parent_schema": parent["schema"],
            "parent_round2_clue": parent["round2_clue"],
            "parent_failure_profile_by_count_Q": [
                [0, 3, 3], [0, 3, 3], [0, 3, 3]],
        },
        "selection_protocol": {
            "grid_start": GRID_START, "grid_step": GRID_STEP,
            "grid_count": GRID_COUNT,
            "candidate_origins": [GRID_START + GRID_STEP * i
                                   for i in range(GRID_COUNT)],
            "origin_indices": list(ORIGIN_INDICES),
            "origins": list(ORIGINS),
            "origin_rule":
                "new coordinate-disjoint affine grid, endpoints fixed before response",
            "counts": list(COUNTS),
            "count_rule": "predeclared endpoint counts 1024 and 2048",
            "block_length": BLOCK_LENGTH,
            "block_counts": list(BLOCK_COUNTS),
            "q_anchors": list(Q_ANCHORS),
            "response_used_for_selection": False,
            "signed_metric_used_for_selection": False,
            "panel_complete_before_metric_read": True,
        },
        "protocol": {
            "origins": list(ORIGINS), "window_counts": list(COUNTS),
            "block_length": BLOCK_LENGTH, "block_counts": list(BLOCK_COUNTS),
            "partition": "nested prefixes with contiguous 256-point blocks",
            "band_cutoff": BAND_CUTOFF,
            "band_definition": "sum of layers with block distance <= 1",
            "q_anchors": list(Q_ANCHORS), "kernel_exponents": [EXPONENT],
            "laws": [LAW], "betas": [BETA], "height": HEIGHT,
            "common_normalization": True, "source_response_used": False,
            "origin_selection_used": False, "count_selection_used": False,
            "row_selection_used": False,
            "mode_rule": "largest absolute eigenvalue; minimum mode wins ties",
        },
        "exact_theorem": {
            "coordinate_disjointness":
                "All declared current and inherited finite intervals are disjoint by integer endpoint inequalities.",
            "common_band_rule":
                "The inherited c=1 block-distance mask defines B1 and T-B1 entrywise at each scale.",
            "scale_relation":
                "The two endpoint counts use the same left endpoint within each new origin.",
            "rayleigh_identity":
                "For the selected full eigenvector, band and tail Rayleigh terms sum to its eigenvalue.",
            "geometry":
                "Each normalization diagonal is a finite sum of nonnegative rational squares.",
        },
        "finite_audit": {
            "rows": len(rows), "origin_count": len(ORIGINS),
            "count_count": len(COUNTS), "q_count": len(Q_ANCHORS),
            "spectral_rows": len(rows),
            "spectral_cap_violations": phase["spectral_cap_violations"],
            "schur_cap_violations": phase["schur_cap_violations"],
            "failure_profile_by_count_Q": phase["failure_profile_by_count_Q"],
            "coordinate_disjoint_from_prior": True,
            "profile_transfer": True,
            "fixed_power_credit": 0, "arithmetic_advance": "NO",
        },
        "phase_summary": phase,
        "rows": rows,
        "row_digest": hashlib.sha256(canonical(rows)).hexdigest(),
        "exact_anchor": exact_anchor(),
        "claim_firewall": CLAIM_FIREWALL,
        "round2_clue": ROUND2_CLUE,
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
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(canonical(build_document()))
            print("TPC378_CERTIFICATE=WRITTEN")
        else:
            raw = RESULT.read_bytes()
            stored = json.loads(raw)
            need(raw == canonical(stored), "certificate canonicality")
            rebuilt = build_document()
            need(stored == rebuilt, "certificate replay")
            audit = rebuilt["payload"]["finite_audit"]
            print("TPC378_CERTIFICATE=PASS rows=" + str(audit["rows"]) +
                  " failures=" + str(audit["spectral_cap_violations"]) +
                  " profiles=" + ";".join(
                      ",".join(str(x) for x in profile)
                      for profile in audit["failure_profile_by_count_Q"]))
        return 0
    except (CheckFailure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC378_CERTIFICATE=FAIL " + str(error), file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
