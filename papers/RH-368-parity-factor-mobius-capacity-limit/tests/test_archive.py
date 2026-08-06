from __future__ import annotations

from experiments import build_archive


def test_archive_verification_is_zero_failure() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 21
    assert len(build_archive.EXTERNAL_INPUTS) == 11
    assert all(".." not in member.split("/") for member in build_archive.LOCAL_MEMBERS)
    assert all(".." not in member.split("/") for member in build_archive.EXTERNAL_INPUTS)
