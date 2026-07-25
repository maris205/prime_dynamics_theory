"""Outward audit of typed source packets through the RH-96 update chain."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
import time

from flint import arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
RH142 = PAPERS / "RH-142-factorized-arb-snapshot-packet-closure"
RH143 = PAPERS / "RH-143-threshold-branch-stability-radius"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH77 / "experiments"),
    str(RH82 / "src"),
    str(RH94 / "src"),
    str(RH94 / "experiments"),
    str(RH96 / "src"),
    str(RH143 / "src"),
]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from packet_transport import (  # noqa: E402
    cross_operator_radius,
    enriched_projector_radius,
    ideal_truncation_packet_gate,
    packet_transfer_radius,
    ritz_operator_radius,
    singular_direction_enclosure,
    spectral_packet_enclosure,
)
from run_effective_rank_audit import (  # noqa: E402
    HORIZONS,
    SIGMAS,
    arb_matrix,
    build_models,
    frobenius_norm,
    matrix_power,
)
from run_source_seeded_horizon_audit import ETA, memory_grams  # noqa: E402
from source_seeded_refresh import source_right_packet  # noqa: E402
from threshold_branch import branch_radius  # noqa: E402
from weak_mode_quotient import adaptive_width  # noqa: E402


PRECISION_BITS = 384
PRIMARY_THRESHOLD = 1e-8
MINIMUM_WIDTH = 2
MAXIMUM_WIDTH = 4
INHERITED_RANK = 4
ROUNDING_MULTIPLIER = 128.0


def json_default(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot serialize {type(value).__name__}")


def upper(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def exact_frobenius_squared(matrix) -> arb:
    return sum((entry * entry for entry in matrix.entries()), arb(0))


def projector_distance(first: np.ndarray, second: np.ndarray) -> float:
    left = np.asarray(first, dtype=float)
    right = np.asarray(second, dtype=float)
    difference = left @ left.T - right @ right.T
    return min(1.0, math.nextafter(float(np.linalg.norm(difference, 2)), math.inf))


def safe_eigendecomposition(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, float]:
    """Return descending eigenpairs and a conservative binary-center proxy."""
    hermitian = (np.asarray(matrix, dtype=float) + np.asarray(matrix, dtype=float).T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    order = np.argsort(values)[::-1]
    values = values[order]
    vectors = vectors[:, order]
    reconstructed = (vectors * values) @ vectors.T
    norm = float(np.linalg.norm(hermitian, 2))
    guard = ROUNDING_MULTIPLIER * np.finfo(float).eps * max(1, hermitian.shape[0]) * max(1.0, norm)
    error = math.nextafter(float(np.linalg.norm(hermitian - reconstructed, 2)) + guard, math.inf)
    return values, vectors, error


def exact_memory_radii(
    operator_values: np.ndarray,
    source_values: np.ndarray,
    nominal_grams: list[np.ndarray],
) -> tuple[list[float], list[float]]:
    """Enclose exact-binary memory Grams around their fp64 centers."""
    operator = arb_matrix(operator_values)
    state = arb_matrix(source_values)
    memory = None
    radii: list[float] = []
    center_norms: list[float] = []
    for time, nominal in enumerate(nominal_grams):
        if time:
            state = operator * state
        snapshot = (state.transpose() * state) * (arb(1) / exact_frobenius_squared(state))
        memory = snapshot if memory is None else snapshot + arb(1) / 512 * memory
        center = arb_matrix(nominal)
        radii.append(upper(frobenius_norm(memory - center)))
        center_norms.append(upper(frobenius_norm(center)))
    return radii, center_norms


def nominal_update(
    gram: np.ndarray,
    packet: np.ndarray,
    threshold: float,
) -> tuple[np.ndarray, dict[str, object]]:
    rank = packet.shape[1]
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, singular, _ = np.linalg.svd(cross, full_matrices=False)
    selected = adaptive_width(singular, threshold, minimum=MINIMUM_WIDTH, maximum=MAXIMUM_WIDTH)
    full_basis, _ = np.linalg.qr(
        np.column_stack([packet, left[:, :MAXIMUM_WIDTH]]),
        mode="reduced",
    )
    enriched = full_basis[:, : rank + selected]
    compressed = enriched.T @ gram @ enriched
    compressed = (compressed + compressed.T) / 2.0
    values, vectors, eigen_error = safe_eigendecomposition(compressed)
    next_packet = enriched @ vectors[:, :rank]
    return next_packet, {
        "rank": rank,
        "cross": cross,
        "cross_singular_values": singular,
        "selected_width": selected,
        "enriched": enriched,
        "ritz_values": values,
        "ritz_eigen_error": eigen_error,
    }


def compatibility_record(
    sigma: float,
    model: dict[str, object],
    rank: int,
    inherited: dict[str, object],
) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    source_packet = source_right_packet(source, rank)
    postblock = np.linalg.matrix_power(operator, HORIZONS[sigma]) @ source
    _, _, right = np.linalg.svd(postblock, full_matrices=False)
    postblock_packet = right[:INHERITED_RANK].T
    distance = projector_distance(postblock_packet, source_packet)
    transfer = packet_transfer_radius(
        distance,
        float(inherited["projector_radius"]),
        INHERITED_RANK,
        rank,
    )
    return {
        "inherited_time": HORIZONS[sigma],
        "target_time": 0,
        "inherited_rank": INHERITED_RANK,
        "target_rank": rank,
        "nominal_center_projector_distance": distance,
        "inherited_projector_radius": float(inherited["projector_radius"]),
        **transfer,
        "obstruction": "rank_mismatch" if rank != INHERITED_RANK else "vacuous_triangle_transfer",
    }


def transport_chain(
    grams: list[np.ndarray],
    gram_radii: list[float],
    gram_norms: list[float],
    seed: np.ndarray,
    rank: int,
) -> dict[str, object]:
    seed_values, seed_vectors, seed_eigen_error = safe_eigendecomposition(grams[0])
    seed_nominal_gap = float(seed_values[rank - 1] - seed_values[rank])
    seed_gap_lower = max(0.0, seed_nominal_gap - 2.0 * seed_eigen_error)
    seed_gate = spectral_packet_enclosure(seed_gap_lower, gram_radii[0])
    packet_radius = seed_gate["projector_radius"]
    if packet_radius is None:
        return {
            "source_seed": {
                "nominal_gap": seed_nominal_gap,
                "gap_lower": seed_gap_lower,
                "eigen_backward_proxy": seed_eigen_error,
                "gram_radius": gram_radii[0],
                "certified": False,
                "projector_radius": None,
            },
            "steps": [],
            "certified_prefix_updates": 0,
            "first_failure_time": 0,
            "first_failure_gate": "source_seed",
            "complete_chain": False,
        }

    gram_seed = np.asarray(seed_vectors[:, :rank], dtype=float)
    seed_realization_distance = projector_distance(np.asarray(seed, dtype=float), gram_seed)
    packet = gram_seed
    steps = []
    first_failure_time = None
    first_failure_gate = None
    for time in range(1, len(grams)):
        next_packet, nominal = nominal_update(grams[time], packet, PRIMARY_THRESHOLD)
        singular = np.asarray(nominal["cross_singular_values"], dtype=float)
        selected = int(nominal["selected_width"])
        leading = float(singular[0])
        local_relative_budget = ROUNDING_MULTIPLIER * np.finfo(float).eps * grams[time].shape[0]
        local_cross_budget = local_relative_budget * leading
        # The nominal packet is the exact spectral center of the archived
        # binary Gram.  A local backward proxy is charged to evaluating the
        # cross, but it is not reinterpreted as an independent projector ball.
        effective_packet_radius = float(packet_radius)
        intrinsic_cross_radius = cross_operator_radius(
            gram_radii[time], gram_norms[time], effective_packet_radius
        )
        cross_radius = intrinsic_cross_radius + local_cross_budget
        branch = branch_radius(singular[:MAXIMUM_WIDTH], PRIMARY_THRESHOLD, minimum=MINIMUM_WIDTH, maximum=MAXIMUM_WIDTH)
        branch_stable = cross_radius < float(branch["absolute_radius"])
        direction = singular_direction_enclosure(singular, selected, cross_radius)

        enriched_radius = None
        ritz_radius = None
        ritz_gap_lower = None
        output = None
        if branch_stable and direction["stable"]:
            enriched_radius = enriched_projector_radius(
                effective_packet_radius,
                float(direction["projector_radius"]),
            )
            ritz_radius = ritz_operator_radius(
                gram_radii[time], gram_norms[time], enriched_radius
            )
            ritz_radius += local_relative_budget * gram_norms[time]
            ritz_values = np.asarray(nominal["ritz_values"], dtype=float)
            raw_ritz_gap = float(ritz_values[rank - 1] - ritz_values[rank])
            ritz_gap_lower = max(0.0, raw_ritz_gap - 2.0 * float(nominal["ritz_eigen_error"]))
            output = spectral_packet_enclosure(ritz_gap_lower, ritz_radius)

        if not branch_stable:
            failure_gate = "branch"
        elif not direction["stable"]:
            failure_gate = "direction_gap"
        elif output is None or not output["stable"]:
            failure_gate = "ritz_gap"
        else:
            failure_gate = None

        record = {
            "time": time,
            "input_projector_radius": float(packet_radius),
            "gram_operator_radius": gram_radii[time],
            "gram_frobenius_norm_upper": gram_norms[time],
            "local_relative_backward_proxy": local_relative_budget,
            "intrinsic_cross_radius": intrinsic_cross_radius,
            "local_cross_backward_proxy": local_cross_budget,
            "effective_cross_radius": cross_radius,
            "cross_singular_values": [float(value) for value in singular],
            "selected_width": selected,
            "absolute_branch_radius": float(branch["absolute_radius"]),
            "branch_radius_ratio": cross_radius / max(float(branch["absolute_radius"]), np.finfo(float).tiny),
            "branch_stable": branch_stable,
            "direction_gap": float(direction["singular_gap"]),
            "direction_gap_ratio": 2.0 * cross_radius / max(float(direction["singular_gap"]), np.finfo(float).tiny),
            "direction_stable": bool(direction["stable"]),
            "direction_projector_radius": direction["projector_radius"],
            "enriched_projector_radius": enriched_radius,
            "ritz_operator_radius": ritz_radius,
            "ritz_gap_lower": ritz_gap_lower,
            "ritz_gap_ratio": None if ritz_radius is None or ritz_gap_lower is None else 2.0 * ritz_radius / max(ritz_gap_lower, np.finfo(float).tiny),
            "ritz_stable": bool(output is not None and output["stable"]),
            "output_projector_radius": None if output is None else output["projector_radius"],
            "failure_gate": failure_gate,
        }
        steps.append(record)
        if failure_gate is not None:
            first_failure_time = time
            first_failure_gate = failure_gate
            break
        packet_radius = float(output["projector_radius"])
        packet = next_packet

    complete = first_failure_time is None
    certified_prefix = len(steps) if complete else int(first_failure_time) - 1
    return {
        "source_seed": {
            "nominal_gap": seed_nominal_gap,
            "gap_lower": seed_gap_lower,
            "eigen_backward_proxy": seed_eigen_error,
            "gram_radius": gram_radii[0],
            "certified": True,
            "projector_radius": float(seed_gate["projector_radius"]),
            "source_svd_to_gram_packet_distance": seed_realization_distance,
        },
        "steps": steps,
        "certified_prefix_updates": certified_prefix,
        "first_failure_time": first_failure_time,
        "first_failure_gate": first_failure_gate,
        "complete_chain": complete,
    }


def channel_record(
    sigma: float,
    model: dict[str, object],
    inherited: dict[str, object],
) -> dict[str, object]:
    started = time.perf_counter()
    operator = np.asarray(model["operator"], dtype=float)
    source = np.asarray(model["source"], dtype=float)
    rank = clock_rank(sigma, offset=2)
    endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
    states = [source]
    for _ in range(endpoint):
        states.append(operator @ states[-1])
    grams = memory_grams(states)
    gram_radii, gram_norms = exact_memory_radii(operator, source, grams)
    source_seed = source_right_packet(source, rank)
    singular = np.linalg.svd(source, compute_uv=False)
    truncation = ideal_truncation_packet_gate(singular, INHERITED_RANK)
    transport = transport_chain(grams, gram_radii, gram_norms, source_seed, rank)
    return {
        "side": str(model["side"]),
        "dimension": int(operator.shape[0]),
        "source_columns": int(source.shape[1]),
        "inherited_horizon": HORIZONS[sigma],
        "refresh_endpoint": endpoint,
        "clock_rank": rank,
        "anchor_compatibility": compatibility_record(sigma, model, rank, inherited),
        "ideal_time_zero_rank_four_transplant": truncation,
        "maximum_memory_gram_radius": max(gram_radii),
        "transport": transport,
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited_audit = json.loads((RH142 / "results/factorized_arb_audit.json").read_text())
    inherited = {
        (float(row["sigma"]), str(row["side"])): row
        for row in inherited_audit["rows"]
    }
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            dimension, models = build_models(sigma)
            channels = [
                channel_record(sigma, model, inherited[(sigma, str(model["side"]))])
                for model in models
            ]
            rows.append({
                "sigma": sigma,
                "fine_dimension": dimension,
                "half_log_clock": half_log_clock(sigma),
                "clock_rank": clock_rank(sigma, offset=2),
                "channels": channels,
            })
            for channel in channels:
                transport = channel["transport"]
                print(json.dumps({
                    "sigma": sigma,
                    "side": channel["side"],
                    "rank": channel["clock_rank"],
                    "inherited_informative": channel["anchor_compatibility"]["informative"],
                    "seed_radius": transport["source_seed"]["projector_radius"],
                    "certified_prefix": transport["certified_prefix_updates"],
                    "first_failure_time": transport["first_failure_time"],
                    "first_failure_gate": transport["first_failure_gate"],
                }, sort_keys=True, default=json_default), flush=True)
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    transports = [channel["transport"] for channel in channels]
    compatibility = [channel["anchor_compatibility"] for channel in channels]
    seed_rows = [transport["source_seed"] for transport in transports]
    failure_counts = {
        gate: sum(transport["first_failure_gate"] == gate for transport in transports)
        for gate in ("source_seed", "branch", "direction_gap", "ritz_gap")
    }
    decisive_steps = [transport["steps"][-1] for transport in transports if transport["steps"]]
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "rank_mismatch_channel_count": sum(not record["rank_compatible"] for record in compatibility),
        "equal_rank_vacuous_transfer_count": sum(record["rank_compatible"] and not record["informative"] for record in compatibility),
        "informative_inherited_seed_count": sum(record["informative"] for record in compatibility),
        "ideal_time_zero_rank_four_gate_count": sum(channel["ideal_time_zero_rank_four_transplant"]["packet_gate"] for channel in channels),
        "source_aligned_seed_certificate_count": sum(seed["certified"] for seed in seed_rows),
        "maximum_source_seed_projector_radius": max(seed["projector_radius"] for seed in seed_rows if seed["projector_radius"] is not None),
        "minimum_source_seed_gap_lower": min(seed["gap_lower"] for seed in seed_rows),
        "maximum_memory_gram_radius": max(channel["maximum_memory_gram_radius"] for channel in channels),
        "complete_transport_chain_count": sum(transport["complete_chain"] for transport in transports),
        "certified_recursive_update_count": sum(transport["certified_prefix_updates"] for transport in transports),
        "minimum_certified_prefix_updates": min(transport["certified_prefix_updates"] for transport in transports),
        "maximum_certified_prefix_updates": max(transport["certified_prefix_updates"] for transport in transports),
        "earliest_failure_time": min(transport["first_failure_time"] for transport in transports if transport["first_failure_time"] is not None),
        "latest_failure_time": max(transport["first_failure_time"] for transport in transports if transport["first_failure_time"] is not None),
        "failure_gate_counts": failure_counts,
        "decisive_direction_instability_count": sum(not step["direction_stable"] for step in decisive_steps),
        "simultaneous_branch_direction_failure_count": sum(
            not step["branch_stable"] and not step["direction_stable"] for step in decisive_steps
        ),
        "minimum_decisive_failure_ratio": min(
            step["branch_radius_ratio"] if step["failure_gate"] == "branch"
            else step["direction_gap_ratio"] if step["failure_gate"] == "direction_gap"
            else step["ritz_gap_ratio"]
            for step in decisive_steps
        ),
        "total_elapsed_seconds": sum(channel["elapsed_seconds"] for channel in channels),
    }
    payload = {
        "status": "rh150_temporal_anchor_packet_transport_obstruction",
        "precision_bits": PRECISION_BITS,
        "primary_threshold": PRIMARY_THRESHOLD,
        "minimum_width": MINIMUM_WIDTH,
        "maximum_width": MAXIMUM_WIDTH,
        "inherited_rank": INHERITED_RANK,
        "rounding_multiplier": ROUNDING_MULTIPLIER,
        "rows": rows,
        "audit_summary": summary,
        "theorem_boundary": {
            "typed_temporal_rank_anchor_theorem": True,
            "different_rank_projectors_have_unit_distance": True,
            "outward_cross_direction_ritz_transport_theorem": True,
            "sharp_branch_direction_and_ritz_information_gates": True,
            "all_source_aligned_clock_rank_seeds_certified": not args.smoke and summary["source_aligned_seed_certificate_count"] == 10,
            "rh142_packets_are_valid_rh96_seeds": False,
            "any_complete_recursive_transport_chain": False,
            "finite_E_update_interface_closed": False,
            "actual_exact_recursive_chain_disproved": False,
            "joint_gauge_free_output_packet_enclosure_open": True,
            "uniform_all_level_packet_transport": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The ten RH-142 packet balls cannot seed RH-96: eight have the wrong rank, and the two equal-rank temporal transfers are vacuous. "
            "A corrected time-zero clock-rank construction certifies all ten source packets, but the universal norm-ball recursion stops on every channel after only one to three updates, at branch, direction-gap, or Ritz-gap gates. "
            "The source packet is therefore not the immediate finite bottleneck; the next route must enclose the joint output packet without separately resolving weak enrichment directions, or redesign the temporal start/update gauge."
        ),
        "limitations": [
            "A failed universal radius gate means that the archived norm-ball information is insufficient; it does not prove that the exact recursive update itself fails.",
            "The center eigenspaces and singular values are realized numerically, with conservative local backward proxies included in the gates.",
            "Only the five frozen scales, two channels, and primary threshold 1e-8 are audited.",
            "No outward RH-138 assembly is attempted after recursive packet transport loses certification.",
            "No Stage A, Hilbert--Polya operator, zeta-zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = ROOT / "results" / ("packet_transport_smoke.json" if args.smoke else "packet_transport_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True, default=json_default) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True, default=json_default))


if __name__ == "__main__":
    main()
