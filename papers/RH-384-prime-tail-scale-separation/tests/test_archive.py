"""Publication-manifest and archive mutation tests for RH-384."""

import copy
import json
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments import build_archive, verify_archive  # noqa: E402
from experiments.build_result import _safe_source_path  # noqa: E402


def test_archive_membership_contract() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == len(set(build_archive.LOCAL_MEMBERS)) == 29
    assert len(build_archive.SOURCE_FILES) == len(set(build_archive.SOURCE_FILES)) == 51
    for member in (*build_archive.LOCAL_MEMBERS, *build_archive.SOURCE_FILES):
        path = Path(member)
        assert not path.is_absolute() and ".." not in path.parts


def test_archive_json_loaders_reject_duplicate_nonstandard_and_nonobject(tmp_path: Path) -> None:
    for index, text in enumerate(('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', "[]")):
        candidate = tmp_path / f"candidate-{index}.json"
        candidate.write_text(text)
        with pytest.raises(ValueError):
            build_archive.load_json(candidate)
        with pytest.raises(ValueError):
            verify_archive.load_json(candidate)


def test_archive_source_lock_rows_fail_closed() -> None:
    result = build_archive.load_json(ROOT / "results/result.json")
    assert len(build_archive.validated_result_source_map(result)) == 51
    duplicate = copy.deepcopy(result)
    duplicate["source_locks"]["entries"].append(copy.deepcopy(duplicate["source_locks"]["entries"][0]))
    with pytest.raises(RuntimeError, match="frozen 51 rows"):
        build_archive.validated_result_source_map(duplicate)
    rebound = copy.deepcopy(result)
    rebound["source_locks"]["entries"][0]["sha256"] = "0" * 64
    with pytest.raises(RuntimeError, match="differs from fresh release locks"):
        build_archive.validated_result_source_map(rebound)
    boolean_count = copy.deepcopy(result)
    boolean_count["source_locks"]["count"] = True
    with pytest.raises(RuntimeError, match="exact integer 51"):
        build_archive.validated_result_source_map(boolean_count)


def test_mutable_and_escaping_source_paths_fail_closed() -> None:
    for bad in (
        "prime_dynamics_theory/AGENTS.md", "prime_dynamics_theory/RH_HANDOFF.md",
        "prime_dynamics_theory/../RH_HANDOFF.md", "/root/math/RH_HANDOFF.md", "other/input.json",
    ):
        with pytest.raises(ValueError):
            _safe_source_path(bad)


def test_manifest_verifier_rejects_mutations_if_present() -> None:
    path = ROOT / "results/dependency_manifest.json"
    if not path.is_file():
        return
    manifest = build_archive.load_json(path)
    cases = []
    missing = copy.deepcopy(manifest)
    missing["publication_artifacts"].pop(next(iter(missing["publication_artifacts"])))
    cases.append(missing)
    commit = copy.deepcopy(manifest)
    commit["source_commits"]["rh383_release"] = "0" * 40
    cases.append(commit)
    count = copy.deepcopy(manifest)
    count["publication_file_count"] = True
    cases.append(count)
    semantic = copy.deepcopy(manifest)
    semantic["publication_artifacts"]["prime-tail-scale-separation.pdf"] = "0" * 64
    cases.append(semantic)
    for candidate in cases:
        report = verify_archive.verify_manifest(candidate)
        assert report["failure_count"] > 0 and report["status"] == "RH-384_archive_failed"


def test_archive_full_regeneration_if_present() -> None:
    manifest_path = ROOT / "results/dependency_manifest.json"
    report_path = ROOT / "results/archive_verification.json"
    if not manifest_path.is_file() and not report_path.is_file():
        return
    assert manifest_path.is_file() and report_path.is_file()
    manifest = verify_archive.load_json(manifest_path)
    assert manifest == build_archive.build_payload()
    regenerated = verify_archive.verify_manifest(manifest)
    stored = json.loads(report_path.read_text())
    assert regenerated == stored
    assert stored["status"] == "RH-384_archive_verified"
    assert stored["failure_count"] == 0
    assert stored["publication_file_count"] == 29
    assert stored["external_input_count"] == 51
    assert all(stored[key] for key in (
        "manifest_rebuild_match", "result_source_lock_match", "release_blob_identity_pass",
        "source_digest_contract_pass", "exact_certificate_digest_pass", "semantic_pdf_match",
    ))
