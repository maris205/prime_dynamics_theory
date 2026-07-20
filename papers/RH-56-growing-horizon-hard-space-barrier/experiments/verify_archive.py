"""Verify RH-56 hashes, theorem boundaries, and numerical gates."""

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
        "rigorous_two_stage_strong_space_budget_barrier_with_"
        "directional_overlap_escape_route"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    theorem = certificate["two_stage_theorem"]
    if "(theta/r)^(2M)" not in theorem["energy_square_bound"]:
        raise RuntimeError("two-stage tail factor was omitted")
    barrier = certificate["black_box_barrier"]
    if barrier["common_rate_criterion"] != "theta <= r^8":
        raise RuntimeError("critical rate mismatch")
    if barrier["standard_entrance_power_per_direction"] != 1.0:
        raise RuntimeError("strong prefactor mismatch")
    if not barrier["does_not_claim_hardy_divergence"]:
        raise RuntimeError("route no-go boundary was lost")
    overlap = certificate["directional_overlap_theorem"]
    if overlap["spectral_radius_alone_sufficient"]:
        raise RuntimeError("overlap theorem was weakened to radius only")
    conclusion = certificate["program_conclusion"]
    if not conclusion["standard_global_strong_space_route_obstructed"]:
        raise RuntimeError("route obstruction missing")
    if not conclusion["directional_overlap_route_viable"]:
        raise RuntimeError("surviving route missing")
    for gate in (
        "stage_A1_uniform_hardy_budget_closed",
        "stage_A4_unconditional_identification_closed",
    ):
        if conclusion[gate]:
            raise RuntimeError(f"theorem boundary overclaimed: {gate}")


def verify_numerics(certificate, pilot, sector) -> None:
    audit = certificate["binary64_audit"]
    if audit["all_column_rows"] != 5:
        raise RuntimeError("five-scale all-column audit missing")
    if audit["production_rows"] != 5:
        raise RuntimeError("five-scale production audit missing")
    if audit["interval_validated"]:
        raise RuntimeError("binary64 audit was misclassified")
    extrema = pilot["extrema"]
    if extrema["common_strong_rate_threshold"] >= 0.28:
        raise RuntimeError("critical threshold regressed")
    if extrema["edge_two_side_total_power"] <= 1.25:
        raise RuntimeError("edge power gate regressed")
    if extrema["maximum_all_column_energy_over_radial_clock"] >= 1.10:
        raise RuntimeError("all-column energy clock regressed")
    if extrema["maximum_deterministic_tail_relative_excess"] >= 5.0e-4:
        raise RuntimeError("deterministic tail audit regressed")
    if sector["precision_bits"] != 512:
        raise RuntimeError("sector Arb precision mismatch")
    if sector["finite_eigenvalues_in_contour"] != 1:
        raise RuntimeError("sector contour count mismatch")
    if not sector["rate_lower_exceeds_r_to_eight_certified"]:
        raise RuntimeError("sector lower-rate gate failed")
    if float(sector["full_contour_perturbation_product_ball"].split("[")[1].split()[0]) >= 0.08:
        raise RuntimeError("sector contour perturbation margin regressed")
    if sector["production_noisy_bulk_eigensolver_executed"]:
        raise RuntimeError("noisy production eigensolver was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "conditional",
        "route no-go",
        "binary64",
        "arb",
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
    certificate = load(ROOT / "results" / "hardy_barrier_certificate.json")
    pilot = load(ROOT / "results" / "hardy_barrier_pilot.json")
    sector = load(ROOT / "results" / "arb_sector_resonance_certificate.json")
    verify_hashes(summary, dependency)
    verify_theory(certificate)
    verify_numerics(certificate, pilot, sector)
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
        ROOT / "growing-horizon-hard-space-barrier.pdf",
        ROOT / "figures" / "growing_horizon_hard_space_barrier.pdf",
        ROOT / "figures" / "growing_horizon_hard_space_barrier.png",
        ROOT / "results" / "hardy_barrier_certificate.json",
        ROOT / "results" / "hardy_barrier_pilot.json",
        ROOT / "results" / "hardy_barrier_pilot_smoke.json",
        ROOT / "results" / "arb_hardy_barrier_ledger.json",
        ROOT / "results" / "arb_sector_resonance_certificate.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": "all_archived_hashes_hardy_barrier_and_sector_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "standard_strong_route_obstructed": certificate[
                "program_conclusion"
            ]["standard_global_strong_space_route_obstructed"],
            "directional_overlap_route_viable": certificate[
                "program_conclusion"
            ]["directional_overlap_route_viable"],
            "stage_A1_closed": certificate["program_conclusion"][
                "stage_A1_uniform_hardy_budget_closed"
            ],
            "stage_A4_unconditional_closed": certificate["program_conclusion"][
                "stage_A4_unconditional_identification_closed"
            ],
            "sector_precision_bits": sector["precision_bits"],
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

