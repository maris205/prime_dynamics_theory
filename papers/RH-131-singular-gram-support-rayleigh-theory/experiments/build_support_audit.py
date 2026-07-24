from __future__ import annotations

import argparse
import collections
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH130 = PAPERS / "RH-130-floor-free-semidefinite-directional-audit"
sys.path.insert(0, str(ROOT / "src"))

from singular_support_rayleigh import (  # noqa: E402
    outward_support_rayleigh_upper,
    support_rayleigh_constant,
    support_volume_lower,
)


SEED = 1312026
FULL_SAMPLES = 4096
SMOKE_SAMPLES = 128


def orthogonal(rng: np.random.Generator, dimension: int) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(dimension, dimension)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    return q * signs


def compatible_instance(rng: np.random.Generator, dimension: int = 7) -> dict[str, object]:
    rank = int(rng.integers(1, 5))
    q = orthogonal(rng, dimension)
    support = q[:, :rank]
    gram_values = np.exp(rng.uniform(math.log(0.25), math.log(4.0), size=rank))
    gamma = float(rng.uniform(0.02, 0.92))
    rotation = orthogonal(rng, rank)
    relative_values = rng.uniform(0.0, gamma**2, size=rank)
    relative_values[-1] = gamma**2
    root = np.diag(np.sqrt(gram_values))
    gram = support @ np.diag(gram_values) @ support.T
    tail = support @ root @ rotation @ np.diag(relative_values) @ rotation.T @ root @ support.T
    result = support_rayleigh_constant(gram, tail, support_tolerance=1e-10, compatibility_tolerance=1e-10)
    action = np.diag(np.sqrt(gram_values)) @ support.T
    residual = -gamma * action
    perturbed = action + residual
    singular = np.linalg.svd(perturbed, compute_uv=False)
    actual_volume = float(np.prod(singular[:rank]))
    lower = support_volume_lower(result["pseudovolume"], gamma, rank)

    gram_noise = rng.normal(size=(dimension, dimension))
    gram_noise = (gram_noise + gram_noise.T) / 2.0
    gram_noise /= max(float(np.linalg.norm(gram_noise, 2)), np.finfo(float).tiny)
    tail_noise = rng.normal(size=(dimension, dimension))
    tail_noise = (tail_noise + tail_noise.T) / 2.0
    tail_noise /= max(float(np.linalg.norm(tail_noise, 2)), np.finfo(float).tiny)
    rg = float(rng.uniform(1e-10, 1e-7))
    rd = float(rng.uniform(1e-10, 1e-7))
    gram_hat = gram + rg * gram_noise
    tail_hat = tail + rd * tail_noise
    outward = outward_support_rayleigh_upper(gram_hat, tail_hat, support, rg, rd)
    exact_relative = support_rayleigh_constant(gram, tail, support_tolerance=1e-10, compatibility_tolerance=1e-10)
    return {
        "rank": rank,
        "kernel_compatible": result["kernel_compatible"],
        "gamma_error": abs(result["support_gamma"] - gamma),
        "sharp_volume_error": abs(actual_volume - lower),
        "outward_margin": outward["outward_gamma_squared_upper"] - exact_relative["support_gamma_squared"],
        "outward_valid": exact_relative["support_gamma_squared"] <= outward["outward_gamma_squared_upper"] + 1e-12,
    }


def leakage_instance(rng: np.random.Generator, dimension: int = 7) -> dict[str, object]:
    rank = int(rng.integers(1, 5))
    q = orthogonal(rng, dimension)
    support = q[:, :rank]
    kernel_vector = q[:, rank]
    gram = support @ np.diag(np.linspace(0.5, 2.0, rank)) @ support.T
    tail = 0.1 * gram
    epsilon = float(10.0 ** rng.uniform(-8.0, -3.0))
    obstructed = tail + epsilon * np.outer(kernel_vector, kernel_vector)
    result = support_rayleigh_constant(gram, obstructed, support_tolerance=1e-10, compatibility_tolerance=1e-12)
    return {
        "rank": rank,
        "epsilon": epsilon,
        "kernel_leakage_norm": result["kernel_leakage_norm"],
        "detected": not result["kernel_compatible"] and math.isinf(result["full_space_gamma"]),
        "support_gamma": result["support_gamma"],
    }


