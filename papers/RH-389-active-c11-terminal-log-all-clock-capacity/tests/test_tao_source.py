from __future__ import annotations

from collections import deque
from email.message import Message
import json
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

import verify_tao_source as verifier  # noqa: E402


class FakeResponse:
    def __init__(self, body: bytes, *, url: str, status: int = 200, content_type: str = "application/pdf") -> None:
        self._body = body
        self._offset = 0
        self._url = url
        self.status = status
        self.headers = Message()
        self.headers["Content-Type"] = content_type

    def getcode(self) -> int:
        return self.status

    def geturl(self) -> str:
        return self._url

    def read(self, limit: int = -1) -> bytes:
        if limit < 0:
            limit = len(self._body) - self._offset
        start = self._offset
        stop = min(len(self._body), start + limit)
        self._offset = stop
        return self._body[start:stop]

    def close(self) -> None:
        return None


class QueueOpener:
    def __init__(self, *responses: FakeResponse) -> None:
        self.responses = deque(responses)
        self.requests: list[tuple[str, int]] = []

    def __call__(self, request: object, *, timeout: int) -> FakeResponse:
        self.requests.append((request.full_url, timeout))  # type: ignore[attr-defined]
        if not self.responses:
            raise AssertionError("unexpected network request")
        return self.responses.popleft()


