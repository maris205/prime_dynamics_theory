#!/usr/bin/env python3
"""TPC-313: outward-rounded profile-budget certificates on the TPC-312 panel.

TPC-312 supplied a new finite source--shell Gram atlas but left the native
profile-budget interface open.  This release keeps that physical panel fixed,
constructs the literal profile image over Q, and certifies a common-prefix
budget separation at normalized residual radius 1/2.

The computational core is rational.  A ridge coefficient vector is solved
exactly over Q; its feasible primal objective is an upper bound, while the
corresponding Lagrange expression is a lower bound.  Every reported scalar is
also propagated through a decimal-grid interval whose endpoints are rounded
outward.  The result is deliberately finite and source-first: it is not an
arithmetic L2 estimate, a growing-shell theorem, an external holdout, or a
twin-prime proof.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing as mp_pool
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/code/"
    "tpc312_new_source_shell_separation.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/results/"
    "tpc312_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc313_certificate.json"

PARENT_CODE_SHA256 = (
    "dc0d371c71069e97cf685f46163efc285ba8a38801f3732b9283ec990426ddb9")
PARENT_RESULT_SHA256 = (
    "04528d9b7381d2f1b3e1e8ff7854114752816fca49ff8779de5a07714b95224d")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

PARENT_STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
PARENT_SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"
STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_"
    "INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_"
    "SEPARATION")
SCHEMA = "TPC313_OUTWARD_PROFILE_BUDGET_INTERVAL_CERTIFICATE_V1"
ROUND2_CLUE = (
    "AUDIT_EXTERNALLY_JUSTIFIED_WEIGHTING_ON_A_FRESH_PHYSICAL_HOLDOUT_"
    "AFTER_FORMAL_BUDGET_CERTIFICATION")

SCALE = 640
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
TAU = Fraction(1, 2)
WEIGHTED_LOWER_THRESHOLD = Fraction(1, 20_000)  # 5e-5
POSITIVE_UPPER_THRESHOLD = Fraction(1, 100_000)  # 1e-5
GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS

# These are deliberately fixed, conservative rational seeds.  They sit just
# below the high-precision ridge roots found during the exploratory pass; the
# exact feasibility check below shrinks them further if a platform changes a
# last-bit boundary.  No floating value enters the certificate.
RHO_SEEDS: dict[tuple[int, int, str], Fraction] = {
    (24, 1, "minimum"): Fraction("14.5"),
    (24, 1, "plus"): Fraction("190000"),
    (24, 2, "minimum"): Fraction("12.5"),
    (24, 2, "plus"): Fraction("100000"),
    (36, 1, "minimum"): Fraction("169"),
    (36, 1, "plus"): Fraction("350000"),
    (36, 2, "minimum"): Fraction("31"),
    (36, 2, "plus"): Fraction("180000"),
    (54, 1, "minimum"): Fraction("252"),
    (54, 1, "plus"): Fraction("600000"),
    (54, 2, "minimum"): Fraction("9.6"),
    (54, 2, "plus"): Fraction("250000"),
    (80, 1, "minimum"): Fraction("71"),
    (80, 1, "plus"): Fraction("850000"),
    (80, 2, "minimum"): Fraction("0.69"),
    (80, 2, "plus"): Fraction("370000"),
}

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc312_for_tpc313", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-312 physical panel unavailable")
PARENT = importlib.util.module_from_spec(parent_spec)
parent_spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def vector_digest(values: list[Fraction]) -> str:
    raw = "".join(f"{value.numerator}/{value.denominator}\n"
                   for value in values)
    return hashlib.sha256(raw.encode("ascii")).hexdigest()


def grid_floor(value: Fraction) -> Fraction:
    quotient, _ = divmod(value.numerator * GRID, value.denominator)
    return Fraction(quotient, GRID)


def grid_ceil(value: Fraction) -> Fraction:
    quotient, remainder = divmod(value.numerator * GRID,
                                  value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


def fixed_decimal(value: Fraction) -> str:
    """Render a fraction whose denominator divides GRID exactly."""
    scaled = value * GRID
    need(scaled.denominator == 1, "non-grid interval endpoint")
    number = scaled.numerator
    sign = "-" if number < 0 else ""
    number = abs(number)
    whole, remainder = divmod(number, GRID)
    if remainder == 0:
        return sign + str(whole)
    tail = f"{remainder:0{GRID_DIGITS}d}".rstrip("0")
    return sign + str(whole) + "." + tail


class DirectedInterval:
    """A closed interval rounded to the declared decimal grid."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int,
                 hi: Fraction | int | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        need(raw_lo <= raw_hi, "reversed raw interval")
        self.lo = grid_floor(raw_lo)
        self.hi = grid_ceil(raw_hi)
        need(self.lo <= self.hi, "reversed rounded interval")

    def __add__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        right = as_interval(other)
        return DirectedInterval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> DirectedInterval:
        return DirectedInterval(-self.hi, -self.lo)

    def __sub__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        return self + (-as_interval(other))

    def __rsub__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        return as_interval(other) - self

    def __mul__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return DirectedInterval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: DirectedInterval | Fraction | int
                    ) -> DirectedInterval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0,
             "interval denominator crosses zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return DirectedInterval(min(values), max(values))

    def square(self) -> DirectedInterval:
        if self.lo <= 0 <= self.hi:
            return DirectedInterval(Fraction(0),
                                    max(self.lo * self.lo,
                                        self.hi * self.hi))
        return DirectedInterval(min(self.lo * self.lo, self.hi * self.hi),
                                max(self.lo * self.lo, self.hi * self.hi))


