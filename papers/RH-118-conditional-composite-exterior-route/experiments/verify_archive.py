"""Verify the RH-118 archive and fixed route claims."""

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
    audit = load("results/conditional_route_audit.json")
    for path, expected in summary["result_hashes"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["local_sources"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["publication_artifacts"].items():
        assert sha(ROOT / path) == expected
    for record in dependency["external_inputs"].values():
        assert sha(REPO / record["path"]) == record["sha256"]

    metrics = audit["audit_summary"]
    assert (metrics["scale_count"], metrics["update_count"], metrics["fine_update_count"]) == (5, 360, 234)
    assert (metrics["actual_support_count"], metrics["composite_support_count"], metrics["adaptive_support_count"]) == (322, 321, 322)
    assert metrics["composite_missed_supported_count"] == 1
    assert metrics["adaptive_missed_supported_count"] == 0
    assert metrics["composite_false_positive_count"] == 0
    assert metrics["adaptive_false_positive_count"] == 0
    assert metrics["support_label_disagreement_count"] == 0
    assert metrics["selected_route_counts"] == {
        "direct_weyl": 189,
        "directional_rayleigh": 171,
        "spectral_capacity": 0,
        "trace_concentration": 0,
    }
    expected = {"1e-08": (115, 114, 115), "1e-06": (109, 109, 109), "1e-04": (98, 98, 98)}
    for key, counts in expected.items():
        record = audit["threshold_summary"][key]
        assert (record["actual_support_count"], record["composite_support_count"], record["adaptive_support_count"]) == counts
    assert len(audit["minimal_physical_packets"]) == 3
    assert not audit["theorem_boundary"]["any_all_level_physical_packet_proved"]
    for name in ("uniform_stage_A_closed", "hilbert_polya_operator", "riemann_hypothesis"):
        assert not audit["theorem_boundary"][name]

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("conditional composite exterior route", "liminf closure", "alternating-route", "riemann hypothesis"):
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
            "conditional-composite-exterior-route.pdf",
            "figures/conditional_composite_exterior_route.pdf",
            "figures/conditional_composite_exterior_route.png",
            "results/conditional_route_audit.json",
            "results/conditional_route_smoke.json",
            "results/dependency_manifest.json",
            "results/summary.json",
        )
    ]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(
            {"status": "all_rh118_archive_hashes_verified", "file_count": len(files), "files": files},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": "all_rh118_archive_hashes_verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
