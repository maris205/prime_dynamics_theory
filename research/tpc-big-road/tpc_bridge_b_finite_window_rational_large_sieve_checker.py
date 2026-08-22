#!/usr/bin/env python3
"""Fail-closed release checker for TPC-217."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_finite_window_rational_large_sieve.md"
PAPER = ROOT / "papers/tpc-217-finite-window-rational-large-sieve"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC217_MAXIMUM_CLAIM = SOURCE_LOCKED_COMMON_SOURCE_FINITE_WINDOW_ATTACHMENT_BY_REDUCED_RATIONAL_LARGE_SIEVE",
    "TPC217_ROUTE_ADVANCE = YES",
    "TPC217_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC217_REDUCED_FREQUENCY_REGROUPING = PROVED_EXACT",
    "TPC217_FAREY_SPACING = PROVED_EXACT",
    "TPC217_ADDITIVE_LARGE_SIEVE = PROVED_STANDARD",
    "TPC217_FINITE_WINDOW_ATTACHMENT = PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED",
    "TPC217_UNNORMALIZED_WINDOW_EXPONENT = PROVED_43_OVER_32",
    "TPC217_WINDOW_LOSS = PROVED_1_PLUS_U2_OVER_N",
    "TPC217_FINITE_WINDOW_OFF_FREQUENCY_GRAM = CONTROLLED_BY_LARGE_SIEVE",
    "TPC217_ALIGNED_ONE_POINT_ORTHOGONALITY = REFUTED_SCOPED",
    "TPC217_PRIME_SHELL_REASSEMBLY = OPEN",
    "TPC217_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN",
    "TPC217_ARITHMETIC_CANCELLATION = NONE",
    "TPC217_ARITHMETIC_ADVANCE = NO",
    "TPC217_FIXED_ATOM_CREDIT = 0",
    "TPC217_L2 = NONE",
    "TPC217_FULL_GATE_B = OPEN",
    "TPC217_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC217_TPC_TRIGGER = true",
)

REQUIRED = (
    ".gitignore",
    "README.md",
    "DERIVATION_PACKAGE.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/finite_window_attachment.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/frequency_crowding.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)

EXPECTED_FIREWALL = {
    "route_a": "NOT_APPLICABLE",
    "route_b_structural_threshold_a": "PASS",
    "reduced_frequency_regrouping": "PROVED_EXACT",
    "finite_window_large_sieve": "PROVED_STANDARD",
    "finite_window_attachment": "PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED",
    "normalized_exponent": "11/32",
    "finite_window_off_frequency_gram": "CONTROLLED_BY_LARGE_SIEVE",
    "prime_shell_reassembly": "OPEN",
    "four_packet_signed_reassembly": "OPEN",
    "arithmetic_cancellation": "NONE",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "l2": "NONE",
    "full_gate_b": "OPEN",
    "full_gate_b_strict_1_over_400": "UNPAID",
    "finite_window_orthogonality": "REFUTED_SCOPED",
}


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def run(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        arguments,
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check_layout() -> None:
    require(PROOF.is_file(), "proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    for anchor in (
        "Exact reduced-frequency regrouping",
        "Farey spacing",
        "Finite-window large-sieve attachment",
        "ROUND2_CLUE = PRESERVE_THE_FINITE_WINDOW_LARGE_SIEVE_ATTACHMENT",
    ):
        require(anchor in proof, f"proof anchor missing: {anchor}")
    for relative in REQUIRED:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    require("Liang Wang" in (PAPER / "README.md").read_text(encoding="utf-8"), "author lock")
    for relative in ("README.md", "PROOF_PACKAGE.md", "notes/route_evaluation.md"):
        text = (PAPER / relative).read_text(encoding="utf-8")
        require("ARITHMETIC_ADVANCE" in text or "arithmetic" in text, f"firewall missing: {relative}")


def check_certificate() -> dict[str, object]:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    require(data["schema"] == "TPC217_FINITE_WINDOW_RATIONAL_LARGE_SIEVE_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_FINITE_WINDOW_ATTACHMENT", "classification")
    require(data["source_exponents"]["Q3_over_H"] == "11/32", "direct exponent")
    require(data["source_exponents"]["U2_over_x"] == "-67/200", "window exponent")
    require(data["theorem"]["finite_window_attachment"] == "PROVED_X_11_OVER_32_LOG_FIVE_NORMALIZED", "attachment")
    require(data["theorem"]["prime_count_used"] is False, "prime count dependency")
    require(data["theorem"]["mobius_cancellation_used"] is False, "mobius dependency")
    require(data["claim_firewall"] == EXPECTED_FIREWALL, "claim firewall")
    fixture = data["finite_fixture"]
    require(len(fixture["divisors"]) == 14, "fixture divisor count")
    require(len(fixture["reduced_denominators"]) == 16, "fixture denominator count")
    require(len(fixture["intervals"]) == 3, "fixture interval count")
    adversary = data["frequency_crowding_adversary"]
    require(adversary["support"] == [1, 4], "adversary support")
    require(adversary["window_to_diagonal_ratio"] == "2", "adversary ratio")
    require(adversary["classification"] == "FINITE_STRUCTURAL_ADVERSARY", "adversary class")
    return data


def check_subcheckers() -> None:
    scripts = PAPER / "experiments"
    commands = (
        ("run_certificate.py", ()),
        ("independent_checker.py", ()),
        ("independent_checker.py", ("-O",)),
        ("frequency_crowding.py", ()),
        ("frequency_crowding.py", ("-O",)),
    )
    outputs: dict[str, bytes] = {}
    for script, options in commands:
        label = script + " " + " ".join(options)
        executable = [sys.executable]
        if "-O" in options:
            executable.append("-O")
        executable.extend(("-B", str(scripts / script), "--check"))
        result = run(executable)
        require(result.returncode == 0, f"subchecker failed: {label}: {result.stderr.decode('utf-8', 'replace')}")
        outputs[label] = result.stdout
    require(outputs["independent_checker.py "] == outputs["independent_checker.py -O"], "independent stdout mismatch")
    require(outputs["frequency_crowding.py "] == outputs["frequency_crowding.py -O"], "crowding stdout mismatch")


def check_pdf() -> None:
    pdf = PAPER / "paper/paper.pdf"
    payload = pdf.read_bytes()
    require(payload.startswith(b"%PDF-"), "PDF header")
    require(len(payload) > 100_000, "PDF unexpectedly small")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check_layout()
        data = check_certificate()
        check_subcheckers()
        check_pdf()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"TPC217_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_fixture"]
    adversary = data["frequency_crowding_adversary"]
    print("TPC217_BRIDGE_CHECK=PASS")
    print("active_divisors=", len(fixture["divisors"]))
    print("reduced_denominators=", len(fixture["reduced_denominators"]))
    print("intervals=", len(fixture["intervals"]))
    print("crowding_ratio=", adversary["window_to_diagonal_ratio"])
    print("normalized_exponent=11/32")
    print("claim_level=PROVED_STRUCTURAL_L1_FINITE_WINDOW_ATTACHMENT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
