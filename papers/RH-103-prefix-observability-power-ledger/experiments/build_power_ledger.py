"""Build the RH-103 max-plus power ledger and independence counterexamples."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from power_ledger import (  # noqa: E402
    quarter_power_margin,
    rh49_full_range_green,
    side_hardy_power,
    stress_mesh_decay_power,
    two_side_hardy_power,
    zero_power_overheads,
)


FULL_OUTPUT = ROOT / "results" / "prefix_observability_power_ledger.json"
SMOKE_OUTPUT = ROOT / "results" / "prefix_observability_power_smoke.json"
PREFIX_COUNTEREXAMPLE_POWER = 1.25
OBSERVATION_COUNTEREXAMPLE_POWER = 0.75


def load(relative: str) -> dict[str, object]:
    return json.loads((PAPERS / relative).read_text(encoding="utf-8"))


def keyed(rows: list[dict[str, object]]) -> dict[float, dict[str, object]]:
    return {float(row["sigma"]): row for row in rows}


def fit_power(sigmas: np.ndarray, values: np.ndarray) -> float:
    slope, _ = np.polyfit(np.log(sigmas), np.log(values), 1)
    return float(-slope)


def scenario(name: str, left: dict[str, float], right: dict[str, float]) -> dict[str, object]:
    left_power = side_hardy_power(**left)
    right_power = side_hardy_power(**right)
    total = two_side_hardy_power(left_power, right_power)
    return {
        "name": name,
        "left_terms": left,
        "right_terms": right,
        "left_hardy_power": left_power,
        "right_hardy_power": right_power,
        "total_hardy_power": total,
        "quarter_power_margin": quarter_power_margin(total),
        "rh49_full_strict_mesh_range_green": rh49_full_range_green(total),
        "stress_mesh_decay_power": stress_mesh_decay_power(total),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()

    rh74 = load("RH-74-validated-upstream-hardy-bridge/results/validated_upstream_bridge_audit.json")
    rh75 = load("RH-75-log-square-block-contraction-law/results/log_square_block_audit.json")
    rh77 = load("RH-77-postblock-effective-rank-compression/results/effective_rank_audit.json")
    rh78 = load("RH-78-two-corridor-stage-A1-composition/results/stage_composition_audit.json")
    rh82 = load("RH-82-half-log-postblock-rank-clock/results/half_log_rank_audit.json")
    rh101 = load("RH-101-finite-memory-packet-gram-action/results/finite_memory_gram_audit.json")
    rh102 = load("RH-102-stopped-hybrid-quotient-clock/results/stopped_hybrid_clock_audit.json")

    rows74 = keyed(rh74["rows"])
    rows75 = keyed(rh75["rows"])
    rows77 = keyed(rh77["rows"])
    rows78 = keyed(rh78["rows"])
    rows82 = keyed(rh82["rows"])
    rows102 = keyed(rh102["rows"])
    sigmas = sorted(rows78, reverse=True)
    if args.smoke:
        sigmas = sigmas[:1]

    rows = []
    for sigma in sigmas:
        prefix = rows75[sigma]
        upstream = rows74[sigma]
        effective = rows77[sigma]
        composition = rows78[sigma]
        clock = rows82[sigma]
        stopped = rows102[sigma]
        prefix_energy = max(math.sqrt(channel["finite_energy_squared_upper"]) for channel in prefix["channels"])
        upstream_bridge = max(channel["robust_hardy_bridge"]["bridge_energy_upper"] for channel in upstream["channels"])
        observability_sqrt = max(
            math.sqrt(float(str(channel["full_observability_norm_upper_ball"]).split()[0].lstrip("[")))
            for channel in effective["channels"]
        )
        stopped_primary_ratio = max(
            channel["chains"]["1e-08"]["interval_final_endpoint_to_reference_upper"]
            for channel in stopped["channels"]
        )
        rows.append(
            {
                "sigma": sigma,
                "level": int(composition["level"]),
                "source_normalization_power": 0.0,
                "finite_prefix_energy_upper": prefix_energy,
                "conditional_zero_power_hardy_upper": composition["conditional_hardy_upper"],
                "future_observability_sqrt_upper": observability_sqrt,
                "clock_rank": int(clock["clock_rank"]),
                "clock_future_residual_upper": max(
                    channel["full_future_hardy_perturbation_upper"] for channel in clock["channels"]
                ),
                "upstream_bridge_upper": upstream_bridge,
                "finite_memory_depth": rh101["audit_summary"]["minimum_successful_uniform_depth"],
                "stopped_primary_endpoint_ratio_upper": stopped_primary_ratio,
                "stress_mesh_identification_envelope_upper": composition["identification_stress_envelope_upper"],
                "all_finite_anchor_gates_green": bool(
                    prefix["all_channels_green"]
                    and upstream["all_channels_green"]
                    and clock["all_channels_green"]
                    and stopped["all_threshold_clocks_green"]
                    and composition["quarter_power_gate"]
                ),
            }
        )

    zero = {
        "normalization": 0.0,
        "upstream_bridge": 0.0,
        "finite_prefix": 0.0,
        "reduced_future": 0.0,
        "observability": 0.0,
        "packet_residual": 0.0,
    }
    balanced_left = {**zero, "finite_prefix": 0.125}
    balanced_right = {**zero, "observability": 0.08, "packet_residual": 0.045}
    scenarios = [
        scenario("zero_power_target", zero, zero),
        scenario("balanced_quarter_boundary", balanced_left, balanced_right),
        scenario("one_sided_observability_leak", {**zero, "observability": 0.20, "packet_residual": 0.10}, zero),
        scenario("two_sided_prefix_leak", {**zero, "finite_prefix": 0.16}, {**zero, "finite_prefix": 0.12}),
        scenario(
            "observation_residual_cancellation",
            {**zero, "observability": 0.5, "packet_residual": -0.5},
            {**zero, "observability": 0.4, "packet_residual": -0.4},
        ),
        scenario(
            "max_not_sum_within_one_side",
            {**zero, "finite_prefix": 0.12, "reduced_future": 0.11, "observability": 0.07, "packet_residual": 0.05},
            {**zero, "finite_prefix": 0.10},
        ),
    ]

    counter_sigmas = np.logspace(-1, -6, 6)
    prefix_energy = counter_sigmas ** (-PREFIX_COUNTEREXAMPLE_POWER)
    observation_energy = counter_sigmas ** (-OBSERVATION_COUNTEREXAMPLE_POWER) / math.sqrt(1.0 - 0.5**2)
    counterexamples = {
        "prefix_transient": {
            "family": "A_sigma=[[0,sigma^-a],[0,0]], X=e2, Y=e1*",
            "power": PREFIX_COUNTEREXAMPLE_POWER,
            "normalized_packet_gram": 1.0,
            "packet_relative_tail": 0.0,
            "postblock_state_after_two_steps": 0.0,
            "rows": [
                {"sigma": float(sigma), "hardy_energy": float(value)}
                for sigma, value in zip(counter_sigmas, prefix_energy)
            ],
            "fitted_hardy_power": fit_power(counter_sigmas, prefix_energy),
        },
        "observation_scaling": {
            "family": "A=1/2, X=1, Y_sigma=sigma^-b",
            "power": OBSERVATION_COUNTEREXAMPLE_POWER,
            "normalized_packet_gram": 1.0,
            "packet_relative_tail": 0.0,
            "rows": [
                {"sigma": float(sigma), "hardy_energy": float(value)}
                for sigma, value in zip(counter_sigmas, observation_energy)
            ],
            "fitted_hardy_power": fit_power(counter_sigmas, observation_energy),
        },
    }

    summary = {
        "anchor_count": len(rows),
        "all_finite_anchor_gates_green": all(row["all_finite_anchor_gates_green"] for row in rows),
        "maximum_conditional_zero_power_hardy_upper": max(row["conditional_zero_power_hardy_upper"] for row in rows),
        "maximum_upstream_bridge_upper": max(row["upstream_bridge_upper"] for row in rows),
        "maximum_clock_future_residual_upper": max(row["clock_future_residual_upper"] for row in rows),
        "maximum_clock_rank": max(row["clock_rank"] for row in rows),
        "finite_memory_depth": rh101["audit_summary"]["minimum_successful_uniform_depth"],
        "maximum_stopped_primary_endpoint_ratio": max(row["stopped_primary_endpoint_ratio_upper"] for row in rows),
        "stress_identification_envelope_first": rows[0]["stress_mesh_identification_envelope_upper"],
        "stress_identification_envelope_last": rows[-1]["stress_mesh_identification_envelope_upper"],
        "prefix_counterexample_fitted_power": counterexamples["prefix_transient"]["fitted_hardy_power"],
        "observation_counterexample_fitted_power": counterexamples["observation_scaling"]["fitted_hardy_power"],
        "scenario_green_count": sum(item["rh49_full_strict_mesh_range_green"] for item in scenarios),
        "scenario_count": len(scenarios),
    }
    payload = {
        "status": "rh103_prefix_observability_sigma_power_ledger",
        "rows": rows,
        "max_plus_theorem": {
            "side_expression": "alpha_s=max(u_s,n_s+p_s,n_s+z_s,n_s+o_s+r_s)",
            "two_side_expression": "delta=alpha_left+alpha_right",
            "rh49_full_range_condition": "delta<=1/4",
            "stress_mesh_decay_expression": "sigma^(3/4-delta) L(sigma)^-2",
        },
        "closed_zero_power_overheads": {
            "normalized_coupling_source": True,
            "logarithmic_packet_rank": True,
            "fixed_depth_five_memory_action": True,
            "fixed_1p01_stopped_endpoint_gate": True,
            "strict_mesh_substitution_algebra": True,
            "all_zero_power": zero_power_overheads(
                logarithmic_rank=True,
                fixed_memory_depth=True,
                fixed_endpoint_gate=True,
                normalized_source=True,
            ),
        },
        "open_uniform_terms": {
            "finite_prefix_directional_power": "p_s",
            "reduced_packet_future_power": "z_s",
            "future_observability_power": "o_s",
            "absolute_packet_residual_power": "r_s",
            "uniform_upstream_bridge_power": "u_s",
        },
        "scenarios": scenarios,
        "counterexamples": counterexamples,
        "audit_summary": summary,
        "theorem_boundary": {
            "max_plus_sigma_power_ledger_theorem": True,
            "normalization_rank_memory_stop_mesh_overheads_power_zero": True,
            "prefix_independence_counterexample": True,
            "observation_independence_counterexample": True,
            "five_anchor_ledger_composed": True,
            "prefix_observability_gate_closed": False,
            "only_uniform_quotient_gate_remains": False,
            "uniform_stage_A_closed": False,
            "moving_cloud_A5_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The inherited prefix/normalization/observability gate is no longer a vague polylogarithmic placeholder. Its exact Hardy power is a max-plus expression, while the two sides add and must fit the shared RH-49 quarter-power budget. "
            "Normalization, logarithmic rank, depth-five memory, stopped constants, and mesh substitution carry zero sigma power. However normalized packet mechanics cannot control finite-prefix transients or absolute observation scale; explicit families keep every packet tail zero while assigning arbitrary positive Hardy power. "
            "Therefore RH-101 and RH-102 do not reduce the preferred Stage-A bundle to Q alone: uniform prefix and observation-weighted future estimates remain independent scalar gates."
        ),
        "limitations": [
            "The five-anchor ledger validates arithmetic and status, not any missing all-level exponent estimate.",
            "The counterexamples are abstract stable systems showing logical independence; they do not assert that the physical folded-Gaussian family realizes the bad scaling.",
            "The max-plus theorem records powers but does not provide the uniform prefix, reduced-future, observability, residual, or upstream bounds.",
            "No Stage A, moving-cloud, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