def as_interval(value: DirectedInterval | Fraction | int) -> DirectedInterval:
    return value if isinstance(value, DirectedInterval) else DirectedInterval(value)


def interval_text(value: DirectedInterval) -> list[str]:
    return [fixed_decimal(value.lo), fixed_decimal(value.hi)]


def row_key(row: dict[str, Any]) -> tuple[int, int]:
    return int(row["Q"]), int(row["kernel_exponent"])


def load_parent() -> tuple[dict[str, Any], dict[tuple[int, int], dict[str, Any]]]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-312 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-312 result provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC-312 canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == PARENT_STATUS,
         "TPC-312 status")
    payload = document.get("payload", {})
    need(payload.get("schema") == PARENT_SCHEMA, "TPC-312 schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "TPC-312 payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and
         audit.get("strict_separation_rows") == 8 and
         audit.get("explicit_shell_targets") == 84,
         "TPC-312 finite census")
    rows = payload.get("rows", [])
    mapped = {row_key(row): row for row in rows}
    need(len(rows) == 8 and len(mapped) == 8, "TPC-312 row map")
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            need((q0, exponent) in mapped, "missing TPC-312 row")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "TPC-268 engine provenance")
    return payload, mapped


def literal_beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    prime_power_part = Fraction(0) if power is None else Fraction(1, power[1])
    divisor_part = sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                        if value % d == 0), Fraction(0))
    return prime_power_part - divisor_part


