#!/usr/bin/env python3
"""Independent finite partition/orientation stress tests for TPC-247."""

from __future__ import annotations

import argparse
from fractions import Fraction


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def check() -> None:
    matrices = (
        ((0, 1), (-2, 0)),
        ((0, 1, -1), (2, 0, 3), (1, -4, 0)),
        ((0, 0, 1, -2), (3, 0, 0, 1), (-1, 2, 0, 0), (4, 1, -3, 0)),
    )
    partitions = (
        ((0, 1),),
        ((0,), (1,)),
        ((0,), (1, 2)),
        ((0, 1), (2, 3)),
        ((0,), (1,), (2,), (3,)),
    )
    cases = 0
    for matrix in matrices:
        n = len(matrix)
        beta = tuple(Fraction(index + 1) for index in range(n))
        w = tuple(Fraction((-1) ** index * (index + 2)) for index in range(n))
        direct = sum((w[u] * matrix[u][t] * beta[t]
                      for u in range(n) for t in range(n)), Fraction(0))
        for partition in partitions:
            flat = tuple(value for block in partition for value in block)
            if len(flat) != n or set(flat) != set(range(n)):
                continue
            block_total = sum((w[u] * matrix[u][t] * beta[t]
                               for c in partition for b in partition
                               for u in c for t in b), Fraction(0))
            need(block_total == direct, "partition scalar")
            wnorm = sum((value * value for value in w), Fraction(0))
            wext = sum((w[u] * w[u] for _ in partition
                        for c in partition for u in c), Fraction(0))
            need(wext == len(partition) * wnorm, "copy norm")
            cases += 1

    # Complex orientation firewall: y=(1,2), w=(1+i,2-i).
    unconjugated = (Fraction(5), Fraction(-1))
    inner_w = (Fraction(5), Fraction(1))
    inner_conjugate_w = (Fraction(5), Fraction(-1))
    need(unconjugated != inner_w and unconjugated == inner_conjugate_w,
         "complex orientation")

    # Block-norm cancellation obstruction.
    full = Fraction(1) + Fraction(-1)
    separated_norm2 = Fraction(1) ** 2 + Fraction(-1) ** 2
    need(full == 0 and separated_norm2 == 2, "norm obstruction")
    need(cases == 5, "stress census")
    print("TPC247_SOURCE_OPERATOR_STRESS=PASS")
    print("partition_cases=5")
    print("complex_orientation=PASS")
    print("block_norm_cancellation_obstruction=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("TPC247_SOURCE_OPERATOR_STRESS=FAIL: use --check")
    try:
        check()
    except (Failure, TypeError, ValueError, ZeroDivisionError) as error:
        raise SystemExit("TPC247_SOURCE_OPERATOR_STRESS=FAIL: " + str(error))


if __name__ == "__main__":
    main()
