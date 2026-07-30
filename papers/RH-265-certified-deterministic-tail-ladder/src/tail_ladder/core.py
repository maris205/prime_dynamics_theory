"""Certified first-omitted-order tail ladder."""

from __future__ import annotations

from direct_tail import direct_tail_majorant


def validate_orders(orders: tuple[int, ...]) -> tuple[int, ...]:
    normalized = tuple(int(order) for order in orders)
    if not normalized or any(order < 3 or order % 2 == 0 for order in normalized):
        raise ValueError("orders must be nonempty odd integers at least three")
    if normalized != tuple(sorted(set(normalized))):
        raise ValueError("orders must be strictly increasing")
    return normalized


def build_ladder(reduced_bounds: object, orders: tuple[int, ...]):
    """Return direct-tail records for a validated sequence of odd orders."""

    return tuple(
        direct_tail_majorant(reduced_bounds, first_omitted_order=order)
        for order in validate_orders(orders)
    )