def exact_profile_matrix(indices: list[int]) -> list[list[Fraction]]:
    return [[literal_beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
            for value in indices]


def exact_matrices(q0: int, exponent: int) -> tuple[
        list[int], list[Fraction], list[list[Fraction]],
        list[list[Fraction]], list[list[Fraction]]]:
    indices = list(range(SCALE // 2 + 1, SCALE + 1))
    beta = [ENGINE.beta_value(value, SCALE) for value in indices]
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [PARENT.PARENT.physical_prime_output(
        indices, beta, HEIGHT, prime, exponent) for prime in shell]
    profiles = exact_profile_matrix(indices)
    image = [[sum((outputs[row][u] * profiles[u][column]
                   for u in range(len(indices))), Fraction(0))
              for column in range(len(PROFILE_CUTOFFS))]
             for row in range(len(shell))]
    gram = [[sum((profiles[u][left] * profiles[u][right]
                  for u in range(len(indices))), Fraction(0))
             for right in range(len(PROFILE_CUTOFFS))]
            for left in range(len(PROFILE_CUTOFFS))]
    return indices, beta, shell, image, gram


def exact_solve(matrix: list[list[Fraction]],
                rhs: list[Fraction]) -> list[Fraction]:
    """Gauss--Jordan elimination over Q with deterministic first pivots."""
    n = len(rhs)
    need(n > 0 and len(matrix) == n and
         all(len(row) == n for row in matrix), "square exact system")
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column] != 0), None)
        need(pivot is not None, "singular profile normal matrix")
        augmented[column], augmented[pivot] = (
            augmented[pivot], augmented[column])
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    augmented[row][entry] - factor * augmented[column][entry]
                    for entry in range(n + 1)]
    return [augmented[row][-1] for row in range(n)]


def prefix_parts(image: list[list[Fraction]],
                 gram: list[list[Fraction]], k: int
                 ) -> tuple[list[list[Fraction]], list[list[Fraction]]]:
    rows = len(image)
    W = [row[:k] for row in image]
    M = [row[:k] for row in gram[:k]]
    normal = [[sum((W[row][left] * W[row][right]
                    for row in range(rows)), Fraction(0))
               for right in range(k)] for left in range(k)]
    need(all(normal[i][i] > 0 for i in range(k)),
         "nonpositive profile normal diagonal")
    return W, M


def image_of(W: list[list[Fraction]], c: list[Fraction]
             ) -> list[Fraction]:
    return [sum((W[row][column] * c[column]
                 for column in range(len(c))), Fraction(0))
            for row in range(len(W))]


def squared_norm(values: list[Fraction]) -> Fraction:
    return sum((value * value for value in values), Fraction(0))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    need(len(left) == len(right), "dot-product length")
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def quadratic(c: list[Fraction], matrix: list[list[Fraction]]) -> Fraction:
    return sum((c[left] * matrix[left][right] * c[right]
                for left in range(len(c))
                for right in range(len(c))), Fraction(0))


def least_squares_residual(image: list[list[Fraction]],
                           gram: list[list[Fraction]], target: list[int],
                           k: int) -> tuple[Fraction, list[Fraction]]:
    W, _ = prefix_parts(image, gram, k)
    normal = [[sum((W[row][left] * W[row][right]
                    for row in range(len(W))), Fraction(0))
               for right in range(k)] for left in range(k)]
    rhs = [sum((W[row][column] * target[row]
                for row in range(len(W))), Fraction(0))
           for column in range(k)]
    coefficients = exact_solve(normal, rhs)
    residual = [value - target[row]
                for row, value in enumerate(image_of(W, coefficients))]
    return squared_norm(residual), coefficients


def first_feasible_prefix(image: list[list[Fraction]],
                          gram: list[list[Fraction]],
                          target: list[int]) -> tuple[int, list[dict[str, Any]]]:
    radius_squared = Fraction(len(target), 4)
    scan: list[dict[str, Any]] = []
    for k in range(1, min(len(target), len(PROFILE_CUTOFFS)) + 1):
        residual_squared, _ = least_squares_residual(image, gram, target, k)
        feasible = residual_squared <= radius_squared
        scan.append({
            "k": k,
            "cutoff": PROFILE_CUTOFFS[k - 1],
            "residual_squared": residual_squared,
            "feasible": feasible,
        })
        if feasible:
            need(all(not item["feasible"] for item in scan[:-1]),
                 "nonminimal first feasible prefix")
            return k, scan
    raise CheckFailure("no feasible profile prefix")


