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


def verify(records: dict[str, str], base: Path, kind: str) -> None:
    for relative, expected in records.items():
        if sha(base / relative) != expected:
            raise RuntimeError(f"{kind} hash mismatch: {relative}")


def main() -> None:
    summary = json.loads((ROOT / "results/summary.json").read_text())
    dependency = json.loads((ROOT / "results/dependency_manifest.json").read_text())
    audit = json.loads((ROOT / "results/typed_assembly_audit.json").read_text())
    verify(summary["result_hashes"], ROOT, "result")
    verify(dependency["local_sources"], ROOT, "source")
    verify(dependency["publication_artifacts"], ROOT, "publication")
    for record in dependency["external_inputs"].values():
        if sha(REPO / record["path"]) != record["sha256"]:
            raise RuntimeError(f"external hash mismatch: {record['path']}")

    if not all(summary["theorem"].values()):
        raise RuntimeError("theorem gate missing")
    expected = [
        ["Q", "R", "S_lagged", "T", "U", "Z"],
        ["Q", "R", "S_native", "T", "U", "Z"],
    ]
    if audit["minimal_completion_bundles"] != expected:
        raise RuntimeError("typed completion frontier changed")
    if audit["audit_summary"]["omission_witness_count"] != 6:
        raise RuntimeError("omission witness ledger changed")
    boundary = audit["theorem_boundary"]
    for key in (
        "one_step_two_step_limits_identified",
        "eventual_reset_interfaces_proved",
        "physical_packet_to_riesz_bridge_proved",
        "cloud_coefficient_bridge_proved",
        "uniform_complement_limit_proved",
        "canonical_intrinsic_determinant_constructed",
        "gate_A_closed",
        "hilbert_polya_operator",
        "riemann_hypothesis",
    ):
        if boundary[key]:
            raise RuntimeError(f"claim boundary overrun: {key}")

    manuscript = " ".join((ROOT / "main.tex").read_text().lower().split())
    for phrase in (
        "quantitative packet-to-riesz lift",
        "typed relative-determinant assembly",
        "second regularized determinant",
        "does not identify their limits",
        "marked-word stability",
        "architecture-relative completion frontier",
        "does not prove those premises",
        "riemann hypothesis",
    ):
        if phrase not in manuscript:
            raise RuntimeError(f"missing manuscript phrase: {phrase}")

    archived = [ROOT / relative for relative in (
        ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md",
        "main.tex", "references.bib", "pyproject.toml", "requirements.txt",
        "main.pdf", "packet-riesz-relative-determinant-assembly.pdf",
        "figures/typed_moving_cloud_assembly.pdf",
        "figures/typed_moving_cloud_assembly.png",
        "results/typed_assembly_audit.json",
        "results/dependency_manifest.json", "results/summary.json",
    )]
    files = {str(path.relative_to(ROOT)): sha(path) for path in archived}
    output = ROOT / "results/archive_verification.json"
    status = "all_rh161_hashes_typed_frontier_and_claim_boundaries_verified"
    output.write_text(json.dumps({
        "status": status, "file_count": len(files), "files": files,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "file_count": len(files), "status": status}, sort_keys=True))


if __name__ == "__main__":
    main()
