"""Verify RH-42 hashes, Euclidean contour gates, and theorem boundaries."""

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
    grushin: dict[str, object],
    midpoint: dict[str, object],
    envelope: dict[str, object],
    uniform: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    if grushin["hashes"]["source"] != sha256_file(
        ROOT / "experiments" / "run_euclidean_grushin_certificate.py"
    ):
        raise RuntimeError("Euclidean Grushin source hash is stale")
    if grushin["hashes"]["snapshot"] != external[
        "rh36_factor_snapshot"
    ]["sha256"]:
        raise RuntimeError("Euclidean Grushin snapshot hash is stale")
    if grushin["hashes"]["rh41_coarse_source"] != external[
        "rh41_coarse_source"
    ]["sha256"]:
        raise RuntimeError("RH-41 Grushin source hash is stale")

    midpoint_links = {
        "snapshot": "rh36_factor_snapshot",
        "rh41_midpoint_bridge_source": "rh41_midpoint_bridge_source",
    }
    for certificate_name, manifest_name in midpoint_links.items():
        if midpoint["dependencies"][certificate_name] != external[
            manifest_name
        ]:
            raise RuntimeError(
                f"midpoint dependency mismatch: {certificate_name}"
            )

    if envelope["source_sha256"] != sha256_file(
        ROOT / "experiments" / "build_hilbert_envelope_certificate.py"
    ):
        raise RuntimeError("Hilbert-envelope source hash is stale")

    local_uniform_links = {
        "euclidean_grushin_certificate": (
            ROOT
            / "results"
            / "euclidean_grushin_contour_certificate.json"
        ),
        "euclidean_midpoint_bridge": (
            ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json"
        ),
        "hilbert_envelope_certificate": (
            ROOT / "results" / "hilbert_schmidt_envelope_certificate.json"
        ),
    }
    for name, path in local_uniform_links.items():
        record = uniform["dependencies"][name]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"uniform local dependency mismatch: {name}")
        if REPOSITORY / record["path"] != path:
            raise RuntimeError(f"uniform local dependency path mismatch: {name}")

    for name in (
        "rh39_cutoff_certificate",
        "rh40_weighted_riesz_manuscript",
        "rh41_continuum_certificate",
    ):
        if uniform["dependencies"][name] != external[name]:
            raise RuntimeError(f"uniform external dependency mismatch: {name}")


def verify_grushin(grushin: dict[str, object]) -> None:
    expected = "rigorous_exact_stored_euclidean_parity_circle_count_one"
    if grushin["status"] != expected:
        raise RuntimeError("Euclidean Grushin status is not closed")
    if grushin["dimension"] != 4096 or grushin["border_scale"] != 16.0:
        raise RuntimeError("unexpected Euclidean Grushin geometry")
    if not math.isfinite(grushin["residual_two_upper"]):
        raise RuntimeError("non-finite Euclidean residual")
    if grushin["residual_two_upper"] >= 2.0e-10:
        raise RuntimeError("Euclidean inverse residual gate failed")
    ledger = grushin["contour_ledger"]
    if not ledger["bordered_disk_invertible"] or not ledger[
        "rouche_count_one"
    ]:
        raise RuntimeError("Euclidean Grushin Rouche gate failed")
    if ledger["center_transport_product_upper"] >= 1.0:
        raise RuntimeError("Euclidean center transport gate failed")
    if ledger["scalar_error_upper"] >= ledger[
        "affine_scalar_boundary_lower"
    ]:
        raise RuntimeError("Euclidean scalar Rouche inequality failed")
    if ledger["contour_resolvent_upper"] >= 85.0:
        raise RuntimeError("stored Euclidean contour-resolvent gate failed")


def verify_midpoint(midpoint: dict[str, object]) -> None:
    if midpoint["status"] != "arb_exact_stored_to_midpoint_euclidean_bridge":
        raise RuntimeError("stored-to-midpoint Euclidean status is not closed")
    if midpoint["arb_precision_bits"] < 224:
        raise RuntimeError("stored-to-midpoint Arb precision gate failed")
    if not midpoint["critical_u_bracket"]["strict_sign_change"]:
        raise RuntimeError("critical-parameter root bracket failed")
    if not midpoint["support_geometry_verified_for_all_rows"]:
        raise RuntimeError("stored support geometry is not verified")
    if midpoint["minimum_center_floor_clearance"] <= 0.0:
        raise RuntimeError("stored support floor clearance failed")
    if midpoint["spectral_norm_upper"] >= 1.1e-5:
        raise RuntimeError("stored-to-midpoint Frobenius gate failed")


def verify_envelope(envelope: dict[str, object]) -> None:
    expected = "rigorous_arb_hilbert_schmidt_derivative_envelope"
    if envelope["status"] != expected:
        raise RuntimeError("Hilbert-Schmidt envelope status is not closed")
    if envelope["arb_precision_bits"] < 160:
        raise RuntimeError("Hilbert-Schmidt Arb precision gate failed")
    for name, row in envelope["quantities"].items():
        if not row["imaginary_part_contains_zero"]:
            raise RuntimeError(f"non-real Hilbert quantity: {name}")
        if not math.isfinite(row["norm_upper"]) or row["norm_upper"] <= 0.0:
            raise RuntimeError(f"invalid Hilbert norm upper: {name}")
    if envelope["quantities"]["source_second_target_second"][
        "norm_upper"
    ] >= 1.45e10:
        raise RuntimeError("mixed fourth-derivative envelope gate failed")


