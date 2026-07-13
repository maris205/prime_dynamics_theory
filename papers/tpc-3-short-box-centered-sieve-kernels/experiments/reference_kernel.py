#!/usr/bin/env python3
"""Exact small-box reference implementation for centered local sieve kernels.

The implementation deliberately favors transparent finite calculations over
speed.  It constructs every entry of a small box, validates two independent
constructions, performs exact empirical double-centering, and then uses NumPy
only for floating-point singular-value calculations.

Nothing computed here is an asymptotic theorem.  In particular, a small
finite-box norm is not evidence for a uniform Type-II estimate.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np


DEFAULT_SEED = 20260713
INTERPRETATION_WARNING = (
    "Finite matrices and numerical singular values are diagnostics only; "
    "they do not prove a uniform subperiod-box estimate, an asymptotic theorem, "
    "or any statement about twin primes."
)


@dataclass(frozen=True)
class BoxSpec:
    """A finite factor box and its local-prime window.

    The intervals are ``[m_start, m_start + m_length)`` and
    ``[n_start, n_start + n_length)``.  The prime window is ``w < p <= y``.
    """

    m_start: int
    m_length: int
    n_start: int
    n_length: int
    w: int
    y: int
    h: int

    def validate(self) -> None:
        if self.m_start < 1 or self.n_start < 1:
            raise ValueError("box starts must be positive")
        if self.m_length < 1 or self.n_length < 1:
            raise ValueError("box lengths must be positive")
        if self.w < 2 or self.y <= self.w:
            raise ValueError("the prime window must satisfy 2 <= w < y")
        if self.h == 0 or self.h % 2 != 0:
            raise ValueError("h must be a nonzero even integer")


@dataclass(frozen=True)
class KernelConstruction:
    """The binary kernel on surviving rows and columns."""

    spec: BoxSpec
    primes: tuple[int, ...]
    active_primes: tuple[int, ...]
    kappa: Fraction
    m_values: tuple[int, ...]
    n_values: tuple[int, ...]
    m_survivor_indices: tuple[int, ...]
    n_survivor_indices: tuple[int, ...]
    kernel: np.ndarray
    method: str

    @property
    def m_survivors(self) -> tuple[int, ...]:
        return tuple(self.m_values[index] for index in self.m_survivor_indices)

    @property
    def n_survivors(self) -> tuple[int, ...]:
        return tuple(self.n_values[index] for index in self.n_survivor_indices)


@dataclass(frozen=True)
class ExactDoubleCentered:
    """An exact rational representation of a doubly centered matrix.

    If ``D`` is the returned matrix, then

        D[i,j] = scale * numerator[i,j].

    The numerator has Python-integer entries, and every row and column sum is
    exactly zero before conversion to floating point.
    """

    numerator: np.ndarray
    scale: Fraction

    def as_float(self) -> np.ndarray:
        return np.asarray(self.numerator, dtype=np.float64) * float(self.scale)

    def has_exact_zero_margins(self) -> bool:
        if self.numerator.size == 0:
            return True
        row_sums = np.sum(self.numerator, axis=1)
        column_sums = np.sum(self.numerator, axis=0)
        return all(value == 0 for value in row_sums) and all(
            value == 0 for value in column_sums
        )


def primes_up_to(limit: int) -> tuple[int, ...]:
    """Return all primes at most ``limit`` by an elementary sieve."""

    if limit < 2:
        return ()
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if not sieve[p]:
            continue
        start = p * p
        sieve[start : limit + 1 : p] = b"\x00" * (
            ((limit - start) // p) + 1
        )
    return tuple(index for index, is_prime in enumerate(sieve) if is_prime)


def primes_in_window(w: int, y: int) -> tuple[int, ...]:
    if w < 2 or y <= w:
        raise ValueError("the prime window must satisfy 2 <= w < y")
    primes = tuple(p for p in primes_up_to(y) if p > w)
    if not primes:
        raise ValueError("the prime window contains no primes")
    return primes


def active_primes_for_shift(primes: Iterable[int], h: int) -> tuple[int, ...]:
    """Delete the local factors with ``p | h``."""

    return tuple(p for p in primes if h % p != 0)


def kappa_for_shift(primes: Iterable[int], h: int) -> Fraction:
    """Return the exact local mean, omitting every prime divisor of ``h``."""

    value = Fraction(1, 1)
    for p in active_primes_for_shift(primes, h):
        value *= Fraction(p - 2, p - 1)
    return value


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def _box_data(
    spec: BoxSpec, primes: Sequence[int]
) -> tuple[
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    m_values = tuple(range(spec.m_start, spec.m_start + spec.m_length))
    n_values = tuple(range(spec.n_start, spec.n_start + spec.n_length))
    modulus = product(primes)
    m_indices = tuple(
        index for index, value in enumerate(m_values) if math.gcd(value, modulus) == 1
    )
    n_indices = tuple(
        index for index, value in enumerate(n_values) if math.gcd(value, modulus) == 1
    )
    return m_values, n_values, m_indices, n_indices


def build_kernel_prime_loop(spec: BoxSpec) -> KernelConstruction:
    """Construct the kernel by testing every active prime separately."""

    spec.validate()
    primes = primes_in_window(spec.w, spec.y)
    active = active_primes_for_shift(primes, spec.h)
    kappa = kappa_for_shift(primes, spec.h)
    m_values, n_values, m_indices, n_indices = _box_data(spec, primes)
    m_survivors = tuple(m_values[index] for index in m_indices)
    n_survivors = tuple(n_values[index] for index in n_indices)

    kernel = np.empty((len(m_survivors), len(n_survivors)), dtype=np.uint8)
    for row, m in enumerate(m_survivors):
        for column, n in enumerate(n_survivors):
            kernel[row, column] = int(
                all((m * n + spec.h) % p != 0 for p in active)
            )

    return KernelConstruction(
        spec=spec,
        primes=primes,
        active_primes=active,
        kappa=kappa,
        m_values=m_values,
        n_values=n_values,
        m_survivor_indices=m_indices,
        n_survivor_indices=n_indices,
        kernel=kernel,
        method="prime-loop",
    )


def build_kernel_direct_modulus(spec: BoxSpec) -> KernelConstruction:
    """Construct the same kernel from one direct gcd with the active modulus."""

    spec.validate()
    primes = primes_in_window(spec.w, spec.y)
    active = active_primes_for_shift(primes, spec.h)
    kappa = kappa_for_shift(primes, spec.h)
    active_modulus = product(active)
    m_values, n_values, m_indices, n_indices = _box_data(spec, primes)
    m_survivors = tuple(m_values[index] for index in m_indices)
    n_survivors = tuple(n_values[index] for index in n_indices)

    kernel = np.empty((len(m_survivors), len(n_survivors)), dtype=np.uint8)
    for row, m in enumerate(m_survivors):
        for column, n in enumerate(n_survivors):
            kernel[row, column] = int(
                math.gcd(m * n + spec.h, active_modulus) == 1
            )

    return KernelConstruction(
        spec=spec,
        primes=primes,
        active_primes=active,
        kappa=kappa,
        m_values=m_values,
        n_values=n_values,
        m_survivor_indices=m_indices,
        n_survivor_indices=n_indices,
        kernel=kernel,
        method="direct-active-modulus",
    )


def validate_constructions(spec: BoxSpec) -> KernelConstruction:
    """Build the matrix in two independent ways and require exact agreement."""

    prime_loop = build_kernel_prime_loop(spec)
    direct = build_kernel_direct_modulus(spec)
    scalar_fields = (
        "primes",
        "active_primes",
        "kappa",
        "m_values",
        "n_values",
        "m_survivor_indices",
        "n_survivor_indices",
    )
    for field in scalar_fields:
        if getattr(prime_loop, field) != getattr(direct, field):
            raise AssertionError(f"construction mismatch in {field}")
    if not np.array_equal(prime_loop.kernel, direct.kernel):
        mismatch = np.argwhere(prime_loop.kernel != direct.kernel)
        raise AssertionError(
            f"kernel constructions differ at {mismatch[:5].tolist()}"
        )
    return prime_loop


def centered_survivor_matrix(construction: KernelConstruction) -> np.ndarray:
    """Return ``K/kappa - 1`` on the surviving rows and columns."""

    return construction.kernel.astype(np.float64) / float(construction.kappa) - 1.0


def centered_ambient_matrix(
    construction: KernelConstruction, survivor_matrix: np.ndarray | None = None
) -> np.ndarray:
    """Embed the survivor matrix in the full box, using zero off the support."""

    if survivor_matrix is None:
        survivor_matrix = centered_survivor_matrix(construction)
    ambient = np.zeros(
        (construction.spec.m_length, construction.spec.n_length), dtype=np.float64
    )
    ambient[
        np.ix_(
            construction.m_survivor_indices,
            construction.n_survivor_indices,
        )
    ] = survivor_matrix
    return ambient


def exact_double_center_binary(
    kernel: np.ndarray, kappa: Fraction
) -> ExactDoubleCentered:
    """Double-center ``K/kappa - 1`` using an exact integer certificate.

    For an ``R x S`` binary matrix ``K``, multiplication by ``R*S`` turns
    empirical double-centering of ``K`` into the integer matrix

        R*S*K - R*row_sum - S*column_sum + total_sum.

    The constant ``-1`` in ``K/kappa - 1`` disappears under double-centering.
    """

    if kernel.ndim != 2:
        raise ValueError("kernel must be a matrix")
    rows, columns = kernel.shape
    if rows == 0 or columns == 0:
        raise ValueError("double-centering requires nonempty survivor sets")
    if kappa <= 0:
        raise ValueError("kappa must be positive")

    exact_kernel = np.asarray(kernel, dtype=object)
    row_sums = np.sum(exact_kernel, axis=1)
    column_sums = np.sum(exact_kernel, axis=0)
    total = sum(row_sums)
    numerator = (
        rows * columns * exact_kernel
        - rows * row_sums[:, np.newaxis]
        - columns * column_sums[np.newaxis, :]
        + total
    )
    scale = Fraction(kappa.denominator, kappa.numerator * rows * columns)
    result = ExactDoubleCentered(numerator=numerator, scale=scale)
    if not result.has_exact_zero_margins():
        raise AssertionError("exact double-centering failed its zero-margin check")
    return result


def floating_double_center(matrix: np.ndarray) -> np.ndarray:
    """Standard floating-point formula, used only as a cross-check."""

    if matrix.ndim != 2 or min(matrix.shape) == 0:
        raise ValueError("matrix must be nonempty and two-dimensional")
    return (
        matrix
        - matrix.mean(axis=1, keepdims=True)
        - matrix.mean(axis=0, keepdims=True)
        + matrix.mean()
    )


def full_singular_values(matrix: np.ndarray) -> np.ndarray:
    """Compute the complete finite singular-value list with NumPy LAPACK."""

    if matrix.ndim != 2 or min(matrix.shape) == 0:
        raise ValueError("SVD requires a nonempty matrix")
    return np.linalg.svd(matrix, compute_uv=False, full_matrices=False)


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _float_list(values: np.ndarray) -> list[float]:
    return [float(value) for value in values]


def analyze_small_box(spec: BoxSpec) -> dict[str, Any]:
    """Run the complete deterministic reference analysis for one small box."""

    construction = validate_constructions(spec)
    survivor_rows, survivor_columns = construction.kernel.shape
    if survivor_rows == 0 or survivor_columns == 0:
        raise ValueError("the requested box has an empty survivor side")

    centered = centered_survivor_matrix(construction)
    ambient = centered_ambient_matrix(construction, centered)
    exact_double = exact_double_center_binary(construction.kernel, construction.kappa)
    double_centered = exact_double.as_float()
    floating_check = floating_double_center(centered)
    if not np.allclose(double_centered, floating_check, rtol=1e-13, atol=1e-13):
        raise AssertionError("exact and floating double-centering disagree")

    survivor_singular_values = full_singular_values(centered)
    ambient_singular_values = full_singular_values(ambient)
    double_singular_values = full_singular_values(double_centered)

    allowed_count = int(np.sum(construction.kernel, dtype=np.int64))
    survivor_pairs = survivor_rows * survivor_columns
    ambient_pairs = spec.m_length * spec.n_length
    exact_centered_sum = Fraction(allowed_count, 1) / construction.kappa - survivor_pairs
    exact_ambient_normalization = exact_centered_sum / ambient_pairs
    exact_survivor_normalization = exact_centered_sum / survivor_pairs

    return {
        "warning": INTERPRETATION_WARNING,
        "spec": {
            "m_start": spec.m_start,
            "m_length": spec.m_length,
            "n_start": spec.n_start,
            "n_length": spec.n_length,
            "w": spec.w,
            "y": spec.y,
            "h": spec.h,
        },
        "local_data": {
            "primes": list(construction.primes),
            "active_primes_excluding_divisors_of_h": list(
                construction.active_primes
            ),
            "kappa_exact": fraction_text(construction.kappa),
            "kappa_float": float(construction.kappa),
        },
        "support": {
            "ambient_rows": spec.m_length,
            "ambient_columns": spec.n_length,
            "survivor_rows": survivor_rows,
            "survivor_columns": survivor_columns,
            "survivor_row_values": list(construction.m_survivors),
            "survivor_column_values": list(construction.n_survivors),
            "allowed_kernel_entries": allowed_count,
        },
        "raw_centered_sum": {
            "exact": fraction_text(exact_centered_sum),
            "float": float(exact_centered_sum),
            "raw_interval_normalized_exact": fraction_text(
                exact_ambient_normalization
            ),
            "raw_interval_normalized_float": float(exact_ambient_normalization),
            "survivor_normalized_exact": fraction_text(
                exact_survivor_normalization
            ),
            "survivor_normalized_float": float(exact_survivor_normalization),
        },
        "double_centering": {
            "exact_scale": fraction_text(exact_double.scale),
            "exact_zero_row_and_column_sums": exact_double.has_exact_zero_margins(),
            "max_float_row_sum": float(
                np.max(np.abs(np.sum(double_centered, axis=1)))
            ),
            "max_float_column_sum": float(
                np.max(np.abs(np.sum(double_centered, axis=0)))
            ),
        },
        "svd": {
            "method": "numpy.linalg.svd; complete finite singular-value list",
            "survivor_raw_singular_values": _float_list(
                survivor_singular_values
            ),
            "ambient_raw_singular_values": _float_list(ambient_singular_values),
            "survivor_double_centered_singular_values": _float_list(
                double_singular_values
            ),
            "raw_interval_operator_normalization": float(
                ambient_singular_values[0] / math.sqrt(ambient_pairs)
            ),
            "survivor_operator_normalization": float(
                survivor_singular_values[0] / math.sqrt(survivor_pairs)
            ),
            "survivor_double_centered_operator_normalization": float(
                double_singular_values[0] / math.sqrt(survivor_pairs)
            ),
        },
        "validation": {
            "prime_loop_equals_direct_active_modulus": True,
            "exact_double_center_equals_floating_formula": True,
            "stochastic_sampling_used": False,
            "reference_seed": DEFAULT_SEED,
        },
    }


def deterministic_validation_specs(seed: int = DEFAULT_SEED) -> list[BoxSpec]:
    """Generate repeatable extra test cases; no sampling enters reported norms."""

    rng = random.Random(seed)
    shifts = (-30, -6, -2, 2, 6, 10, 30)
    specs: list[BoxSpec] = []
    for _ in range(8):
        w, y = rng.choice(((2, 11), (3, 13), (5, 19), (7, 23)))
        specs.append(
            BoxSpec(
                m_start=rng.randint(20, 80),
                m_length=rng.randint(6, 13),
                n_start=rng.randint(20, 80),
                n_length=rng.randint(6, 13),
                w=w,
                y=y,
                h=rng.choice(shifts),
            )
        )
    return specs


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exact small-box centered local-kernel reference calculation."
    )
    parser.add_argument("--m-start", type=int, default=100)
    parser.add_argument("--m-length", type=int, default=24)
    parser.add_argument("--n-start", type=int, default=140)
    parser.add_argument("--n-length", type=int, default=20)
    parser.add_argument("--w", type=int, default=3)
    parser.add_argument("--y", type=int, default=19)
    parser.add_argument("--h", type=int, default=2)
    parser.add_argument(
        "--output",
        type=Path,
        help="write JSON to this path; the default is standard output",
    )
    parser.add_argument("--indent", type=int, default=2)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    spec = BoxSpec(
        m_start=args.m_start,
        m_length=args.m_length,
        n_start=args.n_start,
        n_length=args.n_length,
        w=args.w,
        y=args.y,
        h=args.h,
    )
    try:
        report = analyze_small_box(spec)
    except (AssertionError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"WARNING: {INTERPRETATION_WARNING}", file=sys.stderr)
    payload = json.dumps(report, indent=args.indent, sort_keys=True) + "\n"
    if args.output is None:
        sys.stdout.write(payload)
    else:
        args.output.write_text(payload, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
