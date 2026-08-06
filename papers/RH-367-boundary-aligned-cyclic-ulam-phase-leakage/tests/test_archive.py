from __future__ import annotations

import json
from pathlib import Path

from experiments import build_archive


ROOT = Path(__file__).resolve().parents[1]


def test_archive_replays_without_failures() -> None:
    assert len(build_archive.LOCAL_MEMBERS) == 21
    assert len(build_archive.EXTERNAL_INPUTS) == 23
    assert all(".." not in member.split("/") for member in build_archive.LOCAL_MEMBERS)
    assert all(".." not in member.split("/") for member in build_archive.EXTERNAL_INPUTS)
