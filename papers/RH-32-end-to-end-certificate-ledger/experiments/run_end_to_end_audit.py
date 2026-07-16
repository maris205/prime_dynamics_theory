"""Build the RH-32 projected-count and contour-composition ledger."""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
from pathlib import Path
import sys
import zipfile

import flint
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH29 = PAPERS / "RH-29-deflated-complement-resolvent"
RH31 = PAPERS / "RH-31-sparse-threshold-inertia"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

from certificate_ledger import (  # noqa: E402
    certify_projected_model,
    compose_lifted_bound,
    sha256_file,
    transport_arc_cover,
)
import run_contour_feshbach_audit as rh24_builder  # noqa: E402
import run_directional_closure_audit as rh25_builder  # noqa: E402


SIGMAS = (1.0e-2, 4.0e-3, 2.0e-3)
MODEL_STEMS = {
    1.0e-2: "1e-02",
    4.0e-3: "4e-03",
    2.0e-3: "2e-03",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def indexed(rows: list[dict[str, str]]) -> dict[float, dict[str, str]]:
    return {float(row["sigma"]): row for row in rows}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_deterministic_npz(path: Path, arrays: dict[str, np.ndarray]) -> None:
    """Write a reproducible NPZ with fixed ZIP metadata and sorted members."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        for name in sorted(arrays):
            stream = io.BytesIO()
            np.lib.format.write_array(
                stream, np.asarray(arrays[name]), allow_pickle=False
            )
            member = zipfile.ZipInfo(
                filename=f"{name}.npy", date_time=(1980, 1, 1, 0, 0, 0)
            )
            member.compress_type = zipfile.ZIP_DEFLATED
            member.external_attr = 0o600 << 16
            archive.writestr(member, stream.getvalue())


def rebuild_rh28_base_snapshot(
    sigma: float,
    output: Path,
) -> dict[str, object]:
    """Rebuild the exact primal base realization consumed by RH-28."""

    setting = rh24_builder.physical_settings()[float(sigma)]
    data = rh25_builder.build_physical_extended_model(float(sigma), setting)
    model = data["model"]
    depth = int(data["base_depth"])
    arrays: dict[str, np.ndarray] = {
        "reduced": np.asarray(model.reduced, dtype=np.complex128),
        "forcing_norms": np.asarray(model.forcing_norms, dtype=np.float64),
    }
    for column in range(model.packet_rank):
        arrays[f"hessenberg_{column}"] = np.asarray(
            model.hessenbergs[column], dtype=np.complex128
        )[: depth + 1, :depth]
        arrays[f"coupling_{column}"] = np.asarray(
            model.output_couplings[column], dtype=np.complex128
        )[:, :depth]
    write_deterministic_npz(output, arrays)

    discovery = (
        RH24
        / "results"
        / "models"
        / f"contour_model_sigma_{MODEL_STEMS[float(sigma)]}.npz"
    )
    distinct_fields = []
    maximum_difference = 0.0
    with np.load(discovery, allow_pickle=False) as archive:
        for name, value in arrays.items():
            comparison = np.asarray(archive[name])
            if not np.array_equal(value, comparison):
                distinct_fields.append(name)
                maximum_difference = max(
                    maximum_difference,
                    float(np.max(np.abs(value - comparison))),
                )
    return {
        "sigma": float(sigma),
        "packet_rank": int(model.packet_rank),
        "base_depth": depth,
        "maximum_depth_built_by_rh28": int(model.maximum_depth),
        "snapshot_path": relative(output),
        "snapshot_sha256": sha256_file(output),
        "rh24_discovery_model_path": relative(discovery),
        "rh24_discovery_model_sha256": sha256_file(discovery),
        "bitwise_equal_to_rh24_discovery_model": not distinct_fields,
        "distinct_fields": distinct_fields,
        "maximum_absolute_entry_difference": maximum_difference,
        "status": (
            "bitwise_identical"
            if not distinct_fields
            else "distinct_deterministic_base_realization"
        ),
    }


def relative(path: Path) -> str:
    return str(path.relative_to(REPOSITORY))


def add_node(nodes: dict[str, dict[str, str]], name: str, path: Path, role: str) -> None:
    nodes[name] = {
        "path": relative(path),
        "sha256": sha256_file(path),
        "role": role,
    }


def build_dependency_ledger(
    rh29_rows: dict[float, dict[str, str]],
    rh31_rows: dict[float, dict[str, str]],
    reconstruction_rows: dict[float, dict[str, object]],
) -> dict[str, object]:
    rh24_scale = RH24 / "results" / "scale_summary.csv"
    rh24_summary_path = RH24 / "results" / "contour_feshbach_summary.json"
    rh25_summary_path = RH25 / "results" / "directional_closure_summary.json"
    rh27_hybrid = RH27 / "results" / "hybrid_scale_summary.csv"
    rh28_arcs = RH28 / "results" / "arcwise_contour_arcs.csv"
    rh28_scale_path = RH28 / "results" / "arcwise_scale_summary.csv"
    rh28_meta_path = RH28 / "results" / "arcwise_metadata.json"
    reconstruction_verification_path = (
        ROOT / "results" / "rh28_reconstruction_verification.json"
    )
    rh29_meta_path = RH29 / "results" / "deflated_metadata.json"
    rh31_summary_path = RH31 / "results" / "summary.json"
    rh28_meta = json.loads(rh28_meta_path.read_text(encoding="utf-8"))
    rh29_meta = json.loads(rh29_meta_path.read_text(encoding="utf-8"))
    rh31_summary = json.loads(rh31_summary_path.read_text(encoding="utf-8"))
    rh24_summary = json.loads(rh24_summary_path.read_text(encoding="utf-8"))
    rh25_summary = json.loads(rh25_summary_path.read_text(encoding="utf-8"))
    reconstruction_verification = json.loads(
        reconstruction_verification_path.read_text(encoding="utf-8")
    )

    nodes: dict[str, dict[str, str]] = {}
    add_node(nodes, "rh24_scale_summary", rh24_scale, "stored contour geometry")
    add_node(nodes, "rh24_summary", rh24_summary_path, "RH-24 source-hash index")
    add_node(nodes, "rh25_summary", rh25_summary_path, "RH-25 source-hash index")
    add_node(nodes, "rh27_hybrid_summary", rh27_hybrid, "outward residual input")
    add_node(nodes, "rh28_arc_cover", rh28_arcs, "exact dyadic arc cover and budgets")
    add_node(
        nodes,
        "rh28_scale_summary",
        rh28_scale_path,
        "RH-28 deterministic scale fields",
    )
    add_node(nodes, "rh28_metadata", rh28_meta_path, "RH-28 provenance metadata")
    add_node(
        nodes,
        "rh28_reconstruction_verification",
        reconstruction_verification_path,
        "exact reproduction of all deterministic RH-28 archive fields",
    )
    add_node(
        nodes,
        "rh29_scale_summary",
        RH29 / "results" / "deflated_scale_summary.csv",
        "one-channel residuals and lifted budgets",
    )
    add_node(nodes, "rh29_metadata", rh29_meta_path, "RH-29 provenance metadata")
    add_node(
        nodes,
        "rh31_threshold_summary",
        RH31 / "results" / "threshold_inertia_summary.csv",
        "verified threshold-inertia bounds",
    )
    add_node(nodes, "rh31_summary", rh31_summary_path, "RH-31 source-hash index")

    checks: dict[str, bool] = {
        "rh28_records_rh24_scale_hash": (
            rh28_meta["input_hashes"]["rh24_scale_summary.csv"]
            == nodes["rh24_scale_summary"]["sha256"]
        ),
        "rh28_records_rh27_hybrid_hash": (
            rh28_meta["input_hashes"]["rh27_hybrid_scale_summary.csv"]
            == nodes["rh27_hybrid_summary"]["sha256"]
        ),
        "rh29_records_rh28_arc_hash": (
            rh29_meta["input_hashes"]["rh28_arcwise_contour_arcs.csv"]
            == nodes["rh28_arc_cover"]["sha256"]
        ),
        "rh28_reconstruction_all_fields_exact": (
            reconstruction_verification["status"]
            == "all_deterministic_rh28_fields_exactly_reproduced"
        ),
        "rh28_reconstruction_arc_hash": (
            reconstruction_verification["arc_archive_sha256"]
            == nodes["rh28_arc_cover"]["sha256"]
        ),
        "rh28_reconstruction_scale_hash": (
            reconstruction_verification["scale_archive_sha256"]
            == nodes["rh28_scale_summary"]["sha256"]
        ),
    }

    rh24_sources = {
        "audit.py": RH24 / "experiments" / "run_contour_feshbach_audit.py",
        "model.py": RH24 / "src" / "contour_feshbach" / "model.py",
        "rh18_gaussian_operators.py": PAPERS
        / "RH-18-branch-isolated-gaussian-return"
        / "src"
        / "gaussian_return"
        / "operators.py",
        "rh21_biorthogonal_algebra.py": PAPERS
        / "RH-21-peripheral-biorthogonal-branch-collapse"
        / "src"
        / "biorthogonal_branches"
        / "algebra.py",
        "rh23_packets.py": PAPERS
        / "RH-23-physical-packet-complement-feshbach"
        / "src"
        / "physical_feshbach"
        / "packets.py",
    }
    rh25_sources = {
        "algebra.py": RH25 / "src" / "directional_rouche" / "algebra.py",
        "audit.py": RH25 / "experiments" / "run_directional_closure_audit.py",
        "rh24_audit.py": rh24_sources["audit.py"],
        "rh24_model.py": rh24_sources["model.py"],
    }
    rh28_sources = {
        "coordinates.py": RH28 / "src" / "arcwise_feshbach" / "coordinates.py",
        "evaluator.py": RH28 / "src" / "arcwise_feshbach" / "evaluator.py",
        "geometry.py": RH28 / "src" / "arcwise_feshbach" / "geometry.py",
        "relations.py": RH28 / "src" / "arcwise_feshbach" / "relations.py",
        "run_arcwise_enclosure.py": RH28
        / "experiments"
        / "run_arcwise_enclosure.py",
    }
    for label, path in rh24_sources.items():
        node = f"rh24_source_{label.replace('.', '_')}"
        add_node(nodes, node, path, "RH-24 deterministic model source")
        checks[f"{node}_recorded_hash"] = (
            nodes[node]["sha256"] == rh24_summary["source_hashes"][label]
        )
    for label, path in rh25_sources.items():
        node = f"rh25_source_{label.replace('.', '_')}"
        add_node(nodes, node, path, "RH-25 extended-model source")
        checks[f"{node}_recorded_hash"] = (
            nodes[node]["sha256"] == rh25_summary["source_hashes"][label]
        )
    for label, path in rh28_sources.items():
        node = f"rh28_source_{label.replace('.', '_')}"
        add_node(nodes, node, path, "RH-28 arcwise construction source")
        checks[f"{node}_recorded_hash"] = (
            nodes[node]["sha256"] == rh28_meta["source_hashes"][label]
        )
    edges: list[dict[str, object]] = [
        {
            "source": "rh24_scale_summary",
            "target": "rh28_arc_cover",
            "relation": "recorded input hash",
            "verified": checks["rh28_records_rh24_scale_hash"],
        },
        {
            "source": "rh27_hybrid_summary",
            "target": "rh28_arc_cover",
            "relation": "recorded input hash",
            "verified": checks["rh28_records_rh27_hybrid_hash"],
        },
        {
            "source": "rh28_arc_cover",
            "target": "rh29_scale_summary",
            "relation": "recorded input hash",
            "verified": checks["rh29_records_rh28_arc_hash"],
        },
        {
            "source": "rh28_reconstruction_verification",
            "target": "rh28_arc_cover",
            "relation": "all non-timing arc and scale fields reproduced exactly",
            "verified": checks["rh28_reconstruction_all_fields_exact"],
        },
    ]

    for sigma in SIGMAS:
        stem = MODEL_STEMS[sigma]
        model_path = RH24 / "results" / "models" / f"contour_model_sigma_{stem}.npz"
        model_name = f"rh24_discovery_model_sigma_{stem}"
        add_node(nodes, model_name, model_path, "RH-24 discovery realization")

        snapshot_path = REPOSITORY / str(reconstruction_rows[sigma]["snapshot_path"])
        snapshot_name = f"rh28_base_snapshot_sigma_{stem}"
        add_node(
            nodes,
            snapshot_name,
            snapshot_path,
            "deterministically reconstructed RH-28 base realization",
        )
        snapshot_check = (
            nodes[snapshot_name]["sha256"]
            == reconstruction_rows[sigma]["snapshot_sha256"]
        )
        checks[f"{snapshot_name}_reconstruction_hash"] = snapshot_check
        edges.append(
            {
                "source": "rh25_summary",
                "target": snapshot_name,
                "relation": "deterministic RH-28 base-depth reconstruction with recorded source hashes",
                "verified": snapshot_check,
            }
        )

        triplet_path = RH29 / rh29_rows[sigma]["triplet_file"]
        triplet_name = f"rh29_triplet_sigma_{stem}"
        add_node(nodes, triplet_name, triplet_path, "stored dangerous singular channel")
        triplet_check = (
            nodes[triplet_name]["sha256"] == rh29_rows[sigma]["triplet_sha256"]
        )
        checks[f"{triplet_name}_recorded_hash"] = triplet_check
        edges.append(
            {
                "source": "rh28_arc_cover",
                "target": triplet_name,
                "relation": "selected RH-28 arc and RH-29 recorded triplet hash",
                "verified": triplet_check,
            }
        )

        certificate_path = RH31 / rh31_rows[sigma]["source_file"]
        certificate_name = f"rh31_certificate_sigma_{stem}"
        add_node(
            nodes,
            certificate_name,
            certificate_path,
            "exact-target sparse inertia certificate",
        )
        summary_hash = rh31_summary["source_hashes"][rh31_rows[sigma]["source_file"]]
        certificate_check = nodes[certificate_name]["sha256"] == summary_hash
        row_check = nodes[certificate_name]["sha256"] == rh31_rows[sigma]["source_sha256"]
        checks[f"{certificate_name}_summary_hash"] = certificate_check
        checks[f"{certificate_name}_row_hash"] = row_check
        edges.append(
            {
                "source": triplet_name,
                "target": certificate_name,
                "relation": "same stored singular channel; scalar identity audited separately",
                "verified": certificate_check and row_check,
            }
        )

    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"upstream provenance hash failure(s): {failures}")
    return {
        "status": "all_recorded_upstream_hashes_verified",
        "nodes": nodes,
        "edges": edges,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision", type=int, default=256)
    parser.add_argument(
        "--skip-projected-counts",
        action="store_true",
        help="reuse the existing projected-count JSON and rebuild the cheaper ledger",
    )
    arguments = parser.parse_args()
    precision = int(arguments.precision)
    results = ROOT / "results"
    results.mkdir(parents=True, exist_ok=True)

    rh24_rows = indexed(read_csv(RH24 / "results" / "scale_summary.csv"))
    rh28_scale_rows = indexed(
        read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
    )
    all_arcs = read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
    rh29_rows = indexed(read_csv(RH29 / "results" / "deflated_scale_summary.csv"))
    rh31_rows = indexed(
        read_csv(RH31 / "results" / "threshold_inertia_summary.csv")
    )

    projected_path = results / "projected_count_certificates.json"
    reconstruction_path = results / "model_reconstruction_audit.json"
    if arguments.skip_projected_counts:
        projected_payload = json.loads(projected_path.read_text(encoding="utf-8"))
        reconstruction_payload = json.loads(
            reconstruction_path.read_text(encoding="utf-8")
        )
    else:
        projected_scales = []
        reconstruction_scales = []
        for sigma in SIGMAS:
            row = rh28_scale_rows[sigma]
            model_path = (
                results
                / "models"
                / f"rh28_base_model_sigma_{MODEL_STEMS[sigma]}.npz"
            )
            print(f"rebuilding RH-28 base model at sigma={sigma:g}", flush=True)
            reconstruction = rebuild_rh28_base_snapshot(sigma, model_path)
            reconstruction_scales.append(reconstruction)
            center = complex(
                float(row["contour_center_real"]),
                float(row["contour_center_imag"]),
            )
            print(
                f"certifying reconstructed sigma={sigma:g}, model={model_path.name}, "
                f"precision={precision} bits",
                flush=True,
            )
            certificate, timings = certify_projected_model(
                model_path,
                center,
                float(row["contour_radius"]),
                precision=precision,
            )
            certificate["sigma"] = sigma
            certificate["model_path"] = relative(model_path)
            certificate["model_sha256"] = sha256_file(model_path)
            certificate["model_origin"] = (
                "deterministic RH-28 base-depth reconstruction"
            )
            projected_scales.append(certificate)
            print(
                "  count="
                f"{certificate['projected_zero_count']}-"
                f"{certificate['projected_pole_count']}="
                f"{certificate['projected_determinant_winding']}, "
                f"augmented solve {timings['augmented_eigensolve_seconds']:.2f}s",
                flush=True,
            )
            partial = {
                "status": "rigorous_exact_binary64_projected_counts",
                "arithmetic": "Arb eigenvalue balls with complete strict circle classification",
                "model_family": "RH-28 reconstructed primal base realizations",
                "precision_bits": precision,
                "python_flint": flint.__version__,
                "numpy": np.__version__,
                "scales": projected_scales,
            }
            write_json(projected_path, partial)
            reconstruction_partial = {
                "status": "deterministic_rh28_base_snapshots_archived",
                "construction": (
                    "RH-25 build_physical_extended_model, exactly the primal "
                    "base-model path called by RH-28"
                ),
                "important_nonidentity": (
                    "The RH-28 base snapshots are not silently identified with "
                    "the earlier RH-24 discovery NPZ files."
                ),
                "scales": reconstruction_scales,
            }
            write_json(reconstruction_path, reconstruction_partial)
        projected_payload = partial
        reconstruction_payload = reconstruction_partial

    reconstruction_rows = {
        float(row["sigma"]): row for row in reconstruction_payload["scales"]
    }

    coverage_rows = []
    composition_rows = []
    identity_checks: dict[str, bool] = {}
    for sigma in SIGMAS:
        rh24 = rh24_rows[sigma]
        rh28_scale = rh28_scale_rows[sigma]
        rh29 = rh29_rows[sigma]
        rh31 = rh31_rows[sigma]
        selected_arc = int(rh29["tightest_arc"])
        arcs = [row for row in all_arcs if float(row["sigma"]) == sigma]
        arcs.sort(key=lambda row: int(row["arc"]))
        selected = next(row for row in arcs if int(row["arc"]) == selected_arc)

        prefix = f"sigma_{MODEL_STEMS[sigma]}"
        identity_checks[f"{prefix}_rh24_rh28_center"] = (
            float(rh24["direct_center_real"]) == float(rh28_scale["contour_center_real"])
            and float(rh24["direct_center_imag"])
            == float(rh28_scale["contour_center_imag"])
        )
        identity_checks[f"{prefix}_rh24_rh28_radius"] = (
            float(rh24["selected_contour_radius"])
            == float(rh28_scale["contour_radius"])
        )
        identity_checks[f"{prefix}_rh28_rh29_selected_center"] = (
            float(selected["center_real"]) == float(rh29["spectral_parameter_real"])
            and float(selected["center_imag"])
            == float(rh29["spectral_parameter_imag"])
        )
        identity_checks[f"{prefix}_rh28_rh29_selected_radius"] = (
            float(selected["disc_radius"]) == float(rh29["arc_disc_radius"])
        )
        identity_checks[f"{prefix}_rh28_rh29_selected_budget"] = (
            float(selected["resolvent_budget_lower"])
            == float(rh29["rh28_arc_resolvent_budget_lower"])
        )
        identity_checks[f"{prefix}_rh29_rh31_dimension"] = (
            int(rh29["folded_dimension"]) == int(rh31["physical_dimension"])
        )
        expected_threshold = float(
            np.nextafter(
                2.0 / float(rh29["lifted_inverse_budget_lower"]), np.inf
            )
        )
        identity_checks[f"{prefix}_rh29_rh31_threshold"] = (
            expected_threshold == float(rh31["threshold"])
        )
        expected_inverse = float(
            np.nextafter(1.0 / float(rh31["threshold"]), np.inf)
        )
        identity_checks[f"{prefix}_rh31_inverse_summary"] = (
            expected_inverse == float(rh31["certified_full_grushin_inverse_upper"])
        )
        identity_checks[f"{prefix}_rh28_snapshot_rank"] = (
            int(reconstruction_rows[sigma]["packet_rank"])
            == int(rh28_scale["packet_rank"])
        )
        identity_checks[f"{prefix}_rh28_snapshot_depth"] = (
            int(reconstruction_rows[sigma]["base_depth"])
            == int(rh28_scale["base_depth"])
        )

        composed, center_bound = compose_lifted_bound(
            threshold=float(rh31["threshold"]),
            singular_scalar=float(rh29["stored_singular_scalar"]),
            right_residual_upper=float(rh29["normalized_right_residual_norm_upper"]),
            left_residual_upper=float(rh29["normalized_left_residual_norm_upper"]),
            lift=float(rh29["lift"]),
            selected_arc_radius_upper=float(rh29["arc_disc_radius"]),
            selected_arc_budget_lower=float(
                rh29["rh28_arc_resolvent_budget_lower"]
            ),
            precision=precision,
        )
        transports = transport_arc_cover(
            sigma=sigma,
            source_center=complex(
                float(rh29["spectral_parameter_real"]),
                float(rh29["spectral_parameter_imag"]),
            ),
            center_inverse_upper=center_bound,
            arcs=arcs,
            selected_arc=selected_arc,
            precision=precision,
        )
        closed = [row for row in transports if row.status == "closed"]
        failed = [row for row in transports if row.status == "neumann_failure"]
        ambiguous = [
            row for row in transports if row.status == "ambiguous_neumann_boundary"
        ]
        budget_failures = [row for row in transports if row.status == "budget_failure"]
        unselected = [row for row in transports if not row.selected]
        selected_transport = next(row for row in transports if row.selected)
        nearest_unselected = min(
            unselected, key=lambda row: row.neumann_product_lower
        )
        composition_rows.append(
            {
                "sigma": sigma,
                "selected_arc": selected_arc,
                "accepted_arc_count": len(arcs),
                "transport_closed_arc_count": len(closed),
                "neumann_failure_arc_count": len(failed),
                "budget_failure_arc_count": len(budget_failures),
                "ambiguous_arc_count": len(ambiguous),
                "lifted_inverse_upper": composed.lifted_inverse_upper,
                "sherman_morrison_denominator_lower": composed.denominator_lower,
                "center_inverse_upper": composed.center_inverse_upper,
                "selected_arc_neumann_product_upper": selected_transport.neumann_product_upper,
                "nearest_unselected_arc": nearest_unselected.arc,
                "nearest_unselected_neumann_product_lower": nearest_unselected.neumann_product_lower,
                "selected_arc_inverse_upper": composed.selected_arc_inverse_upper,
                "selected_arc_budget_lower": composed.selected_arc_budget_lower,
                "selected_arc_budget_margin_lower": math.nextafter(
                    composed.selected_arc_budget_lower
                    / composed.selected_arc_inverse_upper,
                    -math.inf,
                ),
                "selected_arc_closed": int(composed.selected_arc_closed),
                "full_contour_closed": int(len(closed) == len(arcs)),
            }
        )
        coverage_rows.extend(transports)

    if not all(identity_checks.values()):
        failures = [name for name, passed in identity_checks.items() if not passed]
        raise RuntimeError(f"cross-paper object identity failure(s): {failures}")

    composition_path = results / "composition_summary.csv"
    with composition_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(composition_rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(composition_rows)

    coverage_path = results / "arc_transport_coverage.csv"
    coverage_fields = [
        "sigma",
        "arc",
        "selected",
        "center_distance_upper",
        "disc_distance_upper",
        "neumann_product_lower",
        "neumann_product_upper",
        "transported_inverse_upper",
        "arc_budget_lower",
        "status",
    ]
    with coverage_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=coverage_fields, lineterminator="\n"
        )
        writer.writeheader()
        for record in coverage_rows:
            writer.writerow({field: getattr(record, field) for field in coverage_fields})

    object_identity_path = results / "object_identity_checks.json"
    write_json(
        object_identity_path,
        {
            "status": "all_cross_paper_object_identities_verified",
            "checks": identity_checks,
            "model_relationships": {
                MODEL_STEMS[sigma]: {
                    "rh28_snapshot": reconstruction_rows[sigma]["snapshot_path"],
                    "rh24_discovery_model": reconstruction_rows[sigma][
                        "rh24_discovery_model_path"
                    ],
                    "bitwise_equal": reconstruction_rows[sigma][
                        "bitwise_equal_to_rh24_discovery_model"
                    ],
                    "maximum_absolute_entry_difference": reconstruction_rows[
                        sigma
                    ]["maximum_absolute_entry_difference"],
                }
                for sigma in SIGMAS
            },
        },
    )
    dependency_path = results / "dependency_ledger.json"
    write_json(
        dependency_path,
        build_dependency_ledger(rh29_rows, rh31_rows, reconstruction_rows),
    )

    discovery_counts_path = results / "rh24_discovery_count_certificates.json"
    reconstruction_verification_path = (
        results / "rh28_reconstruction_verification.json"
    )
    result_hashes = {
        path.name: sha256_file(path)
        for path in (
            projected_path,
            reconstruction_path,
            reconstruction_verification_path,
            discovery_counts_path,
            composition_path,
            coverage_path,
            object_identity_path,
            dependency_path,
        )
    }
    summary = {
        "status": "projected_base_certified_selected_arcs_closed_full_contours_open",
        "sigmas": list(SIGMAS),
        "projected_counts": [
            {
                "sigma": row["sigma"],
                "zeros": row["projected_zero_count"],
                "poles": row["projected_pole_count"],
                "winding": row["projected_determinant_winding"],
            }
            for row in projected_payload["scales"]
        ],
        "selected_arc_closures": composition_rows,
        "result_hashes": result_hashes,
        "closed_gates": [
            "rigorous projected zero/pole count and winding for the reconstructed RH-28 base model at three stored scales",
            "exact reproduction of every deterministic RH-28 arc and scale archive field",
            "RH-31 to RH-29 to RH-28 composition on each selected tightest-budget arc",
            "cross-paper geometry/scalar identity and recorded source/input-hash chain",
        ],
        "remaining_gates": [
            "validated complement-resolvent coverage on every other RH-28 arc",
            "rigorous complement pole count, equivalently interior analyticity of the exact finite Feshbach map",
        ],
        "scope": "exact stored binary64 finite models only",
        "nonclaims": [
            "no full-contour exact root count",
            "no continuum or zero-noise limit",
            "no Hilbert-Polya operator",
            "no identification with zeta zeros",
            "no Riemann-hypothesis implication",
        ],
    }
    write_json(results / "summary.json", summary)
    print("wrote rigorous projected counts and end-to-end ledger", flush=True)


if __name__ == "__main__":
    main()
