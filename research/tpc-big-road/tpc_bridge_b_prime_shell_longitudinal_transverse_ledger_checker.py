#!/usr/bin/env python3
"""Fail-closed release checker for TPC-219."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-219-prime-shell-longitudinal-ledger"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_prime_shell_longitudinal_transverse_ledger.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "2a3fba34e0a19cd75be402b12454b86e3e430889cf0c0cdff205dce204d8c5a8"


class CheckFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def run(command: list[str]) -> str:
    result = subprocess.run(
        command, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    require(result.returncode == 0, f"command failed: {' '.join(command)}")
    require(result.stderr == "", f"command wrote stderr: {' '.join(command)}")
    return result.stdout


def check_layout() -> None:
    required = (
        "README.md", "PAPER_PLAN.md", "DERIVATION_PACKAGE.md", "PROOF_PACKAGE.md",
        "paper/main.tex", "paper/references.bib", "paper/main.pdf", "paper/paper.pdf",
        "code/longitudinal_transverse.py", "experiments/run_certificate.py",
        "experiments/independent_checker.py", "experiments/adversarial_alignment.py",
        "results/certificate.json", "notes/theorem_ledger.md", "notes/source_lock.md",
        "notes/route_evaluation.md",
    )
    for relative in required:
        require((PROJECT / relative).is_file(), f"missing project file: {relative}")
    require(PROJECT.joinpath("paper/main.pdf").read_bytes() == PROJECT.joinpath("paper/paper.pdf").read_bytes(), "PDF copies differ")
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    text = PROOF.read_text()
    for anchor in (
        "TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT",
        "TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT",
        "TPC219_ARITHMETIC_ADVANCE = NO",
        "TPC219_FULL_GATE_B = OPEN",
    ):
        require(anchor in text, f"missing proof anchor: {anchor}")
    require("Liang Wang" in (PROJECT / "README.md").read_text(), "author lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc219-longitudinal-transverse-certificate-v1", "schema mismatch")
    require(data.get("status") == "PASS", "certificate status is not PASS")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level mismatch")
    records = data.get("records")
    require(type(records) is dict and set(records) == {"aligned", "balanced", "orthogonal", "mixed"}, "fixture record set mismatch")
    for name, record in records.items():
        require(type(record) is dict, f"record is not an object: {name}")
        require(record.get("identity_residual") == "0", f"identity failed: {name}")
        require(type(record.get("P")) is int and record["P"] == 4, f"P mismatch: {name}")
    checks = data.get("checks")
    require(type(checks) is dict, "checks missing")
    for key, value in checks.items():
        require(type(value) is bool and value, f"certificate check failed: {key}")
    firewall = data.get("firewall")
    require(firewall == {
        "arithmetic_advance": "NO", "fixed_atom_credit": 0, "l2": "NONE",
        "full_gate_b": "OPEN", "strict_1_over_400": "UNPAID",
    }, "firewall mismatch")


def check_subchecks() -> None:
    commands = [
        [sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
        [sys.executable, "-B", str(PROJECT / "experiments/adversarial_alignment.py")],
    ]
    outputs = [run(command) for command in commands]
    require("TPC219_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check did not pass")
    require(outputs[0] == outputs[1], "normal and optimized independent outputs differ")
    require("TPC219_ALIGNMENT_ADVERSARY=PASS" in outputs[2], "adversary did not pass")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF is unexpectedly small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           3" in info, "unexpected PDF page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in ("Prime-Shell Longitudinal Ledger", "Liang Wang", "Eshell", "References"):
        require(phrase in text, f"missing PDF text: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            require(line.split()[-4] == "yes", "unembedded font detected")


def main() -> int:
    try:
        check_layout()
        check_certificate()
        check_subchecks()
        check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC219_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC219_BRIDGE_CHECK=PASS")
    print("fixtures=4")
    print("aligned_transverse=0")
    print("balanced_shell=0")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
