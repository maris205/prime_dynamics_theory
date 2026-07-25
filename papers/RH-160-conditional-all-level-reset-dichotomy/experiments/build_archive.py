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
    external = {
        "rh152_overlap_audit": paper(152) / "results/overlap_audit.json",
        "rh155_memory_audit": paper(155) / "results/memory_pair_audit.json",
        "rh156_support_audit": paper(156) / "results/support_audit.json",
        "rh158_lag_audit": paper(158) / "results/lag_audit.json",
        "rh159_route_audit": paper(159) / "results/route_audit.json",
    }
    for number in range(151, 160):
        external[f"rh{number}_archive"] = paper(number) / "results/archive_verification.json"
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "figures/conditional_all_level_reset_dichotomy.pdf",
        "figures/conditional_all_level_reset_dichotomy.png", "main.pdf", "conditional-all-level-reset-dichotomy.pdf",
    )]
    dependency = {
        "status": "all_rh160_inputs_sources_and_publication_artifacts_hashed",
        "external_inputs": {key: {"path": str(path.relative_to(REPO)), "sha256": sha(path)} for key, path in external.items()},
        "local_sources": {str(path.relative_to(ROOT)): sha(path) for path in local},
        "publication_artifacts": {str(path.relative_to(ROOT)): sha(path) for path in publications},
    }
    (ROOT / "results/dependency_manifest.json").write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n")
    audit = json.loads((ROOT / "results/conditional_audit.json").read_text())
    result_files = [ROOT / "results/conditional_audit.json", ROOT / "results/dependency_manifest.json"]
    summary = {
        "status": "rh160_conditional_all_level_reset_dichotomy_archived",
        "theorem": {
            "three_interface_native_floor": True,
            "adaptive_lag_directional_floor": True,
            "outward_lag_certificate": True,
            "interface_minimality_with_witnesses": True,
        },
        "audit": audit["audit_summary"],
        "constants": audit["constants"],
        "conditional_interfaces": audit["conditional_interfaces"],
        "program_boundary": audit["theorem_boundary"],
        "route_consequence": audit["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha(path) for path in result_files},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    output = ROOT / "results/summary.json"
    output.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"summary": str(output.relative_to(ROOT)), **audit["audit_summary"], **audit["constants"]}, sort_keys=True))


if __name__ == "__main__":
    main()
