from __future__ import annotations


def coefficient_error(norm: float, rho: float, order: int) -> float:
    if norm < 0.0 or rho <= 0.0 or order < 2:
        raise ValueError("invalid coefficient parameters")
    return order * norm * rho ** (-order)


def head_transport_bound(
    total_trace_error: float,
    shell_error: float,
    annular_norm: float,
    rho: float,
    order: int,
) -> float:
    if total_trace_error < 0.0 or shell_error < 0.0:
        raise ValueError("errors must be nonnegative")
    return total_trace_error + shell_error + coefficient_error(
        annular_norm, rho, order
    )
