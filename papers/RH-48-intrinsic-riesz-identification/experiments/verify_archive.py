"""Verify RH-48 hashes, Schur clocks, numerical fits, and theorem limits."""

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


def verify_certificate(certificate: dict[str, object]) -> None:
    if certificate["status"] != (
        "rigorous_quadratic_schur_and_dyadic_reduction_with_directional_small_noise_gate"
    ):
        raise RuntimeError("certificate status is unexpected")
    schur = certificate["exact_schur_identification"]
    if schur["global_full_resolvent_required"]:
        raise RuntimeError("global resolvent was incorrectly required")
    if "quadratic" not in schur["structural_order"]:
        raise RuntimeError("quadratic Schur order was lost")
    dyadic = certificate["dyadic_telescoping"]
    if not math.isclose(
        float(dyadic["quadratic_geometric_factor"]),
        4.0 / 3.0,
        rel_tol=0.0,
        abs_tol=1.0e-15,
    ):
        raise RuntimeError("dyadic geometric factor mismatch")
    closure = certificate["conditional_small_noise_closure"]
    if closure["preserves_every_n_sigma_squared_schedule_when"] != (
        "gamma<=1/2"
    ):
        raise RuntimeError("directional threshold mismatch")
    if closure["unconditional_for_the_folded_gaussian_family_here"]:
        raise RuntimeError("conditional gate was overclaimed")
    reduced = certificate["residue_reduced_split"]
    if reduced["full_reduced_resolvent_upper_proved_here"]:
        raise RuntimeError("full reduced resolvent was overclaimed")
    if reduced["directional_reduced_resolvent_upper_proved_here"]:
        raise RuntimeError("directional reduced resolvent was overclaimed")


def verify_pilot(
    certificate: dict[str, object], pilot: dict[str, object], replay: dict[str, object]
) -> None:
    if pilot["status"] != (
        "floating_exact_dyadic_intrinsic_identification_audit"
    ):
        raise RuntimeError("pilot status is unexpected")
    if len(pilot["rows"]) != 6:
        raise RuntimeError("unexpected number of pilot noise levels")
    if replay["fine_resolution_target"] != 81.92:
        raise RuntimeError("double-resolution replay target mismatch")
    audit = certificate["floating_exact_haar_audit"]
    if audit["adjacent_defects"] != 18:
        raise RuntimeError("adjacent defect count mismatch")
    if audit["largest_dimension"] != 204800:
        raise RuntimeError("largest dimension mismatch")
    if audit["largest_nonzeros"] != 133873007:
        raise RuntimeError("largest nonzero count mismatch")
    if not -2.001 < audit["mesh_power_minimum"] < -1.99:
        raise RuntimeError("mesh power minimum is inconsistent")
    if not -2.001 < audit["mesh_power_maximum"] < -1.99:
        raise RuntimeError("mesh power maximum is inconsistent")
    joint = audit["joint_power_fit"]
    if abs(joint["dimension_power"] + 2.0) >= 0.01:
        raise RuntimeError("joint dimension power gate failed")
    if abs(joint["sigma_power"] + 2.0) >= 0.05:
        raise RuntimeError("joint sigma power gate failed")
    if joint["maximum_log_residual"] >= 0.02:
        raise RuntimeError("joint regression residual gate failed")
    replay_audit = audit["double_resolution_replay"]
    if replay_audit["maximum_relative_difference"] >= 2.0e-4:
        raise RuntimeError("double-resolution replay gate failed")
    if audit["candidate_law_is_a_theorem"]:
        raise RuntimeError("floating candidate law was overclaimed")


def verify_dependencies(
    certificate: dict[str, object],
    pilot: dict[str, object],
    dependency: dict[str, object],
) -> None:
    external = dependency["external_inputs"]
    for name in (
        "rh43_weighted_schur_source",
        "rh46_small_noise_mesh_certificate",
        "rh47_logarithmic_conditioning_certificate",
        "rh47_logarithmic_conditioning_manuscript",
    ):
        if certificate["dependencies"][name] != external[name]:
            raise RuntimeError(f"certificate dependency mismatch: {name}")
    pilot_source = external["rh14_folded_gaussian_operator_source"]
    if pilot["source"] != pilot_source:
        raise RuntimeError("pilot operator source mismatch")
    for name, relative in (
        (
            "local_dyadic_identification_pilot",
            "results/dyadic_identification_pilot.json",
        ),
        (
            "local_double_resolution_replay",
            "results/dyadic_identification_pilot_smoke.json",
        ),
    ):
        record = certificate["dependencies"][name]
        if record["path"] != relative:
            raise RuntimeError(f"local dependency path mismatch: {name}")
        if record["sha256"] != sha256_file(ROOT / relative):
            raise RuntimeError(f"local dependency hash mismatch: {name}")


def verify_boundaries(certificate: dict[str, object]) -> None:
    limitations = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "directional gain condition",
        "no global or directional reduced l2 resolvent",
        "not promoted to an analytic theorem",
        "not an interval enclosure",
        "arithmetic trace formula",
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
        ROOT / "results" / "intrinsic_riesz_identification_certificate.json"
    )
    pilot = load(ROOT / "results" / "dyadic_identification_pilot.json")
    replay = load(
        ROOT / "results" / "dyadic_identification_pilot_smoke.json"
    )
    verify_certificate(certificate)
    verify_pilot(certificate, pilot, replay)
    verify_dependencies(certificate, pilot, dependency)
    verify_boundaries(certificate)
    if summary["status"] != certificate["status"]:
        raise RuntimeError("summary status mismatch")

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "quadratic-schur-intrinsic-riesz-identification.pdf",
        ROOT / "figures" / "intrinsic_riesz_identification.pdf",
        ROOT / "figures" / "intrinsic_riesz_identification.png",
        ROOT / "results" / "intrinsic_riesz_identification_certificate.json",
        ROOT / "results" / "dyadic_identification_pilot.json",
        ROOT / "results" / "dyadic_identification_pilot_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    audit = certificate["floating_exact_haar_audit"]
    payload = {
        "status": (
            "all_archived_hashes_quadratic_schur_dyadic_directional_threshold_and_exact_haar_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "quadratic_structural_order": certificate[
                "exact_schur_identification"
            ]["structural_order"],
            "global_full_resolvent_required": certificate[
                "exact_schur_identification"
            ]["global_full_resolvent_required"],
            "dyadic_geometric_factor": certificate["dyadic_telescoping"][
                "quadratic_geometric_factor"
            ],
            "directional_threshold": certificate[
                "conditional_small_noise_closure"
            ]["preserves_every_n_sigma_squared_schedule_when"],
            "directional_reduced_resolvent_proved": certificate[
                "residue_reduced_split"
            ]["directional_reduced_resolvent_upper_proved_here"],
            "largest_dimension": audit["largest_dimension"],
            "joint_dimension_power": audit["joint_power_fit"][
                "dimension_power"
            ],
            "joint_sigma_power": audit["joint_power_fit"]["sigma_power"],
            "double_resolution_maximum_relative_difference": audit[
                "double_resolution_replay"
            ]["maximum_relative_difference"],
            "candidate_law_is_a_theorem": audit[
                "candidate_law_is_a_theorem"
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
