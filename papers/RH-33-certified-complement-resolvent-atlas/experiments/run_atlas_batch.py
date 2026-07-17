"""Run a resumable parallel batch of direct complement certificates."""

from __future__ import annotations

import argparse
import csv
import json
from multiprocessing import get_context
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH30 = PAPERS / "RH-30-sparse-two-step-grushin-inverse"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH30 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from outward_residuals import ComponentwiseStoredFactorGraph  # noqa: E402
from resolvent_atlas import (  # noqa: E402
    build_direct_grushin_system,
    certify_arc_coverage,
    certify_direct_inverse,
)


_WORKER_CONTEXT = None


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _initialize_worker(sigma: float, chunk_size: int) -> None:
    global _WORKER_CONTEXT
    environment = rh25_global.build_environment(
        float(sigma), rh24.physical_settings()[float(sigma)]
    )
    spectrum = environment["spectrum"]
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )
    arcs = [
        row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == float(sigma)
    ]
    _WORKER_CONTEXT = {
        "sigma": float(sigma),
        "chunk_size": int(chunk_size),
        "environment": environment,
        "spectrum": spectrum,
        "graph": graph,
        "arcs": arcs,
    }


def _certify_target(target: dict[str, object]) -> dict[str, object]:
    if _WORKER_CONTEXT is None:
        raise RuntimeError("worker context is not initialized")
    arcs = _WORKER_CONTEXT["arcs"]
    point = complex(
        float(target["spectral_parameter_real"]),
        float(target["spectral_parameter_imag"]),
    )
    environment = _WORKER_CONTEXT["environment"]
    spectrum = _WORKER_CONTEXT["spectrum"]
    system = build_direct_grushin_system(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
        point,
    )
    certificate = certify_direct_inverse(
        system,
        _WORKER_CONTEXT["graph"],
        point,
        chunk_size=_WORKER_CONTEXT["chunk_size"],
    )
    coverage = [
        certify_arc_coverage(point, certificate.center_inverse_two_norm_upper, row)
        for row in arcs
    ]
    closed = [row.arc for row in coverage if row.closed]
    payload = {
        "status": (
            "rigorous_direct_center_certificate"
            if certificate.admissible
            else "failed_direct_center_certificate"
        ),
        "sigma": _WORKER_CONTEXT["sigma"],
        "center_id": str(target["center_id"]),
        "source_kind": str(target["source_kind"]),
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "physical_dimension": int(system.physical_dimension),
        "border_rank": int(system.border_rank),
        "bordered_dimension": int(system.bordered_dimension),
        "matrix_nnz": int(system.matrix.nnz),
        "factor_nnz": certificate.factor_nnz,
        "factor_seconds": certificate.factor_seconds,
        "certificate_seconds": certificate.certificate_seconds,
        "approximate_inverse_frobenius_upper": certificate.approximate_inverse_frobenius_upper,
        "residual_frobenius_upper": certificate.residual_frobenius_upper,
        "residual_center_frobenius_upper": certificate.residual_center_frobenius_upper,
        "residual_radius_frobenius_upper": certificate.residual_radius_frobenius_upper,
        "center_inverse_two_norm_upper": certificate.center_inverse_two_norm_upper,
        "inverse_sha256": certificate.inverse_sha256,
        "residual_center_sha256": certificate.residual_center_sha256,
        "residual_radius_sha256": certificate.residual_radius_sha256,
        "closed_arc_count": len(closed),
        "closed_arcs": closed,
        "closed_arc_minimum": min(closed) if closed else None,
        "closed_arc_maximum": max(closed) if closed else None,
    }
    for key in (
        "source_arc",
        "component",
        "parent_arcs",
        "turn_numerator",
        "turn_denominator",
    ):
        if key in target:
            payload[key] = target[key]
    return payload


def arc_target(arcs: list[dict[str, str]], arc_id: int) -> dict[str, object]:
    selected = next(row for row in arcs if int(row["arc"]) == int(arc_id))
    return {
        "center_id": f"arc_{int(arc_id):05d}",
        "source_kind": "rh28_parent_arc_midpoint",
        "source_arc": int(arc_id),
        "spectral_parameter_real": float(selected["center_real"]),
        "spectral_parameter_imag": float(selected["center_imag"]),
    }


def validate_target(target: dict[str, object]) -> dict[str, object]:
    required = {
        "center_id",
        "source_kind",
        "spectral_parameter_real",
        "spectral_parameter_imag",
    }
    missing = sorted(required - set(target))
    if missing:
        raise ValueError(f"atlas target is missing fields: {missing}")
    identifier = str(target["center_id"])
    if re.fullmatch(r"[A-Za-z0-9_-]+", identifier) is None:
        raise ValueError(f"unsafe center identifier: {identifier!r}")
    normalized = dict(target)
    normalized["center_id"] = identifier
    normalized["source_kind"] = str(target["source_kind"])
    normalized["spectral_parameter_real"] = float(
        target["spectral_parameter_real"]
    )
    normalized["spectral_parameter_imag"] = float(
        target["spectral_parameter_imag"]
    )
    return normalized


