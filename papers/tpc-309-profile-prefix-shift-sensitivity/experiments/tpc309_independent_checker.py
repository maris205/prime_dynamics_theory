#!/usr/bin/env python3
"""Independent NumPy replay for the TPC-309 profile-ladder atlas.

This checker does not import the TPC-309 producer.  It rebuilds the literal
source profiles from the frozen TPC-268 engine, reconstructs the physical
common-ambient rows, solves each ladder's overlap frontier, and enumerates
the finite exclusive-completion envelopes.  The replay is numerical evidence
for a finite audit, not a directed-rounding or asymptotic certificate.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-309-profile-prefix-shift-sensitivity"
RESULT = PROJECT / "results/tpc309_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-308-adversarial-exclusive-completion-envelope/code/"
    "tpc308_adversarial_exclusive_completion_envelope.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-308-adversarial-exclusive-completion-envelope/results/"
    "tpc308_certificate.json")
TPC307_RESULT = ROOT / (
    "papers/tpc-307-common-ambient-union-shell-holdout/results/"
    "tpc307_certificate.json")
TPC302_RESULT = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/results/"
    "tpc302_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

PARENT_CODE_SHA256 = (
    "08a5058cc2229b2fde2af6d1ee79ed7b7857270dfede5a0109a53364dbfac35c")
PARENT_RESULT_SHA256 = (
    "b25f9317f26dc85231c9315bb87c1343b316c2afa760a0e00798d37da1541453")
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS")
TPC307_RESULT_SHA256 = (
    "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593")
TPC302_RESULT_SHA256 = (
    "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
RESULT_SHA256 = (
    "a4c8f7cd4aef327682b9457c21236f3756f454f4b82f5a901ab2933f1d4cad4a")
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_LADDER_SHIFT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_PROFILE_SENSITIVITY_ATLAS")
SCHEMA = "TPC309_THREE_WINDOW_PROFILE_PREFIX_SHIFT_AUDIT_V1"

Q_SPINE = (50, 60, 70, 90)
PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
RADII = (0, 1, 2)
PROFILE_POOL = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67)
PROFILE_LADDERS = {
    "LOW": PROFILE_POOL[:17],
    "BASE": PROFILE_POOL[1:18],
    "HIGH": PROFILE_POOL[2:19],
}
SLACK_RELATIVE = 2e-3
INTERVAL_RELATIVE_RADIUS = 1e-5


class Failure(RuntimeError):
    """A fail-closed replay error."""


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load(path: Path, expected_hash: str | None = None) -> dict[str, Any]:
    raw = path.read_bytes()
    if expected_hash is not None:
        need(digest(raw) == expected_hash, path.name + " provenance")
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


def enclosure(value: float) -> tuple[float, float]:
    radius = INTERVAL_RELATIVE_RADIUS * max(abs(value), 1e-30)
    return value - radius, value + radius


def ratio_interval(numerator: float, denominator: float
                   ) -> tuple[float, float]:
    nlo, nhi = enclosure(numerator)
    dlo, dhi = enclosure(denominator)
    need(dlo > 0, "positive ratio denominator")
    return nlo / dhi, nhi / dlo


def classify(value: tuple[float, float]) -> str:
    lo, hi = value
    if hi < 0.9:
        return "RIGHT_COMPLETION_LOWER"
    if lo > 1.1:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def agreement(budget: str, holdout: str) -> str:
    if budget == holdout and budget != "PREFERENCE_UNRESOLVED":
        return "CONCORDANT"
    if {budget, holdout} == {
            "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}:
        return "DISCORDANT"
    return "UNRESOLVED"


def engine_module() -> Any:
    raw = ENGINE_CODE.read_bytes()
    need(digest(raw) == ENGINE_SHA256, "TPC-268 engine provenance")
    spec = importlib.util.spec_from_file_location("independent_tpc268_309",
                                                  ENGINE_CODE)
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


def source_context(engine: Any, cutoffs: tuple[int, ...]
                   ) -> tuple[list[int], np.ndarray, np.ndarray]:
    need(tuple(sorted(cutoffs)) == cutoffs and len(cutoffs) == 17,
         "profile ladder shape")
    indices = list(range(257, 513))
    beta = np.asarray([literal_beta(engine, value, 5) for value in indices],
                      dtype=np.float64)
    profiles = np.asarray(
        [[literal_beta(engine, value, cutoff) for cutoff in cutoffs]
         for value in indices], dtype=np.float64)
    return indices, beta, profiles


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


def least_squares(V: np.ndarray, target: np.ndarray
                  ) -> tuple[np.ndarray, float]:
    coefficients = np.linalg.lstsq(V, target, rcond=None)[0]
    residual = V @ coefficients - target
    return coefficients, float(residual @ residual)


def feasible_prefix(V: np.ndarray, target: np.ndarray, tau: float) -> int:
    target_norm = float(target @ target)
    need(target_norm > 0, "positive target norm")
    for k in range(1, min(V.shape) + 1):
        _, residual = least_squares(V[:, :k], target)
        if residual / target_norm <= tau * tau + 1e-7:
            return k
    raise Failure("no feasible prefix")


def frontier(V: np.ndarray, gram: np.ndarray, target: np.ndarray,
             tau: float) -> tuple[np.ndarray, float]:
    target_norm = float(target @ target)
    radius = tau * tau * target_norm
    _, least_residual = least_squares(V, target)
    need(least_residual <= radius + 1e-7, "infeasible common prefix")
    if radius >= target_norm:
        coefficients, residual = least_squares(V, target)
        return coefficients, residual

    def ridge(log_rho: float) -> tuple[np.ndarray, float]:
        rho = 10.0 ** log_rho
        coefficients = np.linalg.solve(V.T @ V + rho * gram,
                                        V.T @ target)
        residual = V @ coefficients - target
        return coefficients, float(residual @ residual)

    lo, hi = -14.0, 14.0
    while ridge(hi)[1] < radius:
        hi += 2.0
        need(hi < 80.0, "frontier bracket overflow")
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if ridge(mid)[1] < radius:
            lo = mid
        else:
            hi = mid
    return ridge((lo + hi) / 2.0)


def completion_values(prediction: np.ndarray, positions: list[int],
                      target: list[int], radius: int
                      ) -> tuple[float, float, float, int]:
    need(len(positions) == len(target) and bool(target),
         "completion shape")
    values: list[float] = []
    for count in range(min(radius, len(target)) + 1):
        for flips in itertools.combinations(range(len(target)), count):
            candidate = np.asarray(target, dtype=np.float64).copy()
            candidate[list(flips)] *= -1.0
            residual = prediction[positions] - candidate
            values.append(float(np.mean(residual * residual)))
    native = float(np.mean((prediction[positions] -
                            np.asarray(target, dtype=np.float64)) ** 2))
    need(bool(values) and bool(np.isfinite(values).all()),
         "completion values")
    return native, min(values), max(values), len(values)


def expected_count(size: int, radius: int) -> int:
    return sum(math.comb(size, j)
               for j in range(min(size, radius) + 1))


def empty_preferences() -> dict[str, int]:
    return {"RIGHT_COMPLETION_LOWER": 0,
            "LEFT_COMPLETION_LOWER": 0,
            "PREFERENCE_UNRESOLVED": 0}


def empty_agreements() -> dict[str, int]:
    return {"CONCORDANT": 0, "DISCORDANT": 0, "UNRESOLVED": 0}


def recompute_case(engine: Any, rows: dict[tuple[int, int], dict[str, Any]],
                   indices: list[int], beta: np.ndarray,
                   profiles: np.ndarray, parent_case: dict[str, Any],
                   tpc307_case: dict[str, Any],
                   image_cache: dict[tuple[str, int, int, int], np.ndarray],
                   ladder: str, stored: dict[str, Any]) -> None:
    left_q, right_q = int(stored["from_Q"]), int(stored["to_Q"])
    exponent, tau_text = int(stored["kernel_exponent"]), stored["tau"]
    tau = float(tau_text)
    need(ladder in PROFILE_LADDERS and (left_q, right_q) in PAIRS and
         exponent in EXPONENTS and tau_text in TAUS, "case coordinates")
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    exclusive_left = sorted(set(left_map) - set(right_map))
    exclusive_right = sorted(set(right_map) - set(left_map))
    union = sorted(set(left_map) | set(right_map))
    need(tpc307_case["overlap_primes"] == overlap and
         tpc307_case["exclusive_left_primes"] == exclusive_left and
         tpc307_case["exclusive_right_primes"] == exclusive_right and
         tpc307_case["union_primes"] == union, "source partition")
    need(stored["profile_cutoffs"] == list(PROFILE_LADDERS[ladder]) and
         stored["union_cardinality"] == len(union) and
         stored["overlap_cardinality"] == len(overlap) and
         stored["exclusive_left_cardinality"] == len(exclusive_left) and
         stored["exclusive_right_cardinality"] == len(exclusive_right),
         "case cardinalities")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    sign = 1 if raw_inner >= 0 else -1
    need(tpc307_case["optimal_alignment_sign"] == sign, "alignment sign")
    aligned_right = {p: sign * value for p, value in right_map.items()}
    need(tpc307_case["left_overlap_target"] ==
         [left_map[p] for p in overlap] and
         tpc307_case["right_overlap_target"] ==
         [aligned_right[p] for p in overlap], "overlap labels")
    need(tpc307_case["left_exclusive_holdout_target"] ==
         [left_map[p] for p in exclusive_left] and
         tpc307_case["right_exclusive_holdout_target"] ==
         [aligned_right[p] for p in exclusive_right], "holdout labels")

    image_key = (ladder, left_q, right_q, exponent)
    if image_key not in image_cache:
        image_cache[image_key] = physical_image(
            engine, indices, beta, profiles, union, exponent)
    ambient = image_cache[image_key]
    position = {prime: index for index, prime in enumerate(union)}
    overlap_indices = [position[p] for p in overlap]
    left_indices = [position[p] for p in exclusive_left]
    right_indices = [position[p] for p in exclusive_right]
    overlap_matrix = ambient[overlap_indices, :]
    left_target = np.asarray([left_map[p] for p in overlap], dtype=np.float64)
    right_target = np.asarray([aligned_right[p] for p in overlap],
                              dtype=np.float64)
    left_k = feasible_prefix(overlap_matrix, left_target, tau)
    right_k = feasible_prefix(overlap_matrix, right_target, tau)
    k = max(left_k, right_k)
    need(stored["overlap_fit_feasible_prefix"] ==
         {"left": left_k, "right": right_k} and
         stored["comparison_prefix_k"] == k, "prefix record")
    gram = profiles.T @ profiles
    left_coefficients, left_residual = frontier(
        overlap_matrix[:, :k], gram[:k, :k], left_target, tau)
    right_coefficients, right_residual = frontier(
        overlap_matrix[:, :k], gram[:k, :k], right_target, tau)
    del left_residual, right_residual
    left_source = float(left_coefficients @ gram[:k, :k] @ left_coefficients)
    right_source = float(right_coefficients @ gram[:k, :k] @ right_coefficients)
    beta_norm = float(beta @ beta)
    norms = (beta_norm, float(np.trace(gram[:k, :k]) / k),
             float(gram[0, 0]))
    budget_intervals = {}
    for name, normalizer in zip(
            ("beta_norm_squared", "profile_trace_mean",
             "first_profile_norm_squared"), norms):
        budget_intervals[name] = ratio_interval(
            right_source / normalizer, left_source / normalizer)
    budget_classes = {name: classify((lo, hi))
                      for name, (lo, hi) in budget_intervals.items()}
    need(len(set(budget_classes.values())) == 1, "budget normalizer invariance")
    profile_budget = next(iter(budget_classes.values()))
    frozen_budget = parent_case["envelopes"][0]["budget_preference"]
    need(stored["profile_budget_preference"] == profile_budget and
         stored["frozen_budget_preference"] == frozen_budget,
         "budget class")
    for name, bounds in budget_intervals.items():
        contains(stored["budget_right_over_left_interval"][name], bounds[0],
                 name + " budget lower")
        contains(stored["budget_right_over_left_interval"][name], bounds[1],
                 name + " budget upper")

    predictions = (ambient[:, :k] @ left_coefficients,
                   ambient[:, :k] @ right_coefficients)
    targets = ([left_map[p] for p in exclusive_left],
               [aligned_right[p] for p in exclusive_right])
    positions = (left_indices, right_indices)
    for record in stored["envelopes"]:
        radius = int(record["radius"])
        need(radius in RADII, "radius")
        extrema = []
        for prediction, target, pos in zip(predictions, targets, positions):
            extrema.append(completion_values(prediction, pos, target, radius))
        left_native, left_min, left_max, left_count = extrema[0]
        right_native, right_min, right_max, right_count = extrema[1]
        need(left_count == expected_count(len(targets[0]), radius) and
             right_count == expected_count(len(targets[1]), radius),
             "candidate count")
        need(record["candidate_count"] == left_count + right_count and
             record["left_completion"]["candidate_count"] == left_count and
             record["right_completion"]["candidate_count"] == right_count,
             "candidate census")
        for label, stored_value, value in (
                ("left native", record["left_completion"]["native_holdout_mse"],
                 left_native),
                ("left minimum", record["left_completion"]["envelope_min_mse"],
                 left_min),
                ("left maximum", record["left_completion"]["envelope_max_mse"],
                 left_max),
                ("right native", record["right_completion"]["native_holdout_mse"],
                 right_native),
                ("right minimum", record["right_completion"]["envelope_min_mse"],
                 right_min),
                ("right maximum", record["right_completion"]["envelope_max_mse"],
                 right_max)):
            contains(stored_value, value, label)
        need(left_min - 1e-10 <= left_native <= left_max + 1e-10 and
             right_min - 1e-10 <= right_native <= right_max + 1e-10,
             "native inside envelope")
        if radius > 0:
            previous = stored["envelopes"][radius - 1]
            old_left_min = interval(previous["left_completion"][
                "envelope_min_mse"])[0]
            old_right_min = interval(previous["right_completion"][
                "envelope_min_mse"])[0]
            old_left_max = interval(previous["left_completion"][
                "envelope_max_mse"])[1]
            old_right_max = interval(previous["right_completion"][
                "envelope_max_mse"])[1]
            need(left_min <= old_left_min +
                 SLACK_RELATIVE * max(abs(old_left_min), 1e-12) + 1e-8 and
                 right_min <= old_right_min +
                 SLACK_RELATIVE * max(abs(old_right_min), 1e-12) + 1e-8 and
                 left_max >= old_left_max -
                 SLACK_RELATIVE * max(abs(old_left_max), 1e-12) - 1e-8 and
                 right_max >= old_right_max -
                 SLACK_RELATIVE * max(abs(old_right_max), 1e-12) - 1e-8,
                 "envelope monotonicity")
        ratio_lo = right_min / left_max
        ratio_hi = right_max / left_min
        contains(record["holdout_right_over_left_interval"], ratio_lo,
                 "holdout ratio lower")
        contains(record["holdout_right_over_left_interval"], ratio_hi,
                 "holdout ratio upper")
        holdout = classify(interval(record["holdout_right_over_left_interval"]))
        need(record["holdout_preference"] == holdout and
             record["agreement"] == agreement(profile_budget, holdout) and
             record["frozen_agreement"] == agreement(frozen_budget, holdout),
             "classification")


def expected_summaries() -> dict[str, dict[str, Any]]:
    return {
        "LOW": {
            "budget": {"RIGHT_COMPLETION_LOWER": 11,
                        "LEFT_COMPLETION_LOWER": 6,
                        "PREFERENCE_UNRESOLVED": 1},
            "holdout": {
                "0": {"RIGHT_COMPLETION_LOWER": 13,
                       "LEFT_COMPLETION_LOWER": 5,
                       "PREFERENCE_UNRESOLVED": 0},
                "1": {"RIGHT_COMPLETION_LOWER": 10,
                       "LEFT_COMPLETION_LOWER": 3,
                       "PREFERENCE_UNRESOLVED": 5},
                "2": {"RIGHT_COMPLETION_LOWER": 7,
                       "LEFT_COMPLETION_LOWER": 2,
                       "PREFERENCE_UNRESOLVED": 9},
            },
            "agreement": {
                "0": {"CONCORDANT": 13, "DISCORDANT": 4, "UNRESOLVED": 1},
                "1": {"CONCORDANT": 10, "DISCORDANT": 2, "UNRESOLVED": 6},
                "2": {"CONCORDANT": 8, "DISCORDANT": 1, "UNRESOLVED": 9},
            },
            "discordance": {
                "0": {"(50, 60)": 2, "(60, 70)": 1, "(70, 90)": 1},
                "1": {"(50, 60)": 2, "(60, 70)": 0, "(70, 90)": 0},
                "2": {"(50, 60)": 1, "(60, 70)": 0, "(70, 90)": 0},
            },
        },
        "BASE": {
            "budget": {"RIGHT_COMPLETION_LOWER": 13,
                        "LEFT_COMPLETION_LOWER": 5,
                        "PREFERENCE_UNRESOLVED": 0},
            "holdout": {
                "0": {"RIGHT_COMPLETION_LOWER": 13,
                       "LEFT_COMPLETION_LOWER": 3,
                       "PREFERENCE_UNRESOLVED": 2},
                "1": {"RIGHT_COMPLETION_LOWER": 11,
                       "LEFT_COMPLETION_LOWER": 2,
                       "PREFERENCE_UNRESOLVED": 5},
                "2": {"RIGHT_COMPLETION_LOWER": 9,
                       "LEFT_COMPLETION_LOWER": 2,
                       "PREFERENCE_UNRESOLVED": 7},
            },
            "agreement": {
                "0": {"CONCORDANT": 13, "DISCORDANT": 3, "UNRESOLVED": 2},
                "1": {"CONCORDANT": 11, "DISCORDANT": 2, "UNRESOLVED": 5},
                "2": {"CONCORDANT": 10, "DISCORDANT": 1, "UNRESOLVED": 7},
            },
            "discordance": {
                "0": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 3},
                "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 2},
                "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 1},
            },
        },
        "HIGH": {
            "budget": {"RIGHT_COMPLETION_LOWER": 9,
                        "LEFT_COMPLETION_LOWER": 7,
                        "PREFERENCE_UNRESOLVED": 2},
            "holdout": {
                "0": {"RIGHT_COMPLETION_LOWER": 8,
                       "LEFT_COMPLETION_LOWER": 9,
                       "PREFERENCE_UNRESOLVED": 1},
                "1": {"RIGHT_COMPLETION_LOWER": 4,
                       "LEFT_COMPLETION_LOWER": 2,
                       "PREFERENCE_UNRESOLVED": 12},
                "2": {"RIGHT_COMPLETION_LOWER": 4,
                       "LEFT_COMPLETION_LOWER": 1,
                       "PREFERENCE_UNRESOLVED": 13},
            },
            "agreement": {
                "0": {"CONCORDANT": 10, "DISCORDANT": 5, "UNRESOLVED": 3},
                "1": {"CONCORDANT": 5, "DISCORDANT": 0, "UNRESOLVED": 13},
                "2": {"CONCORDANT": 5, "DISCORDANT": 0, "UNRESOLVED": 13},
            },
            "discordance": {
                "0": {"(50, 60)": 2, "(60, 70)": 2, "(70, 90)": 1},
                "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 0},
                "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 0},
            },
        },
    }


def main() -> int:
    try:
        data = load(RESULT, RESULT_SHA256)
        parent = load(PARENT_RESULT, PARENT_RESULT_SHA256)
        need(parent["claim_status"] == PARENT_STATUS and
             parent["payload"]["schema"] ==
             "TPC308_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_V1",
             "TPC-308 parent header")
        tpc307 = load(TPC307_RESULT, TPC307_RESULT_SHA256)
        tpc302 = load(TPC302_RESULT, TPC302_RESULT_SHA256)
        need(data["claim_status"] == STATUS and
             data["payload"]["schema"] == SCHEMA, "TPC-309 header")
        payload = data["payload"]
        need(payload["parent_lock"] == {
            "tpc308_code_sha256": PARENT_CODE_SHA256,
            "tpc308_result_sha256": PARENT_RESULT_SHA256,
            "tpc308_cases": 18,
            "tpc308_envelope_observations": 54,
        }, "parent lock")
        parent_cases = {}
        for case in parent["payload"]["cases"]:
            key = (int(case["from_Q"]), int(case["to_Q"]),
                   int(case["kernel_exponent"]), case["tau"])
            parent_cases[key] = case
        need(len(parent_cases) == 18, "parent case map")
        tpc307_cases = {}
        for case in tpc307["payload"]["cases"]:
            key = (int(case["from_Q"]), int(case["to_Q"]),
                   int(case["kernel_exponent"]), case["tau"])
            tpc307_cases[key] = case
        need(len(tpc307_cases) == 18, "TPC-307 case map")
        rows = {}
        for row in tpc302["payload"]["rows"]:
            if (row.get("axis") == "GROWTH_PATH" and
                    row.get("scale") == 512 and row.get("H") == 58 and
                    row.get("comparison_cutoff_z") == 5 and
                    row.get("Q") in set(Q_SPINE) and
                    row.get("kernel_exponent") in set(EXPONENTS)):
                key = (int(row["Q"]), int(row["kernel_exponent"]))
                need(key not in rows, "duplicate source row")
                rows[key] = row
        need(len(rows) == 8, "source row census")
        engine = engine_module()
        contexts = {}
        for ladder, cutoffs in PROFILE_LADDERS.items():
            indices, beta, profiles = source_context(engine, cutoffs)
            contexts[ladder] = (indices, beta, profiles)
        image_cache: dict[tuple[str, int, int, int], np.ndarray] = {}
        cases = payload["cases"]
        need(len(cases) == 54, "case census")
        seen = set()
        for case in cases:
            key = (case["profile_ladder"], int(case["from_Q"]),
                   int(case["to_Q"]), int(case["kernel_exponent"]),
                   case["tau"])
            need(key not in seen, "duplicate profile case")
            seen.add(key)
            ladder = case["profile_ladder"]
            indices, beta, profiles = contexts[ladder]
            parent_key = key[1:]
            recompute_case(engine, rows, indices, beta, profiles,
                           parent_cases[parent_key], tpc307_cases[parent_key],
                           image_cache, ladder, case)
        need(seen == {(ladder, l, r, e, t)
                      for ladder in PROFILE_LADDERS
                      for l, r in PAIRS for e in EXPONENTS for t in TAUS},
             "profile case coverage")

        expected = expected_summaries()
        summaries = {s["profile_ladder"]: s
                     for s in payload["ladder_summary"]}
        need(set(summaries) == set(PROFILE_LADDERS), "summary coverage")
        calculated_candidates = {str(radius): 0 for radius in RADII}
        for ladder in PROFILE_LADDERS:
            subset = [c for c in cases if c["profile_ladder"] == ladder]
            summary = summaries[ladder]
            exp = expected[ladder]
            budget = empty_preferences()
            holdout = {str(r): empty_preferences() for r in RADII}
            agreements = {str(r): empty_agreements() for r in RADII}
            discordance = {str(r): {str(pair): 0 for pair in PAIRS}
                           for r in RADII}
            for case in subset:
                budget[case["profile_budget_preference"]] += 1
                for record in case["envelopes"]:
                    radius = str(record["radius"])
                    holdout[radius][record["holdout_preference"]] += 1
                    agreements[radius][record["agreement"]] += 1
                    if record["agreement"] == "DISCORDANT":
                        discordance[radius][str((case["from_Q"],
                                                 case["to_Q"]))] += 1
                    calculated_candidates[radius] += record["candidate_count"]
            need(budget == exp["budget"] and
                 holdout == exp["holdout"] and
                 agreements == exp["agreement"] and
                 discordance == exp["discordance"],
                 ladder + " recomputed summary")
            need(summary["profile_budget_preference_counts"] == budget and
                 summary["holdout_preference_counts_by_radius"] == holdout and
                 summary["agreement_counts_by_radius"] == agreements and
                 summary["discordance_by_pair_and_radius"] == discordance,
                 ladder + " stored summary")
            need(summary["cases"] == 18 and
                 summary["profile_cutoffs"] == list(PROFILE_LADDERS[ladder]),
                 ladder + " summary header")
        audit = payload["finite_audit"]
        need(audit["profile_ladders"] == 3 and
             audit["cases_per_ladder"] == 18 and
             audit["profile_case_observations"] == 54 and
             audit["envelope_observations"] == 162 and
             audit["directional_envelope_records"] == 324 and
             audit["candidate_evaluations_by_radius"] ==
             {"0": 108, "1": 558, "2": 1440} and
             calculated_candidates == {"0": 108, "1": 558, "2": 1440} and
             audit["baseline_tpc308_class_recovery"] is True and
             audit["fixed_power_credit"] == 0 and
             audit["full_gate_b"] == "OPEN" and
             audit["twin_prime_result"] == "NONE",
             "aggregate audit")
        print("TPC309_INDEPENDENT_CHECK=PASS ladders=3 cases=54 "
              "envelopes=162 candidates=108/558/1440")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC309_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
