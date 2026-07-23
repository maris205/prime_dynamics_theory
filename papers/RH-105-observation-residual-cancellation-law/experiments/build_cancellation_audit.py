"""Compose RH-77 observability factors with RH-82 clock residuals."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from observation_cancellation import (  # noqa: E402
    full_observability_factor,
    matched_scale_factors,
    nonnegative_cancellation_power,
    signed_cancellation_power,
    weighted_residual_upper,
)


FULL_OUTPUT = ROOT / "results" / "observation_residual_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "observation_residual_smoke.json"
BALL = re.compile(r"\[\s*([+\-0-9.eE]+)\s*\+/-\s*([+\-0-9.eE]+)\s*\]")


def load(path: str) -> dict[str, object]:
    return json.loads((PAPERS / path).read_text(encoding="utf-8"))


def ball_upper(text: str) -> float:
    match = BALL.fullmatch(str(text).strip())
    if match is None:
        raise ValueError(f"cannot parse ball: {text}")
    return math.nextafter(float(match.group(1)) + abs(float(match.group(2))), math.inf)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    effective = load("RH-77-postblock-effective-rank-compression/results/effective_rank_audit.json")
    clock = load("RH-82-half-log-postblock-rank-clock/results/half_log_rank_audit.json")
    effective_rows = effective["rows"][:1] if args.smoke else effective["rows"]
    clock_rows = clock["rows"][:1] if args.smoke else clock["rows"]
    clock_index = {
        (float(row["sigma"]), channel["side"]): channel
        for row in clock_rows
        for channel in row["channels"]
    }

    rows = []
    all_channels = []
    for level, row in enumerate(effective_rows):
        sigma = float(row["sigma"])
        channels = []
        for channel in row["channels"]:
            key = (sigma, channel["side"])
            clock_channel = clock_index[key]
            full_observability = ball_upper(channel["full_observability_norm_upper_ball"])
            omega = full_observability_factor(full_observability)
            residual = float(clock_channel["residual_frobenius_upper"])
            weighted = weighted_residual_upper(omega, residual)
            archived = float(clock_channel["full_future_hardy_perturbation_upper"])
            scaled_observation, scaled_residual = matched_scale_factors(sigma, omega, residual)
            relative_discrepancy = abs(weighted - archived) / max(archived, math.ulp(0.0))
            record = {
                "side": channel["side"],
                "sigma": sigma,
                "horizon": channel["horizon"],
                "clock_rank": clock_channel["clock_rank"],
                "full_observability_norm_upper": full_observability,
                "observation_factor_upper": omega,
                "clock_residual_frobenius_upper": residual,
                "weighted_residual_upper": weighted,
                "archived_full_future_perturbation_upper": archived,
                "relative_recomposition_discrepancy": relative_discrepancy,
                "sqrt_sigma_observation_factor": scaled_observation,
                "residual_over_sqrt_sigma": scaled_residual,
                "weighted_residual_below_1e_minus_8": weighted < 1.0e-8,
            }
            channels.append(record)
            all_channels.append(record)
        rows.append({"level": level, "sigma": sigma, "channels": channels})

    scenarios = []
    for name, observation_power, residual_power in (
        ("matched_square_root", 0.5, 0.5),
        ("strict_overcancellation", 0.5, 0.75),
        ("undercancellation", 0.5, 0.25),
        ("bounded_observation", 0.0, 0.0),
    ):
        signed = signed_cancellation_power(observation_power, residual_power)
        scenarios.append(
            {
                "name": name,
                "observation_growth_power": observation_power,
                "residual_decay_power": residual_power,
                "signed_product_power": signed,
                "nonnegative_growth_power": nonnegative_cancellation_power(observation_power, residual_power),
                "zero_power": signed <= 0.0,
            }
        )

    barrier_rows = []
    for exponent in range(1, 7):
        sigma = 10.0 ** (-exponent)
        omega = sigma ** (-0.5)
        residual = sigma**0.25
        barrier_rows.append(
            {
                "sigma": sigma,
                "observation_factor": omega,
                "residual": residual,
                "weighted_residual": omega * residual,
            }
        )
    barrier = {
        "family": "T_sigma(z)=sigma^-o |z|, B_sigma=sigma^rho, B_r=0",
        "observation_growth_power": 0.5,
        "residual_decay_power": 0.25,
        "weighted_growth_power": 0.25,
        "rows": barrier_rows,
    }

    summary = {
        "anchor_count": len(rows),
        "channel_count": len(all_channels),
        "maximum_clock_rank": max(channel["clock_rank"] for channel in all_channels),
        "maximum_observation_factor": max(channel["observation_factor_upper"] for channel in all_channels),
        "maximum_sqrt_sigma_observation_factor": max(channel["sqrt_sigma_observation_factor"] for channel in all_channels),
        "maximum_clock_residual": max(channel["clock_residual_frobenius_upper"] for channel in all_channels),
        "maximum_residual_over_sqrt_sigma": max(channel["residual_over_sqrt_sigma"] for channel in all_channels),
        "maximum_weighted_residual": max(channel["weighted_residual_upper"] for channel in all_channels),
        "maximum_recomposition_discrepancy": max(channel["relative_recomposition_discrepancy"] for channel in all_channels),
        "all_weighted_residuals_below_1e_minus_8": all(channel["weighted_residual_below_1e_minus_8"] for channel in all_channels),
        "sharp_barrier_weighted_growth_power": barrier["weighted_growth_power"],
    }
    payload = {
        "status": "rh105_observation_residual_cancellation_audit",
        "rows": rows,
        "scenarios": scenarios,
        "sharpness_barrier": barrier,
        "audit_summary": summary,
        "theorem_boundary": {
            "signed_observation_residual_cancellation_theorem": True,
            "matched_scale_factorization_theorem": True,
            "sharp_rate_matching_boundary": True,
            "five_anchor_clock_cancellation_validated": True,
            "uniform_observation_growth_law_proved": False,
            "uniform_clock_residual_decay_law_proved": False,
            "uniform_observation_residual_law_closed": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Observation growth and packet residual decay must be composed as a signed product before powers are truncated. "
            "The exact growth power is max(0,o-rho), so residual decay rho at least as large as observation growth o gives a zero-power future error. "
            "At the five anchors the square-root-normalized observation factor is at most 2.126, the normalized residual is at most 3.078e-9, and every weighted residual is below 5.044e-9. "
            "The all-level observation and residual hypotheses remain separate open laws."
        ),
        "limitations": [
            "The five-anchor recomposition validates archived finite matrices only.",
            "A tiny finite weighted product does not prove an all-level residual decay exponent.",
            "The scalar sharpness family is abstract and does not assert failure of the folded-Gaussian family.",
            "No Stage A, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
