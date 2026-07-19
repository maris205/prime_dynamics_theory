"""Verify RH-51 hashes, theorem boundaries, and numerical gates."""

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
        "rigorous_minimal_gramian_cyclic_rank_obstruction_"
        "and_growing_horizon_block_stein_route"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    minimal = certificate["minimal_gramian"]
    if minimal["minimality"] != (
        "H>=0 and H-A H A^*>=X X^* imply H>=G"
    ):
        raise RuntimeError("minimal-Gramian statement mismatch")
    if "Ran(G)=span" not in minimal["cyclic_support"]:
        raise RuntimeError("cyclic support identity mismatch")
    rank = certificate["cyclic_rank_obstruction"]
    if "rank(H)>=" not in rank["rank_lower"]:
        raise RuntimeError("rank obstruction mismatch")
    if rank["physical_divergence_proved_analytically_here"]:
        raise RuntimeError("physical cyclic growth was overclaimed")
    floor = certificate["low_rank_plus_floor"]
    if "lambda_(k+1)(G)" not in floor["statement"]:
        raise RuntimeError("low-rank floor mismatch")
    block = certificate["block_stein"]
    if block["fixed_rank_obstruction_removed"]:
        raise RuntimeError("block theorem incorrectly removed rank obstruction")
    if block["fixed_step_global_contraction_required"]:
        raise RuntimeError("fixed-step contraction was incorrectly required")
    if not block["horizon_may_grow_with_noise_or_dimension"]:
        raise RuntimeError("growing-horizon route was lost")
    if certificate["program_conclusion"]["stage_A1_closed"]:
        raise RuntimeError("Stage A1 was overclaimed")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5 or audit["largest_dimension"] != 512:
        raise RuntimeError("five-scale dimensions mismatch")
    if audit["resolution"] != 5.12 or audit["hardy_radius"] != 0.85:
        raise RuntimeError("dense audit geometry mismatch")
    rows = audit["rows"]
    if [row["left_rank_for_99_percent_trace"] for row in rows] != [
        5,
        9,
        17,
        35,
        69,
    ]:
        raise RuntimeError("left 99-percent ranks mismatch")
    if [row["right_rank_for_99_percent_trace"] for row in rows] != [
        5,
        9,
        17,
        33,
        64,
    ]:
        raise RuntimeError("right 99-percent ranks mismatch")
    if [row["left_cyclic_numerical_rank"] for row in rows] != [
        22,
        43,
        84,
        165,
        322,
    ]:
        raise RuntimeError("cyclic ranks mismatch")
    if [row["left_selected_block_horizon"] for row in rows] != [
        4,
        8,
        16,
        24,
        32,
    ]:
        raise RuntimeError("left block horizons mismatch")
    if [row["right_selected_block_horizon"] for row in rows] != [
        4,
        8,
        16,
        24,
        32,
    ]:
        raise RuntimeError("right block horizons mismatch")
    if audit["maximum_left_block_relative_excess"] >= 5.5e-4:
        raise RuntimeError("left block upper lost sharpness")
    if audit["maximum_right_block_relative_excess"] >= 6.3e-4:
        raise RuntimeError("right block upper lost sharpness")
    if audit["identity_cone_obstructed_levels"] != 4:
        raise RuntimeError("identity witness count mismatch")
    if audit["diagonal_extraction_failed_levels"] != 5:
        raise RuntimeError("diagonal failure count mismatch")
    if audit["interval_validated"]:
        raise RuntimeError("floating audit was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "not proved here",
        "not an interval",
        "logarithmic-looking",
        "anisotropic trace budget",
        "arithmetic trace formula",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
        "twin-prime",
        "independent tpc",
    ):
        if phrase not in text:
            raise RuntimeError(
                f"missing theorem-boundary phrase: {phrase}"
            )


def main() -> None:
    summary = load(ROOT / "results" / "summary.json")
    dependency = load(ROOT / "results" / "dependency_manifest.json")
    certificate = load(
        ROOT / "results" / "structured_stein_certificate.json"
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
        ROOT / "cyclic-rank-growing-horizon-stein-certificates.pdf",
        ROOT / "figures" / "structured_stein_geometry.pdf",
        ROOT / "figures" / "structured_stein_geometry.png",
        ROOT / "results" / "structured_stein_certificate.json",
        ROOT / "results" / "structured_stein_pilot.json",
        ROOT / "results" / "structured_stein_pilot_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_minimal_gramian_cyclic_rank_"
            "and_growing_horizon_boundary_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "minimality": certificate["minimal_gramian"]["minimality"],
            "physical_cyclic_growth_proved": certificate[
                "cyclic_rank_obstruction"
            ]["physical_divergence_proved_analytically_here"],
            "fixed_rank_obstruction_removed_by_blocks": certificate[
                "block_stein"
            ]["fixed_rank_obstruction_removed"],
            "stage_A1_closed": certificate["program_conclusion"][
                "stage_A1_closed"
            ],
            "cyclic_rank_power": certificate[
                "floating_five_scale_audit"
            ]["left_cyclic_rank_power_fit"]["power"],
            "largest_dimension": certificate[
                "floating_five_scale_audit"
            ]["largest_dimension"],
            "selected_horizons": [
                row["left_selected_block_horizon"]
                for row in certificate["floating_five_scale_audit"]["rows"]
            ],
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
