from __future__ import annotations

from collections import deque
from email.message import Message
from io import BytesIO
import json
from pathlib import Path
import subprocess
import sys
import tarfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import verify_remote_source as verifier  # noqa: E402
from vk_prime_tail.core import remote_source_lock  # noqa: E402


class FakeResponse:
    def __init__(
        self,
        body: bytes,
        *,
        url: str,
        status: int = 200,
        content_type: str = "application/pdf",
    ) -> None:
        self._body = body
        self._url = url
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        self.closed = False

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self._url

    def read(self, _limit: int = -1) -> bytes:
        return self._body

    def close(self) -> None:
        self.closed = True


class QueueOpener:
    def __init__(self, *responses: FakeResponse) -> None:
        self.responses = deque(responses)
        self.requests: list[tuple[str, int]] = []

    def __call__(self, request: object, *, timeout: int) -> FakeResponse:
        self.requests.append((request.full_url, timeout))  # type: ignore[attr-defined]
        if not self.responses:
            raise AssertionError("unexpected network request")
        return self.responses.popleft()


class FakeHash:
    def __init__(self, digest: str) -> None:
        self.digest = digest

    def hexdigest(self) -> str:
        return self.digest


def _hash_sequence(monkeypatch: pytest.MonkeyPatch, *digests: str) -> None:
    remaining = deque(digests)

    def fake_sha256(_data: bytes) -> FakeHash:
        if not remaining:
            raise AssertionError("unexpected SHA-256 call")
        return FakeHash(remaining.popleft())

    monkeypatch.setattr(verifier, "sha256", fake_sha256)


def _tar_bytes(rows: list[tuple[str, bytes]]) -> bytes:
    stream = BytesIO()
    with tarfile.open(fileobj=stream, mode="w:gz") as archive:
        for name, data in rows:
            member = tarfile.TarInfo(name)
            member.size = len(data)
            archive.addfile(member, BytesIO(data))
    return stream.getvalue()


