"""Verify RH-50 hashes, theorem boundaries, and numerical gates."""

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
            raise RuntimeError(
                f"publication artifact mismatch: {relative}"
            )


def verify_theory(certificate) -> None:
    expected = (
        "rigorous_two_pole_hardy_stein_reduction_with_"
        "global_contraction_no_go_and_directional_energy_gate"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    decomposition = certificate["two_pole_decomposition"]
    if not decomposition["bulk_spectral_radius_below_contour_required"]:
        raise RuntimeError("Hardy spectral-radius condition was lost")
    if "P_+/(z-lambda_+)" not in decomposition["resolvent"]:
        raise RuntimeError("two-pole Laurent identity mismatch")
    hardy = certificate["hardy_energy_theorem"]
    if hardy["condition"] != "rho(N)<r<inf_(z in Gamma)|z|":
        raise RuntimeError("Hardy window mismatch")
    if "sqrt(d_Gamma^2-r^2)" not in hardy["upper"]:
        raise RuntimeError("Hardy Cauchy factor mismatch")
    stein = certificate["stein_certificate"]
    if stein["global_inverse_or_global_power_contraction_required"]:
        raise RuntimeError("global inverse was incorrectly required")
    if "H-r^(-2)N H N^*" not in stein["validated_supersolution"]:
        raise RuntimeError("Stein supersolution mismatch")
    derivative = certificate["sharp_spike_derivative"]
    if derivative["law"] != (
        "||pi_sigma'||_2+||g_sigma'||_2=Theta(sigma^(-1))"
    ):
        raise RuntimeError("sharp derivative law mismatch")
    coupling = certificate["outgoing_hilbert_schmidt_scale"]
    if coupling["law"] != (
        "c h sigma^(-3/2)<=||B||_S2<=C h sigma^(-3/2)"
    ):
        raise RuntimeError("outgoing coupling scale mismatch")
    residue = certificate["fine_side_residue_suppression"]
    if residue[
        "dyadically_uniform_intrinsic_finite_factor_transfer_proved_here"
    ]:
        raise RuntimeError("finite factor transfer was overclaimed")
    if residue["conditional_normalized_residue_action"] != (
        "O(sigma^(1/2))"
    ):
        raise RuntimeError("conditional residue scale mismatch")
    no_go = certificate["global_contraction_no_go"]
    if no_go["directional_gramian_route_ruled_out"]:
        raise RuntimeError("directional Gramian route was incorrectly lost")
    if "-> 1" not in no_go["small_noise_consequence"]:
        raise RuntimeError("fixed-step no-go limit mismatch")
    closure = certificate["conditional_hilbert_schmidt_closure"]
    if closure["premises_proved_for_full_small_noise_family_here"]:
        raise RuntimeError("conditional closure was overclaimed")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5 or audit["largest_dimension"] != 40960:
        raise RuntimeError("five-scale audit dimensions mismatch")
    if audit["maximum_power"] != 64 or audit["probe_count"] != 8:
        raise RuntimeError("power/probe ledger mismatch")
    if audit["hardy_radius"] != 0.85:
        raise RuntimeError("primary Hardy radius mismatch")
    fits = audit["fits"]
    if fits["left_energy_r085"]["growth_exponent"] != 0.0:
        raise RuntimeError("left Hardy plateau gate failed")
    if fits["right_energy_r085"]["growth_exponent"] >= 0.09:
        raise RuntimeError("right Hardy growth gate failed")
    if fits["maximum_bulk_product"]["growth_exponent"] != 0.0:
        raise RuntimeError("bulk-product plateau gate failed")
    rows = audit["rows"]
    if max(row["left_hardy_energy_r085"] for row in rows) >= 1.7:
        raise RuntimeError("left Hardy level gate failed")
    if max(row["right_hardy_energy_r085"] for row in rows) >= 2.4:
        raise RuntimeError("right Hardy level gate failed")
    for row in rows:
        bulk = row["fine_bulk_radius_candidate"]
        if abs(row["left_tail_decay_base"] - bulk) >= 0.007:
            raise RuntimeError("left tail/base gate failed")
        if abs(row["right_tail_decay_base"] - bulk) >= 0.008:
            raise RuntimeError("right tail/base gate failed")
        if row["left_power_at_maximum_horizon"] >= 4.0e-9:
            raise RuntimeError("left horizon gate failed")
        if row["right_power_at_maximum_horizon"] >= 1.5e-8:
            raise RuntimeError("right horizon gate failed")
    residue = audit["residue_fits"]
    if not 0.50 < residue["left_perron"]["fit"][
        "vanishing_exponent"
    ] < 0.56:
        raise RuntimeError("left Perron residue exponent mismatch")
    if not 0.52 < residue["left_parity"]["fit"][
        "vanishing_exponent"
    ] < 0.58:
        raise RuntimeError("left parity residue exponent mismatch")
    if not residue["right_perron"]["numerically_zero"]:
        raise RuntimeError("right Perron residue lost exact-zero ledger")
    if residue["right_parity"]["fit"]["vanishing_exponent"] <= 0.9:
        raise RuntimeError("right parity residue gate failed")
    if audit["hardy_tail_validated"]:
        raise RuntimeError("truncated Hardy tail was overclaimed")
    if audit["hutchinson_values_are_validated_uppers"]:
        raise RuntimeError("Hutchinson estimate was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "uniform small-noise hardy-energy premise is not proved",
        "time 64",
        "not validated norm uppers",
        "finite matrix's own left factors",
        "coarse parity projector",
        "arithmetic trace formula",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        if phrase not in text:
            raise RuntimeError(
                f"missing theorem-boundary phrase: {phrase}"
            )


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    certificate = load(
        ROOT / "results" / "two_pole_hardy_certificate.json"
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
        ROOT / "two-pole-hilbert-schmidt-hardy-energies.pdf",
        ROOT / "figures" / "two_pole_hardy_energy.pdf",
        ROOT / "figures" / "two_pole_hardy_energy.png",
        ROOT / "results" / "two_pole_hardy_certificate.json",
        ROOT / "results" / "two_pole_hardy_pilot.json",
        ROOT / "results" / "two_pole_hardy_pilot_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_two_pole_hardy_stein_no_go_"
            "and_floating_boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "hardy_condition": certificate["hardy_energy_theorem"][
                "condition"
            ],
            "stein_needs_global_inverse": certificate[
                "stein_certificate"
            ]["global_inverse_or_global_power_contraction_required"],
            "sharp_derivative": certificate["sharp_spike_derivative"][
                "law"
            ],
            "finite_factor_transfer_proved": certificate[
                "fine_side_residue_suppression"
            ][
                "dyadically_uniform_intrinsic_finite_factor_transfer_proved_here"
            ],
            "fixed_step_limit": certificate[
                "global_contraction_no_go"
            ]["small_noise_consequence"],
            "left_hardy_growth_exponent": certificate[
                "floating_five_scale_audit"
            ]["fits"]["left_energy_r085"]["growth_exponent"],
            "right_hardy_growth_exponent": certificate[
                "floating_five_scale_audit"
            ]["fits"]["right_energy_r085"]["growth_exponent"],
            "largest_dimension": certificate[
                "floating_five_scale_audit"
            ]["largest_dimension"],
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
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
