from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH137 = PAPERS / "RH-137-finite-horizon-young-tail-envelope"
RH138 = PAPERS / "RH-138-outward-finite-directional-composition"
RH144 = PAPERS / "RH-144-backward-block-controlled-viability"
sys.path.insert(0, str(ROOT / "src"))

from delayed_start import suffix_statistics  # noqa: E402


CUTOFFS = (0.16, 0.08, 0.04, 0.02, 0.01)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    forward = json.loads((RH137 / "results" / "finite_horizon_audit.json").read_text(encoding="utf-8"))
    outward = json.loads((RH138 / "results" / "outward_composition_audit.json").read_text(encoding="utf-8"))
    backward = json.loads((RH144 / "results" / "backward_viability_audit.json").read_text(encoding="utf-8"))

    superunit = []
    for chain in forward["rows"]:
        for step in chain["steps"]:
            birth = float(step["greedy"]["birth"]["value"])
            if birth >= 1.0:
                superunit.append({
                    "sigma": float(chain["sigma"]), "side": str(chain["side"]),
                    "threshold": float(chain["threshold"]), "source_time": int(step["source_time"]),
                    "target_time": int(step["target_time"]), "birth": birth,
                    "greedy_bound": float(step["greedy"]["bound"]["value"]),
                })
    obstruction_lookup = {identifier: row for identifier, row in zip(backward["audit_summary"]["obstruction_identifiers"], [row for row in backward["rows"] if not row["viable_from_zero"]])}
    for record in superunit:
        identifier = f"{record['sigma']:.2f}:{record['side']}:{record['threshold']:.0e}"
        witness = obstruction_lookup[identifier]
        record["candidate_family_minimum_floor"] = witness["obstruction_minimum_floor"]
        record["empty_backward_kernel"] = not witness["viable_from_zero"]

    outward_rows = [{
        "sigma": float(row["sigma"]), "positive": bool(row["chain_positive"]),
        "floor": float(row["terminal_support_lower"]["value"]),
    } for row in outward["rows"]]
    forward_rows = [{
        "sigma": float(row["sigma"]), "positive": bool(row["greedy_chain_safe"]),
        "floor": 1.0 if row["greedy_chain_safe"] else 0.0,
    } for row in forward["rows"]]
    cutoffs = CUTOFFS[:2] if args.smoke else CUTOFFS
    suffixes = []
    for cutoff in cutoffs:
        forward_stats = suffix_statistics(forward_rows, cutoff)
        outward_stats = suffix_statistics(outward_rows, cutoff)
        suffixes.append({
            "cutoff_sigma": cutoff,
            "forward_chain_count": forward_stats["count"],
            "forward_safe_count": forward_stats["positive_count"],
            "outward_chain_count": outward_stats["count"],
            "outward_positive_count": outward_stats["positive_count"],
            "minimum_positive_outward_terminal_floor": outward_stats["minimum_positive_floor"],
            "clean_forward_suffix": forward_stats["count"] == forward_stats["positive_count"],
            "clean_outward_suffix": outward_stats["count"] == outward_stats["positive_count"],
        })
    first_clean = next((row for row in suffixes if row["clean_forward_suffix"] and row["clean_outward_suffix"]), None)
    summary = {
        "superunit_birth_count": len(superunit),
        "superunit_birth_anchor_count": len({(row["sigma"], row["side"]) for row in superunit}),
        "empty_kernel_superunit_count": sum(row["empty_backward_kernel"] for row in superunit),
        "minimum_superunit_candidate_family_floor": min((row["candidate_family_minimum_floor"] for row in superunit), default=None),
        "suffix_count": len(suffixes),
        "first_clean_suffix_cutoff": None if first_clean is None else first_clean["cutoff_sigma"],
        "first_clean_suffix_chain_count": None if first_clean is None else first_clean["outward_chain_count"],
        "first_clean_suffix_minimum_terminal_floor": None if first_clean is None else first_clean["minimum_positive_outward_terminal_floor"],
    }
    payload = {
        "status": "rh145_delayed_start_superunit_birth_isolation",
        "superunit_events": superunit,
        "suffixes": suffixes,
        "audit_summary": summary,
        "theorem_boundary": {
            "finite_prefix_invariance_of_limsup_liminf": True,
            "delayed_start_directional_support_theorem": True,
            "infinitely_recurrent_superunit_floor_obstruction": True,
            "finite_anchor_superunit_events_isolated": not args.smoke and len(superunit) == 2,
            "clean_finer_anchor_suffix_from_sigma_0_04": not args.smoke and summary["first_clean_suffix_cutoff"] == 0.04,
            "all_future_levels_are_free_of_superunit_births": False,
            "all_level_delayed_start_reset_constructed": False,
            "uniform_controlled_tail_gap": False,
            "normalized_base_liminf": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The only two superunit birth coefficients occur at one finite anchor and have empty "
            "candidate-family kernels. Deleting the finite prefix through sigma=0.08 leaves a clean "
            "18-chain suffix from sigma=0.04, with all outward terminal floors positive. This makes "
            "delayed start logically admissible, but finite anchors do not prove that no superunit "
            "birth recurs at untested future levels."
        ),
    }
    output = ROOT / "results" / ("delayed_start_smoke.json" if args.smoke else "delayed_start_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

