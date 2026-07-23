"""Verify the RH-119 archive and fixed ten-layer claims."""

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
    audit = load("results/ten_layer_review_audit.json")
    for path, expected in summary["result_hashes"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["local_sources"].items():
        assert sha(ROOT / path) == expected
    for path, expected in dependency["publication_artifacts"].items():
        assert sha(ROOT / path) == expected
    for record in dependency["external_inputs"].values():
        assert sha(REPO / record["path"]) == record["sha256"]

    metrics = audit["audit_summary"]
    assert (metrics["layer_count"], metrics["upstream_archive_count"]) == (10, 9)
    assert (metrics["constructive_layer_count"], metrics["negative_layer_count"], metrics["synthesis_layer_count"]) == (6, 2, 2)
    assert metrics["theorem_check_failure_count"] == 0
    assert metrics["closed_route_count"] == 4
    assert metrics["frontier_packet_count"] == 3
    assert metrics["proved_frontier_packet_count"] == 0
    assert not metrics["eventual_support_reachable"]
    assert metrics["finite_archive_support_reachable"]
    assert metrics["each_physical_packet_individually_completes_conditional_graph"]
    assert metrics["finite_actual_support_count"] == metrics["finite_adaptive_support_count"] == 322
    assert audit["proof_graph"]["mathematical_minimal_missing_sets"] == [
        ["direct_margin_packet"],
        ["directional_rayleigh_packet"],
        ["trace_concentration_packet"],
    ]
    for name in (
        "eventual_fourth_mode_support_proved",
        "all_level_outward_admissibility_proved",
        "uniform_stage_A_closed",
        "hilbert_polya_operator",
        "zeta_zero_identification",
        "riemann_hypothesis",
    ):
        assert not audit["theorem_boundary"][name]

    manuscript = " ".join((ROOT / "main.tex").read_text(encoding="utf-8").lower().split())
    for phrase in ("q_4=\\frac{\\nu_4}{\\lambda_{23}}", "proof-frontier antichain", "closed branches", "riemann hypothesis"):
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
            "ten-layer-exterior-route-review.pdf",
            "figures/ten_layer_exterior_route_review.pdf",
            "figures/ten_layer_exterior_route_review.png",
            "results/ten_layer_review_audit.json",
            "results/ten_layer_review_smoke.json",
            "results/dependency_manifest.json",
            "results/summary.json",
        )
    ]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(
            {"status": "all_rh119_archive_hashes_verified", "file_count": len(files), "files": files},
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": "all_rh119_archive_hashes_verified"}, sort_keys=True))


if __name__ == "__main__":
    main()
