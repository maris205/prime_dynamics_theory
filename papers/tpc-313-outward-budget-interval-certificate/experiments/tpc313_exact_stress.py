#!/usr/bin/env python3
"""Small adversarial stress suite for TPC-313 interval arithmetic."""

from __future__ import annotations

from fractions import Fraction


GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def floor_grid(value: Fraction) -> Fraction:
    quotient, _ = divmod(value.numerator * GRID, value.denominator)
    return Fraction(quotient, GRID)


def ceil_grid(value: Fraction) -> Fraction:
    quotient, remainder = divmod(value.numerator * GRID,
                                  value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int,
                 hi: Fraction | int | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        need(raw_lo <= raw_hi, "raw order")
        self.lo = floor_grid(raw_lo)
        self.hi = ceil_grid(raw_hi)

    def __add__(self, other: Interval | Fraction | int) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction | int) -> Interval:
        return self + (-other if isinstance(other, Interval)
                       else -Interval(other))

    def __mul__(self, other: Interval | Fraction | int) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction | int) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        need(right.lo > 0 or right.hi < 0, "division through zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(0, max(self.lo * self.lo, self.hi * self.hi))
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))


def check_enclosure(interval: Interval, value: Fraction) -> None:
    need(interval.lo <= value <= interval.hi, "lost exact value")


def main() -> int:
    try:
        values = [Fraction(-17, 13), Fraction(-1, 10**9),
                  Fraction(0), Fraction(1, 7), Fraction(23, 5)]
        intervals = [Interval(value) for value in values]
        for value, interval in zip(values, intervals):
            check_enclosure(interval, value)
        exact_sum = sum(values, Fraction(0))
        check_enclosure(sum(intervals, Interval(0)), exact_sum)
        exact_product = values[0] * values[-1]
        check_enclosure(intervals[0] * intervals[-1], exact_product)
        exact_square = values[0] * values[0]
        check_enclosure(intervals[0].square(), exact_square)
        exact_quotient = values[4] / values[3]
        check_enclosure(intervals[4] / intervals[3], exact_quotient)

        # A cancellation-heavy dual expression.  The interval must remain
        # valid even when the numerator is much smaller than its summands.
        target_norm = Fraction(15, 1)
        radius = Fraction(15, 4)
        btv = target_norm - radius - Fraction(7, 10**12)
        rho = Fraction(11, 7)
        exact_dual = (target_norm - radius - btv) / rho
        dual_interval = ((Interval(target_norm) - Interval(radius) -
                          Interval(btv)) / Interval(rho))
        check_enclosure(dual_interval, exact_dual)
        need(dual_interval.lo >= 0, "cancellation changed sign")

        # Check an interval quotient with a negative numerator and positive
        # denominator, which exercises endpoint reversal indirectly.
        negative = Interval(Fraction(-5, 3))
        positive = Interval(Fraction(9, 11))
        check_enclosure(negative / positive, Fraction(-55, 27))
    except (Failure, ZeroDivisionError):
        return 1
    print("TPC313_STRESS=PASS interval_fixtures=5 "
          "cancellation_dual=1 signed_quotient=1 grid_digits=36")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
