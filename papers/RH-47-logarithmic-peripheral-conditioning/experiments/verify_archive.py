"""Verify RH-47 hashes, logarithmic laws, and theorem boundaries."""

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
    pilot: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    for name in external:
        if certificate["dependencies"][name] != external[name]:
            raise RuntimeError(f"certificate dependency mismatch: {name}")
    local = certificate["dependencies"]["local_floating_factor_pilot"]
    if local["path"] != "results/small_noise_peripheral_factor_pilot.json":
        raise RuntimeError("local pilot path mismatch")
    if local["sha256"] != sha256_file(
        ROOT / "results" / "small_noise_peripheral_factor_pilot.json"
    ):
        raise RuntimeError("local pilot hash mismatch")
    if pilot["source"] != external["rh14_operator_source"]:
        raise RuntimeError("pilot operator source mismatch")


def verify_certificate(certificate: dict[str, object]) -> None:
    if certificate["status"] != (
        "rigorous_logarithmic_peripheral_conditioning_anchored_bulk_mesh_and_intrinsic_identification_boundary"
    ):
        raise RuntimeError("certificate status is unexpected")
    endpoint = certificate["mesoscopic_endpoint_theorem"]
    if not 0.2264 < endpoint["endpoint_tail_constant"] < 0.2265:
        raise RuntimeError("endpoint tail constant gate failed")
    if not math.isclose(
        endpoint["endpoint_squared_log_coefficient"],
        endpoint["endpoint_tail_constant"] ** 2,
        rel_tol=0.0,
        abs_tol=2.0e-16,
    ):
        raise RuntimeError("endpoint log coefficient mismatch")

    conditioning = certificate["peripheral_conditioning_theorem"]
    if conditioning["regular_variation_index"] != 0.0:
        raise RuntimeError("regular-variation index mismatch")
    if conditioning["bounded_in_L2"]:
        raise RuntimeError("peripheral terms were incorrectly marked bounded")
    if conditioning["perron_projector_hilbert_schmidt"] != (
        "Theta(sqrt(log(1/sigma)))"
    ):
        raise RuntimeError("Perron logarithmic law mismatch")

    obstruction = certificate["resolvent_obstruction"]
    if obstruction["fixed_geometry_uniform_L2_resolvent"]:
        raise RuntimeError("uniform L2 resolvent obstruction was lost")
    if obstruction["forced_lower_growth"] != (
        "Omega(sqrt(log(1/sigma)))"
    ):
        raise RuntimeError("resolvent lower clock mismatch")
    if obstruction["reduced_resolvent_upper_determined"]:
        raise RuntimeError("reduced resolvent upper was overclaimed")
    if obstruction["polynomial_beta_identified"]:
        raise RuntimeError("polynomial beta was overclaimed")

    anchored = certificate["continuum_anchored_bulk"]
    if anchored["critical_power"] != 2.0:
        raise RuntimeError("anchored critical power mismatch")
    if anchored["sufficient_power_law"] != (
        "n(sigma) sigma^2 -> infinity"
    ):
        raise RuntimeError("anchored mesh law mismatch")
    boundary = certificate["intrinsic_discrete_identification_boundary"]
    if boundary["controlled_here"]:
        raise RuntimeError("intrinsic identification was overclaimed")
    if boundary["sufficient_next_bound"] != (
        "||I_n,sigma||_S2=O(n^-1 sigma^-3/2)"
    ):
        raise RuntimeError("next identification target mismatch")

    schedules = certificate["normalized_power_schedule_audit"]
    if schedules["2.0"]["square_trace_norm_converges"]:
        raise RuntimeError("critical p=2 schedule was marked convergent")
    if not schedules["2.25"]["square_trace_norm_converges"]:
        raise RuntimeError("supercritical p=2.25 schedule gate failed")


def verify_pilot(pilot: dict[str, object]) -> None:
    if pilot["status"] != (
        "floating_small_noise_peripheral_factor_conditioning_pilot"
    ):
        raise RuntimeError("factor pilot status is unexpected")
    if len(pilot["rows"]) != 9:
        raise RuntimeError("unexpected number of noise levels")
    smallest = pilot["rows"][-1]
    if smallest["sigma"] != 1.0e-4 or smallest["dimension"] != 204800:
        raise RuntimeError("smallest pilot level mismatch")
    if smallest["perron_projector_norm"] <= 1.4:
        raise RuntimeError("Perron projector growth gate failed")
    if smallest["parity_projector_norm"] <= 1.35:
        raise RuntimeError("parity projector growth gate failed")
    if smallest["perron_contour_resolvent_lower"] <= 28.0:
        raise RuntimeError("Perron resolvent lower gate failed")
    expected = pilot["analytic_endpoint_tail_constant"]
    if abs(smallest["endpoint_perron_tail_coefficient"] - expected) >= 0.02:
        raise RuntimeError("stationary endpoint coefficient gate failed")
    if abs(smallest["endpoint_parity_tail_coefficient"] - expected) >= 0.02:
        raise RuntimeError("parity endpoint coefficient gate failed")
    if pilot["rank_two_log_fit"]["slope"] <= 0.30:
        raise RuntimeError("rank-two logarithmic fit gate failed")


def verify_boundaries(certificate: dict[str, object]) -> None:
    limitations = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "from below",
        "reduced resolvent",
        "compressed continuum",
        "actual weighted riesz",
        "not proved",
        "unknown theorem constants",
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
        ROOT
        / "results"
        / "logarithmic_peripheral_conditioning_certificate.json"
    )
    pilot = load(
        ROOT / "results" / "small_noise_peripheral_factor_pilot.json"
    )
    verify_certificate(certificate)
    verify_pilot(pilot)
    verify_boundaries(certificate)
    verify_dependency_links(certificate, pilot, dependency)
    if summary["status"] != certificate["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "logarithmic-peripheral-conditioning.pdf",
        ROOT / "figures" / "logarithmic_peripheral_conditioning.pdf",
        ROOT / "figures" / "logarithmic_peripheral_conditioning.png",
        ROOT
        / "results"
        / "logarithmic_peripheral_conditioning_certificate.json",
        ROOT / "results" / "small_noise_peripheral_factor_pilot.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    endpoint = certificate["mesoscopic_endpoint_theorem"]
    smallest = pilot["rows"][-1]
    payload = {
        "status": (
            "all_archived_hashes_endpoint_log_resolvent_obstruction_anchored_mesh_and_identification_boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "endpoint_tail_constant": endpoint["endpoint_tail_constant"],
            "peripheral_regular_variation_index": certificate[
                "peripheral_conditioning_theorem"
            ]["regular_variation_index"],
            "fixed_geometry_uniform_L2_resolvent": certificate[
                "resolvent_obstruction"
            ]["fixed_geometry_uniform_L2_resolvent"],
            "forced_resolvent_lower_growth": certificate[
                "resolvent_obstruction"
            ]["forced_lower_growth"],
            "anchored_critical_power": certificate[
                "continuum_anchored_bulk"
            ]["critical_power"],
            "intrinsic_identification_controlled": certificate[
                "intrinsic_discrete_identification_boundary"
            ]["controlled_here"],
            "smallest_sigma": smallest["sigma"],
            "smallest_dimension": smallest["dimension"],
            "smallest_perron_resolvent_lower": smallest[
                "perron_contour_resolvent_lower"
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
