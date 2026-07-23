"""Audit the uniform price/stopped-law boundary from RH-96 and RH-102."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from quotient_law import (  # noqa: E402
    gap_weighted_loss,
    quotient_decay_exponent,
    quotient_growth_power,
    total_debit_upper,
    total_price_fits,
)


FULL_OUTPUT = ROOT / "results" / "uniform_quotient_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "uniform_quotient_smoke.json"
THRESHOLDS = ("1e-08", "1e-06", "1e-04")


def load(path: str) -> dict[str, object]:
    return json.loads((PAPERS / path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    weak = load("RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json")
    stopped = load("RH-102-stopped-hybrid-quotient-clock/results/stopped_hybrid_clock_audit.json")
    weak_rows = weak["rows"][:2] if args.smoke else weak["rows"]
    stopped_rows = stopped["rows"][:2] if args.smoke else stopped["rows"]

    thresholds = []
    all_events = []
    for threshold in THRESHOLDS:
        events = []
        for row in weak_rows:
            for channel in row["channels"]:
                chain = channel["chains"][threshold]
                for step in chain["steps"]:
                    if step["retained_to_omitted_gap_lower"] is None:
                        continue
                    coupling = float(step["omitted_cross_frobenius_upper"])
                    gap = float(step["retained_to_omitted_gap_lower"])
                    price = gap_weighted_loss(coupling, gap)
                    raw_ratio = price / max(float(step["gap_weighted_tail_loss_bound"]), math.ulp(0.0))
                    event = {
                        "sigma": float(row["sigma"]),
                        "side": channel["side"],
                        "time": step["time"],
                        "threshold": float(step["threshold"]),
                        "coupling_upper": coupling,
                        "gap_lower": gap,
                        "quotient_price_upper": price,
                        "archived_gap_bound_upper": float(step["gap_weighted_tail_loss_bound"]),
                        "price_recomposition_ratio": raw_ratio,
                        "gap_certificate_green": bool(step["gap_certificate_green"]),
                    }
                    events.append(event)
                    all_events.append(event)
        stopped_chains = [
            channel["chains"][threshold]
            for row in stopped_rows
            for channel in row["channels"]
        ]
        replay_ratios = [
            event["propagated_debit_abs_upper"] / event["local_gap_weighted_tail_loss_bound"]
            for chain in stopped_chains
            for event in chain["events"]
            if event["local_gap_weighted_tail_loss_bound"] > 0.0
        ]
        local_prices = [event["quotient_price_upper"] for event in events]
        gaps = [event["gap_lower"] for event in events]
        threshold_record = {
            "threshold": float(threshold),
            "candidate_count": len(events),
            "accepted_count": sum(chain["accepted_quotient_count"] for chain in stopped_chains),
            "rejected_count": sum(chain["rejected_quotient_count"] for chain in stopped_chains),
            "stopped_channel_count": sum(bool(chain["stopped"]) for chain in stopped_chains),
            "all_local_gap_certificates_green": all(event["gap_certificate_green"] for event in events),
            "minimum_gap_lower": min(gaps) if gaps else None,
            "maximum_quotient_price_upper": max(local_prices) if local_prices else 0.0,
            "maximum_price_recomposition_ratio": max(event["price_recomposition_ratio"] for event in events) if events else 1.0,
            "maximum_replay_multiplier": max(replay_ratios) if replay_ratios else 0.0,
            "maximum_spent_fraction_of_allowance": max(
                chain["spent_budget"] / chain["stopped_allowance"]
                if chain["stopped_allowance"] > 0.0 else 0.0
                for chain in stopped_chains
            ),
            "maximum_unrestricted_endpoint_to_reference_ratio": max(
                chain["unrestricted"]["interval_endpoint_to_reference_upper"] for chain in stopped_chains
            ),
            "maximum_stopped_endpoint_to_reference_ratio": max(
                chain["interval_final_endpoint_to_reference_upper"] for chain in stopped_chains
            ),
            "unrestricted_endpoint_green_count": sum(
                chain["unrestricted"]["interval_endpoint_to_reference_upper"] < stopped["endpoint_gate"]
                for chain in stopped_chains
            ),
            "stopped_endpoint_green_count": sum(bool(chain["endpoint_gate_green"]) for chain in stopped_chains),
        }
        thresholds.append(threshold_record)

    # A model family demonstrating that a collapsing gap is harmless when the
    # cross energy collapses faster, and harmful when it does not.
    ratio_rows = []
    for exponent in range(1, 7):
        sigma = 10.0 ** (-exponent)
        gap = sigma
        good_coupling = sigma**1.25
        bad_coupling = sigma**0.5
        ratio_rows.append(
            {
                "sigma": sigma,
                "gap": gap,
                "good_coupling": good_coupling,
                "good_price": good_coupling**2 / gap,
                "bad_coupling": bad_coupling,
                "bad_price": bad_coupling**2 / gap,
            }
        )
    ratio_principle = {
        "good_family": "g=sigma, c=sigma^(5/4), c^2/g=sigma^(3/2)",
        "bad_family": "g=sigma, c=sigma^(1/2), c^2/g=1",
        "rows": ratio_rows,
    }

    scenarios = []
    for name, chi, gamma, propagation in (
        ("balanced_price", 1.0, 1.0, 0.0),
        ("gap_collapses_but_price_decays", 1.25, 1.0, 0.0),
        ("gap_collapses_without_cross_decay", 0.5, 1.0, 0.0),
        ("propagation_consumes_margin", 0.5, 1.0, 0.25),
    ):
        signed = quotient_decay_exponent(chi, gamma, propagation)
        scenarios.append(
            {
                "name": name,
                "coupling_decay_exponent": chi,
                "gap_decay_exponent": gamma,
                "propagation_growth_exponent": propagation,
                "signed_price_decay_exponent": signed,
                "price_growth_power": quotient_growth_power(chi, gamma, propagation),
                "zero_power": signed >= 0.0,
            }
        )

    summary = {
        "threshold_count": len(thresholds),
        "candidate_count": sum(record["candidate_count"] for record in thresholds),
        "accepted_count": sum(record["accepted_count"] for record in thresholds),
        "rejected_count": sum(record["rejected_count"] for record in thresholds),
        "all_local_gap_certificates_green": all(record["all_local_gap_certificates_green"] for record in thresholds),
        "maximum_local_price_upper": max(record["maximum_quotient_price_upper"] for record in thresholds),
        "maximum_replay_multiplier": max(record["maximum_replay_multiplier"] for record in thresholds),
        "minimum_gap_lower": min(record["minimum_gap_lower"] for record in thresholds),
        "maximum_stopped_endpoint_ratio": max(record["maximum_stopped_endpoint_to_reference_ratio"] for record in thresholds),
        "maximum_unrestricted_endpoint_ratio": max(record["maximum_unrestricted_endpoint_to_reference_ratio"] for record in thresholds),
        "maximum_spent_fraction": max(record["maximum_spent_fraction_of_allowance"] for record in thresholds),
        "primary_all_candidates_fit_stopped_budget": thresholds[0]["rejected_count"] == 0,
        "ratio_collapse_good_price_power": 1.5,
        "ratio_collapse_bad_price_power": 0.0,
    }
    payload = {
        "status": "rh106_uniform_gap_aware_quotient_audit",
        "thresholds": thresholds,
        "events": all_events,
        "ratio_principle": ratio_principle,
        "scenarios": scenarios,
        "audit_summary": summary,
        "theorem_boundary": {
            "local_gap_price_identity": True,
            "uniform_all_candidates_fit_law": True,
            "stopped_sparse_supply_safety_law": True,
            "ratio_not_gap_principle": True,
            "five_anchor_uniform_price_audit": True,
            "uniform_gap_aware_physical_supply_proved": False,
            "replay_free_uniform_debit_envelope_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "The correct uniform quotient object is the propagated price K*c^2/g, summed over candidate count and compared with endpoint slack. "
            "A fixed positive gap is sufficient but not necessary: a collapsing gap is harmless when cross energy collapses faster. "
            "The all-candidate power law gives a sufficient no-stop regime; the stopped theorem gives safety when the supply is sparse or the price budget fails. "
            "The five frozen chains satisfy the local certificates and the stopped endpoint gates, but a replay-free all-level physical supply law remains open."
        ),
        "limitations": [
            "The audit inherits exact hybrid replay prices from RH-102.",
            "The power criterion is a conditional sufficient law, not a proof of physical gap/cross-energy exponents.",
            "The ratio-collapse family is abstract and does not identify the production exponents.",
            "No Stage A, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
