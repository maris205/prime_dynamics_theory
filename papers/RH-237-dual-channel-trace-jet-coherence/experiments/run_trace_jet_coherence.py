"""Compare left/right cloud-extracted trace jets on three disks."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH230 = PAPERS / "RH-230-dual-channel-det2-coherence-noncontraction"
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path.insert(0, str(ROOT / "src"))

from trace_coherence import complex_values, trace_jet_distance  # noqa: E402


RADII = (0.5, 0.75, 1.0)
UNIT_DISK_GATE = 0.02


def run() -> dict[str, object]:
    atlas = json.loads((RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8"))
    inherited = json.loads(
        (RH230 / "results/det2_coherence_audit.json").read_text(encoding="utf-8")
    )
    endpoints = {
        (float(row["sigma"]), str(row["side"])): complex_values(
            row["cloud_extracted_trace_powers"]
        )
        for row in atlas["endpoint_rows"]
    }
    sigmas = sorted({key[0] for key in endpoints}, reverse=True)
    rows = []
    for sigma in sigmas:
        distances = {
            str(radius): trace_jet_distance(
                endpoints[(sigma, "left")], endpoints[(sigma, "right")], radius=radius
            )
            for radius in RADII
        }
        rows.append({
            "sigma": sigma,
            "trace_jet_distances": distances,
            "unit_disk_distance": distances["1.0"],
            "unit_disk_gate": distances["1.0"] < UNIT_DISK_GATE,
        })
    return {
        "status": "rh237_dual_channel_trace_jet_coherence",
        "maximum_order": atlas["maximum_order"],
        "radii": list(RADII),
        "unit_disk_gate": UNIT_DISK_GATE,
        "channel_case_count": len(rows),
        "channel_radius_case_count": len(rows) * len(RADII),
        "unit_disk_gate_pass_count": sum(row["unit_disk_gate"] for row in rows),
        "maximum_unit_disk_trace_jet_distance": max(row["unit_disk_distance"] for row in rows),
        "maximum_distance_by_radius": {
            str(radius): max(row["trace_jet_distances"][str(radius)] for row in rows)
            for radius in RADII
        },
        "inherited_selected_det2_grid_difference": inherited["maximum_channel_log_difference"],
        "channel_rows": rows,
        "theorem_boundary": {
            "finite_trace_jet_metric_defined": True,
            "all_dual_channel_unit_disk_jet_cases_pass": all(
                row["unit_disk_gate"] for row in rows
            ),
            "all_order_channel_determinant_coherence": False,
            "small_noise_trace_jet_convergence": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/trace_jet_coherence.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "passes": payload["unit_disk_gate_pass_count"],
        "maximum_unit_disk_distance": payload["maximum_unit_disk_trace_jet_distance"],
        "radius_maxima": payload["maximum_distance_by_radius"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
