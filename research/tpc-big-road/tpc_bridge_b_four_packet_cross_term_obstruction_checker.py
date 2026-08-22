#!/usr/bin/env python3
"""Fail-closed release checker for TPC-222."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-222-four-packet-cross-term-obstruction"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_four_packet_cross_term_obstruction.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "849403350e356a913a8b7c6a8f775a118a757976d0af6a8294461d63cb41f780"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    require(result.returncode == 0, f"command failed: {' '.join(command)}")
    require(result.stderr == "", f"stderr from command: {' '.join(command)}")
    return result.stdout


def check_layout() -> None:
    required = (
        "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
        "code/four_packet_psd.py", "experiments/run_certificate.py",
        "experiments/independent_checker.py", "experiments/trace_cross_term_adversary.py",
        "results/certificate.json", "notes/theorem_ledger.md", "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing project file: {relative}")
    require(PROJECT.joinpath("paper/main.pdf").read_bytes() == PROJECT.joinpath("paper/paper.pdf").read_bytes(), "PDF copies differ")
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    proof_text = PROOF.read_text()
    for anchor in (
        "TPC222_PSD_PACKET_GRAM = PROVED_EXACT",
        "TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT",
        "TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT",
        "TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED",
        "TPC222_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    require("Liang Wang" in (PROJECT / "README.md").read_text(), "author lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc222-four-packet-cross-term-obstruction-v1", "schema mismatch")
    require(data.get("status") == "PASS", "certificate status mismatch")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level mismatch")
    require(data.get("packet_count") == 4, "packet count mismatch")
    fixtures = data.get("fixtures")
    require(type(fixtures) is list and len(fixtures) == 2, "fixture count mismatch")
    by_name = {item["name"]: item for item in fixtures}
    require(set(by_name) == {"plus", "minus"}, "fixture names mismatch")
    for item in fixtures:
        require(item["rank_one"] is True, "fixture is not rank one")
        require(all(value == "0" for value in item["polarization_residuals"]), "polarization residual")
        require(item["trace"] == "4", "trace mismatch")
        require(item["diagonal"] == ["1", "1", "1", "1"], "diagonal mismatch")
        require(item["trace_bound"] == "16", "trace bound mismatch")
    require(by_name["plus"]["target_energy"] == "16", "plus energy mismatch")
    require(by_name["minus"]["target_energy"] == "0", "minus energy mismatch")
    require(data["firewall"] == {
        "arithmetic_advance": "NO", "fixed_atom_credit": 0, "l2": "NONE",
        "full_gate_b": "OPEN", "strict_1_over_400": "UNPAID",
    }, "firewall mismatch")
    for key, value in data["checks"].items():
        require(type(value) is bool and value, f"certificate check failed: {key}")


def check_subchecks() -> None:
    commands = [
        [sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
    ]
    outputs = [run(command) for command in commands]
    require(outputs[0] == outputs[1], "normal/optimized output differs")
    require("TPC222_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check failed")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/trace_cross_term_adversary.py")])
    require("TPC222_TRACE_CROSS_TERM_ADVERSARY=PASS" in adversary, "adversary failed")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           3" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in ("Four-Packet Polarization", "Liang Wang", "cross-term", "References"):
        require(phrase in text, f"missing PDF phrase: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            require(line.split()[-4] == "yes", "unembedded font")


def main() -> int:
    try:
        check_layout(); check_certificate(); check_subchecks(); check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC222_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC222_BRIDGE_CHECK=PASS")
    print("fixtures=plus,minus")
    print("signed_energy_pair=16,0")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
