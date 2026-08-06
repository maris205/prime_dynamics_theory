from __future__ import annotations

import copy
import json

import pytest

from experiments import verify_archive


def test_fixed_archive_replays_without_failures() -> None:
    payload = verify_archive.verification_payload()
    assert payload == {
        "status": "RH-366_archive_verified",
        "publication_file_count": 21,
        "external_input_count": 23,
        "failure_count": 0,
        "failures": [],
    }


def test_archive_rejects_membership_and_path_mutations(tmp_path, monkeypatch) -> None:
    manifest = verify_archive.strict_load(verify_archive.MANIFEST)
    missing = copy.deepcopy(manifest)
    missing["publication_artifacts"].pop("README.md")
    missing_path = tmp_path / "missing.json"
    missing_path.write_text(json.dumps(missing))
    monkeypatch.setattr(verify_archive, "MANIFEST", missing_path)
    with pytest.raises(RuntimeError, match="publication membership changed"):
        verify_archive.verification_payload()

    traversal = copy.deepcopy(manifest)
    value = traversal["publication_artifacts"].pop("README.md")
    traversal["publication_artifacts"]["../README.md"] = value
    traversal_path = tmp_path / "traversal.json"
    traversal_path.write_text(json.dumps(traversal))
    monkeypatch.setattr(verify_archive, "MANIFEST", traversal_path)
    with pytest.raises(RuntimeError, match="publication membership changed"):
        verify_archive.verification_payload()


def test_archive_rejects_source_commit_and_boolean_count(tmp_path, monkeypatch) -> None:
    manifest = verify_archive.strict_load(verify_archive.MANIFEST)
    commit = copy.deepcopy(manifest)
    commit["source_commits"]["henon_mobius_correlations"] = "0" * 40
    commit_path = tmp_path / "commit.json"
    commit_path.write_text(json.dumps(commit))
    monkeypatch.setattr(verify_archive, "MANIFEST", commit_path)
    with pytest.raises(RuntimeError, match="source commit lock changed"):
        verify_archive.verification_payload()

    boolean = copy.deepcopy(manifest)
    boolean["publication_file_count"] = True
    boolean_path = tmp_path / "boolean.json"
    boolean_path.write_text(json.dumps(boolean))
    monkeypatch.setattr(verify_archive, "MANIFEST", boolean_path)
    with pytest.raises(RuntimeError, match="not an integer"):
        verify_archive.verification_payload()