def ridge_certificate(W: list[list[Fraction]],
                      M: list[list[Fraction]], target: list[int],
                      rho: Fraction) -> dict[str, Any]:
    need(rho > 0, "ridge parameter must be positive")
    k = len(M)
    normal = [[sum((W[row][left] * W[row][right]
                    for row in range(len(W))), Fraction(0)) +
               rho * M[left][right]
               for right in range(k)] for left in range(k)]
    rhs = [sum((W[row][column] * target[row]
                for row in range(len(W))), Fraction(0))
           for column in range(k)]
    coefficients = exact_solve(normal, rhs)
    image = image_of(W, coefficients)
    residual = [image[row] - target[row] for row in range(len(target))]
    residual_squared = squared_norm(residual)
    target_norm_squared = Fraction(len(target))
    radius_squared = target_norm_squared * TAU * TAU
    source_norm_squared = quadratic(coefficients, M)
    btv = dot([Fraction(value) for value in target], image)
    dual = (target_norm_squared - radius_squared - btv) / rho
    need(residual_squared <= radius_squared,
         "rational ridge witness is infeasible")
    need(source_norm_squared >= dual >= 0,
         "weak-duality ordering")
    return {
        "rho": rho,
        "coefficients": coefficients,
        "image": image,
        "residual": residual,
        "residual_squared": residual_squared,
        "target_norm_squared": target_norm_squared,
        "radius_squared": radius_squared,
        "source_norm_squared": source_norm_squared,
        "btv": btv,
        "dual": dual,
    }


def choose_ridge(W: list[list[Fraction]], M: list[list[Fraction]],
                 target: list[int], seed: Fraction
                 ) -> tuple[dict[str, Any], int]:
    rho = seed
    for step in range(101):
        try:
            certificate = ridge_certificate(W, M, target, rho)
            return certificate, step
        except CheckFailure as error:
            if "infeasible" not in str(error):
                raise
            rho *= Fraction(999, 1000)
            need(rho > 0, "ridge shrink reached zero")
    raise CheckFailure("unable to find feasible rational ridge seed")


def interval_quadratic(c: list[Fraction],
                       matrix: list[list[Fraction]]) -> DirectedInterval:
    total = DirectedInterval(0)
    for left in range(len(c)):
        for right in range(len(c)):
            total += (DirectedInterval(c[left]) *
                      DirectedInterval(matrix[left][right]) *
                      DirectedInterval(c[right]))
    return total


def interval_dot(left: list[Fraction], right: list[Fraction]
                ) -> DirectedInterval:
    total = DirectedInterval(0)
    for a, b in zip(left, right):
        total += DirectedInterval(a) * DirectedInterval(b)
    return total


def interval_norm(values: list[Fraction]) -> DirectedInterval:
    total = DirectedInterval(0)
    for value in values:
        total += DirectedInterval(value).square()
    return total


def scalar_interval(value: Fraction) -> DirectedInterval:
    return DirectedInterval(value)


