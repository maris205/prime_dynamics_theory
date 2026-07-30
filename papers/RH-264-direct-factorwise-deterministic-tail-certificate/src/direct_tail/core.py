"""Direct factorwise all-order tail majorants for the deterministic target."""

from __future__ import annotations

from dataclasses import dataclass

from flint import arb

from boundary_budget import certify_boundary_budget


@dataclass(frozen=True)
class DirectTail:
    first_omitted_order: int
    fredholm: arb
    astar: arb
    bfactor: arb
    even_total: arb
    odd: arb
    total: arb
    multiplicative_error: arb


def _up(value: arb) -> arb:
    return value.upper()


def _first_k(order: int, residue: int) -> int:
    k = 0
    while 3 * k + residue < order:
        k += 1
    return k


def odd_tail_exact_majorant(
    *, first_order: int, ratio: arb, lam: arb, cutoff: int = 401
) -> arb:
    """Sum the exact odd endpoint terms and bound the remaining geometric tail."""

    start = int(first_order)
    if start < 3 or start % 2 == 0:
        raise ValueError("first_order must be odd and at least three")
    stop = max(int(cutoff), start + 2)
    if stop % 2 == 0:
        stop += 1
    total = arb(0)
    for order in range(start, stop + 1, 2):
        total += ratio**order / (order * (1 + lam**(-order)))
    next_order = stop + 2
    total += ratio**next_order / (next_order * (1 - ratio**2))
    return _up(total)


def direct_tail_majorant(
    reduced_bounds: object,
    *,
    inner_radius: arb = arb(1),
    first_omitted_order: int = 29,
) -> DirectTail:
    """Bound the target logarithmic tail by factor, parity, and trace ideals."""

    radius = arb(inner_radius)
    order = int(first_omitted_order)
    if radius < 0 or order < 3:
        raise ValueError("require a nonnegative radius and order at least three")
    budget = certify_boundary_budget(reduced_bounds, scaled_circle=radius)
    one = arb(1)
    w = budget.squared_circle
    x = budget.cube_geometric_ratio
    nu = {
        1: budget.nuclear_norm,
        2: _up(budget.operator_norm * budget.nuclear_norm),
        3: _up(budget.operator_square_norm * budget.nuclear_norm),
    }
    n_min = (order + 1) // 2
    fredholm = arb(0)
    for residue in (1, 2, 3):
        k0 = _first_k(n_min, residue)
        fredholm += (
            nu[residue]
            * w**residue
            * x**k0
            / ((3 * k0 + residue) * (1 - x))
        )
    fredholm = _up(fredholm)
    y = _up(budget.radius_ratio**2)
    astar = _up(y**n_min / (n_min * (1 - y)))
    bfactor = _up(astar / (2 * (1 - reduced_bounds.lam**-2)))
    odd_start = order if order % 2 else order + 1
    odd = odd_tail_exact_majorant(
        first_order=max(3, odd_start),
        ratio=budget.radius_ratio,
        lam=reduced_bounds.lam,
    )
    even_total = _up(fredholm + astar + bfactor)
    total = _up(even_total + odd)
    multiplicative = _up(arb.exp(total) - one)
    return DirectTail(
        first_omitted_order=order,
        fredholm=fredholm,
        astar=astar,
        bfactor=bfactor,
        even_total=even_total,
        odd=odd,
        total=total,
        multiplicative_error=multiplicative,
    )
