"""Verify RH-40 hashes, exact-stored intervals, and theorem-boundary gates."""

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


def verify_interval(
    record: dict[str, float], *, lower_key: str = "lower", upper_key: str = "upper"
) -> None:
    lower = float(record[lower_key])
    upper = float(record[upper_key])
    if not math.isfinite(lower) or not math.isfinite(upper) or lower > upper:
        raise RuntimeError(f"invalid interval: {record}")


def verify_block_ledger(certificate: dict[str, object]) -> None:
    targets = {
        "coarse_consistency": (0.25, 0.251, 2),
        "coarse_to_detail": (0.5, 0.501, 1),
        "detail_to_coarse": (0.5, 0.501, 1),
        "detail_block": (0.25, 0.251, 2),
    }
    first = certificate["exact_stored_frobenius_blocks"]["2048_to_4096"]
    second = certificate["exact_stored_frobenius_blocks"]["4096_to_8192"]
    ratios = certificate["exact_stored_frobenius_ratios"]
    renormalized = certificate["renormalized_exact_stored_frobenius"]
    for name, (_, gate, exponent) in targets.items():
        verify_interval(first[name], lower_key="frobenius_lower", upper_key="frobenius_upper")
        verify_interval(second[name], lower_key="frobenius_lower", upper_key="frobenius_upper")
        verify_interval(ratios[name])
        calculated_lower = float(second[name]["frobenius_lower"]) / float(
            first[name]["frobenius_upper"]
        )
        calculated_upper = float(second[name]["frobenius_upper"]) / float(
            first[name]["frobenius_lower"]
        )
        if ratios[name]["lower"] != calculated_lower:
            raise RuntimeError(f"ratio lower mismatch: {name}")
        if ratios[name]["upper"] != calculated_upper:
            raise RuntimeError(f"ratio upper mismatch: {name}")
        if float(ratios[name]["upper"]) >= gate:
            raise RuntimeError(f"quarter-half gate failed: {name}")
        for label, mesh, blocks in (
            ("2048_to_4096", 1.0 / 2048.0, first),
            ("4096_to_8192", 1.0 / 4096.0, second),
        ):
            archived = renormalized[label][name]
            expected_lower = float(blocks[name]["frobenius_lower"]) / mesh**exponent
            expected_upper = float(blocks[name]["frobenius_upper"]) / mesh**exponent
            if archived["lower"] != expected_lower or archived["upper"] != expected_upper:
                raise RuntimeError(f"renormalized interval mismatch: {label} {name}")


def verify_spectral_diagnostics(certificate: dict[str, object]) -> None:
    pilot = load(ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json")
    if pilot["status"] != "floating_stored_weighted_peripheral_projector_pilot":
        raise RuntimeError("unexpected pilot status")
    parity = pilot["parity_convergence"]
    if float(parity["second_to_first_increment_ratio"]) >= 0.251:
        raise RuntimeError("floating parity convergence gate failed")
    if float(parity["richardson_disagreement"]) >= 1.0e-9:
        raise RuntimeError("floating Richardson gate failed")
    exact_parity = certificate["parity_convergence"]
    if float(exact_parity["increment_ratio_upper"]) >= 0.251:
        raise RuntimeError("exact-stored parity ratio gate failed")
    if float(exact_parity["richardson_disagreement_upper"]) >= 1.0e-9:
        raise RuntimeError("exact-stored Richardson gate failed")
    if certificate["maximum_exact_stored_biorthogonality_upper"] >= 1.0e-13:
        raise RuntimeError("exact-stored biorthogonality gate failed")
    audit = certificate["floating_isolation_audit"]
    if float(audit["minimum_parity_to_observed_bulk_radial_gap"]) <= 0.31:
        raise RuntimeError("floating observed-isolation gate failed")
    if float(audit["maximum_eigen_residual"]) >= 1.0e-13:
        raise RuntimeError("floating residual gate failed")


def verify_boundary(certificate: dict[str, object]) -> None:
    statements = certificate["analytic_statements"]
    if "unconditional" not in statements["perron_status"]:
        raise RuntimeError("Perron theorem boundary was weakened or removed")
    if "conditional" not in statements["parity_status"]:
        raise RuntimeError("parity theorem boundary was weakened or removed")
    limitations = " ".join(certificate["limitations"]).lower()
    required = (
        "continuum simplicity",
        "floating residuals",
        "not the full sparse eigensolver",
        "only two dyadic refinements",
        "binary64 construction",
        "no zero-noise",
    )
    for phrase in required:
        if phrase not in limitations:
            raise RuntimeError(f"missing theorem-boundary phrase: {phrase}")


def main() -> None:
    summary, dependency = verify_hashes()
    certificate = load(
        ROOT / "results" / "weighted_riesz_projector_bridge_certificate.json"
    )
    expected_status = (
        "analytic_conditional_weighted_riesz_bridge_with_exact_stored_peripheral_ledger"
    )
    if certificate["status"] != expected_status or summary["status"] != expected_status:
        raise RuntimeError("the weighted-Riesz certificate status is not closed")
    if not certificate["stored_ledger_closed"]:
        raise RuntimeError("the stored-factor ledger is not closed")
    for name, record in certificate["dependencies"].items():
        if record != dependency["external_inputs"][name]:
            raise RuntimeError(f"certificate dependency mismatch: {name}")
    if sha256_file(
        ROOT / certificate["pilot"]["path"]
    ) != certificate["pilot"]["sha256"]:
        raise RuntimeError("certificate pilot hash mismatch")

    verify_block_ledger(certificate)
    verify_spectral_diagnostics(certificate)
    verify_boundary(certificate)

    archived_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "weighted-riesz-projector-bridge.pdf",
        ROOT / "figures" / "weighted_riesz_projector_bridge.pdf",
        ROOT / "figures" / "weighted_riesz_projector_bridge.png",
        ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json",
        ROOT / "results" / "weighted_riesz_projector_bridge_certificate.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {
        str(path.relative_to(ROOT)): sha256_file(path) for path in archived_paths
    }
    payload = {
        "status": "all_archived_hashes_weighted_riesz_ledgers_and_boundary_gates_verified",
        "file_count": len(files),
        "files": files,
        "theorem_gates": {
            "analytic_resolvent_lipschitz_recorded": True,
            "analytic_simple_branch_second_order_recorded": True,
            "perron_full_kernel_unconditional": True,
            "parity_continuum_bridge_conditional": True,
            "cutoff_transfer_requires_uniform_contour_resolvent": True,
            "exact_stored_block_count": 8,
            "maximum_exact_stored_biorthogonality_upper": certificate[
                "maximum_exact_stored_biorthogonality_upper"
            ],
            "minimum_floating_observed_radial_gap": certificate[
                "floating_isolation_audit"
            ]["minimum_parity_to_observed_bulk_radial_gap"],
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
