"""Verify the committed RH-32 certificate, source, figure, and PDF archive."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from certificate_ledger import sha256_file  # noqa: E402


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    results = ROOT / "results"
    summary = load_json(results / "summary.json")
    projected = load_json(results / "projected_count_certificates.json")
    reconstruction = load_json(results / "model_reconstruction_audit.json")
    replay = load_json(results / "rh28_reconstruction_verification.json")
    dependency = load_json(results / "dependency_ledger.json")

    checks: dict[str, bool] = {}
    checks["summary_status"] = summary["status"] == (
        "projected_base_certified_selected_arcs_closed_full_contours_open"
    )
    checks["projected_status"] = (
        projected["status"] == "rigorous_exact_binary64_projected_counts"
    )
    checks["reconstruction_status"] = (
        reconstruction["status"] == "deterministic_rh28_base_snapshots_archived"
    )
    checks["replay_status"] = (
        replay["status"] == "all_deterministic_rh28_fields_exactly_reproduced"
    )
    checks["dependency_status"] = (
        dependency["status"] == "all_recorded_upstream_hashes_verified"
        and all(dependency["checks"].values())
        and all(edge["verified"] for edge in dependency["edges"])
    )
    checks["projected_counts"] = all(
        row["projected_zero_count"] == 1
        and row["projected_pole_count"] == 0
        and row["projected_determinant_winding"] == 1
        and row["augmented"]["ambiguous_count"] == 0
        and row["projected_poles"]["ambiguous_count"] == 0
        for row in projected["scales"]
    )
    checks["replay_counts"] = all(
        row["arc_mismatch_count"] == 0
        and row["summary_mismatch_count"] == 0
        and row["snapshot_matches_fresh_rebuild_bitwise"]
        for row in replay["scales"]
    )

    for name, expected in summary["result_hashes"].items():
        checks[f"summary_hash_{name}"] = sha256_file(results / name) == expected
    for name, node in dependency["nodes"].items():
        checks[f"dependency_node_{name}"] = (
            sha256_file(REPOSITORY / node["path"]) == node["sha256"]
        )

    with (results / "composition_summary.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        composition = list(csv.DictReader(handle))
    checks["composition_locality"] = all(
        int(row["transport_closed_arc_count"]) == 1
        and int(row["neumann_failure_arc_count"])
        == int(row["accepted_arc_count"]) - 1
        and int(row["full_contour_closed"]) == 0
        for row in composition
    )

    manuscript = ROOT / "end-to-end-certificate-ledger.pdf"
    checks["manuscript_exists"] = manuscript.is_file() and manuscript.stat().st_size > 0
    if not all(checks.values()):
        failures = [name for name, passed in checks.items() if not passed]
        raise RuntimeError(f"archive verification failure(s): {failures}")

    code_paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "pyproject.toml",
        ROOT / "requirements.txt",
    ]
    code_paths.extend(sorted((ROOT / "src").rglob("*.py")))
    code_paths.extend(sorted((ROOT / "experiments").glob("*.py")))
    code_paths.extend(sorted((ROOT / "tests").glob("*.py")))
    result_paths = sorted(
        path
        for path in results.rglob("*")
        if path.is_file() and path.name != "archive_verification.json"
    )
    figure_paths = sorted(path for path in (ROOT / "figures").glob("*") if path.is_file())
    payload = {
        "status": "verified",
        "checks": checks,
        "code_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in code_paths
        },
        "result_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in result_paths
        },
        "figure_hashes": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in figure_paths
        },
        "manuscript": {
            "path": manuscript.name,
            "sha256": sha256_file(manuscript),
        },
    }
    (results / "archive_verification.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
