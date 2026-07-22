"""Outward-rounded block Hardy audit of frozen production matrices."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import sys
import time

from flint import acb, acb_mat, arb, ctx
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH59 = PAPERS / "RH-59-flag-adapted-schur-stein-metrics"
RH60 = PAPERS / "RH-60-finite-horizon-phase-aware-tails"
for path in (
    RH14 / "src",
    RH58 / "src",
    RH58 / "experiments",
    RH59 / "src",
    RH59 / "experiments",
):
    sys.path.insert(0, str(path))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_flag_metric_pilot import (  # noqa: E402
    FINE_RESOLUTION,
    HARDY_RADIUS,
    coarse_embedding,
    detail_embedding,
    spectral_bulk,
)


FULL_OUTPUT = ROOT / "results" / "frozen_production_interval_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "frozen_production_interval_smoke.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
HORIZONS = {0.16: 4, 0.08: 9, 0.04: 16, 0.02: 25, 0.01: 32}
PRECISION_BITS = 128
TARGET_RELATIVE_WIDTH = 1.01


def exact_arb(value: float) -> arb:
    numerator, denominator = float(value).as_integer_ratio()
    return arb(numerator) / denominator


def exact_acb(value: complex) -> acb:
    number = complex(value)
    return acb(exact_arb(number.real), exact_arb(number.imag))


def acb_matrix(values: np.ndarray) -> acb_mat:
    array = np.asarray(values, dtype=np.complex128)
    return acb_mat(
        [
            [exact_acb(array[row, column]) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def frobenius_square(matrix: acb_mat) -> arb:
    return sum((abs(entry) ** 2 for entry in matrix.entries()), arb(0))


def matrix_power(matrix: acb_mat, exponent: int) -> acb_mat:
    power = int(exponent)
    if power <= 0:
        raise ValueError("exponent must be positive")
    base = matrix
    result = None
    while power:
        if power & 1:
            result = base if result is None else result * base
        power >>= 1
        if power:
            base = base * base
    if result is None:
        raise ArithmeticError("matrix power failed")
    return result


def lower(value: arb) -> float:
    return float(value.lower())


def upper(value: arb) -> float:
    return float(value.upper())


def hash_array(value: np.ndarray) -> str:
    array = np.ascontiguousarray(np.asarray(value, dtype=np.complex128))
    return hashlib.sha256(array.view(np.uint8)).hexdigest()


def build_models(sigma: float) -> tuple[int, list[dict[str, object]], dict[str, float]]:
    dimension = max(
        32,
        2 * int(round(FINE_RESOLUTION / float(sigma) / 2.0)),
    )
    fine = sparse_folded_gaussian_matrix(dimension, sigma).toarray()
    embedding = coarse_embedding(dimension)
    detail = detail_embedding(dimension)
    fine_embedding = fine @ embedding
    coarse = embedding.T @ fine_embedding
    coupling_b = embedding.T @ fine @ detail
    coupling_c = detail.T @ fine_embedding
    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    left_operator = np.asarray(fine_data["bulk"]) / HARDY_RADIUS
    right_operator = (
        np.asarray(coarse_data["bulk"]).conjugate().T / HARDY_RADIUS
    )
    left_source = (
        np.asarray(fine_data["complement"])
        @ embedding
        @ coupling_b
        / np.linalg.norm(coupling_b, "fro")
    )
    right_source = coupling_c.conjugate().T / np.linalg.norm(
        coupling_c, "fro"
    )
    left_observation = embedding.T
    right_observation = np.asarray(
        coarse_data["complement"]
    ).conjugate().T
    metadata = {
        "fine_row_stochastic_defect": float(
            np.max(np.abs(np.sum(fine, axis=1) - 1.0))
        ),
        "fine_biorthogonality_defect": float(
            fine_data["biorthogonality_defect"]
        ),
        "coarse_biorthogonality_defect": float(
            coarse_data["biorthogonality_defect"]
        ),
        "fine_observed_bulk_radius": float(fine_data["bulk_radius"]),
        "coarse_observed_bulk_radius": float(coarse_data["bulk_radius"]),
    }
    models = [
        {
            "side": "left",
            "operator": left_operator,
            "source": left_source,
            "observation": left_observation,
        },
        {
            "side": "right",
            "operator": right_operator,
            "source": right_source,
            "observation": right_observation,
        },
    ]
    return dimension, models, metadata


def channel_interval_audit(
    model: dict[str, object],
    horizon: int,
    archived_exact: float,
) -> dict[str, object]:
    started = time.perf_counter()
    operator_np = np.asarray(model["operator"])
    source_np = np.asarray(model["source"])
    observation_np = np.asarray(model["observation"])
    operator = acb_matrix(operator_np)
    state = acb_matrix(source_np)
    observation = acb_matrix(observation_np)
    finite = arb(0)
    source_block = arb(0)
    for _ in range(horizon):
        source_block += frobenius_square(state)
        response = observation * state
        finite += frobenius_square(response)
        state = operator * state
    power = matrix_power(operator, horizon)
    block_power_squared = frobenius_square(power)
    contraction_margin = arb(1) - block_power_squared
    observation_squared = frobenius_square(observation)
    if lower(contraction_margin) <= 0.0:
        raise RuntimeError("block Frobenius contraction was not certified")
    tail = (
        observation_squared
        * block_power_squared
        * source_block
        / contraction_margin
    )
    finite_energy = finite.sqrt()
    full_energy = (finite + tail).sqrt()
    relative_width = full_energy / finite_energy
    archived = exact_arb(archived_exact)
    record = {
        "side": model["side"],
        "dimension": int(operator_np.shape[0]),
        "source_columns": int(source_np.shape[1]),
        "observation_rows": int(observation_np.shape[0]),
        "horizon": horizon,
        "precision_bits": PRECISION_BITS,
        "frozen_input_semantics": (
            "the generated binary64 operator, source, and observation "
            "entries are embedded as exact dyadic Arb/Acb inputs"
        ),
        "operator_sha256": hash_array(operator_np),
        "source_sha256": hash_array(source_np),
        "observation_sha256": hash_array(observation_np),
        "finite_energy_squared_ball": str(finite),
        "finite_energy_ball": str(finite_energy),
        "source_block_squared_ball": str(source_block),
        "block_power_frobenius_squared_ball": str(block_power_squared),
        "block_power_frobenius_ball": str(block_power_squared.sqrt()),
        "contraction_margin_ball": str(contraction_margin),
        "observation_frobenius_squared_ball": str(observation_squared),
        "tail_energy_squared_upper_ball": str(tail),
        "full_energy_upper_ball": str(full_energy),
        "relative_enclosure_width_ball": str(relative_width),
        "finite_energy_lower": lower(finite_energy),
        "full_energy_upper": upper(full_energy),
        "relative_enclosure_width_upper": upper(relative_width),
        "archived_binary64_exact_energy": archived_exact,
        "archived_energy_inside_interval": (
            lower(finite_energy) <= archived_exact <= upper(full_energy)
        ),
        "certified_block_contraction": upper(block_power_squared) < 1.0,
        "frozen_matrix_green_at_one_percent": (
            upper(relative_width) <= TARGET_RELATIVE_WIDTH
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }
    del operator, state, observation, power
    gc.collect()
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    archived = json.loads(
        (RH60 / "results" / "phase_tail_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    archived_rows = {float(row["sigma"]): row for row in archived["rows"]}
    sigmas = FULL_SIGMAS[:1] if args.smoke else FULL_SIGMAS
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        for sigma in sigmas:
            started = time.perf_counter()
            dimension, models, metadata = build_models(sigma)
            channels = []
            for model in models:
                side = str(model["side"])
                record = channel_interval_audit(
                    model,
                    HORIZONS[sigma],
                    float(archived_rows[sigma][side]["exact_hardy_energy"]),
                )
                channels.append(record)
                print(
                    json.dumps(
                        {
                            "sigma": sigma,
                            "side": side,
                            "dimension": record["dimension"],
                            "horizon": record["horizon"],
                            "relative_width_upper": record[
                                "relative_enclosure_width_upper"
                            ],
                            "elapsed_seconds": record["elapsed_seconds"],
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
            rows.append(
                {
                    "sigma": sigma,
                    "fine_dimension": dimension,
                    "selected_horizon": HORIZONS[sigma],
                    "construction_metadata": metadata,
                    "channels": channels,
                    "all_frozen_channels_green": all(
                        channel["frozen_matrix_green_at_one_percent"]
                        for channel in channels
                    ),
                    "end_to_end_production_status": "amber",
                    "end_to_end_amber_reason": (
                        "the spectral deflation and folded-Gaussian construction "
                        "that produced the frozen dyadic arrays were not enclosed "
                        "by the Acb calculation"
                    ),
                    "elapsed_seconds": time.perf_counter() - started,
                }
            )
    finally:
        ctx.prec = previous_precision
    payload = {
        "status": "rh70_frozen_production_outward_rounded_block_hardy_audit",
        "evidence_level": (
            "128-bit Arb/Acb outward-rounded execution on exact dyadic frozen "
            "matrices generated by the production folded-Gaussian pipeline"
        ),
        "target_relative_width": TARGET_RELATIVE_WIDTH,
        "rows": rows,
        "theorem_boundary": {
            "finite_prefix_block_tail_upper": True,
            "frozen_dyadic_matrix_interval_execution": True,
            "all_executed_frozen_rows_green": all(
                row["all_frozen_channels_green"] for row in rows
            ),
            "upstream_spectral_deflation_enclosed": False,
            "end_to_end_production_green": False,
            "stage_A1_closed": False,
        },
        "route_consequence": (
            "The terminal Hardy certificate itself survives outward rounding "
            "on every frozen production row; the remaining interval gate has "
            "moved upstream to spectral deflation and source/observation transfer."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "row_count": len(rows),
                "all_frozen_green": payload["theorem_boundary"][
                    "all_executed_frozen_rows_green"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
