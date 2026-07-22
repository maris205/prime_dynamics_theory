"""Verify RH-100 hashes, inventory, frontier, roadmap, and boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]; REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""): digest.update(chunk)
    return digest.hexdigest()


def load(path: str): return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json"); dependency = load("results/dependency_manifest.json"); review = load("results/hundred_layer_route_review.json")
    for relative, expected in summary["result_hashes"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"result hash mismatch: {relative}")
    for relative, expected in dependency["local_sources"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"source hash mismatch: {relative}")
    for relative, expected in dependency["publication_artifacts"].items():
        if sha256_file(ROOT / relative) != expected: raise RuntimeError(f"publication hash mismatch: {relative}")
    for record in dependency["external_inputs"].values():
        path = REPOSITORY / record["path"]
        if sha256_file(path) != record["sha256"]: raise RuntimeError(f"external hash mismatch: {path}")

    inventory = review["inventory_summary"]
    if inventory["paper_count"] != 99 or inventory["readme_count"] != 99 or inventory["main_tex_count"] != 99 or inventory["paper_pdf_count"] != 99: raise RuntimeError("centennial inventory incomplete")
    if inventory["summary_count"] != 70: raise RuntimeError("summary count changed")
    if len(review["stage_A_minimal_completion_bundles"]) != 3 or len(review["stage_A5_minimal_completion_bundles"]) != 3: raise RuntimeError("completion frontier changed")
    if review["preferred_packet_bundle"] not in review["stage_A_minimal_completion_bundles"]: raise RuntimeError("preferred bundle missing")
    if [row["layer"] for row in review["next_three_layers"]] != [101, 102, 103]: raise RuntimeError("post-centennial plan changed")
    if not all(summary["theorem"].values()): raise RuntimeError("review theorem missing")
    for key, value in review["claim_boundary"].items():
        if value: raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("status-aware completion frontier theorem", "ninety-nine-layer inventory", "preferred stopped-hybrid packet bundle", "moving-cloud a5 frontier", "hilbert--polya", "riemann hypothesis"):
        if phrase not in manuscript: raise RuntimeError(f"missing phrase: {phrase}")

    archived = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "main.pdf", ROOT / "hundred-layer-route-review.pdf", ROOT / "figures" / "hundred_layer_route_review.pdf", ROOT / "figures" / "hundred_layer_route_review.png", ROOT / "results" / "hundred_layer_route_review.json", ROOT / "results" / "hundred_layer_route_review_smoke.json", ROOT / "results" / "dependency_manifest.json", ROOT / "results" / "summary.json"]
    files = {str(path.relative_to(ROOT)): sha256_file(path) for path in archived}; output = ROOT / "results" / "archive_verification.json"
    payload = {"status": "all_archived_hashes_centennial_inventory_frontier_roadmap_and_boundaries_verified", "file_count": len(files), "files": files}; output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__": main()
