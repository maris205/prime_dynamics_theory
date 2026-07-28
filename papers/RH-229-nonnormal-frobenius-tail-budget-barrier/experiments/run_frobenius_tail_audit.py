"""Compare full finite-matrix Frobenius tails with resolved shell tails."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH228 = PAPERS / "RH-228-resolved-det2-omitted-shell-control"
sys.path.insert(0, str(ROOT / "src"))

from frobenius_tail import det2_log_tail_upper, power_growth_fit  # noqa: E402


DISK_RADIUS = 1.0
SMALL_TAIL_GATE = 1.0


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    resolved = json.loads((RH228 / "results/resolved_tail_audit.json").read_text(encoding="utf-8"))
    resolved_rows = {(float(row["sigma"]), str(row["side"])): row for row in resolved["endpoint_rows"]}
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        next_modulus = float(endpoint["minimum_selected_modulus"] - endpoint["radial_gap_after_cloud"])
        squared_budget = float(endpoint["frobenius_tail_budget_after_perron_parity_cloud"])
        full_upper = det2_log_tail_upper(squared_budget, next_modulus, DISK_RADIUS)
        shell = resolved_rows[(float(endpoint["sigma"]), str(endpoint["side"]))]
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "dimension": endpoint["dimension"],
            "selected_rank": endpoint["actual_rank"],
            "next_bulk_modulus": next_modulus,
            "q_on_unit_disk": next_modulus,
            "full_scaled_frobenius_squared": endpoint["full_scaled_frobenius_squared"],
            "squared_eigenvalue_tail_budget": squared_budget,
            "full_frobenius_log_tail_upper": full_upper,
            "resolved_shell_log_tail_upper": shell["log_tail_upper"],
            "full_to_resolved_upper_ratio": full_upper / max(shell["log_tail_upper"], np.finfo(float).tiny),
            "small_tail_gate": full_upper < SMALL_TAIL_GATE,
        })
    fits = {}
    for side in ("left", "right"):
        channel = [row for row in rows if row["side"] == side]
        fits[side] = power_growth_fit(
            np.asarray([row["sigma"] for row in channel]),
            np.asarray([row["full_frobenius_log_tail_upper"] for row in channel]),
        )
    return {
        "status": "rh229_nonnormal_frobenius_tail_budget_barrier",
        "disk_radius": DISK_RADIUS,
        "small_tail_gate": SMALL_TAIL_GATE,
        "endpoint_count": len(rows),
        "small_tail_gate_pass_count": sum(row["small_tail_gate"] for row in rows),
        "minimum_full_frobenius_log_tail_upper": min(row["full_frobenius_log_tail_upper"] for row in rows),
        "maximum_full_frobenius_log_tail_upper": max(row["full_frobenius_log_tail_upper"] for row in rows),
        "maximum_full_to_resolved_upper_ratio": max(row["full_to_resolved_upper_ratio"] for row in rows),
        "maximum_q_on_unit_disk": max(row["q_on_unit_disk"] for row in rows),
        "channel_power_fits": fits,
        "endpoint_rows": rows,
        "theorem_boundary": {
            "finite_matrix_schur_frobenius_tail_bound": True,
            "unit_disk_frobenius_tail_gate_passed": False,
            "resolved_shell_control_invalidated": False,
            "sharper_complement_ideal_bound_ruled_out": False,
            "uniform_small_noise_det2_family": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/frobenius_tail_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "pass_count": payload["small_tail_gate_pass_count"],
        "full_bound_range": [payload["minimum_full_frobenius_log_tail_upper"], payload["maximum_full_frobenius_log_tail_upper"]],
        "maximum_ratio": payload["maximum_full_to_resolved_upper_ratio"],
        "growth_exponents": {side: fit["growth_exponent"] for side, fit in payload["channel_power_fits"].items()},
    }, sort_keys=True))


if __name__ == "__main__":
    main()