def targets_from_file(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = (
        payload.get("suggested_centers", payload)
        if isinstance(payload, dict)
        else payload
    )
    if not isinstance(rows, list):
        raise ValueError("target file must be a list or contain suggested_centers")
    return [validate_target(dict(row)) for row in rows]


def record_center_identifier(record: dict[str, object]) -> str:
    if "center_id" in record:
        return str(record["center_id"])
    return f"arc_{int(record['source_arc']):05d}"


def initial_grid_arcs(arcs: list[dict[str, str]], count: int) -> list[int]:
    angles = np.asarray([float(row["theta_midpoint"]) for row in arcs])
    selected = []
    for index in range(int(count)):
        target = 2.0 * np.pi * (index + 0.5) / int(count)
        distance = np.abs(np.angle(np.exp(1.0j * (angles - target))))
        selected.append(int(arcs[int(np.argmin(distance))]["arc"]))
    return sorted(set(selected))


def uncovered_runs(total: int, covered: set[int]) -> list[list[int]]:
    missing = [index for index in range(int(total)) if index not in covered]
    if not missing:
        return []
    runs = [[missing[0]]]
    for value in missing[1:]:
        if value == runs[-1][-1] + 1:
            runs[-1].append(value)
        else:
            runs.append([value])
    if len(runs) > 1 and runs[0][0] == 0 and runs[-1][-1] == total - 1:
        runs[0] = runs[-1] + runs[0]
        runs.pop()
    return runs


def write_summary(sigma: float, arcs: list[dict[str, str]], center_dir: Path) -> None:
    records = []
    for path in sorted(center_dir.glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        if record["status"] == "rigorous_direct_center_certificate":
            source = complex(
                float(record["spectral_parameter_real"]),
                float(record["spectral_parameter_imag"]),
            )
            coverage = [
                certify_arc_coverage(
                    source,
                    float(record["center_inverse_two_norm_upper"]),
                    row,
                )
                for row in arcs
            ]
            closed = [row.arc for row in coverage if row.closed]
            record["closed_arc_count"] = len(closed)
            record["closed_arcs"] = closed
            record["closed_arc_minimum"] = min(closed) if closed else None
            record["closed_arc_maximum"] = max(closed) if closed else None
            path.write_text(
                json.dumps(record, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        records.append(record)
    covered: set[int] = set()
    for row in records:
        if row["status"] == "rigorous_direct_center_certificate":
            covered.update(int(value) for value in row["closed_arcs"])
    runs = uncovered_runs(len(arcs), covered)
    payload = {
        "status": "full_boundary_atlas" if not runs else "partial_boundary_atlas",
        "sigma": float(sigma),
        "center_count": len(records),
        "certified_center_count": sum(
            row["status"] == "rigorous_direct_center_certificate" for row in records
        ),
        "arc_count": len(arcs),
        "covered_arc_count": len(covered),
        "uncovered_arc_count": len(arcs) - len(covered),
        "uncovered_runs": [
            {
                "length": len(run),
                "first": run[0],
                "last": run[-1],
                "middle": run[len(run) // 2],
            }
            for run in runs
        ],
        "minimum_center_inverse_upper": min(
            (row["center_inverse_two_norm_upper"] for row in records),
            default=None,
        ),
        "maximum_center_inverse_upper": max(
            (row["center_inverse_two_norm_upper"] for row in records),
            default=None,
        ),
        "center_ids": sorted(
            record_center_identifier(row) for row in records
        ),
        "center_arcs": sorted(
            int(row["source_arc"]) for row in records if "source_arc" in row
        ),
    }
    path = ROOT / "results" / f"atlas_sigma_{sigma:.0e}_summary.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--initial-grid", type=int)
    parser.add_argument("--arcs", nargs="*", type=int)
    parser.add_argument("--target-file", type=Path)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--chunk-size", type=int, default=256)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    arcs = [
        row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    ]
    if arguments.target_file is not None:
        target_file = arguments.target_file
        if not target_file.is_absolute():
            target_file = ROOT / target_file
        requested = targets_from_file(target_file)
    elif arguments.arcs:
        requested = [
            arc_target(arcs, value)
            for value in sorted(set(int(value) for value in arguments.arcs))
        ]
    elif arguments.initial_grid:
        requested = [
            arc_target(arcs, value)
            for value in initial_grid_arcs(arcs, int(arguments.initial_grid))
        ]
    else:
        raise ValueError("provide --arcs, --initial-grid, or --target-file")
    unique = {}
    for target in requested:
        normalized = validate_target(target)
        unique[str(normalized["center_id"])] = normalized
    requested = [unique[key] for key in sorted(unique)]
    center_dir = ROOT / "results" / "centers" / f"sigma_{sigma:.0e}"
    center_dir.mkdir(parents=True, exist_ok=True)
    pending = [
        target
        for target in requested
        if not (center_dir / f"{target['center_id']}.json").exists()
    ]
    print(
        f"atlas batch sigma={sigma:g}: requested={len(requested)}, pending={len(pending)}, "
        f"workers={arguments.workers}",
        flush=True,
    )
    if pending:
        context = get_context("fork")
        with context.Pool(
            processes=int(arguments.workers),
            initializer=_initialize_worker,
            initargs=(sigma, int(arguments.chunk_size)),
        ) as pool:
            for result in pool.imap_unordered(_certify_target, pending, chunksize=1):
                path = center_dir / f"{result['center_id']}.json"
                path.write_text(
                    json.dumps(result, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                print(
                    f"completed center={result['center_id']}: "
                    f"M={result['center_inverse_two_norm_upper']:.6g}, "
                    f"closed={result['closed_arc_count']}",
                    flush=True,
                )
    write_summary(sigma, arcs, center_dir)


if __name__ == "__main__":
    main()
