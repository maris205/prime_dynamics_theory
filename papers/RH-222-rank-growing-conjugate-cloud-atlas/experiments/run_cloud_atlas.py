"""Build the frozen sixteen-level, shell-complete resonance-cloud atlas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from resonance_cloud import (  # noqa: E402
    HARDY_RADIUS,
    cloud_gauge,
    complex_payload,
    conjugacy_error,
    conjugate_shells,
    haar_coarse_embedding,
    reciprocal_zeros,
    resolve_bulk,
    select_shell_complete_cloud,
    shell_gap,
)


SIGMAS = (
    0.04, 0.032, 0.025, 0.02, 0.016, 0.0125, 0.01, 0.008,
    0.00625, 0.005, 0.004, 0.0032, 0.0025, 0.002, 0.0016, 0.00125,
)
TARGET_RANKS = tuple(4 + 2 * index for index in range(len(SIGMAS)))
FINE_RESOLUTION = 5.12
CANDIDATE_MARGIN = 16


def scalar_complex(value: complex) -> dict[str, float]:
    number = complex(value)
    return {"real": float(number.real), "imag": float(number.imag)}


def endpoint_row(sigma: float, target_rank: int, side: str, matrix) -> dict[str, object]:
    resolution = resolve_bulk(matrix, int(target_rank) + CANDIDATE_MARGIN)
    shells = conjugate_shells(resolution.bulk)
    complete_candidate_count = sum(shell.size for shell in shells)
    cloud, selected_shells = select_shell_complete_cloud(shells, target_rank)
    gauge = cloud_gauge(cloud)
    reciprocals = reciprocal_zeros(cloud)
    selected_mass = float(np.sum(np.abs(cloud) ** 2))
    return {
        "sigma": float(sigma),
        "side": str(side),
        "dimension": int(matrix.shape[0]),
        "hardy_radius": HARDY_RADIUS,
        "target_rank": int(target_rank),
        "actual_rank": int(cloud.size),
        "candidate_bulk_count": int(resolution.bulk.size),
        "complete_candidate_count": int(complete_candidate_count),
        "discarded_incomplete_candidate_count": int(resolution.bulk.size - complete_candidate_count),
        "selected_shell_count": len(selected_shells),
        "selected_real_shell_count": sum(shell.size == 1 for shell in selected_shells),
        "selected_conjugate_pair_count": sum(shell.size == 2 for shell in selected_shells),
        "perron_scaled": scalar_complex(resolution.perron),
        "parity_scaled": scalar_complex(resolution.parity),
        "candidate_roots": complex_payload(resolution.bulk),
        "selected_roots": complex_payload(cloud),
        "normalized_roots": complex_payload(np.asarray(gauge["normalized"])),
        "reciprocal_zeros": complex_payload(reciprocals),
        "center": scalar_complex(complex(gauge["center"])),
        "rms_radius": float(gauge["radius"]),
        "conjugacy_error": conjugacy_error(cloud),
        "radial_gap_after_cloud": shell_gap(shells, len(selected_shells)),
        "minimum_selected_modulus": float(np.min(np.abs(cloud))),
        "maximum_selected_modulus": float(np.max(np.abs(cloud))),
        "minimum_reciprocal_modulus": float(np.min(np.abs(reciprocals))),
        "maximum_reciprocal_modulus": float(np.max(np.abs(reciprocals))),
        "selected_squared_eigenvalue_mass": selected_mass,
        "full_scaled_frobenius_squared": resolution.full_frobenius_squared,
        "frobenius_tail_budget_after_perron_parity_cloud": float(
            max(
                0.0,
                resolution.full_frobenius_squared
                - abs(resolution.perron) ** 2
                - abs(resolution.parity) ** 2
                - selected_mass,
            )
        ),
    }


def run(sigmas: tuple[float, ...], target_ranks: tuple[int, ...]) -> dict[str, object]:
    started = time.perf_counter()
    rows = []
    for sigma, target in zip(sigmas, target_ranks):
        dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
        fine = sparse_folded_gaussian_matrix(dimension, sigma).tocsr()
        embedding = haar_coarse_embedding(dimension)
        coarse = (embedding.T @ fine @ embedding).tocsr()
        current = [
            endpoint_row(sigma, target, "left", fine),
            endpoint_row(sigma, target, "right", coarse),
        ]
        rows.extend(current)
        print(json.dumps({
            "sigma": sigma,
            "target_rank": target,
            "actual_ranks": [row["actual_rank"] for row in current],
            "conjugacy_error_max": max(row["conjugacy_error"] for row in current),
        }, sort_keys=True), flush=True)
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in rows}
    channel_rows = []
    for sigma in sigmas:
        left = endpoint[(sigma, "left")]
        right = endpoint[(sigma, "right")]
        channel_rows.append({
            "sigma": sigma,
            "rank_difference": abs(int(left["actual_rank"]) - int(right["actual_rank"])),
            "center_difference": abs(left["center"]["real"] - right["center"]["real"]),
            "rms_radius_difference": abs(left["rms_radius"] - right["rms_radius"]),
            "outer_radius_difference": abs(left["maximum_selected_modulus"] - right["maximum_selected_modulus"]),
            "inner_radius_difference": abs(left["minimum_selected_modulus"] - right["minimum_selected_modulus"]),
        })
    return {
        "status": "rh222_rank_growing_conjugate_cloud_atlas",
        "sigmas": list(sigmas),
        "target_ranks": list(target_ranks),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "candidate_margin": CANDIDATE_MARGIN,
        "endpoint_count": len(rows),
        "endpoint_rows": rows,
        "channel_rows": channel_rows,
        "minimum_actual_rank": min(int(row["actual_rank"]) for row in rows),
        "maximum_actual_rank": max(int(row["actual_rank"]) for row in rows),
        "maximum_rank_overshoot": max(int(row["actual_rank"]) - int(row["target_rank"]) for row in rows),
        "maximum_discarded_incomplete_candidate_count": max(
            int(row["discarded_incomplete_candidate_count"]) for row in rows
        ),
        "maximum_conjugacy_error": max(float(row["conjugacy_error"]) for row in rows),
        "minimum_radial_gap": min(float(row["radial_gap_after_cloud"]) for row in rows),
        "strict_rank_growth_by_channel": {
            side: all(
                int(endpoint[(fine, side)]["actual_rank"]) > int(endpoint[(coarse, side)]["actual_rank"])
                for coarse, fine in zip(sigmas[:-1], sigmas[1:])
            )
            for side in ("left", "right")
        },
        "maximum_channel_center_difference": max(float(row["center_difference"]) for row in channel_rows),
        "maximum_channel_radius_difference": max(float(row["rms_radius_difference"]) for row in channel_rows),
        "elapsed_seconds": time.perf_counter() - started,
        "theorem_boundary": {
            "deterministic_shell_complete_selection_defined": True,
            "finite_sixteen_scale_rank_growth_audited": True,
            "selected_clouds_conjugate_closed": True,
            "canonical_rank_schedule": False,
            "all_level_radial_gap": False,
            "locally_uniform_determinant_limit": False,
            "gate_A": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    targets = TARGET_RANKS[:1] if args.smoke else TARGET_RANKS
    payload = run(sigmas, targets)
    name = "cloud_atlas_smoke.json" if args.smoke else "cloud_atlas.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoints": payload["endpoint_count"],
        "rank_range": [payload["minimum_actual_rank"], payload["maximum_actual_rank"]],
        "maximum_conjugacy_error": payload["maximum_conjugacy_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
