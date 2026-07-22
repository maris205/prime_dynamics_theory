"""Verify RH-75 hashes, anchors, and boundaries."""

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
    audit = load("results/log_square_block_audit.json")
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
    if len(audit["rows"]) != 5 or not audit["all_executed_anchors_green"]:
        raise RuntimeError("five-anchor audit is incomplete")
    metrics = summary["audit"]
    if metrics["maximum_q_over_sqrt_sigma"] > 0.086:
        raise RuntimeError("square-root contraction constant changed")
    if metrics["maximum_actual_tail"] >= metrics["common_tail_envelope"]:
        raise RuntimeError("common tail envelope failed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    boundary = summary["program_boundary"]
    if not boundary["five_anchor_law_validated"] or any(value for key, value in boundary.items() if key != "five_anchor_law_validated"):
        raise RuntimeError("claim boundary was overrun")
    manuscript = (ROOT / "main.tex").read_text(encoding="utf-8").lower()
    for phrase in ("log-square square-root block criterion", "critical", "five interval anchors", "all-dyadic", "stage a1", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    archived = [ROOT / "README.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "log-square-block-contraction-law.pdf", ROOT / "figures" / "log_square_block_contraction.pdf", ROOT / "figures" / "log_square_block_contraction.png", ROOT / "results" / "log_square_block_audit.json", ROOT / "results" / "log_square_block_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_log_square_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
