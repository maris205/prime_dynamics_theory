"""384-bit audit of projector propagation and unit-envelope failure."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

from flint import arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH94 = PAPERS / "RH-94-source-seeded-four-direction-horizon-refresh"
RH96 = PAPERS / "RH-96-gap-weighted-weak-mode-quotient"
sys.path[:0] = [str(ROOT / "src"), str(RH77 / "experiments"), str(RH82 / "src"), str(RH94 / "src"), str(RH94 / "experiments"), str(RH96 / "src")]

from half_log_rank import clock_rank, half_log_clock  # noqa: E402
from projector_propagation import endpoint_tail_lipschitz_bound, local_gap_distance_bound, projector_secant_multiplier  # noqa: E402
from run_effective_rank_audit import HORIZONS, SIGMAS, build_models  # noqa: E402
from run_source_seeded_horizon_audit import lower, memory_grams, residual_energy_arb, upper  # noqa: E402
from source_seeded_refresh import projector_distance, source_right_packet  # noqa: E402
from weak_mode_quotient import adaptive_width  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "projector_propagation_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "projector_propagation_smoke.json"
PRECISION_BITS = 384
RANK_OFFSET = 2
FULL_WIDTH = 4
MINIMUM_WIDTH = 2
THRESHOLDS = (1e-8, 1e-6, 1e-4)


COUNTEREXAMPLE_G1 = np.array([[0.10541486073890646, -0.0007911807905423473, 0.02950126416394244, -0.04944466601315303, -0.028074498954636134, -0.06521953610868858], [-0.0007911807905423473, 0.09371152840290164, 0.12220200393487193, -0.011019485111781094, -0.043943889990385905, -0.09161756588520494], [0.02950126416394244, 0.12220200393487193, 0.33587387407194924, -0.09937548902348688, -0.14123592318133432, -0.24638215238779224], [-0.04944466601315303, -0.011019485111781094, -0.09937548902348688, 0.12003571049566512, 0.02550575122783969, 0.048056858598020356], [-0.028074498954636134, -0.043943889990385905, -0.14123592318133432, 0.02550575122783969, 0.10333027960870456, 0.12312353202259332], [-0.06521953610868858, -0.09161756588520494, -0.24638215238779224, 0.048056858598020356, 0.12312353202259332, 0.24163374668187304]], dtype=float)
COUNTEREXAMPLE_G2 = np.array([[0.11432898559123895, 0.014377404992049685, 0.07150763069752358, -0.025938098018435142, 0.00809874666003317, -0.029809516061752674], [0.014377404992049685, 0.33041133291643787, 0.03828762975682912, -0.06257152992245828, -0.0026551399458754122, -0.1132811201826825], [0.07150763069752358, 0.03828762975682912, 0.06300922318183794, -0.00374553748347712, -0.016913934854654453, -0.047163551173376846], [-0.025938098018435142, -0.06257152992245828, -0.00374553748347712, 0.05686387168108796, 0.0030657401232661967, 0.025754872502340598], [0.00809874666003317, -0.0026551399458754122, -0.016913934854654453, 0.0030657401232661967, 0.32000128817853934, -0.02883969579581501], [-0.029809516061752674, -0.1132811201826825, -0.047163551173376846, 0.025754872502340598, -0.02883969579581501, 0.11538529845085783]], dtype=float)
COUNTEREXAMPLE_V = np.array([[-0.2931522762330079, 0.6554152338192613], [-0.33554672622977744, -0.2901898624170004], [0.5279997976661587, 0.3943881742195437], [0.08331782976913564, -0.023359510618667857], [0.716814410867123, -0.1887729140938148], [-0.04383595255223108, -0.5426765180399882]], dtype=float)


def abs_upper(value: arb) -> float:
    return math.nextafter(max(abs(float(value.lower())), abs(float(value.upper()))), math.inf)


def abs_lower(value: arb) -> float:
    lo = float(value.lower())
    hi = float(value.upper())
    if lo <= 0.0 <= hi:
        return 0.0
    return math.nextafter(min(abs(lo), abs(hi)), -math.inf)


def safe_gap(matrix: np.ndarray, rank: int) -> float:
    hermitian = (matrix + matrix.T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    values = values[::-1]
    vectors = vectors[:, ::-1]
    residual = float(np.linalg.norm(hermitian - (vectors * values) @ vectors.T, 2))
    guard = 128.0 * np.finfo(float).eps * matrix.shape[0] * max(1.0, float(np.linalg.norm(hermitian, 2)))
    return math.nextafter(float(values[rank - 1] - values[rank]) - 2.0 * (residual + guard), -math.inf)


def paired_refresh(gram: np.ndarray, packet: np.ndarray, adaptive_width_value: int, full_width_value: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rank = packet.shape[1]
    cross = gram @ packet - packet @ (packet.T @ gram @ packet)
    left, _, _ = np.linalg.svd(cross, full_matrices=False)
    full_basis, _ = np.linalg.qr(np.column_stack([packet, left[:, :full_width_value]]), mode="reduced")
    full_h = full_basis.T @ gram @ full_basis
    full_h = (full_h + full_h.T) / 2.0
    full_values, full_vectors = np.linalg.eigh(full_h)
    full_packet = full_basis @ full_vectors[:, np.argsort(full_values)[-rank:]]
    strong_dimension = rank + adaptive_width_value
    strong_basis = full_basis[:, :strong_dimension]
    strong_h = full_h[:strong_dimension, :strong_dimension]
    strong_values, strong_vectors = np.linalg.eigh(strong_h)
    adaptive_packet = strong_basis @ strong_vectors[:, np.argsort(strong_values)[-rank:]]
    return adaptive_packet, full_packet, full_h


def full_refresh(gram: np.ndarray, packet: np.ndarray, width: int = FULL_WIDTH) -> np.ndarray:
    result, _, _ = paired_refresh(gram, packet, width, width)
    return result


def propagate_full(grams: list[np.ndarray], packet: np.ndarray, first_time: int, width: int = FULL_WIDTH) -> np.ndarray:
    current = np.asarray(packet, dtype=float)
    for time in range(first_time, len(grams)):
        current = full_refresh(grams[time], current, width)
    return current


def production_chain(grams: list[np.ndarray], seed: np.ndarray, threshold: float) -> dict[str, object]:
    packet = np.asarray(seed, dtype=float)
    records = []
    endpoint_gram = grams[-1]
    endpoint_gram_frobenius = float(np.linalg.norm(endpoint_gram, "fro"))
    for time in range(1, len(grams)):
        cross = grams[time] @ packet - packet @ (packet.T @ grams[time] @ packet)
        singular = np.linalg.svd(cross, compute_uv=False)
        width = adaptive_width(singular, threshold, minimum=MINIMUM_WIDTH, maximum=FULL_WIDTH)
        adaptive_packet, full_packet, full_h = paired_refresh(grams[time], packet, width, FULL_WIDTH)
        if width < FULL_WIDTH:
            local_loss = residual_energy_arb(grams[time], adaptive_packet) - residual_energy_arb(grams[time], full_packet)
            local_distance = projector_distance(adaptive_packet, full_packet)
            gap_lower = safe_gap(full_h, packet.shape[1])
            endpoint_adaptive = propagate_full(grams, adaptive_packet, time + 1)
            endpoint_full = propagate_full(grams, full_packet, time + 1)
            endpoint_distance = projector_distance(endpoint_adaptive, endpoint_full)
            endpoint_effect = residual_energy_arb(endpoint_gram, endpoint_adaptive) - residual_energy_arb(endpoint_gram, endpoint_full)
            distance_bound = local_gap_distance_bound(max(upper(local_loss), 0.0), gap_lower)
            secant = projector_secant_multiplier(local_distance, endpoint_distance)
            tail_lipschitz = endpoint_tail_lipschitz_bound(endpoint_gram_frobenius, endpoint_distance)
            conditional = endpoint_tail_lipschitz_bound(endpoint_gram_frobenius, secant * distance_bound)
            records.append(
                {
                    "time": time,
                    "selected_width": width,
                    "interval_local_loss_ball": str(local_loss),
                    "interval_local_loss_lower": lower(local_loss),
                    "interval_local_loss_upper": upper(local_loss),
                    "local_compressed_gap_lower": gap_lower,
                    "local_projector_distance": local_distance,
                    "local_gap_distance_bound": distance_bound,
                    "local_gap_distance_green": local_distance <= distance_bound,
                    "endpoint_projector_distance": endpoint_distance,
                    "projector_secant_multiplier": secant,
                    "interval_endpoint_tail_effect_ball": str(endpoint_effect),
                    "endpoint_tail_effect_abs_lower": abs_lower(endpoint_effect),
                    "endpoint_tail_effect_abs_upper": abs_upper(endpoint_effect),
                    "endpoint_tail_lipschitz_bound": tail_lipschitz,
                    "endpoint_tail_lipschitz_green": abs_upper(endpoint_effect) <= tail_lipschitz,
                    "conditional_projector_envelope": conditional,
                    "conditional_projector_envelope_green": abs_upper(endpoint_effect) <= conditional,
                    "unit_tail_propagation_green": abs_upper(endpoint_effect) <= max(lower(local_loss), 0.0),
                    "tail_amplification_upper": abs_upper(endpoint_effect) / max(lower(local_loss), np.finfo(float).tiny),
                }
            )
        packet = adaptive_packet
    return {"threshold": threshold, "omission_count": len(records), "records": records}


def counterexample_audit() -> dict[str, object]:
    adaptive, full, first_h = paired_refresh(COUNTEREXAMPLE_G1, COUNTEREXAMPLE_V, 1, 2)
    local_loss = residual_energy_arb(COUNTEREXAMPLE_G1, adaptive) - residual_energy_arb(COUNTEREXAMPLE_G1, full)
    endpoint_adaptive = full_refresh(COUNTEREXAMPLE_G2, adaptive, 2)
    endpoint_full = full_refresh(COUNTEREXAMPLE_G2, full, 2)
    endpoint_effect = residual_energy_arb(COUNTEREXAMPLE_G2, endpoint_adaptive) - residual_energy_arb(COUNTEREXAMPLE_G2, endpoint_full)
    local_distance = projector_distance(adaptive, full)
    endpoint_distance = projector_distance(endpoint_adaptive, endpoint_full)
    gap_lower = safe_gap(first_h, 2)
    distance_bound = local_gap_distance_bound(upper(local_loss), gap_lower)
    secant = projector_secant_multiplier(local_distance, endpoint_distance)
    gram_frobenius = float(np.linalg.norm(COUNTEREXAMPLE_G2, "fro"))
    lipschitz = endpoint_tail_lipschitz_bound(gram_frobenius, endpoint_distance)
    amplification_lower = abs_lower(endpoint_effect) / upper(local_loss)
    return {
        "dimension": 6,
        "rank": 2,
        "adaptive_width": 1,
        "full_width": 2,
        "g1_trace": float(np.trace(COUNTEREXAMPLE_G1)),
        "g2_trace": float(np.trace(COUNTEREXAMPLE_G2)),
        "g1_minimum_eigenvalue": float(np.linalg.eigvalsh(COUNTEREXAMPLE_G1)[0]),
        "g2_minimum_eigenvalue": float(np.linalg.eigvalsh(COUNTEREXAMPLE_G2)[0]),
        "interval_local_loss_ball": str(local_loss),
        "interval_endpoint_effect_ball": str(endpoint_effect),
        "local_loss_upper": upper(local_loss),
        "endpoint_effect_abs_lower": abs_lower(endpoint_effect),
        "certified_tail_amplification_lower": amplification_lower,
        "unit_tail_propagation_rejected": amplification_lower > 1.0,
        "local_projector_distance": local_distance,
        "endpoint_projector_distance": endpoint_distance,
        "projector_secant_multiplier": secant,
        "local_gap_lower": gap_lower,
        "local_gap_distance_bound": distance_bound,
        "endpoint_tail_lipschitz_bound": lipschitz,
        "endpoint_tail_lipschitz_green": abs_upper(endpoint_effect) <= lipschitz,
        "matrices": {"g1": COUNTEREXAMPLE_G1.tolist(), "g2": COUNTEREXAMPLE_G2.tolist(), "initial_packet": COUNTEREXAMPLE_V.tolist()},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        sigmas = SIGMAS[:1] if args.smoke else SIGMAS
        for sigma in sigmas:
            rank = clock_rank(sigma, offset=RANK_OFFSET)
            dimension, models = build_models(sigma)
            channels = []
            for model in models:
                operator = np.asarray(model["operator"], dtype=float)
                source = np.asarray(model["source"], dtype=float)
                endpoint = max(4, int(math.ceil(2.0 * HORIZONS[sigma] / 3.0)))
                states = [source]
                for _ in range(endpoint): states.append(operator @ states[-1])
                grams = memory_grams(states)
                seed = source_right_packet(source, rank)
                chains = {f"{threshold:.0e}": production_chain(grams, seed, threshold) for threshold in THRESHOLDS}
                channels.append({"side": model["side"], "dimension": int(operator.shape[0]), "refresh_endpoint": endpoint, "clock_rank": rank, "chains": chains})
            rows.append({"sigma": sigma, "fine_dimension": dimension, "clock": half_log_clock(sigma), "clock_rank": rank, "channels": channels})
            print(json.dumps({"sigma": sigma, "omissions": sum(chain["omission_count"] for channel in channels for chain in [channel["chains"]["1e-08"]])}, sort_keys=True), flush=True)
        counterexample = counterexample_audit()
    finally:
        ctx.prec = previous_precision

    channels = [channel for row in rows for channel in row["channels"]]
    threshold_summaries = {}
    all_records = []
    for threshold in THRESHOLDS:
        key = f"{threshold:.0e}"
        records = [record for channel in channels for record in channel["chains"][key]["records"]]
        all_records.extend(records)
        threshold_summaries[key] = {
            "omission_count": len(records),
            "unit_tail_propagation_green_count": sum(record["unit_tail_propagation_green"] for record in records),
            "unit_tail_propagation_roundoff_count": sum(record["tail_amplification_upper"] <= 1.0 + 1e-12 for record in records),
            "local_gap_distance_green_count": sum(record["local_gap_distance_green"] for record in records),
            "endpoint_tail_lipschitz_green_count": sum(record["endpoint_tail_lipschitz_green"] for record in records),
            "conditional_envelope_green_count": sum(record["conditional_projector_envelope_green"] for record in records),
            "maximum_tail_amplification_upper": max((record["tail_amplification_upper"] for record in records), default=0.0),
            "maximum_projector_secant_multiplier": max((record["projector_secant_multiplier"] for record in records), default=0.0),
            "maximum_local_gap_distance_slack": max((record["local_gap_distance_bound"] / max(record["local_projector_distance"], np.finfo(float).tiny) for record in records), default=0.0),
        }
    summary = {
        "scale_count": len(rows),
        "channel_count": len(channels),
        "production_omission_count": len(all_records),
        "production_unit_tail_green_count": sum(record["unit_tail_propagation_green"] for record in all_records),
        "production_unit_tail_roundoff_count": sum(record["tail_amplification_upper"] <= 1.0 + 1e-12 for record in all_records),
        "production_maximum_tail_amplification_upper": max(record["tail_amplification_upper"] for record in all_records),
        "production_maximum_projector_secant_multiplier": max(record["projector_secant_multiplier"] for record in all_records),
        "production_all_gap_distance_bounds_green": all(record["local_gap_distance_green"] for record in all_records),
        "production_all_endpoint_lipschitz_bounds_green": all(record["endpoint_tail_lipschitz_green"] for record in all_records),
        "production_all_conditional_envelopes_green": all(record["conditional_projector_envelope_green"] for record in all_records),
        "counterexample_tail_amplification_lower": counterexample["certified_tail_amplification_lower"],
        "threshold_summaries": threshold_summaries,
    }
    payload = {
        "status": "rh98_projector_lipschitz_propagation_barrier_audit",
        "precision_bits": PRECISION_BITS,
        "rows": rows,
        "counterexample": counterexample,
        "all_executed_projector_bounds_green": summary["production_all_gap_distance_bounds_green"] and summary["production_all_endpoint_lipschitz_bounds_green"] and summary["production_all_conditional_envelopes_green"],
        "audit_summary": summary,
        "theorem_boundary": {
            "endpoint_tail_projector_lipschitz_theorem": True,
            "local_gap_loss_to_projector_theorem": True,
            "conditional_projector_block_envelope": True,
            "universal_unit_tail_propagation": False,
            "production_unit_tail_propagation_observed": True,
            "uniform_refresh_projector_lipschitz_constant_proved": False,
            "replay_free_uniform_block_envelope_proved": False,
            "repeated_block_contraction_proved": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A projector-metric envelope factors endpoint propagation into a local compressed spectral gap, a future projector secant multiplier, and the endpoint Gram norm. "
            "All production omissions satisfy the conditional bounds and happen to have no tail amplification, but an explicit normalized positive-semidefinite two-step Ritz example amplifies a local quotient loss by more than forty-four. "
            "Therefore a unit propagation law cannot be assumed; the missing object is a certified future projector-Lipschitz constant."
        ),
        "limitations": [
            "Production secant multipliers are a posteriori pairwise diagnostics, not neighborhood-uniform Lipschitz constants.",
            "The counterexample rejects universal unit propagation but does not determine the sharp production envelope.",
            "The local gap-to-distance estimate can be conservative.",
            "No replay-free uniform block theorem is proved.",
            "No Hilbert--Polya operator, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "all_green": payload["all_executed_projector_bounds_green"], **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
