import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from experiments import build_archive, verify_archive  # noqa: E402


def test_archive_membership_contract() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 28
    assert len(set(build_archive.LOCAL_MEMBERS)) == 28
    assert len(build_archive.SOURCE_FILES) == 28
    assert len(set(build_archive.SOURCE_FILES)) == 28
    for member in (*build_archive.LOCAL_MEMBERS, *build_archive.SOURCE_FILES):
        path = Path(member)
        assert not path.is_absolute()
        assert ".." not in path.parts


def test_archive_full_regeneration_if_present() -> None:
    manifest_path = ROOT / "results" / "dependency_manifest.json"
    report_path = ROOT / "results" / "archive_verification.json"
    if not manifest_path.is_file() and not report_path.is_file():
        return
    assert manifest_path.is_file() and report_path.is_file()
    manifest = verify_archive.load_json(manifest_path)
    assert manifest == build_archive.build_payload()
    regenerated_report = verify_archive.verify_manifest(manifest)
    stored_report = json.loads(report_path.read_text())
    assert regenerated_report == stored_report
    assert stored_report["status"] == "RH-379_archive_verified"
    assert stored_report["failure_count"] == 0
    assert stored_report["publication_file_count"] == 28
    assert stored_report["external_input_count"] == 28
    assert stored_report["manifest_rebuild_match"]
    assert stored_report["result_source_lock_match"]
    assert stored_report["semantic_pdf_match"]
