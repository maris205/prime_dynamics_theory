"""Deterministic audit of RH-56 exponent and overlap clocks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
RH51 = PAPERS / "RH-51-cyclic-rank-growing-horizon-stein"
RH53 = PAPERS / "RH-53-deterministic-hardy-tail-cutoff"
sys.path.insert(0, str(ROOT / "src"))

from hardy_barrier import (  # noqa: E402
    critical_strong_rate,
    strong_space_ledger,
)


OUTPUT = ROOT / "results" / "hardy_barrier_pilot.json"
HARDY_RADIUS = 0.85
LAMBDA = 1.678573510428322
EDGE_RADIUS = LAMBDA ** -0.5
ENTRANCE_POWER_PER_SIDE = 1.0
TOTAL_BUDGET = 0.25


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source(path: Path):
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def build_payload(*, smoke: bool = False):
    rh50_path = RH50 / "results" / "two_pole_hardy_pilot.json"
    rh51_path = RH51 / "results" / "structured_stein_pilot.json"
    rh53_path = RH53 / "results" / "deterministic_tail_pilot.json"
    rh50 = load(rh50_path)
    rh51 = load(rh51_path)
    rh53 = load(rh53_path)

    common_threshold = critical_strong_rate(
        HARDY_RADIUS, 2.0 * ENTRANCE_POWER_PER_SIDE, TOTAL_BUDGET
    )
    edge_side = strong_space_ledger(
        HARDY_RADIUS, EDGE_RADIUS, ENTRANCE_POWER_PER_SIDE
    )
    rates = (0.329642076293171, EDGE_RADIUS, 0.82)
    rate_ledgers = []
    for rate in rates:
        side = strong_space_ledger(
            HARDY_RADIUS, rate, ENTRANCE_POWER_PER_SIDE
        )
        rate_ledgers.append(
            {
                "strong_rate": rate,
                "single_side_energy_power": side.energy_power,
                "two_side_total_power": 2.0 * side.energy_power,
                "within_quarter_power_budget": (
                    2.0 * side.energy_power <= TOTAL_BUDGET
                ),
            }
        )

    all_column = []
    for row in rh51["rows"]:
        rho = max(
            float(row["fine_bulk_radius_candidate"]),
            float(row["coarse_bulk_radius_candidate"]),
        )
        radial_clock = 1.0 / math.sqrt(
            1.0 - (rho / HARDY_RADIUS) ** 2
        )
        all_column.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "bulk_radius_candidate": rho,
                "radial_hardy_clock": radial_clock,
                "left_exact_hardy_energy": float(
                    row["left_exact_hardy_energy"]
                ),
                "right_exact_hardy_energy": float(
                    row["right_exact_hardy_energy"]
                ),
                "left_energy_over_radial_clock": float(
                    row["left_exact_hardy_energy"] / radial_clock
                ),
                "right_energy_over_radial_clock": float(
                    row["right_exact_hardy_energy"] / radial_clock
                ),
            }
        )
    if smoke:
        all_column = all_column[:2]

    production = []
    for row in rh50["rows"]:
        production.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "fine_bulk_radius_candidate": float(
                    row["fine_bulk_radius_candidate"]
                ),
                "left_truncated_energy_r085": float(
                    row["hardy_energies"]["r=0.85"][
                        "left_truncated_hardy_energy"
                    ]
                ),
                "right_truncated_energy_r085": float(
                    row["hardy_energies"]["r=0.85"][
                        "right_truncated_hardy_energy"
                    ]
                ),
                "left_tail_decay_candidate": float(
                    row["left_tail_fit"]["decay_base"]
                ),
                "right_tail_decay_candidate": float(
                    row["right_tail_fit"]["decay_base"]
                ),
            }
        )
    if smoke:
        production = production[:2]

    tail_rows = []
    for row in rh53["rows"]:
        tail_rows.append(
            {
                "sigma": float(row["sigma"]),
                "fine_dimension": int(row["fine_dimension"]),
                "horizon": int(row["left"]["horizon"]),
                "left_block_power_norm": float(
                    row["left"]["block_power_norm"]
                ),
                "right_block_power_norm": float(
                    row["right"]["block_power_norm"]
                ),
                "maximum_relative_energy_excess": max(
                    float(row["left"]["relative_energy_excess"]),
                    float(row["right"]["relative_energy_excess"]),
                ),
            }
        )
    if smoke:
        tail_rows = tail_rows[:2]

    extrema = {
        "common_strong_rate_threshold": common_threshold,
        "edge_two_side_total_power": 2.0 * edge_side.energy_power,
        "maximum_all_column_energy_over_radial_clock": max(
            max(
                row["left_energy_over_radial_clock"],
                row["right_energy_over_radial_clock"],
            )
            for row in all_column
        ),
        "maximum_all_column_hardy_energy": max(
            max(
                row["left_exact_hardy_energy"],
                row["right_exact_hardy_energy"],
            )
            for row in all_column
        ),
        "maximum_production_truncated_hardy_energy": max(
            max(
                row["left_truncated_energy_r085"],
                row["right_truncated_energy_r085"],
            )
            for row in production
        ),
        "maximum_deterministic_tail_relative_excess": max(
            row["maximum_relative_energy_excess"] for row in tail_rows
        ),
    }
    return {
        "status": "deterministic_hardy_barrier_and_overlap_target_audit",
        "evidence_level": (
            "exact scalar exponent formulas and inherited deterministic "
            "all-column binary64 Hardy traces; production traces remain "
            "Hutchinson/truncated diagnostics; no interval eigensolver"
        ),
        "hardy_radius": HARDY_RADIUS,
        "lambda": LAMBDA,
        "deterministic_edge_radius": EDGE_RADIUS,
        "strong_space_barrier": {
            "entrance_power_per_side": ENTRANCE_POWER_PER_SIDE,
            "total_entrance_power": 2.0 * ENTRANCE_POWER_PER_SIDE,
            "allowed_total_hardy_power": TOTAL_BUDGET,
            "common_rate_threshold": common_threshold,
            "threshold_formula": "theta <= r^(p_total/budget)=r^8",
            "rate_ledgers": rate_ledgers,
        },
        "all_column_dense_audit": all_column,
        "production_directional_audit": production,
        "deterministic_tail_audit": tail_rows,
        "extrema": extrema,
        "sources": {
            "rh50_pilot": source(rh50_path),
            "rh51_all_column_pilot": source(rh51_path),
            "rh53_tail_pilot": source(rh53_path),
        },
        "limitations": [
            "The strong-space result is a no-go for a stated black-box ledger, not a lower bound on the true Hardy energies.",
            "The five-scale all-column matrices are binary64 diagnostics and do not prove a uniform small-noise theorem.",
            "The production RH-50 values use Hutchinson probes and a truncated time horizon.",
            "The deterministic edge radius comes from the deterministic physical trace law; noisy cloud quantization remains conjectural.",
            "Stage A1 and unconditional Stage A4 remain open.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = build_payload(smoke=args.smoke)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "hardy_barrier_pilot_smoke.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "all_column_rows": len(payload["all_column_dense_audit"]),
                "production_rows": len(payload["production_directional_audit"]),
                "extrema": payload["extrema"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
