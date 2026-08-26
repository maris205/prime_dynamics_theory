#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-269 finite transfer audit."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-269-growing-cutoff-profile-transfer"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_growing_cutoff_profile_transfer.md"
PRODUCER = PROJECT / "code/tpc269_growing_cutoff_profile_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc269_independent_checker.py"
STRESS = PROJECT / "experiments/tpc269_profile_stress.py"
CERTIFICATE = PROJECT / "results/tpc269_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "bc94e1727ff7d57aae67290eace41b485319a73e"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER"
BRIDGE_SHA256 = "139f07492d1d27d0f2feeb81626f37c9820ffa9c14065489eca77190bd8f1e9d"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "883b1793d3a72e0200b2d0339b4444b16f45de299a46a0a2ad563612e94ccc6c",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/README.md": "f1b02185dc8695aea90781984ef5eda53e2fd27aae21b6e07ab841bb2a2e87e8",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/PROOF_PACKAGE.md": "39146dba4c0147e7ffe6f18a02c9389544812806925526712fdd1dbecc5513bf",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/notes/theorem_ledger.md": "c0b014eaafd99208c0e3a393bf065afe4fcb66cc96b2a9bd0f4074e8ff5e3345",
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/notes/route_evaluation.md": "a17d377b3c9f5a363cdd045d0d3efb4b44dd6739d50179f688053c66b5781637",
    "research/tpc-big-road/bridge_b_finite_cutoff_sensitivity_obstruction.md": "6b4c7fe61bf9ef2d72c24aef60bf998e71738c856e9511b06bbceb33e6966851",
    "research/tpc-big-road/tpc_bridge_b_finite_cutoff_sensitivity_obstruction_checker.py": "3366574ed7b43f6745778c8c48935a4eeb11ef659a475bc5ba0e9c70d1c35170",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "14a2f40143c295b0cd45b104ff7f5c9281a4e91e56d99fbf26a3363facfa9446",
    "PAPER_PLAN.md": "dfd3b224ad0b3ffacf7340c1549b95543569c6a11844ec4bc0890eec75cbefda",
    "PROOF_PACKAGE.md": "4284ee1b1919851f3b7ab1f94b89cdbc8eadbcded7007c65c3aecb4767c56d1b",
    "README.md": "ed56f6403d1037c37a1ebe0960c515e6fef135d2c079ebb12e13b957099604df",
    "code/tpc269_growing_cutoff_profile_certificate.py": "4a173db746f13172c34845e37351fd003b253442aa983c95a7d695e0856d22c9",
    "experiments/tpc269_independent_checker.py": "2e45db78a00afbe14beb312e95c30c1d053a546745eb460fe1e61427d58cde9d",
    "experiments/tpc269_profile_stress.py": "9908749c7a03d5ec855c0aa6413cff2af3ac177e4b42e9b1662aefdb45b67b87",
    "notes/citation_verification.md": "7b95cb9bbd26ed8da579738e499cfc28af638d6ce71c09c8a08ea277691e117e",
    "notes/claim_firewall.md": "4446ea1c9ddbd0c2a98bf57055f838fae8fd2d99cd546b28c0837ad6f9f6b24f",
    "notes/computational_protocol.md": "d2dc9e828e108a081869617feadae83571693036c2845263fa5f11cecd928ce7",
    "notes/route_evaluation.md": "214d593ff8260186b47e50e4d62241cd863828451708b4d94222e8726012ab58",
    "notes/theorem_ledger.md": "45491ee91ae494044c48821f97781899fbeb3eaaf8f0192c80ffbbec5120cd08",
    "paper/main.pdf": "b6fbe8a59126e6b9e1a066759cf822fa902bbe4ee97f2b6a18407ee8631e9a4b",
    "paper/main.tex": "5289bccb1ae976558007eb9c7dbc3f3677955b1c4b300bcc0ae258f4fe5e675f",
    "paper/paper.pdf": "b6fbe8a59126e6b9e1a066759cf822fa902bbe4ee97f2b6a18407ee8631e9a4b",
    "paper/references.bib": "0418494fac8afa4ed74303e6397adbd4eec3dafb72739d2dd95b3e0ee77a860d",
    "results/tpc269_certificate.json": "67dcce57acbb025e2af4cfe7920e16e9db4f7fb4046fe6d397a8aa7573d052ac",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest_bytes(data: bytes) -> str:
    data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def frozen(path: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + path],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "missing frozen source: " + path)
    return result.stdout