def case_record(W: list[list[Fraction]], M: list[list[Fraction]],
                beta_norm_squared: Fraction, target: list[int],
                target_name: str, q0: int, exponent: int, k: int,
                scan: list[dict[str, Any]]) -> dict[str, Any]:
    seed = RHO_SEEDS[(q0, exponent, target_name)]
    certificate, shrink_steps = choose_ridge(W, M, target, seed)
    rho = certificate["rho"]
    residual = certificate["residual"]
    target_norm = certificate["target_norm_squared"]
    radius_squared = certificate["radius_squared"]
    source_norm = certificate["source_norm_squared"]
    dual = certificate["dual"]
    primal_ratio = source_norm / beta_norm_squared
    dual_ratio = dual / beta_norm_squared

    # The following computations intentionally use the interval operators,
    # rather than simply printing a decimal approximation of the exact value.
    residual_interval = interval_norm(residual)
    primal_interval = interval_quadratic(certificate["coefficients"], M)
    beta_interval = scalar_interval(beta_norm_squared)
    primal_ratio_interval = primal_interval / beta_interval
    target_interval = scalar_interval(target_norm)
    radius_interval = scalar_interval(radius_squared)
    btv_interval = interval_dot(
        [Fraction(value) for value in target], certificate["image"])
    dual_interval = ((target_interval - radius_interval - btv_interval) /
                     scalar_interval(rho))
    dual_ratio_interval = dual_interval / beta_interval
    gap_interval = primal_interval - dual_interval

    need(residual_interval.lo <= certificate["residual_squared"] <=
         residual_interval.hi,
         "residual interval misses exact value")
    need(primal_ratio_interval.lo <= primal_ratio <=
         primal_ratio_interval.hi, "primal ratio interval misses value")
    need(dual_ratio_interval.lo <= dual_ratio <= dual_ratio_interval.hi,
         "dual ratio interval misses value")
    need(gap_interval.lo <= source_norm - dual <= gap_interval.hi,
         "duality-gap interval misses value")

    scan_saved = [{
        "k": item["k"],
        "cutoff": item["cutoff"],
        "residual_squared_interval": interval_text(
            scalar_interval(item["residual_squared"])),
        "residual_squared_sha256": fraction_digest(
            item["residual_squared"]),
        "feasible": item["feasible"],
    } for item in scan]
    return {
        "target": target_name,
        "Q": q0,
        "kernel_exponent": exponent,
        "common_prefix_k": k,
        "profile_cutoff": PROFILE_CUTOFFS[k - 1],
        "tau": ["1/2", "0.5"],
        "rho_seed": {
            "numerator": str(seed.numerator),
            "denominator": str(seed.denominator),
        },
        "rho_shrink_steps": shrink_steps,
        "rho": {
            "numerator": str(rho.numerator),
            "denominator": str(rho.denominator),
        },
        "coefficient_vector_sha256": vector_digest(
            certificate["coefficients"]),
        "residual_squared_interval": interval_text(residual_interval),
        "residual_squared_sha256": fraction_digest(
            certificate["residual_squared"]),
        "radius_squared": str(radius_squared),
        "feasible_witness": True,
        "primal_source_norm_squared_interval": interval_text(primal_interval),
        "primal_source_norm_squared_sha256": fraction_digest(source_norm),
        "primal_budget_ratio_interval": interval_text(primal_ratio_interval),
        "primal_budget_ratio_sha256": fraction_digest(primal_ratio),
        "dual_lower_bound_interval": interval_text(dual_interval),
        "dual_lower_bound_sha256": fraction_digest(dual),
        "dual_budget_ratio_interval": interval_text(dual_ratio_interval),
        "dual_budget_ratio_sha256": fraction_digest(dual_ratio),
        "duality_gap_interval": interval_text(gap_interval),
        "duality_gap_sha256": fraction_digest(source_norm - dual),
        "first_feasible_prefix_scan": scan_saved,
        "weighted_lower_threshold_pass": (
            target_name == "minimum" and
            dual_ratio > WEIGHTED_LOWER_THRESHOLD),
        "positive_upper_threshold_pass": (
            target_name == "plus" and
            primal_ratio < POSITIVE_UPPER_THRESHOLD),
    }


