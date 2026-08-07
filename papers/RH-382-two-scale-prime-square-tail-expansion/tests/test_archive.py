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
    assert len(build_archive.SOURCE_FILES) == len(set(build_archive.SOURCE_FILES)) == 33
    for member in (*build_archive.LOCAL_MEMBERS, *build_archive.SOURCE_FILES):
        path = Path(member)
        assert not path.is_absolute() and ".." not in path.parts


def test_archive_json_loaders_reject_duplicate_nonstandard_and_nonobject(tmp_path: Path) -> None:
    values = (
        '{"x":1,"x":2}',
        '{"value":NaN}',
        '{"value":Infinity}',
        '{"value":-Infinity}',
        "[]",
    )
    for index, text in enumerate(values):
        candidate = tmp_path / f"candidate-{index}.json"
        candidate.write_text(text)
        with pytest.raises(ValueError):
            build_archive.load_json(candidate)
        with pytest.raises(ValueError):
            verify_archive.load_json(candidate)


def test_archive_source_lock_rows_fail_closed() -> None:
    result = build_archive.load_json(ROOT / "results/result.json")
    assert len(build_archive.validated_result_source_map(result)) == 33

    duplicate = copy.deepcopy(result)
    duplicate["source_locks"]["entries"].append(copy.deepcopy(duplicate["source_locks"]["entries"][0]))
    with pytest.raises(RuntimeError, match="frozen 33 rows"):
        build_archive.validated_result_source_map(duplicate)

    duplicate_path = copy.deepcopy(result)
    duplicate_path["source_locks"]["entries"][-1]["path"] = duplicate_path["source_locks"]["entries"][0]["path"]
    with pytest.raises(RuntimeError, match="unique set"):
        build_archive.validated_result_source_map(duplicate_path)

    for key, value in (("group", "rh379_release"), ("commit", "0" * 40), ("sha256", "0" * 64)):
        rebound = copy.deepcopy(result)
        rebound["source_locks"]["entries"][0][key] = value
        with pytest.raises(RuntimeError, match="differs from fresh release locks"):
            build_archive.validated_result_source_map(rebound)

    boolean_count = copy.deepcopy(result)
    boolean_count["source_locks"]["count"] = True
    with pytest.raises(RuntimeError, match="exact integer 33"):
        build_archive.validated_result_source_map(boolean_count)


def test_mutable_and_escaping_source_paths_fail_closed() -> None:
    for bad in (
        "prime_dynamics_theory/AGENTS.md",
        "prime_dynamics_theory/RH_HANDOFF.md",
        "prime_dynamics_theory/../RH_HANDOFF.md",
        "/root/math/prime_dynamics_theory/RH_HANDOFF.md",
        "other_repository/input.json",
    ):
        with pytest.raises(ValueError):
            _safe_source_path(bad)


def test_manifest_verifier_rejects_membership_commit_and_boolean_alias_mutations() -> None:
    manifest_path = ROOT / "results/dependency_manifest.json"
    if not manifest_path.is_file():
        return
    manifest = build_archive.load_json(manifest_path)
    cases = []
    missing_local = copy.deepcopy(manifest)
    missing_local["publication_artifacts"].pop(next(iter(missing_local["publication_artifacts"])))
    cases.append(missing_local)
    rebound_commit = copy.deepcopy(manifest)
    rebound_commit["source_commits"]["rh381_release"] = "0" * 40
    cases.append(rebound_commit)
    boolean_count = copy.deepcopy(manifest)
    boolean_count["publication_file_count"] = True
    cases.append(boolean_count)
    for candidate in cases:
        report = verify_archive.verify_manifest(candidate)
        assert report["failure_count"] > 0
        assert report["status"] == "RH-382_archive_failed"


def test_archive_full_regeneration_if_present() -> None:
    manifest_path = ROOT / "results/dependency_manifest.json"
    report_path = ROOT / "results/archive_verification.json"
    if not manifest_path.is_file() and not report_path.is_file():
        return
    assert manifest_path.is_file() and report_path.is_file()
    manifest = verify_archive.load_json(manifest_path)
    assert manifest == build_archive.build_payload()
    regenerated_report = verify_archive.verify_manifest(manifest)
    stored_report = json.loads(report_path.read_text())
    assert regenerated_report == stored_report
    assert stored_report["status"] == "RH-382_archive_verified"
    assert stored_report["failure_count"] == 0
    assert stored_report["publication_file_count"] == 29
    assert stored_report["external_input_count"] == 33
    assert stored_report["manifest_rebuild_match"]
    assert stored_report["result_source_lock_match"]
    assert stored_report["release_blob_identity_pass"]
    assert stored_report["source_digest_contract_pass"]
    assert stored_report["exact_certificate_digest_pass"]
    assert stored_report["semantic_pdf_match"]
