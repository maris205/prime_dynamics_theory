from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PAPERS = ROOT.parent


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def paper(number: int) -> Path:
    matches = list(PAPERS.glob(f"RH-{number}-*"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one RH-{number} directory")
    return matches[0]


def main() -> None:
    external = {}
    for number in range(151, 159):
        directory = paper(number)
        external[f"rh{number}_summary"] = directory / "results/summary.json"
        external[f"rh{number}_archive"] = directory / "results/archive_verification.json"
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/ten_layer_reset_route_review.pdf",
        "figures/ten_layer_reset_route_review.png", "main.pdf", "ten-layer-reset-route-review.pdf",
    )]
    dependency = {
        "status": "all_rh159_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/route_audit.json").read_text())
    result_files = [ROOT / "results/route_audit.json", ROOT / "results/dependency_manifest.json"]
    summary = {
        "status": "rh159_ten_layer_reset_route_review_archived",
        "theorem": {
            "positive_block_cross_to_compression": True,
            "strict_reverse_nonimplication": True,
            "typed_finite_route_classification": True,
        },
        "audit": audit["audit_summary"],
        "metrics": audit["metrics"],
        "typed_route_conclusion": audit["typed_route_conclusion"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
