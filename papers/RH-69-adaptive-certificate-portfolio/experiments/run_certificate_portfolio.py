"""Compose archived upper and lower certificates into an adaptive ledger."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from certificate_portfolio import (  # noqa: E402
    Candidate,
    pareto_frontier,
    select_feasible,
    triage,
)


FULL_OUTPUT = ROOT / "results" / "certificate_portfolio.json"
SMOKE_OUTPUT = ROOT / "results" / "certificate_portfolio_smoke.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_dict(candidate: Candidate | None) -> dict[str, object] | None:
    if candidate is None:
        return None
    return {
        "name": candidate.name,
        "upper": candidate.upper,
        "costs": dict(candidate.costs),
        "evidence": candidate.evidence,
    }


def phase_horizon_portfolio(smoke: bool) -> list[dict[str, object]]:
    phase = load(
        PAPERS
        / "RH-60-finite-horizon-phase-aware-tails"
        / "results"
        / "phase_tail_pilot.json"
    )
    horizon = load(
        PAPERS
        / "RH-61-directional-horizon-scaling-barrier"
        / "results"
        / "horizon_scaling_audit.json"
    )
    horizon_rows = {row["sigma"]: row for row in horizon["rows"]}
    selected_rows = phase["rows"][:1] if smoke else phase["rows"]
    output = []
    for row in selected_rows:
        for side in ("left", "right"):
            candidates = []
            for length in phase["horizons"]:
                record = row[side]["horizons"][str(length)]
                candidates.append(
                    Candidate(
                        name=f"phase_L{length}",
                        upper=float(
                            record["phase_aware_upper"]
                            / row[side]["exact_hardy_energy"]
                        ),
                        costs={"horizon": float(length)},
                        evidence="archived_binary64_phase_diagnostic",
                    )
                )
            selected = select_feasible(
                candidates,
                1.01,
                "horizon",
            )
            geometric = horizon_rows[row["sigma"]][side][
                "geometric_horizons"
            ]["0.01"]
            output.append(
                {
                    "sigma": row["sigma"],
                    "side": side,
                    "target_gain": 1.01,
                    "selected": candidate_dict(selected),
                    "pareto_frontier": [
                        candidate_dict(candidate)
                        for candidate in pareto_frontier(candidates)
                    ],
                    "geometric_horizon_for_same_tolerance": geometric,
                    "geometric_over_selected_horizon": (
                        geometric / selected.costs["horizon"]
                        if selected is not None
                        else None
                    ),
                    "claim_level": (
                        "selection among archived binary64 diagnostics; "
                        "not a production validated upper"
                    ),
                }
            )
    return output


def covariance_portfolio(smoke: bool) -> list[dict[str, object]]:
    payload = load(
        PAPERS
        / "RH-67-physical-covariance-block-envelopes"
        / "results"
        / "covariance_envelope_pilot.json"
    )
    targets = {
        "exact_diagonal_cancellation": 1.01,
        "nonnormal_three_packet_chain": 4.0,
        "six_mode_complex_phase_packets": 1.3,
    }
    models = payload["models"][:1] if smoke else payload["models"]
    output = []
    for model in models:
        candidates = []
        for row in model["rows"]:
            epsilon = float(row["epsilon"])
            candidates.append(
                Candidate(
                    name=f"covariance_eps_{epsilon:.0e}",
                    upper=float(row["physical_gain"]),
                    costs={
                        "focus_exponent": max(0.0, -math.log10(epsilon)),
                        "global_gain": float(row["global_spectral_gain"]),
                    },
                    evidence=(
                        "exact_scalar_reduction"
                        if model["exact_scalar_reduction"]
                        else "binary64_block_diagnostic"
                    ),
                )
            )
        selected = select_feasible(
            candidates,
            targets[model["name"]],
            "focus_exponent",
        )
        output.append(
            {
                "name": model["name"],
                "target_gain": targets[model["name"]],
                "selected": candidate_dict(selected),
                "pareto_frontier": [
                    candidate_dict(candidate)
                    for candidate in pareto_frontier(candidates)
                ],
            }
        )
    return output


def depth_triage(smoke: bool) -> dict[str, object]:
    payload = load(
        PAPERS
        / "RH-68-phase-coherence-block-depth-barrier"
        / "results"
        / "depth_barrier_pilot.json"
    )
    ring_rows = payload["exact_rings"][:1] if smoke else payload["exact_rings"]
    rings = []
    for row in ring_rows:
        budget = row["horizon"]
        result = triage(
            [
                Candidate(
                    name=f"depth_{budget}",
                    upper=1.0,
                    costs={"depth": float(budget)},
                    evidence="analytic_fourier_ring",
                )
            ],
            0.1,
            "depth",
            budgets={"depth": float(budget)},
            approximation_lower_bound=1.0,
            approximation_target=0.1,
        )
        rings.append(
            {
                "dimension": row["dimension"],
                "horizon": row["horizon"],
                "depth_budget": budget,
                "status": result.status,
                "lower_bound": result.lower_bound,
                "reason": result.reason,
            }
        )
    jitter_rows = payload["jittered_rings"][:1] if smoke else payload[
        "jittered_rings"
    ]
    jitters = []
    for row in jitter_rows:
        depth_row = next(value for value in row["depths"] if value["depth"] == 32)
        result = triage(
            [
                Candidate(
                    name="depth_32_observed",
                    upper=float(depth_row["projection_error"]),
                    costs={"depth": 32.0},
                    evidence="binary64_projection_diagnostic",
                )
            ],
            0.1,
            "depth",
            budgets={"depth": 32.0},
            approximation_lower_bound=float(
                depth_row["spectral_lower_bound"]
            ),
            approximation_target=0.1,
        )
        jitters.append(
            {
                "jitter": row["jitter_in_phase_cells"],
                "status": result.status,
                "spectral_lower_bound": result.lower_bound,
                "observed_error": depth_row["projection_error"],
                "reason": result.reason,
            }
        )
    arcs = []
    for row in payload["phase_arcs"]:
        required = row["required_depth_for_10_percent_error"]
        status = "green" if required <= 8 else "amber"
        arcs.append(
            {
                "arc_width_radians": row["arc_width_radians"],
                "required_depth": required,
                "depth_budget": 8,
                "status": status,
                "reason": (
                    "an observed depth meets the diagnostic target"
                    if status == "green"
                    else "stored diagnostics miss the budget, but no analytic lower bound is claimed"
                ),
            }
        )
    return {
        "target_projection_error": 0.1,
        "exact_rings": rings,
        "jittered_rings": jitters,
        "phase_arcs": arcs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    phase = phase_horizon_portfolio(args.smoke)
    covariance = covariance_portfolio(args.smoke)
    depth = depth_triage(args.smoke)
    payload = {
        "status": "rh69_adaptive_upper_lower_certificate_portfolio",
        "evidence_level": (
            "analytic portfolio logic over archived exact, Arb, and binary64 "
            "inputs; source claim levels are preserved per row"
        ),
        "phase_horizon_portfolio": phase,
        "covariance_portfolio": covariance,
        "depth_triage": depth,
        "theorem_boundary": {
            "safe_pareto_pruning": True,
            "green_red_amber_triage": True,
            "finite_prefix_tail_composition": True,
            "conditional_budget_closure": True,
            "production_upper_validation": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "The candidate architecture is now explicit: try finite phase "
            "fusion, prune impossible block depths with a lower gate, then "
            "optimize the surviving block/covariance upper on a Pareto ledger."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "phase_rows": len(phase),
                "covariance_rows": len(covariance),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