def test_default_cli_is_offline_and_accepts_posix_path() -> None:
    completed = subprocess.run(
        [sys.executable, "-B", str(ROOT / "experiments" / "verify_remote_source.py")],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": str(ROOT / "src")},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0
    assert completed.stderr == ""
    assert json.loads(completed.stdout) == {
        "lock_verified_offline": True,
        "network_opt_in": False,
        "requests_made": 0,
        "status": "NETWORK_DISABLED",
    }


def test_default_api_never_calls_opener() -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network was touched without opt in")

    result = verifier.verify_remote_source(remote_source_lock(), network=False, opener=forbidden)
    assert result["status"] == "NETWORK_DISABLED"
    assert result["requests_made"] == 0


def test_lock_and_direct_versioned_source_url_are_exact() -> None:
    lock = verifier._load_lock(ROOT / "results" / "external_source_lock.json")
    assert lock == remote_source_lock()
    assert lock["source_tar_url"] == "https://arxiv.org/src/2204.01980v2"
    assert lock["source_tar_final_url"] == lock["source_tar_url"]
    assert lock["source_tar_vendored"] is False
    assert lock["redistributable_in_release"] is False


@pytest.mark.parametrize(
    "url",
    [
        "https://arxiv.org/pdf/2204.01980",
        "https://arxiv.org/pdf/2204.01980v1",
        "https://arxiv.org/pdf/2204.01980latest",
    ],
)
def test_latest_unversioned_and_wrong_version_urls_are_rejected(url: str) -> None:
    with pytest.raises(verifier.RemoteVerificationError, match="unversioned"):
        verifier._fetch_exact(url, url, 1, opener=lambda *_args, **_kwargs: None)


def test_transport_and_http_failures_are_closed() -> None:
    lock = remote_source_lock()

    def transport_failure(*_args: object, **_kwargs: object) -> object:
        raise OSError("offline")

    with pytest.raises(verifier.RemoteVerificationError, match="network request failed"):
        verifier._fetch_exact(lock["versioned_url"], lock["versioned_url"], 1, opener=transport_failure)

    response = FakeResponse(b"x", url=lock["versioned_url"], status=503)
    with pytest.raises(verifier.RemoteVerificationError, match="HTTP status"):
        verifier._fetch_exact(lock["versioned_url"], lock["versioned_url"], 1, opener=QueueOpener(response))


def test_redirect_mime_and_byte_count_attacks_are_rejected() -> None:
    lock = remote_source_lock()
    redirected = FakeResponse(b"x", url="https://example.invalid/2204.01980v2")
    with pytest.raises(verifier.RemoteVerificationError, match="redirect/final URL"):
        verifier._fetch_exact(lock["versioned_url"], lock["versioned_url"], 1, opener=QueueOpener(redirected))

    short = FakeResponse(b"x", url=lock["versioned_url"])
    with pytest.raises(verifier.RemoteVerificationError, match="byte count"):
        verifier._fetch_exact(lock["versioned_url"], lock["versioned_url"], 2, opener=QueueOpener(short))

    wrong_mime = FakeResponse(
        b"x" * lock["bytes"],
        url=lock["versioned_url"],
        content_type="text/html",
    )
    with pytest.raises(verifier.RemoteVerificationError, match="PDF MIME"):
        verifier.verify_remote_source(lock, network=True, opener=QueueOpener(wrong_mime))


def test_pdf_sha_and_page_count_attacks_are_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    lock = remote_source_lock()
    pdf = FakeResponse(b"x" * lock["bytes"], url=lock["versioned_url"])
    with pytest.raises(verifier.RemoteVerificationError, match="PDF SHA-256"):
        verifier.verify_remote_source(lock, network=True, opener=QueueOpener(pdf))

    _hash_sequence(monkeypatch, lock["sha256"])
    pdf = FakeResponse(b"x" * lock["bytes"], url=lock["versioned_url"])
    with pytest.raises(verifier.RemoteVerificationError, match="page count"):
        verifier.verify_remote_source(
            lock,
            network=True,
            opener=QueueOpener(pdf),
            page_counter=lambda _data: 21,
        )


def test_source_tar_sha_and_main_hash_attacks_are_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    lock = remote_source_lock()
    pdf_data = b"p" * lock["bytes"]
    tar_data = b"t" * lock["source_tar_bytes"]
    pdf = FakeResponse(pdf_data, url=lock["versioned_url"])
    source = FakeResponse(tar_data, url=lock["source_tar_url"], content_type="application/gzip")
    _hash_sequence(monkeypatch, lock["sha256"], "0" * 64)
    with pytest.raises(verifier.RemoteVerificationError, match="source tar SHA-256"):
        verifier.verify_remote_source(
            lock,
            network=True,
            opener=QueueOpener(pdf, source),
            page_counter=lambda _data: 22,
        )

    pdf = FakeResponse(pdf_data, url=lock["versioned_url"])
    source = FakeResponse(tar_data, url=lock["source_tar_url"], content_type="application/gzip")
    _hash_sequence(monkeypatch, lock["sha256"], lock["source_tar_sha256"])
    monkeypatch.setattr(verifier, "_source_main_sha", lambda _data: ("0" * 64, 1))
    with pytest.raises(verifier.RemoteVerificationError, match="main.tex SHA-256"):
        verifier.verify_remote_source(
            lock,
            network=True,
            opener=QueueOpener(pdf, source),
            page_counter=lambda _data: 22,
        )


def test_tar_reader_rejects_unsafe_missing_and_duplicate_main() -> None:
    for data in (
        _tar_bytes([("../main.tex", b"x")]),
        _tar_bytes([("paper.tex", b"x")]),
        _tar_bytes([("main.tex", b"x"), ("./main.tex", b"y")]),
    ):
        with pytest.raises(verifier.RemoteVerificationError):
            verifier._source_main_sha(data)


def test_full_network_path_can_be_replayed_with_exact_oracles(monkeypatch: pytest.MonkeyPatch) -> None:
    lock = remote_source_lock()
    pdf_data = b"p" * lock["bytes"]
    tar_data = b"t" * lock["source_tar_bytes"]
    pdf = FakeResponse(pdf_data, url=lock["versioned_url"])
    source = FakeResponse(tar_data, url=lock["source_tar_url"], content_type="application/gzip")
    opener = QueueOpener(pdf, source)
    _hash_sequence(monkeypatch, lock["sha256"], lock["source_tar_sha256"])
    monkeypatch.setattr(
        verifier,
        "_source_main_sha",
        lambda _data: (lock["source_main_tex_sha256"], 57_970),
    )
    result = verifier.verify_remote_source(
        lock,
        network=True,
        opener=opener,
        page_counter=lambda _data: 22,
    )
    assert result["status"] == "PASS"
    assert result["requests_made"] == 2
    assert result["downloaded_source_vendored"] is False
    assert opener.requests == [
        (lock["versioned_url"], 60),
        (lock["source_tar_url"], 60),
    ]


def test_non_boolean_network_and_rebound_lock_are_rejected() -> None:
    lock = remote_source_lock()
    with pytest.raises(TypeError):
        verifier.verify_remote_source(lock, network=1)  # type: ignore[arg-type]
    lock["versioned_url"] = "https://arxiv.org/pdf/2204.01980"
    with pytest.raises(verifier.RemoteVerificationError, match="sealed core contract"):
        verifier.verify_remote_source(lock, network=False)
