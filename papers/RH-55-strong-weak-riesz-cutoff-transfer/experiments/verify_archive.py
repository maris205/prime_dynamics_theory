"""Verify RH-55 hashes, theorem boundaries, and numerical gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_hashes(summary, dependency) -> None:
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
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


def verify_theory(certificate) -> None:
    expected = (
        "rigorous_adaptive_strong_weak_riesz_cutoff_transfer_with_"
        "midpoint_ulam_contour_inheritance"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    midpoint = certificate["midpoint_ulam_theorem"]
    if midpoint["row_l1"] != "O(h^2 sigma^-2)":
        raise RuntimeError("midpoint row scale mismatch")
    if midpoint["piecewise_bv"] != "O(h sigma^-2)":
        raise RuntimeError("midpoint strong scale mismatch")
    sandwich = certificate["sandwich_riesz_theorem"]
    if "rho M R" not in sandwich["sandwich_defect"]:
        raise RuntimeError("sandwich ledger was omitted")
    if sandwich["global_l2_contour_required"]:
        raise RuntimeError("global L2 contour was incorrectly required")
    generic = certificate["mass_only_route"]
    if generic["all_strict_mesh_schedules_threshold"] != "kappa>=7/4":
        raise RuntimeError("generic adaptive threshold mismatch")
    shape = certificate["gaussian_shape_route"]
    if shape["all_strict_mesh_schedules_threshold"] != "kappa>=5/4":
        raise RuntimeError("shape-aware adaptive threshold mismatch")
    if shape["rh39_kappa_two_conclusion"] != "o(sigma^(3/2))":
        raise RuntimeError("RH-39 adaptive conclusion mismatch")
    if generic["threshold_is_necessary"] or shape["threshold_is_necessary"]:
        raise RuntimeError("a sufficient threshold was overclaimed")
    if not certificate["fixed_window_no_go"][
        "does_not_claim_actual_riesz_divergence"
    ]:
        raise RuntimeError("fixed-window route boundary was lost")

    conclusion = certificate["program_conclusion"]
    for gate in (
        "midpoint_to_ulam_contour_inheritance_closed",
        "adaptive_sparse_full_projector_modulus_closed",
        "adaptive_sparse_full_weighted_riesz_modulus_closed",
        "rh54_factor_aware_cutoff_premise_closed",
        "stage_A3_analytic_factor_transfer_component_closed",
    ):
        if not conclusion[gate]:
            raise RuntimeError(f"proved gate not recorded: {gate}")
    for gate in (
        "production_intrinsic_riesz_interval_eigensolver_executed",
        "stage_A1_uniform_hardy_budget_closed",
        "stage_A3_production_interval_program_closed",
        "stage_A4_unconditional_identification_closed",
    ):
        if conclusion[gate]:
            raise RuntimeError(f"theorem boundary overclaimed: {gate}")


def verify_numerics(certificate, pilot) -> None:
    audit = certificate["binary64_audit"]
    if audit["midpoint_ulam_levels"] != 4:
        raise RuntimeError("four-level midpoint audit missing")
    if audit["factor_rows"] != 15:
        raise RuntimeError("inherited factor rows missing")
    if audit["interval_validated"]:
        raise RuntimeError("binary64 audit was misclassified")
    extrema = pilot["extrema"]
    if extrema["maximum_midpoint_row_scaled_ratio"] >= 0.43:
        raise RuntimeError("midpoint row scale regressed")
    if extrema["maximum_midpoint_bv_scaled_ratio"] >= 0.25:
        raise RuntimeError("midpoint BV scale regressed")
    if extrema["maximum_five_sigma_actual_riesz_sum"] >= 6.6e-8:
        raise RuntimeError("five-sigma Riesz diagnostic regressed")
    if extrema["maximum_five_sigma_actual_over_shape_envelope"] >= 0.0014:
        raise RuntimeError("shape-envelope diagnostic regressed")
    if not extrema["kappa_two_shape_ratio_strictly_decreases"]:
        raise RuntimeError("kappa-two schedule regression")
    if extrema["fixed_window_strong_proxy_growth"] < 9999.0:
        raise RuntimeError("fixed-window no-go clock missing")

    arb = certificate["arb_audit"]
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    if not arb["adaptive_below_sqrt_sigma_certified"]:
        raise RuntimeError("Arb adaptive schedule gate failed")
    if arb["production_intrinsic_riesz_interval_eigensolver_executed"]:
        raise RuntimeError("formula audit was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "asymptotic",
        "binary64",
        "arb",
        "not claimed necessary",
        "proof-route no-go",
        "stage a1",
        "stage a4",
        "arithmetic trace formula",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert--polya",
        "t log t",
        "riemann-hypothesis",
        "tpc twin-prime",
    ):
        if phrase not in text:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    certificate = load(ROOT / "results" / "riesz_cutoff_closure_certificate.json")
    pilot = load(ROOT / "results" / "riesz_cutoff_pilot.json")
    verify_hashes(summary, dependency)
    verify_theory(certificate)
    verify_numerics(certificate, pilot)
    verify_limitations(certificate)
    if summary["status"] != certificate["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "strong-weak-riesz-cutoff-transfer.pdf",
        ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.pdf",
        ROOT / "figures" / "strong_weak_riesz_cutoff_transfer.png",
        ROOT / "results" / "riesz_cutoff_closure_certificate.json",
        ROOT / "results" / "riesz_cutoff_pilot.json",
        ROOT / "results" / "riesz_cutoff_pilot_smoke.json",
        ROOT / "results" / "arb_riesz_cutoff_ledger.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_strong_weak_riesz_cutoff_and_boundary_"
            "gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "adaptive_riesz_cutoff_closed": certificate["program_conclusion"][
                "adaptive_sparse_full_weighted_riesz_modulus_closed"
            ],
            "rh54_cutoff_premise_closed": certificate["program_conclusion"][
                "rh54_factor_aware_cutoff_premise_closed"
            ],
            "stage_A1_closed": certificate["program_conclusion"][
                "stage_A1_uniform_hardy_budget_closed"
            ],
            "stage_A4_unconditional_closed": certificate["program_conclusion"][
                "stage_A4_unconditional_identification_closed"
            ],
            "arb_precision_bits": certificate["arb_audit"]["precision_bits"],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "file_count": len(files),
                "status": payload["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
