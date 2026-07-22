"""Build the RH-62--RH-70 theorem ledger and Stage A1 frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from route_review import TerminalBracket, first_open_frontier  # noqa: E402


OUTPUT = ROOT / "results" / "route_review.json"
SMOKE_OUTPUT = ROOT / "results" / "route_review_smoke.json"
RH70_AUDIT = (
    PAPERS
    / "RH-70-frozen-production-block-hardy-audit"
    / "results"
    / "frozen_production_interval_audit.json"
)


PAPERS_LEDGER = {
    62: {
        "directory": "RH-62-krylov-residual-stein-tails",
        "route_effect": "advance",
        "primary_result": "Arnoldi residual identity and directional power upper",
        "remaining_boundary": "residual propagation remained nondirectional",
    },
    63: {
        "directory": "RH-63-nested-krylov-residual-closure",
        "route_effect": "advance",
        "primary_result": "coherent nested residual closure and breakdown exactness",
        "remaining_boundary": "uniform recursion depth remained open",
    },
    64: {
        "directory": "RH-64-weighted-terminal-residuals",
        "route_effect": "advance",
        "primary_result": "Lyapunov-weighted terminal contraction",
        "remaining_boundary": "metric conditioning became the controlling cost",
    },
    65: {
        "directory": "RH-65-physical-family-metric-conditioning",
        "route_effect": "no_go_boundary",
        "primary_result": "sharp Jordan coupling/gap conditioning threshold",
        "remaining_boundary": "global weighting cannot replace localized deflation",
    },
    66: {
        "directory": "RH-66-block-cross-column-krylov-gram",
        "route_effect": "advance",
        "primary_result": "block Galerkin identity and phase-preserving Gram upper",
        "remaining_boundary": "uniform PSD majorization could lose physical sharpness",
    },
    67: {
        "directory": "RH-67-physical-covariance-block-envelopes",
        "route_effect": "advance_and_correct",
        "primary_result": "covariance-optimal PSD allocation and sharpness/size duality",
        "remaining_boundary": "physical sharpness can force global PSD growth",
    },
    68: {
        "directory": "RH-68-phase-coherence-block-depth-barrier",
        "route_effect": "exact_no_go",
        "primary_result": "Fourier-ring obstruction to universal fixed Krylov depth",
        "remaining_boundary": "phase compression or growing depth must be proved",
    },
    69: {
        "directory": "RH-69-adaptive-certificate-portfolio",
        "route_effect": "synthesis",
        "primary_result": "safe Pareto pruning and green/red/amber triage",
        "remaining_boundary": "production interval execution was still absent",
    },
    70: {
        "directory": "RH-70-frozen-production-block-hardy-audit",
        "route_effect": "validated_advance",
        "primary_result": "outward-rounded frozen production block-Hardy upper",
        "remaining_boundary": "upstream construction and uniform scaling remain open",
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def paper_ledger() -> list[dict[str, object]]:
    rows = []
    for number, record in PAPERS_LEDGER.items():
        directory = PAPERS / str(record["directory"])
        summary_path = directory / "results" / "summary.json"
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        theorem = summary.get("theorem", {})
        boundary = summary.get("program_boundary", {})
        if not theorem or not all(theorem.values()):
            raise RuntimeError(f"RH-{number} theorem ledger is incomplete")
        if boundary.get("stage_A1_closed", True):
            raise RuntimeError(f"RH-{number} unexpectedly claims Stage A1")
        rows.append(
            {
                "paper": number,
                **record,
                "summary_status": summary["status"],
                "theorem_count": len(theorem),
                "all_theorem_gates_true": all(theorem.values()),
                "stage_A1_closed": boundary["stage_A1_closed"],
                "summary_sha256": sha256_file(summary_path),
            }
        )
    return rows


def bridge_budget_rows(smoke: bool) -> list[dict[str, object]]:
    payload = json.loads(RH70_AUDIT.read_text(encoding="utf-8"))
    rows = payload["rows"][:1] if smoke else payload["rows"]
    output = []
    for row in rows:
        for channel in row["channels"]:
            bracket = TerminalBracket(
                finite_lower=float(channel["finite_energy_lower"]),
                full_upper=float(channel["full_energy_upper"]),
            )
            budgets = {}
            for tolerance in (0.01, 0.02, 0.05):
                key = f"{int(round(100 * tolerance))}_percent"
                budgets[key] = {
                    "absolute_bridge_slack": bracket.bridge_slack(tolerance),
                    "relative_bridge_slack": bracket.relative_bridge_slack(
                        tolerance
                    ),
                    "positive": bracket.bridge_slack(tolerance) > 0.0,
                }
            output.append(
                {
                    "sigma": row["sigma"],
                    "side": channel["side"],
                    "horizon": channel["horizon"],
                    "finite_energy_lower": bracket.finite_lower,
                    "frozen_full_upper": bracket.full_upper,
                    "completion_factor_upper": channel[
                        "relative_enclosure_width_upper"
                    ],
                    "budgets": budgets,
                }
            )
    return output


def dependency_frontiers() -> tuple[dict[str, tuple[str, ...]], set[str], dict[str, list[str]]]:
    dependencies = {
        "bridge_instance": (
            "augmented_bridge_theorem",
            "upstream_interval_triple",
        ),
        "finite_scale_validated_hardy": (
            "terminal_frozen_upper",
            "bridge_instance",
        ),
        "stage_A1": (
            "finite_scale_validated_hardy",
            "uniform_family_scaling",
        ),
        "stage_A4_unconditional": (
            "stage_A1",
            "peripheral_factor_transfer",
            "adaptive_cutoff_transfer",
            "identification_composition_theorem",
        ),
        "renormalized_determinant_limit": (
            "stage_A4_unconditional",
            "pole_renormalized_limit_theorem",
        ),
    }
    closed = {
        "augmented_bridge_theorem",
        "terminal_frozen_upper",
        "peripheral_factor_transfer",
        "adaptive_cutoff_transfer",
        "identification_composition_theorem",
    }
    frontiers = {
        "finite_scale": sorted(
            first_open_frontier(
                "finite_scale_validated_hardy", dependencies, closed
            )
        ),
        "stage_A1": sorted(
            first_open_frontier("stage_A1", dependencies, closed)
        ),
        "stage_A4_unconditional": sorted(
            first_open_frontier(
                "stage_A4_unconditional", dependencies, closed
            )
        ),
        "renormalized_determinant_limit": sorted(
            first_open_frontier(
                "renormalized_determinant_limit", dependencies, closed
            )
        ),
    }
    return dependencies, closed, frontiers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    ledger = paper_ledger()
    bridge = bridge_budget_rows(args.smoke)
    dependencies, closed, frontiers = dependency_frontiers()
    one_percent = [
        row["budgets"]["1_percent"]["relative_bridge_slack"]
        for row in bridge
    ]
    payload = {
        "status": "rh71_directional_tail_certificate_stack_route_review",
        "scope": (
            "RH-62 through RH-70 are audited as the nine inputs; RH-71 is "
            "the tenth synthesis layer."
        ),
        "paper_ledger": ledger,
        "theorem": {
            "stacked_bridge_upper": True,
            "common_bridge_pareto_invariance": True,
            "relative_bridge_slack_criterion": True,
            "polylogarithmic_stack_closure": True,
            "first_open_frontier_decomposition": True,
        },
        "bridge_budget_rows": bridge,
        "bridge_budget_summary": {
            "all_one_percent_diagnostic_slacks_positive": all(
                value > 0.0 for value in one_percent
            ),
            "minimum_one_percent_relative_slack": min(one_percent),
            "minimum_one_percent_relative_slack_percent": 100.0
            * min(one_percent),
            "engineering_target_only": (
                "the one-percent ledger is a finite-scale sharpness target, "
                "not a necessary condition for Stage A1"
            ),
        },
        "dependencies": {
            key: list(value) for key, value in dependencies.items()
        },
        "closed_nodes": sorted(closed),
        "frontiers": frontiers,
        "stage_ledger": {
            "A1_terminal_finite_matrix_mechanism": "green",
            "A1_frozen_production_execution": "green",
            "A1_upstream_interval_inclusion": "amber",
            "A1_uniform_small_noise_family_bound": "amber",
            "A2_sufficient_peripheral_factor_transfer": "green",
            "A3_analytic_adaptive_cutoff_transfer": "green",
            "A3_production_interval_composition": "amber",
            "A4_conditional_identification_composition": "green",
            "A4_unconditional_identification": "amber",
            "A5_renormalized_determinant_limit": "not_started",
            "B_scattering_completion": "not_started",
            "C_self_adjoint_counting": "not_started",
            "D_arithmetic_zeta_identity": "not_started",
        },
        "closed_false_routes": [
            "one-step or plain geometric norm propagation as a uniform proof",
            "unlocalized full-space Lyapunov weighting as a polylogarithmic shortcut",
            "universal fixed block Krylov depth from stability data alone",
            "trace-global PSD sharpness without a physical/global-size tradeoff",
        ],
        "surviving_route": [
            "validated upstream folded-Gaussian and peripheral-factor inclusion",
            "augmented H2 difference bridge to the frozen terminal certificate",
            "analytic uniform horizon or phase-compression budget",
            "conditional RH-54 identification composition",
            "pole-renormalized determinant limit only after Stage A4",
        ],
        "next_priority": (
            "Validate the folded-Gaussian matrix and rank-two peripheral "
            "deflation before attempting more terminal-tail variants."
        ),
        "program_boundary": {
            "finite_scale_end_to_end_hardy_closed": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "renormalized_determinant_limit_closed": False,
            "canonical_scattering_object": False,
            "self_adjoint_generator": False,
            "T_log_T_counting_law": False,
            "prime_power_trace_formula": False,
            "completed_zeta_identity": False,
            "riemann_hypothesis": False,
        },
        "source_hashes": {
            "rh70_interval_audit": sha256_file(RH70_AUDIT),
        },
        "route_consequence": (
            "The finite-scale terminal layer is no longer the active wall. "
            "The finite-scale frontier is one upstream inclusion gate, while "
            "full Stage A1 has a second independent gate: uniform family scaling."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "paper_count": len(ledger),
                "bridge_row_count": len(bridge),
                "finite_frontier": frontiers["finite_scale"],
                "stage_A1_frontier": frontiers["stage_A1"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
