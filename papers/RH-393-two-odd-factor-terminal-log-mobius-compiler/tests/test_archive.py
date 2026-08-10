from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT, ROOT / "experiments", ROOT / "src"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from experiments import build_archive, build_result, build_schema, source_locks, verify_archive  # noqa: E402
from two_odd_compiler.core import exact_equal, loads_strict  # noqa: E402


def file_sha(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def test_manifest_is_exact_fresh_regeneration() -> None:
    stored_path = ROOT / "results" / "dependency_manifest.json"
    stored = loads_strict(stored_path.read_text(encoding="utf-8"))
    fresh = build_archive.build_payload()
    assert exact_equal(stored, fresh)
    assert stored_path.read_text(encoding="utf-8") == build_archive.serialized_payload(fresh)
    assert stored["publication_file_count"] == len(build_archive.LOCAL_MEMBERS) == 38
    assert stored["release_stage_file_count"] == 40
    assert stored["external_git_input_count"] == 117
    assert stored["remote_logical_input_count"] == 3
    assert stored["logical_input_total"] == 120
    assert stored["logical_source_digest"] == source_locks.EXPECTED_LOGICAL_SOURCE_DIGEST
    assert all(stored[key] is True for key in build_archive.BOOLEAN_KEYS)


def test_archive_report_is_exact_and_failure_free() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    fresh = verify_archive.verify_manifest(manifest)
    stored = loads_strict((ROOT / "results" / "archive_verification.json").read_text(encoding="utf-8"))
    assert exact_equal(stored, fresh)
    assert stored["status"] == "RH-393_archive_verified"
    assert stored["failure_count"] == 0
    assert stored["failures"] == []


def test_five_external_payloads_are_excluded_from_members_and_tree() -> None:
    members = set(build_archive.LOCAL_MEMBERS)
    assert len(build_archive.REMOTE_PAYLOAD_HASHES) == 5
    assert {item for item in members if item.endswith(".pdf")} == build_archive.PUBLICATION_PDFS
    member_hashes = {file_sha(ROOT / item) for item in members}
    tree_hashes = {
        file_sha(path) for path in ROOT.rglob("*") if path.is_file() and not path.is_symlink()
    }
    assert member_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES)
    assert tree_hashes.isdisjoint(build_archive.REMOTE_PAYLOAD_HASHES)
    assert build_archive.payload_hash_scan() == {
        "remote_payload_hash_count": 5,
        "publication_payload_hash_hit_count": 0,
        "tree_payload_hash_hit_count": 0,
    }
    assert build_archive.external_payload_exclusion() is True


def test_three_offline_remote_replays_make_zero_requests() -> None:
    rows = list(build_archive.offline_remote_replay())
    assert [row["source_key"] for row in rows] == list(build_archive.REMOTE_KEYS)
    assert all(row["status"] == "NETWORK_DISABLED" for row in rows)
    assert all(
        row["network_opt_in"] is False
        and type(row["requests_made"]) is int
        and row["requests_made"] == 0
        for row in rows
    )


def test_frozen_stage_digests_are_exact() -> None:
    assert len(build_archive.FROZEN_STAGE_DIGESTS) == 10
    assert all(
        file_sha(ROOT / path) == expected
        for path, expected in build_archive.FROZEN_STAGE_DIGESTS.items()
    )


def test_manifest_hash_membership_and_path_attacks_fail_closed() -> None:
    manifest = build_archive.build_payload()
    for relative in ("README.md",):
        attacked = deepcopy(manifest)
        attacked["publication_artifacts"][relative] = "0" * 64
        assert verify_archive.verify_manifest(attacked)["failure_count"] > 0
    for relative in ("unexpected.pdf", "../outside", "x" * 5000):
        attacked = deepcopy(manifest)
        attacked["publication_artifacts"][relative] = "0" * 64
        attacked["publication_file_count"] += 1
        report = verify_archive.verify_manifest(attacked)
        assert report["status"] == "RH-393_archive_failed"
        assert report["failure_count"] > 0


def test_manifest_nested_type_and_sha_attacks_fail_closed() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"] = []
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["external_git_inputs"] = None
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["publication_artifacts"]["README.md"] = True
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["extra"] = False
    attacks.append(attacked)
    for payload in attacks:
        assert verify_archive.verify_manifest(payload)["failure_count"] > 0


def test_remote_order_logical_offline_and_rights_attacks_fail() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    attacked = deepcopy(manifest)
    attacked["remote_source_lock_sha256"].reverse()
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["logical_source_digest"] = "0" * 64
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["offline_remote_replay"][2]["requests_made"] = 1
    attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["remote_rights_nonvendor_pass"] = False
    attacks.append(attacked)
    for payload in attacks:
        assert verify_archive.verify_manifest(payload)["failure_count"] > 0


