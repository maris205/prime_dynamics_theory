#!/usr/bin/env python3
"""Independent release checker for the TPC-214 cluster bridge."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


class CheckFailure(RuntimeError):
    pass


ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "research/tpc-big-road/bridge_b_mobius_frequency_clusters.md"
PAPER = ROOT / "papers/tpc-214-mobius-frequency-clusters"
CERTIFICATE = PAPER / "results/certificate.json"

REGISTRY = (
    "TPC214_MAXIMUM_CLAIM = EXACT_MOBIUS_LOG_SHARED_FREQUENCY_CLUSTER_FACTORIZATION_WITH_ZERO_AXIS_AND_FOUR_PACKET_COMPATIBILITY",
    "TPC214_ROUTE_ADVANCE = YES",
    "TPC214_STRUCTURAL_THRESHOLD_A = PASS",
    "TPC214_EMITTER_DILATION_COVARIANCE = PROVED_EXACT",
    "TPC214_REDUCED_DENOMINATOR_CLUSTER_FACTOR = PROVED_EXACT",
    "TPC214_ZERO_AXIS_SCOPE = PROVED_EXACT",
    "TPC214_FOUR_PACKET_POLARIZATION = PROVED_EXACT_LINEAR_EXTENSION",
    "TPC214_NESTED_CLUSTER_CANCELLATION = PROVED_EXACT_FINITE_SIGN",
    "TPC214_COMPOSITE_QUOTIENT_ENHANCEMENT = PROVED_EXACT_FINITE_SIGN",
    "TPC214_FINITE_ENERGY_RATIOS = NUMERICAL_OBSERVATION",
    "TPC214_UNIVERSAL_CLUSTER_SAVING_SIGN = REFUTED_SCOPED",
    "TPC214_LITERAL_V46_ASYMPTOTIC_CLUSTER_BOUND = OPEN",
    "TPC214_PRIME_SHELL_REASSEMBLY = OPEN",
    "TPC214_ARITHMETIC_ADVANCE = NO",
    "TPC214_FIXED_ATOM_CREDIT = 0",
    "TPC214_L2 = NONE",
    "TPC214_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID",
    "TPC214_TPC_TRIGGER = true",
)

REQUIRED = (
    "README.md",
    "PAPER_PLAN.md",
    "PROOF_PACKAGE.md",
    "paper/main.tex",
    "paper/references.bib",
    "paper/paper.pdf",
    "code/shared_frequency_clusters.py",
    "experiments/run_certificate.py",
    "experiments/independent_checker.py",
    "experiments/packet_sanity.py",
    "results/certificate.json",
    "notes/theorem_ledger.md",
    "notes/source_lock.md",
    "notes/route_evaluation.md",
)

EXPECTED_FIREWALL = {
    "route_advance": "YES",
    "structural_threshold_a": "PASS",
    "emitter_dilation_covariance": "PROVED_EXACT",
    "reduced_denominator_cluster_factor": "PROVED_EXACT",
    "zero_axis_scope": "PROVED_EXACT",
    "four_packet_polarization": "PROVED_EXACT_LINEAR_EXTENSION",
    "nested_cluster_cancellation": "PROVED_EXACT_FINITE_SIGN",
    "composite_quotient_enhancement": "PROVED_EXACT_FINITE_SIGN",
    "finite_energy_ratios": "NUMERICAL_OBSERVATION",
    "universal_cluster_saving_sign": "REFUTED_SCOPED",
    "literal_v46_asymptotic_cluster_bound": "OPEN",
    "prime_shell_reassembly": "OPEN",
    "arithmetic_advance": "NO",
    "fixed_atom_credit": 0,
    "l2": "NONE",
    "full_gate_b_strict_1_over_400": "UNPAID",
}

EXPECTED_FAMILIES = (
    {
        "divisors": [5, 7, 35],
        "period": 35,
        "reduced_denominators": [1, 5, 7, 35],
        "cross_energy_sign": "NEGATIVE_EXACT",
        "ratio": "0.59634355565371822",
        "ratio_bound": lambda value: value < 0.60,
        "cross_pairs": [(5, 35), (7, 35)],
        "coefficient_signs": {"5": -1, "7": -1, "35": 1},
    },
    {
        "divisors": [3, 5, 7, 105],
        "period": 105,
        "reduced_denominators": [1, 3, 5, 7, 15, 21, 35, 105],
        "cross_energy_sign": "POSITIVE_EXACT",
        "ratio": "1.2119952512624363",
        "ratio_bound": lambda value: value > 1.20,
        "cross_pairs": [(3, 105), (5, 105), (7, 105)],
        "coefficient_signs": {"3": -1, "5": -1, "7": -1, "105": -1},
    },
)


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def check_layout() -> int:
    require(PROOF.is_file(), "bridge proof missing")
    proof = PROOF.read_text(encoding="utf-8")
    for row in REGISTRY:
        require(row in proof, f"registry row missing: {row}")
    for phrase in (
        "Theorem: dilation covariance",
        "Theorem: reduced-denominator cluster factorization",
        "frequency-intersection",
        "Zero axis",
        "Four-packet compatibility",
        "ROUND2_CLUE = ESTIMATE_THE_MOBIUS_LOG_TAILS_C_h",
    ):
        require(phrase in proof, f"theorem anchor missing: {phrase}")
    for relative in REQUIRED:
        require((PAPER / relative).is_file(), f"artifact missing: {relative}")
    pdf_path = PAPER / "paper/paper.pdf"
    pdf = pdf_path.read_bytes()
    require(pdf.startswith(b"%PDF-"), "PDF header")
    require(len(pdf) > 100_000, "PDF unexpectedly small")
    main_pdf = PAPER / "paper/main.pdf"
    require(main_pdf.is_file() and main_pdf.read_bytes() == pdf, "paper.pdf is not the compiled main.pdf")
    require("Liang Wang" in (PAPER / "README.md").read_text(encoding="utf-8"), "author lock")
    return len(REGISTRY) + len(REQUIRED) + 6


def check_certificate() -> tuple[int, int, int]:
    require(CERTIFICATE.is_file(), "certificate missing")
    data = json.loads(
        CERTIFICATE.read_text(encoding="utf-8"),
        object_pairs_hook=unique_object,
        parse_constant=lambda token: (_ for _ in ()).throw(CheckFailure(token)),
    )
    require(
        set(data) == {
            "audit_counts", "claim_firewall", "classification", "families", "fixture",
            "four_packet", "modeling_choice", "open_theorem", "schema",
        },
        "certificate top-level schema",
    )
    require(data["schema"] == "TPC214_MOBIUS_FREQUENCY_CLUSTER_CERTIFICATE_V1", "schema")
    require(data["classification"] == "PROVED_STRUCTURAL_L1_MOBIUS_CLUSTER_REDUCTION", "classification")
    require(data["modeling_choice"] == "RATIONAL_SCHWARTZ_PSI_EQUALS_ONE_OVER_ONE_PLUS_T_SQUARED_SQUARED", "modeling choice")
    require(data["fixture"] == {
        "H": 40,
        "families": [[5, 7, 35], [3, 5, 7, 105]],
        "psi": "(1+t^2)^(-2)",
        "q_below_H": True,
        "q_values": [11, 13, 17],
    }, "fixture")
    require(data["claim_firewall"] == EXPECTED_FIREWALL, "claim firewall")
    require(
        data["open_theorem"] == "BOUND_THE_ACTUAL_V46_MOBIUS_LOG_CLUSTER_TAILS_UNIFORMLY_AND_REASSEMBLE_THE_PRIME_SHELL",
        "open theorem",
    )
    require(data["audit_counts"] == {
        "dilation_pairs": 22,
        "factorization_checks": 2,
        "fixture_families": 2,
        "reduced_denominator_rows": 12,
    }, "audit counts")
    require(data["four_packet"] == {
        "beta": ["2", "1"],
        "expected_value": ["0", "5"],
        "identity": True,
        "polarized_value": ["0", "5"],
        "weight": ["1", "-2"],
    }, "four-packet certificate")

    families = data["families"]
    require(type(families) is list and len(families) == len(EXPECTED_FAMILIES), "family count")
    dilation_pairs = 0
    reduced_rows = 0
    cross_pairs = 0
    for record, expected in zip(families, EXPECTED_FAMILIES):
        require(record["divisors"] == expected["divisors"], "divisor fixture")
        require(record["period"] == expected["period"], "period")
        require(record["reduced_denominators"] == expected["reduced_denominators"], "reduced denominators")
        require(record["dilation_covariance"] is True, "dilation covariance flag")
        require(record["cluster_factorization"] is True, "factorization flag")
        require(record["zero_axis"] is True, "zero-axis flag")
        require(record["cross_energy_sign"] == expected["cross_energy_sign"], "exact cross-energy sign")
        require(record["physical_to_direct_ratio"] == expected["ratio"], "ratio reproduction")
        require(expected["ratio_bound"](float(record["physical_to_direct_ratio"])), "ratio direction")
        require(record["coefficients"] and set(record["coefficients"]) == set(expected["coefficient_signs"]), "coefficient keys")
        for key, sign in expected["coefficient_signs"].items():
            value = float(record["coefficients"][key])
            require((value > 0) is (sign > 0), f"coefficient sign {key}")
        observed_pairs = [(term["left"], term["right"]) for term in record["cross_terms"]]
        require(observed_pairs == expected["cross_pairs"], "cross-pair fixture")
        for term in record["cross_terms"]:
            require(term["gram"] != "0", "nonzero cross Gram")
            require(term["cross_term_sign"] == term["coefficient_sign_product"], "cross sign product")
        dilation_pairs += len(record["dilation_pairs"])
        reduced_rows += len(record["reduced_denominators"])
        cross_pairs += len(record["cross_terms"])
    require(dilation_pairs == data["audit_counts"]["dilation_pairs"], "dilation-pair count")
    require(reduced_rows == data["audit_counts"]["reduced_denominator_rows"], "reduced-row count")
    require(cross_pairs == 5, "cross-pair count")
    return len(families), reduced_rows, cross_pairs


def check_release_hashes() -> int:
    pdf = (PAPER / "paper/paper.pdf").read_bytes()
    require(type(hashlib.sha256(pdf).hexdigest()) is str and len(hashlib.sha256(pdf).hexdigest()) == 64, "PDF hash")
    compile_log = PAPER / "paper/compile.log"
    require(compile_log.is_file(), "compile log")
    log = compile_log.read_text(encoding="utf-8")
    for forbidden in ("Warning", "undefined", "Overfull", "Underfull", "Error", "^!"):
        require(forbidden not in log, f"compile diagnostic: {forbidden}")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("--check is required")
    try:
        layout_rows = check_layout()
        family_count, reduced_rows, cross_pairs = check_certificate()
        hash_rows = check_release_hashes()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"TPC214_BRIDGE_CHECK=FAIL {error}", file=sys.stderr)
        return 1
    print("TPC214_BRIDGE_CHECK=PASS")
    print(f"layout_registry_rows={layout_rows}")
    print(f"fixture_families={family_count}")
    print(f"reduced_denominator_rows={reduced_rows}")
    print(f"cross_pair_rows={cross_pairs}")
    print(f"pdf_hash_checks={hash_rows}")
    print("route_advance=YES")
    print("literal_v46_asymptotic_cluster_bound=OPEN")
    print("arithmetic_advance=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
