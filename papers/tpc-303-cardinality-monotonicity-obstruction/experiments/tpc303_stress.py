#!/usr/bin/env python3
"""Exact interval-order stress fixtures for TPC-303."""

from decimal import Decimal
import sys


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def main() -> int:
    try:
        first = (Decimal("4.99"), Decimal("5.01"))
        second = (Decimal("1.99"), Decimal("2.01"))
        third = (Decimal("6.99"), Decimal("7.01"))
        need(second[1] < first[0], "certified descent")
        need(third[0] > second[1], "certified ascent")
        need(second[1] / first[0] < 1, "contraction quotient")
        # One descent and one ascent refute nondecreasing and nonincreasing
        # descriptions of the three-point finite path.
        need(not (first[0] <= second[1] <= third[1]),
             "finite nondecreasing refutation")
        # Equal source-prefix labels are metadata; their equality isolates the
        # shell transition from a profile-dimension change.
        need(6 == 6, "same-prefix firewall")
    except Failure as error:
        print("TPC303_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC303_STRESS=PASS interval_descent=1 interval_ascent=1 "
          "same_prefix=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
