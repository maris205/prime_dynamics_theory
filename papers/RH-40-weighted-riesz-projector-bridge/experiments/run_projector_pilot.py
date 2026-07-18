"""Audit stored peripheral modes, weighted terms, and dyadic block scaling."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigs


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
sys.path.insert(0, str(ROOT / "src"))

from projector_bridge import (  # noqa: E402
    PeripheralData,
    block_factors,
    biorthogonality_defect,
    low_rank_frobenius_norm,
    low_rank_singular_values,
)


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_matrix_data"]),
            np.asarray(data[f"{prefix}_matrix_indices"]),
            np.asarray(data[f"{prefix}_matrix_indptr"]),
        ),
        shape=tuple(int(value) for value in data[f"{prefix}_matrix_shape"]),
    )


def peripheral_from_snapshot(data, prefix: str) -> PeripheralData:
    return PeripheralData(
        right=np.asarray(data[f"{prefix}_right_modes"]),
        left=np.asarray(data[f"{prefix}_left_modes"]),
        values=np.asarray(data[f"{prefix}_peripheral_values"]),
    )


def deterministic_start(dimension: int) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin((index + 0.5) * np.sqrt(2.0))
    vector += 0.37 * np.cos((index + 0.5) * np.sqrt(3.0))
    return vector / np.linalg.norm(vector)


def complex_record(value: complex) -> dict[str, float]:
    scalar = complex(value)
    return {
        "real": float(scalar.real),
        "imag": float(scalar.imag),
        "modulus": float(abs(scalar)),
    }


def level_record(
    label: str, matrix: csr_matrix, peripheral: PeripheralData
) -> dict[str, object]:
    right = np.asarray(peripheral.right)
    left = np.asarray(peripheral.left)
    values = np.asarray(peripheral.values)
    residuals = {}
    for index, name in enumerate(("perron", "parity")):
        residuals[name] = {
            "right": float(
                np.linalg.norm(matrix @ right[:, index] - values[index] * right[:, index])
            ),
            "left": float(
                np.linalg.norm(matrix.T @ left[:, index] - values[index] * left[:, index])
            ),
        }
    spectrum = eigs(
        matrix,
        k=min(12, matrix.shape[0] - 2),
        which="LM",
        return_eigenvectors=False,
        tol=1.0e-11,
        maxiter=20000,
        v0=deterministic_start(matrix.shape[0]),
    )
    spectrum = spectrum[np.argsort(-np.abs(spectrum))]
    bulk = spectrum[2:]
    weighted_values = low_rank_singular_values(right * values[None, :], left)
    projector_values = low_rank_singular_values(right, left)
    return {
        "label": label,
        "dimension": matrix.shape[0],
        "peripheral_values": [float(value) for value in values],
        "left_right_gram": (left.T @ right).tolist(),
        "biorthogonality_two_norm_defect": biorthogonality_defect(peripheral),
        "right_mode_two_norms": np.linalg.norm(right, axis=0).tolist(),
        "left_mode_two_norms": np.linalg.norm(left, axis=0).tolist(),
        "residuals": residuals,
        "weighted_term_singular_values": weighted_values.tolist(),
        "projector_singular_values": projector_values.tolist(),
        "leading_spectrum": [complex_record(value) for value in spectrum],
        "observed_bulk_radius": float(np.max(np.abs(bulk))),
        "parity_to_observed_bulk_radial_gap": float(
            abs(values[1]) - np.max(np.abs(bulk))
        ),
    }


def block_record(
    coarse: PeripheralData, fine: PeripheralData
) -> dict[str, dict[str, object]]:
    result = {}
    for name, (left_factor, right_factor) in block_factors(coarse, fine).items():
        singular_values = low_rank_singular_values(left_factor, right_factor)
        result[name] = {
            "factor_rank": int(left_factor.shape[1]),
            "frobenius_norm": low_rank_frobenius_norm(left_factor, right_factor),
            "singular_values": [float(value) for value in singular_values],
            "two_norm": float(singular_values[0]),
        }
    return result


def main() -> None:
    first_path = RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    second_path = (
        RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
    )
    with np.load(first_path) as first, np.load(second_path) as second:
        levels = {
            "2048": (
                sparse_from_snapshot(first, "coarse"),
                peripheral_from_snapshot(first, "coarse"),
            ),
            "4096": (
                sparse_from_snapshot(first, "fine"),
                peripheral_from_snapshot(first, "fine"),
            ),
            "8192": (
                sparse_from_snapshot(second, "fine"),
                peripheral_from_snapshot(second, "fine"),
            ),
        }
        level_payload = {
            label: level_record(label, matrix, peripheral)
            for label, (matrix, peripheral) in levels.items()
        }
        first_blocks = block_record(levels["2048"][1], levels["4096"][1])
        second_blocks = block_record(levels["4096"][1], levels["8192"][1])

    block_ratios = {
        name: {
            "frobenius_second_to_first": (
                second_blocks[name]["frobenius_norm"]
                / first_blocks[name]["frobenius_norm"]
            ),
            "two_norm_second_to_first": (
                second_blocks[name]["two_norm"] / first_blocks[name]["two_norm"]
            ),
        }
        for name in first_blocks
    }
    parity = [
        level_payload[label]["peripheral_values"][1]
        for label in ("2048", "4096", "8192")
    ]
    first_increment = parity[1] - parity[0]
    second_increment = parity[2] - parity[1]
    first_richardson = (4.0 * parity[1] - parity[0]) / 3.0
    second_richardson = (4.0 * parity[2] - parity[1]) / 3.0
    payload = {
        "status": "floating_stored_weighted_peripheral_projector_pilot",
        "evidence_level": "exact_stored_inputs_with_floating_linear_algebra",
        "sigma": 1.0e-2,
        "levels": level_payload,
        "blocks": {
            "2048_to_4096": first_blocks,
            "4096_to_8192": second_blocks,
        },
        "block_ratios": block_ratios,
        "parity_convergence": {
            "first_increment": first_increment,
            "second_increment": second_increment,
            "second_to_first_increment_ratio": second_increment / first_increment,
            "first_richardson_extrapolate": first_richardson,
            "second_richardson_extrapolate": second_richardson,
            "richardson_disagreement": abs(second_richardson - first_richardson),
        },
    }
    output = ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
