"""Verify RH-109 hashes, exterior certificates, barrier, and claim boundary."""

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


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/exterior_fourth_support_audit.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]:
            raise RuntimeError(f"external hash mismatch: {path}")

    values = audit["audit_summary"]
    if values["scale_count"] != 5 or values["channel_count"] != 10 or values["update_count"] != 360:
        raise RuntimeError("exterior support audit count changed")
    if values["fine_update_count"] != 234:
        raise RuntimeError("fine exterior support count changed")
    for key in (
        "spectral_certificate_implication_violation_count",
        "trace_certificate_implication_violation_count",
        "spectral_trace_certificate_order_failure_count",
        "volume_ordering_violation_count",
        "selector_equivalence_failure_count",
        "observed_cross_error_bound_failure_count",
    ):
        if values[key] != 0:
            raise RuntimeError(f"audit invariant failed: {key}")
    threshold = audit["threshold_summary"]
    if not threshold["1e-08"]["fine_spectral_certificate_green"]:
        raise RuntimeError("fine 1e-8 spectral exterior gate changed")
    if threshold["1e-06"]["fine_spectral_certificate_green"]:
        raise RuntimeError("fine 1e-6 spectral exterior boundary changed")
    if threshold["1e-04"]["fine_spectral_certificate_green"]:
        raise RuntimeError("fine 1e-4 spectral exterior boundary changed")
    barrier = audit["barrier"]
    if not barrier["all_trace_clocks_constant"] or not barrier["all_diagonal_blocks_constant"]:
        raise RuntimeError("scalar-volume barrier invariants changed")
    if not barrier["all_snapshots_psd"]:
        raise RuntimeError("scalar-volume barrier lost positivity")
    if barrier["maximum_volume_formula_error"] >= 1e-13 or barrier["maximum_endpoint_ratio_error"] >= 1e-13:
        raise RuntimeError("scalar-volume barrier formula changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem ledger is incomplete")
    for key in (
        "all_level_physical_exterior_lower_bound_proved",
        "all_level_loss_factor_control_proved",
        "uniform_fine_support_separation_proved",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "zero_identification",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "finite-memory spectral exterior certificate",
        "trace exterior certificate",
        "sharp scalar-volume interval",
        "source-seeded scalar-volume barrier",
        "all-level physical exterior lower bound",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript phrase: {phrase}")

    archived = [
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "UPDATED_ROADMAP.md",
        ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
        ROOT / "main.pdf",
        ROOT / "exterior-power-fourth-cross-support.pdf",
        ROOT / "figures" / "exterior_power_fourth_cross_support.pdf",
        ROOT / "figures" / "exterior_power_fourth_cross_support.png",
        ROOT / "results" / "exterior_fourth_support_audit.json",
        ROOT / "results" / "exterior_fourth_support_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {
        "status": "all_archived_hashes_exterior_certificates_barrier_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