def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected, "frozen source hash: " + path)


def check_project() -> None:
    actual = {
        str(path.relative_to(PROJECT))
        for path in PROJECT.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(digest(PROJECT / relative) == expected, "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    markers = (
        "TPC269_MAXIMUM_CLAIM = " + STATUS,
        "TPC269_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER",
        "TPC269_GROWING_CUTOFF_PROXY = NUMERICALLY_CERTIFIED_FINITE",
        "TPC269_PROFILE_MIXTURE_IDENTITY = PROVED_EXACT_FINITE",
        "TPC269_PROFILE_PATH_FLIP = NUMERICALLY_CERTIFIED_FINITE",
        "TPC269_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC",
        "TPC269_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC",
        "TPC269_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC",
        "TPC269_FIXED_POWER_CREDIT = 0",
        "TPC269_ARITHMETIC_ADVANCE = NO",
        "TPC269_L2 = NONE",
        "TPC269_FULL_GATE_B = OPEN",
        "TPC269_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC269_TWIN_PRIME_RESULT = NONE",
        "TPC269_STATUS = " + STATUS,
        "TPC269_ROUND2_CLUE = TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE",
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    need("theta=9/10" in text and "theta=24/25" in text,
         "bridge profile flip")


def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command, cwd=ROOT, env=environment, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == "",
         "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    pairs = (
        (child(PRODUCER, "TPC269_CERTIFICATE=PASS"),
         child(PRODUCER, "TPC269_CERTIFICATE=PASS", True)),
        (child(INDEPENDENT, "TPC269_INDEPENDENT_CHECK=PASS"),
         child(INDEPENDENT, "TPC269_INDEPENDENT_CHECK=PASS", True)),
        (child(STRESS, "TPC269_PROFILE_STRESS=PASS"),
         child(STRESS, "TPC269_PROFILE_STRESS=PASS", True)),
    )
    for normal, optimized in pairs:
        need(normal == optimized, "normal/optimized mismatch")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (
        json.dumps(parsed, ensure_ascii=True, sort_keys=True,
                   separators=(",", ":")) + "\n"
    ).encode("ascii")
    need(raw == canonical, "certificate is not canonical")
    need(parsed.get("certificate_version") == 1 and
         parsed.get("claim_status") == STATUS, "certificate header")
    payload = parsed.get("payload", {})
    need(payload.get("schema") ==
         "TPC269_GROWING_CUTOFF_PROFILE_TRANSFER_CERTIFICATE_V1",
         "certificate schema")
    payload_raw = (
        json.dumps(payload, ensure_ascii=True, sort_keys=True,
                   separators=(",", ":")) + "\n"
    ).encode("ascii")
    need(hashlib.sha256(payload_raw).hexdigest() == parsed.get("payload_sha256"),
         "payload digest")
    parameters = payload.get("parameters", {})
    need(parameters.get("registered_scales") == [64, 96, 128, 192, 256, 384],
         "registered scales")
    need(parameters.get("cutoff_rule") == "z_N=floor(log(N)) on registered rows",
         "cutoff rule")
    theorem = payload.get("finite_theorem", {})
    need(theorem.get("total_cases") == 12 and
         theorem.get("certified_contractions") == 8 and
         theorem.get("certified_obstructions") == 4,
         "theorem counts")
    need(theorem.get("universal_quarter_claim") ==
         "REFUTED_SCOPED_GROWING_PROXY_FAMILY", "theorem scope")
    need(theorem.get("matched_profile_flip") ==
         "9/10_OBSTRUCTION_TO_24/25_CONTRACTION", "profile flip ledger")
    cases = payload.get("cases", [])
    need(len(cases) == 12, "case count")
    need(sum(case.get("classification") == "CONTRACTION" for case in cases) == 8,
         "contraction count")
    need(sum(case.get("classification") == "OBSTRUCTION" for case in cases) == 4,
         "obstruction count")
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    for case in cases:
        scale = case.get("scale")
        need(scale in schedule and case.get("comparison_cutoff_z") == schedule[scale],
             "cutoff schedule")
        interval = case.get("rho_squared_interval", [])
        need(len(interval) == 2 and 0 < float(interval[0]) <= float(interval[1]),
             "rho interval")
        need(float(case.get("radius_squared_interval", [0])[0]) > 0 and
             case.get("exact_projection_identity") is True,
             "row identity")
        if case.get("classification") == "CONTRACTION":
            need(float(interval[1]) < 1 / 16 and
                 float(case.get("rho_upper", "1")) < 0.25 and
                 case.get("certified_obstruction") is False,
                 "contraction row")
        elif case.get("classification") == "OBSTRUCTION":
            need(float(interval[0]) > 1 / 16 and
                 float(case.get("rho_upper", "0")) > 0.25 and
                 case.get("certified_obstruction") is True,
                 "obstruction row")
        else:
            raise Failure("unresolved row")

    def find(scale: int, height: int, q0: int, theta: str) -> dict:
        matches = [case for case in cases if
                   (case.get("scale"), case.get("H"), case.get("Q"),
                    case.get("profile_theta")) == (scale, height, q0, theta)]
        need(len(matches) == 1, "central row missing: " + theta)
        return matches[0]

    need(find(64, 15, 4, "9/10")["classification"] == "OBSTRUCTION" and
         find(64, 15, 4, "24/25")["classification"] == "CONTRACTION" and
         find(64, 15, 4, "1/1")["classification"] == "CONTRACTION",
         "central profile flip")
    base = [case for case in cases if case.get("role") == "GROWING_CUTOFF_BASE"]
    need(len(base) == 6 and
         sum(case.get("classification") == "OBSTRUCTION" for case in base) == 2,
         "base rows")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC269_GROWING_CUTOFF_PROXY") ==
         "NUMERICALLY_CERTIFIED_FINITE" and
         firewall.get("TPC269_PROFILE_MIXTURE_IDENTITY") ==
         "PROVED_EXACT_FINITE" and
         firewall.get("TPC269_PROFILE_PATH_FLIP") ==
         "NUMERICALLY_CERTIFIED_FINITE" and
         firewall.get("TPC269_GROWING_UNIFORMITY") == "OPEN_ASYMPTOTIC" and
         firewall.get("TPC269_ACTUAL_V59_RADIUS") == "OPEN_ASYMPTOTIC" and
         firewall.get("TPC269_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC269_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC269_L2") == "NONE" and
         firewall.get("TPC269_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC269_TWIN_PRIME_RESULT") == "NONE",
         "firewall")
    need(payload.get("round2_clue") ==
         "TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE",
         "round-two clue")


