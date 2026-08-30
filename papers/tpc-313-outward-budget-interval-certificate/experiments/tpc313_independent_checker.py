#!/usr/bin/env python3
"""Independent exact replay for TPC-313.

This checker does not import the TPC-313 producer or TPC-312's producer.  It
loads only the locked finite arithmetic engine, copies the deleted-diagonal
physical output formula, rebuilds the profile image, and verifies every
rational primal/dual witness and every outward-rounded interval endpoint.
"""

from __future__ import annotations

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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-313-outward-budget-interval-certificate"
RESULT = PROJECT / "results/tpc313_certificate.json"
PARENT_RESULT = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/results/"
    "tpc312_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

STATUS = (
    "PROVED_EXACT_FINITE_PROFILE_PREFIX_FEASIBILITY_AND_OUTWARD_"
    "INTERVAL_BUDGET_CERTIFICATES_PLUS_NUMERICALLY_CERTIFIED_NEW_PANEL_"
    "SEPARATION")
SCHEMA = "TPC313_OUTWARD_PROFILE_BUDGET_INTERVAL_CERTIFICATE_V1"
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
PARENT_SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"
PARENT_RESULT_SHA256 = (
    "04528d9b7381d2f1b3e1e8ff7854114752816fca49ff8779de5a07714b95224d")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

SCALE = 640
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
TAU = Fraction(1, 2)
WEIGHTED_THRESHOLD = Fraction(1, 20_000)
POSITIVE_THRESHOLD = Fraction(1, 100_000)
GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS

spec = importlib.util.spec_from_file_location("locked_engine_tpc313_check",
                                               ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("locked arithmetic engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


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


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def vector_digest(values: list[Fraction]) -> str:
    return hashlib.sha256("".join(
        f"{value.numerator}/{value.denominator}\n" for value in values
    ).encode("ascii")).hexdigest()


def grid_floor(value: Fraction) -> Fraction:
    quotient, _ = divmod(value.numerator * GRID, value.denominator)
    return Fraction(quotient, GRID)


def grid_ceil(value: Fraction) -> Fraction:
    quotient, remainder = divmod(value.numerator * GRID,
                                  value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


def fixed_decimal(value: Fraction) -> str:
    scaled = value * GRID
    need(scaled.denominator == 1, "non-grid endpoint")
    number = scaled.numerator
    sign = "-" if number < 0 else ""
    number = abs(number)
    whole, remainder = divmod(number, GRID)
    if remainder == 0:
        return sign + str(whole)
    tail = f"{remainder:0{GRID_DIGITS}d}".rstrip("0")
    return sign + str(whole) + "." + tail


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int,
                 hi: Fraction | int | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        need(raw_lo <= raw_hi, "reversed interval")
        self.lo = grid_floor(raw_lo)
        self.hi = grid_ceil(raw_hi)
        need(self.lo <= self.hi, "reversed rounded interval")

    def __add__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction | int) -> Interval:
        return self + (-as_interval(other))

    def __rsub__(self, other: Interval | Fraction | int) -> Interval:
        return as_interval(other) - self

    def __mul__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0, "zero-crossing denominator")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(0, max(self.lo * self.lo, self.hi * self.hi))
        return Interval(min(self.lo * self.lo, self.hi * self.hi),
                        max(self.lo * self.lo, self.hi * self.hi))


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(value)


def interval_text(value: Interval) -> list[str]:
    return [fixed_decimal(value.lo), fixed_decimal(value.hi)]


def parse_interval(raw: Any) -> Interval:
    need(isinstance(raw, list) and len(raw) == 2,
         "two-sided stored interval")
    lo, hi = Fraction(raw[0]), Fraction(raw[1])
    need(lo <= hi, "stored interval order")
    return Interval(lo, hi)


def row_key(row: dict[str, Any]) -> tuple[int, int]:
    return int(row["Q"]), int(row["kernel_exponent"])


def load_documents() -> tuple[dict[str, Any], dict[tuple[int, int], dict[str, Any]],
                                dict[str, Any]]:
    raw = RESULT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document["payload"]
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(document.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "certificate payload hash")
    parent_raw = PARENT_RESULT.read_bytes()
    need(digest(parent_raw) == PARENT_RESULT_SHA256,
         "TPC-312 result provenance")
    parent = json.loads(parent_raw)
    need(parent_raw == canonical(parent), "TPC-312 canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") == PARENT_STATUS and
         parent.get("payload", {}).get("schema") == PARENT_SCHEMA,
         "TPC-312 header")
    parent_rows = {row_key(row): row for row in parent["payload"]["rows"]}
    need(len(parent_rows) == 8, "parent row census")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_SHA256,
         "engine provenance")
    return payload, {row_key(row): row for row in payload["rows"]}, parent_rows


