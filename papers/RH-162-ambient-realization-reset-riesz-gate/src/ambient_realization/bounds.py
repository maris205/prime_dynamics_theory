"""Scalar bounds for an ambient source-to-transfer realization."""

from __future__ import annotations

import math


def realization_coupling_bounds(
    primal_packet_defect: float,
    adjoint_packet_defect: float,
) -> dict[str, float]:
    """Return the two directed off-packet coupling bounds.

    The inputs bound ``||(AJ-JM)P||`` and ``||(A*J-JM*)P||`` after an
    isometric realization.  They control the outward and inward couplings,
    respectively.
    """

    primal = float(primal_packet_defect)
    adjoint = float(adjoint_packet_defect)
    if not all(math.isfinite(value) for value in (primal, adjoint)):
        raise ValueError("defects must be finite")
    if min(primal, adjoint) < 0.0:
        raise ValueError("defects must be nonnegative")
    return {
        "packet_to_complement_upper": primal,
        "complement_to_packet_upper": adjoint,
        "feedback_product_upper": primal * adjoint,
    }


def polar_repair_bounds(gram_error: float) -> dict[str, float | bool]:
    """Bounds for replacing a near-isometry J by J(J*J)^(-1/2)."""

    eta = float(gram_error)
    if not math.isfinite(eta) or eta < 0.0:
        raise ValueError("gram error must be finite and nonnegative")
    if eta >= 1.0:
        return {
            "repair_certified": False,
            "inverse_square_root_upper": math.inf,
            "correction_upper": math.inf,
        }
    inverse = 1.0 / math.sqrt(1.0 - eta)
    return {
        "repair_certified": True,
        "inverse_square_root_upper": inverse,
        "correction_upper": inverse - 1.0,
    }
