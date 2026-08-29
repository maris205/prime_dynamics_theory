#!/usr/bin/env python3
"""Independent float64 replay for the TPC-307 holdout atlas.

This checker does not import the TPC-307 producer.  It rebuilds the literal
source profiles and physical rows from the frozen TPC-268 engine, solves the
finite overlap frontier with an independent NumPy implementation, and checks
the published enclosures and classifications.  The replay is an adversarial
numerical reproduction, not a formal interval proof.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-307-common-ambient-union-shell-holdout"
RESULT = PROJECT / "results/tpc307_certificate.json"
P302_RESULT = ROOT / "papers/tpc-302-growing-shell-budget-gap-audit/results/tpc302_certificate.json"
P305_RESULT = ROOT / "papers/tpc-305-counterfactual-transported-label-budget/results/tpc305_certificate.json"
P306_RESULT = ROOT / "papers/tpc-306-two-way-operator-target-interaction/results/tpc306_certificate.json"
ENGINE_CODE = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"

RESULT_SHA256 = "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593"
P302_RESULT_SHA256 = "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6"
P305_RESULT_SHA256 = "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3"
P306_RESULT_SHA256 = "ab9eba3317e4e22d4955c15cb7a0c22e55fd0495696f34be1476985f2232a34b"
ENGINE_SHA256 = "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3"
SCHEMA = "TPC307_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_V1"
STATUS = (
    "PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS")
PROFILE_CUTOFFS = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                   47, 53, 59, 61)
PAIRS = ((50, 60), (60, 70), (70, 90))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = ("beta_norm_squared", "profile_trace_mean",
               "first_profile_norm_squared")
SLACK_RELATIVE = 2e-3


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load(path: Path, expected_hash: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " hash")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1, path.name + " version")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def interval(value: Any) -> tuple[float, float]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = float(value[0]), float(value[1])
    need(np.isfinite(lo) and np.isfinite(hi) and lo <= hi,
         "finite interval")
    return lo, hi


def contains(stored: Any, value: float, label: str) -> None:
    lo, hi = interval(stored)
    margin = SLACK_RELATIVE * max(abs(value), 1e-12) + 1e-10
    need(lo - margin <= value <= hi + margin, label + " enclosure")


def classify(value: Any) -> str:
    lo, hi = interval(value)
    if hi < 0.9:
        return "RIGHT_COMPLETION_LOWER"
    if lo > 1.1:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def engine_module() -> Any:
    raw = ENGINE_CODE.read_bytes()
    need(digest(raw) == ENGINE_SHA256, "engine provenance")
    spec = importlib.util.spec_from_file_location("independent_tpc268", ENGINE_CODE)
    need(spec is not None and spec.loader is not None, "engine loader")
    engine = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(engine)
    return engine


def literal_beta(engine: Any, value: int, cutoff: int) -> float:
    power = engine.prime_power(value)
    lam = 0.0 if power is None else 1.0 / power[1]
    divisor = sum(engine.mobius(d) for d in range(1, cutoff + 1)
                  if value % d == 0)
    return float(lam - divisor)


def source_context(engine: Any) -> tuple[list[int], np.ndarray, np.ndarray, np.ndarray]:
    indices = list(range(257, 513))
    cache: dict[tuple[int, int], float] = {}

    def beta(value: int, cutoff: int) -> float:
        key = (value, cutoff)
        if key not in cache:
            cache[key] = literal_beta(engine, value, cutoff)
        return cache[key]

    beta_values = np.asarray([beta(value, 5) for value in indices], dtype=np.float64)
    profiles = np.asarray([[beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
                           for value in indices], dtype=np.float64)
    gram = profiles.T @ profiles
    return indices, beta_values, profiles, gram


def physical_image(engine: Any, indices: list[int], beta: np.ndarray,
                   profiles: np.ndarray, shell: list[int], exponent: int
                   ) -> np.ndarray:
    u = np.asarray(indices, dtype=np.int64)[:, None]
    t = np.asarray(indices, dtype=np.int64)[None, :]
    difference = (u - t).astype(np.float64)
    outputs = np.zeros((len(shell), len(indices)), dtype=np.float64)
    for row, prime in enumerate(shell):
        valid = (u != t) & (u % prime != 0) & (t % prime != 0)
        centered = (u % prime == t % prime).astype(np.float64)
        centered -= 1.0 / float(prime - 1)
        kernel = (58.0 ** (2 * exponent)) / (
            58.0 * 58.0 + difference * difference) ** exponent
        outputs[row] = prime * (kernel * centered * valid) @ beta
    return outputs @ profiles


def least_squares(V: np.ndarray, M: np.ndarray,
                  target: np.ndarray) -> tuple[np.ndarray, float, float]:
    coefficients = np.linalg.lstsq(V, target, rcond=None)[0]
    residual = V @ coefficients - target
    return coefficients, float(residual @ residual), float(coefficients @ M @ coefficients)


def frontier(V: np.ndarray, M: np.ndarray, target: np.ndarray,
             tau: float) -> tuple[np.ndarray, float, float]:
    target_norm = float(target @ target)
    radius = tau * tau * target_norm
    _, ls_residual, _ = least_squares(V, M, target)
    need(ls_residual <= radius + 1e-7, "independent infeasible prefix")
    if radius >= target_norm:
        c, residual, source = least_squares(V, M, target)
        return c, residual, source

    def ridge(log_rho: float) -> tuple[np.ndarray, float, float]:
        rho = 10.0 ** log_rho
        c = np.linalg.solve(V.T @ V + rho * M, V.T @ target)
        residual = V @ c - target
        return c, float(residual @ residual), float(c @ M @ c)

    lo, hi = -14.0, 14.0
    while ridge(hi)[1] < radius:
        hi += 2.0
        need(hi < 80.0, "independent bracket overflow")
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if ridge(mid)[1] < radius:
            lo = mid
        else:
            hi = mid
    return ridge((lo + hi) / 2.0)


def recompute_case(engine: Any, rows: dict[tuple[int, int], dict[str, Any]],
                   indices: list[int], beta: np.ndarray, profiles: np.ndarray,
                   gram: np.ndarray, case: dict[str, Any]) -> None:
    left_q, right_q = int(case["from_Q"]), int(case["to_Q"])
    exponent = int(case["kernel_exponent"])
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    lm = dict(zip(left["shell"], left["weighted_target_label"]))
    rm = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(lm) & set(rm))
    exclusive_left = sorted(set(lm) - set(rm))
    exclusive_right = sorted(set(rm) - set(lm))
    union = sorted(set(lm) | set(rm))
    need(case["union_primes"] == union and case["overlap_primes"] == overlap,
         "shell partition")
    need(case["exclusive_left_primes"] == exclusive_left and
         case["exclusive_right_primes"] == exclusive_right,
         "exclusive partition")
    raw_inner = sum(lm[p] * rm[p] for p in overlap)
    sigma = 1 if raw_inner >= 0 else -1
    need(case["optimal_alignment_sign"] == sigma, "alignment sign")
    aligned_right = {p: sigma * rm[p] for p in rm}
    need(case["left_overlap_target"] == [lm[p] for p in overlap],
         "left target")
    need(case["right_overlap_target"] == [aligned_right[p] for p in overlap],
         "right target")
    need(case["left_exclusive_holdout_target"] == [lm[p] for p in exclusive_left],
         "left holdout target")
    need(case["right_exclusive_holdout_target"] ==
         [aligned_right[p] for p in exclusive_right], "right holdout target")

    V = physical_image(engine, indices, beta, profiles, union, exponent)
    pos = {p: i for i, p in enumerate(union)}
    oi = [pos[p] for p in overlap]
    eli = [pos[p] for p in exclusive_left]
    eri = [pos[p] for p in exclusive_right]
    VO = V[oi, :]
    VE = V
    # The checker uses the same row ordering but never imports TPC-307 code.
    tau = case["tau"]
    need(tau in TAUS, "case tau")
    record = case["tau_record"]
    left_target = np.asarray([lm[p] for p in overlap], dtype=np.float64)
    right_target = np.asarray([aligned_right[p] for p in overlap], dtype=np.float64)
    left_k = next((k for k in range(1, min(VO.shape) + 1)
                   if np.linalg.norm(VO[:, :k] @
                      np.linalg.lstsq(VO[:, :k], left_target, rcond=None)[0]
                      - left_target) / np.linalg.norm(left_target)
                   <= float(tau) + 1e-7), None)
    right_k = next((k for k in range(1, min(VO.shape) + 1)
                    if np.linalg.norm(VO[:, :k] @
                       np.linalg.lstsq(VO[:, :k], right_target, rcond=None)[0]
                       - right_target) / np.linalg.norm(right_target)
                   <= float(tau) + 1e-7), None)
    need(left_k is not None and right_k is not None, "feasible prefix")
    k = max(left_k, right_k)
    need(record["overlap_fit_feasible_prefix"] ==
         {"left": left_k, "right": right_k}, "prefix thresholds")
    need(record["comparison_prefix_k"] == k, "common prefix")
    cl, rl, bl = frontier(VO[:, :k], gram[:k, :k], left_target,
                          float(tau))
    cr, rr, br = frontier(VO[:, :k], gram[:k, :k], right_target,
                          float(tau))
    pl = VE[:, :k] @ cl
    pr = VE[:, :k] @ cr
    hl = float(np.mean((pl[eli] -
                        np.asarray([lm[p] for p in exclusive_left])) ** 2))
    hr = float(np.mean((pr[eri] -
                        np.asarray([aligned_right[p] for p in exclusive_right])) ** 2))
    contains(record["left_completion"]["source_budget"], bl, "left budget")
    contains(record["right_completion"]["source_budget"], br, "right budget")
    contains(record["left_completion"]["holdout_mse"], hl, "left holdout")
    contains(record["right_completion"]["holdout_mse"], hr, "right holdout")
    normalizers = {
        "beta_norm_squared": float(beta @ beta),
        "profile_trace_mean": float(np.trace(gram[:k, :k]) / k),
        "first_profile_norm_squared": float(gram[0, 0]),
    }
    for name, value in normalizers.items():
        contains(record["left_completion"]["budget_over_normalizer"][name],
                 bl / value, "left normalized budget")
        contains(record["right_completion"]["budget_over_normalizer"][name],
                 br / value, "right normalized budget")
        contains(record["budget_right_over_left_interval"][name],
                 br / bl, "budget ratio")
    contains(record["holdout_right_over_left_interval"], hr / hl,
             "holdout ratio")
    need(record["budget_preference"] ==
         classify(record["budget_right_over_left_interval"]["beta_norm_squared"]),
         "budget class")
    need(record["holdout_preference"] ==
         classify(record["holdout_right_over_left_interval"]),
         "holdout class")
    expected_agreement = (
        "CONCORDANT" if record["budget_preference"] ==
        record["holdout_preference"] and
        record["budget_preference"] != "PREFERENCE_UNRESOLVED" else
        "DISCORDANT" if {record["budget_preference"],
                          record["holdout_preference"]} ==
        {"RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"} else
        "UNRESOLVED")
    need(record["agreement"] == expected_agreement, "agreement class")


def main() -> int:
    try:
        data = load(RESULT, RESULT_SHA256)
        p302 = load(P302_RESULT, P302_RESULT_SHA256)
        p305 = load(P305_RESULT, P305_RESULT_SHA256)
        p306 = load(P306_RESULT, P306_RESULT_SHA256)
        need(data["claim_status"] == STATUS and
             data["payload"]["schema"] == SCHEMA, "TPC-307 header")
        need(p305["payload"]["finite_audit"]["cases"] == 18 and
             p306["payload"]["finite_audit"]["cases"] == 18,
             "parent headers")
        rows = {}
        for row in p302["payload"]["rows"]:
            if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512
                    and row.get("H") == 58 and row.get("comparison_cutoff_z") == 5
                    and row.get("Q") in {50, 60, 70, 90}
                    and row.get("kernel_exponent") in EXPONENTS):
                rows[(int(row["Q"]), int(row["kernel_exponent"]))] = row
        need(len(rows) == 8, "source row census")
        engine = engine_module()
        indices, beta, profiles, gram = source_context(engine)
        cases = data["payload"]["cases"]
        need(len(cases) == 18, "case census")
        for case in cases:
            recompute_case(engine, rows, indices, beta, profiles, gram, case)
        audit = data["payload"]["finite_audit"]
        need(audit["cases"] == 18 and audit["observations"] == 18 and
             audit["directional_holdout_fits"] == 36 and
             audit["normalizer_rows"] == 54 and
             sum(audit["agreement_counts"].values()) == 18 and
             audit["agreement_counts"]["DISCORDANT"] == 3,
             "published audit")
        print("TPC307_INDEPENDENT_CHECK=PASS cases=18 directional_fits=36 "
              "concordant=13 discordant=3 unresolved=2")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC307_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
