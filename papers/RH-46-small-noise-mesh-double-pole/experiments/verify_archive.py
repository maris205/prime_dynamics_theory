"""Verify RH-46 hashes, mesh laws, pole obstruction, and theorem boundaries."""

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
    certificate: dict[str, object],
    cloud: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    for name in (
        "rh14_square_root_summary",
        "rh15_bulk_scattering_manuscript",
        "rh15_bulk_scattering_summary",
        "rh16_endpoint_rank_summary",
        "rh42_fixed_noise_hilbert_envelope",
        "rh45_fixed_noise_trace_determinant",
    ):
        if certificate["dependencies"][name] != external[name]:
            raise RuntimeError(f"certificate dependency mismatch: {name}")
    if cloud["source"] != external["rh15_outer_resonance_cloud"]:
        raise RuntimeError("RH-15 cloud source mismatch")


def verify_certificate(certificate: dict[str, object]) -> None:
    if certificate["status"] != (
        "rigorous_markov_mesh_laws_two_step_double_pole_obstruction_and_conditional_bulk_route"
    ):
        raise RuntimeError("main theorem certificate status is unexpected")

    envelope = certificate["uniform_gaussian_envelope"]
    reference = envelope["rows"]["0.01"]
    if envelope["sigma_maximum"] != 0.03:
        raise RuntimeError("uniform sigma range is incorrect")
    if envelope["normalizer_linear_lower"] < 1.253314137315:
        raise RuntimeError("normalizer lower bound gate failed")
    if reference["kernel_scaled_constant"] > 2.124503864055:
        raise RuntimeError("kernel Hilbert--Schmidt constant gate failed")
    if reference["combined_first_scaled_constant"] > 11.373709849582:
        raise RuntimeError("first derivative constant gate failed")
    hs_constant = reference["combined_first_scaled_constant"] / math.pi
    if hs_constant > 3.620364287708:
        raise RuntimeError("Galerkin Hilbert--Schmidt constant gate failed")

    theorem = certificate["raw_markov_resolution_theorems"]
    if theorem["one_step_hilbert_schmidt_sufficient_condition"] != (
        "n(sigma)*sigma^(3/2)->infinity"
    ):
        raise RuntimeError("one-step mesh law mismatch")
    if theorem["two_step_trace_norm_sufficient_condition"] != (
        "n(sigma)*sigma^2->infinity"
    ):
        raise RuntimeError("two-step mesh law mismatch")
    if theorem["shrinking_disk_determinant_sufficient_condition"] != (
        "n(sigma)*sigma->infinity"
    ):
        raise RuntimeError("shrinking-disk mesh law mismatch")

    schedules = certificate["power_schedule_audit"]
    if schedules["1.5"]["hilbert_schmidt_converges"]:
        raise RuntimeError("critical one-step schedule was marked convergent")
    if not schedules["2.0"]["hilbert_schmidt_converges"]:
        raise RuntimeError("supercritical one-step schedule gate failed")
    if schedules["2.0"]["square_trace_norm_converges"]:
        raise RuntimeError("critical two-step schedule was marked convergent")
    if not schedules["2.25"]["square_trace_norm_converges"]:
        raise RuntimeError("supercritical two-step schedule gate failed")

    pole = certificate["two_step_small_noise_obstruction"]
    if not math.isclose(
        pole["two_step_double_pole"],
        1.6785735104283224,
        rel_tol=0.0,
        abs_tol=5.0e-15,
    ):
        raise RuntimeError("double-pole location mismatch")
    if pole["two_step_factor"] != (
        "D_0,square(w)=H(w)/(1-w/lambda)^2"
    ):
        raise RuntimeError("double-pole factor mismatch")
    if not pole["coefficientwise_small_noise_bridge"]:
        raise RuntimeError("coefficient bridge is missing")
    if pole["locally_uniform_entire_small_noise_limit"]:
        raise RuntimeError("entire small-noise obstruction was lost")
    if pole["family_locally_bounded_on_disks_R_gt_lambda"]:
        raise RuntimeError("normal-family obstruction was lost")

    conditional = certificate["conditional_bulk_extension"]
    if conditional["proved_uniformly_in_sigma"]:
        raise RuntimeError("open peripheral transport gate was overclaimed")
    if conditional["two_step_bulk_mesh_power"] != (
        "max(1/2,q)+max(3/2,r)"
    ):
        raise RuntimeError("conditional bulk mesh law mismatch")
    if conditional["matched_markov_case_q_1_2_r_3_2"] != 2.0:
        raise RuntimeError("matched Markov bulk exponent mismatch")
    moving = conditional["moving_contour_resolvent_corollary"]
    if moving["resolvent_identity_error_power_r"] != "3/2+2 beta":
        raise RuntimeError("moving-contour error exponent mismatch")
    if moving["sufficient_two_step_mesh_powers"]["0.5"] != 3.0:
        raise RuntimeError("moving-contour beta=1/2 audit failed")

    model = certificate["canonical_square_cloud_model"]
    if model["squared_zero_multiplicity"] != 2:
        raise RuntimeError("canonical squared multiplicity mismatch")
    if model["identification_with_actual_noisy_cloud"] != "floating_only":
        raise RuntimeError("cloud theorem boundary is incorrect")


