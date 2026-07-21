"""256-bit Arb audit of a finite-horizon phase-aware Stein tail."""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results" / "arb_phase_tail_audit.json"


def contains_zero(value: arb) -> bool:
    return float(value.lower()) <= 0.0 <= float(value.upper())


def lower_positive(value: arb) -> bool:
    return float(value.lower()) > 0.0


def main() -> None:
    ctx.prec = 256
    a = arb("0.2")
    b = arb("0.7")
    coupling = arb("0.3")
    source_outer = arb("0.4")
    y1 = arb("0.8")
    y2 = arb("0.6")
    scale1 = arb("0.25")
    scale2 = arb(1)
    horizon = 8

    h1 = 1 / (1 - a * a)
    h2 = 1 / (1 - b * b)
    p1 = scale1 * scale1 * h1
    p2 = scale2 * scale2 * h2
    r11 = p1 * (1 - a * a)
    r12 = -p1 * a * coupling
    r22 = p2 * (1 - b * b) - p1 * coupling * coupling
    determinant = r11 * r22 - r12 * r12
    sharp_kappa = (
        y1 * y1 * r22
        - 2 * y1 * y2 * r12
        + y2 * y2 * r11
    ) / determinant
    safety_factor = arb("1.000001")
    kappa = safety_factor * sharp_kappa

    state0 = arb(0)
    state1 = source_outer
    finite_energy_squared = arb(0)
    for _ in range(horizon):
        output = y1 * state0 + y2 * state1
        finite_energy_squared += output * output
        state0, state1 = (
            a * state0 + coupling * state1,
            b * state1,
        )
    tail_metric_squared = kappa * (
        p1 * state0 * state0 + p2 * state1 * state1
    )

    o11 = y1 * y1 / (1 - a * a)
    o12 = (y1 * y2 + a * coupling * o11) / (1 - a * b)
    o22 = (
        y2 * y2
        + coupling * coupling * o11
        + 2 * b * coupling * o12
    ) / (1 - b * b)
    exact_energy_squared = source_outer * source_outer * o22
    exact_tail_squared = exact_energy_squared - finite_energy_squared
    tail_gap = tail_metric_squared - exact_tail_squared
    completion_gap = finite_energy_squared + tail_metric_squared - (
        exact_energy_squared
    )

    supersolution11 = kappa * r11 - y1 * y1
    supersolution12 = kappa * r12 - y1 * y2
    supersolution22 = kappa * r22 - y2 * y2
    supersolution_determinant = (
        supersolution11 * supersolution22 - supersolution12**2
    )
    local_residuals = (
        h1 - a * a * h1 - 1,
        h2 - b * b * h2 - 1,
    )

    payload = {
        "status": "arb_two_block_phase_aware_stein_tail_audit",
        "evidence_level": (
            "256-bit Arb evaluation of a two-scalar-block finite-horizon "
            "Gram and inherited Stein tail; no production interval audit"
        ),
        "precision_bits": 256,
        "model": {
            "diagonal_blocks": [str(a), str(b)],
            "upper_coupling": str(coupling),
            "outer_packet_source": str(source_outer),
            "observation": [str(y1), str(y2)],
            "scales": [str(scale1), str(scale2)],
            "horizon": horizon,
        },
        "local_metrics": [str(h1), str(h2)],
        "local_lyapunov_residual_balls": [
            str(value) for value in local_residuals
        ],
        "dissipation": {
            "r11": str(r11),
            "r12": str(r12),
            "r22": str(r22),
            "determinant": str(determinant),
        },
        "sharp_kappa_ball": str(sharp_kappa),
        "safety_factor": str(safety_factor),
        "certified_kappa_ball": str(kappa),
        "supersolution_residual": {
            "s11": str(supersolution11),
            "s12": str(supersolution12),
            "s22": str(supersolution22),
            "determinant": str(supersolution_determinant),
        },
        "finite_energy_squared_ball": str(finite_energy_squared),
        "exact_energy_squared_ball": str(exact_energy_squared),
        "exact_tail_squared_ball": str(exact_tail_squared),
        "tail_metric_squared_ball": str(tail_metric_squared),
        "tail_gap_ball": str(tail_gap),
        "completion_gap_ball": str(completion_gap),
        "local_lyapunov_identities_certified": all(
            contains_zero(value) for value in local_residuals
        ),
        "dissipation_positive_definite_certified": (
            lower_positive(r11)
            and lower_positive(r22)
            and lower_positive(determinant)
        ),
        "supersolution_positive_definite_certified": (
            lower_positive(supersolution11)
            and lower_positive(supersolution22)
            and lower_positive(supersolution_determinant)
        ),
        "tail_upper_certified": lower_positive(tail_gap),
        "completion_upper_certified": lower_positive(completion_gap),
        "production_interval_audit_executed": False,
        "arithmetic_scope": (
            "Only the displayed two-scalar-block model is interval evaluated. "
            "The folded-Gaussian finite Grams remain binary64 diagnostics."
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