def literal_beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    prime_power_part = Fraction(0) if power is None else Fraction(1, power[1])
    divisor_part = sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                        if value % d == 0), Fraction(0))
    return prime_power_part - divisor_part


def physical_prime_output(indices: list[int], beta: list[Fraction],
                          prime: int, exponent: int) -> list[Fraction]:
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(u - t, HEIGHT, exponent) *
                      centered * beta_t)
        output.append(total)
    return output


def exact_matrices(q0: int, exponent: int) -> tuple[
        list[int], list[Fraction], list[int], list[list[Fraction]],
        list[list[Fraction]]]:
    indices = list(range(SCALE // 2 + 1, SCALE + 1))
    beta = [ENGINE.beta_value(value, SCALE) for value in indices]
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [physical_prime_output(indices, beta, prime, exponent)
               for prime in shell]
    profiles = [[literal_beta(value, cutoff) for cutoff in PROFILE_CUTOFFS]
                for value in indices]
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
    n = len(rhs)
    need(n > 0 and len(matrix) == n and
         all(len(row) == n for row in matrix), "square system")
    augmented = [row[:] + [value] for row, value in zip(matrix, rhs)]
    for column in range(n):
        pivot = next((row for row in range(column, n)
                      if augmented[row][column] != 0), None)
        need(pivot is not None, "singular exact system")
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
    W = [row[:k] for row in image]
    M = [row[:k] for row in gram[:k]]
    need(all(sum((W[row][i] * W[row][i]
                  for row in range(len(W))), Fraction(0)) > 0
             for i in range(k)), "zero profile image column")
    return W, M


def image_of(W: list[list[Fraction]], c: list[Fraction]) -> list[Fraction]:
    return [sum((W[row][column] * c[column]
                 for column in range(len(c))), Fraction(0))
            for row in range(len(W))]


def squared_norm(values: list[Fraction]) -> Fraction:
    return sum((value * value for value in values), Fraction(0))


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def quadratic(c: list[Fraction], matrix: list[list[Fraction]]) -> Fraction:
    return sum((c[i] * matrix[i][j] * c[j]
                for i in range(len(c)) for j in range(len(c))), Fraction(0))


def least_squares_residual(image: list[list[Fraction]],
                           gram: list[list[Fraction]], target: list[int],
                           k: int) -> Fraction:
    W, _ = prefix_parts(image, gram, k)
    normal = [[sum((W[row][i] * W[row][j]
                    for row in range(len(W))), Fraction(0))
               for j in range(k)] for i in range(k)]
    rhs = [sum((W[row][j] * target[row]
                for row in range(len(W))), Fraction(0))
           for j in range(k)]
    c = exact_solve(normal, rhs)
    residual = [value - target[row]
                for row, value in enumerate(image_of(W, c))]
    return squared_norm(residual)


def interval_quadratic(c: list[Fraction],
                       matrix: list[list[Fraction]]) -> Interval:
    total = Interval(0)
    for i in range(len(c)):
        for j in range(len(c)):
            total += Interval(c[i]) * Interval(matrix[i][j]) * Interval(c[j])
    return total


def interval_dot(left: list[Fraction], right: list[Fraction]) -> Interval:
    total = Interval(0)
    for a, b in zip(left, right):
        total += Interval(a) * Interval(b)
    return total


def interval_norm(values: list[Fraction]) -> Interval:
    total = Interval(0)
    for value in values:
        total += Interval(value).square()
    return total


def parse_rational_pair(raw: Any) -> Fraction:
    need(isinstance(raw, dict), "rational pair")
    return Fraction(int(raw["numerator"]), int(raw["denominator"]))


def check_case(case: dict[str, Any], W: list[list[Fraction]],
               M: list[list[Fraction]], beta_norm: Fraction,
               target: list[int], expected_k: int) -> None:
    k = int(case["common_prefix_k"])
    need(k == expected_k and int(case["profile_cutoff"]) ==
         PROFILE_CUTOFFS[k - 1], "common prefix")
    rho = parse_rational_pair(case["rho"])
    need(rho > 0, "rho sign")
    need(len(M) == k and len(W[0]) == k, "prefix dimensions")
    normal = [[sum((W[row][i] * W[row][j]
                    for row in range(len(W))), Fraction(0)) +
               rho * M[i][j]
               for j in range(k)] for i in range(k)]
    rhs = [sum((W[row][j] * target[row]
                for row in range(len(W))), Fraction(0)) for j in range(k)]
    coefficients = exact_solve(normal, rhs)
    image = image_of(W, coefficients)
    residual = [image[row] - target[row] for row in range(len(target))]
    residual_squared = squared_norm(residual)
    target_norm = Fraction(len(target))
    radius_squared = target_norm * TAU * TAU
    source_norm = quadratic(coefficients, M)
    btv = dot([Fraction(value) for value in target], image)
    dual = (target_norm - radius_squared - btv) / rho
    need(residual_squared <= radius_squared, "infeasible stored witness")
    need(source_norm >= dual >= 0, "weak duality")
    need(case["radius_squared"] == str(radius_squared), "radius")
    need(case["coefficient_vector_sha256"] == vector_digest(coefficients),
         "coefficient digest")
    need(case["residual_squared_sha256"] == fraction_digest(residual_squared),
         "residual digest")
    need(case["primal_source_norm_squared_sha256"] ==
         fraction_digest(source_norm), "primal digest")
    need(case["dual_lower_bound_sha256"] == fraction_digest(dual),
         "dual digest")
    primal_ratio = source_norm / beta_norm
    dual_ratio = dual / beta_norm
    need(case["primal_budget_ratio_sha256"] == fraction_digest(primal_ratio),
         "primal ratio digest")
    need(case["dual_budget_ratio_sha256"] == fraction_digest(dual_ratio),
         "dual ratio digest")
    gap = source_norm - dual
    need(case["duality_gap_sha256"] == fraction_digest(gap), "gap digest")

    residual_i = interval_norm(residual)
    primal_i = interval_quadratic(coefficients, M)
    beta_i = Interval(beta_norm)
    primal_ratio_i = primal_i / beta_i
    btv_i = interval_dot([Fraction(value) for value in target], image)
    dual_i = ((Interval(target_norm) - Interval(radius_squared) - btv_i) /
              Interval(rho))
    dual_ratio_i = dual_i / beta_i
    gap_i = primal_i - dual_i
    for key, actual in (
            ("residual_squared_interval", residual_i),
            ("primal_source_norm_squared_interval", primal_i),
            ("primal_budget_ratio_interval", primal_ratio_i),
            ("dual_lower_bound_interval", dual_i),
            ("dual_budget_ratio_interval", dual_ratio_i),
            ("duality_gap_interval", gap_i)):
        need(case[key] == interval_text(actual), key + " interval mismatch")
    need(residual_i.lo <= residual_squared <= residual_i.hi,
         "residual enclosure")
    need(primal_ratio_i.lo <= primal_ratio <= primal_ratio_i.hi,
         "primal ratio enclosure")
    need(dual_ratio_i.lo <= dual_ratio <= dual_ratio_i.hi,
         "dual ratio enclosure")
    need(case["target"] in ("minimum", "plus"), "target name")
    if case["target"] == "minimum":
        need(dual_ratio > WEIGHTED_THRESHOLD and
             case["weighted_lower_threshold_pass"] is True,
             "weighted threshold")
    else:
        need(primal_ratio < POSITIVE_THRESHOLD and
             case["positive_upper_threshold_pass"] is True,
             "positive threshold")


def check_row(argument: tuple[dict[str, Any], dict[str, Any]]) -> tuple[int, int]:
    row, parent_row = argument
    q0 = int(row["Q"])
    exponent = int(row["kernel_exponent"])
    need((q0, exponent) in {(q, e) for q in Q_ANCHORS for e in EXPONENTS},
         "row key")
    indices, beta, shell, image, gram = exact_matrices(q0, exponent)
    need(row["source_interval"] == [321, 640] and
         row["index_count"] == len(indices) and row["shell"] == shell,
         "row geometry")
    need(parent_row["prime_shell"] == shell, "parent shell")
    minimum = [int(value) for value in parent_row["minimum_label"]]
    plus = [1] * len(shell)
    need(len(minimum) == len(shell), "target length")
    beta_norm = squared_norm(beta)
    need(row["beta_norm_squared_sha256"] == fraction_digest(beta_norm),
         "beta norm digest")
    need(row["beta_norm_squared_interval"] ==
         interval_text(Interval(beta_norm)), "beta norm interval")
    weighted_k = int(row["weighted_first_feasible_k"])
    plus_k = int(row["positive_first_feasible_k"])
    need(plus_k <= weighted_k, "prefix ordering")
    need(len(row["cases"]) == 2, "case count")
    W, M = prefix_parts(image, gram, weighted_k)
    targets = {"minimum": minimum, "plus": plus}
    for case in row["cases"]:
        name = case["target"]
        need(name in targets, "case target")
        check_case(case, W, M, beta_norm, targets[name], weighted_k)
        scan = case["first_feasible_prefix_scan"]
        expected_scan: list[dict[str, Any]] = []
        for k in range(1, min(len(shell), len(PROFILE_CUTOFFS)) + 1):
            residual = least_squares_residual(image, gram, targets[name], k)
            expected_scan.append({
                "k": k,
                "cutoff": PROFILE_CUTOFFS[k - 1],
                "residual_squared_interval": interval_text(Interval(residual)),
                "residual_squared_sha256": fraction_digest(residual),
                "feasible": residual <= Fraction(len(shell), 4),
            })
            if residual <= Fraction(len(shell), 4):
                break
        need(scan == expected_scan, name + " prefix scan")
    need(row["weighted_first_feasible_k"] == next(
        case["common_prefix_k"] for case in row["cases"]
        if case["target"] == "minimum"), "weighted k alignment")
    return q0, exponent


def main() -> int:
    try:
        payload, rows, parent_rows = load_documents()
        need(len(rows) == 8 and len(parent_rows) == 8, "document census")
        arguments = [(rows[(q, e)], parent_rows[(q, e)])
                     for q in Q_ANCHORS for e in EXPONENTS]
        workers_text = os.environ.get("TPC313_CHECK_WORKERS", str(len(arguments)))
        try:
            workers = max(1, min(len(arguments), int(workers_text)))
        except ValueError:
            workers = len(arguments)
        if workers > 1:
            try:
                with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                    completed = pool.map(check_row, arguments)
            except (AttributeError, OSError, RuntimeError):
                completed = [check_row(argument) for argument in arguments]
        else:
            completed = [check_row(argument) for argument in arguments]
        need(len(completed) == 8, "checked row census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 8 and audit.get("budget_cases") == 16 and
             audit.get("weighted_dual_above_5e-5") == 8 and
             audit.get("positive_primal_below_1e-5") == 8,
             "audit counters")
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC313_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC313_INDEPENDENT_CHECK=PASS rows=8 cases=16 "
          "exact_prefix_scans=16 outward_intervals=16 "
          "weighted_dual_gt_5e-5=8 positive_primal_lt_1e-5=8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
