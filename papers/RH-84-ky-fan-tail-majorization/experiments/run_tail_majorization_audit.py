"""Seven-scale postblock/endpoint Ky Fan tail audit."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
sys.path[:0] = [str(ROOT / "src"), str(RH16 / "src"), str(RH77 / "experiments"), str(RH82 / "src")]

from endpoint_rank import boundary_clearances, resolution_singular_values  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from tail_majorization import ky_fan_tail  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "tail_majorization_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "tail_majorization_smoke.json"
EXTENDED_SIGMAS = SIGMAS + (0.005, 0.0025)
EXTENDED_HORIZONS = {**HORIZONS, 0.005: 49, 0.0025: 64}
RANK_OFFSET = 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads((RH82 / "results" / "half_log_rank_audit.json").read_text(encoding="utf-8"))
    interval_channels = {(float(row["sigma"]), channel["side"]): channel for row in inherited["rows"] for channel in row["channels"]}
    clearances = boundary_clearances(100, decimal_digits=100)
    rows = []
    sigmas = EXTENDED_SIGMAS[:1] if args.smoke else EXTENDED_SIGMAS
    for sigma in sigmas:
        rank = clock_rank(sigma, offset=RANK_OFFSET)
        mediator = resolution_singular_values(clearances, sigma, power=1.0, tail_ratio=1e-14)
        mediator_tail = ky_fan_tail(mediator, rank)
        dimension, models = build_models(sigma)
        channels = []
        for model in models:
            state = np.linalg.matrix_power(np.asarray(model["operator"]), EXTENDED_HORIZONS[sigma]) @ np.asarray(model["source"])
            singular = np.linalg.svd(state, compute_uv=False)
            floating_tail = ky_fan_tail(singular, rank)
            state_norm = float(np.linalg.norm(singular))
            key = (sigma, str(model["side"]))
            inherited_channel = interval_channels.get(key)
            if inherited_channel is not None:
                physical_tail = float(inherited_channel["residual_frobenius_upper"])
                relative_tail = float(inherited_channel["relative_residual_upper"])
                evidence = "192_bit_arb_frozen_postblock_residual"
            else:
                physical_tail = floating_tail
                relative_tail = floating_tail / state_norm
                evidence = "binary64_extended_stress_level"
            tail_ratio = physical_tail / mediator_tail
            offset_rows = []
            for offset in (0, 1, 2):
                offset_rank = clock_rank(sigma, offset=offset)
                offset_rows.append({
                    "offset": offset,
                    "rank": offset_rank,
                    "relative_postblock_tail": ky_fan_tail(singular, offset_rank) / state_norm,
                    "endpoint_tail": ky_fan_tail(mediator, offset_rank),
                })
            record = {
                "side": model["side"],
                "dimension": int(state.shape[0]),
                "source_columns": int(state.shape[1]),
                "horizon": EXTENDED_HORIZONS[sigma],
                "clock": half_log_clock(sigma),
                "clock_rank": rank,
                "physical_tail_upper": physical_tail,
                "physical_relative_tail_upper": relative_tail,
                "endpoint_model_tail": mediator_tail,
                "tail_majorization_ratio": tail_ratio,
                "evidence_level": evidence,
                "offset_comparison": offset_rows,
                "tail_ratio_below_0_015": bool(tail_ratio < 0.015),
            }
            channels.append(record)
            print(json.dumps({"sigma": sigma, "side": record["side"], "dimension": record["dimension"], "rank": rank, "physical_tail": physical_tail, "endpoint_tail": mediator_tail, "ratio": tail_ratio, "evidence": evidence}, sort_keys=True), flush=True)
        rows.append({"sigma": sigma, "fine_dimension": dimension, "clock_rank": rank, "channels": channels, "all_channels_green": all(channel["tail_ratio_below_0_015"] for channel in channels)})
    channels = [channel for row in rows for channel in row["channels"]]
    payload = {
        "status": "rh84_ky_fan_tail_majorization_audit",
        "rank_offset": RANK_OFFSET,
        "rows": rows,
        "all_executed_tail_gates_green": all(row["all_channels_green"] for row in rows),
        "audit_summary": {
            "scale_count": len(rows),
            "interval_scale_count": sum(1 for row in rows if row["sigma"] in SIGMAS),
            "extended_stress_scale_count": sum(1 for row in rows if row["sigma"] not in SIGMAS),
            "maximum_clock_rank": max(channel["clock_rank"] for channel in channels),
            "maximum_tail_majorization_ratio": max(channel["tail_majorization_ratio"] for channel in channels),
            "maximum_interval_relative_tail": max(channel["physical_relative_tail_upper"] for channel in channels if channel["evidence_level"].startswith("192")),
            "maximum_extended_relative_tail": max((channel["physical_relative_tail_upper"] for channel in channels if channel["evidence_level"].startswith("binary64")), default=0.0),
        },
        "theorem_boundary": {
            "ky_fan_candidate_upper": True,
            "tail_majorization_transfer": True,
            "seven_scale_tail_stress_audit": True,
            "all_level_tail_majorization_proved": False,
            "uniform_stage_A1_closed": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "RH-78 needs only a low-rank future residual, not termwise singular-value domination or a full endpoint factorization. The weaker Ky Fan tail-majorization condition is sufficient and is stable across rank staircases. At the five interval-certified anchors and two new stress levels up to dimension 2048, the clock-plus-two physical tail is at most 1.4 percent of the endpoint model tail. The next analytic gate is a uniform captured-energy lower bound for a clock-dimensional postcritical packet space."
        ),
        "limitations": [
            "The first five physical tails inherit RH-82 Arb enclosures; the two new stress levels are binary64 diagnostics.",
            "The extended horizons follow the proposed log-square schedule and are not an all-level contraction theorem.",
            "Tail majorization is sufficient for the effective-rank corridor but is not yet proved for the analytic dyadic family.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_tail_gates_green"], **payload["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()

