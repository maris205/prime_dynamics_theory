"""Verify RH-52 hashes, theorem boundaries, and numerical gates."""

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
        "rigorous_weak_factor_direct_residue_closure_"
        "with_sharp_detail_barrier"
    )
    if certificate["status"] != expected:
        raise RuntimeError("certificate status mismatch")
    weak = certificate["weak_finite_factor_theorem"]
    if weak["schedule"] != (
        "h=o(sigma^2), equivalently n sigma^2 -> infinity"
    ):
        raise RuntimeError("weak factor schedule mismatch")
    direct = certificate["direct_kernel_bounds"]
    if "h sigma^(-3/2)" not in direct["target_detail"]:
        raise RuntimeError("target detail scale mismatch")
    if "h sigma^(-1)" not in direct["source_detail"]:
        raise RuntimeError("source detail scale mismatch")
    closure = certificate["direct_residue_closure"]
    if closure["sharp_finite_detail_transfer_required"]:
        raise RuntimeError("sharp detail was incorrectly required")
    if closure["finite_projector_polylog_upper_required"]:
        raise RuntimeError("global projector was incorrectly required")
    if "O(1)" not in closure["fine_perron_and_parity"]:
        raise RuntimeError("fine residue closure mismatch")
    if "O(1)" not in closure["coarse_parity"]:
        raise RuntimeError("right residue closure mismatch")
    barrier = certificate["sharp_detail_barrier"]
    if "Theta(h sigma^(-3/2))" not in barrier["operator_law"]:
        raise RuntimeError("sharp barrier mismatch")
    if barrier["physical_sharp_transfer_proved_here"]:
        raise RuntimeError("sharp physical transfer was overclaimed")
    conclusion = certificate["program_conclusion"]
    if not conclusion["stage_A2_sufficient_residue_gate_closed"]:
        raise RuntimeError("sufficient A2 closure was lost")
    if conclusion["stage_A2_original_sharp_sqrt_sigma_target_closed"]:
        raise RuntimeError("original sharp A2 target was overclaimed")


def verify_numerics(certificate) -> None:
    audit = certificate["floating_five_scale_audit"]
    if audit["noise_levels"] != 5 or audit["largest_dimension"] != 40960:
        raise RuntimeError("five-scale dimensions mismatch")
    if audit["fine_resolution_target"] != 20.48:
        raise RuntimeError("resolution mismatch")
    if audit["maximum_parity_weak_condition_product"] >= 1.1:
        raise RuntimeError("weak condition gate failed")
    if audit["maximum_parity_sharp_detail_ratio"] >= 0.056:
        raise RuntimeError("sharp detail ratio gate failed")
    if audit["maximum_parity_adjacent_left_l1_error"] >= 8.3e-5:
        raise RuntimeError("left adjacent weak gate failed")
    if audit["maximum_parity_adjacent_right_linf_error"] >= 2.91e-4:
        raise RuntimeError("right adjacent weak gate failed")
    if audit[
        "maximum_parity_adjacent_projector_relative_defect"
    ] >= 1.46e-4:
        raise RuntimeError("adjacent projector gate failed")
    fits = audit["fits"]
    if not 0.52 < fits["fine_perron_residue"]["vanishing_exponent"] < 0.54:
        raise RuntimeError("fine Perron exponent mismatch")
    if not 0.54 < fits["fine_parity_residue"]["vanishing_exponent"] < 0.56:
        raise RuntimeError("fine parity exponent mismatch")
    if not 0.92 < fits["right_parity_residue"]["vanishing_exponent"] < 0.95:
        raise RuntimeError("right parity exponent mismatch")
    if audit["interval_validated"]:
        raise RuntimeError("floating audit was overclaimed")


def verify_limitations(certificate) -> None:
    text = " ".join(certificate["limitations"]).lower()
    for phrase in (
        "not proved",
        "not provide an explicit interval",
        "not a numerical realization",
        "not interval enclosures",
        "stage a1",
        "stage a3",
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
        ROOT / "results" / "factor_transfer_certificate.json"
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
        ROOT / "intrinsic-peripheral-residue-transfer.pdf",
        ROOT / "figures" / "factor_residue_transfer.pdf",
        ROOT / "figures" / "factor_residue_transfer.png",
        ROOT / "results" / "factor_transfer_certificate.json",
        ROOT / "results" / "factor_transfer_pilot.json",
        ROOT / "results" / "factor_transfer_pilot_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    payload = {
        "status": (
            "all_archived_hashes_weak_factor_residue_closure_"
            "and_sharp_barrier_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "weak_schedule": certificate["weak_finite_factor_theorem"][
                "schedule"
            ],
            "sharp_detail_required": certificate[
                "direct_residue_closure"
            ]["sharp_finite_detail_transfer_required"],
            "A2_sufficient_gate_closed": certificate[
                "program_conclusion"
            ]["stage_A2_sufficient_residue_gate_closed"],
            "A2_sharp_target_closed": certificate[
                "program_conclusion"
            ]["stage_A2_original_sharp_sqrt_sigma_target_closed"],
            "largest_dimension": certificate[
                "floating_five_scale_audit"
            ]["largest_dimension"],
            "fine_parity_residue_power": certificate[
                "floating_five_scale_audit"
            ]["fits"]["fine_parity_residue"]["vanishing_exponent"],
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
