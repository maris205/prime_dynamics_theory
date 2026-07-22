"""Build RH-100 dependency, inventory, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]; PAPERS = ROOT.parent; REPOSITORY = PAPERS.parent


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""): digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    review = json.loads((ROOT / "results" / "hundred_layer_route_review.json").read_text(encoding="utf-8"))
    external = {}
    for row in review["inventory"]:
        directory = PAPERS / row["directory"]
        for label, relative in (("readme", "README.md"), ("main_tex", "main.tex"), ("summary", "results/summary.json")):
            path = directory / relative
            if path.exists():
                external[f"RH-{row['number']}_{label}"] = {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "hundred_layer_route_review.pdf", ROOT / "figures" / "hundred_layer_route_review.png", ROOT / "main.pdf", ROOT / "hundred-layer-route-review.pdf"]
    dependency = {"status": "all_rh100_inventory_sources_and_publication_artifacts_hashed", "external_inputs": external, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"; dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_paths = [ROOT / "results" / "hundred_layer_route_review.json", ROOT / "results" / "hundred_layer_route_review_smoke.json", dependency_path]
    summary = {
        "status": "rh100_hundred_layer_route_review_archived",
        "theorem": {"status_aware_minimal_completion_bundles": True, "conservative_route_substitution": True, "centennial_inventory": True},
        "inventory": review["inventory_summary"], "stage_A_bundles": review["stage_A_minimal_completion_bundles"], "stage_A5_bundles": review["stage_A5_minimal_completion_bundles"], "next_three_layers": review["next_three_layers"], "claim_boundary": review["claim_boundary"], "executive_verdict": review["executive_verdict"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths}, "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"; summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **review["inventory_summary"], "external_hash_count": len(external)}, sort_keys=True))


if __name__ == "__main__": main()
