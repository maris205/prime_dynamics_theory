"""Aggregate the frozen RH-194 physical channel geometry."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
RH194 = PAPERS / "RH-194-physical-edge-root-matching"
sys.path.insert(0, str(ROOT / "src"))

from physical_transversality import conditioning_ratio, normalized_residue_condition, summarize  # noqa: E402


def run() -> dict[str, object]:
    matching = json.loads((RH194 / "results/physical_edge_matching.json").read_text(encoding="utf-8"))
    temporal = json.loads((RH185 / "results/bi_krylov_audit.json").read_text(encoding="utf-8"))
    temporal_lookup = {
        (str(item["side"]), int(item["start"])): item
        for item in temporal["records"]
        if float(item["sigma"]) == 0.01 and int(item["candidate_length"]) == 4
    }
    side_records = []
    window_records = []
    for side in ("left", "right"):
        modes = [item for item in matching["unique_modes"] if str(item["side"]) == side]
        windows = [item for item in matching["windows"] if str(item["side"]) == side]
        canonical_condition = float(windows[0]["canonical_optimal_norm_product"])
        canonical_cross = float(windows[0]["canonical_minimum_cross_singular_value"])
        side_records.append({
            "side": side,
            "mode_count": len(modes),
            "canonical_minimum_cross_singular_value": canonical_cross,
            "canonical_optimal_norm_product": canonical_condition,
            "canonical_balanced_frame_norm": canonical_condition**0.5,
            "residue_modulus": summarize(float(item["source_observation_residue_modulus"]) for item in modes),
            "normalized_mode_overlap": summarize(float(item["normalized_cross_overlap"]) for item in modes),
            "modewise_residue_condition": summarize(normalized_residue_condition(float(item["normalized_cross_overlap"])) for item in modes),
            "spectral_projector_norm": summarize(float(item["spectral_projector_norm"]) for item in modes),
            "source_activation_norm": summarize(float(item["source_activation_norm"]) for item in modes),
            "observation_activation_norm": summarize(float(item["observation_activation_norm"]) for item in modes),
        })
        for window in windows:
            frozen = temporal_lookup[(side, int(window["start"]))]
            temporal_condition = float(frozen["oblique_condition_number"])
            ratio = conditioning_ratio(temporal_condition, canonical_condition)
            window_records.append({
                "side": side,
                "start": int(window["start"]),
                "temporal_oblique_condition_number": temporal_condition,
                "canonical_optimal_norm_product": canonical_condition,
                "temporal_to_canonical_condition_ratio": ratio,
                "relative_condition_difference": abs(ratio - 1.0),
                "right_alignment_sine": float(window["right_temporal_to_spectral_alignment"]["maximum_principal_sine"]),
                "left_alignment_sine": float(window["left_temporal_to_spectral_alignment"]["maximum_principal_sine"]),
            })
    latest = [max((item for item in window_records if item["side"] == side), key=lambda item: int(item["start"])) for side in ("left", "right")]
    return {
        "status": "rh197_physical_residue_transversality_audit",
        "sigma": 0.01,
        "unique_mode_count": sum(int(item["mode_count"]) for item in side_records),
        "side_count": len(side_records),
        "accepted_window_count": len(window_records),
        "minimum_physical_residue_modulus": min(float(item["residue_modulus"]["minimum"]) for item in side_records),
        "minimum_canonical_cross_singular_value": min(float(item["canonical_minimum_cross_singular_value"]) for item in side_records),
        "maximum_canonical_optimal_norm_product": max(float(item["canonical_optimal_norm_product"]) for item in side_records),
        "latest_maximum_relative_condition_difference": max(float(item["relative_condition_difference"]) for item in latest),
        "side_records": side_records,
        "window_records": window_records,
        "theorem_boundary": {
            "finite_nonzero_source_observation_residues": True,
            "finite_transverse_canonical_quartets": True,
            "temporal_condition_approaches_canonical_condition": True,
            "well_conditioned_packet": False,
            "uniform_residue_lower_bound": False,
            "uniform_cross_angle": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/physical_transversality_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "modes": payload["unique_mode_count"],
        "min_cross": payload["minimum_canonical_cross_singular_value"],
        "max_condition": payload["maximum_canonical_optimal_norm_product"],
        "latest_condition_difference": payload["latest_maximum_relative_condition_difference"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
