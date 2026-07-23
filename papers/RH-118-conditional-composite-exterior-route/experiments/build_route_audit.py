"""Audit the complete finite gate and archive the remaining all-level packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from conditional_route import conditional_composite_gate  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "conditional_route_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "conditional_route_smoke.json"
THRESHOLDS = (1e-8, 1e-6, 1e-4)


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def transform_step(composite: dict[str, object], adaptive: dict[str, object]) -> dict[str, object]:
    candidates = {
        "direct_weyl": float(composite["candidates"]["direct_weyl"]),
        "spectral_capacity": float(composite["candidates"]["capacity_volume"]),
        "trace_concentration": float(composite["candidates"]["tail_energy_trace"]),
        "directional_rayleigh": float(composite["candidates"]["psd_packet_block"]),
    }
    gate = conditional_composite_gate(candidates, float(composite["threshold"]))
    first_depth = adaptive["first_certifying_depth"]
    first_lower = None
    if first_depth is not None:
        first_lower = float(adaptive["depths"][int(first_depth) - 1]["ratio_lower"])
    return {
        "time": int(composite["time"]),
        "threshold": float(composite["threshold"]),
        "candidates": candidates,
        "composite_lower": float(gate["lower"]),
        "selected_route": str(gate["selected_route"]),
        "composite_support": bool(gate["support_certified"]),
        "archived_composite_agrees": abs(float(gate["lower"]) - float(composite["composite_lower"])) < 2e-15,
        "adaptive_first_depth": first_depth,
        "adaptive_first_lower": first_lower,
        "adaptive_support": bool(adaptive["certificate_found"]),
        "composite_actual_support": bool(composite["actual_support"]),
        "adaptive_actual_support": bool(adaptive["actual_support"]),
        "support_labels_agree": bool(composite["actual_support"]) == bool(adaptive["actual_support"]),
        "composite_false_positive": bool(gate["support_certified"]) and not bool(composite["actual_support"]),
        "adaptive_false_positive": bool(adaptive["certificate_found"]) and not bool(adaptive["actual_support"]),
        "composite_missed_supported": bool(composite["actual_support"]) and not bool(gate["support_certified"]),
        "adaptive_missed_supported": bool(adaptive["actual_support"]) and not bool(adaptive["certificate_found"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    composite = load(PAPERS / "RH-115-composite-directional-support-gate/results/composite_gate_audit.json")
    adaptive = load(PAPERS / "RH-116-monotone-memory-depth-optimization/results/memory_depth_audit.json")
    row_count = 1 if args.smoke else 5
    rows = []
    for composite_row, adaptive_row in zip(composite["rows"][:row_count], adaptive["rows"][:row_count]):
        channels = []
        for composite_channel, adaptive_channel in zip(composite_row["channels"], adaptive_row["channels"]):
            thresholds = []
            for composite_record, adaptive_record in zip(
                composite_channel["thresholds"], adaptive_channel["thresholds"]
            ):
                if float(composite_record["threshold"]) != float(adaptive_record["threshold"]):
                    raise RuntimeError("threshold alignment failed")
                steps = [
                    transform_step(composite_step, adaptive_step)
                    for composite_step, adaptive_step in zip(
                        composite_record["steps"], adaptive_record["steps"]
                    )
                ]
                thresholds.append({"threshold": composite_record["threshold"], "steps": steps})
            channels.append({"side": composite_channel["side"], "thresholds": thresholds})
        rows.append({"sigma": composite_row["sigma"], "channels": channels})

    records = [
        (row["sigma"], record)
        for row in rows
        for channel in row["channels"]
        for record in channel["thresholds"]
    ]
    all_steps = [step for _, record in records for step in record["steps"]]
    threshold_summary = {}
    for threshold in THRESHOLDS:
        selected = [(sigma, record) for sigma, record in records if float(record["threshold"]) == threshold]
        steps = [step for _, record in selected for step in record["steps"]]
        fine = [step for sigma, record in selected if sigma <= 0.02 for step in record["steps"]]
        labels = ("direct_weyl", "spectral_capacity", "trace_concentration", "directional_rayleigh")
        threshold_summary[f"{threshold:.0e}"] = {
            "threshold": threshold,
            "update_count": len(steps),
            "actual_support_count": sum(step["adaptive_actual_support"] for step in steps),
            "candidate_support_counts": {
                label: sum(step["candidates"][label] >= threshold for step in steps) for label in labels
            },
            "composite_support_count": sum(step["composite_support"] for step in steps),
            "adaptive_support_count": sum(step["adaptive_support"] for step in steps),
            "composite_missed_supported_count": sum(step["composite_missed_supported"] for step in steps),
            "adaptive_missed_supported_count": sum(step["adaptive_missed_supported"] for step in steps),
            "fine_update_count": len(fine),
            "fine_composite_support_count": sum(step["composite_support"] for step in fine),
            "fine_adaptive_support_count": sum(step["adaptive_support"] for step in fine),
        }

    minimal_packets = {
        "direct_margin": {
            "compound_condition": "liminf direct_weyl_lower > tau",
            "primitive_physical_inputs": ["uniform recent fourth-mode support margin against the omitted tail"],
            "finite_algebra_closed": True,
            "five_scale_validated": not args.smoke,
            "all_level_condition_proved": False,
        },
        "trace_concentration": {
            "compound_condition": "liminf sqrt(theta_lower/kappa_upper)/capacity_upper > tau",
            "primitive_physical_inputs": [
                "normalized exterior-trace lower",
                "exterior-concentration upper",
                "route-closing capacity upper",
            ],
            "finite_algebra_closed": True,
            "five_scale_validated": not args.smoke,
            "all_level_condition_proved": False,
        },
        "directional_rayleigh": {
            "compound_condition": "liminf (1-gamma_upper)^4 frame_volume_lower/capacity_upper > tau",
            "primitive_physical_inputs": [
                "normalized recent-frame volume lower",
                "relative tail gamma upper below one",
                "route-closing capacity upper",
            ],
            "finite_algebra_closed": True,
            "five_scale_validated": not args.smoke,
            "all_level_condition_proved": False,
        },
    }
    fine_steps = [step for sigma, record in records if sigma <= 0.02 for step in record["steps"]]
    summary = {
        "scale_count": len(rows),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "actual_support_count": sum(step["adaptive_actual_support"] for step in all_steps),
        "composite_support_count": sum(step["composite_support"] for step in all_steps),
        "adaptive_support_count": sum(step["adaptive_support"] for step in all_steps),
        "selected_route_counts": {
            label: sum(step["selected_route"] == label for step in all_steps)
            for label in ("direct_weyl", "spectral_capacity", "trace_concentration", "directional_rayleigh")
        },
        "archived_composite_reconstruction_failure_count": sum(
            not step["archived_composite_agrees"] for step in all_steps
        ),
        "support_label_disagreement_count": sum(not step["support_labels_agree"] for step in all_steps),
        "composite_false_positive_count": sum(step["composite_false_positive"] for step in all_steps),
        "adaptive_false_positive_count": sum(step["adaptive_false_positive"] for step in all_steps),
        "composite_missed_supported_count": sum(step["composite_missed_supported"] for step in all_steps),
        "adaptive_missed_supported_count": sum(step["adaptive_missed_supported"] for step in all_steps),
        "physical_packet_count": len(minimal_packets),
        "all_level_physical_packet_count_proved": sum(
            packet["all_level_condition_proved"] for packet in minimal_packets.values()
        ),
    }
    payload = {
        "status": "rh118_conditional_composite_exterior_route_audit",
        "rows": rows,
        "threshold_summary": threshold_summary,
        "minimal_physical_packets": minimal_packets,
        "audit_summary": summary,
        "theorem_boundary": {
            "normalized_trace_factorization": True,
            "directional_rayleigh_factorization": True,
            "conditional_composite_liminf_theorem": True,
            "alternating_route_closure": True,
            "strict_margin_outward_robustness": True,
            "five_scale_complete_gate_audited": not args.smoke,
            "any_all_level_physical_packet_proved": False,
            "finite_anchor_extrapolation_admitted": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "All algebraic, compositional, first-passage, and finite-audit steps of the exterior route are now explicit. Eventual support follows from a strict liminf crossing by any admitted combination of direct, trace-concentration, or directional-Rayleigh candidates, even if the winning route alternates with level. None of the three minimal all-level physical packets is currently proved, and RH-117 excludes finite-anchor fitting as a substitute."
        ),
        "limitations": [
            "The finite adaptive route uses its own internally consistent assembly and is not numerically fused with RH-115 candidates without transport losses.",
            "The liminf theorem is conditional and does not establish any of its physical hypotheses.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