def build_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    q0 = int(parent_row["Q"])
    exponent = int(parent_row["kernel_exponent"])
    indices, beta, shell, image, gram = exact_matrices(q0, exponent)
    need(parent_row["prime_shell"] == shell, "parent shell mismatch")
    minimum = [int(value) for value in parent_row["minimum_label"]]
    plus = [1] * len(shell)
    need(len(minimum) == len(shell), "minimum label length")
    beta_norm_squared = squared_norm(beta)
    weighted_k, weighted_scan = first_feasible_prefix(image, gram, minimum)
    plus_k, plus_scan = first_feasible_prefix(image, gram, plus)
    need(plus_k <= weighted_k, "positive target should not need later prefix")
    W, M = prefix_parts(image, gram, weighted_k)
    weighted = case_record(W, M, beta_norm_squared, minimum, "minimum",
                           q0, exponent, weighted_k, weighted_scan)
    positive = case_record(W, M, beta_norm_squared, plus, "plus", q0,
                           exponent, weighted_k, plus_scan)
    need(weighted["weighted_lower_threshold_pass"],
         "weighted lower threshold failed")
    need(positive["positive_upper_threshold_pass"],
         "positive upper threshold failed")
    return {
        "Q": q0,
        "kernel_exponent": exponent,
        "source_interval": [321, 640],
        "index_count": len(indices),
        "shell": shell,
        "shell_cardinality": len(shell),
        "profile_cutoffs": list(PROFILE_CUTOFFS),
        "beta_norm_squared_interval": interval_text(
            scalar_interval(beta_norm_squared)),
        "beta_norm_squared_sha256": fraction_digest(beta_norm_squared),
        "weighted_first_feasible_k": weighted_k,
        "positive_first_feasible_k": plus_k,
        "common_prefix_is_weighted_first_feasible": True,
        "cases": [weighted, positive],
        "source_profile_gram_positive_definite_on_scanned_prefixes": True,
        "exact_physical_operator_replayed": True,
    }


