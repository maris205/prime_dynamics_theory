"""Publication manifest and archive-verification tests for RH-385."""

from copy import deepcopy
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.build_archive import LOCAL_MEMBERS, build_payload  # noqa: E402
from experiments.build_result import _strict_load  # noqa: E402
from experiments.verify_archive import verify_manifest  # noqa: E402


def test_publication_manifest_regenerates_exactly() -> None:
    stored = _strict_load(ROOT / "results/dependency_manifest.json")
    assert stored == build_payload()
    assert stored["publication_file_count"] == len(LOCAL_MEMBERS) == 29
    assert stored["external_input_count"] == 67
    assert all(stored[key] is True for key in (
        "result_source_lock_match", "release_blob_identity_pass",
        "source_digest_contract_pass", "exact_certificate_digest_pass", "semantic_pdf_match",
    ))


def test_archive_verification_is_clean_and_rebuilds() -> None:
    manifest = _strict_load(ROOT / "results/dependency_manifest.json")
    verification = verify_manifest(manifest)
    assert verification["failure_count"] == 0
    assert verification["manifest_rebuild_match"] is True
    assert verification["publication_file_count"] == 29
    assert verification["external_input_count"] == 67


def test_manifest_hash_and_membership_mutations_fail() -> None:
    manifest = _strict_load(ROOT / "results/dependency_manifest.json")
    mutated = deepcopy(manifest)
    mutated["publication_artifacts"]["main.tex"] = "0" * 64
    assert verify_manifest(mutated)["failure_count"] > 0
    mutated = deepcopy(manifest)
    mutated["publication_artifacts"]["../RH_HANDOFF.md"] = "0" * 64
    mutated["publication_file_count"] += 1
    assert verify_manifest(mutated)["failure_count"] > 0
