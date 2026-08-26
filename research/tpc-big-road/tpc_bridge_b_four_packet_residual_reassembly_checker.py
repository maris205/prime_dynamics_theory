#!/usr/bin/env python3
"""Fail-closed release checker for TPC-260."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers/tpc-260-four-packet-residual-reassembly"
BRIDGE = ROOT / "research/tpc-big-road/bridge_b_four_packet_residual_reassembly.md"
PRODUCER = PROJECT / "code/tpc260_four_packet_residual_certificate.py"
INDEPENDENT = PROJECT / "experiments/tpc260_independent_checker.py"
STRESS = PROJECT / "experiments/tpc260_residual_stress.py"
CERTIFICATE = PROJECT / "results/tpc260_certificate.json"
PDF = PROJECT / "paper/paper.pdf"
MAIN_PDF = PROJECT / "paper/main.pdf"
BASELINE_HEAD = "aa129b88ea2af47bcbf3473601bcb33f9b78380b"
STATUS = "PROVED_STRUCTURAL_NULL_COMPATIBLE_FOUR_PACKET_COMPLETION_OBSTRUCTION"
BRIDGE_SHA256 = "01daeff6289bfa857a1f108bea785b908139f749b8233a227a00002dd239561a"

SOURCE_HASHES = {
    "AGENTS.md": "c86859130ddcf77082f17ffd3477f32e5bf216a43be73a19901fd5e6efa741c1",
    "TPC_HANDOFF.md": "bddb89f6ce0fa7f17481c091bc53cec23ed8da2c228ac389e846625b6b5b7ef0",
    "papers/tpc-259-same-clock-null-coupling/README.md":
        "a54e3ade4a56aec2e79be049ff4db06d30b79356115691af3686c00a844d5f86",
    "papers/tpc-259-same-clock-null-coupling/PROOF_PACKAGE.md":
        "f4573edbd6d30045f0f476508d3bccf315fba42fb50603c6da8f54c3b466eb14",
    "papers/tpc-259-same-clock-null-coupling/notes/theorem_ledger.md":
        "6ecbad2368776856aa7ed4c1c20987ab2df0422c86283c5ec691f5d9c379d1de",
    "papers/tpc-259-same-clock-null-coupling/notes/route_evaluation.md":
        "e0d40481e4c745323be9618c72e127de14523118899c9c26b040c38407105431",
    "research/tpc-big-road/bridge_b_same_clock_null_coupling.md":
        "8c09035660c026d21606955b41a10affa06cb330dcdaf4782065adc42f1153ff",
    "research/tpc-big-road/tpc_bridge_b_same_clock_null_coupling_checker.py":
        "cc0adf0bf7d5c28dcbe831f3aca3a65f81708620d09f4a7ffe70c2349ed991c3",
}

# Filled after the project sources and final PDF are frozen.
PROJECT_HASHES = {
    ".gitignore": "d92f5c8f90059cd13dc2b16e79d88d4b4d7bfb936cb1ae88d90f407177332bb3",
    "DERIVATION_PACKAGE.md": "8acfc11dd69614a5de0bb7a302a19f7df28dba3cd642e3b02ba3604f4c01ca6f",
    "PAPER_PLAN.md": "a016b2db77d35c9ddff9c72f7cafd042855ca92c074e2a94a705801b5de33717",
    "PROOF_PACKAGE.md": "e5cfb3d7b1f5b32ddc59270656ec2ff11e2d97c90c2deb68395d03aab55a03b2",
    "README.md": "f45e54e26672327578535e88d948e5559d1e7c6517cfe7a3cefcd29f19630949",
    "code/tpc260_four_packet_residual_certificate.py": "f2d2d1c9d2f9b689a1d5a0395685b388ed0e9bfed24abed0e9bb4443f6857ac1",
    "experiments/tpc260_independent_checker.py": "7061395670148a2a04d078a7a0b4983b70d3031ed26c72f94a17e23023653d85",
    "experiments/tpc260_residual_stress.py": "016dd4b31f097a9514b8312c7b56c268766d2049506ed6b87613c5ed397ddce3",
    "notes/citation_verification.md": "8e5f16b029b332d1db42ae85fd3c3532ee9a6c60bcbe8345c9249058dcdc8d07",
    "notes/claim_firewall.md": "a864cdec41ed42872fe000c8f945b156be172cadb26aadaf6c2558059bbca91d",
    "notes/computational_protocol.md": "7ec4202048c4bf76255f71caa8c7637fad075fe21c7d45490b26b9236d6015cb",
    "notes/route_evaluation.md": "2cee2e6e166c4e484bf8f88b7f9ef80ec72d893d8c829606b4353aab39f2f9dd",
    "notes/theorem_ledger.md": "32ef275efbecb0175dbb01bfc068f654106f9ab3accb89703350ea9628aad746",
    "paper/main.tex": "9cf4bbca7c15ceef4df54d5fbb6b48cae1715545c7260907c70cb6f49c5cf4e1",
    "paper/main.pdf": "3cd9b55b17cde098fe7f231ef8d523e5bb6e4941c15b3377959e51a05c3e2159",
    "paper/paper.pdf": "3cd9b55b17cde098fe7f231ef8d523e5bb6e4941c15b3377959e51a05c3e2159",
    "paper/references.bib": "32b5c92480b495ce2657795b2cc83442748afd1d00e9b1e4588dce384a6f32d8",
    "results/tpc260_certificate.json": "ef5fb5d3599f4a191eda76d5629b099cad8d8d465a4d7036a48366bfd30ef468",
}

EXPECTED_FILES = set(PROJECT_HASHES)
BUILD_INTERMEDIATES = {
    "paper/main.aux", "paper/main.bbl", "paper/main.blg",
    "paper/main.log", "paper/main.out",
}

MARKERS = (
    "TPC260_MAXIMUM_CLAIM = " + STATUS,
    "TPC260_ROUTE_ADVANCE = YES_SCOPED_MODE_AUDIT",
    "TPC260_HAAR_COMPLEMENT = PROVED_EXACT_FINITE",
    "TPC260_POLYGON_COMPLETION = PROVED_EXACT_FINITE",
    "TPC260_DFT_MODE_LEDGER = PROVED_EXACT",
    "TPC260_NULL_CHANNEL_COMPATIBILITY = PROVED_EXACT_SYNTHETIC",
    "TPC260_FULL_RESIDUAL_IDENTIFIABILITY = REFUTED_SCOPED",
    "TPC260_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE",
    "TPC260_ARITHMETIC_ADVANCE = NO",
    "TPC260_FIXED_ATOM_CREDIT = 0",
    "TPC260_L2 = NONE",
    "TPC260_FULL_GATE_B = OPEN",
    "TPC260_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL",
    "TPC260_TWIN_PRIME_RESULT = NONE",
    "TPC260_STATUS = " + STATUS,
)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_digest(path: Path) -> str:
    return digest(path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n"))


def baseline_bytes(relative: str) -> bytes:
    result = subprocess.run(
        ["git", "show", BASELINE_HEAD + ":" + relative], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0 and result.stderr == b"",
         "baseline source: " + relative)
    return result.stdout


def check_sources() -> None:
    for relative, expected in SOURCE_HASHES.items():
        need(digest(baseline_bytes(relative)) == expected,
             "source hash: " + relative)


def check_project() -> None:
    actual = {str(path.relative_to(PROJECT)) for path in PROJECT.rglob("*")
              if path.is_file()}
    need(actual - BUILD_INTERMEDIATES == EXPECTED_FILES, "project manifest")
    for relative, expected in PROJECT_HASHES.items():
        need(expected != "PLACEHOLDER", "project hash placeholder: " + relative)
        need(normalized_digest(PROJECT / relative) == expected,
             "project hash: " + relative)
    need(MAIN_PDF.read_bytes() == PDF.read_bytes(), "PDF copies differ")


def check_bridge() -> None:
    need(BRIDGE_SHA256 != "PLACEHOLDER_BRIDGE_HASH", "bridge hash placeholder")
    need(normalized_digest(BRIDGE) == BRIDGE_SHA256, "bridge hash")
    text = BRIDGE.read_text(encoding="utf-8")
    for marker in MARKERS:
        need(marker in text, "bridge marker: " + marker)
    need("ROUND2_CLUE = PROVE_A_LITERAL_MODE_ZERO_OR_CROSS_GRAM_ESTIMATE" in text,
         "round-two clue")


def run_child(path: Path, marker: str) -> str:
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend(["-B", str(path), "--check"])
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    need(result.returncode == 0 and result.stderr == "", "child failed: " + path.name)
    need(result.stdout.startswith(marker), "child marker: " + path.name)
    return result.stdout


def check_children() -> None:
    producer = run_child(PRODUCER, "TPC260_CERTIFICATE=PASS")
    independent = run_child(INDEPENDENT, "TPC260_INDEPENDENT_CHECK=PASS")
    stress = run_child(STRESS, "TPC260_STRESS=PASS")
    need("literal_mode_zero=OPEN" in producer, "producer firewall")
    need("producer_imported=NO" in independent, "independent isolation")
    need("residual_range=EXACT" in stress, "stress result")


def check_certificate() -> None:
    raw = CERTIFICATE.read_bytes()
    parsed = json.loads(raw)
    canonical = (json.dumps(parsed, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")
    need(raw == canonical, "certificate canonical")
    need(parsed.get("schema") == "TPC260_CERTIFICATE_V1", "certificate schema")
    need(parsed.get("claim") == STATUS, "certificate claim")
    need(parsed.get("baseline", {}).get("head") == BASELINE_HEAD,
         "certificate baseline")
    need(parsed.get("exact_checks") == {
        "clocks": 128, "frame_norms": 384, "null_scaling": 128,
        "orthogonality": 384, "scaling_dots": 384,
    }, "exact counts")
    need(parsed.get("polygon_audit", {}).get("equal_lengths") == {
        "D": "4", "energy_max": "16", "energy_min": "0",
        "r_max": "4", "r_min": "0",
    }, "polygon endpoints")
    modes = parsed.get("mode_audit", {})
    need(modes.get("plus", {}).get("mode_energy") == ["4", "0", "0", "0"],
         "plus modes")
    need(modes.get("alternating", {}).get("mode_energy") == ["0", "0", "4", "0"],
         "alternating modes")
    need(modes.get("plus", {}).get("full_energy") == "16" and
         modes.get("alternating", {}).get("full_energy") == "0",
         "full energies")
    firewall = parsed.get("firewall", {})
    need(firewall.get("TPC260_ARITHMETIC_ADVANCE") == "NO" and
         firewall.get("TPC260_L2") == "NONE" and
         firewall.get("TPC260_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC260_FIXED_ATOM_CREDIT") == 0 and
         firewall.get("TPC260_TWIN_PRIME_RESULT") == "NONE",
         "certificate firewall")


def check_pdf() -> None:
    for name in ("pdftotext", "pdffonts", "pdfinfo"):
        need(shutil.which(name) is not None, "PDF tool: " + name)
    text = subprocess.run(["pdftotext", "-layout", str(PDF), "-"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          check=False)
    need(text.returncode == 0 and text.stderr == b"", "PDF text")
    decoded = text.stdout.decode("utf-8", errors="replace")
    for phrase in (
        "Null-Compatible Four-Packet Completion Obstruction",
        "Liang Wang", "polygon completion", "missing DFT mode",
        "residual energies", "References",
    ):
        need(phrase in decoded, "PDF phrase: " + phrase)
    info = subprocess.run(["pdfinfo", str(PDF)], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    info_text = info.stdout.decode("ascii", errors="replace")
    need(info.returncode == 0 and
         re.search(r"(?m)^Pages:\s+5\s*$", info_text) is not None,
         "PDF pages")
    fonts = subprocess.run(["pdffonts", str(PDF)], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, check=False)
    need(fonts.returncode == 0 and fonts.stderr == b"", "PDF fonts")
    rows = [row for row in fonts.stdout.decode("ascii").splitlines()[2:]
            if row.strip()]
    need(len(rows) == 14, "PDF font count")
    for row in rows:
        columns = row.split()
        need(len(columns) >= 8 and columns[-5:-2] == ["yes", "yes", "yes"],
             "PDF font embedding")


def check_source_hygiene() -> None:
    for path in (PRODUCER, INDEPENDENT, STRESS):
        need("assert " not in path.read_text(encoding="utf-8"),
             "unsafe assertion syntax: " + path.name)
    independent_text = INDEPENDENT.read_text(encoding="utf-8")
    need("tpc260_four_packet_residual_certificate" not in independent_text,
         "producer import")


def main() -> int:
    try:
        check_sources()
        check_project()
        check_bridge()
        check_source_hygiene()
        check_certificate()
        check_children()
        check_pdf()
    except (Failure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print("TPC260_BRIDGE_CHECK=FAIL: " + str(exc), file=sys.stderr)
        return 1
    print("TPC260_BRIDGE_CHECK=PASS")
    print("claim=" + STATUS)
    print("polygon=PROVED_EXACT_FINITE")
    print("dft=PROVED_EXACT")
    print("full_residual=REFUTED_SCOPED")
    print("literal_mode_zero=OPEN")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
