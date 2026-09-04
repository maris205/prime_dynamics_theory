#!/usr/bin/env python3
"""Independent reverse-order replay for the TPC-387 count-ladder certificate."""

from __future__ import annotations

import hashlib
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
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-387-c1-count-ladder-renormalization"
CERTIFICATE = PROJECT / "results/tpc387_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-386-c1-count-holdout-bandwidth/code/"
    "tpc386_c1_count_holdout_bandwidth.py")
PARENT_CERT = ROOT / (
    "papers/tpc-386-c1-count-holdout-bandwidth/results/"
    "tpc386_certificate.json")
PARENT_CODE_SHA256 = "24df166dee0b54f6503eb5dd03385e0702bb474ad0737a28c081a7d0dc1be006"
PARENT_CERT_SHA256 = "4f34aee5970006efce06586c90ad599a7b484fdb9fea3921ffcfab7560d2a285"
CERTIFICATE_SHA256 = "337aa65feedd4c729cd34c7d6de8865baeb96c4888ab44fbdf00f840d079e344"
SCHEMA = "TPC387_C1_COUNT_LADDER_RENORMALIZATION_V1"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_C1_COUNT_LADDER_RENORMALIZATION"
ROUND2_CLUE = "TEST_C1_COUNT_LADDER_SECOND_HOLDOUT"
ORIGINS = (2400001, 2404011, 2408021, 2412031, 2416041)
CALIBRATION_ORIGINS = (2400001, 2404011, 2408021)
HOLDOUT_ORIGINS = (2412031, 2416041)
CALIBRATION_COUNTS = (512, 768)
HOLDOUT_COUNT = 1024
BLOCK_LENGTH = 128
BAND_MODES = ("fixed_c3", "full_relative")
QS = (2048, 8192)
EXPONENT = 1
BETA = 2
HEIGHT = 66
LAWS = ("all_plus", "alternating_index", "mod4_character", "half_split")
NORMS = ("local_diagonal", "pooled_train_scalar")
SPREAD_CAP = 0.01
SPECTRAL_CAP = 0.64
SCHUR_CAP = 0.83
RENORM_ERROR_CAP = 0.03


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


