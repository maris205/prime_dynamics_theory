"""Claim-boundary logic for the quartet-shape frontier review."""

from __future__ import annotations


def review_coordinate(statuses: dict[str, bool]) -> str:
    required = (
        "normalization_negative",
        "shape_manifold_exact",
        "finite_clock_positive",
        "prediction_law_open",
        "boundary_theorem_exact",
        "transverse_quenching_exact",
        "recurrence_identification_negative",
        "fixed_degree_counting_negative",
        "gauge_completion_exact",
    )
    if not all(bool(statuses.get(key)) for key in required):
        return "quartet_shape_review_incomplete"
    if statuses.get("rank_growing_divisor_constructed"):
        return "rank_growing_divisor_open_local_uniform_limit"
    return "finite_gauge_complete_shape_flow_open_rank_growing_divisor"


def strict_gate_vector() -> dict[str, bool]:
    return {
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
        "hilbert_polya_operator": False,
        "zeta_zero_identification": False,
        "riemann_hypothesis": False,
    }
