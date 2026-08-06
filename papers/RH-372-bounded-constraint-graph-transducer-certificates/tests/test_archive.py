from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from experiments import build_archive, verify_archive


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "results/dependency_manifest.json"
VERIFICATION = ROOT / "results/archive_verification.json"


def test_archive_membership_is_fixed_and_path_safe() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 21
    assert len(build_archive.EXTERNAL_INPUTS) == 9
    assert len(set(build_archive.LOCAL_MEMBERS)) == 21
    assert len(set(build_archive.EXTERNAL_INPUTS)) == 9
    assert all(".." not in Path(member).parts for member in build_archive.LOCAL_MEMBERS)
    assert all(".." not in Path(member).parts for member in build_archive.EXTERNAL_INPUTS)


def test_archive_digest_matches_standard_sha256(tmp_path: Path) -> None:
    sample = tmp_path / "sample.bin"
    sample.write_bytes(b"RH-372 archive hash\n")
    expected = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert build_archive.digest(sample) == expected
    assert verify_archive.digest(sample) == expected


def test_manifest_hashes_are_current_when_archive_exists() -> None:
    if not MANIFEST.is_file():
        # `make test` is intentionally usable before the publication archive
        # is built; the end-to-end archive job checks the manifest strictly.
        return
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["status"] == "RH-372_fixed_publication_manifest"
    assert manifest["publication_file_count"] == 21
    assert manifest["external_input_count"] == 9
    for relative, expected in manifest["publication_artifacts"].items():
        assert build_archive.digest(ROOT / relative) == expected
    for relative, expected in manifest["external_inputs"].items():
        assert build_archive.digest(build_archive.WORKSPACE / relative) == expected


def test_verification_report_is_clean_when_archive_exists() -> None:
    if not VERIFICATION.is_file():
        return
    report = json.loads(VERIFICATION.read_text())
    assert report["status"] == "RH-372_archive_verified"
    assert report["failure_count"] == 0
    assert report["failures"] == []


def test_verifier_rejects_a_shortened_manifest_when_archive_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not MANIFEST.is_file():
        return
    manifest = json.loads(MANIFEST.read_text())
    removed = next(iter(manifest["publication_artifacts"]))
    manifest["publication_artifacts"].pop(removed)
    manifest["publication_file_count"] -= 1
    manifest_path = tmp_path / "dependency_manifest.json"
    report_path = tmp_path / "archive_verification.json"
    manifest_path.write_text(json.dumps(manifest))
    monkeypatch.setattr(verify_archive, "MANIFEST", manifest_path)
    monkeypatch.setattr(verify_archive, "OUTPUT", report_path)
    with pytest.raises(SystemExit) as raised:
        verify_archive.main()
    assert raised.value.code == 1
    report = json.loads(report_path.read_text())
    assert report["status"] == "RH-372_archive_failed"
    assert "manifest:publication_membership_count" in report["failures"]
