#!/usr/bin/env python3
"""Fail-closed release checker for TPC-220."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-220-prime-ap-collision-crosswalk"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_prime_ap_collision_crosswalk.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "4cc77d288c24fedef11d9954504c8c5ff889e521861e9934df25c05f1a1cbabc"


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
        "code/prime_ap_crosswalk.py", "experiments/run_certificate.py",
        "experiments/independent_checker.py", "experiments/collision_adversary.py",
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
        "TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT",
        "TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT",
        "TPC220_DIAGONAL_REDUCTION = PROVED_EXACT",
        "TPC220_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in text, f"missing proof anchor: {anchor}")
    require("Liang Wang" in (PROJECT / "README.md").read_text(), "author lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc220-prime-ap-collision-crosswalk-v1", "schema mismatch")
    require(data.get("status") == "PASS", "certificate status mismatch")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level mismatch")
    require(data.get("height") == 500, "height mismatch")
    require(data.get("q_values") == [101, 103, 107, 109], "q fixture mismatch")
    require(data.get("h_values") == [17, 19, 23], "h fixture mismatch")
    records = data.get("records")
    require(type(records) is list and len(records) == 6, "record count mismatch")
    for record in records:
        require(type(record) is dict, "record is not object")
        require(all(value == "0" for value in record["crosswalk_residuals"]), "crosswalk residual")
        require(all(value == "0" for value in record["gram_residuals"]), "Gram residual")
        require(all(value == "0" for value in record["diagonal_residuals"]), "diagonal residual")
    require(any(record["offdiag_entry_count"] > 0 for record in records), "collision graph empty")
    for key, value in data["checks"].items():
        require(type(value) is bool and value, f"certificate check failed: {key}")
    require(data["firewall"] == {
        "arithmetic_advance": "NO", "fixed_atom_credit": 0, "l2": "NONE",
        "full_gate_b": "OPEN", "strict_1_over_400": "UNPAID",
    }, "firewall mismatch")


def check_subchecks() -> None:
    independent = [
        [sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
    ]
    outputs = [run(command) for command in independent]
    require(outputs[0] == outputs[1], "normal/optimized output differs")
    require("TPC220_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check failed")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/collision_adversary.py")])
    require("TPC220_COLLISION_ADVERSARY=PASS" in adversary, "collision adversary failed")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           3" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in ("Prime-AP Collision Crosswalk", "Liang Wang", "Gamma", "References"):
        require(phrase in text, f"missing PDF phrase: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            require(line.split()[-4] == "yes", "unembedded font")


def main() -> int:
    try:
        check_layout(); check_certificate(); check_subchecks(); check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC220_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC220_BRIDGE_CHECK=PASS")
    print("records=6")
    print("offdiagonal_collision=OBSERVED")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
