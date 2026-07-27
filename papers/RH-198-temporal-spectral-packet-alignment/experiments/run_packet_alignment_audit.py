"""Audit finite temporal-to-canonical packet alignment at sigma=0.01."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH194 = PAPERS / "RH-194-physical-edge-root-matching"
RH197 = PAPERS / "RH-197-physical-residue-transversality-audit"
sys.path.insert(0, str(ROOT / "src"))

from packet_alignment import endpoint_is_minimum, log_linear_decay  # noqa: E402


def run() -> dict[str, object]:
    matching = json.loads((RH194 / "results/physical_edge_matching.json").read_text(encoding="utf-8"))
    transversality = json.loads((RH197 / "results/physical_transversality_audit.json").read_text(encoding="utf-8"))
    condition_lookup = {(str(item["side"]), int(item["start"])): item for item in transversality["window_records"]}
    sequences = []
    windows = []
    for side in ("left", "right"):
        selected = sorted((item for item in matching["windows"] if str(item["side"]) == side), key=lambda item: int(item["start"]))
        starts = [int(item["start"]) for item in selected]
        diagnostics = {
            "right_subspace_gap": [float(item["right_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in selected],
            "left_subspace_gap": [float(item["left_temporal_to_spectral_alignment"]["maximum_principal_sine"]) for item in selected],
            "maximum_root_matching_error": [max(float(root["absolute_matching_error"]) for root in item["roots"]) for item in selected],
            "maximum_trace_power_error": [float(item["maximum_relative_trace_power_error"]) for item in selected],
        }
        for name, values in diagnostics.items():
            sequences.append({
                "side": side,
                "diagnostic": name,
                "endpoint_is_minimum": endpoint_is_minimum(values),
                **log_linear_decay(starts, values),
            })
        for item in selected:
            condition = condition_lookup[(side, int(item["start"]))]
            windows.append({
                "side": side,
                "start": int(item["start"]),
                "right_subspace_gap": float(item["right_temporal_to_spectral_alignment"]["maximum_principal_sine"]),
                "left_subspace_gap": float(item["left_temporal_to_spectral_alignment"]["maximum_principal_sine"]),
                "maximum_root_matching_error": max(float(root["absolute_matching_error"]) for root in item["roots"]),
                "relative_determinant_error": float(item["relative_determinant_error"]),
                "maximum_trace_power_error": float(item["maximum_relative_trace_power_error"]),
                "relative_condition_difference": float(condition["relative_condition_difference"]),
            })
    alignment_sequences = [item for item in sequences if "subspace_gap" in str(item["diagnostic"])]
    root_sequences = [item for item in sequences if item["diagnostic"] == "maximum_root_matching_error"]
    return {
        "status": "rh198_temporal_spectral_packet_alignment_audit",
        "sigma": 0.01,
        "accepted_window_count": len(windows),
        "sequence_count": len(sequences),
        "all_alignment_log_slopes_negative": all(float(item["log_slope"]) < 0.0 for item in alignment_sequences),
        "all_alignment_endpoints_are_minima": all(bool(item["endpoint_is_minimum"]) for item in alignment_sequences),
        "alignment_per_step_ratio_range": {
            "minimum": min(float(item["per_step_ratio"]) for item in alignment_sequences),
            "maximum": max(float(item["per_step_ratio"]) for item in alignment_sequences),
        },
        "minimum_alignment_fit_r_squared": min(float(item["r_squared"]) for item in alignment_sequences),
        "root_error_per_step_ratio_range": {
            "minimum": min(float(item["per_step_ratio"]) for item in root_sequences),
            "maximum": max(float(item["per_step_ratio"]) for item in root_sequences),
        },
        "latest_maximum_subspace_gap": max(
            max(float(item["right_subspace_gap"]), float(item["left_subspace_gap"]))
            for item in windows
            if item["start"] == max(row["start"] for row in windows if row["side"] == item["side"])
        ),
        "sequences": sequences,
        "windows": windows,
        "theorem_boundary": {
            "graph_coordinate_angle_identity": True,
            "finite_alignment_decay_signal": True,
            "finite_root_error_decay_signal": True,
            "asymptotic_convergence_rate": False,
            "uniform_spectral_gap_and_vandermonde_bound": False,
            "cross_scale_transport": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/packet_alignment_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["accepted_window_count"],
        "alignment_ratio_range": payload["alignment_per_step_ratio_range"],
        "min_r2": payload["minimum_alignment_fit_r_squared"],
        "latest_gap": payload["latest_maximum_subspace_gap"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