def build_payload() -> dict[str, Any]:
    _, parent_rows = load_parent()
    specifications = [parent_rows[(q0, exponent)]
                      for q0 in Q_ANCHORS for exponent in EXPONENTS]
    workers_text = os.environ.get("TPC313_WORKERS", str(len(specifications)))
    try:
        workers = max(1, min(len(specifications), int(workers_text)))
    except ValueError:
        workers = len(specifications)
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, specifications)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(row) for row in specifications]
    else:
        rows = [build_row(row) for row in specifications]
    need(len(rows) == 8, "row census")
    cases = [case for row in rows for case in row["cases"]]
    weighted = [case for case in cases if case["target"] == "minimum"]
    positive = [case for case in cases if case["target"] == "plus"]
    need(len(cases) == 16 and len(weighted) == 8 and len(positive) == 8,
         "case census")
    need(all(case["weighted_lower_threshold_pass"] for case in weighted),
         "weighted threshold census")
    need(all(case["positive_upper_threshold_pass"] for case in positive),
         "positive threshold census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc312_code_sha256": PARENT_CODE_SHA256,
            "tpc312_result_sha256": PARENT_RESULT_SHA256,
            "tpc268_engine_sha256": ENGINE_CODE_SHA256,
            "tpc312_status": PARENT_STATUS,
        },
        "protocol": {
            "source_interval": [321, 640],
            "source_scale": SCALE,
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "profile_cutoffs": list(PROFILE_CUTOFFS),
            "profile_definition": (
                "beta_cutoff(t)=1_{t=p^a}/a-sum_{d|t,d<=cutoff} mu(d)"),
            "physical_beta_rule": "locked TPC-268 beta_value at scale 640",
            "target_rule": (
                "TPC-312 exact Gram minimum label and all-positive control"),
            "tau": "1/2 normalized Euclidean residual",
            "common_prefix_rule": (
                "least profile prefix feasible for the weighted minimum target; "
                "the positive control is evaluated on that same prefix"),
            "grid_digits": GRID_DIGITS,
            "grid": str(GRID),
            "rho_seed_rule": (
                "fixed rational seed table followed by exact 999/1000 shrink "
                "until residual feasibility"),
        },
        "exact_theorem": {
            "profile_budget": (
                "B_tau(b)=min{c^T M c: ||Wc-b||_2^2<=tau^2||b||_2^2}"),
            "ridge_system": (
                "(W^T W+rho M)c_rho=W^T b, rho>0"),
            "dual_lower_bound": (
                "D_rho=(||b||^2-R^2-b^T Wc_rho)/rho <= B_tau(b)"),
            "primal_upper_bound": (
                "any exact feasible c gives B_tau(b)<=c^T M c"),
            "common_prefix_minimality": (
                "exact least-squares residuals certify all earlier prefixes "
                "infeasible and the selected prefix feasible"),
            "outward_interval_rule": (
                "every rational operation is enclosed on the 10^-36 grid "
                "by floor/ceiling endpoint rounding"),
            "scope": "finite rational source-profile image only",
        },
        "finite_audit": {
            "rows": 8,
            "budget_cases": 16,
            "weighted_cases": 8,
            "positive_control_cases": 8,
            "common_prefix_cases": 8,
            "outward_interval_cases": 16,
            "weighted_dual_above_5e-5": len(weighted),
            "positive_primal_below_1e-5": len(positive),
            "all_dual_witnesses_nonnegative": all(
                case["dual_lower_bound_interval"][0] != "-0"
                for case in cases),
            "fixed_power_credit": 0,
            "external_physical_holdout": "NONE_SAME_LOCKED_ENGINE",
        },
        "thresholds": {
            "weighted_dual_lower_ratio": "1/20000",
            "positive_primal_upper_ratio": "1/100000",
            "tau": "1/2",
        },
        "claim_firewall": {
            "TPC313_PROFILE_PREFIX_FEASIBILITY":
                "PROVED_EXACT_FINITE_8_OF_8",
            "TPC313_RATIONAL_PRIMAL_WITNESSES":
                "PROVED_EXACT_FINITE_16_OF_16",
            "TPC313_RATIONAL_DUAL_LOWER_BOUNDS":
                "PROVED_EXACT_FINITE_16_OF_16",
            "TPC313_OUTWARD_GRID_ENCLOSURES":
                "PROVED_EXACT_FINITE_16_OF_16",
            "TPC313_WEIGHTED_LOWER_SEPARATION":
                "NUMERICALLY_CERTIFIED_FINITE_8_OF_8_ABOVE_5E_MINUS_5",
            "TPC313_POSITIVE_UPPER_SEPARATION":
                "NUMERICALLY_CERTIFIED_FINITE_8_OF_8_BELOW_1E_MINUS_5",
            "TPC313_EXTERNAL_INDEPENDENCE": "NONE",
            "TPC313_TARGET_GENERATION_LEAKAGE":
                "INHERITED_TPC312_SOURCE_FIRST_GRAM_LABEL",
            "TPC313_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC313_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC313_EXTERNAL_WEIGHTING": "OPEN",
            "TPC313_FIXED_POWER_CREDIT": 0,
            "TPC313_FULL_GATE_B": "OPEN",
            "TPC313_TWIN_PRIME_RESULT": "NONE",
            "TPC313_STATUS": STATUS,
        },
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def check_document(data: dict[str, Any]) -> None:
    need(data.get("certificate_version") == 1, "certificate version")
    need(data.get("claim_status") == STATUS, "claim status")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and
         audit.get("budget_cases") == 16 and
         audit.get("outward_interval_cases") == 16 and
         audit.get("weighted_dual_above_5e-5") == 8 and
         audit.get("positive_primal_below_1e-5") == 8 and
         audit.get("fixed_power_credit") == 0,
         "finite audit")
    rows = payload.get("rows", [])
    need(len(rows) == 8 and all(len(row.get("cases", [])) == 2
                                for row in rows), "row payload")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC313_EXTERNAL_INDEPENDENCE") == "NONE" and
         firewall.get("TPC313_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC313_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC313_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC313_TWIN_PRIME_RESULT") == "NONE",
         "claim firewall")


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        built = document()
        check_document(built)
        raw = canonical(built)
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(raw)
        else:
            need(RESULT.is_file(), "missing certificate")
            need(RESULT.read_bytes() == raw, "certificate is not reproducible")
    except (CheckFailure, OSError, ValueError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC313_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC313_CERTIFICATE=PASS rows=8 cases=16 common_prefixes=8 "
          "weighted_dual_gt_5e-5=8 positive_primal_lt_1e-5=8 "
          "grid_digits=36 fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
