"""Verify the RH-162--171 publication manifest and claim boundaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "experiments"))

from build_archive import publication_files  # noqa: E402


NAMED_PDFS = {
    162: "ambient-realization-reset-riesz-gate.pdf",
    163: "two-sided-schur-packet-riesz-certificate.pdf",
    164: "balanced-similarity-packet-coupling.pdf",
    165: "midgap-normal-block-contour.pdf",
    166: "bi-ritz-directional-riesz-graph.pdf",
    167: "finite-mesh-resolvent-envelope.pdf",
    168: "operator-ball-mesh-schur-transfer.pdf",
    169: "common-coordinate-riesz-transport.pdf",
    170: "rank-growing-riesz-shell-atlas.pdf",
    171: "ten-layer-physical-riesz-interface-review.pdf",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    manifest_path = ROOT / "results" / "dependency_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest["files"]
    actual_paths = publication_files()
    actual_names = {str(path.relative_to(PAPERS)) for path in actual_paths}
    if actual_names != set(expected):
        missing = sorted(set(expected) - actual_names)
        extra = sorted(actual_names - set(expected))
        raise RuntimeError(f"manifest file-set mismatch: missing={missing}, extra={extra}")
    mismatches = []
    for relative, digest in expected.items():
        actual = sha256(PAPERS / relative)
        if actual != digest:
            mismatches.append(relative)
    if mismatches:
        raise RuntimeError(f"hash mismatches: {mismatches}")

    pdf_pairs = []
    for number, named in NAMED_PDFS.items():
        matches = tuple(PAPERS.glob(f"RH-{number}-*"))
        directory = matches[0]
        main_digest = sha256(directory / "main.pdf")
        named_digest = sha256(directory / named)
        if main_digest != named_digest:
            raise RuntimeError(f"RH-{number} named PDF differs from main.pdf")
        pdf_pairs.append({"paper": f"RH-{number}", "sha256": main_digest})

    frontier = json.loads((ROOT / "results" / "r_frontier_audit.json").read_text(encoding="utf-8"))
    if frontier["finite_matrix_case_count"] != 3584:
        raise RuntimeError("aggregate finite-case count changed")
    if frontier["rank_change_witness_count"] != 63 or frontier["aggregate_failure_count"] != 0:
        raise RuntimeError("aggregate audit boundary failed")
    boundary = frontier["theorem_boundary"]
    forbidden_true = (
        "physical_R_interface",
        "macro_gate_A",
        "gate_B",
        "gate_C",
        "gate_D",
        "gate_E",
        "riemann_hypothesis",
    )
    if any(boundary[key] for key in forbidden_true):
        raise RuntimeError("claim boundary was promoted")

    payload = {
        "status": "all_rh162_171_hashes_pdfs_audits_and_claim_boundaries_verified",
        "file_count": len(expected),
        "pdf_pair_count": len(pdf_pairs),
        "pdf_pairs": pdf_pairs,
        "finite_matrix_case_count": frontier["finite_matrix_case_count"],
        "rank_change_witness_count": frontier["rank_change_witness_count"],
        "aggregate_failure_count": frontier["aggregate_failure_count"],
    }
    output = ROOT / "results" / "archive_verification.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(expected), "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
