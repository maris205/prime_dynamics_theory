"""Verify the RH-116 archive and its fixed numerical claims."""

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
    audit = load("results/memory_depth_audit.json")
    for path, expected in summary["result_hashes"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["local_sources"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["publication_artifacts"].items():
        assert sha(ROOT / path) == expected
    for record in dependency["external_inputs"].values():
        assert sha(REPO / record["path"]) == record["sha256"]

    metrics = audit["audit_summary"]
    assert (metrics["scale_count"], metrics["channel_count"], metrics["update_count"]) == (5, 10, 360)
    assert metrics["supported_update_count"] == metrics["adaptive_certificate_count"] == 322
    assert metrics["maximum_certifying_depth"] == 6
    assert metrics["tail_enclosure_failure_count"] == 0
    assert metrics["dominance_failure_count"] == 0
    assert metrics["monotone_failure_count"] == 0
    assert metrics["completeness_failure_count"] == 0
    expected = {"1e-08": (115, 6), "1e-06": (109, 5), "1e-04": (98, 4)}
    for key, values in expected.items():
        record = audit["threshold_summary"][key]
        assert (record["adaptive_certificate_count"], record["maximum_certifying_depth"]) == values
        assert record["fine_certificate_count"] == 78
    for name in ("all_level_uniform_depth_proved", "uniform_stage_A_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        assert not audit["theorem_boundary"][name]

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("nested weyl monotonicity", "first-passage", "full-history completeness", "riemann hypothesis"):
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
            "monotone-memory-depth-optimization.pdf",
            "figures/monotone_memory_depth_optimization.pdf",
            "figures/monotone_memory_depth_optimization.png",
            "results/memory_depth_audit.json",
            "results/memory_depth_smoke.json",
            "results/dependency_manifest.json",
            "results/summary.json",
        )
    ]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(
            {"status": "all_rh116_archive_hashes_verified", "file_count": len(files), "files": files},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": "all_rh116_archive_hashes_verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
