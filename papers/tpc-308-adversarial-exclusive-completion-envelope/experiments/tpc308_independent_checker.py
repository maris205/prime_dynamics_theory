#!/usr/bin/env python3
"""Independent NumPy replay for the TPC-308 completion-envelope atlas.

The checker never imports the TPC-308 producer.  It rebuilds the literal
source profiles and common-ambient rows from the frozen TPC-268 engine,
solves the overlap frontier independently, enumerates each finite Hamming
ball, and checks the published enclosures and classifications.  The replay
is adversarial numerical evidence, not a directed-rounding proof.
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
PROJECT = ROOT / "papers/tpc-308-adversarial-exclusive-completion-envelope"
RESULT = PROJECT / "results/tpc308_certificate.json"
PARENT_RESULT = ROOT / (
    "papers/tpc-307-common-ambient-union-shell-holdout/results/"
    "tpc307_certificate.json")
P302_RESULT = ROOT / (
    "papers/tpc-302-growing-shell-budget-gap-audit/results/"
    "tpc302_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

RESULT_SHA256 = (
    "b25f9317f26dc85231c9315bb87c1343b316c2afa760a0e00798d37da1541453")
PARENT_RESULT_SHA256 = (
    "8513586b5e7343b257cdd293fe100a4d1680c5df193d568404ebc18539c5f593")
P302_RESULT_SHA256 = (
    "469431136dd2b80ccdddeeedeabe48be8e74405c6df36eead2ae58936a8c24d6")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
SCHEMA = "TPC308_ADVERSARIAL_EXCLUSIVE_COMPLETION_ENVELOPE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_HAMMING_COMPLETION_ENVELOPE_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_HOLDOUT_STABILITY_ATLAS")
PROFILE_CUTOFFS = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                   47, 53, 59, 61)
PAIRS = ((50, 60), (60, 70), (70, 90))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
RADII = (0, 1, 2)
SLACK_RELATIVE = 2e-3


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


def load(path: Path, expected_hash: str) -> dict[str, Any]:
    raw = path.read_bytes()
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


def classify(value: Any) -> str:
    lo, hi = interval(value)
    if hi < 0.9:
        return "RIGHT_COMPLETION_LOWER"
    if lo > 1.1:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def engine_module() -> Any:
    raw = ENGINE_CODE.read_bytes()
    need(digest(raw) == ENGINE_SHA256, "TPC-268 engine provenance")
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


def source_context(engine: Any
                   ) -> tuple[list[int], np.ndarray, np.ndarray, np.ndarray]:
    indices = list(range(257, 513))
    cache: dict[tuple[int, int], float] = {}

    def beta(value: int, cutoff: int) -> float:
        key = (value, cutoff)
        if key not in cache:
            cache[key] = literal_beta(engine, value, cutoff)
        return cache[key]

    beta_values = np.asarray([beta(value, 5) for value in indices],
                             dtype=np.float64)
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
    _, least_residual, _ = least_squares(V, M, target)
    need(least_residual <= radius + 1e-7, "infeasible overlap prefix")
    if radius >= target_norm:
        return least_squares(V, M, target)

    def ridge(log_rho: float) -> tuple[np.ndarray, float, float]:
        rho = 10.0 ** log_rho
        coefficients = np.linalg.solve(V.T @ V + rho * M,
                                        V.T @ target)
        residual = V @ coefficients - target
        return (coefficients, float(residual @ residual),
                float(coefficients @ M @ coefficients))

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


def recompute_case(engine: Any, rows: dict[tuple[int, int], dict[str, Any]],
                   indices: list[int], beta: np.ndarray,
                   profiles: np.ndarray, gram: np.ndarray,
                   parent_cases: dict[tuple[int, int, int, str], dict[str, Any]],
                   image_cache: dict[tuple[int, int, int], np.ndarray],
                   case: dict[str, Any]) -> None:
    left_q, right_q = int(case["from_Q"]), int(case["to_Q"])
    exponent = int(case["kernel_exponent"])
    tau = case["tau"]
    need((left_q, right_q) in PAIRS and exponent in EXPONENTS and tau in TAUS,
         "case coordinates")
    parent_case = parent_cases[(left_q, right_q, exponent, tau)]
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    exclusive_left = sorted(set(left_map) - set(right_map))
    exclusive_right = sorted(set(right_map) - set(left_map))
    union = sorted(set(left_map) | set(right_map))
    need(parent_case["overlap_primes"] == overlap and
         parent_case["exclusive_left_primes"] == exclusive_left and
         parent_case["exclusive_right_primes"] == exclusive_right and
         parent_case["union_primes"] == union, "case partition")
    need(case["union_cardinality"] == len(union) and
         case["overlap_cardinality"] == len(overlap) and
         case["exclusive_left_cardinality"] == len(exclusive_left) and
         case["exclusive_right_cardinality"] == len(exclusive_right),
         "case cardinalities")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    sigma = 1 if raw_inner >= 0 else -1
    need(parent_case["optimal_alignment_sign"] == sigma, "alignment sign")
    aligned_right = {p: sigma * value for p, value in right_map.items()}
    need(parent_case["left_overlap_target"] ==
         [left_map[p] for p in overlap] and
         parent_case["right_overlap_target"] ==
         [aligned_right[p] for p in overlap], "overlap targets")
    need(parent_case["left_exclusive_holdout_target"] ==
         [left_map[p] for p in exclusive_left] and
         parent_case["right_exclusive_holdout_target"] ==
         [aligned_right[p] for p in exclusive_right], "holdout targets")

    image_key = (left_q, right_q, exponent)
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
    left_k = next((k for k in range(1, min(overlap_matrix.shape) + 1)
                   if np.linalg.norm(overlap_matrix[:, :k] @
                      np.linalg.lstsq(overlap_matrix[:, :k], left_target,
                                     rcond=None)[0] - left_target) /
                      np.linalg.norm(left_target) <= float(tau) + 1e-7), None)
    right_k = next((k for k in range(1, min(overlap_matrix.shape) + 1)
                    if np.linalg.norm(overlap_matrix[:, :k] @
                       np.linalg.lstsq(overlap_matrix[:, :k], right_target,
                                      rcond=None)[0] - right_target) /
                       np.linalg.norm(right_target) <= float(tau) + 1e-7), None)
    need(left_k is not None and right_k is not None, "feasible prefix")
    k = max(left_k, right_k)
    need(case["overlap_fit_feasible_prefix"] ==
         {"left": left_k, "right": right_k} and
         case["comparison_prefix_k"] == k, "prefix record")
    left_coefficients, _, left_budget = frontier(
        overlap_matrix[:, :k], gram[:k, :k], left_target, float(tau))
    right_coefficients, _, right_budget = frontier(
        overlap_matrix[:, :k], gram[:k, :k], right_target, float(tau))
    left_prediction = ambient[:, :k] @ left_coefficients
    right_prediction = ambient[:, :k] @ right_coefficients
    left_holdout = [left_map[p] for p in exclusive_left]
    right_holdout = [aligned_right[p] for p in exclusive_right]

    parent_record = parent_case["tau_record"]
    for record, radius in zip(case["envelopes"], RADII):
        need(record["radius"] == radius, "radius order")
        left_native, left_min, left_max, left_count = completion_values(
            left_prediction, left_indices, left_holdout, radius)
        right_native, right_min, right_max, right_count = completion_values(
            right_prediction, right_indices, right_holdout, radius)
        need(left_count == expected_count(len(left_holdout), radius) and
             right_count == expected_count(len(right_holdout), radius),
             "candidate count")
        need(record["candidate_count"] == left_count + right_count and
             record["left_completion"]["candidate_count"] == left_count and
             record["right_completion"]["candidate_count"] == right_count,
             "candidate census")
        for label, stored, value in (
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
            contains(stored, value, label)
        need(left_min - 1e-10 <= left_native <= left_max + 1e-10 and
             right_min - 1e-10 <= right_native <= right_max + 1e-10,
             "native inside envelope")
        # Check monotonicity separately for each directional envelope.
        if record["radius"] > 0:
            old = case["envelopes"][record["radius"] - 1]
            old_left_min = interval(old["left_completion"]["envelope_min_mse"])[0]
            old_right_min = interval(old["right_completion"]["envelope_min_mse"])[0]
            old_left_max = interval(old["left_completion"]["envelope_max_mse"])[1]
            old_right_max = interval(old["right_completion"]["envelope_max_mse"])[1]
            need(left_min <= old_left_min + SLACK_RELATIVE * max(abs(old_left_min), 1e-12) + 1e-8 and
                 right_min <= old_right_min + SLACK_RELATIVE * max(abs(old_right_min), 1e-12) + 1e-8,
                 "lower-envelope monotonicity")
            need(left_max >= old_left_max - SLACK_RELATIVE * max(abs(old_left_max), 1e-12) - 1e-8 and
                 right_max >= old_right_max - SLACK_RELATIVE * max(abs(old_right_max), 1e-12) - 1e-8,
                 "upper-envelope monotonicity")
        ratio_lo = right_min / left_max
        ratio_hi = right_max / left_min
        contains(record["holdout_right_over_left_interval"], ratio_lo,
                 "ratio lower")
        contains(record["holdout_right_over_left_interval"], ratio_hi,
                 "ratio upper")
        need(record["holdout_preference"] ==
             classify(record["holdout_right_over_left_interval"]),
             "holdout class")
        need(record["budget_preference"] == parent_record["budget_preference"],
             "inherited budget class")
        expected_agreement = (
            "CONCORDANT" if record["budget_preference"] ==
            record["holdout_preference"] and
            record["budget_preference"] != "PREFERENCE_UNRESOLVED" else
            "DISCORDANT" if {record["budget_preference"],
                              record["holdout_preference"]} ==
            {"RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"} else
            "UNRESOLVED")
        need(record["agreement"] == expected_agreement, "agreement class")
        if radius == 0:
            need(record["holdout_preference"] ==
                 parent_record["holdout_preference"] and
                 record["agreement"] == parent_record["agreement"],
                 "radius-zero parent recovery")


def main() -> int:
    try:
        data = load(RESULT, RESULT_SHA256)
        parent = load(PARENT_RESULT, PARENT_RESULT_SHA256)
        p302 = load(P302_RESULT, P302_RESULT_SHA256)
        need(data["claim_status"] == STATUS and
             data["payload"]["schema"] == SCHEMA, "TPC-308 header")
        parent_payload = parent["payload"]
        need(parent_payload["schema"] ==
             "TPC307_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_V1" and
             parent_payload["finite_audit"]["cases"] == 18,
             "TPC-307 parent header")
        parent_cases = {}
        for case in parent_payload["cases"]:
            key = (int(case["from_Q"]), int(case["to_Q"]),
                   int(case["kernel_exponent"]), case["tau"])
            parent_cases[key] = case
        need(len(parent_cases) == 18, "parent case map")
        rows: dict[tuple[int, int], dict[str, Any]] = {}
        for row in p302["payload"]["rows"]:
            if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512
                    and row.get("H") == 58 and
                    row.get("comparison_cutoff_z") == 5 and
                    row.get("Q") in {50, 60, 70, 90} and
                    row.get("kernel_exponent") in EXPONENTS):
                rows[(int(row["Q"]), int(row["kernel_exponent"]))] = row
        need(len(rows) == 8, "source row census")
        engine = engine_module()
        indices, beta, profiles, gram = source_context(engine)
        cases = data["payload"]["cases"]
        need(len(cases) == 18, "case census")
        image_cache: dict[tuple[int, int, int], np.ndarray] = {}
        seen = set()
        for case in cases:
            key = (int(case["from_Q"]), int(case["to_Q"]),
                   int(case["kernel_exponent"]), case["tau"])
            need(key not in seen, "duplicate case")
            seen.add(key)
            recompute_case(engine, rows, indices, beta, profiles, gram,
                           parent_cases, image_cache, case)
        need(seen == {(l, r, e, t) for l, r in PAIRS
                      for e in EXPONENTS for t in TAUS}, "case coverage")

        audit = data["payload"]["finite_audit"]
        expected_agreement = {
            "0": {"CONCORDANT": 13, "DISCORDANT": 3, "UNRESOLVED": 2},
            "1": {"CONCORDANT": 11, "DISCORDANT": 2, "UNRESOLVED": 5},
            "2": {"CONCORDANT": 10, "DISCORDANT": 1, "UNRESOLVED": 7},
        }
        expected_holdout = {
            "0": {"RIGHT_COMPLETION_LOWER": 13,
                  "LEFT_COMPLETION_LOWER": 3,
                  "PREFERENCE_UNRESOLVED": 2},
            "1": {"RIGHT_COMPLETION_LOWER": 11,
                  "LEFT_COMPLETION_LOWER": 2,
                  "PREFERENCE_UNRESOLVED": 5},
            "2": {"RIGHT_COMPLETION_LOWER": 9,
                  "LEFT_COMPLETION_LOWER": 2,
                  "PREFERENCE_UNRESOLVED": 7},
        }
        expected_pairs = {str(radius): {str(pair): 0 for pair in PAIRS}
                          for radius in RADII}
        calculated = {str(radius): {name: 0 for name in (
            "CONCORDANT", "DISCORDANT", "UNRESOLVED")} for radius in RADII}
        calculated_holdout = {str(radius): {name: 0 for name in (
            "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER",
            "PREFERENCE_UNRESOLVED")} for radius in RADII}
        candidate_totals = {str(radius): 0 for radius in RADII}
        for case in cases:
            pair = str((int(case["from_Q"]), int(case["to_Q"])))
            for radius in RADII:
                record = case["envelopes"][radius]
                calculated[str(radius)][record["agreement"]] += 1
                calculated_holdout[str(radius)][record["holdout_preference"]] += 1
                candidate_totals[str(radius)] += record["candidate_count"]
                if record["agreement"] == "DISCORDANT":
                    expected_pairs[str(radius)][pair] += 1
        need(audit["agreement_counts_by_radius"] == expected_agreement and
             audit["holdout_preference_counts_by_radius"] == expected_holdout and
             audit["candidate_evaluations_by_radius"] ==
             {"0": 36, "1": 186, "2": 480}, "aggregate audit")
        need(calculated == expected_agreement and
             calculated_holdout == expected_holdout and
             candidate_totals == {"0": 36, "1": 186, "2": 480},
             "recomputed aggregate")
        need(audit["discordance_by_pair_and_radius"] == expected_pairs and
             expected_pairs == {
                 "0": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 3},
                 "1": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 2},
                 "2": {"(50, 60)": 0, "(60, 70)": 0, "(70, 90)": 1},
             }, "discordance localization")
        need(audit["cases"] == 18 and audit["radii"] == 3 and
             audit["envelope_observations"] == 54 and
             audit["directional_envelope_records"] == 108 and
             audit["radius_zero_parent_recovery"] is True and
             audit["fixed_power_credit"] == 0 and
             audit["full_gate_b"] == "OPEN" and
             audit["twin_prime_result"] == "NONE", "claim firewall")
        print("TPC308_INDEPENDENT_CHECK=PASS cases=18 observations=54 "
              "candidates=36/186/480 r0=13/3/2 r1=11/2/5 r2=10/1/7")
        return 0
    except (Failure, OSError, json.JSONDecodeError, ValueError,
            np.linalg.LinAlgError) as error:
        print("TPC308_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
