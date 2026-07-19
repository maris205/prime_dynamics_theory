"""Verify RH-44 hashes, rank-two gates, and theorem boundaries."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_hashes() -> tuple[dict[str, object], dict[str, object]]:
    summary = load(ROOT / "results" / "summary.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external input mismatch: {path}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"local source mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication artifact mismatch: {relative}")
    return summary, dependency


def verify_dependency_links(
    multilevel: dict[str, object],
    rank_two: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    if multilevel["source_sha256"] != sha256_file(
        ROOT / "experiments" / "run_multilevel_perron_grushin.py"
    ):
        raise RuntimeError("multilevel Perron source hash is stale")
    multilevel_links = {
        "rh36_snapshot": "rh36_factor_snapshot",
        "rh37_snapshot": "rh37_factor_snapshot",
        "rh43_multilevel_grushin_engine": "rh43_multilevel_grushin_engine",
    }
    for certificate_name, manifest_name in multilevel_links.items():
        if multilevel["dependencies"][certificate_name] != external[
            manifest_name
        ]:
            raise RuntimeError(
                f"multilevel dependency mismatch: {certificate_name}"
            )

    local_record = rank_two["dependencies"][
        "multilevel_perron_grushin_certificate"
    ]
    local_path = ROOT / "results" / "multilevel_perron_grushin.json"
    if REPOSITORY / local_record["path"] != local_path:
        raise RuntimeError("rank-two local dependency path mismatch")
    if local_record["sha256"] != sha256_file(local_path):
        raise RuntimeError("rank-two local dependency hash mismatch")

    for name in (
        "rh36_factor_snapshot",
        "rh37_factor_snapshot",
        "rh39_cutoff_certificate",
        "rh40_projector_builder",
        "rh40_weighted_riesz_certificate",
        "rh42_uniform_euclidean_certificate",
        "rh42_midpoint_bridge",
        "rh43_intrinsic_parity_certificate",
        "rh43_weighted_kernel_source",
    ):
        if rank_two["dependencies"][name] != external[name]:
            raise RuntimeError(f"rank-two dependency mismatch: {name}")


def verify_multilevel(multilevel: dict[str, object]) -> None:
    if multilevel["status"] != (
        "rigorous_multilevel_exact_stored_euclidean_perron_factors"
    ):
        raise RuntimeError("multilevel Perron status is not closed")
    if multilevel["contour_radius"] != 0.05:
        raise RuntimeError("unexpected Perron contour radius")
    if set(multilevel["levels"]) != {"2048", "4096", "8192"}:
        raise RuntimeError("unexpected Perron dimensions")
    expected_snapshot = {
        "2048": multilevel["dependencies"]["rh36_snapshot"]["sha256"],
        "4096": multilevel["dependencies"]["rh36_snapshot"]["sha256"],
        "8192": multilevel["dependencies"]["rh37_snapshot"]["sha256"],
    }
    for name, row in multilevel["levels"].items():
        if row["status"] != (
            "rigorous_exact_stored_euclidean_perron_circle_count_one"
        ):
            raise RuntimeError(f"stored Perron circle is not closed: {name}")
        if row["hashes"]["snapshot"] != expected_snapshot[name]:
            raise RuntimeError(f"stored Perron snapshot mismatch: {name}")
        if row["residual_two_upper"] >= 4.0e-10:
            raise RuntimeError(f"Perron inverse residual gate failed: {name}")
        ledger = row["contour_ledger"]
        if not ledger["bordered_disk_invertible"] or not ledger[
            "rouche_count_one"
        ]:
            raise RuntimeError(f"Perron Grushin gate failed: {name}")
        if ledger["center_transport_product_upper"] >= 0.69:
            raise RuntimeError(f"Perron center transport gate failed: {name}")
        if ledger["contour_resolvent_upper"] >= 66.0:
            raise RuntimeError(f"Perron resolvent gate failed: {name}")


def verify_rank_two(rank_two: dict[str, object]) -> None:
    if rank_two["status"] != (
        "rigorous_intrinsic_rank_two_peripheral_kernel_and_bulk_deflation"
    ):
        raise RuntimeError("rank-two status is not closed")
    contours = rank_two["contours"]
    if not contours["disjoint"] or contours["union_inside_count"] != 2:
        raise RuntimeError("disjoint union-contour gate failed")

    factors = rank_two["stored_perron_factor_validation"]
    if not factors["all_three_levels_are_actual_spectral_factors"]:
        raise RuntimeError("not every Perron factor is spectral")
    for name, row in factors["levels"].items():
        if not row["admissible"]:
            raise RuntimeError(f"Perron correction failed: {name}")
        if row["weighted_term_error_upper"] >= 8.4e-10:
            raise RuntimeError(f"Perron weighted-term gate failed: {name}")

    haar = rank_two["stored_rank_two_haar_law"]
    if haar["status"] != (
        "rigorous_actual_stored_rank_two_quarter_half_mechanism"
    ):
        raise RuntimeError("actual rank-two Haar status is not closed")
    if haar["arb_precision_bits"] < 224:
        raise RuntimeError("rank-two Haar precision gate failed")
    if not haar["all_ratio_targets_within_one_thousandth"]:
        raise RuntimeError("rank-two quarter--half gate failed")
    for name, row in haar["actual_spectral_ratios"].items():
        if not 0.0 < row["lower"] <= row["upper"]:
            raise RuntimeError(f"invalid rank-two Haar interval: {name}")
        if row["maximum_target_deviation"] >= 1.0e-3:
            raise RuntimeError(f"rank-two Haar target failed: {name}")

    perron = rank_two["perron_continuum_contour"]
    if perron["continuum_inside_count"] != 1:
        raise RuntimeError("continuum Perron count is not one")
    if not perron["continuum_eigenvalue_is_exactly_one_and_simple"]:
        raise RuntimeError("continuum Perron identity is missing")
    if perron["continuum_L2_resolvent_upper"] >= 82.0:
        raise RuntimeError("continuum Perron resolvent gate failed")
    if not perron["center_shift_transfer"]["admissible"]:
        raise RuntimeError("Perron center-shift gate failed")
    if not perron["infinite_complement"]["resolvent_step"][
        "count_transfers"
    ]:
        raise RuntimeError("Perron infinite complement did not transfer")

    perron_kernel = rank_two["intrinsic_perron_kernel"]
    if perron_kernel["rank"] != 1 or not perron_kernel[
        "source_independent"
    ]:
        raise RuntimeError("intrinsic Perron-kernel gate failed")
    envelope = perron_kernel["envelope"]
    if envelope["source_first_hilbert_schmidt_upper"] != 0.0:
        raise RuntimeError("Perron source derivative is not zero")
    if envelope["midpoint_to_cell_average_upper"] >= 2.6e-6:
        raise RuntimeError("Perron midpoint gate failed")

    kernel = rank_two["intrinsic_rank_two_kernel"]
    if kernel["rank"] != 2 or not kernel["real_smooth_gauge_free"]:
        raise RuntimeError("intrinsic rank-two kernel gate failed")
    if kernel[
        "continuum_kernel_L2_distance_from_combined_4096_center_upper"
    ] >= 3.9:
        raise RuntimeError("rank-two construction ball failed")

    family = rank_two["uniform_perron_and_rank_two_families"]
    if family["certified_threshold_dimension"] != 65536:
        raise RuntimeError("unexpected rank-two all-grid threshold")
    if family["uniform_union_contour_resolvent_upper"] >= 268.0:
        raise RuntimeError("union-contour resolvent gate failed")
    if family["uniform_rank_two_weighted_riesz_cutoff_upper"] >= 1.0e-9:
        raise RuntimeError("rank-two weighted cutoff gate failed")
    if family[
        "uniform_rank_two_intrinsically_deflated_cutoff_upper"
    ] >= 1.0e-9:
        raise RuntimeError("rank-two deflated cutoff gate failed")
    if family["fixed_eight_sigma_convergence_to_full_claimed"]:
        raise RuntimeError("fixed-width theorem boundary is incorrect")

    bulk = rank_two["intrinsic_bulk_operator"]
    if not bulk["perron_and_parity_eigenvalues_are_replaced_by_zero"]:
        raise RuntimeError("bulk peripheral annihilation is missing")
    if not bulk["remaining_spectrum_is_unchanged_away_from_zero"]:
        raise RuntimeError("bulk remaining-spectrum claim is missing")
    for name in (
        "power_identity",
        "trace_identity",
        "fredholm_determinant_factorization",
    ):
        if not bulk[name]:
            raise RuntimeError(f"bulk algebra field is missing: {name}")
    if not bulk["factorization_is_structural_not_arithmetic"]:
        raise RuntimeError("bulk theorem boundary is missing")

    limitations = " ".join(rank_two["limitations"]).lower()
    required = (
        "fixed positive noise",
        "pointwise interval",
        "exact-real",
        "binary64",
        "row norm",
        "structural operator",
        "arithmetic trace",
        "prime-power",
        "zero-noise",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    multilevel = load(ROOT / "results" / "multilevel_perron_grushin.json")
    rank_two = load(
        ROOT / "results" / "validated_rank_two_peripheral_complement.json"
    )
    verify_multilevel(multilevel)
    verify_rank_two(rank_two)
    verify_dependency_links(multilevel, rank_two, dependency)
    if summary["status"] != rank_two["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "validated-rank-two-peripheral-complement.pdf",
        ROOT / "figures" / "validated_rank_two_peripheral_complement.pdf",
        ROOT / "figures" / "validated_rank_two_peripheral_complement.png",
        ROOT / "results" / "multilevel_perron_grushin.json",
        ROOT / "results" / "validated_rank_two_peripheral_complement.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    factors = rank_two["stored_perron_factor_validation"]["levels"]
    ratios = rank_two["stored_rank_two_haar_law"]["actual_spectral_ratios"]
    family = rank_two["uniform_perron_and_rank_two_families"]
    payload = {
        "status": (
            "all_archived_hashes_perron_rank_two_haar_union_contour_and_bulk_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "stored_perron_factor_dimensions": [2048, 4096, 8192],
            "maximum_perron_weighted_term_error_upper": max(
                row["weighted_term_error_upper"] for row in factors.values()
            ),
            "maximum_actual_rank_two_haar_target_deviation": max(
                row["maximum_target_deviation"] for row in ratios.values()
            ),
            "perron_continuum_resolvent_upper": rank_two[
                "perron_continuum_contour"
            ]["continuum_L2_resolvent_upper"],
            "continuum_rank_two_kernel_rank": rank_two[
                "intrinsic_rank_two_kernel"
            ]["rank"],
            "uniform_matrix_threshold_dimension": family[
                "certified_threshold_dimension"
            ],
            "uniform_union_contour_resolvent_upper": family[
                "uniform_union_contour_resolvent_upper"
            ],
            "uniform_rank_two_weighted_cutoff_upper": family[
                "uniform_rank_two_weighted_riesz_cutoff_upper"
            ],
            "uniform_rank_two_deflated_cutoff_upper": family[
                "uniform_rank_two_intrinsically_deflated_cutoff_upper"
            ],
            "bulk_trace_and_determinant_factorizations_present": True,
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