def test_exact_integer_boolean_commit_and_hygiene_attacks_fail() -> None:
    manifest = build_archive.build_payload()
    attacks = []
    for key, value in (
        ("release_stage_file_count", True),
        ("remote_logical_input_count", True),
        ("logical_input_total", 108),
        ("tree_payload_hash_hit_count", 1),
        ("text_eof_defect_count", True),
        ("semantic_pdf_match", 1),
    ):
        attacked = deepcopy(manifest)
        attacked[key] = value
        attacks.append(attacked)
    attacked = deepcopy(manifest)
    attacked["source_commits"]["rh392_release"] = "0" * 40
    attacks.append(attacked)
    for payload in attacks:
        assert verify_archive.verify_manifest(payload)["failure_count"] > 0


@pytest.mark.parametrize("value", [[], None, 1, "not-an-object"])
def test_nonobject_manifest_has_standard_failure(value: object) -> None:
    report = verify_archive.verify_manifest(value)
    assert report["status"] == "RH-393_archive_failed"
    assert report["failure_count"] == 1
    assert report["failures"] == ["manifest:top_level_not_an_object"]
    assert report["release_stage_file_count"] == 0
    assert report["logical_input_total"] == 0
    assert all(report[key] is False for key in build_archive.BOOLEAN_KEYS)


def test_publication_pdfs_are_byte_identical() -> None:
    main_pdf = ROOT / "main.pdf"
    semantic = ROOT / build_archive.SEMANTIC_PDF
    assert main_pdf.read_bytes() == semantic.read_bytes()
    assert file_sha(main_pdf) == build_archive.FROZEN_STAGE_DIGESTS["main.pdf"]


def test_no_cache_symlink_sentinel_or_eof_defect() -> None:
    scan = build_archive.tree_hygiene_scan()
    assert scan == {
        "tree_symlink_count": 0,
        "cache_path_count": 0,
        "sentinel_path_count": 0,
        "sentinel_content_hit_count": 0,
        "text_eof_defect_count": 0,
    }
    assert all((ROOT / item).is_file() and not (ROOT / item).is_symlink() for item in build_archive.LOCAL_MEMBERS)


def test_symlink_member_attack_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.write_bytes(b"regular\n")
    link = tmp_path / "link"
    link.symlink_to(target)
    with pytest.raises(FileNotFoundError):
        build_archive.hash_map(tmp_path, ["link"])
    failures: list[str] = []
    assert verify_archive._verify_map(tmp_path, {"link": file_sha(target)}, "attack", failures) == 1
    assert failures == ["attack:link:missing_or_nonregular"]


def test_literal_sealing_sentinel_attack_is_detected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    probe = tmp_path / "probe.txt"
    probe.write_text("TO_" + "BE_" + "SEALED\n", encoding="utf-8")
    monkeypatch.setattr(build_archive, "ROOT", tmp_path)
    monkeypatch.setattr(build_archive, "LOCAL_MEMBERS", ("probe.txt",))
    scan = build_archive.tree_hygiene_scan()
    assert scan["sentinel_content_hit_count"] == 1


def test_normal_and_optimized_four_objects_are_fresh_exact() -> None:
    names = ("result.json", "result.schema.json", "dependency_manifest.json", "archive_verification.json")
    stored_hashes = [file_sha(ROOT / "results" / name) for name in names]
    code = """
import gc, hashlib, json, sys
sys.path[:0] = ['src', 'experiments', '.']
import build_result, build_schema, build_archive, verify_archive
def emit(value):
    raw = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\\n').encode()
    print(hashlib.sha256(raw).hexdigest(), flush=True)
value = build_result.build_payload(); emit(value); del value; gc.collect()
value = build_schema.build_schema(); emit(value); del value; gc.collect()
manifest = build_archive.build_payload(); emit(manifest)
value = verify_archive.verify_manifest(manifest); emit(value)
"""
    outputs: list[list[str]] = []
    inherited_pythonpath = os.environ.get("PYTHONPATH", "")
    subprocess_pythonpath = os.pathsep.join(
        part for part in ("src", "experiments", ".", inherited_pythonpath) if part
    )
    for optimized in (False, True):
        completed = subprocess.run(
            [sys.executable, *(["-OO"] if optimized else []), "-B", "-c", code],
            cwd=ROOT,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPATH": subprocess_pythonpath,
            },
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        assert completed.returncode == 0, completed.stderr
        outputs.append(completed.stdout.strip().splitlines())
    assert outputs == [stored_hashes, stored_hashes]


def test_official_schema_is_closed_and_accepts_result() -> None:
    jsonschema = pytest.importorskip("jsonschema")
    schema = loads_strict((ROOT / "results" / "result.schema.json").read_text(encoding="utf-8"))
    result = loads_strict((ROOT / "results" / "result.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(result)) == []


def test_outer_verifier_replays_without_writing() -> None:
    manifest = loads_strict((ROOT / "results" / "dependency_manifest.json").read_text(encoding="utf-8"))
    report = verify_archive.verify_manifest(manifest)
    assert report["status"] == "RH-393_archive_verified"
    assert report["failure_count"] == 0
    assert verify_archive.serialized_report(report) == (
        ROOT / "results" / "archive_verification.json"
    ).read_text(encoding="utf-8")
