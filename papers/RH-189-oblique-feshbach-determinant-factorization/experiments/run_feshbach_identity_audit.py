"""Random exact-arithmetic-scale audit of the oblique Feshbach identity."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from oblique_feshbach import block_coordinates, feshbach_determinant_identity  # noqa: E402


def one_case(rng: np.random.Generator, dimension: int, rank: int, trial: int) -> dict[str, float | int]:
    right = rng.normal(size=(dimension, rank)) + 1j * rng.normal(size=(dimension, rank))
    left = rng.normal(size=(dimension, rank)) + 1j * rng.normal(size=(dimension, rank))
    # Normalize the pair through an exact finite biorthogonal correction.
    right, _ = np.linalg.qr(right, mode="reduced")
    left, _ = np.linalg.qr(left, mode="reduced")
    cross = left.conj().T @ right
    left = left @ np.linalg.inv(cross.conj().T)
    operator = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
    z = 2.5 + 0.37j + 0.11 * trial
    blocks = block_coordinates(operator, right, left)
    coordinates = blocks["coordinate_matrix"]
    inverse = blocks["coordinate_inverse"]
    similarity = inverse @ operator @ coordinates
    assembled = np.block([[blocks["K"], blocks["B"]], [blocks["C"], blocks["D"]]])
    identity = feshbach_determinant_identity(z, operator, blocks)
    projector = np.eye(dimension) - right @ left.conj().T
    complement = blocks["complement_frame"]
    dual_complement = blocks["dual_complement_frame"]
    orthonormal_dual_error = np.linalg.norm(
        dual_complement.conj().T - complement.conj().T @ projector, 2
    )
    one_factor_bound_violation = max(
        0.0,
        float(np.linalg.norm(blocks["D"], 2))
        - float(np.linalg.norm(projector, 2)) * float(np.linalg.norm(operator, 2)),
    )
    gauge = rng.normal(size=(dimension - rank, dimension - rank))
    gauge += (dimension - rank + 1.0) * np.eye(dimension - rank)
    gauge_inverse = np.linalg.inv(gauge)
    transformed_self_energy = (
        blocks["B"] @ gauge
        @ np.linalg.inv(z * np.eye(dimension - rank) - gauge_inverse @ blocks["D"] @ gauge)
        @ gauge_inverse @ blocks["C"]
    )
    self_energy = blocks["B"] @ np.linalg.inv(
        z * np.eye(dimension - rank) - blocks["D"]
    ) @ blocks["C"]
    return {
        "dimension": dimension,
        "rank": rank,
        "trial": trial,
        "coordinate_inverse_error": float(np.linalg.norm(inverse @ coordinates - np.eye(dimension), 2)),
        "block_similarity_error": float(np.linalg.norm(similarity - assembled, 2)),
        "determinant_relative_error": float(identity["relative_error"]),
        "orthonormal_dual_error": float(orthonormal_dual_error),
        "one_factor_bound_violation": float(one_factor_bound_violation),
        "self_energy_gauge_error": float(np.linalg.norm(transformed_self_energy - self_energy, 2)),
    }


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(189)
    dimensions = (5, 7) if smoke else (5, 7, 9, 11)
    trials = 10 if smoke else 20
    records = []
    for dimension in dimensions:
        for rank in (1, 2, 3):
            for trial in range(trials):
                records.append(one_case(rng, dimension, rank, trial))
    maxima = {
        "coordinate_inverse_error": max(float(item["coordinate_inverse_error"]) for item in records),
        "block_similarity_error": max(float(item["block_similarity_error"]) for item in records),
        "determinant_relative_error": max(float(item["determinant_relative_error"]) for item in records),
        "orthonormal_dual_error": max(float(item["orthonormal_dual_error"]) for item in records),
        "one_factor_bound_violation": max(float(item["one_factor_bound_violation"]) for item in records),
        "self_energy_gauge_error": max(float(item["self_energy_gauge_error"]) for item in records),
    }
    failures = sum(any(float(item[key]) > 1e-8 for key in maxima) for item in records)
    return {
        "status": "rh189_oblique_feshbach_determinant_identity_audit",
        "case_count": len(records),
        "failure_count": failures,
        "maximum_errors": maxima,
        "records": records,
        "theorem_boundary": {
            "exact_oblique_coordinate_factorization": True,
            "exact_feshbach_determinant_identity": True,
            "orthonormal_complement_one_factor_bound": True,
            "complement_gauge_self_energy_invariance": True,
            "finite_random_audit": True,
            "physical_complement_resolvent_bound": False,
            "physical_cycle_to_transfer_map": False,
            "gate_A": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "feshbach_identity_smoke.json" if args.smoke else "feshbach_identity_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "cases": payload["case_count"], "failures": payload["failure_count"], "maximum_errors": payload["maximum_errors"]}, sort_keys=True))


if __name__ == "__main__":
    main()
