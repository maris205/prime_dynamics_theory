"""Verify the RH-117 archive and fixed scale-law claims."""

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


def load(path: str) -> dict[str, object]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    summary = load("results/summary.json")
    dependency = load("results/dependency_manifest.json")
    audit = load("results/scale_law_audit.json")
    for path, expected in summary["result_hashes"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["local_sources"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["publication_artifacts"].items():
        assert sha(ROOT / path) == expected
    for record in dependency["external_inputs"].values():
        assert sha(REPO / record["path"]) == record["sha256"]

    metrics = audit["audit_summary"]
    assert (metrics["scale_count"], metrics["physical_record_count"]) == (5, 120)
    assert metrics["alignment_failure_count"] == 0
    assert metrics["continuation_anchor_failure_count"] == 0
    assert metrics["maximum_observed_certifying_depth"] == 6
    assert metrics["maximum_fit_residual_factor"] > 100.0
    assert metrics["maximum_leave_one_out_exponent_span"] > 4.0
    examples = audit["continuation_barrier"]["examples"]
    assert examples["vanishing"]["probe_value"] < 2e-6
    assert examples["interior_limit"]["probe_value"] == 0.5
    assert examples["unit_limit"]["probe_value"] > 0.99999
    for name in (
        "descriptive_fit_is_asymptotic_law",
        "all_level_capacity_law_proved",
        "all_level_concentration_law_proved",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        assert not audit["theorem_boundary"][name]

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("bounded finite-anchor extension", "asymptotic nonidentifiability", "descriptive", "riemann hypothesis"):
        assert phrase in manuscript
    archived = [
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
            "main.pdf",
            "finite-anchor-scale-law-barrier.pdf",
            "figures/finite_anchor_scale_law_barrier.pdf",
            "figures/finite_anchor_scale_law_barrier.png",
            "results/scale_law_audit.json",
            "results/scale_law_smoke.json",
            "results/dependency_manifest.json",
            "results/summary.json",
        )
    ]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(
            {"status": "all_rh117_archive_hashes_verified", "file_count": len(files), "files": files},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": "all_rh117_archive_hashes_verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
