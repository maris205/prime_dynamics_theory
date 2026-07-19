"""Two-pole Hilbert--Schmidt Hardy-energy audit for RH-50."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
for path in (
    RH14 / "src",
    RH47 / "src",
    RH47 / "experiments",
    RH48 / "experiments",
    RH49 / "experiments",
):
    sys.path.insert(0, str(path))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_dyadic_identification_pilot import haar_compress_matrix  # noqa: E402
from run_peripheral_factor_pilot import resolve_factors  # noqa: E402


OUTPUT = ROOT / "results" / "two_pole_hardy_pilot.json"
STABLE_AUDIT = RH49 / "results" / "coupling_stable_rank_pilot.json"
FULL_SIGMAS = (0.01, 0.004, 0.002, 0.001, 0.0005)
SMOKE_SIGMAS = (0.01, 0.004)
FINE_RESOLUTION = 20.48
CONTOUR_RADIUS = 0.05
ENERGY_RADII = (0.82, 0.85, 0.88, 0.90)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def coarse_to_fine(values: np.ndarray) -> np.ndarray:
    return np.repeat(np.asarray(values), 2, axis=0) / math.sqrt(2.0)


def detail_to_fine(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values)
    result = np.empty(
        (2 * source.shape[0],) + source.shape[1:], dtype=source.dtype
    )
    result[0::2] = source / math.sqrt(2.0)
    result[1::2] = -source / math.sqrt(2.0)
    return result


def coarse_from_fine(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values)
    return (source[0::2] + source[1::2]) / math.sqrt(2.0)


def detail_from_fine(values: np.ndarray) -> np.ndarray:
    source = np.asarray(values)
    return (source[0::2] - source[1::2]) / math.sqrt(2.0)


def coupling_actions(matrix):
    def b(values):
        return coarse_from_fine(matrix @ detail_to_fine(values))

    def bt(values):
        return detail_from_fine(matrix.T @ coarse_to_fine(values))

    def c(values):
        return detail_from_fine(matrix @ coarse_to_fine(values))

    def ct(values):
        return coarse_from_fine(matrix.T @ detail_to_fine(values))

    return b, bt, c, ct


def biorthogonal_modes(factors):
    dimension = np.asarray(factors["perron_mass"]).size
    right = np.column_stack(
        (
            np.ones(dimension, dtype=np.float64),
            np.asarray(factors["parity_right"], dtype=np.float64),
        )
    )
    left = np.column_stack(
        (
            np.asarray(factors["perron_mass"], dtype=np.float64),
            np.asarray(factors["parity_mass"], dtype=np.float64),
        )
    )
    gram = left.T @ right
    left = left @ np.linalg.inv(gram).T
    eigenvalues = np.asarray(
        (1.0, float(factors["parity_eigenvalue"])), dtype=np.float64
    )
    return right, left, eigenvalues, gram


def project_complement(values, right, left):
    source = np.asarray(values)
    return source - right @ (left.T @ source)


def bulk_apply(matrix, values, right, left, eigenvalues):
    source = np.asarray(values)
    return matrix @ source - right @ (
        eigenvalues[:, None] * (left.T @ source)
    )


def deterministic_probes(dimension: int, count: int, seed: int):
    rng = np.random.default_rng(int(seed))
    return rng.choice(
        np.asarray((-1.0, 1.0)), size=(int(dimension), int(count))
    )


def circle_nodes(center: float, count: int):
    return [
        complex(center)
        + CONTOUR_RADIUS * np.exp(2j * np.pi * index / count)
        for index in range(int(count))
    ]


def frobenius_probe_norm(values: np.ndarray, probes: int) -> float:
    return float(np.linalg.norm(values, "fro") / math.sqrt(float(probes)))


def fine_left_residue_norms(
    *, right, left, b_transpose, b_hilbert_schmidt: float
):
    rows = []
    for index, name in enumerate(("perron", "parity")):
        coarse_right = coarse_from_fine(right[:, index])
        coarse_left = coarse_from_fine(left[:, index])
        left_dual = b_transpose(coarse_left)
        left_norm = float(
            np.linalg.norm(coarse_right)
            * np.linalg.norm(left_dual)
            / b_hilbert_schmidt
        )
        rows.append(
            {
                "mode": name,
                "left_residue_action_over_B_hilbert_schmidt": left_norm,
            }
        )
    return rows


def coarse_right_residue_norms(
    *, right, left, c, c_hilbert_schmidt: float
):
    rows = []
    for index, name in enumerate(("perron", "parity")):
        right_image = c(right[:, index])
        right_norm = float(
            np.linalg.norm(right_image)
            * np.linalg.norm(left[:, index])
            / c_hilbert_schmidt
        )
        rows.append(
            {
                "mode": name,
                "right_residue_action_over_C_hilbert_schmidt": right_norm,
            }
        )
    return rows


def fit_tail(sequence, start: int):
    indices = np.arange(len(sequence), dtype=np.float64)
    values = np.asarray(sequence, dtype=np.float64)
    mask = (indices >= int(start)) & (values > 1.0e-14)
    if np.count_nonzero(mask) < 3:
        return {
            "start": int(start),
            "decay_base": None,
            "log_intercept": None,
            "maximum_log_residual": None,
            "points": int(np.count_nonzero(mask)),
        }
    slope, intercept = np.polyfit(indices[mask], np.log(values[mask]), 1)
    residual = np.log(values[mask]) - (slope * indices[mask] + intercept)
    return {
        "start": int(start),
        "decay_base": float(np.exp(slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "points": int(np.count_nonzero(mask)),
    }


def run_sigma(
    sigma: float,
    *,
    fine_resolution: float,
    probes: int,
    powers: int,
    nodes: int,
    stable_rows,
):
    fine_dimension = max(
        128, 2 * int(round(float(fine_resolution) / sigma / 2.0))
    )
    coarse_dimension = fine_dimension // 2
    stable_row = min(
        stable_rows, key=lambda row: abs(float(row["sigma"]) - sigma)
    )
    b_hs = float(stable_row["B_hilbert_schmidt_norm"])
    c_hs = float(stable_row["C_hilbert_schmidt_norm"])
    begun = time.perf_counter()
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    coarse = haar_compress_matrix(fine)
    fine_factors = resolve_factors(fine, sigma)
    coarse_factors = resolve_factors(coarse, sigma)
    fine_right, fine_left, fine_eigenvalues, fine_gram = biorthogonal_modes(
        fine_factors
    )
    coarse_right, coarse_left, coarse_eigenvalues, coarse_gram = (
        biorthogonal_modes(coarse_factors)
    )
    b, bt, c, _ = coupling_actions(fine)
    probe_matrix = deterministic_probes(
        coarse_dimension, probes, 50000 + int(round(1.0e6 * sigma))
    )
    b_images = b(probe_matrix)
    source_fine = coarse_to_fine(b_images)
    fine_states = project_complement(
        source_fine, fine_right, fine_left
    ).astype(np.complex128)
    coarse_states = project_complement(
        probe_matrix, coarse_right, coarse_left
    ).astype(np.complex128)

    branch_nodes = {
        "perron": circle_nodes(1.0, nodes),
        "parity": circle_nodes(float(fine_eigenvalues[1]), nodes),
    }
    left_accumulators = {
        branch: [
            np.zeros((coarse_dimension, probes), dtype=np.complex128)
            for _ in values
        ]
        for branch, values in branch_nodes.items()
    }
    right_accumulators = {
        branch: [
            np.zeros((coarse_dimension, probes), dtype=np.complex128)
            for _ in values
        ]
        for branch, values in branch_nodes.items()
    }
    left_sequence = []
    right_sequence = []
    for power in range(int(powers) + 1):
        left_output = coarse_from_fine(fine_states)
        right_output = c(coarse_states)
        left_sequence.append(
            frobenius_probe_norm(left_output, probes) / b_hs
        )
        right_sequence.append(
            frobenius_probe_norm(right_output, probes) / c_hs
        )
        for branch, values in branch_nodes.items():
            for index, z in enumerate(values):
                coefficient = z ** (-power - 1)
                left_accumulators[branch][index] += coefficient * left_output
                right_accumulators[branch][index] += coefficient * right_output
        if power < int(powers):
            fine_states = bulk_apply(
                fine,
                fine_states,
                fine_right,
                fine_left,
                fine_eigenvalues,
            )
            coarse_states = bulk_apply(
                coarse,
                coarse_states,
                coarse_right,
                coarse_left,
                coarse_eigenvalues,
            )

    energies = {}
    for radius in ENERGY_RADII:
        left_energy = math.sqrt(
            sum(
                value * value / radius ** (2 * power)
                for power, value in enumerate(left_sequence)
            )
        )
        right_energy = math.sqrt(
            sum(
                value * value / radius ** (2 * power)
                for power, value in enumerate(right_sequence)
            )
        )
        energies[f"r={radius:.2f}"] = {
            "radius": radius,
            "left_truncated_hardy_energy": left_energy,
            "right_truncated_hardy_energy": right_energy,
        }

    branches = {}
    for branch, values in branch_nodes.items():
        node_rows = []
        for index, z in enumerate(values):
            left_gain = (
                frobenius_probe_norm(left_accumulators[branch][index], probes)
                / b_hs
            )
            right_gain = (
                frobenius_probe_norm(right_accumulators[branch][index], probes)
                / c_hs
            )
            node_rows.append(
                {
                    "node": index,
                    "z_real": float(z.real),
                    "z_imag": float(z.imag),
                    "left_two_pole_bulk_gain_candidate": left_gain,
                    "right_two_pole_bulk_gain_candidate": right_gain,
                    "bulk_gain_product_candidate": left_gain * right_gain,
                }
            )
        minimum_modulus = min(abs(value) for value in values)
        hardy_bounds = {}
        for key, energy in energies.items():
            radius = float(energy["radius"])
            if radius >= minimum_modulus:
                continue
            factor = 1.0 / math.sqrt(
                minimum_modulus * minimum_modulus - radius * radius
            )
            hardy_bounds[key] = {
                "minimum_contour_modulus": minimum_modulus,
                "hardy_cauchy_factor": factor,
                "left_bulk_gain_upper_candidate": factor
                * float(energy["left_truncated_hardy_energy"]),
                "right_bulk_gain_upper_candidate": factor
                * float(energy["right_truncated_hardy_energy"]),
            }
        branches[branch] = {
            "nodes": node_rows,
            "minimum_contour_modulus": minimum_modulus,
            "maximum_left_two_pole_bulk_gain_candidate": max(
                row["left_two_pole_bulk_gain_candidate"] for row in node_rows
            ),
            "maximum_right_two_pole_bulk_gain_candidate": max(
                row["right_two_pole_bulk_gain_candidate"] for row in node_rows
            ),
            "maximum_bulk_gain_product_candidate": max(
                row["bulk_gain_product_candidate"] for row in node_rows
            ),
            "hardy_bounds": hardy_bounds,
        }

    residue_rows = {
        "fine_left": fine_left_residue_norms(
            right=fine_right,
            left=fine_left,
            b_transpose=bt,
            b_hilbert_schmidt=b_hs,
        ),
        "coarse_right": coarse_right_residue_norms(
            right=coarse_right,
            left=coarse_left,
            c=c,
            c_hilbert_schmidt=c_hs,
        ),
    }
    row = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": coarse_dimension,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "fine_bulk_radius_candidate": float(fine_factors["bulk_radius"]),
        "coarse_bulk_radius_candidate": float(coarse_factors["bulk_radius"]),
        "fine_mode_gram_maximum_defect": float(
            np.max(np.abs(fine_gram - np.eye(2)))
        ),
        "coarse_mode_gram_maximum_defect": float(
            np.max(np.abs(coarse_gram - np.eye(2)))
        ),
        "B_hilbert_schmidt_norm": b_hs,
        "C_hilbert_schmidt_norm": c_hs,
        "probe_count": probes,
        "maximum_power": powers,
        "left_power_gain_sequence": left_sequence,
        "right_power_gain_sequence": right_sequence,
        "left_tail_fit": fit_tail(left_sequence, max(8, powers // 3)),
        "right_tail_fit": fit_tail(right_sequence, max(8, powers // 3)),
        "hardy_energies": energies,
        "branches": branches,
        "residue_action_ledgers": residue_rows,
        "elapsed_seconds": time.perf_counter() - begun,
    }
    del fine, coarse, fine_factors, coarse_factors
    gc.collect()
    return row


def fit_power(rows, extractor):
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([float(extractor(row)) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--fine-resolution", type=float, default=FINE_RESOLUTION)
    parser.add_argument("--probes", type=int, default=8)
    parser.add_argument("--powers", type=int, default=64)
    parser.add_argument("--nodes", type=int, default=8)
    args = parser.parse_args()
    stable = json.loads(STABLE_AUDIT.read_text(encoding="utf-8"))
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(
            sigma,
            fine_resolution=args.fine_resolution,
            probes=args.probes,
            powers=args.powers,
            nodes=args.nodes,
            stable_rows=stable["rows"],
        )
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "fine_dimension": row["fine_dimension"],
                    "left_energy_r085": row["hardy_energies"]["r=0.85"][
                        "left_truncated_hardy_energy"
                    ],
                    "right_energy_r085": row["hardy_energies"]["r=0.85"][
                        "right_truncated_hardy_energy"
                    ],
                    "maximum_bulk_product": max(
                        branch["maximum_bulk_gain_product_candidate"]
                        for branch in row["branches"].values()
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": "floating_two_pole_hilbert_schmidt_hardy_energy_audit",
        "evidence_level": (
            "binary64 exact-Haar two-pole power audit with Hutchinson traces and truncated Hardy energies; not interval validated"
        ),
        "fine_resolution_target": float(args.fine_resolution),
        "probe_count": int(args.probes),
        "maximum_power": int(args.powers),
        "contour_node_count": int(args.nodes),
        "energy_radii": list(ENERGY_RADII),
        "source": {
            "path": str(source_path.relative_to(REPOSITORY)),
            "sha256": sha256_file(source_path),
        },
        "stable_audit": {
            "path": str(STABLE_AUDIT.relative_to(REPOSITORY)),
            "sha256": sha256_file(STABLE_AUDIT),
        },
        "rows": rows,
        "fits": {
            "left_energy_r085": fit_power(
                rows,
                lambda row: row["hardy_energies"]["r=0.85"][
                    "left_truncated_hardy_energy"
                ],
            ),
            "right_energy_r085": fit_power(
                rows,
                lambda row: row["hardy_energies"]["r=0.85"][
                    "right_truncated_hardy_energy"
                ],
            ),
            "maximum_bulk_product": fit_power(
                rows,
                lambda row: max(
                    branch["maximum_bulk_gain_product_candidate"]
                    for branch in row["branches"].values()
                ),
            ),
        },
        "limitations": [
            "The Hardy energies are truncated after the archived maximum power; no interval tail enclosure is applied.",
            "Hutchinson probes estimate Hilbert-Schmidt norms and are not deterministic uppers.",
            "The two-pole factors and bulk radii are binary64 eigensolver outputs.",
            "A uniform analytic directional Hardy-energy bound is not inferred from the finite audit.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "two_pole_hardy_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "fits": payload["fits"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
