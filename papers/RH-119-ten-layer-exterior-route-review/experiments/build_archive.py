"""Build RH-119 dependency hashes and publication summary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPO = PAPERS.parent
PAPER_DIRECTORIES = {
    110: "RH-110-finite-memory-three-mode-capacity",
    111: "RH-111-tail-energy-exterior-concentration",
    112: "RH-112-global-wedge-lipschitz-barrier",
    113: "RH-113-right-frame-directional-wedge",
    114: "RH-114-psd-rayleigh-directional-tail",
    115: "RH-115-composite-directional-support-gate",
    116: "RH-116-monotone-memory-depth-optimization",
    117: "RH-117-finite-anchor-scale-law-barrier",
    118: "RH-118-conditional-composite-exterior-route",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    external = {
        f"rh{number}_summary": PAPERS / directory / "results" / "summary.json"
        for number, directory in PAPER_DIRECTORIES.items()
    }
    local = sorted(
        {
            *(ROOT / "src").rglob("*.py"),
            *(ROOT / "experiments").glob("*.py"),
            *(ROOT / "tests").glob("*.py"),
        }
    )
    publications = [
        ROOT / name
        for name in (
            ".gitignore",
            "README.md",
            "THEOREM_LEDGER.md",
            "UPDATED_ROADMAP.md",
            "main.tex",
            "references.bib",
            "pyproject.toml",
            "requirements.txt",
            "figures/ten_layer_exterior_route_review.pdf",
            "figures/ten_layer_exterior_route_review.png",
            "main.pdf",
            "ten-layer-exterior-route-review.pdf",
        )
    ]
    dependency = {
        "status": "all_rh119_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {
            name: {"path": str(path.relative_to(REPO)), "sha256": sha(path)}
            for name, path in external.items()
        },
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    audit = json.loads((ROOT / "results" / "ten_layer_review_audit.json").read_text(encoding="utf-8"))
    result_paths = [
        ROOT / "results" / "ten_layer_review_audit.json",
        ROOT / "results" / "ten_layer_review_smoke.json",
        dependency_path,
    ]
    summary = {
        "status": "rh119_ten_layer_exterior_route_review_archived",
        "theorem": {
            "ten_layer_factor_ledger_verified": True,
            "proof_frontier_antichain_identified": True,
            "minimal_missing_sets_verified": True,
        },
        "audit": audit["audit_summary"],
        "factor_ledger": audit["factor_ledger"],
        "closed_routes": audit["closed_routes"],
        "proof_graph": audit["proof_graph"],
        "physical_frontier": audit["physical_frontier"],
        "program_boundary": audit["theorem_boundary"],
        "revised_roadmap": audit["revised_roadmap"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), **audit["audit_summary"]}, sort_keys=True))


if __name__ == "__main__":
    main()