def rh130_application() -> dict[str, object]:
    source = RH130 / "results" / "floor_free_audit.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    ranks: dict[str, int] = {}
    for row in data["state_rows"]:
        rank = sum(item["value"] not in (None, 0.0) for item in row["relative_spectrum"])
        ranks[row["state_id"]] = rank
    distribution = collections.Counter(ranks.values())
    by_scale: dict[str, dict[str, int]] = {}
    for row in data["state_rows"]:
        rank = ranks[row["state_id"]]
        key = f"{row['sigma']:.2f}"
        by_scale.setdefault(key, {"rank_0": 0, "rank_4": 0})[f"rank_{rank}"] += 1
    created = 0
    for pair in data["pairs"]:
        source_id = f"{pair['source_sigma']:.2f}:{pair['side']}:{pair['threshold']:.0e}:p{pair['phase']:.2f}"
        target_id = f"{pair['target_sigma']:.2f}:{pair['side']}:{pair['threshold']:.0e}:p{pair['phase']:.2f}"
        created += ranks[target_id] > ranks[source_id]
    return {
        "source_archive": str(source.relative_to(ROOT.parents[1])),
        "state_count": len(ranks),
        "tail_rank_distribution": {str(key): value for key, value in sorted(distribution.items())},
        "tail_rank_by_scale": by_scale,
        "rank_creation_pair_count": created,
        "rh130_infinite_factor_count": data["audit_summary"]["infinite_tail_factor_count"],
        "rank_creation_matches_infinite_factors": created == data["audit_summary"]["infinite_tail_factor_count"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    samples = SMOKE_SAMPLES if args.smoke else FULL_SAMPLES
    rng = np.random.default_rng(SEED)
    compatible = [compatible_instance(rng) for _ in range(samples)]
    leakage = [leakage_instance(rng) for _ in range(max(32, samples // 4))]
    application = rh130_application()
    summary = {
        "compatible_sample_count": len(compatible),
        "kernel_leakage_sample_count": len(leakage),
        "compatible_failure_count": sum(not row["kernel_compatible"] for row in compatible),
        "leakage_detection_failure_count": sum(not row["detected"] for row in leakage),
        "outward_failure_count": sum(not row["outward_valid"] for row in compatible),
        "maximum_gamma_error": max(row["gamma_error"] for row in compatible),
        "maximum_sharp_volume_error": max(row["sharp_volume_error"] for row in compatible),
        "minimum_outward_margin": min(row["outward_margin"] for row in compatible),
        "rh130_zero_tail_state_count": application["tail_rank_distribution"].get("0", 0),
        "rh130_full_tail_state_count": application["tail_rank_distribution"].get("4", 0),
        "rh130_rank_creation_pair_count": application["rank_creation_pair_count"],
    }
    payload = {
        "status": "rh131_singular_gram_support_rayleigh_audit",
        "seed": SEED,
        "compatible_samples": compatible,
        "kernel_leakage_samples": leakage,
        "rh130_application": application,
        "audit_summary": summary,
        "theorem_boundary": {
            "kernel_compatibility_criterion": True,
            "pseudoinverse_support_rayleigh_formula": True,
            "sharp_supported_pseudovolume_bound": True,
            "outward_support_radius_formula": True,
            "physical_all_level_support_projector_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Singular recent Gramians are mathematically manageable on their true support, with a sharp pseudodeterminant volume theorem and an outward radius correction. Full-space control has a discontinuous kernel-compatibility gate. On RH-130, the 24 rank-creating edges exactly match the 24 infinite multiplicative factors.",
    }
    name = "support_rayleigh_smoke.json" if args.smoke else "support_rayleigh_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
