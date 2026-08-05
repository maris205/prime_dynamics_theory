"""Independently replay the four-volume archive and claim firewall."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
MANIFEST_PATH = ROOT / "results/four_volume_archive_manifest.json"
OUTPUT_PATH = ROOT / "results/four_volume_archive_verification.json"
SHA256 = re.compile(r"[0-9a-f]{64}")

VOLUME_SPECS = (
    (1, "papers/RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap", (1, 160), "conditional-prime-dynamics-hilbert-polya-roadmap.pdf"),
    (2, "papers/RH-VOL2-physical-riesz-cloud-trace-envelope-synthesis", (161, 241), "physical-riesz-cloud-trace-envelope-synthesis.pdf"),
    (3, "papers/RH-VOL3-deterministic-numerator-anchor-counterloop-synthesis", (242, 281), "deterministic-numerator-anchor-counterloop-synthesis.pdf"),
    (4, "papers/RH-VOL4-noisy-head-annulus-signed-completion-synthesis", (282, 361), "noisy-head-annulus-signed-completion-synthesis.pdf"),
)

MVP1_MEMBERS = {
    ".gitignore", "README.md", "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md",
    "main.tex", "references.bib", "pyproject.toml", "requirements.txt",
    "results/atomic_index.tex", "main.pdf",
    "conditional-prime-dynamics-hilbert-polya-roadmap.pdf",
    "figures/conditional_mvp_roadmap.pdf",
    "figures/conditional_mvp_roadmap.png", "results/mvp_audit.json",
    "results/dependency_manifest.json", "results/summary.json",
}
VOLUME_MEMBERS = {
    ".gitignore", "Makefile", "README.md", "CROSSWALK.md",
    "THEOREM_LEDGER.md", "UPDATED_ROADMAP.md", "main.tex",
    "experiments/build_volume_audit.py", "experiments/build_archive.py",
    "experiments/verify_archive.py", "tests/test_volume.py", "pyproject.toml",
    "requirements.txt", "main.pdf", "results/volume_audit.json",
    "results/dependency_manifest.json", "results/summary.json",
    "results/atomic_index.tex",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_path(base: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise RuntimeError(f"invalid relative path: {relative!r}")
    base_resolved = base.resolve()
    path = (base_resolved / relative).resolve()
    try:
        path.relative_to(base_resolved)
    except ValueError as exc:
        raise RuntimeError(f"path escapes archive root: {relative}") from exc
    if path == base_resolved:
        raise RuntimeError(f"path names archive root, not a file: {relative}")
    return path


def verify_hash_map(records: dict[str, str], base: Path, label: str) -> int:
    count = 0
    for relative, expected in records.items():
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise RuntimeError(f"invalid {label} SHA-256: {relative}")
        path = safe_path(base, relative)
        if not path.is_file() or sha(path) != expected:
            raise RuntimeError(f"{label} hash mismatch: {relative}")
        count += 1
    return count


def validate_archive_payload(
    payload: dict[str, Any], expected_members: set[str], label: str
) -> None:
    files = payload.get("files")
    if not isinstance(files, dict):
        raise RuntimeError(f"{label} archive files map is missing")
    if payload.get("file_count") != len(files):
        raise RuntimeError(f"{label} archive file count mismatch")
    if set(files) != expected_members:
        missing = sorted(expected_members - set(files))
        extra = sorted(set(files) - expected_members)
        raise RuntimeError(
            f"{label} archive membership changed: missing={missing}, extra={extra}"
        )


def validate_manifest_structure(manifest: dict[str, Any]) -> None:
    if manifest.get("schema") != "rh-four-volume-archive-v1":
        raise RuntimeError("four-volume archive schema changed")
    if manifest.get("numbered_source_count") != 361:
        raise RuntimeError("four-volume source count changed")
    if manifest.get("numbered_endpoint_changed") is not False:
        raise RuntimeError("numbered endpoint was changed")
    if manifest.get("atomic_sources_preserved") is not True:
        raise RuntimeError("atomic source preservation flag changed")
    if manifest.get("route_coordinate") != "actual_same_clock_unnormalized_head_transport_open":
        raise RuntimeError("route coordinate was promoted")
    gates = manifest.get("gates")
    if not isinstance(gates, dict) or set(gates) != set("ABCDE") or any(gates.values()):
        raise RuntimeError("four-volume Gate firewall overrun")

    rows = manifest.get("volumes")
    if not isinstance(rows, list) or len(rows) != 4:
        raise RuntimeError("four-volume manifest must contain four volumes")
    observed = []
    archive_counts = []
    for row in rows:
        observed.append((
            row.get("volume"), row.get("root"),
            tuple(row.get("source_range", ())), row.get("distribution_pdf"),
        ))
        if row.get("archive") != "results/archive_verification.json":
            raise RuntimeError("volume archive path changed")
        for key in ("archive_sha256", "main_pdf_sha256", "distribution_pdf_sha256"):
            value = row.get(key)
            if not isinstance(value, str) or not SHA256.fullmatch(value):
                raise RuntimeError(f"invalid manifest SHA-256: {key}")
        count = row.get("archive_file_count")
        if not isinstance(count, int) or count <= 0:
            raise RuntimeError("invalid volume archive file count")
        archive_counts.append(count)

    if observed != list(VOLUME_SPECS):
        raise RuntimeError("four-volume roots or source ranges changed")
    if len({row[1] for row in observed}) != 4:
        raise RuntimeError("duplicate volume root")
    covered = [
        number
        for _, _, (start, end), _ in observed
        for number in range(start, end + 1)
    ]
    if covered != list(range(1, 362)):
        raise RuntimeError("four-volume ranges do not cover RH-1--RH-361")
    if manifest.get("aggregate_archive_file_count") != sum(archive_counts):
        raise RuntimeError("aggregate archive file count mismatch")


def verify_external_inputs(records: dict[str, Any]) -> int:
    count = 0
    for key, value in records.items():
        if isinstance(value, dict):
            relative = value.get("path")
            expected = value.get("sha256")
        else:
            relative = key
            expected = value
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise RuntimeError(f"invalid external input record: {key}")
        count += verify_hash_map({relative: expected}, REPO, "external source")
    return count


def verify_claim_boundary(volume: int, summary: dict[str, Any]) -> None:
    if volume == 1:
        gates = {
            row["key"]: row["status"]
            for row in summary.get("gates", [])
            if row.get("key") in set("ABCDE")
        }
        if gates != {key: "open" for key in "ABCDE"}:
            raise RuntimeError("Volume I Gate boundary changed")
        boundary = summary.get("theorem_boundary", {})
        forbidden = (
            "all_macro_assumptions_proved", "stage_A_proved",
            "canonical_self_adjoint_operator_constructed",
            "prime_power_trace_formula_proved", "zeta_spectral_identity_proved",
            "riemann_hypothesis_proved",
        )
        if any(boundary.get(key) is not False for key in forbidden):
            raise RuntimeError("Volume I theorem boundary overrun")
    else:
        gates = summary.get("gates")
        forbidden = summary.get("forbidden_claims")
        if not isinstance(gates, dict) or any(gates.values()):
            raise RuntimeError(f"Volume {volume} Gate boundary overrun")
        if not isinstance(forbidden, dict) or any(forbidden.values()):
            raise RuntimeError(f"Volume {volume} forbidden claim overrun")
    if volume == 4 and summary.get("rh_362_activated") is not False:
        raise RuntimeError("Volume IV activated RH-362")


def verify_manifest(manifest: dict[str, Any], write_output: bool = True) -> dict[str, Any]:
    validate_manifest_structure(manifest)
    archive_member_count = 0
    dependency_hash_count = 0
    result_hash_count = 0

    for row in manifest["volumes"]:
        volume = int(row["volume"])
        volume_root = safe_path(REPO, row["root"])
        archive_path = safe_path(volume_root, row["archive"])
        if not archive_path.is_file() or sha(archive_path) != row["archive_sha256"]:
            raise RuntimeError(f"Volume {volume} archive seal mismatch")
        archive = json.loads(archive_path.read_text())
        expected = set(MVP1_MEMBERS if volume == 1 else VOLUME_MEMBERS)
        expected.add(row["distribution_pdf"])
        if volume == 1:
            expected.discard(row["distribution_pdf"])
            expected.add("conditional-prime-dynamics-hilbert-polya-roadmap.pdf")
        validate_archive_payload(archive, expected, f"Volume {volume}")
        if archive["file_count"] != row["archive_file_count"]:
            raise RuntimeError(f"Volume {volume} stored file count mismatch")
        archive_member_count += verify_hash_map(
            archive["files"], volume_root, f"Volume {volume} archive member"
        )

        if sha(volume_root / "main.pdf") != row["main_pdf_sha256"]:
            raise RuntimeError(f"Volume {volume} main PDF mismatch")
        if sha(volume_root / row["distribution_pdf"]) != row["distribution_pdf_sha256"]:
            raise RuntimeError(f"Volume {volume} distribution PDF mismatch")
        if row["main_pdf_sha256"] != row["distribution_pdf_sha256"]:
            raise RuntimeError(f"Volume {volume} semantic PDF is not byte-identical")

        dependency = json.loads((volume_root / "results/dependency_manifest.json").read_text())
        dependency_hash_count += verify_hash_map(
            dependency.get("local_sources", {}), volume_root,
            f"Volume {volume} local source",
        )
        dependency_hash_count += verify_hash_map(
            dependency.get("publication_artifacts", {}), volume_root,
            f"Volume {volume} publication artifact",
        )
        dependency_hash_count += verify_external_inputs(
            dependency.get("external_inputs", {})
        )

        summary = json.loads((volume_root / "results/summary.json").read_text())
        result_hash_count += verify_hash_map(
            summary.get("result_hashes", {}), volume_root,
            f"Volume {volume} result",
        )
        verify_claim_boundary(volume, summary)

    result = {
        "status": "rh_four_volume_archive_verified",
        "manifest_sha256": sha(MANIFEST_PATH),
        "volume_count": 4,
        "numbered_source_count": 361,
        "archive_member_count": archive_member_count,
        "dependency_hash_count": dependency_hash_count,
        "result_hash_count": result_hash_count,
        "failure_count": 0,
    }
    if write_output:
        OUTPUT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text())
    result = verify_manifest(manifest)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