def test_default_cli_is_offline() -> None:
    completed = subprocess.run(
        [sys.executable, "-B", str(ROOT / "experiments" / "verify_tao_source.py")],
        cwd=ROOT,
        env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"},
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert completed.returncode == 0
    assert completed.stderr == ""
    result = json.loads(completed.stdout)
    assert result == {
        "lock_canonical_sha256": verifier.lock_canonical_sha256(verifier.tao_source_lock()),
        "lock_verified_offline": True,
        "network_opt_in": False,
        "requests_made": 0,
        "status": "NETWORK_DISABLED",
    }


def test_default_api_makes_zero_requests() -> None:
    def forbidden(*_args: object, **_kwargs: object) -> object:
        raise AssertionError("network was touched without explicit opt in")

    result = verifier.verify_remote_source(verifier.tao_source_lock(), network=False, opener=forbidden)
    assert result["requests_made"] == 0
    assert result["status"] == "NETWORK_DISABLED"


def test_stored_lock_is_exact_canonical_and_no_newline() -> None:
    lock = verifier._load_lock(ROOT / "results" / "tao_external_source_lock.json")
    assert verifier.exact_equal(lock, verifier.tao_source_lock())
    canonical = verifier.canonical_json_bytes(lock)
    assert not canonical.endswith(b"\n")
    assert len(canonical) == 2952
    assert verifier.lock_canonical_sha256(lock) == "d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84"


def test_locator_domain_typo_and_license_are_exact() -> None:
    lock = verifier.tao_source_lock()
    locator = lock["locators"][0]
    assert locator["label"] == "Theorem 2"
    assert locator["equation"] == "(3)"
    assert locator["pdf_page"] == locator["printed_page"] == 3
    for token in ("natural a1,a2", "integer b1,b2", "a1*b2-a2*b1!=0", "1<=omega(x)<=x", "omega(x)->infinity", "x->infinity"):
        assert token in locator["statement"]
    assert lock["known_source_typos"] == [{
        "location": "immediately after Theorem 2, equation (3), printed/PDF page 3",
        "printed_text": "as n tends to infinity",
        "resolution": "read as x tends to infinity, consistently with the theorem variable, abstract, and surrounding context",
        "scope": "typographical only; no mathematical strengthening or changed hypothesis",
    }]
    assert lock["license"]["published_version_cc_by"] is True
    assert lock["license"]["license_url"] == "https://creativecommons.org/licenses/by/4.0/"
    assert lock["redistributable_in_release"] is True
    assert lock["pdf_vendored"] is False


def test_non_boolean_network_and_semantic_rebinding_are_rejected() -> None:
    lock = verifier.tao_source_lock()
    for value in (0, 1, "false", None):
        with pytest.raises(TypeError, match="exact Boolean"):
            verifier.verify_remote_source(lock, network=value)  # type: ignore[arg-type]
    attacks = (
        ("doi", "10.0/wrong"),
        ("bytes", 534085),
        ("pages", 35),
        ("redistributable_in_release", False),
        ("pdf_vendored", True),
        ("source_key", "latest"),
    )
    for key, value in attacks:
        candidate = json.loads(json.dumps(lock))
        candidate[key] = value
        with pytest.raises(verifier.RemoteVerificationError, match="semantic contract"):
            verifier.verify_remote_source(candidate, network=False)
    candidate = json.loads(json.dumps(lock))
    candidate["unexpected"] = 1
    with pytest.raises(verifier.RemoteVerificationError, match="semantic contract"):
        verifier.verify_remote_source(candidate, network=False)


def test_locator_license_and_typo_rebinding_are_rejected() -> None:
    lock = verifier.tao_source_lock()
    attacks = (
        ("locators", 0, "statement", "weaker"),
        ("known_source_typos", 0, "resolution", "ignore"),
    )
    for group, index, key, value in attacks:
        candidate = json.loads(json.dumps(lock))
        candidate[group][index][key] = value
        with pytest.raises(verifier.RemoteVerificationError, match="semantic contract"):
            verifier.verify_remote_source(candidate, network=False)
    candidate = json.loads(json.dumps(lock))
    candidate["license"]["published_version_cc_by"] = False
    with pytest.raises(verifier.RemoteVerificationError, match="semantic contract"):
        verifier.verify_remote_source(candidate, network=False)


def test_transport_status_redirect_mime_and_length_fail_closed() -> None:
    lock = verifier.tao_source_lock()

    def transport_failure(*_args: object, **_kwargs: object) -> object:
        raise OSError("offline")

    with pytest.raises(verifier.RemoteVerificationError, match="network request failed"):
        verifier.verify_remote_source(lock, network=True, opener=transport_failure)
    cases = (
        (FakeResponse(b"x" * lock["bytes"], url=lock["pdf_url"], status=503), "HTTP status"),
        (FakeResponse(b"x" * lock["bytes"], url="https://example.invalid/source.pdf"), "redirect/final URL"),
        (FakeResponse(b"x" * lock["bytes"], url=lock["pdf_url"], content_type="text/html"), "PDF MIME"),
        (FakeResponse(b"x" * (lock["bytes"] - 1), url=lock["pdf_url"]), "byte count"),
        (FakeResponse(b"x" * (lock["bytes"] + 1), url=lock["pdf_url"]), "byte count"),
    )
    for response, message in cases:
        with pytest.raises(verifier.RemoteVerificationError, match=message):
            verifier.verify_remote_source(lock, network=True, opener=QueueOpener(response))


def test_sha_and_page_count_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    lock = verifier.tao_source_lock()
    body = b"x" * lock["bytes"]
    with pytest.raises(verifier.RemoteVerificationError, match="SHA-256"):
        verifier.verify_remote_source(lock, network=True, opener=QueueOpener(FakeResponse(body, url=lock["pdf_url"])))

    class FakeHash:
        def hexdigest(self) -> str:
            return lock["sha256"]

    monkeypatch.setattr(verifier, "sha256", lambda _data: FakeHash())
    with pytest.raises(verifier.RemoteVerificationError, match="page count"):
        verifier.verify_remote_source(
            lock,
            network=True,
            opener=QueueOpener(FakeResponse(body, url=lock["pdf_url"])),
            page_counter=lambda _data: 35,
        )


def test_fake_full_network_path_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    lock = verifier.tao_source_lock()
    body = b"x" * lock["bytes"]

    class FakeHash:
        def hexdigest(self) -> str:
            return lock["sha256"]

    monkeypatch.setattr(verifier, "sha256", lambda _data: FakeHash())
    opener = QueueOpener(FakeResponse(body, url=lock["pdf_url"]))
    result = verifier.verify_remote_source(lock, network=True, opener=opener, page_counter=lambda _data: 36)
    assert result["status"] == "PASS"
    assert result["requests_made"] == 1
    assert result["downloaded_source_vendored"] is False
    assert opener.requests == [(lock["pdf_url"], 60)]


@pytest.mark.parametrize("text", ["[]", "null", "1", '"x"', '{"a":NaN}', '{"a":1,"a":2}'])
def test_strict_json_and_nonobject_attacks_are_rejected(tmp_path: Path, text: str) -> None:
    path = tmp_path / "lock.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises((TypeError, ValueError, verifier.RemoteVerificationError)):
        verifier._load_lock(path)


def test_tao_pdf_is_not_present_in_publication_tree() -> None:
    lock = verifier.tao_source_lock()
    hits: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            if path.stat().st_size == lock["bytes"] and __import__("hashlib").sha256(path.read_bytes()).hexdigest() == lock["sha256"]:
                hits.append(path.relative_to(ROOT).as_posix())
        except OSError:
            continue
    assert hits == []
