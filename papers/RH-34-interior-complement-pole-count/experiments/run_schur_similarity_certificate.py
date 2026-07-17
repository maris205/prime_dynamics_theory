"""Certify the RH-34 stored complement pole count by Schur similarity."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time

import numpy as np
import scipy
from scipy.linalg import schur


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH33 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from complement_poles import (  # noqa: E402
    classify_binary64_diagonal,
    combine_frobenius_bounds,
    sha256_array,
    similarity_certificate,
)
from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_dense_exact_matmul,
    componentwise_subtract,
    frobenius_upper_array,
    magnitude_upper,
)
from resolvent_atlas import sha256_file, verify_leaf_ledger  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def stream_hasher(shape: tuple[int, int], dtype: np.dtype, chunk_size: int):
    digest = hashlib.sha256()
    digest.update(np.dtype(dtype).str.encode("ascii"))
    digest.update(repr(tuple(shape)).encode("ascii"))
    digest.update(f"column_chunks={int(chunk_size)}".encode("ascii"))
    return digest


def update_array_hash(digest, values: np.ndarray) -> None:
    digest.update(np.ascontiguousarray(values).view(np.uint8))


def graph_from_environment(environment: dict[str, object]):
    spectrum = environment["spectrum"]
    return ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )


def compute_schur_factors(
    environment: dict[str, object],
    workspace: Path,
) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    dimension = int(environment["matrix"].shape[0])
    begun = time.perf_counter()
    identity = np.eye(dimension, dtype=np.float64)
    complement = np.asarray(environment["external_action"](identity))
    assembly_seconds = time.perf_counter() - begun
    identity = None
    complement_hash = sha256_array(complement)
    print(
        f"assembled floating complement centre n={dimension} "
        f"in {assembly_seconds:.2f}s",
        flush=True,
    )

    begun = time.perf_counter()
    schur_input = np.array(complement, dtype=np.complex128, order="F")
    triangular, vectors = schur(
        schur_input,
        output="complex",
        overwrite_a=True,
        check_finite=False,
    )
    schur_seconds = time.perf_counter() - begun
    triangular_reference = np.ascontiguousarray(np.triu(triangular))
    vectors = np.ascontiguousarray(vectors)
    discarded_lower_frobenius = float(
        np.linalg.norm(np.tril(triangular, k=-1), ord="fro")
    )
    print(
        f"computed complex Schur factors in {schur_seconds:.2f}s; "
        f"discarded lower Frobenius={discarded_lower_frobenius:.3e}",
        flush=True,
    )
    workspace.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        workspace,
        schur_vectors=vectors,
        triangular_reference=triangular_reference,
    )
    return vectors, triangular_reference, {
        "floating_complement_center_sha256": complement_hash,
        "assembly_seconds": assembly_seconds,
        "schur_seconds": schur_seconds,
        "discarded_lower_frobenius": discarded_lower_frobenius,
        "workspace_reused": False,
    }


def load_schur_factors(workspace: Path) -> tuple[np.ndarray, np.ndarray, dict[str, object]]:
    begun = time.perf_counter()
    with np.load(workspace) as archive:
        vectors = np.ascontiguousarray(archive["schur_vectors"])
        triangular_reference = np.ascontiguousarray(
            archive["triangular_reference"]
        )
    seconds = time.perf_counter() - begun
    print(f"reused Schur workspace in {seconds:.2f}s", flush=True)
    return vectors, triangular_reference, {
        "floating_complement_center_sha256": None,
        "assembly_seconds": 0.0,
        "schur_seconds": 0.0,
        "discarded_lower_frobenius": 0.0,
        "workspace_reused": True,
        "workspace_load_seconds": seconds,
    }


def certify_schur_data(
    graph: ComponentwiseStoredFactorGraph,
    vectors: np.ndarray,
    triangular_reference: np.ndarray,
    *,
    chunk_size: int,
) -> dict[str, object]:
    dimension = int(vectors.shape[0])
    if vectors.shape != (dimension, dimension):
        raise ValueError("Schur vectors must be square")
    if triangular_reference.shape != vectors.shape:
        raise ValueError("Schur factors must have matching shapes")
    absolute_vectors = magnitude_upper(vectors)
    vector_adjoint = np.ascontiguousarray(vectors.conj().T)
    absolute_adjoint = np.ascontiguousarray(absolute_vectors.T)

    residual_bounds: list[float] = []
    residual_center_bounds: list[float] = []
    residual_radius_bounds: list[float] = []
    defect_bounds: list[float] = []
    defect_center_bounds: list[float] = []
    defect_radius_bounds: list[float] = []
    residual_center_hash = stream_hasher(
        vectors.shape, np.dtype(np.complex128), chunk_size
    )
    residual_radius_hash = stream_hasher(
        vectors.shape, np.dtype(np.float64), chunk_size
    )
    defect_center_hash = stream_hasher(
        vectors.shape, np.dtype(np.complex128), chunk_size
    )
    defect_radius_hash = stream_hasher(
        vectors.shape, np.dtype(np.float64), chunk_size
    )

    begun = time.perf_counter()
    for start in range(0, dimension, int(chunk_size)):
        stop = min(start + int(chunk_size), dimension)
        width = stop - start
        vector_block = np.ascontiguousarray(vectors[:, start:stop])

        exact_vector_block = ComponentwiseBall.exact(vector_block)
        applied = graph.action(exact_vector_block)
        triangular_block = ComponentwiseBall.exact(
            np.ascontiguousarray(triangular_reference[:, start:stop])
        )
        reference_action = componentwise_dense_exact_matmul(
            vectors,
            triangular_block,
            absolute_matrix=absolute_vectors,
        )
        residual = componentwise_subtract(applied, reference_action)
        residual_bounds.append(residual.norm_upper)
        residual_center_bounds.append(frobenius_upper_array(residual.center))
        residual_radius_bounds.append(frobenius_upper_array(residual.radius))
        update_array_hash(residual_center_hash, residual.center)
        update_array_hash(residual_radius_hash, residual.radius)

        gram = componentwise_dense_exact_matmul(
            vector_adjoint,
            exact_vector_block,
            absolute_matrix=absolute_adjoint,
        )
        identity_block = np.zeros((dimension, width), dtype=np.complex128)
        identity_block[np.arange(start, stop), np.arange(width)] = 1.0
        defect = componentwise_subtract(
            gram, ComponentwiseBall.exact(identity_block)
        )
        defect_bounds.append(defect.norm_upper)
        defect_center_bounds.append(frobenius_upper_array(defect.center))
        defect_radius_bounds.append(frobenius_upper_array(defect.radius))
        update_array_hash(defect_center_hash, defect.center)
        update_array_hash(defect_radius_hash, defect.radius)
        print(
            f"  certified columns {stop}/{dimension}: "
            f"R_F={residual_bounds[-1]:.3e}, "
            f"Gram_F={defect_bounds[-1]:.3e}",
            flush=True,
        )

    certificate_seconds = time.perf_counter() - begun
    return {
        "chunk_size": int(chunk_size),
        "chunk_count": len(residual_bounds),
        "schur_residual_frobenius_upper": combine_frobenius_bounds(
            residual_bounds
        ),
        "schur_residual_center_frobenius_upper": combine_frobenius_bounds(
            residual_center_bounds
        ),
        "schur_residual_radius_frobenius_upper": combine_frobenius_bounds(
            residual_radius_bounds
        ),
        "unitarity_defect_frobenius_upper": combine_frobenius_bounds(
            defect_bounds
        ),
        "unitarity_defect_center_frobenius_upper": combine_frobenius_bounds(
            defect_center_bounds
        ),
        "unitarity_defect_radius_frobenius_upper": combine_frobenius_bounds(
            defect_radius_bounds
        ),
        "residual_center_chunk_stream_sha256": residual_center_hash.hexdigest(),
        "residual_radius_chunk_stream_sha256": residual_radius_hash.hexdigest(),
        "unitarity_center_chunk_stream_sha256": defect_center_hash.hexdigest(),
        "unitarity_radius_chunk_stream_sha256": defect_radius_hash.hexdigest(),
        "componentwise_certificate_seconds": certificate_seconds,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--chunk-size", type=int, default=256)
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument("--reuse-workspace", action="store_true")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    if sigma != 1.0e-2:
        raise ValueError("RH-34 currently certifies the archived sigma=1e-2 scale")
    settings = rh24.physical_settings()[sigma]
    workspace = arguments.workspace
    if workspace is None:
        workspace = (
            ROOT
            / "results"
            / "work"
            / f"schur_factors_sigma_{sigma:.0e}.npz"
        )
    if not workspace.is_absolute():
        workspace = ROOT / workspace

    total_started = time.perf_counter()
    begun = time.perf_counter()
    environment = rh25_global.build_environment(sigma, settings)
    environment_seconds = time.perf_counter() - begun
    graph = graph_from_environment(environment)
    dimension = int(environment["matrix"].shape[0])
    print(
        f"built stored factor environment n={dimension} "
        f"in {environment_seconds:.2f}s",
        flush=True,
    )

    if arguments.reuse_workspace:
        if not workspace.exists():
            raise FileNotFoundError(workspace)
        vectors, triangular_reference, schur_metadata = load_schur_factors(
            workspace
        )
    else:
        vectors, triangular_reference, schur_metadata = compute_schur_factors(
            environment, workspace
        )
    if vectors.shape != (dimension, dimension):
        raise RuntimeError("workspace dimension does not match the stored model")
    vector_hash = sha256_array(vectors)
    triangular_hash = sha256_array(triangular_reference)
    diagonal = np.ascontiguousarray(np.diag(triangular_reference))
    diagonal_hash = sha256_array(diagonal)

    certified = certify_schur_data(
        graph,
        vectors,
        triangular_reference,
        chunk_size=int(arguments.chunk_size),
    )
    eta = float(certified["unitarity_defect_frobenius_upper"])
    residual = float(certified["schur_residual_frobenius_upper"])

    scale_row = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == sigma
    )
    contour_center = complex(
        float(scale_row["contour_center_real"]),
        float(scale_row["contour_center_imag"]),
    )
    contour_radius = float(scale_row["contour_radius"])
    classification = classify_binary64_diagonal(
        diagonal, contour_center, contour_radius
    )
    diagonal_path = (
        ROOT / "results" / f"schur_diagonal_sigma_{sigma:.0e}.csv"
    )
    write_csv(diagonal_path, list(classification.records))
    diagonal_npz_path = diagonal_path.with_suffix(".npz")
    np.savez_compressed(
        diagonal_npz_path,
        diagonal=diagonal,
        contour_center=np.asarray(contour_center, dtype=np.complex128),
        contour_radius=np.asarray(contour_radius, dtype=np.float64),
    )

    leaf_path = RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    leaf_audit = verify_leaf_ledger(leaf_path)
    if not (
        leaf_audit["exact_rational_partition_verified"]
        and int(leaf_audit["unresolved_leaf_count"]) == 0
    ):
        raise RuntimeError("the inherited RH-33 leaf ledger is not a full cover")
    leaf_rows = read_csv(leaf_path)
    homotopy_rows: list[dict[str, object]] = []
    for row in leaf_rows:
        bound = float(row["transported_inverse_upper"])
        certificate = similarity_certificate(
            eta,
            residual,
            bound,
            precision=int(arguments.precision),
        )
        homotopy_rows.append(
            {
                "parent_arc": int(row["parent_arc"]),
                "start_numerator": int(row["start_numerator"]),
                "end_numerator": int(row["end_numerator"]),
                "turn_denominator": int(row["turn_denominator"]),
                "center_id": row["center_id"],
                "complement_resolvent_upper": bound,
                "transformed_resolvent_upper": (
                    certificate.transformed_resolvent_upper
                ),
                "transformed_residual_upper": (
                    certificate.transformed_residual_upper
                ),
                "homotopy_neumann_product_upper": (
                    certificate.homotopy_neumann_product_upper
                ),
                "homotopy_denominator_lower": (
                    certificate.homotopy_denominator_lower
                ),
                "homotopy_certified": certificate.homotopy_certified,
            }
        )
    homotopy_path = (
        ROOT / "results" / f"schur_homotopy_leaves_sigma_{sigma:.0e}.csv"
    )
    write_csv(homotopy_path, homotopy_rows)
    worst_homotopy = max(
        homotopy_rows,
        key=lambda row: float(row["homotopy_neumann_product_upper"]),
    )
    uniform_similarity = similarity_certificate(
        eta,
        residual,
        max(float(row["transported_inverse_upper"]) for row in leaf_rows),
        precision=int(arguments.precision),
    )

    rh33_summary_path = RH33 / "results" / "summary.json"
    rh33_summary = load_json(rh33_summary_path)
    inherited_relative_count = int(
        rh33_summary["exact_augmented_block_minus_complement_count"]
    )
    inherited_winding = int(rh33_summary["stored_feshbach_boundary_winding"])
    all_homotopies = all(bool(row["homotopy_certified"]) for row in homotopy_rows)
    complement_count_certified = bool(
        uniform_similarity.invertibility_certified
        and uniform_similarity.homotopy_certified
        and all_homotopies
        and classification.boundary_count == 0
    )
    complement_count = (
        classification.inside_count if complement_count_certified else None
    )
    ordinary_zero_count_certified = bool(
        complement_count_certified
        and complement_count == 0
        and inherited_winding == 1
    )
    status = (
        "rigorous_stored_complement_count_zero_and_ordinary_winding_one"
        if ordinary_zero_count_certified
        else "schur_similarity_certificate_incomplete"
    )
    payload = {
        "status": status,
        "scope": "exact finite model defined by stored binary64 factors",
        "evidence_level": "rigorous_computer_assisted_stored_model_certificate",
        "sigma": sigma,
        "physical_dimension": dimension,
        "contour_center_real": contour_center.real,
        "contour_center_imag": contour_center.imag,
        "contour_radius": contour_radius,
        "schur_vectors_sha256": vector_hash,
        "triangular_reference_sha256": triangular_hash,
        "triangular_diagonal_sha256": diagonal_hash,
        **schur_metadata,
        **certified,
        "similarity_certificate": asdict(uniform_similarity),
        "rh33_leaf_count": len(leaf_rows),
        "rh33_exact_rational_partition_verified": bool(
            leaf_audit["exact_rational_partition_verified"]
        ),
        "rh33_leaf_ledger_sha256": sha256_file(leaf_path),
        "maximum_complement_resolvent_upper": max(
            float(row["transported_inverse_upper"]) for row in leaf_rows
        ),
        "maximum_homotopy_neumann_product_upper": float(
            worst_homotopy["homotopy_neumann_product_upper"]
        ),
        "minimum_homotopy_denominator_lower": min(
            float(row["homotopy_denominator_lower"])
            for row in homotopy_rows
        ),
        "all_leaf_homotopies_certified": all_homotopies,
        "worst_homotopy_leaf": worst_homotopy,
        "triangular_inside_count": classification.inside_count,
        "triangular_outside_count": classification.outside_count,
        "triangular_boundary_count": classification.boundary_count,
        "nearest_diagonal_index": classification.nearest_index,
        "nearest_diagonal_real": classification.nearest_value.real,
        "nearest_diagonal_imag": classification.nearest_value.imag,
        "minimum_floating_diagonal_boundary_distance": (
            classification.minimum_floating_boundary_distance
        ),
        "nearest_exact_squared_margin_numerator": (
            classification.nearest_squared_margin_numerator
        ),
        "nearest_exact_squared_margin_denominator": (
            classification.nearest_squared_margin_denominator
        ),
        "interior_complement_pole_count_certified": (
            complement_count_certified
        ),
        "interior_complement_pole_count": complement_count,
        "inherited_stored_feshbach_boundary_winding": inherited_winding,
        "inherited_exact_augmented_minus_complement_count": (
            inherited_relative_count
        ),
        "ordinary_feshbach_zero_count_certified": (
            ordinary_zero_count_certified
        ),
        "ordinary_feshbach_zero_count": (
            inherited_winding if ordinary_zero_count_certified else None
        ),
        "stored_augmented_block_inside_count": (
            complement_count + inherited_relative_count
            if complement_count_certified
            else None
        ),
        "diagonal_ledger": str(diagonal_path.relative_to(ROOT)),
        "diagonal_ledger_sha256": sha256_file(diagonal_path),
        "diagonal_npz": str(diagonal_npz_path.relative_to(ROOT)),
        "diagonal_npz_sha256": sha256_file(diagonal_npz_path),
        "homotopy_ledger": str(homotopy_path.relative_to(ROOT)),
        "homotopy_ledger_sha256": sha256_file(homotopy_path),
        "environment_seconds": environment_seconds,
        "total_seconds": time.perf_counter() - total_started,
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "openblas_num_threads": os.environ.get("OPENBLAS_NUM_THREADS"),
            "omp_num_threads": os.environ.get("OMP_NUM_THREADS"),
        },
        "limitations": [
            "The theorem concerns the exact finite operator defined by stored binary64 factors.",
            "The floating Schur decomposition is only a source of stored comparison matrices; all decisive residual and unitarity bounds are outward rounded.",
            "No continuum or zero-noise limit is proved.",
            "No self-adjoint Hilbert-Polya operator, zeta-zero identification, or Riemann-hypothesis statement is claimed.",
        ],
    }
    output = arguments.output
    if output is None:
        output = (
            ROOT / "results" / f"schur_similarity_sigma_{sigma:.0e}.json"
        )
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not ordinary_zero_count_certified:
        raise RuntimeError("the RH-34 Schur-similarity gate did not close")


if __name__ == "__main__":
    main()
