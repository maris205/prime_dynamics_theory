"""Run resumable rigorous coarse physical-resolvent center certificates."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
from fractions import Fraction
from multiprocessing import get_context
from pathlib import Path
import re
import sys

import numpy as np
from scipy.sparse import csr_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
sys.path[:0] = [
    str(RH27 / "src"),
    str(RH30 / "src"),
    str(RH33 / "src"),
]

from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402
from resolvent_atlas import (  # noqa: E402
    build_direct_grushin_system,
    certify_direct_inverse,
    contour_point,
    turn_center_id,
)


_WORKER_CONTEXT = None


def sparse_from_snapshot(data, prefix: str) -> csr_matrix:
    shape = tuple(int(value) for value in data[f"{prefix}_shape"])
    return csr_matrix(
        (
            np.asarray(data[f"{prefix}_data"]).copy(),
            np.asarray(data[f"{prefix}_indices"]).copy(),
            np.asarray(data[f"{prefix}_indptr"]).copy(),
        ),
        shape=shape,
    )


def _initialize_worker(
    snapshot: str,
    contour_center_real: float,
    contour_center_imag: float,
    contour_radius: float,
    chunk_size: int,
) -> None:
    global _WORKER_CONTEXT
    with np.load(snapshot) as data:
        matrix = sparse_from_snapshot(data, "coarse_matrix")
        right = np.asarray(data["coarse_right_modes"]).copy()
        left = np.asarray(data["coarse_left_modes"]).copy()
        values = np.asarray(data["coarse_peripheral_values"]).copy()
        sigma = float(data["sigma"])
    dimension = int(matrix.shape[0])
    empty_synthesis = np.empty((dimension, 0), dtype=np.float64)
    empty_analysis = np.empty((0, dimension), dtype=np.float64)
    graph = ComponentwiseStoredFactorGraph(
        matrix,
        right,
        left,
        values,
        empty_synthesis,
        empty_analysis,
    )

    class PhysicalGraph:
        @staticmethod
        def action(source):
            return graph.two_step(source)

    _WORKER_CONTEXT = {
        "snapshot": snapshot,
        "sigma": sigma,
        "matrix": matrix,
        "right": right,
        "left": left,
        "values": values,
        "empty_synthesis": empty_synthesis,
        "empty_analysis": empty_analysis,
        "graph": PhysicalGraph(),
        "center": complex(contour_center_real, contour_center_imag),
        "radius": float(contour_radius),
        "chunk_size": int(chunk_size),
    }


def _certify_target(target: dict[str, object]) -> dict[str, object]:
    if _WORKER_CONTEXT is None:
        raise RuntimeError("worker context is not initialized")
    point = complex(
        float(target["spectral_parameter_real"]),
        float(target["spectral_parameter_imag"]),
    )
    system = build_direct_grushin_system(
        _WORKER_CONTEXT["matrix"],
        _WORKER_CONTEXT["right"],
        _WORKER_CONTEXT["left"],
        _WORKER_CONTEXT["values"],
        _WORKER_CONTEXT["empty_synthesis"],
        _WORKER_CONTEXT["empty_analysis"],
        point,
    )
    with contextlib.redirect_stdout(io.StringIO()):
        certificate = certify_direct_inverse(
            system,
            _WORKER_CONTEXT["graph"],
            point,
            chunk_size=_WORKER_CONTEXT["chunk_size"],
        )
    return {
        "status": (
            "rigorous_physical_resolvent_center"
            if certificate.admissible
            else "failed_physical_resolvent_center"
        ),
        "sigma": _WORKER_CONTEXT["sigma"],
        "center_id": str(target["center_id"]),
        "source_kind": str(target["source_kind"]),
        "turn_numerator": int(target["turn_numerator"]),
        "turn_denominator": int(target["turn_denominator"]),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "physical_dimension": int(system.physical_dimension),
        "border_rank": int(system.border_rank),
        "bordered_dimension": int(system.bordered_dimension),
        "matrix_nnz": int(system.matrix.nnz),
        "factor_nnz": certificate.factor_nnz,
        "factor_seconds": certificate.factor_seconds,
        "certificate_seconds": certificate.certificate_seconds,
        "approximate_inverse_frobenius_upper": (
            certificate.approximate_inverse_frobenius_upper
        ),
        "residual_frobenius_upper": certificate.residual_frobenius_upper,
        "residual_center_frobenius_upper": (
            certificate.residual_center_frobenius_upper
        ),
        "residual_radius_frobenius_upper": (
            certificate.residual_radius_frobenius_upper
        ),
        "center_inverse_two_norm_upper": (
            certificate.center_inverse_two_norm_upper
        ),
        "inverse_sha256": certificate.inverse_sha256,
        "residual_center_sha256": certificate.residual_center_sha256,
        "residual_radius_sha256": certificate.residual_radius_sha256,
    }


def validate_target(target: dict[str, object]) -> dict[str, object]:
    required = {
        "center_id",
        "source_kind",
        "turn_numerator",
        "turn_denominator",
        "spectral_parameter_real",
        "spectral_parameter_imag",
    }
    missing = sorted(required - set(target))
    if missing:
        raise ValueError(f"target is missing fields: {missing}")
    identifier = str(target["center_id"])
    if re.fullmatch(r"[A-Za-z0-9_-]+", identifier) is None:
        raise ValueError(f"unsafe center identifier: {identifier!r}")
    result = dict(target)
    result["center_id"] = identifier
    result["source_kind"] = str(target["source_kind"])
    result["turn_numerator"] = int(target["turn_numerator"])
    result["turn_denominator"] = int(target["turn_denominator"])
    result["spectral_parameter_real"] = float(
        target["spectral_parameter_real"]
    )
    result["spectral_parameter_imag"] = float(
        target["spectral_parameter_imag"]
    )
    return result


def target_at_turn(
    center: complex, radius: float, turn: Fraction, source_kind: str
) -> dict[str, object]:
    reduced = Fraction(turn) % 1
    point = contour_point(center, radius, reduced)
    return {
        "center_id": turn_center_id(reduced),
        "source_kind": source_kind,
        "turn_numerator": int(reduced.numerator),
        "turn_denominator": int(reduced.denominator),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
    }


def initial_targets(center: complex, radius: float, count: int):
    total = int(count)
    return [
        target_at_turn(
            center,
            radius,
            Fraction(2 * index + 1, 2 * total),
            "uniform_rational_turn",
        )
        for index in range(total)
    ]


def targets_from_file(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("suggested_centers", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        raise ValueError("target file must be a list or contain suggested_centers")
    return [validate_target(dict(row)) for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=Path("results/nested_grid_snapshot_sigma_1e-02.npz"),
    )
    parser.add_argument(
        "--block-certificate",
        type=Path,
        default=Path("results/nested_block_certificate_sigma_1e-02.json"),
    )
    parser.add_argument("--initial-grid", type=int)
    parser.add_argument("--target-file", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=256)
    arguments = parser.parse_args()

    snapshot = arguments.snapshot
    if not snapshot.is_absolute():
        snapshot = ROOT / snapshot
    block_path = arguments.block_certificate
    if not block_path.is_absolute():
        block_path = ROOT / block_path
    block = json.loads(block_path.read_text(encoding="utf-8"))
    center = complex(
        float(block["contour_center_real"]),
        float(block["contour_center_imag"]),
    )
    radius = float(block["contour_radius"])
    if arguments.target_file is not None:
        target_file = arguments.target_file
        if not target_file.is_absolute():
            target_file = ROOT / target_file
        requested = targets_from_file(target_file)
    elif arguments.initial_grid is not None:
        requested = initial_targets(center, radius, int(arguments.initial_grid))
    else:
        raise ValueError("provide --initial-grid or --target-file")
    unique = {}
    for target in requested:
        normalized = validate_target(target)
        unique[normalized["center_id"]] = normalized
    requested = [unique[key] for key in sorted(unique)]
    center_dir = ROOT / "results" / "physical_centers_sigma_1e-02"
    center_dir.mkdir(parents=True, exist_ok=True)
    pending = [
        target
        for target in requested
        if not (center_dir / f"{target['center_id']}.json").exists()
    ]
    print(
        f"physical atlas batch requested={len(requested)}, pending={len(pending)}, "
        f"workers={arguments.workers}",
        flush=True,
    )
    if pending:
        context = get_context("fork")
        with context.Pool(
            processes=int(arguments.workers),
            initializer=_initialize_worker,
            initargs=(
                str(snapshot),
                center.real,
                center.imag,
                radius,
                int(arguments.chunk_size),
            ),
        ) as pool:
            for result in pool.imap_unordered(_certify_target, pending, chunksize=1):
                path = center_dir / f"{result['center_id']}.json"
                path.write_text(
                    json.dumps(result, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                print(
                    f"completed {result['center_id']}: "
                    f"M={result['center_inverse_two_norm_upper']:.8g}",
                    flush=True,
                )


if __name__ == "__main__":
    main()
