"""Build the RH-192--201 source-channel review ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from source_channel_review import macro_boundary, next_frontier, route_coordinate  # noqa: E402


def load(number: int, directory: str, name: str) -> dict[str, object]:
    return json.loads((PAPERS / f"RH-{number}-{directory}" / "results" / name).read_text(encoding="utf-8"))


def run() -> dict[str, object]:
    rh192 = load(192, "frobenius-left-multiplication-obstruction", "frobenius_obstruction_audit.json")
    rh193 = load(193, "source-cyclic-spectral-quotient", "source_cyclic_identity_audit.json")
    rh194 = load(194, "physical-edge-root-matching", "physical_edge_matching.json")
    rh195 = load(195, "source-observation-riesz-channels", "riesz_channel_identity_audit.json")
    rh196 = load(196, "canonical-biorthogonal-spectral-packet", "canonical_packet_identity_audit.json")
    rh197 = load(197, "physical-residue-transversality-audit", "physical_transversality_audit.json")
    rh198 = load(198, "temporal-spectral-packet-alignment", "packet_alignment_audit.json")
    rh199 = load(199, "source-channel-determinant-trace-factorization", "channel_determinant_audit.json")
    rh200 = load(200, "conjugate-pair-edge-quartet-selection", "edge_quartet_audit.json")
    finite_item_count = sum([
        int(rh192["window_count"]), int(rh192["root_case_count"]),
        int(rh193["case_count"]),
        int(rh194["accepted_window_count"]), int(rh194["root_case_count"]), int(rh194["unique_physical_mode_count"]),
        int(rh195["case_count"]), int(rh196["case_count"]),
        int(rh197["unique_mode_count"]), int(rh197["accepted_window_count"]),
        int(rh198["accepted_window_count"]), int(rh198["sequence_count"]),
        int(rh199["identity_case_count"]), int(rh199["physical_window_count"]),
        int(rh200["physical_case_count"]), int(rh200["temporal_case_count"]),
    ])
    identity_failure_count = sum([
        int(rh193["failure_count"]),
        int(rh195["failure_count"]),
        int(rh196["failure_count"]),
        int(rh199["identity_failure_count"]),
    ])
    statuses = {
        "frobenius_type_corrected": True,
        "source_cyclic_quotient": True,
        "physical_roots_matched": int(rh194["base_single_count_contour_count"]) == 48,
        "canonical_packet_exact": True,
        "edge_quartet_selected": int(rh200["physical_quartet_conjugate_closed_count"]) == 6,
        "cross_scale_transport": False,
    }
    boundary = macro_boundary()
    layers = [
        {"paper": "RH-192", "result": "m-fold Frobenius multiplicity obstruction", "status": "exact negative type correction"},
        {"paper": "RH-193", "result": "source-cyclic invariant quotient and moment preservation", "status": "exact theorem"},
        {"paper": "RH-194", "result": "48/48 roots match one physical quartet per side", "status": "finite floating positive"},
        {"paper": "RH-195", "result": "source-observation Riesz channels and residue pairing", "status": "exact theorem"},
        {"paper": "RH-196", "result": "optimally balanced exact spectral packet", "status": "exact theorem"},
        {"paper": "RH-197", "result": "finite residues and intrinsic transversality", "status": "finite positive, poorly conditioned"},
        {"paper": "RH-198", "result": "temporal-to-spectral graph alignment", "status": "conditional theorem plus finite signal"},
        {"paper": "RH-199", "result": "determinant, Newton trace, and weighted moment factorization", "status": "exact finite theorem"},
        {"paper": "RH-200", "result": "conjugate-pair outer-edge quartet rule", "status": "exact parity plus finite three-scale support"},
    ]
    return {
        "status": "rh201_ten_layer_source_channel_review",
        "reviewed_papers": list(range(192, 201)),
        "layer_count": len(layers),
        "finite_item_count": finite_item_count,
        "identity_failure_count": identity_failure_count,
        "full_frobenius_complement_free_count": int(rh192["whole_packet_complement_free_compatible_count"]),
        "matched_root_count": int(rh194["base_single_count_contour_count"]),
        "maximum_root_matching_error": float(rh194["maximum_absolute_matching_error"]),
        "minimum_physical_residue_modulus": float(rh197["minimum_physical_residue_modulus"]),
        "maximum_canonical_condition": float(rh197["maximum_canonical_optimal_norm_product"]),
        "latest_maximum_subspace_gap": float(rh198["latest_maximum_subspace_gap"]),
        "latest_maximum_determinant_error": float(rh199["latest_maximum_relative_determinant_error"]),
        "latest_maximum_trace_error": float(rh199["latest_maximum_relative_trace_power_error"]),
        "minimum_three_scale_edge_gap": float(rh200["minimum_radial_gap_after_quartet"]),
        "route_coordinate": route_coordinate(statuses),
        "next_frontier": next_frontier(boundary),
        "layers": layers,
        "statuses": statuses,
        "macro_boundary": boundary,
        "claim_boundary": {
            "finite_source_channel_spectral_packet": True,
            "complete_full_frobenius_riesz_shell": False,
            "interval_validated_physical_packet": False,
            "all_level_cloud": False,
            "gate_A": False,
            "gates_B_to_E": False,
            "hilbert_polya": False,
            "zeta_zero_identification": False,
            "riemann_hypothesis": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/source_channel_review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "finite_items": payload["finite_item_count"],
        "identity_failures": payload["identity_failure_count"],
        "matched_roots": payload["matched_root_count"],
        "route": payload["route_coordinate"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