def check_pdf() -> None:
    text = subprocess.run(
        ["pdftotext", "-layout", str(PDF), "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Growing-Cutoff", "Liang Wang", "profile path", "1/4",
                   "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(
        ["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(info.returncode == 0 and b"Pages:           4" in info.stdout,
         "PDF pages")
    fonts = subprocess.run(
        ["pdffonts", str(PDF)], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    rows = [row for row in fonts.stdout.decode("ascii", errors="replace").splitlines()[2:]
            if row.strip()]
    need(fonts.returncode == 0 and fonts.stderr == b"" and rows and
         all(row.split()[-5:-2] == ["yes", "yes", "yes"] for row in rows),
         "PDF fonts")
    if LOG.is_file():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        need("Warning:" not in log and "Overfull \\" not in log and
             "Underfull \\" not in log and "undefined references" not in log,
             "LaTeX log")


def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "assert syntax: " + path.name)
    need("tpc269_growing_cutoff_profile_certificate" not in
         INDEPENDENT.read_text(encoding="utf-8"), "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError,
            json.JSONDecodeError, StopIteration, ValueError) as exc:
        print("TPC269_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC269_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("finite_growing_cutoff_profile_transfer=NUMERICALLY_CERTIFIED")
    print("matched_profile_flip=YES")
    print("actual_v59_radius=OPEN_ASYMPTOTIC")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
