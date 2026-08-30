#!/usr/bin/env python3
"""Small exact stress suite for the TPC-315 fresh-source protocol."""

from __future__ import annotations

from fractions import Fraction


FRESH_SCALE = 1280
FRESH_INTERVAL = list(range(FRESH_SCALE // 2 + 1, FRESH_SCALE + 1))
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)


GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS
LOG_TERMS = 120


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
        left = Fraction(lo)
        right = left if hi is None else Fraction(hi)
        need(left <= right, "raw interval order")
        self.lo = floor_grid(left)
        self.hi = ceil_grid(right)

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


def enclosure(interval: Interval, value: Fraction) -> None:
    need(interval.lo <= value <= interval.hi, "lost exact value")


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    sieve[:2] = [False, False]
    for value in range(2, int(limit ** 0.5) + 1):
        if sieve[value]:
            sieve[value * value:limit + 1:value] = [False] * (
                ((limit - value * value) // value) + 1)
    return [value for value, is_prime in enumerate(sieve) if is_prime]


def gray_visit_count(size: int) -> int:
    """Check the producer's one-bit Gray traversal cardinality."""
    need(size > 0, "gray size")
    labels = [1] * size
    previous = 0
    seen = {tuple(labels)}
    for code in range(1, 1 << (size - 1)):
        gray = code ^ (code >> 1)
        changed = gray ^ previous
        need(changed and changed & (changed - 1) == 0,
             "gray changed more than one bit")
        vertex = changed.bit_length()
        labels[vertex] = -labels[vertex]
        state = tuple(labels)
        need(state not in seen, "gray duplicate")
        seen.add(state)
        previous = gray
    need(len(seen) == 1 << (size - 1), "gray census")
    return len(seen)


def log_from_atanh(z: Fraction, terms: int = LOG_TERMS) -> tuple[Interval, Fraction]:
    need(0 <= z < 1, "atanh domain")
    partial = sum((z ** (2 * j + 1)) / (2 * j + 1)
                  for j in range(terms)) * 2
    tail = (2 * z ** (2 * terms + 1) /
            ((2 * terms + 1) * (1 - z * z)))
    return Interval(partial, partial + tail), tail


def main() -> int:
    try:
        values = [Fraction(-17, 13), Fraction(-1, 10 ** 9), Fraction(0),
                  Fraction(1, 7), Fraction(23, 5)]
        intervals = [Interval(value) for value in values]
        for value, interval in zip(values, intervals):
            enclosure(interval, value)
        enclosure(sum(intervals, Interval(0)), sum(values, Fraction(0)))
        enclosure(intervals[0] * intervals[-1], values[0] * values[-1])
        enclosure(intervals[4] / intervals[3], values[4] / values[3])

        # Cancellation and signed products are the two places where a naive
        # midpoint implementation could silently lose an enclosure.
        tiny = Fraction(7, 10 ** 12)
        btv = Fraction(15) - Fraction(15, 4) - tiny
        dual = (Fraction(15) - Fraction(15, 4) - btv) / Fraction(11, 7)
        dual_i = (Interval(15) - Interval(Fraction(15, 4)) - Interval(btv)) / Interval(Fraction(11, 7))
        enclosure(dual_i, dual)
        need(dual_i.lo >= 0, "cancellation sign")
        negative = Interval(Fraction(-5, 3)) / Interval(Fraction(9, 11))
        enclosure(negative, Fraction(-55, 27))

        for z in (Fraction(0), Fraction(1, 10), Fraction(1, 3),
                  Fraction(7, 25)):
            log_i, tail = log_from_atanh(z)
            partial = sum((z ** (2 * j + 1)) / (2 * j + 1)
                          for j in range(LOG_TERMS)) * 2
            need(log_i.lo <= partial <= log_i.hi,
                 "atanh interval ordering")
            need(tail >= 0 and tail < Fraction(1, 10 ** 100),
                 "atanh tail bound")

        # Range reduction uses y in [1,2), hence z <= 1/3 for every prime.
        log2_i, log2_tail = log_from_atanh(Fraction(1, 3))
        need(log2_i.lo > Fraction(69, 100) and
             log2_i.hi < Fraction(70, 100), "log two coarse enclosure")
        need(log2_tail < Fraction(1, 10 ** 100), "log two tail")
        for prime, lower, upper in ((29, 3, 4), (47, 3, 4),
                                    (107, 4, 5), (157, 5, 6)):
            k = prime.bit_length() - 1
            y = Fraction(prime, 2 ** k)
            z = (y - 1) / (y + 1)
            value_i, _ = log_from_atanh(z)
            value_i = Interval(k) * log2_i + value_i
            need(value_i.lo > lower and value_i.hi < upper,
                 "range-reduced coarse log enclosure")
        # The fresh panel and prime shells are part of the locked protocol.
        need(FRESH_INTERVAL[0] == 641 and FRESH_INTERVAL[-1] == 1280 and
             len(FRESH_INTERVAL) == 640, "fresh source geometry")
        primes = primes_up_to(160)
        shell_sizes = [sum(q < prime <= 2 * q for prime in primes)
                       for q in Q_ANCHORS]
        need(shell_sizes == [6, 9, 12, 15], "fresh shell geometry")
        gray_cases = 0
        for size in shell_sizes:
            for _ in EXPONENTS:
                need(gray_visit_count(size) == 1 << (size - 1),
                     "fresh Gray enumeration")
                gray_cases += 1
    except (Failure, ZeroDivisionError):
        return 1
    print("TPC315_STRESS=PASS interval_fixtures=7 signed_cancellation=1 "
          "atanh_points=4 range_reductions=4 fresh_scale=1280 "
          "gray_cases=8 log_terms=120 grid_digits=36")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
