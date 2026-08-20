#!/usr/bin/env python3
"""Fail-closed release checker for TPC-215."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_short_quotient_mobius_majorant.md"
PAPER = ROOT / "papers/tpc-215-short-quotient-mobius-majorant"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC215_MAXIMUM_CLAIM = SOURCE_LOCKED_SHORT_QUOTIENT_MOBIUS_TAIL_NORMAL_FORM_AND_O_LOG_X_SQUARED_COMPLETE_PERIOD_CLUSTER_TO_DIRECT_MAJORANT_WITH_TOP_SHELL_NO_SAVING_OBSTRUCTION",
    "TPC215_ROUTE_ADVANCE = YES",
    "TPC215_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC215_ACTIVATION_FLOOR = PROVED_EXACT",
    "TPC215_ACTIVE_DENOMINATOR_IN_FULL_BAND = PROVED_EXACT",
    "TPC215_SHORT_QUOTIENT_NORMAL_FORM = PROVED_EXACT",
    "TPC215_QUOTIENT_LENGTH_EXPONENT = PROVED_23_OVER_2400",
    "TPC215_ROW_NORM_DIVISOR_DECOMPOSITION = PROVED_EXACT",
    "TPC215_CLUSTER_TO_DIRECT_MAJORANT = PROVED_O_LOG_X_SQUARED",
    "TPC215_FIXED_POWER_CLUSTER_AMPLIFICATION = EXCLUDED",
    "TPC215_TOP_SHELL_RATIO_ONE = PROVED_EXACT",
    "TPC215_UNIFORM_ROWWISE_POWER_SAVING = REFUTED_SCOPED",
    "TPC215_FINITE_RATIOS = NUMERICAL_OBSERVATION",
    "TPC215_DIRECT_SUM_ARITHMETIC_ENERGY_BOUND = OPEN",
    "TPC215_FINITE_WINDOW_OFF_FREQUENCY_GRAM = OPEN",
    "TPC215_PRIME_SHELL_REASSEMBLY = OPEN",
    "TPC215_ARITHMETIC_ADVANCE = NO",
    "TPC215_FIXED_ATOM_CREDIT = 0",
    "TPC215_L2 = NONE",
    "TPC215_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC215_TPC_TRIGGER = true",
)

REQUIRED = (
    ".gitignore",
    "README.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/short_quotient_majorant.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/majorant_sanity.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)

EXPECTED_FIREWALL = {
    "route_advance": "YES",
    "structural_threshold_a": "PASS",
    "activation_floor": "PROVED_EXACT",
    "active_denominator_in_full_band": "PROVED_EXACT",
    "short_quotient_normal_form": "PROVED_EXACT",
    "quotient_length_exponent": "PROVED_23_OVER_2400",
    "row_norm_divisor_decomposition": "PROVED_EXACT",
    "cluster_to_direct_majorant": "PROVED_O_LOG_X_SQUARED",
    "fixed_power_cluster_amplification": "EXCLUDED",
    "top_shell_ratio_one": "PROVED_EXACT",
    "uniform_rowwise_power_saving": "REFUTED_SCOPED",
    "finite_ratios": "NUMERICAL_OBSERVATION",
    "direct_sum_arithmetic_energy_bound": "OPEN",
    "finite_window_off_frequency_gram": "OPEN",
    "prime_shell_reassembly": "OPEN",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "l2": "NONE",
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


def check_layout() -> None:
    require(PROOF.is_file(), "proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    for anchor in (
        "Theorem: activation floor",
        "Exact short-quotient normal form",
        "Theorem: row-norm divisor decomposition",
        "Theorem: cluster-to-direct majorant",
        "Proposition: top-shell ratio one",
        "ROUND2_CLUE = BOUND_THE_DIRECT_SUM_PHYSICAL_ROW_ENERGY",
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
    require(data["schema"] == "TPC215_SHORT_QUOTIENT_MOBIUS_MAJORANT_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT", "classification")
    require(data["source_exponents"] == {
        "H": "21/32",
        "Q": "1/3",
        "U": "133/400",
        "Y0": "31/96",
        "UQ_over_H": "23/2400",
    }, "source exponent ledger")
    require(data["claim_firewall"] == EXPECTED_FIREWALL, "claim firewall")
    fixture = data["finite_fixture"]
    require(fixture["activation_floor"] == 3, "activation floor")
    require(fixture["actual_max_quotient"] == 10, "actual quotient")
    require(fixture["uniform_quotient_bound"] == 14, "uniform quotient")
    require(fixture["active_denominators"] == [3, 5, 6, 7, 10, 14, 15, 19, 21, 23, 29, 30, 31, 35], "active rows")
    require(fixture["top_shell_denominators"] == [19, 21, 23, 29, 30, 31, 35], "top shell")
    require(len(fixture["tail_rows"]) == 14, "tail rows")
    require(all(
        row["multiples"] == [row["denominator"]]
        and row["tail_to_direct_ratio"] == "1"
        for row in fixture["tail_rows"] if row["top_shell"]
    ), "top-shell equality")
    require(fixture["numeric_classification"] == "NUMERICAL_OBSERVATION", "numeric scope")
    require(abs(float(fixture["cluster_to_direct_ratio"]) - 0.59695325876572969) < 1e-15, "global ratio")
    return data


def run_checker(arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    environment = {"PYTHONDONTWRITEBYTECODE": "1"}
    import os

    environment.update(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        arguments,
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def check_subcheckers() -> None:
    scripts = PAPER / "experiments"
    producer = run_checker([sys.executable, "-B", str(scripts / "run_certificate.py"), "--check"])
    require(producer.returncode == 0, f"producer failed: {producer.stderr.decode('utf-8', 'replace')}")
    normal = run_checker([sys.executable, "-B", str(scripts / "independent_checker.py"), "--check"])
    optimized = run_checker([sys.executable, "-O", "-B", str(scripts / "independent_checker.py"), "--check"])
    require(normal.returncode == 0, f"independent failed: {normal.stderr.decode('utf-8', 'replace')}")
    require(optimized.returncode == 0, f"optimized failed: {optimized.stderr.decode('utf-8', 'replace')}")
    require(normal.stdout == optimized.stdout, "normal/optimized stdout differs")
    sanity = run_checker([sys.executable, "-B", str(scripts / "majorant_sanity.py"), "--check"])
    require(sanity.returncode == 0, f"sanity failed: {sanity.stderr.decode('utf-8', 'replace')}")


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
        print(f"TPC215_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    fixture = data["finite_fixture"]
    print("TPC215_BRIDGE_CHECK=PASS")
    print("active_denominators=", len(fixture["active_denominators"]))
    print("top_shell_rows=", len(fixture["top_shell_denominators"]))
    print("quotient_exponent=23/2400")
    print("majorant=O((log x)^2)=x^(o(1))")
    print("claim_level=PROVED_STRUCTURAL_L1_SHORT_QUOTIENT_CLUSTER_MAJORANT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
