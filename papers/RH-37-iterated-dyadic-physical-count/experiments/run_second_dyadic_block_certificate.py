"""Certify the four 4096-to-8192 blocks and the second Schur gate."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import csv
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
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
sys.path[:0] = [
    str(RH36 / "src"),
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
        "--snapshot-metadata",
        type=Path,
        default=Path("results/second_dyadic_snapshot_sigma_1e-02.json"),
    )
    parser.add_argument("--chunk-size", type=int, default=128)
    parser.add_argument(
        "--reuse-certificate",
        type=Path,
        help="rebind a certificate computed from the identical monolithic arrays",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    metadata_path = arguments.snapshot_metadata
    if not metadata_path.is_absolute():
        metadata_path = ROOT / metadata_path
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    part_paths = {
        name: ROOT / relative
        for name, relative in metadata["snapshot_parts"].items()
    }
    inherited_snapshot = Path(metadata["inherited_snapshot"])
    begun = time.perf_counter()
    with np.load(inherited_snapshot) as inherited:
        coarse_graph = physical_graph(inherited, "fine")
    with np.load(part_paths["fine_object"]) as fine_object:
        sigma = float(fine_object["sigma"])
        dimension = int(fine_object["coarse_dimension"])
        fine_dimension = int(fine_object["fine_dimension"])
        rank = int(fine_object["approximation_rank"])
        fine_graph = physical_graph(fine_object, "fine")

    if arguments.reuse_certificate is not None:
        reused_path = arguments.reuse_certificate
        if not reused_path.is_absolute():
            reused_path = ROOT / reused_path
        reused = json.loads(reused_path.read_text(encoding="utf-8"))
        expected = metadata["construction_monolithic_snapshot_sha256"]
        if reused.get("snapshot_sha256") != expected:
            raise RuntimeError("monolithic construction certificate hash mismatch")
        if (
            int(reused["coarse_dimension"]) != dimension
            or int(reused["fine_dimension"]) != fine_dimension
            or int(reused["approximation_rank"]) != rank
        ):
            raise RuntimeError("reused certificate has incompatible dimensions")
        certificates = dict(reused["block_certificates"])
        timings = dict(reused["certificate_seconds"])
        total_seconds = float(reused["total_seconds"])
        repackaged = True
    else:
        certificates = {}
        timings = {}
        for name in (
            "coarse_consistency",
            "coarse_to_detail",
            "detail_to_coarse",
            "detail_block",
        ):
            with np.load(part_paths[name]) as center_data:
                started = time.perf_counter()
                certificate = certify_low_rank_block(
                    name,
                    coarse_graph,
                    fine_graph,
                    np.asarray(center_data["left"]),
                    np.asarray(center_data["singular_values"]),
                    np.asarray(center_data["right_adjoint"]),
                    chunk_size=int(arguments.chunk_size),
                )
            timings[name] = time.perf_counter() - started
            certificates[name] = asdict(certificate)
            print(
                f"{name}: ||E||_2 <= {certificate.block_two_norm_upper:.16e}, "
                f"residual_F <= {certificate.residual_frobenius_upper:.3e}",
                flush=True,
            )
        total_seconds = time.perf_counter() - begun
        repackaged = False

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
        detail_norm_upper=certificates["detail_block"]["block_two_norm_upper"],
    )
    payload = {
        "status": (
            "rigorous_second_dyadic_block_and_schur_gate"
            if gate.detail_spectrum_outside_counting_circle
            else "failed_second_dyadic_detail_gate"
        ),
        "evidence_level": "rigorous_componentwise_stored_binary64_certificate",
        "sigma": sigma,
        "coarse_dimension": dimension,
        "fine_dimension": fine_dimension,
        "approximation_rank": rank,
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "snapshot_metadata": str(metadata_path.relative_to(ROOT)),
        "snapshot_metadata_sha256": sha256_file(metadata_path),
        "snapshot_parts": dict(metadata["snapshot_parts"]),
        "snapshot_part_sha256": dict(metadata["snapshot_part_sha256"]),
        "inherited_snapshot": str(inherited_snapshot),
        "inherited_snapshot_sha256": sha256_file(inherited_snapshot),
        "construction_monolithic_snapshot_sha256": metadata[
            "construction_monolithic_snapshot_sha256"
        ],
        "repackaged_from_identical_monolithic_arrays": repackaged,
        "block_certificates": certificates,
        "continuation_gate": asdict(gate),
        "certificate_seconds": timings,
        "total_seconds": total_seconds,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    output = arguments.output
    if output is None:
        output = ROOT / "results" / "second_dyadic_block_certificate_sigma_1e-02.json"
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
