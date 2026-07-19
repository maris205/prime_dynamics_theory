"""Verify RH-43 hashes, weighted-kernel gates, and theorem boundaries."""

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
    weighted: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    if multilevel["source_sha256"] != sha256_file(
        ROOT / "experiments" / "run_multilevel_euclidean_grushin.py"
    ):
        raise RuntimeError("multilevel Grushin source hash is stale")

    multilevel_links = {
        "rh36_snapshot": "rh36_factor_snapshot",
        "rh37_snapshot": "rh37_factor_snapshot",
        "rh41_grushin_source": "rh41_grushin_source",
        "rh42_euclidean_grushin_source": (
            "rh42_euclidean_grushin_source"
        ),
    }
    for certificate_name, manifest_name in multilevel_links.items():
        if multilevel["dependencies"][certificate_name] != external[
            manifest_name
        ]:
            raise RuntimeError(
                f"multilevel dependency mismatch: {certificate_name}"
            )

    local_record = weighted["dependencies"][
        "multilevel_grushin_certificate"
    ]
    local_path = ROOT / "results" / "multilevel_euclidean_grushin.json"
    if REPOSITORY / local_record["path"] != local_path:
        raise RuntimeError("weighted local dependency path mismatch")
    if local_record["sha256"] != sha256_file(local_path):
        raise RuntimeError("weighted local dependency hash mismatch")

    for name in (
        "rh36_factor_snapshot",
        "rh37_factor_snapshot",
        "rh39_cutoff_certificate",
        "rh40_projector_builder",
        "rh40_weighted_riesz_certificate",
        "rh40_weighted_riesz_manuscript",
        "rh42_uniform_euclidean_certificate",
        "rh42_hilbert_envelope",
        "rh42_hilbert_source",
    ):
        if weighted["dependencies"][name] != external[name]:
            raise RuntimeError(f"weighted dependency mismatch: {name}")


def verify_multilevel(multilevel: dict[str, object]) -> None:
    expected = "rigorous_multilevel_exact_stored_euclidean_parity_factors"
    if multilevel["status"] != expected:
        raise RuntimeError("multilevel stored-factor status is not closed")
    if multilevel["evidence_level"] != (
        "componentwise_outward_binary64_bordered_inverse_certificates"
    ):
        raise RuntimeError("unexpected multilevel evidence level")
    if set(multilevel["levels"]) != {"2048", "4096", "8192"}:
        raise RuntimeError("unexpected multilevel dimensions")

    expected_snapshot = {
        "2048": multilevel["dependencies"]["rh36_snapshot"]["sha256"],
        "4096": multilevel["dependencies"]["rh36_snapshot"]["sha256"],
        "8192": multilevel["dependencies"]["rh37_snapshot"]["sha256"],
    }
    for name, row in multilevel["levels"].items():
        if row["dimension"] != int(name):
            raise RuntimeError(f"dimension label mismatch: {name}")
        if row["status"] != (
            "rigorous_exact_stored_euclidean_parity_circle_count_one"
        ):
            raise RuntimeError(f"stored circle is not closed: {name}")
        if row["border_scale"] != 16.0 or row["radius"] != 0.05:
            raise RuntimeError(f"unexpected Grushin geometry: {name}")
        if row["hashes"]["snapshot"] != expected_snapshot[name]:
            raise RuntimeError(f"stored snapshot mismatch: {name}")
        if not math.isfinite(row["residual_two_upper"]):
            raise RuntimeError(f"non-finite inverse residual: {name}")
        if row["residual_two_upper"] >= 4.0e-10:
            raise RuntimeError(f"inverse residual gate failed: {name}")
        ledger = row["contour_ledger"]
        if not ledger["bordered_disk_invertible"] or not ledger[
            "rouche_count_one"
        ]:
            raise RuntimeError(f"Grushin Rouche gate failed: {name}")
        if ledger["center_transport_product_upper"] >= 1.0:
            raise RuntimeError(f"center transport gate failed: {name}")
        if ledger["scalar_error_upper"] >= ledger[
            "affine_scalar_boundary_lower"
        ]:
            raise RuntimeError(f"scalar Rouche inequality failed: {name}")
        if ledger["contour_resolvent_upper"] >= 85.0:
            raise RuntimeError(f"stored contour resolvent gate failed: {name}")
        if row["left_right_gram_lower"] <= 0.0:
            raise RuntimeError(f"left-right Gram gate failed: {name}")


