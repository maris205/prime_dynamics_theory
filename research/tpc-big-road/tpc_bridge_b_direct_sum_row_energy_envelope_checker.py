#!/usr/bin/env python3
"""Fail-closed release checker for TPC-216."""

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
PROOF = ROOT / "research/tpc-big-road/bridge_b_direct_sum_row_energy_envelope.md"
PAPER = ROOT / "papers/tpc-216-direct-sum-row-energy-envelope"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC216_MAXIMUM_CLAIM = SOURCE_LOCKED_COMPLETE_PERIOD_DIRECT_SUM_ROW_ENERGY_ENVELOPE_WITH_FIXED_Q_NO_COLLISION_AND_ALIGNED_SHELL_OBSTRUCTION",
    "TPC216_ROUTE_ADVANCE = YES",
    "TPC216_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC216_FIXED_Q_NO_COLLISION = PROVED_EXACT",
    "TPC216_FIXED_Q_ROW_ENERGY = PROVED_EXACT",
    "TPC216_SHELL_CAUCHY_ENVELOPE = PROVED_EXACT",
    "TPC216_PRIME_SHELL_CARDINALITY = PROVED_P_LE_2Q",
    "TPC216_NORMALIZED_EXPONENT = PROVED_11_OVER_32",
    "TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE = PROVED_X_11_OVER_32_LOG_CUBED",
    "TPC216_ARITHMETIC_CANCELLATION = NONE",
    "TPC216_ALIGNED_SUPPORT_ADVERSARY = NUMERICALLY_CERTIFIED_EXACT_RATIONAL",
    "TPC216_FREE_Q_ORTHOGONALITY = REFUTED_SCOPED",
    "TPC216_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN",
    "TPC216_PRIME_SHELL_REASSEMBLY = OPEN",
    "TPC216_FULL_GATE_B = OPEN",
    "TPC216_ARITHMETIC_ADVANCE = NO",
    "TPC216_FIXED_ATOM_CREDIT = 0",
    "TPC216_L2 = NONE",
    "TPC216_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC216_TPC_TRIGGER = true",
)

REQUIRED = (
    ".gitignore",
    "README.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/direct_sum_row_energy.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/adversarial_shell_alignment.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)

EXPECTED_FIREWALL = {
    "route_a": "NOT_APPLICABLE",
    "route_b_structural_threshold_a": "PASS",
    "fixed_q_no_collision": "PROVED_EXACT",
    "shell_cauchy_envelope": "PROVED_EXACT",
    "direct_sum_row_energy_envelope": "PROVED_X_11_OVER_32_LOG_CUBED",
    "normalized_exponent": "PROVED_11_OVER_32",
    "arithmetic_cancellation": "NONE",
    "finite_window_off_frequency_gram": "OPEN",
    "prime_shell_reassembly": "OPEN",
    "full_gate_b": "OPEN",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "l2": "NONE",
    "full_gate_b_strict_1_over_400": "UNPAID",
    "cauchy_bottleneck": "EXHIBITED_BY_ALIGNED_FINITE_FIXTURE",
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


def run_checker(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
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
        "Theorem: fixed-q no-collision",
        "Theorem: direct-sum row-energy envelope",
        "Proposition: aligned-shell obstruction",
        "ROUND2_CLUE = ATTACH_THE_COMPLETE_PERIOD_DIRECT_SUM_ENVELOPE",
    ):
        require(anchor in proof, f"proof anchor missing: {anchor}")
    for relative in REQUIRED:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    for relative in ("README.md", "PROOF_PACKAGE.md", "notes/route_evaluation.md"):
        text = (PAPER / relative).read_text(encoding="utf-8")
        require("ARITHMETIC_ADVANCE" in text or "arithmetic `L2`" in text, f"firewall missing: {relative}")
    require("Liang Wang" in (PAPER / "README.md").read_text(encoding="utf-8"), "author lock")


def check_certificate() -> dict[str, object]:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    require(data["schema"] == "TPC216_DIRECT_SUM_ROW_ENERGY_ENVELOPE_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_DIRECT_SUM_ROW_ENERGY_ENVELOPE", "classification")
    require(data["source_exponents"]["Q3_over_H"] == "11/32", "exponent")
    require(data["source_relations"]["collision_condition"] == "4Q<H for sufficiently large x", "collision lock")
    require(data["theorem"]["prime_shell_cardinality"] == "P<=2Q", "shell count")
    require(data["theorem"]["prime_count_used"] is False, "prime count dependency")
    require(data["claim_firewall"] == EXPECTED_FIREWALL, "claim firewall")
    fixture = data["finite_adversary"]
    require(fixture["q_values"] == [101, 131, 151, 181], "fixture q values")
    require(fixture["aligned_support"] == [1, 4], "fixture support")
    require(fixture["classification"] == "FINITE_STRUCTURAL_ADVERSARY", "fixture classification")
    require(len(fixture["individual_rows"]) == 4, "fixture row count")
    require(fixture["combined_norm"] != fixture["individual_norm_sum"], "fixture has no cross energy")
    return data


def check_subcheckers() -> None:
    scripts = PAPER / "experiments"
    producer = run_checker([sys.executable, "-B", str(scripts / "run_certificate.py"), "--check"])
    require(producer.returncode == 0, f"producer failed: {producer.stderr.decode('utf-8', 'replace')}")
    independent = run_checker([sys.executable, "-B", str(scripts / "independent_checker.py"), "--check"])
    optimized = run_checker([sys.executable, "-O", "-B", str(scripts / "independent_checker.py"), "--check"])
    require(independent.returncode == 0, f"independent failed: {independent.stderr.decode('utf-8', 'replace')}")
    require(optimized.returncode == 0, f"optimized failed: {optimized.stderr.decode('utf-8', 'replace')}")
    require(independent.stdout == optimized.stdout, "independent normal/optimized stdout differs")
    adversarial = run_checker([sys.executable, "-B", str(scripts / "adversarial_shell_alignment.py"), "--check"])
    adversarial_opt = run_checker([sys.executable, "-O", "-B", str(scripts / "adversarial_shell_alignment.py"), "--check"])
    require(adversarial.returncode == 0, f"adversarial failed: {adversarial.stderr.decode('utf-8', 'replace')}")
    require(adversarial_opt.returncode == 0, f"optimized adversarial failed: {adversarial_opt.stderr.decode('utf-8', 'replace')}")
    require(adversarial.stdout == adversarial_opt.stdout, "adversarial normal/optimized stdout differs")


def check_pdf() -> None:
    paper_pdf = PAPER / "paper/paper.pdf"
    main_pdf = PAPER / "paper/main.pdf"
    payload = paper_pdf.read_bytes()
    require(payload.startswith(b"%PDF-"), "PDF header")
    require(len(payload) > 100_000, "PDF unexpectedly small")
    require(main_pdf.is_file() and main_pdf.read_bytes() == payload, "paper.pdf differs from main.pdf")


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
        print(f"TPC216_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_adversary"]
    print("TPC216_BRIDGE_CHECK=PASS")
    print("q_count=", len(fixture["q_values"]))
    print("aligned_support=", fixture["aligned_support"])
    print("normalized_exponent=11/32")
    print("claim_level=PROVED_STRUCTURAL_L1_DIRECT_SUM_ROW_ENERGY_ENVELOPE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
