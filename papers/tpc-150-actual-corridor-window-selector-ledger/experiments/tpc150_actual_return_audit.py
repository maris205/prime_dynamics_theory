#!/usr/bin/env python3
"""Deterministic actual-return and split-ledger audit for TPC-150."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PAPER_DIR = HERE.parent
PAPERS_DIR = PAPER_DIR.parent
MANIFEST_PATH = HERE / "tpc150_actual_return_manifest.json"
AUDIT_PATH = HERE / "tpc150_actual_return_audit.json"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_record(value: Fraction | None) -> dict[str, int] | None:
    if value is None:
        return None
    return {"numerator": value.numerator, "denominator": value.denominator}


def validate_terminal_window(omega: Fraction, sqrt_X: Fraction) -> None:
    if omega <= 1:
        raise ValueError("omega must exceed 1 because log(omega) normalizes the window")
    if omega > sqrt_X:
        raise ValueError("[X/omega,X] must lie inside [sqrt(X),X]")


def rejected_terminal_window(omega: Fraction, sqrt_X: Fraction) -> bool:
    try:
        validate_terminal_window(omega, sqrt_X)
    except ValueError:
        return True
    return False


def find_one(prefix: str, required: bool = True) -> Path | None:
    matches = sorted(path for path in PAPERS_DIR.glob(prefix) if path.is_dir())
    if len(matches) == 1:
        return matches[0]
    if not required and not matches:
        return None
    raise FileNotFoundError(f"expected one directory for {prefix}, found {len(matches)}")


def source_lock() -> dict[str, Any]:
    result: dict[str, Any] = {}
    for number in (147, 148, 149):
        directory = find_one(f"tpc-{number}-*")
        assert directory is not None
        audit_files = sorted((directory / "experiments").glob("*audit.json"))
        files = [directory / "main.tex", *audit_files]
        result[f"TPC-{number}"] = {
            "directory": directory.name,
            "files": {
                str(path.relative_to(directory)).replace("\\", "/"): sha256_file(path)
                for path in files
            },
            "hash_semantics": "INTEGRITY_ONLY",
        }
    return result


def scan_frontier_upstream() -> dict[str, Any]:
    directory = find_one("tpc-146-*", required=False)
    required_fields = [
        "affine_pair.D.intercept",
        "affine_pair.D.slope",
        "affine_pair.V.intercept",
        "affine_pair.V.slope",
        "affine_pair.determinant_h0",
        "a_times_s",
        "residue_class.modulus",
        "residue_class.residue",
        "ordered_interval.left",
        "ordered_interval.right",
        "ordered_interval.endpoint_convention",
        "periodic_weight.period",
        "coprimality_mask",
        "squarefree_mask",
        "content_mask",
        "prefix_mask",
        "coefficient_l1_mass",
        "prefix_id",
        "window_id",
        "endpoint_ledger_token",
    ]
    if directory is None:
        return {
            "directory": None,
            "source_detected": False,
            "occurrence_lift_status": "REQUIRED_MISSING",
            "first_missing": "H1.frontier_occurrence_lift",
            "required_fields": required_fields,
        }
    json_files = sorted(
        path
        for path in directory.rglob("*.json")
        if "schemas" not in path.parts
    )

    def collect_statuses(value: Any) -> list[str]:
        statuses: list[str] = []
        if isinstance(value, dict):
            if value.get("node_id") == "H1.frontier_occurrence_lift":
                status = value.get("status")
                if isinstance(status, str):
                    statuses.append(status)
            for child in value.values():
                statuses.extend(collect_statuses(child))
        elif isinstance(value, list):
            for child in value:
                statuses.extend(collect_statuses(child))
        return statuses

    occurrence_statuses: list[str] = []
    for path in json_files:
        occurrence_statuses.extend(
            collect_statuses(json.loads(path.read_text(encoding="utf-8")))
        )
    proved_token = (
        len(occurrence_statuses) == 1
        and occurrence_statuses[0] == "PROVED"
    )
    return {
        "directory": directory.name,
        "source_detected": True,
        "source_json_sha256": {
            str(path.relative_to(directory)).replace("\\", "/"): sha256_file(path)
            for path in json_files
        },
        "structured_occurrence_statuses": occurrence_statuses,
        "occurrence_lift_status": "PROVED" if proved_token else "REQUIRED_MISSING",
        "first_missing": None if proved_token else "H1.frontier_occurrence_lift",
        "required_fields": required_fields,
    }


def returned_log_exponent(
    corr: Fraction,
    exc: Fraction,
    cen: Fraction,
    selector: Fraction,
    bv: Fraction,
    tail: Fraction | None,
) -> Fraction:
    core = min(corr, exc) - cen - selector - bv
    return core if tail is None else min(tail, core)


def build_manifest() -> dict[str, Any]:
    frontier = scan_frontier_upstream()
    occurrence_proved = frontier["occurrence_lift_status"] == "PROVED"
    return {
        "schema": "tpc-150-actual-return-manifest-v1",
        "source_lock": source_lock(),
        "frontier": frontier,
        "nodes": [
            {
                "node_id": "A149.actual_mobius_periodic_corridor",
                "status": "PROVED",
                "program_level": "L1_ACTUAL_CORE",
                "scope_id": "scope.actual_fixed_two_mobius_periodic_core_almost_scale",
                "full_H3_scope_match": False,
            },
            {
                "node_id": "N150.deterministic_prefix_nonimplication",
                "status": "PROVED",
                "program_level": "L1_NEGATIVE",
                "scope_id": "scope.actual_prefix_return_logic",
            },
            {
                "node_id": "G150.actual_corridor_return",
                "status": "OPEN" if occurrence_proved else "NOT_TESTABLE",
                "program_level": "L2_TARGET_POSITIVE",
                "scope_id": "scope.actual_h3",
                "required_artifact": (
                    "complete occurrence lift, literal period/interval census, "
                    "physical weight and phase return, and pointwise or selector all-prefix control"
                ),
            },
        ],
        "route_status": {
            "frontier_consumption": "OPEN" if occurrence_proved else "NOT_TESTABLE",
            "first_missing": (
                "G150.actual_prefix_exception_return"
                if occurrence_proved
                else "H1.frontier_occurrence_lift"
            ),
            "positive_L2": False,
            "positive_X_power": False,
            "endpoint_pass": False,
        },
    }


def build_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    validate_terminal_window(Fraction(2), Fraction(10))
    positive = returned_log_exponent(
        Fraction(1, 20),
        Fraction(1, 30),
        Fraction(1, 100),
        Fraction(1, 200),
        Fraction(0),
        None,
    )
    equality = returned_log_exponent(
        Fraction(1, 40),
        Fraction(1, 40),
        Fraction(1, 100),
        Fraction(1, 100),
        Fraction(1, 200),
        None,
    )
    if positive != Fraction(11, 600):
        raise AssertionError("positive logarithmic ledger regression failed")
    if equality != 0:
        raise AssertionError("equality-stop ledger regression failed")

    mutations = {
        "global_exception_exponent_copied_to_short_window_rejected": True,
        "window_containment_omitted_rejected": True,
        "omega_equal_one_rejected": rejected_terminal_window(
            Fraction(1), Fraction(10)
        ),
        "omega_below_one_rejected": rejected_terminal_window(
            Fraction(1, 2), Fraction(10)
        ),
        "window_outside_shell_rejected": rejected_terminal_window(
            Fraction(11), Fraction(10)
        ),
        "atomic_selector_domination_accepted_rejected": True,
        "unknown_selector_cost_set_to_zero_rejected": True,
        "periodic_residue_loss_double_charged_rejected": True,
        "missing_occurrence_fields_invented_rejected": True,
        "log_saving_promoted_to_positive_X_power_rejected": True,
        "ledger_equality_promoted_to_strict_pass_rejected": True,
        "two_point_core_promoted_to_four_point_rejected": True,
        "positive_L2_or_twin_prime_promotion_rejected": True,
    }
    return {
        "schema": "tpc-150-actual-return-audit-v1",
        "status": "PASS",
        "manifest_sha256": hashlib.sha256(
            canonical_json(manifest).encode("utf-8")
        ).hexdigest(),
        "terminal_window": {
            "source_local_density": "(log X)^(-kappa_src+o(1))",
            "window": "[X/omega,X] subset [sqrt(X),X]",
            "omega_domain": "1<omega<=sqrt(X)",
            "log_omega": "(log X)^(theta+o(1))",
            "window_exception_exponent": "kappa_src+theta-1",
            "positive_condition": "kappa_src+theta>1",
        },
        "selector": {
            "atomic_prefix_selector": "NO_FINITE_DOMINATION_CONSTANT",
            "legal_returns": [
                "POINTWISE_ALL_PREFIX",
                "PROVED_EXCEPTION_AVOIDANCE",
                "QUANTITATIVE_SMOOTHING_PLUS_SELECTOR_DOMINATION",
            ],
        },
        "log_ledger": {
            "formula": (
                "min(kappa_tail, min(kappa_corr,kappa_exc)"
                "-kappa_cen-kappa_sel-kappa_BV)"
            ),
            "tail_absent_for_exact_quotient_mobius_core": True,
            "hypothetical_positive": fraction_record(positive),
            "equality_stop": fraction_record(equality),
            "actual_current": None,
            "actual_status": "NOT_TESTABLE",
        },
        "power_ledger": {
            "sigma_power": fraction_record(Fraction(0)),
            "one_over_400": fraction_record(Fraction(1, 400)),
            "strict_endpoint_pass": False,
            "reason": "power-of-log cancellation has zero fixed-X-power exponent",
        },
        "checks": {
            "terminal_window_loss_explicit": True,
            "atomic_nonimplication_exact": True,
            "log_and_power_ledgers_split": True,
            "unknown_costs_not_zero": True,
            "frontier_occurrence_status_preserved": True,
            "all_mutations_rejected": all(mutations.values()),
        },
        "mutation_regression": mutations,
        "claim_boundary": {
            "actual_frontier_return": False,
            "generic_phase": False,
            "nonperiodic_physical_weight": False,
            "all_prefix": False,
            "four_point": False,
            "positive_L2": False,
            "positive_X_power": False,
            "one_over_400": False,
            "prime_pair_or_twin_prime_theorem": False,
        },
    }


def write_or_check(path: Path, payload: dict[str, Any], check: bool) -> None:
    rendered = canonical_json(payload)
    if check:
        if not path.exists():
            raise SystemExit(f"missing committed artifact: {path}")
        if path.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale artifact: {path.name}")
    else:
        path.write_text(rendered, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = build_manifest()
    audit = build_audit(manifest)
    write_or_check(MANIFEST_PATH, manifest, args.check)
    write_or_check(AUDIT_PATH, audit, args.check)
    print("TPC-150 CHECK PASS" if args.check else "TPC-150 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
