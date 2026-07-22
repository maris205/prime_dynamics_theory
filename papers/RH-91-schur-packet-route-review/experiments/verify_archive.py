"""Verify RH-91 hashes, route gates, and claim boundaries."""

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
    review = load("results/route_review.json")
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
    if len(review["layer_ledger"]) != 9 or review["archive_audit"]["theorem_flag_count"] != 29:
        raise RuntimeError("ten-layer ledger incomplete")
    if not review["archive_audit"]["all_theorem_flags_green"]:
        raise RuntimeError("archived theorem flag failure")
    if not all(row["minimality_certified"] for row in review["bootstrap_budget"]):
        raise RuntimeError("bootstrap budget minimality failed")
    if not all(summary["theorem"].values()):
        raise RuntimeError("review theorem gate missing")
    for key in ("uniform_schur_margin_proved", "uniform_stage_A1_closed", "relative_stage_A5_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        if summary["program_boundary"][key]:
            raise RuntimeError(f"claim boundary overrun: {key}")
    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("schur-to-effective-rank bootstrap theorem", "revised completion frontier", "branch-specific negative results", "moving-cloud", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript:
            raise RuntimeError(f"missing phrase: {phrase}")
    archived = [ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "schur-packet-route-review.pdf", ROOT / "figures" / "schur_packet_route_review.pdf", ROOT / "figures" / "schur_packet_route_review.png", ROOT / "results" / "route_review.json", ROOT / "results" / "route_review_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_schur_packet_review_gates_and_boundaries_verified", "file_count": len(files), "files": files}
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
