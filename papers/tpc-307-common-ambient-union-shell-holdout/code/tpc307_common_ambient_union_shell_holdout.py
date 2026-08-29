#!/usr/bin/env python3
"""Common-ambient union-shell holdout for the TPC-306 interaction atlas.

TPC-306 decomposed two shell-specific operator rows, but the two rows still
used different ambient domains.  This release puts an adjacent pair in one
union-shell row space.  The overlap is used for the constrained fit and both
exclusive shell pieces are withheld.  Two aligned native completions are
then compared on the same fit operator and on the same exclusive holdout.

The result is deliberately finite.  It is a common-ambient diagnostic and a
holdout obstruction atlas, not a causal or asymptotic theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
P305_CODE = ROOT / (
    "papers/tpc-305-counterfactual-transported-label-budget/code/"
    "tpc305_counterfactual_transported_label_budget.py")
P305_RESULT = ROOT / (
    "papers/tpc-305-counterfactual-transported-label-budget/results/"
    "tpc305_certificate.json")
P306_CODE = ROOT / (
    "papers/tpc-306-two-way-operator-target-interaction/code/"
    "tpc306_two_way_operator_target_interaction.py")
P306_RESULT = ROOT / (
    "papers/tpc-306-two-way-operator-target-interaction/results/"
    "tpc306_certificate.json")
RESULT = PROJECT / "results/tpc307_certificate.json"

P305_CODE_SHA256 = (
    "fa43b82a3a7a7adf8821cf8ebacbfadad80759b917787d00ce365e43adfd4c5d")
P305_RESULT_SHA256 = (
    "e2f243ed86132af0cd4a6de169723246f3e2fdc0e4fa595fa3b1ffafe657cad3")
P306_CODE_SHA256 = (
    "7f5a8b424c0c24d431581ea9acfa938a36c1e7ec2900a76e2517c228dda21405")
P306_RESULT_SHA256 = (
    "ab9eba3317e4e22d4955c15cb7a0c22e55fd0495696f34be1476985f2232a34b")

P305_STATUS = (
    "PROVED_EXACT_FINITE_COUNTERFACTUAL_TARGET_SWAP_PROTOCOL_PLUS_"
    "NUMERICALLY_CERTIFIED_FIXED_OPERATOR_TRANSPORTED_LABEL_BUDGET_ATLAS")
P306_STATUS = (
    "PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_"
    "PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS")
STATUS = (
    "PROVED_EXACT_FINITE_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_FINITE_BUDGET_HOLDOUT_DISCORDANCE_ATLAS")
SCHEMA = "TPC307_COMMON_AMBIENT_UNION_SHELL_HOLDOUT_V1"
ROUND2_CLUE = (
    "STRESS_COMMON_AMBIENT_HOLDOUT_AGAINST_EXCLUSIVE_COMPLETION_ENVELOPES_"
    "AND_PROFILE_PREFIX_PERTURBATIONS_BEFORE_ANY_CAUSAL_PREFERENCE_CLAIM")

Q_SPINE = (50, 60, 70, 90)
ADJACENT_PAIRS = tuple(zip(Q_SPINE[:-1], Q_SPINE[1:]))
EXPONENTS = (1, 2)
TAUS = ("0.25", "0.5", "0.75")
NORMALIZERS = (
    "beta_norm_squared", "profile_trace_mean", "first_profile_norm_squared")
PROFILE_CUTOFFS = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                   47, 53, 59, 61)

# The physical rows are assembled by a vectorized double-precision replay of
# the locked rational formula, followed by a high-precision frontier solve on
# the decimalized matrix.  This is intentionally reported as a numerical
# observation/reproduction rather than a directed-rounding certificate.  The
# published enclosure is wide enough for the observed margins and the
# independent checker repeats the construction separately.
MP_DPS = 70
FRONTIER_STEPS = 100
FRONTIER_TOL = mp.mpf("1e-24")
FRONTIER_RESIDUAL_TOL = mp.mpf("1e-15")
INTERVAL_RELATIVE_RADIUS = mp.mpf("1e-5")
CLASSIFY_BELOW = mp.mpf("0.9")
CLASSIFY_ABOVE = mp.mpf("1.1")
THRESHOLD_TOL = mp.mpf("1e-20")
mp.mp.dps = MP_DPS

spec = importlib.util.spec_from_file_location("frozen_tpc305_for_tpc307",
                                               P305_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-305 parent unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)


class CheckFailure(RuntimeError):
    """A fail-closed certificate validation error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def as_mp(value: Any) -> mp.mpf:
    if isinstance(value, mp.mpf):
        return value
    if isinstance(value, int):
        return mp.mpf(value)
    if isinstance(value, (float, np.floating)):
        return mp.mpf(repr(float(value)))
    return mp.mpf(value.numerator) / value.denominator


