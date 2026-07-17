"""Verify the committed RH-33 code, result, figure, and manuscript archive."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
sys.path.insert(0, str(ROOT / "src"))

from resolvent_atlas import sha256_file, verify_leaf_ledger  # noqa: E402


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    results = ROOT / "results"
    summary = load_json(results / "summary.json")
    manifest = load_json(results / "center_manifest_sigma_1e-02.json")
    dependency = load_json(results / "dependency_manifest.json")
    leaf = verify_leaf_ledger(results / "refined_atlas_sigma_1e-02_leaves.csv")
    checks: dict[str, bool] = {}
    checks["summary_status"] = summary["status"] == (
        "rigorous_full_boundary_resolvent_atlas_and_relative_winding_one_"
        "interior_complement_count_open"
    )
    checks["center_count"] = manifest["center_count"] == 109
    checks["center_residuals"] = all(
        float(row["residual_upper"]) < 1.0 for row in manifest["centers"]
    )
    checks["leaf_count"] = leaf["leaf_count"] == 949
    checks["leaf_partition"] = bool(leaf["exact_rational_partition_verified"])
    checks["leaf_closure"] = (
        leaf["unresolved_leaf_count"] == 0
        and float(leaf["maximum_neumann_product_upper"]) < 1.0
        and float(leaf["maximum_budget_ratio_upper"]) < 1.0
    )
    checks["all_centers_used"] = len(leaf["used_center_ids"]) == 109
    checks["relative_not_absolute_count"] = (
        summary["exact_augmented_block_minus_complement_count"] == 1
        and not summary["interior_complement_pole_count_certified"]
        and not summary["ordinary_feshbach_zero_count_certified"]
    )
    for row in manifest["centers"]:
        checks[f"center_hash_{row['center_id']}"] = (
            sha256_file(ROOT / row["path"]) == row["sha256"]
        )
    for group in ("inputs", "sources"):
        for name, row in dependency[group].items():
            checks[f"dependency_{group}_{name}"] = (
                sha256_file(REPOSITORY / row["path"]) == row["sha256"]
            )
    for name, expected in summary["result_hashes"].items():
        checks[f"summary_hash_{name}"] = (
            sha256_file(results / name) == expected
        )

    manuscript = ROOT / "certified-complement-resolvent-atlas.pdf"
    figure = ROOT / "figures" / "certified_resolvent_atlas.pdf"
    checks["manuscript_exists"] = manuscript.is_file() and manuscript.stat().st_size > 0
    checks["figure_exists"] = figure.is_file() and figure.stat().st_size > 0
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
    figure_paths = sorted(
        path for path in (ROOT / "figures").glob("*") if path.is_file()
    )
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
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
