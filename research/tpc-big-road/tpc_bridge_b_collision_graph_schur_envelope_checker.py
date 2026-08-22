#!/usr/bin/env python3
"""Fail-closed release checker for TPC-221."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "papers" / "tpc-221-collision-graph-schur-envelope"
PROOF = ROOT / "research" / "tpc-big-road" / "bridge_b_collision_graph_schur_envelope.md"
CERTIFICATE = PROJECT / "results" / "certificate.json"
PROOF_SHA256 = "683704ec6d72306dcc7be9ce9dfb86dd0535e00e8bd9298db61bd1dd55c43330"


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
        "code/collision_schur.py", "experiments/run_certificate.py",
        "experiments/independent_checker.py", "experiments/schur_saturation_adversary.py",
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
        "TPC221_COLLISION_GRAM_PSD = PROVED_EXACT",
        "TPC221_SCHUR_ENVELOPE = PROVED_EXACT",
        "TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT",
        "TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE",
        "TPC221_ARITHMETIC_ADVANCE = NO",
    ):
        require(anchor in proof_text, f"missing proof anchor: {anchor}")
    require("Liang Wang" in (PROJECT / "README.md").read_text(), "author lock missing")


def check_certificate() -> None:
    data = json.loads(CERTIFICATE.read_text())
    require(data.get("schema") == "tpc221-collision-graph-schur-envelope-v1", "schema mismatch")
    require(data.get("status") == "PASS", "certificate status mismatch")
    require(data.get("claim_level") == "PROVED_STRUCTURAL_L1", "claim level mismatch")
    require(data.get("height") == 500, "height mismatch")
    require(data.get("q_values") == [101, 103, 107, 109], "generic q fixture mismatch")
    require(data.get("h_values") == [17, 19, 23], "generic h fixture mismatch")
    records = data.get("records")
    require(type(records) is list and len(records) == 6, "record count mismatch")
    for record in records:
        require(all(value == "0" for value in record["gram_residuals"]), "Gram residual")
        require(all(value == "0" for value in record["diagonal_residuals"]), "diagonal residual")
        require(FractionLike(record["schur_slack"]) >= 0, "negative Schur slack")
    saturation = data.get("saturation")
    require(saturation.get("h") == 5, "saturation modulus mismatch")
    require(saturation.get("q_values") == [101, 151, 181, 191], "saturation q mismatch")
    require(saturation.get("cutoffs") == [1, 1, 1, 1], "saturation cutoff mismatch")
    require(saturation.get("row_equal") is True, "rows not aligned")
    require(saturation.get("all_gram_entries_equal") is True, "Gram not constant")
    require(saturation.get("schur_radius") == "8", "Schur radius mismatch")
    require(saturation.get("coherent_energy") == "32", "coherent energy mismatch")
    require(saturation.get("diagonal_total") == "8", "diagonal total mismatch")
    require(saturation.get("coherent_to_diagonal_ratio") == "4", "saturation ratio mismatch")
    require(data["firewall"] == {
        "arithmetic_advance": "NO", "fixed_atom_credit": 0, "l2": "NONE",
        "full_gate_b": "OPEN", "strict_1_over_400": "UNPAID",
    }, "firewall mismatch")
    for key, value in data["checks"].items():
        require(type(value) is bool and value, f"certificate check failed: {key}")


def FractionLike(value: str):
    # Avoid importing the producer: certificate strings are restricted to rational values.
    from fractions import Fraction
    return Fraction(value)


def check_subchecks() -> None:
    commands = [
        [sys.executable, "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
        [sys.executable, "-O", "-B", str(PROJECT / "experiments/independent_checker.py"), "--check"],
    ]
    outputs = [run(command) for command in commands]
    require(outputs[0] == outputs[1], "normal/optimized output differs")
    require("TPC221_INDEPENDENT_CHECK=PASS" in outputs[0], "independent check failed")
    adversary = run([sys.executable, "-B", str(PROJECT / "experiments/schur_saturation_adversary.py")])
    require("TPC221_SCHUR_SATURATION_ADVERSARY=PASS" in adversary, "adversary failed")


def check_pdf() -> None:
    pdf = PROJECT / "paper/paper.pdf"
    require(pdf.stat().st_size > 100_000, "PDF too small")
    info = run(["pdfinfo", str(pdf)])
    require("Pages:           3" in info, "unexpected page count")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    for phrase in ("Collision-Graph Schur Envelope", "Liang Wang", "saturation", "References"):
        require(phrase in text, f"missing PDF phrase: {phrase}")
    fonts = run(["pdffonts", str(pdf)])
    for line in fonts.splitlines()[2:]:
        if line.strip():
            require(line.split()[-4] == "yes", "unembedded font")


def main() -> int:
    try:
        check_layout(); check_certificate(); check_subchecks(); check_pdf()
    except (CheckFailure, OSError, subprocess.SubprocessError, json.JSONDecodeError) as error:
        print(f"TPC221_BRIDGE_CHECK=FAIL: {error}", file=sys.stderr)
        return 1
    print("TPC221_BRIDGE_CHECK=PASS")
    print("records=6")
    print("saturation_ratio=4")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
