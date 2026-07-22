"""Verify RH-73 hashes, validation gates, and claim boundaries."""

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


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/peripheral_validation_audit.json")
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
            raise RuntimeError(f"external input hash mismatch: {path}")
    if len(audit["rows"]) != 5 or not audit["all_executed_channels_green"]:
        raise RuntimeError("five-scale peripheral audit is incomplete")
    for row in audit["rows"]:
        if len(row["channels"]) != 2 or not row["all_channels_green"]:
            raise RuntimeError("fine/coarse channel gate failed")
        for channel in row["channels"]:
            if not channel["parity_contour"]["rouche_count_one"]:
                raise RuntimeError("parity contour count failed")
            if channel["approximate_parity_gram_lower"] <= 0.99:
                raise RuntimeError("parity Gram separation changed")
    metrics = summary["audit"]
    if metrics["maximum_rank_two_projector_error"] >= 1.0e-12:
        raise RuntimeError("rank-two error exceeded budget")
    if metrics["maximum_deflated_bulk_error"] >= 1.0e-12:
        raise RuntimeError("bulk error exceeded budget")
    if metrics["maximum_contour_transport"] >= 0.25:
        raise RuntimeError("contour transport margin changed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("a theorem gate is missing")
    if any(summary["program_boundary"].values()):
        raise RuntimeError("claim boundary was overrun")
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in (
        "stationary neumann certificate",
        "bordered newton validation",
        "left parity validation",
        "rank-two deflation",
        "parity contour count",
        "source/observation",
        "stage a1",
        "hilbert--polya",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing boundary phrase: {phrase}")
    archived = [
        ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib",
        ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf",
        ROOT / "validated-peripheral-rank-two-deflation.pdf",
        ROOT / "figures" / "validated_peripheral_rank_two.pdf",
        ROOT / "figures" / "validated_peripheral_rank_two.png",
        ROOT / "results" / "peripheral_validation_audit.json",
        ROOT / "results" / "peripheral_validation_smoke.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "summary.json",
    ]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    payload = {
        "status": "all_archived_hashes_peripheral_gates_and_boundaries_verified",
        "file_count": len(files),
        "files": files,
        "gates": {"all_channels_green": metrics["all_channels_green"], "source_observation_transfer_validated": summary["program_boundary"]["source_observation_transfer_validated"]},
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