def verify_pilots(
    row_pilot: dict[str, object], cloud: dict[str, object]
) -> None:
    if row_pilot["status"] != (
        "floating_exact_gaussian_row_cell_projection_pilot"
    ):
        raise RuntimeError("Gaussian row pilot status is unexpected")
    expected_constant = 1.0 / (math.sqrt(48.0) * math.pi ** 0.25)
    if not math.isclose(
        row_pilot["asymptotic_constant"],
        expected_constant,
        rel_tol=0.0,
        abs_tol=2.0e-16,
    ):
        raise RuntimeError("sharp Gaussian row constant mismatch")
    if row_pilot["finest_relative_error"] >= 1.0e-6:
        raise RuntimeError("sharp Gaussian row pilot gate failed")

    if cloud["status"] != (
        "floating_two_step_squared_resonance_cloud_scattering_pilot"
    ):
        raise RuntimeError("squared cloud pilot status is unexpected")
    if cloud["maximum_ideal_cloud_polynomial_identity_error"] >= 4.0e-15:
        raise RuntimeError("ideal squared-cloud identity gate failed")
    expected_levels = {
        "0.01",
        "0.004",
        "0.002",
        "0.001",
        "0.0005",
        "0.0002",
        "0.0001",
    }
    if set(cloud["levels"]) != expected_levels:
        raise RuntimeError("unexpected archived cloud levels")
    selected = cloud["levels"]["0.0001"]
    if selected["dimension"] != 204800:
        raise RuntimeError("selected cloud dimension mismatch")
    if selected["effective_degree"] != 7:
        raise RuntimeError("selected cloud degree mismatch")
    central = [
        row for row in selected["rows"] if abs(row["coordinate"]) <= 1.0
    ]
    central_mean = sum(
        row["observed_to_finite_error"] for row in central
    ) / len(central)
    if central_mean >= 0.037:
        raise RuntimeError("central squared-cloud diagnostic gate failed")
    if max(row["observed_to_finite_error"] for row in central) >= 0.116:
        raise RuntimeError("central squared-cloud maximum gate failed")


def verify_boundaries(certificate: dict[str, object]) -> None:
    limitations = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "markov kernel",
        "weighted-riesz",
        "not proved",
        "cell-average",
        "not a necessary",
        "floating diagnostics",
        "arithmetic trace",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    ):
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    certificate = load(
        ROOT / "results" / "small_noise_mesh_double_pole_certificate.json"
    )
    row_pilot = load(
        ROOT / "results" / "gaussian_row_projection_pilot.json"
    )
    cloud = load(ROOT / "results" / "two_step_square_cloud_pilot.json")
    verify_certificate(certificate)
    verify_pilots(row_pilot, cloud)
    verify_boundaries(certificate)
    verify_dependency_links(certificate, cloud, dependency)
    if summary["status"] != certificate["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "small-noise-mesh-double-pole.pdf",
        ROOT / "figures" / "small_noise_mesh_double_pole.pdf",
        ROOT / "figures" / "small_noise_mesh_double_pole.png",
        ROOT / "results" / "small_noise_mesh_double_pole_certificate.json",
        ROOT / "results" / "gaussian_row_projection_pilot.json",
        ROOT / "results" / "two_step_square_cloud_pilot.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    selected = cloud["levels"]["0.0001"]
    central = [
        row for row in selected["rows"] if abs(row["coordinate"]) <= 1.0
    ]
    payload = {
        "status": (
            "all_archived_hashes_mesh_double_pole_conditional_route_and_floating_scope_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "sigma_maximum": certificate["uniform_gaussian_envelope"][
                "sigma_maximum"
            ],
            "normalizer_linear_lower": certificate[
                "uniform_gaussian_envelope"
            ]["normalizer_linear_lower"],
            "one_step_mesh_law": certificate[
                "raw_markov_resolution_theorems"
            ]["one_step_hilbert_schmidt_sufficient_condition"],
            "two_step_mesh_law": certificate[
                "raw_markov_resolution_theorems"
            ]["two_step_trace_norm_sufficient_condition"],
            "double_pole": certificate["two_step_small_noise_obstruction"][
                "two_step_double_pole"
            ],
            "entire_small_noise_limit": certificate[
                "two_step_small_noise_obstruction"
            ]["locally_uniform_entire_small_noise_limit"],
            "uniform_peripheral_transport_proved": certificate[
                "conditional_bulk_extension"
            ]["proved_uniformly_in_sigma"],
            "gaussian_row_finest_relative_error": row_pilot[
                "finest_relative_error"
            ],
            "selected_cloud_sigma": selected["sigma"],
            "selected_cloud_central_mean_error": sum(
                row["observed_to_finite_error"] for row in central
            )
            / len(central),
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