def verify_weighted(weighted: dict[str, object]) -> None:
    expected = (
        "rigorous_intrinsic_continuum_parity_kernel_and_adaptive_deflation"
    )
    if weighted["status"] != expected:
        raise RuntimeError("weighted parity-kernel status is not closed")

    factors = weighted["stored_factor_validation"]
    if not factors["all_three_levels_are_actual_spectral_factors"]:
        raise RuntimeError("not every stored factor is spectral")
    if set(factors["levels"]) != {"2048", "4096", "8192"}:
        raise RuntimeError("unexpected corrected factor dimensions")
    for name, row in factors["levels"].items():
        if not row["admissible"]:
            raise RuntimeError(f"factor correction is not admissible: {name}")
        if row["correction_neumann_product_upper"] >= 4.0e-10:
            raise RuntimeError(f"factor correction gate failed: {name}")
        if row["weighted_term_error_upper"] >= 1.5e-9:
            raise RuntimeError(f"weighted factor error gate failed: {name}")

    haar = weighted["stored_parity_haar_law"]
    if haar["status"] != (
        "rigorous_actual_stored_parity_quarter_half_mechanism"
    ):
        raise RuntimeError("actual spectral Haar status is not closed")
    if haar["arb_precision_bits"] < 224:
        raise RuntimeError("spectral Haar Arb precision gate failed")
    if not haar["all_ratio_targets_within_one_thousandth"]:
        raise RuntimeError("spectral quarter--half gate failed")
    for name, row in haar["actual_spectral_ratios"].items():
        if not 0.0 < row["lower"] <= row["upper"]:
            raise RuntimeError(f"invalid spectral Haar interval: {name}")
        if row["maximum_target_deviation"] >= 1.0e-3:
            raise RuntimeError(f"spectral Haar target gate failed: {name}")

    complement = weighted["continuum_complement_schur"]
    step = complement["resolvent_step"]
    if complement["coarse_dimension"] != 65536:
        raise RuntimeError("unexpected complement dimension")
    if complement["continuum_inside_count"] != 1 or not step[
        "count_transfers"
    ]:
        raise RuntimeError("continuum complement count did not transfer")
    if step["schur_neumann_product_upper"] >= 8.0e-4:
        raise RuntimeError("continuum complement Schur gate failed")
    if complement["improved_continuum_L2_resolvent_upper"] >= 113.0:
        raise RuntimeError("improved continuum resolvent gate failed")

    kernel = weighted["intrinsic_continuum_kernel"]
    envelope = kernel["envelope"]
    if kernel["rank"] != 1 or not kernel["real_smooth_kernel"]:
        raise RuntimeError("intrinsic rank-one smooth-kernel gate failed")
    for name, value in envelope.items():
        if name == "midpoint_dimension":
            continue
        if not math.isfinite(value) or value <= 0.0:
            raise RuntimeError(f"invalid intrinsic kernel envelope: {name}")
    if envelope["midpoint_dimension"] != 65536:
        raise RuntimeError("unexpected intrinsic-kernel midpoint dimension")
    if envelope["midpoint_to_cell_average_upper"] >= 1.8e-5:
        raise RuntimeError("intrinsic-kernel midpoint gate failed")
    if kernel["continuum_operator_distance_from_center_upper"] >= 1.72:
        raise RuntimeError("continuum operator construction ball failed")
    if kernel["continuum_kernel_L2_distance_from_center_upper"] >= 2.43:
        raise RuntimeError("continuum kernel construction ball failed")

    family = weighted["improved_uniform_matrix_family"]
    if family["certified_threshold_dimension"] != 65536:
        raise RuntimeError("unexpected all-grid threshold")
    if not family["applies_to_every_larger_dimension"]:
        raise RuntimeError("all-grid monotonicity conclusion is missing")
    for name in ("midpoint_transfer", "full_transfer", "sparse_transfer"):
        if not family[name]["admissible"]:
            raise RuntimeError(f"family transfer is not admissible: {name}")
        if family[name]["neumann_product_upper"] >= 1.0:
            raise RuntimeError(f"family Neumann gate failed: {name}")
    if family["uniform_full_resolvent_upper"] >= 268.0:
        raise RuntimeError("uniform full-matrix resolvent gate failed")
    if family[
        "uniform_fixed_and_adaptive_sparse_resolvent_upper"
    ] >= 268.0:
        raise RuntimeError("uniform sparse-matrix resolvent gate failed")
    if family["uniform_weighted_riesz_cutoff_upper"] >= 8.0e-10:
        raise RuntimeError("weighted-Riesz cutoff gate failed")
    if family["uniform_intrinsically_deflated_cutoff_upper"] >= 8.0e-10:
        raise RuntimeError("intrinsic-deflation cutoff gate failed")
    if family["fixed_eight_sigma_convergence_to_full_claimed"]:
        raise RuntimeError("fixed-width theorem boundary is incorrect")

    deflation = weighted["intrinsic_deflation"]
    if not deflation["parity_eigenvalue_is_replaced_by_zero"]:
        raise RuntimeError("parity deflation conclusion is missing")
    if not deflation["remaining_spectrum_is_unchanged_away_from_zero"]:
        raise RuntimeError("remaining-spectrum conclusion is missing")

    rh40 = weighted["rh40_condition_status"]
    for name in (
        "simple_isolated_continuum_parity_premise_closed",
        "stored_factor_spectral_status_closed_at_2048_4096_8192",
        "uniform_euclidean_cutoff_premise_closed",
    ):
        if not rh40[name]:
            raise RuntimeError(f"RH-40 premise is not closed: {name}")

    limitations = " ".join(weighted["limitations"]).lower()
    required = (
        "fixed positive noise",
        "pointwise interval",
        "exact-real",
        "binary64",
        "perron",
        "rank-two",
        "row norm",
        "zero-noise",
        "arithmetic trace",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "riemann-hypothesis",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    multilevel = load(
        ROOT / "results" / "multilevel_euclidean_grushin.json"
    )
    weighted = load(
        ROOT / "results" / "validated_weighted_parity_kernel.json"
    )
    verify_multilevel(multilevel)
    verify_weighted(weighted)
    verify_dependency_links(multilevel, weighted, dependency)
    if summary["status"] != weighted["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "validated-weighted-riesz-parity-kernel.pdf",
        ROOT / "figures" / "validated_weighted_parity_kernel.pdf",
        ROOT / "figures" / "validated_weighted_parity_kernel.png",
        ROOT / "results" / "multilevel_euclidean_grushin.json",
        ROOT / "results" / "validated_weighted_parity_kernel.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    factors = weighted["stored_factor_validation"]["levels"]
    ratios = weighted["stored_parity_haar_law"]["actual_spectral_ratios"]
    complement = weighted["continuum_complement_schur"]
    family = weighted["improved_uniform_matrix_family"]
    payload = {
        "status": (
            "all_archived_hashes_multilevel_spectral_haar_kernel_and_deflation_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "stored_spectral_factor_dimensions": [2048, 4096, 8192],
            "maximum_stored_weighted_term_error_upper": max(
                row["weighted_term_error_upper"] for row in factors.values()
            ),
            "maximum_actual_haar_target_deviation": max(
                row["maximum_target_deviation"] for row in ratios.values()
            ),
            "continuum_rank": weighted["intrinsic_continuum_kernel"][
                "rank"
            ],
            "continuum_kernel_is_real_and_smooth": weighted[
                "intrinsic_continuum_kernel"
            ]["real_smooth_kernel"],
            "continuum_L2_resolvent_upper": complement[
                "improved_continuum_L2_resolvent_upper"
            ],
            "uniform_matrix_threshold_dimension": family[
                "certified_threshold_dimension"
            ],
            "uniform_full_matrix_resolvent_upper": family[
                "uniform_full_resolvent_upper"
            ],
            "uniform_fixed_and_adaptive_sparse_resolvent_upper": family[
                "uniform_fixed_and_adaptive_sparse_resolvent_upper"
            ],
            "uniform_weighted_riesz_cutoff_upper": family[
                "uniform_weighted_riesz_cutoff_upper"
            ],
            "uniform_intrinsically_deflated_cutoff_upper": family[
                "uniform_intrinsically_deflated_cutoff_upper"
            ],
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
