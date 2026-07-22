"""Build the RH-82--RH-91 theorem ledger and 256-bit bootstrap budget."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from route_review import minimal_completion_bundles, updates_for_tolerance  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "route_review.json"
SMOKE_OUTPUT = ROOT / "results" / "route_review_smoke.json"
PRECISION_BITS = 256
ETA = 1.0 / 512.0
RHO = 0.24

LAYERS = [
    (82, "RH-82-half-log-postblock-rank-clock", "half-log endpoint rank clock", "rank clock", "physical all-level transfer"),
    (83, "RH-83-optimal-endpoint-singular-factorization", "optimal singular factorization", "factorization clarification", "singular majorization; coordinate branch false"),
    (84, "RH-84-ky-fan-tail-majorization", "Ky Fan captured-energy gate", "weaker invariant", "uniform physical tail energy"),
    (85, "RH-85-midblock-snapshot-packets", "strict-prefix snapshot transfer", "dynamic packet", "uniform prefix packet; unweighted Gram false"),
    (86, "RH-86-trace-normalized-late-memory-packets", "normalized-memory variational law", "gap-free online packet", "uniform memory law; angle route false"),
    (87, "RH-87-rayleigh-injection-recursion", "rank-staircase injection recursion", "scalar drift reduction", "uniform injection law"),
    (88, "RH-88-predictor-corrector-energy-contraction", "predictor-corrector identity", "correction dividend", "global norm and point predictor false"),
    (89, "RH-89-rank-one-complement-ritz-correction", "rank-one complement Ritz theorem", "small corrector", "uniform cross-block enrichment"),
    (90, "RH-90-schur-secular-subquarter-certificate", "Schur trial gain certificate", "full-reference-free finite closure", "uniform Schur sign"),
]

NEGATIVE_BRANCHES = [
    "direct endpoint/physical coordinate identity",
    "unweighted prefix Gramian",
    "tail principal-angle perturbation",
    "global operator-norm contraction",
    "uniform point-packet contraction",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    summaries = []
    ledger = []
    theorem_flags = []
    for number, directory, result, effect, boundary in LAYERS:
        path = PAPERS / directory / "results" / "summary.json"
        summary = json.loads(path.read_text(encoding="utf-8"))
        flags = summary["theorem"]
        theorem_flags.extend(flags.values())
        summaries.append({"paper": number, "path": str(path.relative_to(PAPERS.parent)), "sha256": sha256_file(path), "status": summary["status"]})
        ledger.append({"paper": f"RH-{number}", "result": result, "route_effect": effect, "open_or_negative_boundary": boundary, "theorem_flag_count": len(flags), "all_theorem_flags_green": all(flags.values())})

    tolerances = [1e-2, 1e-4] if args.smoke else [1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12]
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    budgets = []
    try:
        eta = arb(1) / 512
        rho = arb(6) / 25
        one_minus_eta = arb(1) - eta
        for tolerance in tolerances:
            updates = updates_for_tolerance(ETA, RHO, tolerance)
            bound = (rho**updates / one_minus_eta).sqrt()
            previous = (rho ** (updates - 1) / one_minus_eta).sqrt() if updates else bound
            budgets.append({
                "tolerance": tolerance,
                "updates": updates,
                "certified_bound_ball": str(bound),
                "certified_bound_upper": math.nextafter(float(bound.upper()), math.inf),
                "previous_update_bound_lower": math.nextafter(float(previous.lower()), -math.inf),
                "minimality_certified": float(bound.upper()) <= tolerance < float(previous.lower()),
            })
    finally:
        ctx.prec = previous_precision

    stage_a = minimal_completion_bundles([{"L"}, {"S", "R", "O"}])
    stage_a5 = minimal_completion_bundles([{"L"}, {"S", "R", "O"}], {"P", "C", "U"})
    payload = {
        "status": "rh91_schur_packet_route_review",
        "precision_bits": PRECISION_BITS,
        "eta": ETA,
        "rho": RHO,
        "source_summaries": summaries,
        "layer_ledger": ledger,
        "negative_branch_markers": NEGATIVE_BRANCHES,
        "bootstrap_budget": budgets,
        "archive_audit": {
            "paper_count": len(ledger),
            "theorem_flag_count": len(theorem_flags),
            "all_theorem_flags_green": all(theorem_flags),
            "all_uniform_stage_A_boundaries_open": all(not json.loads((PAPERS / directory / "results" / "summary.json").read_text(encoding="utf-8"))["program_boundary"].get("uniform_stage_A1_closed", False) for _, directory, *_ in LAYERS),
            "negative_branch_count": len(NEGATIVE_BRANCHES),
        },
        "route_frontier": {
            "symbols": {
                "L": "all-level RH-75 full-block law",
                "S": "uniform late Schur update/contraction law",
                "R": "polylogarithmic reduced packet future",
                "O": "polylogarithmic finite-prefix/normalization/observability bridge",
                "P": "actual moving-cloud Riesz projection",
                "C": "moving-cloud coefficient bridge",
                "U": "uniform trace-class complementary limit",
            },
            "stage_A_formula": "finite_chain_closed AND (L OR (S AND R AND O))",
            "stage_A_minimal_bundles": stage_a,
            "stage_A5_minimal_bundles": stage_a5,
            "preferred_next_gate": "S: prove the RH-90 Schur trial sign uniformly after burn-in; pursue R and O in parallel",
        },
        "key_metrics": {
            "rh82_maximum_frozen_relative_residual": json.loads((PAPERS / LAYERS[0][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["maximum_relative_residual"],
            "rh85_maximum_prefix_packet_relative_residual": json.loads((PAPERS / LAYERS[3][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["maximum_interval_relative_terminal_residual"],
            "rh86_minimum_angle_gap_ratio": json.loads((PAPERS / LAYERS[4][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["minimum_angle_perturbation_gap_ratio"],
            "rh88_global_norm_failure_count": json.loads((PAPERS / LAYERS[6][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["global_norm_failure_count"],
            "rh89_minimum_ritz_dividend_fraction": json.loads((PAPERS / LAYERS[7][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["minimum_interval_reference_dividend_fraction"],
            "rh90_maximum_corrected_contraction": json.loads((PAPERS / LAYERS[8][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["maximum_interval_corrected_contraction"],
            "rh90_minimum_schur_margin": json.loads((PAPERS / LAYERS[8][1] / "results" / "summary.json").read_text(encoding="utf-8"))["audit"]["minimum_negative_schur_margin"],
        },
        "theorem_boundary": {
            "schur_to_effective_rank_bootstrap": True,
            "revised_completion_frontier": True,
            "nine_summary_hash_audit": True,
            "uniform_schur_margin_proved": False,
            "polylog_reduced_future_proved": False,
            "uniform_observability_bridge_proved": False,
            "uniform_stage_A1_closed": False,
            "stage_A4_unconditional_closed": False,
            "relative_stage_A5_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "RH-82--RH-90 replace endpoint factorization by a direct dynamic packet route and reduce the postblock residual problem to a small uniform Schur sign. If a fixed rho<1 Schur update holds for m late clock-rank updates, the normalized postblock relative tail is at most rho^(m/2)/sqrt(1-eta). At eta=1/512 and rho=0.24, 20 updates certify 1e-6 and 39 certify 1e-12. Stage A nevertheless still needs the reduced packet future and prefix/observability bridge, while the alternative full-block corridor and all three A5 moving-cloud gates remain open."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "papers": len(ledger), "theorem_flags": len(theorem_flags), "all_green": payload["archive_audit"]["all_theorem_flags_green"], "budget_count": len(budgets)}, sort_keys=True))


if __name__ == "__main__":
    main()
