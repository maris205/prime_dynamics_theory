"""Estimate the unique quadratic parameter with the natural prime kneading word.

The script uses only Python's standard library.  For each prefix length M it
computes the parameter interval whose critical-value itinerary under

    f_u(x) = 1 - u*x*x

matches the first M symbols of the natural prime word.  Monotonicity of the
quadratic kneading invariant makes each prefix cylinder an interval.
"""

from __future__ import annotations

from decimal import Decimal, getcontext


PREFIX_LENGTHS = (10, 20, 40, 80, 120, 160, 200)
DECIMAL_PRECISION = 600
BISECTION_STEPS = 800


def prime_table(limit: int) -> bytearray:
    table = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        table[0] = 0
    if limit >= 1:
        table[1] = 0
    for divisor in range(2, int(limit**0.5) + 1):
        if table[divisor]:
            start = divisor * divisor
            count = (limit - start) // divisor + 1
            table[start : limit + 1 : divisor] = b"\x00" * count
    return table


def prime_symbol(index: int, primes: bytearray) -> str:
    if index == 0:
        return "R"
    if index == 1 or primes[index]:
        return "L"
    return "R"


def prefix_compare(parameter: Decimal, length: int, primes: bytearray) -> int:
    """Compare K(f_u) with the prime word in parity-lexicographic order.

    Returns -1, 0, or +1.  Zero means that all requested symbols agree (or
    that the orbit hits the critical point exactly at a cylinder boundary).
    """

    orbit = Decimal(1)
    right_count = 0
    for index in range(length):
        if orbit > 0:
            symbol = "R"
        elif orbit < 0:
            symbol = "L"
        else:
            return 0

        target = prime_symbol(index, primes)
        if symbol != target:
            comparison = -1 if symbol == "L" and target == "R" else 1
            if right_count % 2:
                comparison = -comparison
            return comparison

        if symbol == "R":
            right_count += 1
        orbit = Decimal(1) - parameter * orbit * orbit
    return 0


def prefix_interval(length: int) -> tuple[Decimal, Decimal]:
    primes = prime_table(length)

    # First point whose prefix is not below the target cylinder.
    lower_outside = Decimal(1)
    lower_inside = Decimal(2)
    for _ in range(BISECTION_STEPS):
        midpoint = (lower_outside + lower_inside) / 2
        if prefix_compare(midpoint, length, primes) < 0:
            lower_outside = midpoint
        else:
            lower_inside = midpoint
    lower = lower_inside

    # Last point whose prefix is not above the target cylinder.
    upper_inside = Decimal(1)
    upper_outside = Decimal(2)
    for _ in range(BISECTION_STEPS):
        midpoint = (upper_inside + upper_outside) / 2
        if prefix_compare(midpoint, length, primes) > 0:
            upper_outside = midpoint
        else:
            upper_inside = midpoint
    upper = upper_inside
    return lower, upper


def main() -> None:
    getcontext().prec = DECIMAL_PRECISION
    print("M  midpoint (24 decimal places)       cylinder diameter")
    for length in PREFIX_LENGTHS:
        lower, upper = prefix_interval(length)
        midpoint = (lower + upper) / 2
        diameter = upper - lower
        print(f"{length:3d} {midpoint:.24f} {diameter:.6E}")


if __name__ == "__main__":
    main()
