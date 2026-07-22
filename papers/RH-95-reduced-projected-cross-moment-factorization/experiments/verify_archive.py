"""Verify RH-95 hashes, positive gates, negative branch, and boundaries."""

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
    audit = load("results/reduced_cross_factorization_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_reduced_factorization_gates_green"]:
        raise RuntimeError("reduced-factorization audit incomplete")
    if values["update_count"] != 120 or values["tail_equivalent_update_count"] != 120:
        raise RuntimeError("tail-equivalence count changed")
    if values["maximum_endpoint_to_reference_ratio"] >= 1.01 or values["maximum_reduced_to_ambient_tail_ratio"] >= 1.0001:
        raise RuntimeError("stabilized reduced tail gate failed")
    if values["weak_cutoff_mode_count"] != 5 or values["raw_reconstruction_unstable_count"] < 8:
        raise RuntimeError("weak-mode negative branch changed")
    if values["moment_compression_unstable_count"] < 50:
        raise RuntimeError("moment-only instability disappeared")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    for key in (
        "binary64_moment_only_factorization_stable",
        "uniform_fourth_cross_mode_conditioning",
        "ambient_gram_packet_action_removed",
        "uniform_stage_A1_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in (
        "projected-cross gram identity",
        "reduced moment factorization theorem",
        "weak-mode conditioning barrier",
        "qr stabilization",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")

    archived = [
        ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md",
        ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt",
        ROOT / "main.pdf", ROOT / "reduced-projected-cross-moment-factorization.pdf",
        ROOT / "figures" / "reduced_cross_moment_factorization.pdf", ROOT / "figures" / "reduced_cross_moment_factorization.png",
        ROOT / "results" / "reduced_cross_factorization_audit.json", ROOT / "results" / "reduced_cross_factorization_smoke.json",
        ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_reduced_factorization_gates_negative_branch_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