def close(actual: float, recorded: Any, label: str,
          tolerance: float = 8e-8) -> None:
    try:
        target = float(recorded)
    except (TypeError, ValueError) as error:
        raise Failure(label + " nonnumeric") from error
    need(math.isfinite(actual) and math.isfinite(target) and
         abs(actual - target) <= tolerance * max(1.0, abs(actual), abs(target)),
         label + " mismatch")


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\x00" * (
                ((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


PRIMES = sieve(20000)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def sign(law: str, index: int, prime: int, cardinality: int) -> float:
    if law == "all_plus":
        return 1.0
    if law == "alternating_index":
        return 1.0 if index % 2 == 0 else -1.0
    if law == "mod4_character":
        return 1.0 if prime % 4 == 1 else -1.0
    return 1.0 if index < cardinality / 2 else -1.0


def pack(origin: int, count: int, q0: int):
    values = np.arange(origin, origin + count, dtype=np.int64)
    difference = values[:, None] - values[None, :]
    kernel = float(HEIGHT * HEIGHT) / (
        HEIGHT * HEIGHT + difference.astype(np.float64) ** 2)
    np.fill_diagonal(kernel, 0.0)
    primes = shell(q0)
    matrices = {law: np.zeros((count, count), dtype=np.float64)
                for law in LAWS}
    geometry = np.zeros(count, dtype=np.float64)
    # Reverse prime order intentionally differs from the producer.
    for index, p in reversed(tuple(enumerate(primes))):
        centered = ((difference % p == 0).astype(np.float64) - 1.0 / (p - 1))
        np.fill_diagonal(centered, 0.0)
        valid = ((difference != 0) & (values[:, None] % p != 0) &
                 (values[None, :] % p != 0))
        block = (float(p) / float(q0)) ** BETA * float(p) * kernel * centered * valid
        geometry += np.sum(block * block, axis=1)
        for law in LAWS:
            matrices[law] += sign(law, index, p, len(primes)) * block
    for law in LAWS:
        matrices[law] = (matrices[law] + matrices[law].T) / 2.0
    need(bool(np.all(np.isfinite(geometry) & (geometry > 0))), "geometry")
    return primes, matrices, geometry


def metric(matrix: np.ndarray) -> tuple[float, float, float, float]:
    symmetry = float(np.max(np.abs(matrix - matrix.T)))
    schur = float(np.max(np.sum(np.abs(matrix), axis=1)))
    eig = np.linalg.eigvalsh(matrix)
    spectral = max(abs(float(eig[0])), abs(float(eig[-1])))
    frobenius = float(np.sqrt(np.sum(matrix * matrix)))
    need(symmetry <= 2e-12 and schur > 0 and frobenius > 0 and
         math.isfinite(spectral) and spectral <= schur + 1e-8 and
         spectral <= frobenius + 1e-8, "metric envelope")
    return spectral, schur, frobenius, symmetry


def band(mode: str, count: int) -> np.ndarray:
    blocks = count // BLOCK_LENGTH
    cutoff = 3 if mode == "fixed_c3" else blocks - 1
    ids = np.arange(count) // BLOCK_LENGTH
    return np.abs(ids[:, None] - ids[None, :]) <= cutoff


def replay() -> tuple[dict[tuple[int, int, int, str, str, str], tuple[float, ...]],
                       dict[int, dict[int, float]]]:
    actual: dict[tuple[int, int, int, str, str, str], tuple[float, ...]] = {}
    scalars: dict[int, dict[int, float]] = {}
    for q0 in QS:
        packs = {}
        for origin in CALIBRATION_ORIGINS:
            for count in CALIBRATION_COUNTS:
                packs[origin, count] = pack(origin, count, q0)
        for origin in HOLDOUT_ORIGINS:
            packs[origin, HOLDOUT_COUNT] = pack(origin, HOLDOUT_COUNT, q0)
        train = {count: float(np.mean([packs[o, count][2].mean()
                                       for o in CALIBRATION_ORIGINS])
                              ) for count in CALIBRATION_COUNTS}
        gamma = math.log(train[768] / train[512]) / math.log(1.5)
        extrapolated = train[768] * (1024.0 / 768.0) ** gamma
        scalars[q0] = {512: train[512], 768: train[768], 1024: extrapolated}
        for (origin, count), (primes, matrices, geometry) in packs.items():
            if count == 512:
                pooled = train[512]
            elif count == 768:
                pooled = train[768]
            else:
                pooled = extrapolated
            for mode in BAND_MODES:
                mask = band(mode, count)
                for norm in NORMS:
                    for law in LAWS:
                        normalized = (matrices[law] /
                                      np.sqrt(geometry[:, None] * geometry[None, :])
                                      if norm == "local_diagonal" else
                                      matrices[law] / pooled)
                        actual[(origin, count, q0, law, norm, mode)] = metric(
                            np.where(mask, normalized, 0.0))
    need(len(actual) == 256, "replay row count")
    return actual, scalars


def stat(values: list[float]) -> dict[str, Any]:
    need(len(values) >= 2 and all(math.isfinite(x) and x >= 0 for x in values),
         "stats")
    lo, hi = min(values), max(values)
    mean = sum(values) / len(values)
    spread = (hi - lo) / mean if mean else float("inf")
    return {"value_count": len(values), "minimum": lo, "maximum": hi,
            "mean": mean, "relative_spread": spread,
            "within_one_percent": spread <= SPREAD_CAP, "values": values}


def expected_cells(actual: dict[tuple[int, int, int, str, str, str], tuple[float, ...]]):
    cells = []
    for mode in BAND_MODES:
        for norm in NORMS:
            for law in LAWS:
                for q in QS:
                    by_count = {
                        count: [actual[(o, count, q, law, norm, mode)][0]
                                for o in (CALIBRATION_ORIGINS if count != 1024
                                          else HOLDOUT_ORIGINS)]
                        for count in (512, 768, 1024)
                    }
                    s512, s768, s1024 = (stat(by_count[n])
                                          for n in (512, 768, 1024))
                    m512, m768, m1024 = (x["mean"] for x in (s512, s768, s1024))
                    alpha = math.log(m768 / m512) / math.log(1.5)
                    prediction = m768 * (1024.0 / 768.0) ** alpha
                    ratio = m1024 / prediction
                    cells.append((mode, norm, law, q, s512, s768, s1024,
                                  alpha, prediction, ratio))
    return cells


def anchor_digests() -> tuple[str, dict[str, str]]:
    values = list(range(ORIGINS[0], ORIGINS[0] + 13))
    primes = shell(8)
    matrices: dict[str, list[list[Fraction]]] = {law: [] for law in LAWS}
    geometry: list[Fraction] = []
    for u in values:
        row_values = {law: [] for law in LAWS}
        grow = Fraction(0)
        for t in values:
            components = []
            for p in primes:
                if u == t or u % p == 0 or t % p == 0:
                    base = Fraction(0)
                else:
                    centered = Fraction(int((u - t) % p == 0), 1) - Fraction(1, p - 1)
                    base = (p * Fraction(p, 8) ** BETA *
                            Fraction(HEIGHT * HEIGHT,
                                     HEIGHT * HEIGHT + (u - t) ** 2) * centered)
                components.append(base)
            grow += sum(x * x for x in components)
            for law in LAWS:
                row_values[law].append(sum(
                    Fraction(1 if sign(law, i, p, len(primes)) > 0 else -1) * x
                    for i, (p, x) in enumerate(zip(primes, components))))
        geometry.append(grow)
        for law in LAWS:
            matrices[law].append(row_values[law])

    def txt(x: Fraction) -> str:
        return f"{x.numerator}/{x.denominator}"

    return (hashlib.sha256(canonical([txt(x) for x in geometry])).hexdigest(),
            {law: hashlib.sha256(canonical([
                [txt(x) for x in row] for row in matrix
            ])).hexdigest() for law, matrix in matrices.items()})


def load_target() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes()
    need(CERTIFICATE_SHA256 != "TO_BE_FILLED" and digest(raw) == CERTIFICATE_SHA256,
         "certificate provenance")
    doc = json.loads(raw)
    need(raw == canonical(doc), "certificate canonicality")
    need(doc.get("certificate_version") == 1 and doc.get("claim_status") == STATUS,
         "header")
    payload = doc.get("payload")
    need(isinstance(payload, dict) and payload.get("schema") == SCHEMA and
         payload.get("status") == STATUS, "schema")
    need(doc.get("payload_sha256") == hashlib.sha256(canonical(payload)).hexdigest(),
         "payload hash")
    parent = payload.get("parent_lock", {})
    need(parent.get("parent_code_sha256") == PARENT_CODE_SHA256 and
         parent.get("parent_certificate_sha256") == PARENT_CERT_SHA256 and
         parent.get("forecast_is_fitted") is False, "parent lock")
    selection = payload.get("selection_protocol", {})
    need(selection.get("origins") == list(ORIGINS) and
         selection.get("calibration_origins") == list(CALIBRATION_ORIGINS) and
         selection.get("holdout_origins") == list(HOLDOUT_ORIGINS) and
         selection.get("calibration_counts") == [512, 768] and
         selection.get("holdout_count") == 1024 and
         selection.get("band_modes") == list(BAND_MODES) and
         selection.get("q_anchors") == list(QS) and
         selection.get("laws") == list(LAWS) and
         selection.get("normalizations") == list(NORMS) and
         selection.get("response_used_for_selection") is False and
         selection.get("metric_used_for_selection") is False and
         selection.get("slope_fit_uses_holdout") is False, "selection")
    rows = payload.get("rows")
    need(isinstance(rows, list) and len(rows) == 256, "rows")
    expected = ({(o, n, q, law, norm, mode)
                 for o in CALIBRATION_ORIGINS for n in CALIBRATION_COUNTS
                 for q in QS for law in LAWS for norm in NORMS
                 for mode in BAND_MODES} |
                {(o, HOLDOUT_COUNT, q, law, norm, mode)
                 for o in HOLDOUT_ORIGINS for q in QS for law in LAWS
                 for norm in NORMS for mode in BAND_MODES})
    observed = {(r.get("origin"), r.get("count"), r.get("Q"), r.get("law"),
                 r.get("normalization"), r.get("band_mode")) for r in rows}
    need(observed == expected, "row keys")
    for row in rows:
        expected_count = (512 if row["origin"] in CALIBRATION_ORIGINS and
                          row["count"] == 512 else
                          768 if row["origin"] in CALIBRATION_ORIGINS and
                          row["count"] == 768 else 1024)
        need(row.get("count") == expected_count and
             row.get("origin_role") ==
             (f"calibration_{row['count']}" if row["origin"] in CALIBRATION_ORIGINS
              else "holdout_1024"), "row role")
    summary = payload.get("ladder_summary", {})
    need(summary.get("row_count") == 256 and summary.get("cell_count") == 32 and
         summary.get("renorm_pass_count_all_cells") == 32 and
         isinstance(summary.get("cells"), list) and len(summary["cells"]) == 32 and
         isinstance(summary.get("forecast_summary_all_plus_Q8192"), list) and
         len(summary["forecast_summary_all_plus_Q8192"]) == 4, "summary")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 256 and audit.get("cell_count") == 32 and
         audit.get("calibration_counts") == [512, 768] and
         audit.get("holdout_count") == 1024 and
         audit.get("coordinate_disjoint_from_prior") is True and
         audit.get("arithmetic_advance") == "NO" and
         audit.get("fixed_power_credit") == 0, "audit")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC387_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC387_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC387_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC387_TWIN_PRIME_RESULT") == "NONE", "firewall")
    need(payload.get("round2_clue") == ROUND2_CLUE, "clue")
    return payload


def verify() -> dict[str, Any]:
    target = load_target()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256 and
         digest(PARENT_CERT.read_bytes()) == PARENT_CERT_SHA256, "parent files")
    actual, scalars = replay()
    rows = target["rows"]
    recorded = {(r["origin"], r["count"], r["Q"], r["law"],
                 r["normalization"], r["band_mode"]): r for r in rows}
    for key, values in actual.items():
        row = recorded.get(key)
        need(row is not None, "missing row")
        for value, field in zip(values, ("band_spectral", "band_schur",
                                          "band_frobenius", "symmetry_error")):
            close(value, row[field], field + repr(key))
        origin, count, q, law, norm, mode = key
        pooled = 1.0 if norm == "local_diagonal" else scalars[q][count]
        close(pooled, row["pooled_scalar_used"], "pooled scalar" + repr(key))
    cells = {(x["band_mode"], x["normalization"], x["law"], x["Q"]): x
             for x in target["ladder_summary"]["cells"]}
    need(len(cells) == 32, "cell keys")
    computed = expected_cells(actual)
    for mode, norm, law, q, s512, s768, s1024, alpha, prediction, ratio in computed:
        item = cells[(mode, norm, law, q)]
        for section, expected_stat in (("N512", s512), ("N768", s768),
                                       ("N1024_holdout", s1024)):
            rec = item[section]
            for field in ("minimum", "maximum", "mean", "relative_spread"):
                close(expected_stat[field], rec[field], section + field)
            need(rec["value_count"] == expected_stat["value_count"] and
                 rec["within_one_percent"] is expected_stat["within_one_percent"],
                 section + " flag")
        close(alpha, item["calibration_log2_slope"], "slope")
        close(prediction, item["predicted_N1024_mean"], "prediction")
        close(ratio, item["holdout_to_prediction_ratio"], "ratio")
        close(ratio - 1.0, item["renormalized_error"], "renormalized error")
        need(math.isfinite(float(item["renormalized_holdout_mean"])),
             "renormalized finite")
        need(item["within_renorm_error_cap"] is
             (abs(ratio - 1.0) <= RENORM_ERROR_CAP), "renorm flag")
    summary = target["ladder_summary"]
    need(summary["stable_N512_cells"] == sum(
        x[4]["within_one_percent"] for x in computed), "N512 census")
    need(summary["stable_N768_cells"] == sum(
        x[5]["within_one_percent"] for x in computed), "N768 census")
    need(summary["stable_N1024_holdout_cells"] == sum(
        x[6]["within_one_percent"] for x in computed), "holdout census")
    for key, counts in summary["failure_counts_by_mode_normalization"].items():
        mode = next((m for m in BAND_MODES if key.startswith(m + "_")), None)
        need(mode is not None, "failure mode")
        norm = key[len(mode) + 1:]
        subset = [r for k, r in recorded.items() if k[5] == mode and k[4] == norm]
        need(counts["spectral"] == sum(bool(r["spectral_failure"]) for r in subset) and
             counts["schur"] == sum(bool(r["schur_failure"]) for r in subset),
             "failure census")
    forecasts = {(x["band_mode"], x["normalization"]): x
                 for x in summary["forecast_summary_all_plus_Q8192"]}
    need(len(forecasts) == 4, "forecast census")
    for mode in BAND_MODES:
        for norm in NORMS:
            item = forecasts[(mode, norm)]
            cell = cells[(mode, norm, "all_plus", 8192)]
            close(float(cell["N1024_holdout"]["mean"]),
                  item["N1024_holdout"]["mean"], "forecast hold")
            close(float(cell["N512"]["mean"]), item["N512"]["mean"],
                  "forecast cal512")
            close(float(cell["N768"]["mean"]), item["N768"]["mean"],
                  "forecast cal768")
            close(float(cell["predicted_N1024_mean"]), item["predicted_N1024_mean"], "forecast pred")
            close(float(cell["holdout_to_prediction_ratio"]), item["holdout_to_prediction_ratio"], "forecast ratio")
            need(item["within_renorm_error_cap"] is
                 (abs(float(cell["holdout_to_prediction_ratio"]) - 1.0) <= RENORM_ERROR_CAP),
                 "forecast flag")
    geom = target["geometry_scalar_summary"]
    for q, values in scalars.items():
        close(values[512], geom[str(q)]["by_calibration_count"]["512"], "geometry512")
        close(values[768], geom[str(q)]["by_calibration_count"]["768"], "geometry768")
        close(values[1024], geom[str(q)]["extrapolated_1024"], "geometry1024")
    geometry_hash, matrix_hashes = anchor_digests()
    anchor = target["exact_anchor"]
    need(anchor.get("interval") == [2400001, 2400014] and
         anchor.get("Q") == 8 and anchor.get("shell") == [11, 13] and
         anchor.get("geometry_positive") is True and
         anchor.get("geometry_digest") == geometry_hash and
         anchor.get("law_matrix_digests") == matrix_hashes, "anchor")
    return target


def main() -> int:
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("explicit --check is required")
    try:
        target = verify()
        summary = target["ladder_summary"]
        failures = sum(v["spectral"] for v in
                       summary["failure_counts_by_mode_normalization"].values())
        print("TPC387_INDEPENDENT_CHECK=PASS rows=256 cells=32 "
              f"renorm_pass={summary['renorm_pass_count_all_cells']}/32 "
              f"spectral_failures={failures} "
              f"stable_holdout={summary['stable_N1024_holdout_cells']}/32")
        return 0
    except (Failure, OSError, ValueError, TypeError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC387_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
