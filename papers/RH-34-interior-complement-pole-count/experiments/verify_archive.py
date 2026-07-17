"""Verify and hash the committed RH-34 reproducibility archive."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    summary = json.loads(
        (ROOT / "results" / "summary.json").read_text(encoding="utf-8")
    )
    dependency = json.loads(
        (ROOT / "results" / "dependency_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    for name, expected in summary["result_hashes"].items():
        path = ROOT / "results" / name
        if sha256_file(path) != expected:
            raise RuntimeError(f"result hash mismatch: {path}")
    for group in ("inputs", "sources"):
        for row in dependency[group].values():
            path = REPOSITORY / row["path"]
            if sha256_file(path) != row["sha256"]:
                raise RuntimeError(f"dependency hash mismatch: {path}")

    paths = [
        ROOT / "README.md",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "interior-complement-pole-count.pdf",
        ROOT / "figures" / "schur_similarity_closure.pdf",
        ROOT / "figures" / "schur_similarity_closure.png",
        ROOT / "results" / "summary.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "schur_similarity_sigma_1e-02.json",
        ROOT / "results" / "schur_diagonal_sigma_1e-02.csv",
        ROOT / "results" / "schur_diagonal_sigma_1e-02.npz",
        ROOT / "results" / "schur_homotopy_leaves_sigma_1e-02.csv",
        ROOT / "src" / "complement_poles" / "certificate.py",
        ROOT / "experiments" / "run_schur_similarity_certificate.py",
        ROOT / "experiments" / "build_archive.py",
        ROOT / "experiments" / "make_figures.py",
    ]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise RuntimeError(f"archive paths are missing: {missing}")
    payload = {
        "status": "all_archived_hashes_and_theorem_gates_verified",
        "file_count": len(paths),
        "files": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in paths
        },
        "theorem_gates": {
            "interior_complement_pole_count": summary[
                "interior_complement_pole_count"
            ],
            "ordinary_feshbach_zero_count": summary[
                "ordinary_feshbach_zero_count"
            ],
            "stored_augmented_block_inside_count": summary[
                "stored_augmented_block_inside_count"
            ],
            "maximum_homotopy_neumann_product_upper": summary[
                "maximum_homotopy_neumann_product_upper"
            ],
        },
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
