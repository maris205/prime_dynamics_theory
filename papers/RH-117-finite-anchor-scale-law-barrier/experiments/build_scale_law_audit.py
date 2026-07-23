"""Audit five-scale physical envelopes and finite-anchor extrapolation barriers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from scale_law import bounded_anchor_matching_extension, loglog_fit  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "scale_law_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "scale_law_smoke.json"
PRIMARY_THRESHOLD = 1e-8


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def primary_steps(row: dict[str, object]) -> dict[tuple[str, int], dict[str, object]]:
    output = {}
    for channel in row["channels"]:
        record = next(
            value for value in channel["thresholds"] if float(value["threshold"]) == PRIMARY_THRESHOLD
        )
        for step in record["steps"]:
            output[(str(channel["side"]), int(step["time"]))] = step
    return output


def envelope(values: list[float]) -> dict[str, float]:
    data = np.asarray(values, dtype=float)
    return {
        "minimum": float(np.min(data)),
        "lower_quartile": float(np.quantile(data, 0.25)),
        "median": float(np.median(data)),
        "upper_quartile": float(np.quantile(data, 0.75)),
        "maximum": float(np.max(data)),
    }


def scale_row(
    capacity_row: dict[str, object],
    concentration_row: dict[str, object],
    depth_row: dict[str, object],
) -> dict[str, object]:
    capacity = primary_steps(capacity_row)
    concentration = primary_steps(concentration_row)
    depth = primary_steps(depth_row)
    keys = sorted(capacity)
    alignment_holds = set(keys) == set(concentration) == set(depth)
    if not alignment_holds:
        raise RuntimeError("upstream physical records are not aligned")
    capacity_values = [float(capacity[key]["actual_capacity"]) for key in keys]
    concentration_values = [float(concentration[key]["actual_concentration"]) for key in keys]
    volume_values = [float(capacity[key]["actual_normalized_volume"]) for key in keys]
    ratio_values = [float(depth[key]["actual_ratio"]) for key in keys]
    supported_depths = [
        int(depth[key]["first_certifying_depth"])
        for key in keys
        if bool(depth[key]["actual_support"])
    ]
    return {
        "sigma": float(capacity_row["sigma"]),
        "record_count": len(keys),
        "alignment_holds": alignment_holds,
        "capacity": envelope(capacity_values),
        "concentration": envelope(concentration_values),
        "normalized_four_volume": envelope(volume_values),
        "fourth_mode_ratio": envelope(ratio_values),
        "positive_ratio_count": sum(value > 0.0 for value in ratio_values),
        "support_count": len(supported_depths),
        "certifying_depth": envelope([float(value) for value in supported_depths]) if supported_depths else None,
        "maximum_certifying_depth": max(supported_depths, default=None),
    }


def continuation_barrier(rows: list[dict[str, object]]) -> dict[str, object]:
    scales = np.asarray([row["sigma"] for row in rows], dtype=float)
    values = np.asarray([row["capacity"]["median"] for row in rows], dtype=float)
    probe = float(np.min(scales) * 1e-4)
    points = np.concatenate([scales, [probe]])
    germs = {
        "vanishing": lambda x: x,
        "interior_limit": lambda x: np.full_like(x, 0.5),
        "unit_limit": lambda x: 1.0 - x,
    }
    examples = {}
    for name, germ in germs.items():
        extension = bounded_anchor_matching_extension(scales, values, points, germ)
        examples[name] = {
            "maximum_relative_anchor_error": float(np.max(np.abs(extension[:-1] / values - 1.0))),
            "probe_value": float(extension[-1]),
        }
    return {
        "anchor_metric": "median three-mode capacity",
        "preserved_range": [0.0, 1.0],
        "anchor_count": len(scales),
        "probe_scale": probe,
        "examples": examples,
        "all_anchor_errors_below_tolerance": all(
            record["maximum_relative_anchor_error"] < 2e-10 for record in examples.values()
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    capacity = load(PAPERS / "RH-110-finite-memory-three-mode-capacity/results/three_mode_capacity_audit.json")
    concentration = load(PAPERS / "RH-111-tail-energy-exterior-concentration/results/exterior_concentration_audit.json")
    depth = load(PAPERS / "RH-116-monotone-memory-depth-optimization/results/memory_depth_audit.json")
    count = 3 if args.smoke else 5
    rows = [
        scale_row(capacity_row, concentration_row, depth_row)
        for capacity_row, concentration_row, depth_row in zip(
            capacity["rows"][:count], concentration["rows"][:count], depth["rows"][:count]
        )
    ]
    scales = [row["sigma"] for row in rows]
    fits = {
        "capacity_minimum": loglog_fit(scales, [row["capacity"]["minimum"] for row in rows]),
        "capacity_median": loglog_fit(scales, [row["capacity"]["median"] for row in rows]),
        "concentration_median": loglog_fit(scales, [row["concentration"]["median"] for row in rows]),
        "fourth_mode_ratio_median": loglog_fit(scales, [row["fourth_mode_ratio"]["median"] for row in rows]),
    }
    barrier = continuation_barrier(rows)
    summary = {
        "scale_count": len(rows),
        "physical_record_count": sum(row["record_count"] for row in rows),
        "alignment_failure_count": sum(not row["alignment_holds"] for row in rows),
        "minimum_capacity": min(row["capacity"]["minimum"] for row in rows),
        "maximum_capacity": max(row["capacity"]["maximum"] for row in rows),
        "minimum_concentration": min(row["concentration"]["minimum"] for row in rows),
        "maximum_concentration": max(row["concentration"]["maximum"] for row in rows),
        "maximum_observed_certifying_depth": max(
            row["maximum_certifying_depth"] for row in rows if row["maximum_certifying_depth"] is not None
        ),
        "maximum_fit_residual_factor": max(
            fit["maximum_multiplicative_residual"] for fit in fits.values()
        ),
        "maximum_leave_one_out_exponent_span": max(
            fit["leave_one_out_exponent_maximum"] - fit["leave_one_out_exponent_minimum"]
            for fit in fits.values()
        ),
        "continuation_anchor_failure_count": 0 if barrier["all_anchor_errors_below_tolerance"] else 1,
    }
    payload = {
        "status": "rh117_finite_anchor_scale_law_barrier_audit",
        "primary_threshold": PRIMARY_THRESHOLD,
        "rows": rows,
        "descriptive_power_law_fits": fits,
        "continuation_barrier": barrier,
        "audit_summary": summary,
        "theorem_boundary": {
            "positive_smooth_anchor_extension": True,
            "bounded_interval_anchor_extension": True,
            "arbitrary_near_zero_germ_extension": True,
            "finite_anchor_asymptotic_nonidentifiability": True,
            "five_scale_physical_envelopes_audited": not args.smoke,
            "descriptive_fit_is_asymptotic_law": False,
            "all_level_capacity_law_proved": False,
            "all_level_concentration_law_proved": False,
            "all_level_uniform_depth_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "Capacity, exterior concentration, fourth-volume, fourth-mode ratio, and certifying depth now have a common five-scale envelope ledger. Power-law fits are archived as descriptive diagnostics only. A positive smooth-extension theorem proves that any finite anchor set is compatible with arbitrary positive behavior near zero, so all-level closure requires an independent physical inequality rather than extrapolation."
        ),
        "limitations": [
            "The five scale records are correlated outputs of one finite model family and do not support inferential asymptotics.",
            "The continuation examples are impossibility witnesses, not proposed physical models.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
