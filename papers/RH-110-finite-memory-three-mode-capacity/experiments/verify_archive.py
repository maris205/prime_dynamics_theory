"""Verify RH-110 archive hashes and theorem boundaries."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def load(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

def main() -> None:
    summary = load("results/summary.json")
    dep = load("results/dependency_manifest.json")
    audit = load("results/three_mode_capacity_audit.json")
    for rel, expected in summary["result_hashes"].items():
        assert sha(ROOT / rel) == expected, rel
    for rel, expected in dep["local_sources"].items():
        assert sha(ROOT / rel) == expected, rel
    for rel, expected in dep["publication_artifacts"].items():
        assert sha(ROOT / rel) == expected, rel
    for item in dep["external_inputs"].values():
        path = REPO / item["path"]
        assert sha(path) == item["sha256"], str(path)
    s = audit["audit_summary"]
    assert (s["scale_count"], s["channel_count"], s["update_count"], s["fine_update_count"]) == (5, 10, 360, 234)
    assert s["capacity_enclosure_failure_count"] == 0
    assert s["recovery_implication_failure_count"] == 0
    assert s["selector_equivalence_failure_count"] == 0
    assert s["all_threshold_counts_match_direct_weyl"]
    assert audit["threshold_summary"]["1e-08"]["recovery_support_count"] == 113
    assert audit["threshold_summary"]["1e-06"]["recovery_support_count"] == 109
    assert audit["threshold_summary"]["1e-04"]["recovery_support_count"] == 98
    for key in ("all_level_capacity_upper_law_proved", "all_level_physical_volume_lower_bound_proved", "uniform_stage_A_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        assert not audit["theorem_boundary"][key], key
    text = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("finite-memory three-mode capacity enclosure", "exterior-to-fourth-mode recovery", "sharp fixed-volume capacity interval", "hilbert--polya", "riemann hypothesis"):
        assert phrase in text, phrase
    archived = [ROOT / name for name in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex", "references.bib",
        "pyproject.toml", "requirements.txt", "main.pdf", "finite-memory-three-mode-capacity.pdf",
        "figures/finite_memory_three_mode_capacity.pdf", "figures/finite_memory_three_mode_capacity.png",
        "results/three_mode_capacity_audit.json", "results/three_mode_capacity_smoke.json",
        "results/dependency_manifest.json", "results/summary.json")]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    out = ROOT / "results/archive_verification.json"
    out.write_text(json.dumps({"status": "all_rh110_archive_hashes_verified", "file_count": len(files), "files": files}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out.relative_to(ROOT)), "file_count": len(files), "status": "all_rh110_archive_hashes_verified"}, sort_keys=True))

if __name__ == "__main__":
    main()
