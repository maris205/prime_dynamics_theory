import copy
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments import build_archive, verify_archive  # noqa: E402


def test_archive_membership_contract() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 28
    assert len(set(build_archive.LOCAL_MEMBERS)) == 28
    assert len(build_archive.SOURCE_FILES) == 25
    assert len(set(build_archive.SOURCE_FILES)) == 25
    for member in (*build_archive.LOCAL_MEMBERS, *build_archive.SOURCE_FILES):
        path = Path(member)
        assert not path.is_absolute()
        assert ".." not in path.parts


def test_archive_json_loaders_reject_nonstandard_constants(tmp_path: Path) -> None:
    for token in ("NaN", "Infinity", "-Infinity"):
        candidate = tmp_path / f"candidate-{token.replace('-', 'minus-')}.json"
        candidate.write_text('{"value":' + token + "}")
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            build_archive.load_json(candidate)
        with pytest.raises(ValueError, match="non-finite JSON constant"):
            verify_archive.load_json(candidate)


def test_archive_source_lock_rows_fail_closed() -> None:
    result = build_archive.load_json(ROOT / "results/result.json")
    assert len(build_archive.validated_result_source_map(result)) == 25

    duplicate = copy.deepcopy(result)
    duplicate["source_locks"]["entries"].append(
        copy.deepcopy(duplicate["source_locks"]["entries"][0])
    )
    with pytest.raises(RuntimeError, match="frozen 25 rows"):
        build_archive.validated_result_source_map(duplicate)

    rebound_group = copy.deepcopy(result)
    rebound_group["source_locks"]["entries"][0]["group"] = "rh379_release"
    with pytest.raises(RuntimeError, match="differs from fresh release locks"):
        build_archive.validated_result_source_map(rebound_group)

    rebound_commit = copy.deepcopy(result)
    rebound_commit["source_locks"]["entries"][0]["commit"] = "0" * 40
    with pytest.raises(RuntimeError, match="differs from fresh release locks"):
        build_archive.validated_result_source_map(rebound_commit)


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
    assert stored_report["status"] == "RH-381_archive_verified"
    assert stored_report["failure_count"] == 0
    assert stored_report["publication_file_count"] == 28
    assert stored_report["external_input_count"] == 25
    assert stored_report["manifest_rebuild_match"]
    assert stored_report["result_source_lock_match"]
    assert stored_report["release_blob_identity_pass"]
    assert stored_report["source_digest_contract_pass"]
    assert stored_report["independent_interval_digest_pass"]
    assert stored_report["semantic_pdf_match"]
