"""Verify the global cloud gauge and empirical tightness certificate."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path.insert(0, str(ROOT / "src"))

from cloud_tightness import (  # noqa: E402
    centered_rms_normalize,
    empirical_moments,
    empirical_tail_mass,
    second_moment_tail_bound,
    tightness_radius,
)


TAIL_RADII = (1.0, 1.25, 1.5, 2.0, 3.0)
EPSILONS = (0.25, 0.10, 0.05, 0.01)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        roots = values(endpoint["selected_roots"])
        normalized, center, radius = centered_rms_normalize(roots)
        moments = empirical_moments(normalized)
        tails = []
        for threshold in TAIL_RADII:
            observed = empirical_tail_mass(normalized, threshold)
            bound = second_moment_tail_bound(threshold)
            tails.append({
                "radius": threshold,
                "observed_tail_mass": observed,
                "second_moment_upper_bound": bound,
                "bound_slack": bound - observed,
            })
        archived = values(endpoint["normalized_roots"])
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "rank": endpoint["actual_rank"],
            "center_real": float(center.real),
            "center_imaginary": float(center.imag),
            "rms_radius": radius,
            "archived_normalization_maximum_error": float(np.max(np.abs(np.sort_complex(normalized) - np.sort_complex(archived)))),
            "mean_modulus": float(abs(moments["mean"])),
            "second_moment_error": float(abs(moments["second_absolute_moment"] - 1.0)),
            "fourth_absolute_moment": moments["fourth_absolute_moment"],
            "maximum_normalized_modulus": moments["maximum_modulus"],
            "tail_rows": tails,
        })
    tail_rows = [tail for row in rows for tail in row["tail_rows"]]
    return {
        "status": "rh224_global_cloud_gauge_tightness",
        "endpoint_count": len(rows),
        "tail_radii": list(TAIL_RADII),
        "tightness_radii": {str(epsilon): tightness_radius(epsilon) for epsilon in EPSILONS},
        "maximum_mean_modulus": max(row["mean_modulus"] for row in rows),
        "maximum_second_moment_error": max(row["second_moment_error"] for row in rows),
        "maximum_archived_normalization_error": max(row["archived_normalization_maximum_error"] for row in rows),
        "maximum_fourth_absolute_moment": max(row["fourth_absolute_moment"] for row in rows),
        "maximum_normalized_modulus": max(row["maximum_normalized_modulus"] for row in rows),
        "minimum_tail_bound_slack": min(tail["bound_slack"] for tail in tail_rows),
        "endpoint_rows": rows,
        "theorem_boundary": {
            "global_center_rms_moment_identities": True,
            "uniform_empirical_tightness": True,
            "subsequential_weak_compactness": True,
            "unique_weak_limit": False,
            "divisor_local_finiteness": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/tightness_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "maximum_mean": payload["maximum_mean_modulus"],
        "maximum_second_moment_error": payload["maximum_second_moment_error"],
        "maximum_normalized_modulus": payload["maximum_normalized_modulus"],
        "minimum_tail_slack": payload["minimum_tail_bound_slack"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
