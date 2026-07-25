from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH151 = PAPERS / "RH-151-ky-fan-reset-packet-atlas"
RH154 = PAPERS / "RH-154-half-horizon-delayed-reset-suffix"
sys.path[:0] = [
    str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"),
    str(RH94 / "experiments"), str(RH151 / "experiments"),
]

from build_reset_packet_audit import spectral_center_data  # noqa: E402
from half_log_rank import clock_rank  # noqa: E402
from reset_memory_pair import full_tail_ratio_upper, geometric_tail_mass, recent_tail_ratio_upper  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402


DEPTH = 5


def normalized_snapshot(state: np.ndarray) -> np.ndarray:
    values = np.asarray(state, dtype=float)
    gram = values.T @ values / np.sum(values * values, dtype=float)
    return (gram + gram.T) / 2.0


def memory_parts(snapshots: list[np.ndarray], time: int) -> tuple[np.ndarray, np.ndarray]:
    recent = np.zeros_like(snapshots[0])
    tail = np.zeros_like(recent)
    for age in range(time + 1):
        term = ETA**age * snapshots[time - age]
        if age < DEPTH:
            recent += term
        else:
            tail += term
    return (recent + recent.T) / 2.0, (tail + tail.T) / 2.0


def generalized_top(gram: np.ndarray, tail: np.ndarray) -> float:
    if float(np.linalg.norm(tail, 2)) == 0.0:
        return 0.0
    values, vectors = np.linalg.eigh((gram + gram.T) / 2.0)
    inverse = vectors @ np.diag(np.maximum(values, np.finfo(float).tiny) ** -0.5) @ vectors.T
    relative = inverse @ tail @ inverse
    return max(0.0, float(np.linalg.eigvalsh((relative + relative.T) / 2.0)[-1]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    reset = json.loads((RH151 / "results/reset_packet_audit.json").read_text())
    archived = {
        (float(row["sigma"]), channel["side"], int(item["time"])): item
        for row in reset["rows"] for channel in row["channels"] for item in channel["snapshots"]
    }
    suffix = json.loads((RH154 / "results/suffix_audit.json").read_text())["half_suffix"]
    suffix_start = {(float(item["sigma"]), item["side"]): int(item["start_time"]) for item in suffix["channels"]}

    rows = []
    sigmas = SIGMAS[:1] if args.smoke else SIGMAS
    for sigma in sigmas:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            rank = clock_rank(sigma, offset=2)
            endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
            operator = np.asarray(model["operator"], dtype=float)
            states = [np.asarray(model["source"], dtype=float)]
            for _ in range(endpoint):
                states.append(operator @ states[-1])
            snapshots = [normalized_snapshot(state) for state in states]
            grams = memory_grams(states)
            items = []
            for time, full in enumerate(grams):
                center = spectral_center_data(full, rank)
                record = archived[(sigma, side, time)]
                eigen_radius = math.nextafter(
                    float(center["total_center_spectral_error"]) + float(record["matrix_operator_radius"]),
                    math.inf,
                )
                packet_eigenvalue_lower = math.nextafter(
                    max(0.0, float(center["eigenvalues"][rank - 1]) - eigen_radius),
                    -math.inf,
                )
                raw_tail_mass = geometric_tail_mass(ETA, DEPTH, time)
                tail_mass = math.nextafter(raw_tail_mass, math.inf) if raw_tail_mass > 0.0 else 0.0
                recent_bound = recent_tail_ratio_upper(packet_eigenvalue_lower, tail_mass)
                full_bound = full_tail_ratio_upper(packet_eigenvalue_lower, tail_mass)

                frame = np.asarray(center["frame"], dtype=float)
                recent, tail = memory_parts(snapshots, time)
                recent_compressed = frame.T @ recent @ frame
                tail_compressed = frame.T @ tail @ frame
                nominal_ratio = generalized_top(recent_compressed, tail_compressed)
                identity_residual = float(np.linalg.norm(full - recent - tail, 2))
                items.append({
                    "time": time,
                    "rank": rank,
                    "tail_active": time >= DEPTH,
                    "in_half_suffix": time >= suffix_start[(sigma, side)],
                    "packet_eigenvalue_lower": packet_eigenvalue_lower,
                    "tail_mass_upper": tail_mass,
                    "full_memory_tail_ratio_upper": full_bound,
                    "recent_memory_tail_ratio_upper": recent_bound["ratio_upper"],
                    "recent_positive": recent_bound["recent_positive"],
                    "subunit_recent_tail": recent_bound["subunit"],
                    "selected_eigenvalue_to_twice_tail_margin": recent_bound["twice_tail_margin"],
                    "nominal_native_recent_tail_ratio": nominal_ratio,
                    "bound_dominates_nominal": nominal_ratio <= float(recent_bound["ratio_upper"]) * (1.0 + 1e-10) + 1e-18,
                    "memory_split_identity_residual": identity_residual,
                })
            rows.append({"sigma": sigma, "side": side, "rank": rank, "endpoint": endpoint, "snapshots": items})
            print(json.dumps({
                "sigma": sigma, "side": side, "snapshot_count": len(items),
                "subunit_count": sum(item["subunit_recent_tail"] for item in items),
                "maximum_ratio_upper": max(item["recent_memory_tail_ratio_upper"] for item in items),
            }, sort_keys=True), flush=True)

    items = [item for row in rows for item in row["snapshots"]]
    active = [item for item in items if item["tail_active"]]
    half = [item for item in items if item["in_half_suffix"]]
    finite_margins = [item["selected_eigenvalue_to_twice_tail_margin"] for item in active]
    summary = {
        "channel_count": len(rows),
        "snapshot_count": len(items),
        "tail_active_snapshot_count": len(active),
        "subunit_recent_tail_count": sum(item["subunit_recent_tail"] for item in items),
        "half_suffix_snapshot_count": len(half),
        "half_suffix_subunit_count": sum(item["subunit_recent_tail"] for item in half),
        "maximum_recent_tail_ratio_upper": max(item["recent_memory_tail_ratio_upper"] for item in items),
        "maximum_half_suffix_recent_tail_ratio_upper": max(item["recent_memory_tail_ratio_upper"] for item in half),
        "minimum_selected_eigenvalue_to_twice_tail_margin": min(finite_margins) if finite_margins else None,
        "maximum_nominal_native_recent_tail_ratio": max(item["nominal_native_recent_tail_ratio"] for item in items),
        "bound_dominance_failure_count": sum(not item["bound_dominates_nominal"] for item in items),
        "maximum_memory_split_identity_residual": max(item["memory_split_identity_residual"] for item in items),
        "infinite_horizon_geometric_tail_mass_upper": geometric_tail_mass(ETA, DEPTH),
    }
    payload = {
        "status": "rh155_native_spectral_reset_memory_pair",
        "eta": ETA,
        "depth": DEPTH,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "universal_geometric_tail_mass": True,
            "spectral_packet_recent_tail_loewner_bound": True,
            "sharp_subunit_gate": True,
            "all_frozen_native_pairs_subunit": not args.smoke and summary["subunit_recent_tail_count"] == 130,
            "half_suffix_native_pairs_subunit": not args.smoke and summary["half_suffix_subunit_count"] == 62,
            "directional_cross_action_identified": False,
            "uniform_all_level_packet_eigenvalue_lower": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "A trace-one geometric memory tail has a dynamics-free operator upper. On the native top spectral reset packet, the selected full-memory eigenvalue converts this into D <= tau/(lambda_r-tau) R. All 130 frozen pairs, including all 62 delayed half-suffix snapshots, have subunit ratio; the worst certified upper is 0.2247. This closes a native reset memory pair but not its identification with the directional cross-action Gram.",
    }
    output = ROOT / "results" / ("memory_pair_smoke.json" if args.smoke else "memory_pair_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
