from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import statistics
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from correlated_tube import support, support_factor, tube_base_requirement  # noqa: E402


RH138 = PAPERS / "RH-138-outward-finite-directional-composition/results/outward_composition_audit.json"
RH146 = PAPERS / "RH-146-projective-gram-base-recurrence/results/projective_gram_audit.json"
BETAS = (1e-10, 1e-8, 1e-6, 1e-4)


def key(row: dict[str, object]) -> tuple[float, str, float]:
    return float(row["sigma"]), str(row["side"]), float(row["threshold"])


def chain(row: dict[str, object], projective: dict[str, object]) -> dict[str, object]:
    steps = []
    supports = []
    tails = []
    bases = []
    failures = 0
    for item in row["steps"]:
        tail = float(item["validated_target_bound"]["value"])
        base = float(item["base_lower"]["value"])
        recomputed = support(tail, base)
        archived = float(item["support_lower"]["value"])
        tolerance = 1e-12 * max(1.0, abs(recomputed), abs(archived))
        failures += abs(recomputed - archived) > tolerance
        supports.append(recomputed)
        tails.append(tail)
        bases.append(base)
        steps.append({
            "source_time": int(item["source_time"]),
            "target_time": int(item["target_time"]),
            "tail_upper": tail,
            "base_lower": base,
            "support_lower": recomputed,
            "archive_support_lower": archived,
            "support_recomputation_holds": abs(recomputed - archived) <= tolerance,
            "tube_base_requirements": {
                f"{beta:.0e}": tube_base_requirement(beta, tail) for beta in BETAS
            },
        })
    positive = all(value > 0.0 for value in supports)
    multipliers = [] if not positive else [supports[i] / supports[i - 1] for i in range(1, len(supports))]
    logs = []
    running = 0.0
    for multiplier in multipliers:
        running += math.log(multiplier)
        logs.append(running)
    tube_beta = min(supports)
    rectangular_beta = support(max(tails), min(bases))
    projective_lower = float(projective["terminal_projective_lower"])
    return {
        "sigma": float(row["sigma"]),
        "side": str(row["side"]),
        "threshold": float(row["threshold"]),
        "transition_count": len(steps),
        "positive_tube": positive,
        "maximal_common_tube_beta": tube_beta,
        "rectangular_packet_beta": rectangular_beta,
        "correlation_gain_over_rectangle": None if rectangular_beta == 0.0 else tube_beta / rectangular_beta,
        "projective_terminal_lower": projective_lower,
        "reanchoring_gain_over_projective": None if not positive else tube_beta / projective_lower,
        "minimum_log_cocycle_from_first_state": None if not logs else min(0.0, min(logs)),
        "terminal_log_cocycle_from_first_state": None if not logs else logs[-1],
        "local_support_multipliers": multipliers,
        "support_recomputation_failure_count": failures,
        "tube_membership": {f"{beta:.0e}": all(value >= beta for value in supports) for beta in BETAS},
        "steps": steps,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    outward = json.loads(RH138.read_text())
    projective = json.loads(RH146.read_text())
    projective_rows = {key(row): row for row in projective["rows"]}
    source_rows = outward["rows"]
    if args.smoke:
        source_rows = [row for row in source_rows if row["sigma"] in (0.16, 0.08) and row["side"] == "left" and row["threshold"] == 1e-8]
    rows = [chain(row, projective_rows[key(row)]) for row in source_rows]
    steps = [step for row in rows for step in row["steps"]]
    positive_rows = [row for row in rows if row["positive_tube"]]
    positive_multipliers = [value for row in positive_rows for value in row["local_support_multipliers"]]
    positive_betas = [row["maximal_common_tube_beta"] for row in positive_rows]
    correlation_gains = [row["correlation_gain_over_rectangle"] for row in positive_rows if row["correlation_gain_over_rectangle"] is not None]
    reanchoring_gains = [row["reanchoring_gain_over_projective"] for row in positive_rows if row["reanchoring_gain_over_projective"] is not None]
    clean_suffix = [row for row in rows if row["sigma"] <= 0.04]
    summary = {
        "scale_count": len({row["sigma"] for row in rows}),
        "chain_count": len(rows),
        "transition_count": len(steps),
        "positive_tube_transition_count": sum(step["support_lower"] > 0.0 for step in steps),
        "positive_tube_chain_count": len(positive_rows),
        "support_recomputation_failure_count": sum(row["support_recomputation_failure_count"] for row in rows),
        "common_1e_10_tube_chain_count": sum(row["tube_membership"]["1e-10"] for row in rows),
        "common_1e_8_tube_chain_count": sum(row["tube_membership"]["1e-08"] for row in rows),
        "common_1e_6_tube_chain_count": sum(row["tube_membership"]["1e-06"] for row in rows),
        "common_1e_4_tube_chain_count": sum(row["tube_membership"]["1e-04"] for row in rows),
        "minimum_positive_tube_beta": min(positive_betas),
        "median_positive_tube_beta": float(np.median(positive_betas)),
        "maximum_positive_tube_beta": max(positive_betas),
        "clean_suffix_chain_count": len(clean_suffix),
        "clean_suffix_positive_chain_count": sum(row["positive_tube"] for row in clean_suffix),
        "clean_suffix_minimum_tube_beta": min((row["maximal_common_tube_beta"] for row in clean_suffix), default=None),
        "local_multiplier_count": len(positive_multipliers),
        "local_recovery_multiplier_count": sum(value > 1.0 for value in positive_multipliers),
        "local_loss_multiplier_count": sum(value < 1.0 for value in positive_multipliers),
        "minimum_local_support_multiplier": min(positive_multipliers),
        "median_local_support_multiplier": float(np.median(positive_multipliers)),
        "maximum_local_support_multiplier": max(positive_multipliers),
        "minimum_correlation_gain_over_rectangle": min(correlation_gains),
        "median_correlation_gain_over_rectangle": float(np.median(correlation_gains)),
        "maximum_correlation_gain_over_rectangle": max(correlation_gains),
        "minimum_reanchoring_gain_over_projective": min(reanchoring_gains),
        "median_reanchoring_gain_over_projective": float(np.median(reanchoring_gains)),
        "maximum_reanchoring_gain_over_projective": max(reanchoring_gains),
    }
    payload = {
        "status": "rh147_correlated_base_tail_viability_tube_audit",
        "tube_levels": list(BETAS),
        "rows": rows,
        "audit_summary": summary,
        "sharp_witnesses": {
            "tube_boundary": "a=beta/phi(y)",
            "multiplier_equality": "y'=F(y), a'=r a",
            "negative_cocycle_obstruction": "kappa_n=1/2 gives support 2^{-n}",
        },
        "theorem_boundary": {
            "correlated_support_tube_theorem": True,
            "sharp_correlated_tube_multiplier_proved": True,
            "lower_bounded_log_cocycle_support_theorem": True,
            "negative_log_cocycle_obstruction": True,
            "finite_outward_tube_audited": not args.smoke,
            "all_level_support_cocycle_verified": False,
            "cross_scale_reset_constructed": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "A single support tube K_beta transports the controlled tail and normalized base through a signed logarithmic cocycle, retaining recovery steps that unsigned projective variation discards. The outward finite archive has 28 complete K_1e-10 chains and an 18-chain clean suffix above 1.5e-10. Direct statewise reanchoring improves the RH-146 projective product by 16--48 orders, but an all-level cross-scale cocycle remains unproved.",
    }
    output = ROOT / "results" / ("correlated_tube_smoke.json" if args.smoke else "correlated_tube_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