def verify_uniform(uniform: dict[str, object]) -> None:
    expected = "rigorous_uniform_euclidean_adaptive_sparse_parity_contour"
    if uniform["status"] != expected:
        raise RuntimeError("uniform Euclidean status is not closed")
    gates = uniform["gate_summary"]
    if not gates["all_gates_closed"]:
        raise RuntimeError("not every Euclidean transfer gate is closed")
    for name, value in gates.items():
        if name.endswith("_product_upper") and value >= 1.0:
            raise RuntimeError(f"Euclidean product gate failed: {name}")

    continuum = uniform["continuum_L2_conclusion"]
    if continuum["inside_count"] != 1:
        raise RuntimeError("continuum L2 count is not one")
    if not continuum["eigenvalue_is_real_negative_and_simple"]:
        raise RuntimeError("continuum L2 eigenvalue conclusion failed")
    if continuum["contour_resolvent_upper"] >= 267.0:
        raise RuntimeError("continuum L2 resolvent gate failed")

    for step in uniform["dyadic_hilbert_galerkin_steps"].values():
        ledger = step["resolvent_step"]
        if not ledger["count_transfers"]:
            raise RuntimeError("a dyadic Hilbert count did not transfer")
        if ledger["schur_neumann_product_upper"] >= 1.0:
            raise RuntimeError("a dyadic Hilbert Schur gate failed")

    family = uniform["uniform_matrix_family"]
    if family["certified_threshold_dimension"] != 131072:
        raise RuntimeError("unexpected all-grid Euclidean threshold")
    if not family["applies_to_every_larger_dimension"]:
        raise RuntimeError("all-grid monotonicity conclusion is missing")
    if family["inside_count_for_full_and_adaptive_sparse_matrices"] != 1:
        raise RuntimeError("uniform full/sparse count is not one")
    if family["uniform_full_matrix_resolvent_upper"] >= 839.0:
        raise RuntimeError("uniform full-matrix resolvent gate failed")
    if family["uniform_adaptive_sparse_resolvent_upper"] >= 839.0:
        raise RuntimeError("uniform sparse-matrix resolvent gate failed")
    fixed = family["fixed_eight_sigma_family"]
    if fixed["inside_count"] != 1 or fixed["row_norm_convergence_claimed"]:
        raise RuntimeError("fixed-width theorem boundary is incorrect")
    if fixed["uniform_cutoff_defect_upper"] >= 2.0e-13:
        raise RuntimeError("fixed-width Euclidean cutoff gate failed")
    adaptive = family["adaptive_family"]
    if adaptive["inside_count"] != 1:
        raise RuntimeError("adaptive sparse count is not one")
    if not adaptive["weighted_riesz_bridge_is_second_order"]:
        raise RuntimeError("adaptive weighted-Riesz rate is missing")

    limitations = " ".join(uniform["limitations"]).lower()
    required = (
        "fixed positive noise",
        "exact-real",
        "binary64",
        "zero-noise",
        "zeta zero",
        "self-adjoint",
        "riemann-hypothesis",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    grushin = load(
        ROOT / "results" / "euclidean_grushin_contour_certificate.json"
    )
    midpoint = load(
        ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json"
    )
    envelope = load(
        ROOT / "results" / "hilbert_schmidt_envelope_certificate.json"
    )
    uniform = load(
        ROOT / "results" / "uniform_euclidean_parity_certificate.json"
    )

    verify_grushin(grushin)
    verify_midpoint(midpoint)
    verify_envelope(envelope)
    verify_uniform(uniform)
    verify_dependency_links(
        grushin, midpoint, envelope, uniform, dependency
    )
    if summary["status"] != uniform["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "uniform-euclidean-parity-contour.pdf",
        ROOT / "figures" / "uniform_euclidean_parity_contour.pdf",
        ROOT / "figures" / "uniform_euclidean_parity_contour.png",
        ROOT / "results" / "euclidean_grushin_contour_certificate.json",
        ROOT / "results" / "euclidean_stored_to_midpoint_bridge.json",
        ROOT / "results" / "hilbert_schmidt_envelope_certificate.json",
        ROOT / "results" / "uniform_euclidean_parity_certificate.json",
        ROOT / "results" / "hilbert_constants_pilot.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    family = uniform["uniform_matrix_family"]
    payload = {
        "status": (
            "all_archived_hashes_euclidean_grushin_arb_hilbert_and_sparse_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "exact_stored_circle_count": 1,
            "continuum_L2_circle_count": 1,
            "continuum_eigenvalue_real_negative_simple": True,
            "continuum_L2_resolvent_upper": uniform[
                "continuum_L2_conclusion"
            ]["contour_resolvent_upper"],
            "uniform_matrix_threshold_dimension": family[
                "certified_threshold_dimension"
            ],
            "uniform_full_matrix_resolvent_upper": family[
                "uniform_full_matrix_resolvent_upper"
            ],
            "uniform_fixed_and_adaptive_sparse_resolvent_upper": family[
                "uniform_adaptive_sparse_resolvent_upper"
            ],
            "adaptive_weighted_riesz_bridge_is_second_order": family[
                "adaptive_family"
            ]["weighted_riesz_bridge_is_second_order"],
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
