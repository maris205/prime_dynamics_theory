"""Bound the shells resolved beyond each selected RH-222 cloud."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from det2_tail import det2_log_tail_bound, maximum_grid_log_tail  # noqa: E402
from resonance_cloud import conjugate_shells  # noqa: E402


DISK_RADIUS = 1.0
GRID = np.concatenate([
    radius * np.exp(2j * np.pi * np.arange(48) / 48)
    for radius in (0.25, 0.5, 0.75, 1.0)
])


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        shells = conjugate_shells(values(endpoint["candidate_roots"]))
        selected_shell_count = int(endpoint["selected_shell_count"])
        omitted_shells = shells[selected_shell_count:]
        omitted = np.concatenate(omitted_shells) if omitted_shells else np.asarray([], dtype=complex)
        bound = det2_log_tail_bound(omitted, DISK_RADIUS)
        observed = maximum_grid_log_tail(omitted, GRID)
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "selected_rank": endpoint["actual_rank"],
            "resolved_complete_candidate_rank": sum(shell.size for shell in shells),
            "resolved_omitted_shell_count": len(omitted_shells),
            "resolved_omitted_root_count": int(omitted.size),
            "maximum_omitted_modulus": float(np.max(np.abs(omitted), initial=0.0)),
            "q_on_unit_disk": bound["q"],
            "resolved_omitted_squared_mass": bound["squared_mass"],
            "log_tail_upper": bound["log_tail_upper"],
            "maximum_grid_log_tail": observed,
            "bound_slack": bound["log_tail_upper"] - observed,
        })
    return {
        "status": "rh228_resolved_det2_omitted_shell_control",
        "disk_radius": DISK_RADIUS,
        "grid_point_count": int(GRID.size),
        "endpoint_count": len(rows),
        "minimum_resolved_omitted_root_count": min(row["resolved_omitted_root_count"] for row in rows),
        "maximum_resolved_omitted_root_count": max(row["resolved_omitted_root_count"] for row in rows),
        "maximum_q_on_unit_disk": max(row["q_on_unit_disk"] for row in rows),
        "maximum_log_tail_upper": max(row["log_tail_upper"] for row in rows),
        "maximum_observed_grid_log_tail": max(row["maximum_grid_log_tail"] for row in rows),
        "minimum_bound_slack": min(row["bound_slack"] for row in rows),
        "endpoint_rows": rows,
        "theorem_boundary": {
            "finite_det2_log_tail_bound": True,
            "resolved_omitted_shells_controlled_on_unit_disk": True,
            "unresolved_operator_tail_controlled": False,
            "uniform_small_noise_det2_family": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/resolved_tail_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "omitted_count_range": [payload["minimum_resolved_omitted_root_count"], payload["maximum_resolved_omitted_root_count"]],
        "maximum_q": payload["maximum_q_on_unit_disk"],
        "maximum_bound": payload["maximum_log_tail_upper"],
        "maximum_observed": payload["maximum_observed_grid_log_tail"],
        "minimum_slack": payload["minimum_bound_slack"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
