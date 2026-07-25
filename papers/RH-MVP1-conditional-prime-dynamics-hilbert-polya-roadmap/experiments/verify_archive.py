"""Replay RH-MVP1 hashes and enforce the roadmap claim boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_hashes(records: dict[str, str], base: Path, kind: str) -> None:
    for relative, expected in records.items():
        if sha(base / relative) != expected:
            raise RuntimeError(f"{kind} hash mismatch: {relative}")


def main() -> None:
    summary = json.loads((ROOT / "results/summary.json").read_text())
    dependency = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    audit = json.loads((ROOT / "results/mvp_audit.json").read_text())

    verify_hashes(summary["result_hashes"], ROOT, "result")
    verify_hashes(dependency["local_sources"], ROOT, "source")
    verify_hashes(dependency["publication_artifacts"], ROOT, "publication")
    for record in dependency["external_inputs"].values():
        if sha(REPO / record["path"]) != record["sha256"]:
            raise RuntimeError(f"external hash mismatch: {record['path']}")

    counts = audit["audit_summary"]
    required_counts = {
        "numbered_paper_count": 160,
        "readme_count": 160,
        "main_tex_count": 160,
        "pdf_directory_count": 160,
        "summary_archive_count": 131,
        "verification_archive_count": 131,
        "declared_publication_hash_count": 1717,
        "declared_publication_hash_failure_count": 0,
    }
    for key, expected in required_counts.items():
        if counts[key] != expected:
            raise RuntimeError(f"audit count changed: {key}")
    if counts["full_mvp_completion_bundle"] != ["A", "B", "C", "D", "E"]:
        raise RuntimeError("MVP proof-debt frontier changed")
    if counts["hilbert_polya_completion_bundle"] != ["A", "B", "C"]:
        raise RuntimeError("Hilbert--Polya candidate frontier changed")
    if counts["current_unconditional_claim_level"] != "foundation":
        raise RuntimeError("unconditional claim level was promoted")

    boundary = audit["theorem_boundary"]
    forbidden = (
        "all_macro_assumptions_proved",
        "stage_A_proved",
        "canonical_self_adjoint_operator_constructed",
        "prime_power_trace_formula_proved",
        "zeta_spectral_identity_proved",
        "riemann_hypothesis_proved",
    )
    if any(boundary[key] for key in forbidden):
        raise RuntimeError("claim boundary overrun")

    manuscript = " ".join((ROOT / "main.tex").read_text().lower().split())
    for phrase in (
        "spectral-divisor closure",
        "five bold interfaces",
        "target-independent prime-power trace formula",
        "stopping rules",
        "it does \\emph{not} prove",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript boundary phrase: {phrase}")

    archived = [ROOT / relative for relative in (
        ".gitignore",
        "README.md",
        "THEOREM_LEDGER.md",
        "UPDATED_ROADMAP.md",
        "main.tex",
        "references.bib",
        "pyproject.toml",
        "requirements.txt",
        "main.pdf",
        "conditional-prime-dynamics-hilbert-polya-roadmap.pdf",
        "figures/conditional_mvp_roadmap.pdf",
        "figures/conditional_mvp_roadmap.png",
        "results/mvp_audit.json",
        "results/dependency_manifest.json",
        "results/summary.json",
    )]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results/archive_verification.json"
    status = "all_rh_mvp1_hashes_frontiers_and_claim_boundaries_verified"
    output.write_text(json.dumps({
        "status": status,
        "file_count": len(files),
        "files": files,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "file_count": len(files),
        "status": status,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
