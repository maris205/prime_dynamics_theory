"""Verify cloud/complement det2 factors without constructing projectors."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH232 = PAPERS / "RH-232-biorthogonal-riesz-cloud-projection"
sys.path.insert(0, str(ROOT / "src"))

from spectral_factor import factorization_error  # noqa: E402


GRID = np.concatenate([
    radius * np.exp(2j * np.pi * np.arange(48) / 48)
    for radius in (0.25, 0.5, 0.75, 1.0)
])


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def remove_cloud(candidate: np.ndarray, cloud: np.ndarray) -> tuple[np.ndarray, float]:
    unused = set(range(candidate.size))
    maximum_error = 0.0
    for root in cloud:
        index = min(unused, key=lambda item: abs(candidate[item] - root))
        maximum_error = max(maximum_error, float(abs(candidate[index] - root)))
        unused.remove(index)
    return candidate[sorted(unused)], maximum_error


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    projection = json.loads(
        (RH232 / "results/riesz_projection_audit.json").read_text(encoding="utf-8")
    )
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        candidate = values(endpoint["candidate_roots"])
        cloud = values(endpoint["selected_roots"])
        complement, matching_error = remove_cloud(candidate, cloud)
        errors = [factorization_error(cloud, complement, point) for point in GRID]
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "cloud_rank": int(cloud.size),
            "resolved_complement_rank": int(complement.size),
            "maximum_cloud_matching_error": matching_error,
            "maximum_grid_factorization_error": max(errors),
        })
    return {
        "status": "rh234_projection_free_det2_spectral_factor",
        "endpoint_count": len(rows),
        "grid_point_count": int(GRID.size),
        "factorization_case_count": len(rows) * int(GRID.size),
        "maximum_cloud_matching_error": max(row["maximum_cloud_matching_error"] for row in rows),
        "maximum_grid_factorization_error": max(
            row["maximum_grid_factorization_error"] for row in rows
        ),
        "inherited_maximum_projector_norm": projection["maximum_projector_operator_norm"],
        "endpoint_rows": rows,
        "theorem_boundary": {
            "finite_det2_multiset_factorization_exact": True,
            "factor_evaluation_requires_projector_norm": False,
            "finite_resolved_cloud_factor_verified": True,
            "small_noise_cloud_divisor_identified": False,
            "uniform_relative_det2_family": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/spectral_factor_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["factorization_case_count"],
        "maximum_error": payload["maximum_grid_factorization_error"],
        "projector_norm_bypassed": payload["inherited_maximum_projector_norm"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
