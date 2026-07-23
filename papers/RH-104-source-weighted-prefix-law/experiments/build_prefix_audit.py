"""Build RH-104 prefix certificates and the block-contraction barrier audit."""

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

from prefix_transient import (  # noqa: E402
    block_tail_energy_squared_upper,
    crude_prefix_power,
    crude_prefix_upper,
    directional_prefix_power,
    full_hardy_upper,
)


FULL_OUTPUT = ROOT / "results" / "prefix_transient_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "prefix_transient_smoke.json"


def load(path: str) -> dict[str, object]:
    return json.loads((PAPERS / path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    source = load("RH-75-log-square-block-contraction-law/results/log_square_block_audit.json")
    sigmas = source["rows"][:1] if args.smoke else source["rows"]
    rows = []
    for row in sigmas:
        channels = []
        for channel in row["channels"]:
            sigma = float(row["sigma"])
            observation_norm = math.sqrt(channel["observation_density_upper"] / sigma)
            source_energy = channel["source_block_upper"]
            contraction = channel["true_block_contraction_ball"]
            contraction_value = float(str(contraction).split()[0].lstrip("["))
            finite_squared = channel["finite_energy_squared_upper"]
            actual_prefix = math.sqrt(finite_squared)
            crude = crude_prefix_upper(observation_norm, source_energy)
            tail2 = block_tail_energy_squared_upper(observation_norm, contraction_value, source_energy)
            channels.append(
                {
                    "side": channel["side"],
                    "sigma": sigma,
                    "horizon": channel["selected_horizon"],
                    "observation_norm_upper": observation_norm,
                    "source_block_energy_upper": source_energy,
                    "block_contraction_upper": contraction_value,
                    "actual_directional_prefix_energy_upper": actual_prefix,
                    "crude_norm_product_prefix_upper": crude,
                    "crude_to_directional_prefix_ratio": crude / max(actual_prefix, np.finfo(float).tiny),
                    "block_tail_energy_squared_upper": tail2,
                    "full_crude_hardy_upper": full_hardy_upper(crude, tail2),
                    "full_actual_anchor_upper": full_hardy_upper(actual_prefix, channel["actual_tail_energy_squared_upper"]),
                }
            )
        rows.append({"sigma": row["sigma"], "level": row["level"], "channels": channels})

    sigmas_numeric = np.array([float(row["sigma"]) for row in rows])
    actual_prefixes = np.array([max(channel["actual_directional_prefix_energy_upper"] for channel in row["channels"]) for row in rows])
    crude_prefixes = np.array([max(channel["crude_norm_product_prefix_upper"] for channel in row["channels"]) for row in rows])
    source_energies = np.array([max(channel["source_block_energy_upper"] for channel in row["channels"]) for row in rows])
    observation_norms = np.array([max(channel["observation_norm_upper"] for channel in row["channels"]) for row in rows])

    barrier_sigmas = np.logspace(-1, -6, 6)
    barrier_power = 1.0
    barrier_prefix = barrier_sigmas ** (-(barrier_power + 0.5))
    barrier = {
        "family": "A_sigma=[[0,sigma^-a],[0,0]], X=e2, Y=sigma^-1/2 e1*",
        "a": barrier_power,
        "block_horizon": 2,
        "block_contraction": 0.0,
        "sigma_times_observation_norm_squared": 1.0,
        "normalized_packet_relative_tail": 0.0,
        "source_block_energy_scales_as": f"sigma^(-{2*barrier_power:.1f})",
        "prefix_energy_power": barrier_power + 0.5,
        "rows": [{"sigma": float(s), "prefix_energy": float(v)} for s, v in zip(barrier_sigmas, barrier_prefix)],
    }

    summary = {
        "anchor_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "maximum_actual_directional_prefix_energy": float(max(actual_prefixes)),
        "maximum_crude_prefix_upper": float(max(crude_prefixes)),
        "maximum_crude_to_directional_ratio": float(max(channel["crude_to_directional_prefix_ratio"] for row in rows for channel in row["channels"])),
        "maximum_source_block_energy": float(max(source_energies)),
        "maximum_observation_norm": float(max(observation_norms)),
        "source_block_zero_power_anchor_envelope": True,
        "directional_prefix_zero_power_anchor_envelope": True,
        "barrier_prefix_power": barrier["prefix_energy_power"],
    }
    payload = {
        "status": "rh104_source_weighted_prefix_transient_audit",
        "rows": rows,
        "barrier": barrier,
        "audit_summary": summary,
        "theorem_boundary": {
            "source_weighted_prefix_ledger_theorem": True,
            "block_tail_transfer_theorem": True,
            "physical_five_anchor_directional_prefix_validated": True,
            "uniform_directional_prefix_law_proved": False,
            "block_contraction_alone_closes_prefix": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The correct prefix target is a source-weighted directional law, not a crude product of observation norm and source block norm. "
            "The five anchors have bounded source-block and directional-prefix envelopes, but the explicit nilpotent family shows that block contraction, normalized packet tails, and observation scaling alone cannot prove that law."
        ),
        "limitations": [
            "The five-anchor source and directional envelopes are finite evidence, not an all-level theorem.",
            "The crude norm-product certificate is intentionally dimension-free but can lose the physical directional cancellation.",
            "The barrier family is abstract and does not claim failure of the folded-Gaussian family.",
            "No Stage A, moving-cloud, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
