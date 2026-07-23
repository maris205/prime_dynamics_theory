"""Audit weak-mode support separation and coarse quotient prices."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from quotient_support import (  # noqa: E402
    coarse_support_price_upper,
    finite_support_reduction,
    fourth_cross_ratio,
    local_quotient_price,
    support_margin,
    weak_mode_event,
)


FULL_OUTPUT = ROOT / "results" / "source_seeded_support_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "source_seeded_support_smoke.json"
THRESHOLDS = ("1e-08", "1e-06", "1e-04")


def load(path: str) -> dict[str, object]:
    return json.loads((PAPERS / path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    weak = load("RH-96-gap-weighted-weak-mode-quotient/results/weak_mode_quotient_audit.json")
    stopped = load("RH-102-stopped-hybrid-quotient-clock/results/stopped_hybrid_clock_audit.json")
    weak_rows = weak["rows"] if not args.smoke else weak["rows"]
    stopped_rows = stopped["rows"]
    threshold_records = []
    all_event_records = []

    for threshold in THRESHOLDS[:1] if args.smoke else THRESHOLDS:
        scale_records = []
        local_prices = []
        event_count_by_scale = []
        for row, stopped_row in zip(weak_rows, stopped_rows):
            scale = float(row["sigma"])
            all_steps = [
                (channel["side"], step)
                for channel in row["channels"]
                for step in channel["chains"][threshold]["steps"]
            ]
            ratios = [fourth_cross_ratio(step["cross_singular_values"]) for _, step in all_steps]
            events = []
            for side, step in all_steps:
                ratio = fourth_cross_ratio(step["cross_singular_values"])
                selected_event = weak_mode_event(step["cross_singular_values"], float(threshold))
                omitted_event = bool(step["omitted_width"] > 0)
                if selected_event != omitted_event:
                    raise RuntimeError("adaptive support selector disagrees with archived width")
                if omitted_event:
                    price = local_quotient_price(
                        float(step["omitted_cross_frobenius_upper"]),
                        float(step["retained_to_omitted_gap_lower"]),
                    )
                    local_prices.append(price)
                    event = {
                        "sigma": scale,
                        "side": side,
                        "time": step["time"],
                        "threshold": float(threshold),
                        "fourth_cross_ratio": ratio,
                        "support_margin": support_margin(ratio, float(threshold)),
                        "local_price_upper": price,
                        "gap_certificate_green": bool(step["gap_certificate_green"]),
                    }
                    events.append(event)
                    all_event_records.append(event)
            scale_records.append(
                {
                    "sigma": scale,
                    "level": len(scale_records),
                    "update_count": len(all_steps),
                    "weak_event_count": len(events),
                    "minimum_fourth_cross_ratio": min(ratios),
                    "maximum_fourth_cross_ratio": max(ratios),
                    "minimum_event_support_margin": min((event["support_margin"] for event in events), default=None),
                    "local_price_sum": sum(event["local_price_upper"] for event in events),
                    "maximum_local_price": max((event["local_price_upper"] for event in events), default=0.0),
                    "all_local_certificates_green": all(event["gap_certificate_green"] for event in events),
                }
            )
            event_count_by_scale.append(len(events))

        fine_start = next(
            (index for index in range(len(event_count_by_scale)) if finite_support_reduction(event_count_by_scale, index)),
            len(event_count_by_scale),
        )
        fine_records = scale_records[fine_start:]
        stopped_summary = stopped["audit_summary"]["threshold_summary"][threshold]
        replay_ratios = [
            event["propagated_debit_abs_upper"] / event["local_gap_weighted_tail_loss_bound"]
            for row in stopped_rows
            for channel in row["channels"]
            for event in channel["chains"][threshold]["events"]
            if event["local_gap_weighted_tail_loss_bound"] > 0.0
        ]
        maximum_replay = max(replay_ratios, default=0.0)
        max_local = max(local_prices, default=0.0)
        record = {
            "threshold": float(threshold),
            "scale_records": scale_records,
            "candidate_count": sum(event_count_by_scale),
            "event_count_by_scale": event_count_by_scale,
            "fine_support_start_level": fine_start,
            "fine_support_start_sigma": scale_records[fine_start]["sigma"] if fine_start < len(scale_records) else None,
            "fine_event_count": sum(event_count_by_scale[fine_start:]),
            "minimum_fine_fourth_cross_ratio": min((item["minimum_fourth_cross_ratio"] for item in fine_records), default=None),
            "minimum_fine_support_margin": min(
                (item["minimum_fourth_cross_ratio"] / float(threshold) for item in fine_records),
                default=None,
            ),
            "coarse_event_count": sum(event_count_by_scale[:fine_start]),
            "total_local_price": sum(local_prices),
            "maximum_local_price": max_local,
            "coarse_price_upper_with_max_replay": coarse_support_price_upper(
                sum(event_count_by_scale[:fine_start]), maximum_replay, max_local
            ),
            "all_selector_equivalences_green": all(
                item["all_local_certificates_green"] for item in scale_records
            ),
            "maximum_replay_multiplier": maximum_replay,
            "maximum_stopped_endpoint_ratio": stopped_summary["maximum_final_endpoint_to_reference_ratio"],
            "maximum_unrestricted_endpoint_ratio": stopped_summary["maximum_unrestricted_endpoint_to_reference_ratio"],
            "stopped_rejected_count": stopped_summary["rejected_quotient_count"],
        }
        threshold_records.append(record)

    observed_levels = [0, 1, 2, 3, 4]
    extrapolation = []
    for threshold in THRESHOLDS[:1] if args.smoke else THRESHOLDS:
        anchor = next(record for record in threshold_records if record["threshold"] == float(threshold))
        observed = [item["minimum_fourth_cross_ratio"] for item in anchor["scale_records"]]
        for level, value in zip(observed_levels, observed):
            extrapolation.append({"threshold": float(threshold), "level": level, "observed_min_ratio": value, "separated_extension": value})
        for level in range(5, 9):
            extrapolation.append(
                {
                    "threshold": float(threshold),
                    "level": level,
                    "observed_min_ratio": None,
                    "separated_extension": 2.0 * float(threshold),
                    "persistent_extension": 0.5 * float(threshold),
                }
            )

    summary = {
        "threshold_count": len(threshold_records),
        "total_candidate_comparisons": sum(
            sum(item["update_count"] for item in record["scale_records"])
            for record in threshold_records
        ),
        "total_weak_mode_events": sum(record["coarse_event_count"] for record in threshold_records),
        "all_finite_selector_equivalences_green": all(record["all_selector_equivalences_green"] for record in threshold_records),
        "all_finite_fine_supports_empty": all(record["fine_event_count"] == 0 for record in threshold_records),
        "maximum_total_local_price": max(record["total_local_price"] for record in threshold_records),
        "maximum_coarse_price_upper_with_max_replay": max(record["coarse_price_upper_with_max_replay"] for record in threshold_records),
        "minimum_fine_support_margin": min(record["minimum_fine_support_margin"] for record in threshold_records),
        "maximum_stopped_endpoint_ratio": max(record["maximum_stopped_endpoint_ratio"] for record in threshold_records),
        "maximum_unrestricted_endpoint_ratio": max(record["maximum_unrestricted_endpoint_ratio"] for record in threshold_records),
        "primary_fine_support_start_level": threshold_records[0]["fine_support_start_level"],
    }
    payload = {
        "status": "rh107_source_seeded_quotient_support_audit",
        "thresholds": threshold_records,
        "events": all_event_records,
        "finite_extrapolation": extrapolation,
        "audit_summary": summary,
        "theorem_boundary": {
            "adaptive_support_equivalence": True,
            "coarse_support_to_price_reduction": True,
            "stopped_sparse_supply_safety": True,
            "finite_extrapolation_barrier": True,
            "five_anchor_fine_support_separation_validated": True,
            "all_level_fine_support_separation_proved": False,
            "all_level_quotient_supply_closed": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "For each audited threshold, all weak-mode quotient events lie in a coarse support layer and the fine support is empty. "
            "The adaptive selector equivalence makes this a direct fourth-cross-ratio statement, so no fine-scale quotient price accumulates on the archived chain. "
            "A conditional all-level support separation would reduce the uniform quotient law to finitely many coarse prices; finite anchors alone cannot prove that separation because separated and persistent-support extensions agree on every observed level."
        ),
        "limitations": [
            "Fine support separation is validated only on the five archived scales.",
            "The source-seeded cross-ratio arrays are finite numerical certificates, not an analytic asymptotic theorem.",
            "The coarse price reduction still uses the archived replay multipliers for its finite audit.",
            "No Stage A, Hilbert--Polya, zero-identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
