"""Certify the four stored nested-grid coordinate blocks and Schur gate."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH27 / "src"),
    str(RH30 / "src"),
]

from nested_grid import certify_low_rank_block, continuation_gate  # noqa: E402
from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    shape = tuple(int(value) for value in data[f"{prefix}_shape"])
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_data"]),
            np.asarray(data[f"{prefix}_indices"]),
            np.asarray(data[f"{prefix}_indptr"]),
        ),
        shape=shape,
    )


def physical_graph(data, prefix: str) -> ComponentwiseStoredFactorGraph:
    matrix = sparse_from_snapshot(data, f"{prefix}_matrix")
    dimension = int(matrix.shape[0])
    return ComponentwiseStoredFactorGraph(
        matrix,
        np.asarray(data[f"{prefix}_right_modes"]),
        np.asarray(data[f"{prefix}_left_modes"]),
        np.asarray(data[f"{prefix}_peripheral_values"]),
        np.empty((dimension, 0), dtype=np.float64),
        np.empty((0, dimension), dtype=np.float64),
    )


def contour(sigma: float) -> tuple[complex, float]:
    row = next(
        item
        for item in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(item["sigma"]) == float(sigma)
    )
    return (
        complex(
            float(row["contour_center_real"]),
            float(row["contour_center_imag"]),
        ),
        float(row["contour_radius"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("results/nested_grid_snapshot_sigma_1e-02.npz"),
    )
    parser.add_argument("--chunk-size", type=int, default=128)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    snapshot = arguments.snapshot
    if not snapshot.is_absolute():
        snapshot = ROOT / snapshot
    begun = time.perf_counter()
    with np.load(snapshot) as data:
        sigma = float(data["sigma"])
        dimension = int(data["coarse_dimension"])
        fine_dimension = int(data["fine_dimension"])
        rank = int(data["approximation_rank"])
        coarse_graph = physical_graph(data, "coarse")
        fine_graph = physical_graph(data, "fine")
        certificates = {}
        timings = {}
        for name in (
            "coarse_consistency",
            "coarse_to_detail",
            "detail_to_coarse",
            "detail_block",
        ):
            started = time.perf_counter()
            certificate = certify_low_rank_block(
                name,
                coarse_graph,
                fine_graph,
                np.asarray(data[f"{name}_left"]),
                np.asarray(data[f"{name}_singular_values"]),
                np.asarray(data[f"{name}_right_adjoint"]),
                chunk_size=int(arguments.chunk_size),
            )
            timings[name] = time.perf_counter() - started
            certificates[name] = asdict(certificate)
            print(
                f"{name}: ||E||_2 <= {certificate.block_two_norm_upper:.16e}, "
                f"residual_F <= {certificate.residual_frobenius_upper:.3e}",
                flush=True,
            )

    center, radius = contour(sigma)
    gate = continuation_gate(
        center,
        radius,
        coarse_consistency_upper=certificates["coarse_consistency"][
            "block_two_norm_upper"
        ],
        coarse_to_detail_upper=certificates["coarse_to_detail"][
            "block_two_norm_upper"
        ],
        detail_to_coarse_upper=certificates["detail_to_coarse"][
            "block_two_norm_upper"
        ],
        detail_norm_upper=certificates["detail_block"][
            "block_two_norm_upper"
        ],
    )
    payload = {
        "status": (
            "rigorous_nested_grid_block_and_schur_gate"
            if gate.detail_spectrum_outside_counting_circle
            else "failed_nested_grid_detail_gate"
        ),
        "evidence_level": "rigorous_componentwise_stored_binary64_certificate",
        "sigma": sigma,
        "coarse_dimension": dimension,
        "fine_dimension": fine_dimension,
        "approximation_rank": rank,
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "snapshot": str(snapshot.relative_to(ROOT)),
        "snapshot_sha256": sha256_file(snapshot),
        "block_certificates": certificates,
        "continuation_gate": asdict(gate),
        "certificate_seconds": timings,
        "total_seconds": time.perf_counter() - begun,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "nested_block_certificate_sigma_1e-02.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
