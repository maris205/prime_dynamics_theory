from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "experiments") not in sys.path:
    sys.path.insert(0, str(ROOT / "experiments"))

import verify_offline_sources  # noqa: E402


def require(condition: object, message: str = "requirement failed") -> None:
    if condition is not True:
        raise RuntimeError(message)


def test_runtime_require_survives_optimized_mode() -> None:
    with pytest.raises(RuntimeError):
        require(False, "optimized sentinel")


def test_all_four_locks_verify_with_zero_requests() -> None:
    for source_key in verify_offline_sources.LOCKS:
        row = verify_offline_sources.verify_source(source_key)
        require(row["source_key"] == source_key)
        require(row["status"] == "NETWORK_DISABLED")
        require(row["network_opt_in"] is False)
        require(type(row["requests_made"]) is int and row["requests_made"] == 0)
        require(row["lock_verified_offline"] is True)


def test_cli_is_offline_and_strict() -> None:
    for source_key in verify_offline_sources.LOCKS:
        completed = subprocess.run(
            [sys.executable, "-B", "experiments/verify_offline_sources.py", "--source", source_key],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        require(completed.returncode == 0, completed.stderr)
        require(completed.stderr == "")
        payload = json.loads(completed.stdout)
        require(type(payload["requests_made"]) is int and payload["requests_made"] == 0)
        require(payload["network_opt_in"] is False)


def test_mutated_lock_and_unknown_source_fail_closed(tmp_path: Path) -> None:
    source_key = "tao-cambridge-2016-logarithmic-chowla"
    original = ROOT / verify_offline_sources.LOCKS[source_key]["path"]
    attacked = tmp_path / "lock.json"
    attacked.write_bytes(original.read_bytes() + b"\n")
    with pytest.raises(verify_offline_sources.OfflineSourceError):
        verify_offline_sources.verify_source(source_key, path=attacked)
    with pytest.raises(verify_offline_sources.OfflineSourceError):
        verify_offline_sources.verify_source("unknown")


def test_symlinked_lock_is_rejected(tmp_path: Path) -> None:
    source_key = "tao-cambridge-2016-logarithmic-chowla"
    original = ROOT / verify_offline_sources.LOCKS[source_key]["path"]
    link = tmp_path / "lock.json"
    link.symlink_to(original)
    with pytest.raises(verify_offline_sources.OfflineSourceError):
        verify_offline_sources.verify_source(source_key, path=link)


def test_no_network_implementation_is_exposed() -> None:
    require(not hasattr(verify_offline_sources, "urlopen"))
    require(not hasattr(verify_offline_sources, "Request"))


def test_test_module_has_no_bare_asserts() -> None:
    tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)))
