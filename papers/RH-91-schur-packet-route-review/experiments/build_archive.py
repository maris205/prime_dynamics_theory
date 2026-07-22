"""Build RH-91 dependency, result, and publication hashes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent

LAYERS = [
    "RH-82-half-log-postblock-rank-clock",
    "RH-83-optimal-endpoint-singular-factorization",
    "RH-84-ky-fan-tail-majorization",
    "RH-85-midblock-snapshot-packets",
    "RH-86-trace-normalized-late-memory-packets",
    "RH-87-rayleigh-injection-recursion",
    "RH-88-predictor-corrector-energy-contraction",
    "RH-89-rank-one-complement-ritz-correction",
    "RH-90-schur-secular-subquarter-certificate",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def entry(path: Path) -> dict[str, str]:
    return {"path": str(path.relative_to(REPOSITORY)), "sha256": sha256_file(path)}


def main() -> None:
    external = {directory.lower().replace("-", "_") + "_summary": PAPERS / directory / "results" / "summary.json" for directory in LAYERS}
    external["rh81_route_review_summary"] = PAPERS / "RH-81-stage-A-to-A5-route-review" / "results" / "summary.json"
    external["rh78_two_corridor_summary"] = PAPERS / "RH-78-two-corridor-stage-A1-composition" / "results" / "summary.json"
    local = sorted({*(ROOT / "src").rglob("*.py"), *(ROOT / "experiments").glob("*.py"), *(ROOT / "tests").glob("*.py")})
    publications = [ROOT / ".gitignore", ROOT / "README.md", ROOT / "UPDATED_ROADMAP.md", ROOT / "THEOREM_LEDGER.md", ROOT / "main.tex", ROOT / "references.bib", ROOT / "pyproject.toml", ROOT / "requirements.txt", ROOT / "figures" / "schur_packet_route_review.pdf", ROOT / "figures" / "schur_packet_route_review.png", ROOT / "main.pdf", ROOT / "schur-packet-route-review.pdf"]
    dependency = {"status": "all_rh91_inputs_sources_and_publication_artifacts_hashed", "external_inputs": {name: entry(path) for name, path in external.items()}, "local_sources": {str(path.relative_to(ROOT)): sha256_file(path) for path in local}, "publication_artifacts": {str(path.relative_to(ROOT)): sha256_file(path) for path in publications}}
    dependency_path = ROOT / "results" / "dependency_manifest.json"
    dependency_path.write_text(json.dumps(dependency, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    review = json.loads((ROOT / "results" / "route_review.json").read_text(encoding="utf-8"))
    result_paths = [ROOT / "results" / "route_review.json", ROOT / "results" / "route_review_smoke.json", dependency_path]
    summary = {
        "status": "rh91_schur_packet_route_review_archived",
        "theorem": {"schur_to_effective_rank_bootstrap": True, "revised_completion_frontier": True, "ten_layer_dependency_ledger": True},
        "audit": {**review["archive_audit"], "bootstrap_budget_count": len(review["bootstrap_budget"]), "updates_for_1e_minus_6": next(row["updates"] for row in review["bootstrap_budget"] if row["tolerance"] == 1e-6), "updates_for_1e_minus_12": next(row["updates"] for row in review["bootstrap_budget"] if row["tolerance"] == 1e-12)},
        "program_boundary": review["theorem_boundary"],
        "route_consequence": review["route_consequence"],
        "result_hashes": {str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths},
        "publication_artifact_hashes": dependency["publication_artifacts"],
    }
    summary_path = ROOT / "results" / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"summary": str(summary_path.relative_to(ROOT)), "papers": review["archive_audit"]["paper_count"], "theorem_flags": review["archive_audit"]["theorem_flag_count"], "updates_1e_12": summary["audit"]["updates_for_1e_minus_12"]}, sort_keys=True))


if __name__ == "__main__":
    main()
