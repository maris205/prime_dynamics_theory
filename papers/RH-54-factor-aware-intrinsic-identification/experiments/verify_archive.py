"""Verify RH-54 hashes, theorem boundaries, and numerical gates."""

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
        "rigorous_factor_aware_closure_criterion_with_nonnormal_"
        "conditioning_gate_and_five_scale_transfer_audit"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    normalized = certificate["normalized_coupling_theorem"]
    if "2 epsilon_B/||B||_S2" not in normalized["conclusion"]:
        raise RuntimeError("normalized coupling formula mismatch")
    riesz = certificate["riesz_conditioning_ledger"]
    if "M_Gamma Mtilde_Gamma" not in riesz["projector"]:
        raise RuntimeError("Riesz conditioning was omitted")
    growing = certificate["growing_horizon_transfer"]
    if growing["contraction_condition"] != "q_M+d_M<1":
        raise RuntimeError("growing-horizon condition mismatch")
    composition = certificate["conditional_identification_composition"]
    if "delta=alpha_B+alpha_C" not in composition["hardy_product"]:
        raise RuntimeError("Hardy exponent composition mismatch")
    if composition["all_strict_mesh_schedules_condition"] != "delta<=1/4":
        raise RuntimeError("quarter-power threshold mismatch")
    if not composition["threshold_case"]["preserves_all_strict_schedules"]:
        raise RuntimeError("threshold case was lost")
    if composition["beyond_threshold_case"]["preserves_all_strict_schedules"]:
        raise RuntimeError("beyond-threshold case was overclaimed")
    no_go = certificate["nonnormal_no_go"]
    if no_go["operator_defect"] >= 1.0e-6 or no_go["projector_defect"] <= 1.0:
        raise RuntimeError("nonnormal no-go scaling mismatch")

    conclusion = certificate["program_conclusion"]
    for gate in (
        "normalized_coupling_gate_closed",
        "factor_aware_finite_matrix_transfer_theorem_closed",
        "growing_horizon_block_robustness_closed",
        "conditional_RH48_to_RH53_composition_closed",
    ):
        if not conclusion[gate]:
            raise RuntimeError(f"proved gate not recorded: {gate}")
    for gate in (
        "production_intrinsic_riesz_interval_enclosure_executed",
        "dyadically_uniform_riesz_conditioning_modulus_proved",
        "stage_A1_uniform_hardy_budget_closed",
        "stage_A3_fully_closed",
        "stage_A4_unconditional_identification_closed",
    ):
        if conclusion[gate]:
            raise RuntimeError(f"theorem boundary overclaimed: {gate}")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5:
        raise RuntimeError("five-scale audit missing")
    if audit["dimensions"] != [32, 64, 128, 256, 512]:
        raise RuntimeError("dimension ledger mismatch")
    if audit["horizons"] != [4, 8, 16, 24, 32]:
        raise RuntimeError("horizon ledger mismatch")
    if audit["cutoff_multiples"] != [5.0, 6.0, 8.0]:
        raise RuntimeError("cutoff stress levels mismatch")
    extrema = audit["extrema"]
    if not extrema["all_factor_bounds_dominate_actual"]:
        raise RuntimeError("factor-aware bound failed")
    if not extrema["all_transferred_blocks_contract"]:
        raise RuntimeError("block transfer failed")
    if extrema["maximum_stress_markov_spectral_defect"] >= 7.0e-8:
        raise RuntimeError("stress Markov defect regression")
    if extrema["maximum_stress_normalized_b_defect"] >= 4.2e-7:
        raise RuntimeError("normalized coupling regression")
    if extrema["maximum_stress_block_margin_ratio"] >= 3.4e-7:
        raise RuntimeError("contraction margin regression")
    if audit["interval_validated"]:
        raise RuntimeError("binary64 audit was misclassified")
    for row in audit["stress_rows"]:
        if row["left_actual_energy_squared_difference"] > row[
            "left_finite_perturbation_upper"
        ]:
            raise RuntimeError("left finite perturbation bound failed")
        if row["right_actual_energy_squared_difference"] > row[
            "right_finite_perturbation_upper"
        ]:
            raise RuntimeError("right finite perturbation bound failed")

    arb = certificate["arb_audit"]
    if arb["precision_bits"] != 256:
        raise RuntimeError("Arb precision mismatch")
    if not arb["normalization_bound_certified"]:
        raise RuntimeError("Arb normalization bound failed")
    if not arb["transferred_block_contraction_certified"]:
        raise RuntimeError("Arb block transfer failed")
    if arb["production_intrinsic_riesz_interval_executed"]:
        raise RuntimeError("abstract Arb audit was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "binary64",
        "not an interval",
        "not the n=40960",
        "stage a1",
        "stage a3",
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
    certificate = load(
        ROOT / "results" / "intrinsic_identification_closure_certificate.json"
    )
    verify_hashes(summary, dependency)
    verify_theory(certificate)
    verify_numerics(certificate)
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
        ROOT / "factor-aware-intrinsic-riesz-identification.pdf",
        ROOT / "figures" / "factor_aware_intrinsic_identification.pdf",
        ROOT / "figures" / "factor_aware_intrinsic_identification.png",
        ROOT / "results" / "intrinsic_identification_closure_certificate.json",
        ROOT / "results" / "factor_aware_transfer_pilot.json",
        ROOT / "results" / "factor_aware_transfer_pilot_smoke.json",
        ROOT / "results" / "arb_factor_transfer_audit.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_factor_transfer_closure_and_boundary_"
            "gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "factor_aware_transfer_closed": certificate["program_conclusion"][
                "factor_aware_finite_matrix_transfer_theorem_closed"
            ],
            "conditional_composition_closed": certificate["program_conclusion"][
                "conditional_RH48_to_RH53_composition_closed"
            ],
            "stage_A1_closed": certificate["program_conclusion"][
                "stage_A1_uniform_hardy_budget_closed"
            ],
            "stage_A4_unconditional_closed": certificate["program_conclusion"][
                "stage_A4_unconditional_identification_closed"
            ],
            "largest_dense_dimension": certificate[
                "floating_five_scale_audit"
            ]["dimensions"][-1],
            "arb_precision_bits": certificate["arb_audit"]["precision_bits"],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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
