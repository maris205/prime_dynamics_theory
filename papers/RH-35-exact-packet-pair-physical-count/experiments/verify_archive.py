"""Verify and hash the committed RH-35 reproducibility archive."""

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
        ROOT / "exact-packet-pair-physical-count.pdf",
        ROOT / "figures" / "packet_pair_physical_count.pdf",
        ROOT / "figures" / "packet_pair_physical_count.png",
        ROOT / "results" / "summary.json",
        ROOT / "results" / "dependency_manifest.json",
        ROOT / "results" / "packet_pair_certificate_sigma_1e-02.json",
        ROOT / "results" / "exact_packet_defect_sigma_1e-02.json",
        ROOT / "results" / "packet_pair_transfer_sigma_1e-02.csv",
        ROOT / "src" / "packet_pair" / "certificate.py",
        ROOT / "experiments" / "run_packet_pair_certificate.py",
        ROOT / "experiments" / "build_archive.py",
        ROOT / "experiments" / "make_figures.py",
    ]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise RuntimeError(f"archive paths are missing: {missing}")
    payload = {
        "status": "all_archived_hashes_and_physical_count_gates_verified",
        "file_count": len(paths),
        "files": {
            str(path.relative_to(ROOT)): sha256_file(path) for path in paths
        },
        "theorem_gates": {
            "pair_defect_frobenius_upper": summary[
                "pair_defect_frobenius_upper"
            ],
            "maximum_complement_neumann_product_upper": summary[
                "maximum_complement_neumann_product_upper"
            ],
            "maximum_feshbach_rouche_product_upper": summary[
                "maximum_feshbach_rouche_product_upper"
            ],
            "physical_two_step_inside_count": summary[
                "physical_two_step_inside_count"
            ],
        },
    }
    (ROOT / "results" / "archive_verification.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
