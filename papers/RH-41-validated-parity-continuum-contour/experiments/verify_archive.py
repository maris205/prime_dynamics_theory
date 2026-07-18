"""Verify RH-41 hashes, contour gates, and theorem boundaries."""

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
    continuum: dict[str, object], dependency: dict[str, object]
) -> None:
    local_names = {
        "coarse_grushin_certificate",
        "stored_to_midpoint_certificate",
    }
    for name in local_names:
        record = continuum["dependencies"][name]
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"continuum dependency mismatch: {name}")

    external_names = {
        "rh27_componentwise_rounding",
        "rh36_factor_snapshot",
        "rh38_haar_manuscript",
        "rh39_cutoff_certificate",
        "rh40_weighted_riesz_manuscript",
    }
    for name in external_names:
        if continuum["dependencies"][name] != dependency[
            "external_inputs"
        ][name]:
            raise RuntimeError(f"manifest dependency mismatch: {name}")


def verify_coarse(coarse: dict[str, object]) -> None:
    if coarse["status"] != "rigorous_exact_stored_parity_circle_count_one":
        raise RuntimeError("coarse Grushin status is not closed")
    if coarse["dimension"] != 4096 or coarse["border_scale"] != 16.0:
        raise RuntimeError("unexpected coarse Grushin geometry")
    if not math.isfinite(coarse["residual_infinity_upper"]):
        raise RuntimeError("non-finite coarse residual")
    if coarse["residual_infinity_upper"] >= 1.0e-8:
        raise RuntimeError("coarse inverse residual gate failed")
    ledger = coarse["contour_ledger"]
    if not ledger["bordered_disk_invertible"] or not ledger[
        "rouche_count_one"
    ]:
        raise RuntimeError("Grushin Rouché gate failed")
    if ledger["center_transport_product_upper"] >= 1.0:
        raise RuntimeError("Grushin center transport gate failed")
    if ledger["scalar_error_upper"] >= ledger[
        "affine_scalar_boundary_lower"
    ]:
        raise RuntimeError("effective scalar Rouché inequality failed")
    if ledger["contour_resolvent_upper"] >= 43.0:
        raise RuntimeError("stored contour resolvent gate failed")
    source = ROOT / "experiments" / "run_coarse_grushin_certificate.py"
    if sha256_file(source) != coarse["hashes"]["source"]:
        raise RuntimeError("coarse source hash is stale")


def verify_midpoint(midpoint: dict[str, object]) -> None:
    expected = "arb_exact_stored_to_exact_continuum_midpoint_bridge"
    if midpoint["status"] != expected:
        raise RuntimeError("stored-to-midpoint status is not closed")
    if midpoint["arb_precision_bits"] < 224:
        raise RuntimeError("Arb precision gate failed")
    bracket = midpoint["critical_u_bracket"]
    if not bracket["strict_sign_change"] or not bracket[
        "derivative_is_globally_positive"
    ]:
        raise RuntimeError("critical-parameter root bracket failed")
    if not midpoint["support_geometry_verified_for_all_rows"]:
        raise RuntimeError("stored support geometry is not verified")
    if midpoint["minimum_center_floor_clearance"] <= 0.0:
        raise RuntimeError("stored support floor clearance failed")
    if midpoint["maximum_total_row_l1_difference_upper"] >= 8.0e-6:
        raise RuntimeError("stored-to-midpoint row gate failed")


def verify_continuum(continuum: dict[str, object]) -> None:
    expected = "rigorous_continuum_parity_count_one_with_uniform_resolvent"
    if continuum["status"] != expected:
        raise RuntimeError("continuum status is not closed")
    if not continuum["gate_summary"]["all_gates_closed"]:
        raise RuntimeError("not every continuum gate is closed")
    conclusion = continuum["continuum_conclusion"]
    if conclusion["inside_count"] != 1:
        raise RuntimeError("continuum count is not one")
    for key in (
        "eigenvalue_is_simple",
        "eigenvalue_is_real",
        "eigenvalue_is_negative",
    ):
        if not conclusion[key]:
            raise RuntimeError(f"continuum conclusion failed: {key}")
    if conclusion["contour_resolvent_upper"] >= 149.0:
        raise RuntimeError("continuum resolvent gate failed")

    products = continuum["gate_summary"]
    product_gates = {
        "stored_to_galerkin_neumann_product_upper": 0.07,
        "first_schur_product_upper": 0.012,
        "second_schur_product_upper": 0.003,
        "continuum_neumann_product_upper": 0.66,
    }
    for name, upper in product_gates.items():
        if products[name] >= upper:
            raise RuntimeError(f"continuum product gate failed: {name}")

    midpoint_family = continuum["continuum_to_exact_midpoint_family"]
    if midpoint_family["first_dimension_with_uniform_bound"] != 32768:
        raise RuntimeError("unexpected midpoint-family threshold")
    if midpoint_family["inside_count_for_every_larger_dimension"] != 1:
        raise RuntimeError("midpoint-family count did not transfer")
    if midpoint_family["neumann_transfer_at_threshold"][
        "neumann_product_upper"
    ] >= 1.0:
        raise RuntimeError("midpoint-family Neumann gate failed")

    consequence = continuum["weighted_riesz_consequence"]
    if not consequence["rh40_full_kernel_parity_hypothesis_closed"]:
        raise RuntimeError("RH-40 parity premise was not closed")
    if not consequence[
        "uniform_continuum_Linfinity_contour_resolvent_available"
    ]:
        raise RuntimeError("continuum L-infinity consequence missing")
    if consequence["uniform_euclidean_sparse_matrix_resolvent_claimed"]:
        raise RuntimeError("the theorem boundary overclaims Euclidean control")

    limitations = " ".join(continuum["limitations"]).lower()
    required = (
        "fixed positive noise",
        "l-infinity",
        "no dimension-uniform euclidean",
        "no closed-form eigenvalue",
        "zero-noise",
        "hilbert-polya",
        "riemann-hypothesis",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    coarse = load(
        ROOT / "results" / "coarse_grushin_contour_certificate.json"
    )
    midpoint = load(
        ROOT / "results" / "stored_to_midpoint_bridge_certificate.json"
    )
    continuum = load(
        ROOT / "results" / "validated_parity_continuum_certificate.json"
    )

    verify_coarse(coarse)
    verify_midpoint(midpoint)
    verify_continuum(continuum)
    verify_dependency_links(continuum, dependency)
    if summary["status"] != continuum["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "validated-parity-continuum-contour.pdf",
        ROOT / "figures" / "validated_parity_continuum_contour.pdf",
        ROOT / "figures" / "validated_parity_continuum_contour.png",
        ROOT / "results" / "coarse_grushin_contour_certificate.json",
        ROOT / "results" / "stored_to_midpoint_bridge_certificate.json",
        ROOT / "results" / "validated_parity_continuum_certificate.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_grushin_arb_galerkin_and_boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "exact_stored_circle_count": 1,
            "continuum_circle_count": 1,
            "continuum_eigenvalue_real_negative_simple": True,
            "continuum_Linfinity_resolvent_upper": continuum[
                "continuum_conclusion"
            ]["contour_resolvent_upper"],
            "exact_midpoint_uniform_from_dimension": continuum[
                "continuum_to_exact_midpoint_family"
            ]["first_dimension_with_uniform_bound"],
            "uniform_euclidean_sparse_matrix_resolvent_claimed": False,
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
