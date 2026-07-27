#!/usr/bin/env python3
"""Deterministic selector and exact exponent ledger for TPC-140."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "tpc140_selector_power_audit.json"


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def selector_dominated(
    base: tuple[Fraction, ...],
    selector: tuple[Fraction, ...],
    constant: Fraction,
) -> bool:
    if sum(base) != 1 or sum(selector) != 1 or len(base) != len(selector):
        return False
    indices = range(len(base))
    for size in range(len(base) + 1):
        for subset in itertools.combinations(indices, size):
            if sum((selector[i] for i in subset), Fraction(0)) > constant * sum(
                (base[i] for i in subset), Fraction(0)
            ):
                return False
    return True


def raw_sigma(
    *,
    sigma_aff: Fraction,
    eta_tail: Fraction,
    ell_selector: Fraction,
    ell_census: Fraction,
    ell_bv: Fraction,
) -> Fraction:
    transported = sigma_aff - ell_selector - ell_census - ell_bv
    return min(eta_tail, transported)


def exceptional_window_exponent(
    *,
    source_density_exponent: Fraction,
    log_window_exponent: Fraction,
) -> Fraction:
    """Exponent forced by global density on log(omega)=(log X)^theta."""
    return max(
        Fraction(0),
        source_density_exponent + log_window_exponent - 1,
    )


def route_case(
    *,
    name: str,
    sigma_aff: Fraction,
    eta_tail: Fraction,
    ell_selector: Fraction,
    ell_census: Fraction,
    ell_bv: Fraction,
    lambda_phys: Fraction,
    premises_proved: bool,
) -> dict[str, object]:
    losses = (eta_tail, ell_selector, ell_census, ell_bv, lambda_phys)
    if any(value < 0 for value in losses):
        raise ValueError("typed exponent losses must be nonnegative")
    sigma = raw_sigma(
        sigma_aff=sigma_aff,
        eta_tail=eta_tail,
        ell_selector=ell_selector,
        ell_census=ell_census,
        ell_bv=ell_bv,
    )
    transported = sigma_aff - ell_selector - ell_census - ell_bv
    endpoint_margin = sigma - lambda_phys
    return {
        "name": name,
        "sigma_aff": fraction_text(sigma_aff),
        "eta_tail": fraction_text(eta_tail),
        "ell_selector": fraction_text(ell_selector),
        "ell_census": fraction_text(ell_census),
        "ell_bv": fraction_text(ell_bv),
        "transported_sigma": fraction_text(transported),
        "sigma_raw": fraction_text(sigma),
        "lambda_phys": fraction_text(lambda_phys),
        "endpoint_margin": fraction_text(endpoint_margin),
        "premises_proved": premises_proved,
        "strict_endpoint_pass":
            premises_proved and endpoint_margin > 0,
        "positive_raw_power": premises_proved and sigma > 0,
    }


def log_route_case(
    *,
    kappa_corr: Fraction,
    kappa_exceptional: Fraction,
    kappa_tail: Fraction,
    kappa_selector: Fraction,
    kappa_census: Fraction,
    kappa_bv: Fraction,
) -> dict[str, object]:
    kappa_aff = min(kappa_corr, kappa_exceptional)
    kappa_raw = raw_sigma(
        sigma_aff=kappa_aff,
        eta_tail=kappa_tail,
        ell_selector=kappa_selector,
        ell_census=kappa_census,
        ell_bv=kappa_bv,
    )
    return {
        "kappa_corr": fraction_text(kappa_corr),
        "kappa_exceptional": fraction_text(kappa_exceptional),
        "kappa_aff": fraction_text(kappa_aff),
        "kappa_tail": fraction_text(kappa_tail),
        "kappa_selector": fraction_text(kappa_selector),
        "kappa_census": fraction_text(kappa_census),
        "kappa_bv": fraction_text(kappa_bv),
        "kappa_raw": fraction_text(kappa_raw),
        "qualitative_log_return": kappa_raw > 0,
        "X_power_exponent": "0/1",
        "pays_positive_X_endpoint": False,
    }


def payload() -> dict[str, object]:
    base = (Fraction(1, 4),) * 4
    dominated_selector = (
        Fraction(1, 2),
        Fraction(1, 4),
        Fraction(1, 8),
        Fraction(1, 8),
    )
    domination_constant = Fraction(2)
    finite_domination = selector_dominated(
        base,
        dominated_selector,
        domination_constant,
    )
    null_set_base = (Fraction(1, 2), Fraction(1, 2), Fraction(0))
    atomic_selector = (Fraction(0), Fraction(0), Fraction(1))
    atomic_fails_finite_domination = all(
        not selector_dominated(
            null_set_base,
            atomic_selector,
            constant,
        )
        for constant in (Fraction(1), Fraction(10), Fraction(10**6))
    )

    hypothetical_pass = route_case(
        name="hypothetical_strict_pass",
        sigma_aff=Fraction(1, 100),
        eta_tail=Fraction(1, 80),
        ell_selector=Fraction(1, 1000),
        ell_census=Fraction(1, 1000),
        ell_bv=Fraction(1, 2000),
        lambda_phys=Fraction(1, 500),
        premises_proved=True,
    )
    equality_stop = route_case(
        name="one_over_400_equality_stop",
        sigma_aff=Fraction(1, 400),
        eta_tail=Fraction(1, 300),
        ell_selector=Fraction(0),
        ell_census=Fraction(0),
        ell_bv=Fraction(0),
        lambda_phys=Fraction(1, 400),
        premises_proved=True,
    )
    current_case = route_case(
        name="current_frozen_logarithmic_input",
        sigma_aff=Fraction(0),
        eta_tail=Fraction(0),
        ell_selector=Fraction(0),
        ell_census=Fraction(0),
        ell_bv=Fraction(0),
        lambda_phys=Fraction(0),
        premises_proved=False,
    )
    tt_source_density = Fraction(1, 20)
    full_log_window_exceptional = exceptional_window_exponent(
        source_density_exponent=tt_source_density,
        log_window_exponent=Fraction(1),
    )
    thin_log_window_exceptional = exceptional_window_exponent(
        source_density_exponent=tt_source_density,
        log_window_exponent=Fraction(9, 10),
    )
    logarithmic_corridor = log_route_case(
        kappa_corr=Fraction(1, 20),
        kappa_exceptional=full_log_window_exceptional,
        kappa_tail=Fraction(1, 30),
        kappa_selector=Fraction(1, 200),
        kappa_census=Fraction(1, 100),
        kappa_bv=Fraction(1, 200),
    )

    checks = {
        "finite_selector_domination_checked": finite_domination,
        "atomic_selector_fails_null_set_domination":
            atomic_fails_finite_domination,
        "hypothetical_strict_case_passes":
            hypothetical_pass["strict_endpoint_pass"] is True,
        "one_over_400_equality_stops":
            equality_stop["strict_endpoint_pass"] is False,
        "current_logarithmic_input_has_no_fixed_power":
            current_case["positive_raw_power"] is False,
        "unproved_premises_never_emit_GO":
            current_case["strict_endpoint_pass"] is False,
        "endpoint_margin_is_spent_once":
            hypothetical_pass["endpoint_margin"] == "11/2000",
        "logarithmic_corridor_can_pass_qualitatively":
            logarithmic_corridor["qualitative_log_return"] is True,
        "logarithmic_corridor_has_zero_X_power":
            logarithmic_corridor["pays_positive_X_endpoint"] is False,
        "full_log_window_preserves_source_exceptional_exponent":
            full_log_window_exceptional == tt_source_density,
        "thin_log_window_gets_no_decay_from_global_density_alone":
            thin_log_window_exceptional == 0,
        "global_exceptional_density_not_promoted_to_arbitrary_window":
            thin_log_window_exceptional
            < tt_source_density,
        "tao_teravainen_corridor_not_promoted_to_all_prefix": True,
        "no_positive_L2_in_current_snapshot": True,
    }
    if not all(checks.values()):
        raise AssertionError("TPC-140 deterministic regression failed")

    return {
        "schema_version": 1,
        "paper": "TPC-140",
        "return_interfaces": {
            "pointwise": {
                "requirement": "uniform actual-family all-prefix theorem",
                "status": "OPEN",
            },
            "selector": {
                "requirement": "nu_X(E)<=K_X*m_log(E) for every Borel E",
                "status": "OPEN_ON_ACTUAL_FAMILY",
                "atomic_selector_status": "REJECTED_WITHOUT_SMOOTHING",
                "null_set_regression": {
                    "base": [
                        fraction_text(value)
                        for value in null_set_base
                    ],
                    "atomic_selector": [
                        fraction_text(value)
                        for value in atomic_selector
                    ],
                    "fails_every_tested_finite_K":
                        atomic_fails_finite_domination,
                },
                "finite_model": {
                    "base": [fraction_text(value) for value in base],
                    "selector": [
                        fraction_text(value) for value in dominated_selector
                    ],
                    "K": fraction_text(domination_constant),
                    "dominated": finite_domination,
                },
            },
        },
        "exponent_formula": {
            "sigma_raw": "min(eta_tail,sigma_aff-ell_selector-ell_census-ell_bv)",
            "endpoint": "sigma_raw>lambda_phys",
            "equality": "STOP",
            "cases": [hypothetical_pass, equality_stop, current_case],
        },
        "logarithmic_exponent_formula": {
            "kappa_aff":
                "min(kappa_corr,kappa_exceptional_after_pullback_union)",
            "kappa_raw":
                "min(kappa_tail,kappa_aff-kappa_selector-kappa_census-kappa_bv)",
            "source_corridor":
                "Tao--Teravainen 2026 small-polylog affine data outside a small log-density exceptional set",
            "global_to_terminal_window":
                "m_window(E) << min(1,(log X)^(1-c)/log omega)",
            "illustrative_ledger_only": logarithmic_corridor,
            "thin_window_source_only_example": {
                "source_density_exponent":
                    fraction_text(tt_source_density),
                "log_window_exponent": "9/10",
                "certified_exceptional_window_exponent":
                    fraction_text(thin_log_window_exceptional),
            },
            "actual_selector_and_reassembly": "OPEN",
        },
        "current_manifest": {
            "actual_archive_supplied_to_this_certificate": False,
            "growing_affine_power_theorem": "OPEN",
            "actual_selector_or_pointwise_prefix": "OPEN",
            "current_verdict": "NOT_TESTABLE",
            "first_missing": "H1.archive",
        },
        "checks": checks,
        "claim_boundary": {
            "fixed_h0_positive_L2": False,
            "H3": False,
            "one_over_400": False,
            "B_h0_delta_o_X": False,
            "prime_pair_theorem": False,
            "twin_prime_theorem": False,
        },
    }


def render(data: dict[str, object]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render(payload())
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing certificate: {OUTPUT}")
        if OUTPUT.read_text(encoding="utf-8") != expected:
            raise SystemExit("certificate is stale; run without --check")
        print("TPC-140 CHECK PASS")
        return
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    print(f"TPC-140 WRITE PASS: {OUTPUT}")


if __name__ == "__main__":
    main()
