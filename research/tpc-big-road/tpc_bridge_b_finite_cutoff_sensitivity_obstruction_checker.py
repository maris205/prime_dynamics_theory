#!/usr/bin/env python3
"""Fail-closed release checker for the TPC-268 finite obstruction."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_finite_cutoff_sensitivity_obstruction.md"
PRODUCER = PROJECT / "code/tpc268_cutoff_sensitivity_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc268_independent_checker.py"
STRESS = PROJECT / "experiments/tpc268_adversarial_stress.py"
CERTIFICATE = PROJECT / "results/tpc268_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
LOG = PROJECT / "paper/main.log"
BASELINE_HEAD = "1400b5e8224a1af5b1fcc4ba6d8502fbd9533888"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION"
BRIDGE_SHA256 = "6b4c7fe61bf9ef2d72c24aef60bf998e71738c856e9511b06bbceb33e6966851"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "38089faa9482cf69ddb3005d5a089574957f83f5091e5702517d9d2229d9197c",
    "papers/tpc-267-literal-v59-residual-radius-census/README.md": "6001b3d5db82ca844a049f6e1fb110d42e2f87a1b5e4f6da3d69cfab15c38bd1",
    "papers/tpc-267-literal-v59-residual-radius-census/PROOF_PACKAGE.md": "d62d8580ed1a886f8b57edb88e51179c04a4ef82c9e2133f30e6a30b5e6f67ce",
    "papers/tpc-267-literal-v59-residual-radius-census/notes/theorem_ledger.md": "6a73208a5f7249f2605499563c01dddf2a5b258a1f36b52696c690962f2b6c72",
    "papers/tpc-267-literal-v59-residual-radius-census/notes/route_evaluation.md": "0ca421f4c28d5e9e896c983b4390b51cb2faf7f4f13534f8d1bc99ad0db06e62",
    "research/tpc-big-road/bridge_b_literal_v59_residual_radius_census.md": "ab0287a0aa90f5272899fe513ddb3b11c71335c7d83fb4e990403be9adc51527",
    "research/tpc-big-road/tpc_bridge_b_literal_v59_residual_radius_census_checker.py": "41707b211d7251f84fc8285d776e8249748f921d947ef88735a67f8bfd04b7a2",
}

PROJECT_HASHES = {
    ".gitignore": "63712335348ea30c28eb573c62a401c9b98c8d427a28d6159b7a17fd4830c1d7",
    "DERIVATION_PACKAGE.md": "5f3af4afb86cd5803fae01fd5aee0e699a5795a208a77146087dca03a4ff93f0",
    "PAPER_PLAN.md": "0c988e5709274983270803a46f793a38ca1f11a97093d51ae1c00a85a93e4d3b",
    "PROOF_PACKAGE.md": "39146dba4c0147e7ffe6f18a02c9389544812806925526712fdd1dbecc5513bf",
    "README.md": "f1b02185dc8695aea90781984ef5eda53e2fd27aae21b6e07ab841bb2a2e87e8",
    "code/tpc268_cutoff_sensitivity_certificate.py": "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3",
    "experiments/tpc268_independent_checker.py": "3db32600b2bf04cd1edbc5d786c6c791c4ab0a91fc4f32401dcc2636a0807515",
    "experiments/tpc268_adversarial_stress.py": "3ed49026e728facfe8526d461fd5fa6840d98f623c3777a54242f0e36931e2fd",
    "notes/citation_verification.md": "7bf2750c1072d8445a46b1a81f092c04af7ccdb7e1c342c8f168c9c507546cdb",
    "notes/claim_firewall.md": "6ef86feda81650e680cb81cbe0d656f6c986694e7be454c5a245f959842d2284",
    "notes/computational_protocol.md": "5aef6fe6c931a64a9815dee8740e71fa24d98a3c40837acf1e2aabc6c7fb574b",
    "notes/route_evaluation.md": "a17d377b3c9f5a363cdd045d0d3efb4b44dd6739d50179f688053c66b5781637",
    "notes/theorem_ledger.md": "c0b014eaafd99208c0e3a393bf065afe4fcb66cc96b2a9bd0f4074e8ff5e3345",
    "paper/main.pdf": "99d2bc76d36629a3812b7a3c5673b7e7b7e303a4330489b79ea23f3c78550060",
    "paper/main.tex": "3852064cba5864cd53c94173bfd2e6440ddaae0b8e779d6f4a3dd834fd369f84",
    "paper/paper.pdf": "99d2bc76d36629a3812b7a3c5673b7e7b7e303a4330489b79ea23f3c78550060",
    "paper/references.bib": "353f730d19b87bee733ebe7f308cd219b3d21781a09e98d94e5c55f185d03333",
    "results/tpc268_certificate.json": "19b629425c4e64ec3e9638bb8e9f5baee304a7340d764fb32dfa2c31d49c907d",
}
EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {"paper/main.aux", "paper/main.bbl", "paper/main.blg",
                      "paper/main.log", "paper/main.out"}

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
    result = subprocess.run(["git", "show", BASELINE_HEAD + ":" + path],
                            cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, check=False)
    need(result.returncode == 0 and result.stderr == b"", "missing frozen source: " + path)
    return result.stdout

def check_sources() -> None:
    for path, expected in SOURCE_HASHES.items():
        need(digest_bytes(frozen(path)) == expected, "frozen source hash: " + path)

def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file() and "__pycache__" not in path.parts}
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
        "TPC268_MAXIMUM_CLAIM = " + STATUS,
        "TPC268_ROUTE_ADVANCE = YES_SCOPED_FINITE_CUTOFF_SENSITIVITY_OBSTRUCTION",
        "TPC268_FINITE_CUTOFF_OBSTRUCTION = NUMERICALLY_CERTIFIED",
        "TPC268_MATCHED_Z2_CONTROLS = NUMERICALLY_CERTIFIED",
        "TPC268_CLOCK_STABILITY = REFUTED_SCOPED",
        "TPC268_KERNEL_STABILITY = REFUTED_SCOPED",
        "TPC268_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC",
        "TPC268_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC",
        "TPC268_FIXED_POWER_CREDIT = 0",
        "TPC268_ARITHMETIC_ADVANCE = NO",
        "TPC268_L2 = NONE",
        "TPC268_FULL_GATE_B = OPEN",
        "TPC268_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
        "TPC268_TWIN_PRIME_RESULT = NONE",
        "TPC268_STATUS = " + STATUS,
    )
    for marker in markers:
        need(marker in text, "bridge marker: " + marker)
    need("TPC268_ROUND2_CLUE = TEST_GROWING_CUTOFF_UNIFORMITY_BEFORE_ANY_PHASE_PROMOTION" in text, "round-two clue")

def child(path: Path, marker: str, optimized: bool = False) -> str:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout

def check_children() -> None:
    pairs = (
        (child(PRODUCER, "TPC268_CERTIFICATE=PASS"), child(PRODUCER, "TPC268_CERTIFICATE=PASS", True)),
        (child(INDEPENDENT, "TPC268_INDEPENDENT_CHECK=PASS"), child(INDEPENDENT, "TPC268_INDEPENDENT_CHECK=PASS", True)),
        (child(STRESS, "TPC268_ADVERSARIAL_STRESS=PASS"), child(STRESS, "TPC268_ADVERSARIAL_STRESS=PASS", True)),
    )
    for normal, optimized in pairs:
        need(normal == optimized, "normal/optimized mismatch")

def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "certificate is not canonical")
    need(parsed.get("certificate_version") == 1 and parsed.get("claim_status") == STATUS, "certificate header")
    payload = parsed.get("payload", {})
    need(payload.get("schema") == "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1", "certificate schema")
    payload_raw = (json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    need(hashlib.sha256(payload_raw).hexdigest() == parsed.get("payload_sha256"), "payload digest")
    theorem = payload.get("finite_theorem", {})
    need(theorem.get("matched_control_cases") == 6 and theorem.get("certified_obstruction_cases") == 6 and theorem.get("total_cases") == 16, "theorem counts")
    need(theorem.get("universal_quarter_claim") == "REFUTED_SCOPED_FINITE_PARAMETER_FAMILY", "theorem scope")
    cases = payload.get("cases", [])
    need(len(cases) == 16, "case count")
    need(sum(case.get("role") == "CONTROL_Z2" for case in cases) == 6, "control count")
    need(sum(case.get("classification") == "OBSTRUCTION" for case in cases) == 6, "obstruction count")
    for case in cases:
        interval = case.get("rho_squared_interval", [])
        need(len(interval) == 2 and 0 < float(interval[0]) <= float(interval[1]), "rho interval")
        if case.get("classification") == "CONTRACTION":
            need(float(interval[1]) < 1 / 16 and float(case.get("rho_upper", "1")) < 0.25 and case.get("certified_obstruction") is False, "contraction row")
        elif case.get("classification") == "OBSTRUCTION":
            need(float(interval[0]) > 1 / 16 and float(case.get("rho_upper", "0")) > 0.25 and case.get("certified_obstruction") is True, "obstruction row")
        else:
            raise Failure("unresolved row")
        need(float(case["radius_squared_interval"][0]) > 0 and case.get("exact_projection_identity") is True, "row identity")
    find = lambda z: next(case for case in cases if tuple((case[k] for k in ("scale", "H", "Q", "kernel_exponent", "comparison_cutoff_z"))) == z)
    need(find((64, 15, 4, 1, 2))["classification"] == "CONTRACTION" and find((64, 15, 4, 1, 3))["classification"] == "OBSTRUCTION", "central flip")
    for height in (13, 17):
        need(find((64, height, 4, 1, 3))["classification"] == "OBSTRUCTION", "clock neighborhood")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC268_FINITE_CUTOFF_OBSTRUCTION") == "NUMERICALLY_CERTIFIED" and firewall.get("TPC268_ACTUAL_V59_RADIUS") == "OPEN_ASYMPTOTIC" and firewall.get("TPC268_FIXED_POWER_CREDIT") == 0 and firewall.get("TPC268_ARITHMETIC_ADVANCE") == "NO" and firewall.get("TPC268_FULL_GATE_B") == "OPEN" and firewall.get("TPC268_TWIN_PRIME_RESULT") == "NONE", "firewall")

def check_pdf() -> None:
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in ("Finite Cutoff-Sensitivity Obstruction", "Liang Wang", "finite sensitivity", "1/4", "References"):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False).stdout.decode("ascii", errors="replace")
    need("Pages:           4" in info, "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"" and all(row.split()[-5:-2] == ["yes", "yes", "yes"] for row in fonts.stdout.decode("ascii").splitlines()[2:] if row.strip()), "PDF fonts")
    if LOG.is_file():
        log = LOG.read_text(encoding="utf-8", errors="replace")
        need("Warning:" not in log and "Overfull \\" not in log and "Underfull \\" not in log and "undefined references" not in log, "LaTeX log")

def check_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"), "assert syntax: " + path.name)
    need("tpc268_cutoff_sensitivity_certificate" not in INDEPENDENT.read_text(encoding="utf-8"), "producer import")

def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError, StopIteration, ValueError) as exc:
        print("TPC268_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC268_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("finite_cutoff_obstruction=NUMERICALLY_CERTIFIED")
    print("matched_central_flip=YES")
    print("actual_v59_radius=OPEN_ASYMPTOTIC")
    return 0

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--check":
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
