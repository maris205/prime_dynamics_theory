from __future__ import annotations


def trace_power_bound(n: int, m: int, K: float, eta: float, L: float) -> float:
    if n < m or m < 1 or not (0 <= eta < 1):
        raise ValueError("invalid block parameters")
    ell, r = divmod(n, m)
    return K * (eta ** max(ell - 1, 0)) * L**r


def block_tail_bound(m: int, R: float, K: float, eta: float, L: float) -> float:
    if m < 1 or eta * R**m >= 1:
        raise ValueError("tail series does not converge")
    prefix = sum((L * R) ** r for r in range(m))
    return K * R**m * prefix / (m * (1 - eta * R**m))
