"""Build the RH-1--RH-99 inventory and revised completion frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from hundred_layer_review import minimal_completion_bundles  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "hundred_layer_route_review.json"
SMOKE_OUTPUT = ROOT / "results" / "hundred_layer_route_review_smoke.json"


PHASES = (
    (1, 12, "foundational symbolic dynamics, regularized cycles, and small-noise limits"),
    (13, 23, "parity boundary layers, critical branches, and complement self-energy"),
    (24, 34, "validated contour, Rouché, resolvent, and Grushin certificates"),
    (35, 49, "physical counting, continuum bridges, Riesz projectors, and intrinsic identification"),
    (50, 61, "Hardy energies, Stein metrics, phase fusion, and horizon barriers"),
    (62, 71, "Krylov/covariance closures, certificate portfolios, and upstream validation"),
    (72, 81, "finite Stage-A closure and the moving-cloud determinant frontier"),
    (82, 91, "rank clocks, late-memory packets, Ritz correction, and Schur certification"),
    (92, 99, "recursive horizon packets, weak-mode quotients, and propagation barriers"),
)


EXACT_MILESTONES = [
    {"layer": 1, "result": "published Paper-1 claims are separated from the kneading admissibility hypothesis"},
    {"layer": 10, "result": "exact parity-renormalized cycle counts and noncommuting long-cycle/small-noise limits"},
    {"layer": 20, "result": "exact two-channel critical-branch factorization and dark-mode algebra"},
    {"layer": 30, "result": "exact sparse two-step Grushin linearization with stored inverse certificates"},
    {"layer": 40, "result": "gauge-invariant weighted Riesz projector continuum bridge"},
    {"layer": 50, "result": "directional Hardy/Stein theorem and global-contraction no-go"},
    {"layer": 60, "result": "phase-aware finite-horizon plus positive Stein-tail completion"},
    {"layer": 70, "result": "outward-rounded frozen block Hardy theorem"},
    {"layer": 78, "result": "conditional two-corridor Stage-A composition"},
    {"layer": 80, "result": "moving-cloud relative determinant factorization"},
    {"layer": 84, "result": "Ky Fan tail majorization"},
    {"layer": 90, "result": "Schur-secular correction certificate without ambient reference packet"},
    {"layer": 93, "result": "multi-direction recursive Ritz refresh theorem"},
    {"layer": 94, "result": "source-seed equivalence and full-prefix recursive horizon theorem"},
    {"layer": 95, "result": "exact reduced cross-moment factorization"},
    {"layer": 96, "result": "gap-weighted weak-mode quotient theorem"},
    {"layer": 97, "result": "exact nonlinear hybrid horizon telescoping"},
    {"layer": 98, "result": "projector envelope and strict positive unit-propagation counterexample"},
    {"layer": 99, "result": "two-gap differential projected-cross Ritz bound"},
]


NEGATIVE_MARKERS = [
    {"layer": 4, "branch": "unrenormalized spectral limit", "meaning": "raw spectral shortcuts do not define the desired limit"},
    {"layer": 10, "branch": "interchange of small-noise and long-cycle limits", "meaning": "the limits need not commute"},
    {"layer": 19, "branch": "single critical sibling", "meaning": "an omitted sibling is order one"},
    {"layer": 50, "branch": "uniform fixed-step global contraction", "meaning": "deterministic isometry forbids this Hardy proof"},
    {"layer": 56, "branch": "fixed hard-space growing horizon", "meaning": "ambient hard-space control carries a scaling barrier"},
    {"layer": 61, "branch": "direction-free horizon envelope", "meaning": "forbidden scale power appears"},
    {"layer": 68, "branch": "fixed-depth phase coherence", "meaning": "coherence blocks do not stay uniformly shallow"},
    {"layer": 76, "branch": "single-arc phase compression", "meaning": "broad-arc and moment barriers reject the mechanism"},
    {"layer": 80, "branch": "fixed scalar pole cancellation", "meaning": "exterior exponential growth forces a moving cloud"},
    {"layer": 88, "branch": "global norm and point-packet contraction", "meaning": "both shortcuts fail"},
    {"layer": 93, "branch": "one-direction recursive refresh", "meaning": "four fine channels miss the block target"},
    {"layer": 95, "branch": "binary64 moment-only closure", "meaning": "weak modes cause normal-equation and cancellation failure"},
    {"layer": 96, "branch": "aggressive local quotient cutoffs", "meaning": "locally certified losses can fail cumulatively"},
    {"layer": 98, "branch": "universal unit tail propagation", "meaning": "a positive trace-one Ritz example amplifies by over 44"},
    {"layer": 99, "branch": "first-order finite neighborhood tube", "meaning": "five Ritz gaps are unavailable and radii miss all quotient steps"},
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def phase_for(number: int) -> str:
    for first, last, label in PHASES:
        if first <= number <= last:
            return label
    raise ValueError(number)


def title_from_readme(path: Path) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    quoted = re.search(r">\s*\*([^*]+)\*", text.replace("\n", " "))
    if quoted:
        return " ".join(quoted.group(1).split())
    heading = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return heading.group(1).strip() if heading else ""


def route_formula() -> tuple[dict[str, object], dict[str, object]]:
    leaf = lambda name, status: {"kind": "leaf", "name": name, "status": status}
    stage_a = {
        "kind": "and",
        "children": [
            leaf("finite_stage_A_chain", "closed"),
            {
                "kind": "or",
                "children": [
                    leaf("L_all_level_full_block_law", "open"),
                    {
                        "kind": "and",
                        "children": [
                            leaf("Q_uniform_gap_aware_quotient_law", "open"),
                            leaf("G_structured_packet_Gram_action", "open"),
                            {
                                "kind": "or",
                                "children": [
                                    leaf("H_stopped_hybrid_horizon_law", "open"),
                                    leaf("H_finite_neighborhood_differential_tube", "open"),
                                ],
                            },
                            leaf("O_prefix_normalization_observability_bridge", "open"),
                        ],
                    },
                ],
            },
        ],
    }
    stage_a5 = {
        "kind": "and",
        "children": [
            stage_a,
            leaf("C_actual_moving_cloud_Riesz_projection", "open"),
            leaf("K_cloud_coefficient_bridge", "open"),
            leaf("T_uniform_trace_class_complement", "open"),
        ],
    }
    return stage_a, stage_a5


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    directories = sorted(
        (path for path in PAPERS.iterdir() if path.is_dir() and re.match(r"RH-(\d+)-", path.name)),
        key=lambda path: int(re.match(r"RH-(\d+)-", path.name).group(1)),
    )
    inventory = []
    for directory in directories:
        number = int(re.match(r"RH-(\d+)-", directory.name).group(1))
        if number > 99 or (args.smoke and number > 10):
            continue
        readme = directory / "README.md"
        main_tex = directory / "main.tex"
        summary = directory / "results" / "summary.json"
        pdfs = sorted(path for path in directory.glob("*.pdf") if path.is_file())
        inventory.append(
            {
                "number": number,
                "directory": directory.name,
                "title": title_from_readme(readme),
                "phase": phase_for(number),
                "has_readme": readme.exists(),
                "has_main_tex": main_tex.exists(),
                "has_summary": summary.exists(),
                "pdf_count": len(pdfs),
                "readme_sha256": sha256_file(readme) if readme.exists() else None,
                "main_tex_sha256": sha256_file(main_tex) if main_tex.exists() else None,
                "summary_sha256": sha256_file(summary) if summary.exists() else None,
            }
        )

    stage_a, stage_a5 = route_formula()
    stage_a_bundles = [sorted(bundle) for bundle in minimal_completion_bundles(stage_a)]
    stage_a5_bundles = [sorted(bundle) for bundle in minimal_completion_bundles(stage_a5)]
    phase_counts = []
    for first, last, label in PHASES:
        rows = [row for row in inventory if first <= row["number"] <= last]
        if rows:
            phase_counts.append({"first": first, "last": last, "phase": label, "paper_count": len(rows), "summary_count": sum(row["has_summary"] for row in rows), "pdf_count": sum(row["pdf_count"] > 0 for row in rows)})

    payload = {
        "status": "rh100_hundred_layer_route_review",
        "inventory": inventory,
        "inventory_summary": {
            "paper_count": len(inventory),
            "first_layer": min(row["number"] for row in inventory),
            "last_layer": max(row["number"] for row in inventory),
            "readme_count": sum(row["has_readme"] for row in inventory),
            "main_tex_count": sum(row["has_main_tex"] for row in inventory),
            "summary_count": sum(row["has_summary"] for row in inventory),
            "paper_pdf_count": sum(row["pdf_count"] > 0 for row in inventory),
            "phase_counts": phase_counts,
        },
        "exact_milestones": EXACT_MILESTONES,
        "negative_route_markers": NEGATIVE_MARKERS,
        "stage_A_formula": stage_a,
        "stage_A_minimal_completion_bundles": stage_a_bundles,
        "stage_A5_formula": stage_a5,
        "stage_A5_minimal_completion_bundles": stage_a5_bundles,
        "preferred_packet_bundle": sorted(["Q_uniform_gap_aware_quotient_law", "G_structured_packet_Gram_action", "H_stopped_hybrid_horizon_law", "O_prefix_normalization_observability_bridge"]),
        "fallback_bundle": ["L_all_level_full_block_law"],
        "next_three_layers": [
            {"layer": 101, "target": "G_structured_packet_Gram_action", "paper": "finite-memory realization of the normalized Gram action on a packet"},
            {"layer": 102, "target": "H_stopped_hybrid_horizon_law", "paper": "stopped quotient clock with an exact remaining endpoint budget"},
            {"layer": 103, "target": "O_prefix_normalization_observability_bridge", "paper": "prefix and observability composition with explicit sigma-power ledger"},
        ],
        "later_stages": {
            "A5": "actual moving-cloud projection, coefficient bridge, and uniform trace-class complement all open",
            "B": "canonical scattering completion not started",
            "C": "self-adjoint realization and intrinsic T log T counting not started",
            "D": "prime-power trace identity and completed-zeta identification not started",
        },
        "claim_boundary": {
            "unconditional_stage_A_closed": False,
            "moving_cloud_A5_closed": False,
            "canonical_scattering_function": False,
            "self_adjoint_hilbert_polya_operator": False,
            "T_log_T_counting_law": False,
            "prime_power_trace_formula": False,
            "zeta_zero_identification": False,
            "riemann_hypothesis": False,
        },
        "executive_verdict": (
            "The hundred-layer program has produced a substantial exact finite-dimensional theory, a fully validated five-anchor Stage-A chain, and a precise moving-cloud determinant frontier. "
            "The preferred packet corridor is still viable, but RH-95--RH-99 show that smooth uniform propagation is the wrong default: weak modes, cumulative quotient losses, nonunit propagation, and unavailable Ritz gaps must be handled explicitly. "
            "The next best route is the stopped-hybrid packet bundle, while the RH-75 all-level full-block law remains the clean fallback."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **payload["inventory_summary"], "stage_A_bundle_count": len(stage_a_bundles), "stage_A5_bundle_count": len(stage_a5_bundles)}, sort_keys=True))


if __name__ == "__main__": main()
