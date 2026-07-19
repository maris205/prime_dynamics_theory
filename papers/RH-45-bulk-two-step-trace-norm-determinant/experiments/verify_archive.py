"""Verify RH-45 hashes, trace-ideal gates, and theorem boundaries."""

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
    mapping = {
        "rh39_cutoff_certificate": "rh39_cutoff_certificate",
        "rh42_uniform_euclidean_certificate": (
            "rh42_uniform_euclidean_certificate"
        ),
        "rh43_weighted_schur_source": "rh43_weighted_schur_source",
        "rh44_rank_two_certificate": "rh44_rank_two_certificate",
    }
    for certificate_name, manifest_name in mapping.items():
        if certificate["dependencies"][certificate_name] != external[
            manifest_name
        ]:
            raise RuntimeError(
                f"certificate dependency mismatch: {certificate_name}"
            )
    if pilot["levels"]["2048"]["snapshot"] != external[
        "rh36_stored_2048_4096_snapshot"
    ]:
        raise RuntimeError("2048 pilot snapshot mismatch")
    if pilot["levels"]["4096"]["snapshot"] != external[
        "rh36_stored_2048_4096_snapshot"
    ]:
        raise RuntimeError("4096 pilot snapshot mismatch")
    if pilot["levels"]["8192"]["snapshot"] != external[
        "rh37_stored_8192_snapshot"
    ]:
        raise RuntimeError("8192 pilot snapshot mismatch")


def verify_certificate(certificate: dict[str, object]) -> None:
    if certificate["status"] != (
        "rigorous_full_and_adaptive_bulk_square_trace_norm_and_determinant_convergence"
    ):
        raise RuntimeError("trace-norm certificate status is not closed")
    if not certificate["continuum_bulk"]["square_is_trace_class"]:
        raise RuntimeError("continuum bulk square is not marked trace class")
    if certificate["continuum_bulk"]["hilbert_schmidt_upper"] >= 15.419:
        raise RuntimeError("continuum bulk Hilbert--Schmidt gate failed")
    expected = {str(1 << power) for power in range(16, 31)}
    if set(certificate["dimension_ledgers"]) != expected:
        raise RuntimeError("unexpected displayed dimension ledger")
    if not all(
        row["all_contour_gates_closed"]
        for row in certificate["dimension_ledgers"].values()
    ):
        raise RuntimeError("at least one displayed contour gate is open")
    first = certificate["dimension_ledgers"]["65536"]
    last = certificate["dimension_ledgers"]["1073741824"]
    if first["full_bulk"]["bulk_hilbert_schmidt_error_upper"] >= 0.129:
        raise RuntimeError("threshold Hilbert--Schmidt gate failed")
    if first["full_bulk"]["square_trace_norm_error_upper"] >= 3.968:
        raise RuntimeError("threshold trace-norm gate failed")
    if last["full_bulk"]["bulk_hilbert_schmidt_error_upper"] >= 3.79e-6:
        raise RuntimeError("last Hilbert--Schmidt gate failed")
    if last["full_bulk"]["square_trace_norm_error_upper"] >= 1.17e-4:
        raise RuntimeError("last trace-norm gate failed")
    if last["determinant_disk_bounds"]["0.01"][
        "full_fredholm_determinant_error_upper"
    ] >= 3.69e-4:
        raise RuntimeError("last determinant disk gate failed")
    theorems = certificate["main_theorems"]
    for name in (
        "full_bulk_hilbert_schmidt_rate",
        "adaptive_bulk_hilbert_schmidt_rate",
        "full_bulk_square_trace_norm_rate",
        "adaptive_bulk_square_trace_norm_rate",
        "even_trace_coefficient_convergence",
        "fredholm_determinant_convergence",
        "symmetric_det2_identity",
    ):
        if not theorems[name]:
            raise RuntimeError(f"missing theorem field: {name}")
    if theorems["fixed_eight_sigma_continuum_convergence_claimed"]:
        raise RuntimeError("fixed-width theorem boundary is incorrect")


def verify_pilot(pilot: dict[str, object]) -> None:
    if pilot["status"] != (
        "floating_stored_adaptive_bulk_square_determinant_pilot"
    ):
        raise RuntimeError("stored determinant pilot status is unexpected")
    if pilot["evidence_level"] != (
        "binary64_sparse_lu_diagnostic_not_validated"
    ):
        raise RuntimeError("pilot evidence level is not explicit")
    if set(pilot["levels"]) != {"2048", "4096", "8192"}:
        raise RuntimeError("unexpected pilot dimensions")
    if pilot["maximum_symmetric_det2_identity_error"] >= 3.0e-16:
        raise RuntimeError("symmetric det2 floating identity gate failed")
    first = pilot["consecutive_absolute_differences"]["2048_to_4096"]
    second = pilot["consecutive_absolute_differences"]["4096_to_8192"]
    for radius in pilot["square_parameters"]:
        key = str(radius)
        if second[key] >= 0.26 * first[key]:
            raise RuntimeError(f"dyadic determinant diagnostic failed: {key}")


def verify_boundaries(certificate: dict[str, object]) -> None:
    limitations = " ".join(certificate["limitations"]).lower()
    required = (
        "fixed positive noise",
        "fixed eight-sigma",
        "zero-noise",
        "arithmetic trace",
        "prime-power",
        "zeta-zero",
        "self-adjoint",
        "hilbert-polya",
        "t log t",
        "riemann-hypothesis",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    certificate = load(
        ROOT / "results" / "bulk_trace_norm_determinant_certificate.json"
    )
    pilot = load(ROOT / "results" / "stored_bulk_square_determinants.json")
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
        ROOT / "bulk-two-step-trace-norm-determinant.pdf",
        ROOT / "figures" / "bulk_two_step_trace_norm_determinant.pdf",
        ROOT / "figures" / "bulk_two_step_trace_norm_determinant.png",
        ROOT / "results" / "bulk_trace_norm_determinant_certificate.json",
        ROOT / "results" / "stored_bulk_square_determinants.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in archived_paths
    }
    first = certificate["dimension_ledgers"]["65536"]
    last = certificate["dimension_ledgers"]["1073741824"]
    payload = {
        "status": (
            "all_archived_hashes_bulk_hilbert_schmidt_square_trace_norm_even_trace_and_determinant_gates_verified"
        ),
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "continuum_bulk_hilbert_schmidt_upper": certificate[
                "continuum_bulk"
            ]["hilbert_schmidt_upper"],
            "threshold_dimension": 65536,
            "threshold_full_bulk_hilbert_schmidt_error_upper": first[
                "full_bulk"
            ]["bulk_hilbert_schmidt_error_upper"],
            "threshold_full_square_trace_norm_error_upper": first[
                "full_bulk"
            ]["square_trace_norm_error_upper"],
            "last_dimension": 1073741824,
            "last_full_bulk_hilbert_schmidt_error_upper": last["full_bulk"]
            ["bulk_hilbert_schmidt_error_upper"],
            "last_full_square_trace_norm_error_upper": last["full_bulk"]
            ["square_trace_norm_error_upper"],
            "last_determinant_disk_1e_minus_2_error_upper": last[
                "determinant_disk_bounds"
            ]["0.01"]["full_fredholm_determinant_error_upper"],
            "stored_pilot_dimensions": [2048, 4096, 8192],
            "stored_pilot_maximum_symmetric_det2_identity_error": pilot[
                "maximum_symmetric_det2_identity_error"
            ],
            "fixed_eight_sigma_continuum_convergence_claimed": False,
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
