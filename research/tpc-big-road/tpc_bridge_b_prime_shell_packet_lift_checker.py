#!/usr/bin/env python3
"""Fail-closed release checker for TPC-218."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_prime_shell_packet_lift.md"
PAPER = ROOT / "papers/tpc-218-prime-shell-packet-lift"
CERTIFICATE = PAPER / "results/certificate.json"

# Filled after the proof record is finalized; normalized LF bytes are hashed.
PROOF_SHA256 = "2124beab8ea7c67110697be4a1d1ee0586b0b68a2d240be7fd802d2c5d5e82e4"

REGISTRY = (
    "TPC218_MAXIMUM_CLAIM = PRIME_LABEL_AND_FOUR_PACKET_PRESERVING_HILBERT_LIFT_WITH_EXACT_P_FACTOR_COLLAPSE_BARRIER",
    "TPC218_ROUTE_ADVANCE = YES",
    "TPC218_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT",
    "TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT",
    "TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT",
    "TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE",
    "TPC218_SPLIT_UNNORMALIZED_EXPONENT = PROVED_97_OVER_96",
    "TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE",
    "TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR",
    "TPC218_PACKET_PROJECTION_BOUND = PROVED_TRACE_DOMINATION",
    "TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED",
    "TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED",
    "TPC218_ARITHMETIC_CANCELLATION = NONE",
    "TPC218_ARITHMETIC_ADVANCE = NO",
    "TPC218_FIXED_ATOM_CREDIT = 0",
    "TPC218_L2 = NONE",
    "TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN",
    "TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN",
    "TPC218_FULL_GATE_B = OPEN",
    "TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC218_TPC_TRIGGER = true",
    "TPC218_NUMBERED_RELEASE = YES",
    "TPC218_STATUS = PROVED_STRUCTURAL_L1",
    "TPC218_ROUND2_CLUE = PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE",
)

REQUIRED = (
    ".gitignore",
    "README.md",
    "DERIVATION_PACKAGE.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/main.pdf",
    "paper/paper.pdf",
    "code/prime_shell_packet_lift.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/adversarial_alignment.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)

EXPECTED_FIREWALL = {
    "route_a": "NOT_APPLICABLE",
    "route_b_structural_threshold_a": "PASS",
    "hilbert_valued_large_sieve": "PROVED_STANDARD_TENSOR_LIFT",
    "prime_label_preservation": "PROVED_EXACT",
    "packet_matrix_bound": "PROVED_EXACT",
    "split_normalized_exponent": "PROVED_1_OVER_96_LOG_FIVE",
    "scalar_collapse": "PROVED_P_FACTOR_RECOVERS_11_OVER_32",
    "prime_label_orthogonality": "REFUTED_SCOPED",
    "packet_cancellation": "NONE",
    "prime_shell_signed_reassembly": "OPEN",
    "four_packet_signed_reassembly": "OPEN",
    "arithmetic_cancellation": "NONE",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "l2": "NONE",
    "full_gate_b": "OPEN",
    "full_gate_b_strict_1_over_400": "UNPAID",
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


def normalized_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def run_command(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
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
        "## 2. Fixed-q row estimate",
        "## 3. Coefficient harmonic bound",
        "## 4. Hilbert-valued finite-window theorem",
        "## 6. Sharp scoped obstructions",
        "ROUND2_CLUE = PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE",
    ):
        require(anchor in proof, f"proof anchor missing: {anchor}")
    require(PROOF_SHA256 != "TO_BE_FILLED", "proof hash not frozen")
    require(normalized_sha256(PROOF) == PROOF_SHA256, "proof hash mismatch")
    for relative in REQUIRED:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    require(
        "Liang Wang" in (PAPER / "README.md").read_text(encoding="utf-8"),
        "author lock",
    )
    for relative in ("README.md", "PROOF_PACKAGE.md", "notes/route_evaluation.md"):
        text = (PAPER / relative).read_text(encoding="utf-8")
        require("ARITHMETIC_ADVANCE" in text, f"claim firewall missing: {relative}")


def check_certificate() -> dict[str, object]:
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
    )
    require(
        data["schema"] == "TPC218_PRIME_SHELL_PACKET_LIFT_CERTIFICATE_V1",
        "schema",
    )
    require(
        data["classification"]
        == "PROVED_STRUCTURAL_L1_PRIME_LABEL_AND_PACKET_PRESERVING_LIFT",
        "classification",
    )
    require(
        data["source_exponents"]
        == {
            "H": "21/32",
            "Q": "1/3",
            "Q2_over_H": "1/96",
            "Q3_over_H": "11/32",
            "U": "133/400",
            "U2_over_x": "-67/200",
            "UQ_over_H": "23/2400",
            "Y0": "31/96",
        },
        "source exponents",
    )
    theorem = data["theorem"]
    require(theorem["hilbert_valued_large_sieve"] == "PROVED_STANDARD_TENSOR_LIFT", "lift")
    require(theorem["split_normalized_exponent"] == "PROVED_X_1_OVER_96_LOG_FIVE", "split")
    require(theorem["scalar_shell_recovery"] == "PROVED_X_11_OVER_32_LOG_FIVE", "scalar")
    require(theorem["prime_count_used"] is False, "prime count dependency")
    require(theorem["mobius_cancellation_used"] is False, "Mobius dependency")
    require(theorem["arithmetic_saving"] is False, "arithmetic dependency")
    require(data["claim_firewall"] == EXPECTED_FIREWALL, "claim firewall")

    finite = data["finite_fixture"]
    require(len(finite["q_values"]) == 3, "finite q count")
    require(len(finite["divisor_values"]) == 3, "finite divisor count")
    require(len(finite["reduced_denominators"]) == 6, "finite denominator count")
    require(len(finite["intervals"]) == 3, "finite interval count")

    prime = data["prime_label_alignment"]
    require(prime["coherent_to_diagonal_ratio"] == "4", "q alignment ratio")
    require(prime["row_supports"] == [[1, 4]] * 4, "q alignment support")
    require(
        prime["classification"]
        == "NUMERICALLY_CERTIFIED_FINITE_STRUCTURAL_ADVERSARY",
        "q adversary class",
    )

    packet = data["packet_alignment"]
    require(packet["projection_to_total_ratio"] == "1", "packet alignment ratio")
    require(packet["classification"] == "ALGEBRAIC_FINITE_ALIGNMENT", "packet class")
    return data


def check_subcheckers() -> None:
    scripts = PAPER / "experiments"
    commands = (
        ("run_certificate.py", ()),
        ("independent_checker.py", ()),
        ("independent_checker.py", ("-O",)),
        ("adversarial_alignment.py", ()),
        ("adversarial_alignment.py", ("-O",)),
    )
    outputs: dict[str, bytes] = {}
    for script, options in commands:
        executable = [sys.executable]
        if "-O" in options:
            executable.append("-O")
        executable.extend(("-B", str(scripts / script), "--check"))
        result = run_command(executable)
        label = script + " " + " ".join(options)
        require(
            result.returncode == 0,
            f"subchecker failed: {label}: "
            f"{result.stderr.decode('utf-8', 'replace')}",
        )
        outputs[label] = result.stdout
    require(
        outputs["independent_checker.py "]
        == outputs["independent_checker.py -O"],
        "independent normal/optimized mismatch",
    )
    require(
        outputs["adversarial_alignment.py "]
        == outputs["adversarial_alignment.py -O"],
        "adversarial normal/optimized mismatch",
    )


def check_pdf() -> None:
    main_pdf = PAPER / "paper/main.pdf"
    release_pdf = PAPER / "paper/paper.pdf"
    payload = release_pdf.read_bytes()
    require(payload.startswith(b"%PDF-"), "PDF header")
    require(len(payload) > 100_000, "PDF unexpectedly small")
    require(main_pdf.read_bytes() == payload, "paper.pdf differs from main.pdf")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    try:
        check_layout()
        data = check_certificate()
        check_subcheckers()
        check_pdf()
    except (
        CheckFailure,
        KeyError,
        TypeError,
        ValueError,
        OSError,
        json.JSONDecodeError,
    ) as error:
        print(f"TPC218_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    prime = data["prime_label_alignment"]
    packet = data["packet_alignment"]
    print("TPC218_BRIDGE_CHECK=PASS")
    print("finite_intervals=3")
    print("q_alignment_ratio=", prime["coherent_to_diagonal_ratio"])
    print("packet_projection_ratio=", packet["projection_to_total_ratio"])
    print("split_normalized_exponent=1/96")
    print("scalar_recovery_exponent=11/32")
    print("claim_level=PROVED_STRUCTURAL_L1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