def interval(value: Any) -> tuple[mp.mpf, mp.mpf]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    lo, hi = mp.mpf(value[0]), mp.mpf(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def emit(value: mp.mpf) -> str:
    return mp.nstr(value, 34)


def enclosure(value: mp.mpf) -> list[str]:
    radius = INTERVAL_RELATIVE_RADIUS * max(abs(value), mp.mpf("1e-30"))
    return [emit(value - radius), emit(value + radius)]


def ratio_interval(numerator: list[str], denominator: list[str]) -> list[str]:
    nlo, nhi = interval(numerator)
    dlo, dhi = interval(denominator)
    need(dlo > 0, "positive ratio denominator")
    return [emit(nlo / dhi), emit(nhi / dlo)]


def classify(value: list[str]) -> str:
    lo, hi = interval(value)
    if hi < CLASSIFY_BELOW:
        return "RIGHT_COMPLETION_LOWER"
    if lo > CLASSIFY_ABOVE:
        return "LEFT_COMPLETION_LOWER"
    return "PREFERENCE_UNRESOLVED"


def locked_json(path: Path, expected_hash: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1, path.name + " version")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def load_parents() -> tuple[dict[str, Any], dict[str, Any]]:
    need(digest(P305_CODE.read_bytes()) == P305_CODE_SHA256,
         "TPC-305 code provenance")
    need(digest(P306_CODE.read_bytes()) == P306_CODE_SHA256,
         "TPC-306 code provenance")
    p305 = locked_json(P305_RESULT, P305_RESULT_SHA256)
    p306 = locked_json(P306_RESULT, P306_RESULT_SHA256)
    need(p305.get("claim_status") == P305_STATUS and
         p305["payload"].get("schema") ==
         "TPC305_COUNTERFACTUAL_TRANSPORTED_LABEL_BUDGET_V1",
         "TPC-305 status/schema")
    need(p306.get("claim_status") == P306_STATUS and
         p306["payload"].get("schema") ==
         "TPC306_TWO_WAY_OPERATOR_TARGET_INTERACTION_V1",
         "TPC-306 status/schema")
    need(p305["payload"]["finite_audit"]["cases"] == 18 and
         p305["payload"]["finite_audit"]["operator_budget_tables"] == 36,
         "TPC-305 census")
    need(p306["payload"]["finite_audit"]["cases"] == 18 and
         p306["payload"]["finite_audit"]["decomposition_rows"] == 54,
         "TPC-306 census")
    return p305, p306


def fixed_rows(p305: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    # Reconstruct the same eight TPC-302 rows through the parent module, then
    # use TPC-305's exact labels as the source-first target lock.
    data302, _ = PARENT.parent_data()
    rows: dict[tuple[int, int], dict[str, Any]] = {}
    for row in data302["payload"]["rows"]:
        if (row.get("axis") == "GROWTH_PATH" and row.get("scale") == 512
                and row.get("H") == 58
                and row.get("comparison_cutoff_z") == 5
                and row.get("Q") in Q_SPINE
                and row.get("kernel_exponent") in EXPONENTS):
            key = (int(row["Q"]), int(row["kernel_exponent"]))
            need(key not in rows, "duplicate fixed row")
            need(row["shell"] == sorted(row["shell"]), "shell order")
            need(len(row["shell"]) == len(row["weighted_target_label"]),
                 "label length")
            need(all(value in (-1, 1)
                     for value in row["weighted_target_label"]),
                 "binary source-first labels")
            rows[key] = row
    need(len(rows) == 8, "fixed row census")
    # The parent certificate must contain the same finite shell data.  This
    # check prevents an accidental switch to an unregistered target family.
    parent_cases = p305["payload"]["cases"]
    need(len(parent_cases) == 18, "parent case count")
    return rows


def p306_case_map(p306: dict[str, Any]) -> dict[tuple[int, int, int, str], dict[str, Any]]:
    answer = {}
    for case in p306["payload"]["cases"]:
        key = (int(case["from_Q"]), int(case["to_Q"]),
               int(case["kernel_exponent"]), case["tau"])
        need(key not in answer, "duplicate TPC-306 case")
        answer[key] = case
    need(len(answer) == 18, "TPC-306 case map")
    return answer


def source_context() -> tuple[list[int], list[Any], np.ndarray,
                              mp.matrix, mp.mpf]:
    """Build the locked source/profile context without the unused Fraction Gram.

    TPC-305's helper constructs a full exact physical Gram for every shell;
    the present paper needs only the 256-by-17 profile matrix and its Gram.
    The beta entries and profile entries are still generated by the locked
    integer/Fraction formula, then converted once for the numerical replay.
    """
    mp.mp.dps = MP_DPS
    indices = list(range(257, 513))
    cache: dict[tuple[int, int], Any] = {}

    def beta(value: int, cutoff: int) -> Any:
        key = (value, cutoff)
        if key not in cache:
            cache[key] = PARENT.PARENT.literal_beta(value, cutoff)
        return cache[key]

    beta_values = [beta(value, 5) for value in indices]
    profile_array = np.asarray(
        [[float(beta(value, cutoff)) for cutoff in PROFILE_CUTOFFS]
         for value in indices], dtype=np.float64)
    gram = profile_array.T @ profile_array
    M = mp.matrix([[mp.mpf(repr(float(value))) for value in row]
                   for row in gram.tolist()])
    beta_norm_squared = mp.mpf(repr(float(
        np.dot(np.asarray([float(value) for value in beta_values]),
               np.asarray([float(value) for value in beta_values])))))
    return indices, beta_values, profile_array, M, beta_norm_squared


def physical_image(indices: list[int], beta: list[Any],
                   profiles: np.ndarray, shell: list[int],
                   exponent: int) -> mp.matrix:
    # Vectorize the literal deleted-diagonal prime output.  The formula is
    # identical to the locked parent, but this avoids constructing enormous
    # Fraction numerators for an unused exact shell Gram.
    u = np.asarray(indices, dtype=np.int64)[:, None]
    t = np.asarray(indices, dtype=np.int64)[None, :]
    beta_float = np.asarray([float(value) for value in beta], dtype=np.float64)
    outputs = np.zeros((len(shell), len(indices)), dtype=np.float64)
    difference = u - t
    for row, prime in enumerate(shell):
        valid = (u != t) & (u % prime != 0) & (t % prime != 0)
        centered = (u % prime == t % prime).astype(np.float64)
        centered -= 1.0 / float(prime - 1)
        kernel = (58.0 ** (2 * exponent)) / (
            58.0 * 58.0 + difference.astype(np.float64) ** 2) ** exponent
        outputs[row, :] = (prime * (kernel * centered * valid) @ beta_float)
    image = outputs @ profiles
    return mp.matrix([[mp.mpf(repr(float(value))) for value in row]
                      for row in image.tolist()])


def squared_norm(vector: mp.matrix) -> mp.mpf:
    return mp.fsum(vector[i] ** 2 for i in range(len(vector)))


def least_squares(V: mp.matrix, M: mp.matrix,
                  target: mp.matrix) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.qr_solve(V, target)[0]
    residual = V * coefficients - target
    residual_squared = squared_norm(residual)
    source_squared = (coefficients.T * M * coefficients)[0]
    return coefficients, residual_squared, source_squared


def ridge(V: mp.matrix, M: mp.matrix, target: mp.matrix,
          rho: mp.mpf) -> tuple[mp.matrix, mp.mpf, mp.mpf]:
    coefficients = mp.lu_solve(V.T * V + rho * M, V.T * target)
    residual = V * coefficients - target
    return coefficients, squared_norm(residual), (coefficients.T * M * coefficients)[0]


def feasible_prefix(V: mp.matrix, M: mp.matrix, target: mp.matrix,
                    tau: mp.mpf) -> int:
    target_norm_squared = squared_norm(target)
    need(target_norm_squared > 0, "positive overlap target norm")
    for k in range(1, min(V.rows, V.cols) + 1):
        _, residual, _ = least_squares(V[:, :k], M[:k, :k], target)
        if mp.sqrt(residual / target_norm_squared) <= tau + THRESHOLD_TOL:
            return k
    raise CheckFailure("no feasible overlap prefix")


def frontier(V: mp.matrix, M: mp.matrix, target: mp.matrix,
             tau: mp.mpf) -> tuple[mp.matrix, dict[str, mp.mpf]]:
    target_norm_squared = squared_norm(target)
    radius_squared = tau ** 2 * target_norm_squared
    _, least_residual, _ = least_squares(V, M, target)
    need(least_residual <= radius_squared + FRONTIER_TOL,
         "infeasible common prefix")
    if radius_squared >= target_norm_squared:
        coefficients, residual, source = least_squares(V, M, target)
        return coefficients, {"residual_squared": residual,
                              "source_squared": source}
    if abs(least_residual - radius_squared) <= FRONTIER_TOL:
        coefficients, residual, source = least_squares(V, M, target)
        return coefficients, {"residual_squared": residual,
                              "source_squared": source}
    lo = mp.mpf(0)
    hi = mp.mpf(1)
    while ridge(V, M, target, hi)[1] < radius_squared:
        hi *= 2
        need(hi < mp.mpf("1e80"), "frontier bracket overflow")
    for _ in range(FRONTIER_STEPS):
        mid = (lo + hi) / 2
        if ridge(V, M, target, mid)[1] < radius_squared:
            lo = mid
        else:
            hi = mid
    rho = (lo + hi) / 2
    coefficients, residual, source = ridge(V, M, target, rho)
    need(abs(residual - radius_squared) < FRONTIER_RESIDUAL_TOL,
         "frontier residual")
    return coefficients, {"residual_squared": residual,
                          "source_squared": source}


def normalizers(M: mp.matrix, k: int,
                beta_norm_squared: mp.mpf) -> dict[str, mp.mpf]:
    trace_mean = mp.fsum(M[i, i] for i in range(k)) / k
    first = M[0, 0]
    need(beta_norm_squared > 0 and trace_mean > 0 and first > 0,
         "positive source normalizers")
    return {"beta_norm_squared": beta_norm_squared,
            "profile_trace_mean": trace_mean,
            "first_profile_norm_squared": first}


def holdout_mse(prediction: mp.matrix, target: list[int],
                indices: list[int]) -> mp.mpf:
    need(bool(indices), "nonempty holdout")
    need(len(target) == len(indices), "holdout target length")
    return mp.fsum((prediction[index] - value) ** 2
                   for index, value in zip(indices, target)) / len(indices)


def fit_record(V_union: mp.matrix, V_overlap: mp.matrix, M: mp.matrix,
               target_overlap: list[int], holdout_target: list[int],
               holdout_indices: list[int],
               tau: str, k: int, beta_norm_squared: mp.mpf
               ) -> dict[str, Any]:
    target = mp.matrix([mp.mpf(value) for value in target_overlap])
    coefficients, raw = frontier(V_overlap[:, :k], M[:k, :k], target,
                                 mp.mpf(tau))
    prediction = V_union[:, :k] * coefficients
    overlap_norm = squared_norm(target)
    overlap_residual = raw["residual_squared"]
    holdout_error = holdout_mse(prediction, holdout_target, holdout_indices)
    holdout_rms = mp.sqrt(holdout_error)
    overlap_rms = mp.sqrt(overlap_residual / overlap_norm)
    norms = normalizers(M, k, beta_norm_squared)
    budget_over = {name: enclosure(raw["source_squared"] / value)
                   for name, value in norms.items()}
    need(mp.sqrt(overlap_residual / overlap_norm) <=
         mp.mpf(tau) + mp.mpf("1e-12"), "fit tolerance")
    return {
        "comparison_prefix_k": k,
        "comparison_cutoff": PROFILE_CUTOFFS[k - 1],
        "overlap_relative_rms": enclosure(overlap_rms),
        "source_budget": enclosure(raw["source_squared"]),
        "budget_over_normalizer": budget_over,
        "holdout_row_count": len(holdout_indices),
        "holdout_mse": enclosure(holdout_error),
        "holdout_rms": enclosure(holdout_rms),
        "generalization_gap_rms": enclosure(holdout_rms - overlap_rms),
    }


def build_case(rows: dict[tuple[int, int], dict[str, Any]],
               parent_cases: dict[tuple[int, int, int, str], dict[str, Any]],
               indices: list[int], beta: list[Any], profiles: list[list[Any]],
               M: mp.matrix, beta_norm_squared: mp.mpf,
               left_q: int, right_q: int, exponent: int, tau: str,
               p306_case: dict[str, Any],
               image_cache: dict[tuple[int, int], mp.matrix]
               ) -> dict[str, Any]:
    left = rows[(left_q, exponent)]
    right = rows[(right_q, exponent)]
    left_map = dict(zip(left["shell"], left["weighted_target_label"]))
    right_map = dict(zip(right["shell"], right["weighted_target_label"]))
    overlap = sorted(set(left_map) & set(right_map))
    exclusive_left = sorted(set(left_map) - set(right_map))
    exclusive_right = sorted(set(right_map) - set(left_map))
    union = sorted(set(left_map) | set(right_map))
    need(bool(overlap and exclusive_left and exclusive_right),
         "nonempty overlap and two holdout pieces")
    raw_inner = sum(left_map[p] * right_map[p] for p in overlap)
    alignment_sign = 1 if raw_inner >= 0 else -1
    aligned_right = {p: alignment_sign * value for p, value in right_map.items()}

    # The two directional records are intentionally not forced into one
    # coordinate-wise union target.  Each target is defined on O and its own
    # exclusive holdout only.  This is the corrected common-ambient protocol:
    # the fit rows and profile matrix are shared, while the holdout rows are
    # withheld from coefficient selection.
    target_left_overlap = [left_map[p] for p in overlap]
    target_right_overlap = [aligned_right[p] for p in overlap]
    position = {p: i for i, p in enumerate(union)}
    overlap_indices = [position[p] for p in overlap]
    left_holdout_indices = [position[p] for p in exclusive_left]
    right_holdout_indices = [position[p] for p in exclusive_right]
    image_key = (left_q, right_q, exponent)
    if image_key not in image_cache:
        image_cache[image_key] = physical_image(
            indices, beta, profiles, union, exponent)
    V_union = image_cache[image_key]
    V_overlap = mp.matrix([[V_union[i, j] for j in range(V_union.cols)]
                           for i in overlap_indices])

    left_k = feasible_prefix(
        V_overlap, M, mp.matrix([mp.mpf(v) for v in target_left_overlap]),
        mp.mpf(tau))
    right_k = feasible_prefix(
        V_overlap, M, mp.matrix([mp.mpf(v) for v in target_right_overlap]),
        mp.mpf(tau))
    k = max(left_k, right_k)
    left_record = fit_record(
        V_union, V_overlap, M, target_left_overlap,
        [left_map[p] for p in exclusive_left], left_holdout_indices, tau, k,
        beta_norm_squared)
    right_record = fit_record(
        V_union, V_overlap, M, target_right_overlap,
        [aligned_right[p] for p in exclusive_right], right_holdout_indices,
        tau, k, beta_norm_squared)
    # The ratio is written as right/left: below one means the right
    # directional target has lower overlap-fit budget, above one means the
    # left directional target has lower budget.
    budget_ratios = {
        name: ratio_interval(right_record["budget_over_normalizer"][name],
                             left_record["budget_over_normalizer"][name])
        for name in NORMALIZERS}
    holdout_ratio = ratio_interval(right_record["holdout_mse"],
                                   left_record["holdout_mse"])
    budget_classes = {name: classify(value)
                      for name, value in budget_ratios.items()}
    need(len(set(budget_classes.values())) == 1,
         "normalizer-invariant budget preference")
    budget_class = next(iter(budget_classes.values()))
    holdout_class = classify(holdout_ratio)
    if budget_class == holdout_class and budget_class != "PREFERENCE_UNRESOLVED":
        agreement = "CONCORDANT"
    elif ({budget_class, holdout_class} == {
            "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER"}):
        agreement = "DISCORDANT"
    else:
        agreement = "UNRESOLVED"
    parent_key = (left_q, right_q, exponent, tau)
    parent = parent_cases[parent_key]
    tau_record = {
        "overlap_fit_feasible_prefix": {
            "left": left_k, "right": right_k},
        "comparison_prefix_k": k,
        "left_completion": left_record,
        "right_completion": right_record,
        "budget_right_over_left_interval": budget_ratios,
        "budget_preference": budget_class,
        "holdout_right_over_left_interval": holdout_ratio,
        "holdout_preference": holdout_class,
        "agreement": agreement,
        "same_prefix_parent_descent": bool(
            parent.get("same_prefix_parent_descent", False)),
    }
    return {
        "from_Q": left_q,
        "to_Q": right_q,
        "kernel_exponent": exponent,
        "tau": tau,
        "union_primes": union,
        "overlap_primes": overlap,
        "exclusive_left_primes": exclusive_left,
        "exclusive_right_primes": exclusive_right,
        "union_cardinality": len(union),
        "overlap_cardinality": len(overlap),
        "exclusive_left_cardinality": len(exclusive_left),
        "exclusive_right_cardinality": len(exclusive_right),
        "raw_overlap_inner_product": raw_inner,
        "optimal_alignment_sign": alignment_sign,
        "left_overlap_target": target_left_overlap,
        "right_overlap_target": target_right_overlap,
        "left_exclusive_holdout_target": [left_map[p] for p in exclusive_left],
        "right_exclusive_holdout_target": [aligned_right[p]
                                           for p in exclusive_right],
        "tau_record": tau_record,
        "parent_tpc306_dominance": p306_case["dominance_status"],
    }


def build_payload() -> dict[str, Any]:
    mp.mp.dps = MP_DPS
    p305, p306 = load_parents()
    rows = fixed_rows(p305)
    p306_map = p306_case_map(p306)
    indices, beta, profiles, M, beta_norm_squared = source_context()
    # Build a compact parent case lookup from TPC-305's locked cases.  It is
    # used only to ensure all 18 declared (pair, exponent, tau) cells remain
    # present; TPC-306 supplies the current parent dominance marker.
    parent_cases = {}
    for case in p305["payload"]["cases"]:
        key = (int(case["from_Q"]), int(case["to_Q"]),
               int(case["kernel_exponent"]), case["tau"])
        parent_cases[key] = case
    need(len(parent_cases) == 18, "TPC-305 parent case map")
    cases = []
    image_cache: dict[tuple[int, int, int], mp.matrix] = {}
    for exponent in EXPONENTS:
        for left_q, right_q in ADJACENT_PAIRS:
            for tau in TAUS:
                key = (left_q, right_q, exponent, tau)
                cases.append(build_case(
                    rows, parent_cases, indices, beta, profiles, M,
                    beta_norm_squared, left_q, right_q, exponent,
                    tau, p306_map[key], image_cache))
    need(len(cases) == 18, "case census")

    observations = [
        (case, case["tau"], case["tau_record"])
        for case in cases
    ]
    need(len(observations) == 18, "observation census")
    budget_counts = {name: 0 for name in (
        "RIGHT_COMPLETION_LOWER", "LEFT_COMPLETION_LOWER",
        "PREFERENCE_UNRESOLVED")}
    holdout_counts = dict(budget_counts)
    agreement_counts = {name: 0 for name in (
        "CONCORDANT", "DISCORDANT", "UNRESOLVED")}
    same_prefix_agreement = {name: 0 for name in agreement_counts}
    pair_summary = []
    for left_q, right_q in ADJACENT_PAIRS:
        subset = [(case, tau, rec) for case, tau, rec in observations
                  if (case["from_Q"], case["to_Q"]) == (left_q, right_q)]
        need(len(subset) == 6, "pair observation census")
        local_budget = {name: 0 for name in budget_counts}
        local_holdout = {name: 0 for name in holdout_counts}
        local_agreement = {name: 0 for name in agreement_counts}
        for case, _, rec in subset:
            local_budget[rec["budget_preference"]] += 1
            local_holdout[rec["holdout_preference"]] += 1
            local_agreement[rec["agreement"]] += 1
            budget_counts[rec["budget_preference"]] += 1
            holdout_counts[rec["holdout_preference"]] += 1
            agreement_counts[rec["agreement"]] += 1
            if rec["same_prefix_parent_descent"]:
                same_prefix_agreement[rec["agreement"]] += 1
        pair_summary.append({
            "from_Q": left_q,
            "to_Q": right_q,
            "observations": len(subset),
            "budget_preference_counts": local_budget,
            "holdout_preference_counts": local_holdout,
            "agreement_counts": local_agreement,
            "same_prefix_parent_descent_observations": sum(
                rec["same_prefix_parent_descent"] for _, _, rec in subset),
        })
    need(sum(agreement_counts.values()) == 18, "agreement count")
    need(agreement_counts["DISCORDANT"] > 0,
         "holdout must expose at least one discordance")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc305_code_sha256": P305_CODE_SHA256,
            "tpc305_result_sha256": P305_RESULT_SHA256,
            "tpc306_code_sha256": P306_CODE_SHA256,
            "tpc306_result_sha256": P306_RESULT_SHA256,
            "tpc305_cases": 18,
            "tpc306_cases": 18,
            "tpc306_decomposition_rows": 54,
        },
        "ambient_definition": {
            "source_scale": 512,
            "height": 58,
            "comparison_cutoff_z": 5,
            "Q_spine": list(Q_SPINE),
            "kernel_exponents": list(EXPONENTS),
            "tolerances": list(TAUS),
            "profile_cutoffs": list(PROFILE_CUTOFFS),
            "ambient_operator": (
                "V_U has one physical row for every prime in U=S_left union S_right"),
            "fit_domain": "O=S_left intersect S_right",
            "holdout_domain": "E=(S_left\\O) union (S_right\\O)",
            "directional_target_rule": (
                "left fit uses left labels on O and left-native labels on E_left; "
                "right fit uses aligned-right labels on O and aligned-right labels on E_right"),
            "comparison_prefix_rule": (
                "fit both overlap targets at k=max(first feasible overlap prefixes)"),
            "budget_ratio": "right_completion_budget / left_completion_budget",
            "holdout_ratio": "right_directional_holdout_MSE / left_directional_holdout_MSE",
            "strict_classification": (
                "right lower iff ratio<0.9; left lower iff ratio>1.1; otherwise unresolved"),
        },
        "exact_theorem": {
            "common_ambient_well_defined": (
                "the union row set U and its overlap/exclusive partition are finite and disjoint"),
            "holdout_separation": (
                "frontier coefficients depend only on V_O and overlap target; E is not read by the fit"),
            "global_sign_invariance": (
                "simultaneously negating a directional overlap and its own holdout target leaves budget and squared holdout loss unchanged"),
            "common_prefix_feasibility": (
                "k=max(k_left,k_right) is feasible for both targets because prefix feasibility is nested"),
            "interval_decision_soundness": (
                "an enclosure wholly below 0.9 or above 1.1 implies the stated finite class"),
            "scope": "finite literal source, fixed Q spine, and directional exclusive holdout protocol",
        },
        "cases": cases,
        "pair_summary": pair_summary,
        "finite_audit": {
            "cases": 18,
            "observations": 18,
            "directional_holdout_fits": 36,
            "normalizer_rows": 54,
            "union_shells": 6,
            "budget_preference_counts": budget_counts,
            "holdout_preference_counts": holdout_counts,
            "agreement_counts": agreement_counts,
            "same_prefix_agreement_counts": same_prefix_agreement,
            "pair_groups": 3,
            "strict_below_threshold": emit(CLASSIFY_BELOW),
            "strict_above_threshold": emit(CLASSIFY_ABOVE),
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "uniform_asymptotic_budget": "OPEN",
            "causal_identification": "NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY",
            "fixed_power_credit": 0,
            "full_gate_b": "OPEN",
            "twin_prime_result": "NONE",
        },
        "firewall": {
            "TPC307_COMMON_AMBIENT_PROTOCOL": "PROVED_EXACT_FINITE",
            "TPC307_OVERLAP_ONLY_FIT": "PROVED_EXACT_FINITE",
            "TPC307_EXCLUSIVE_HOLDOUT": "PROVED_EXACT_FINITE",
            "TPC307_FINITE_HOLDOUT_ATLAS":
                "NUMERICALLY_REPRODUCED_FINITE_18_CASES_36_DIRECTIONAL_FITS_54_NORMALIZER_ROWS",
            "TPC307_HOLDOUT_DISCORDANCE":
                "NUMERICALLY_REPRODUCED_FINITE",
            "TPC307_CAUSAL_IDENTIFICATION":
                "NONE_DIRECTIONAL_HOLDOUT_DIAGNOSTIC_ONLY",
            "TPC307_TARGET_GENERATION_LEAKAGE":
                "INHERITED_TPC302_PHYSICAL_GRAM_DEPENDENT_LABELS",
            "TPC307_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC307_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC307_FIXED_POWER_CREDIT": 0,
            "TPC307_FULL_GATE_B": "OPEN",
            "TPC307_TWIN_PRIME_RESULT": "NONE",
            "TPC307_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))
    print("TPC307_CERTIFICATE=WRITTEN " + str(RESULT))


def check() -> None:
    expected = canonical(document())
    raw = RESULT.read_bytes()
    need(raw == expected, "certificate replay mismatch")
    data = json.loads(raw)
    audit = data["payload"]["finite_audit"]
    need(audit["cases"] == 18 and audit["observations"] == 18 and
         audit["directional_holdout_fits"] == 36 and
         audit["normalizer_rows"] == 54 and
         audit["union_shells"] == 6 and
         sum(audit["agreement_counts"].values()) == 18 and
         audit["agreement_counts"]["DISCORDANT"] > 0 and
         audit["fixed_power_credit"] == 0,
         "finite audit")
    print("TPC307_CERTIFICATE=PASS cases=18 directional_fits=36 "
          "union_shells=6 concordant={} discordant={} unresolved={}".format(
              audit["agreement_counts"]["CONCORDANT"],
              audit["agreement_counts"]["DISCORDANT"],
              audit["agreement_counts"]["UNRESOLVED"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    if args.write:
        write()
    else:
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, json.JSONDecodeError, ValueError,
            ArithmeticError) as error:
        print("TPC307_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
