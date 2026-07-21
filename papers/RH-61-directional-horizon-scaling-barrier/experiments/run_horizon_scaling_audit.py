"""Audit physical-family horizon scaling from the RH-59/RH-60 archives."""

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
RH59 = PAPERS / "RH-59-flag-adapted-schur-stein-metrics"
RH60 = PAPERS / "RH-60-finite-horizon-phase-aware-tails"
sys.path.insert(0, str(ROOT / "src"))

from horizon_scaling import (  # noqa: E402
    geometric_tail_envelope,
    log_power_fit,
    minimum_geometric_horizon,
    observed_horizon,
)


FULL_OUTPUT = ROOT / "results" / "horizon_scaling_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "horizon_scaling_smoke.json"
TOLERANCES = (0.20, 0.10, 0.05, 0.01)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tolerance_key(value: float) -> str:
    return str(float(value))


def channel_row(
    phase_row: dict[str, object], metric_row: dict[str, object], side: str
) -> dict[str, object]:
    phase = phase_row[side]
    metric = metric_row[side]
    packets = metric["packets"]
    initial_tails = [
        float(value) for value in phase["horizons"]["0"]["tail_energies"]
    ]
    contractions = [
        float(packet["normalized_contraction"]) for packet in packets
    ]
    if len(initial_tails) != len(contractions):
        raise RuntimeError(f"packet count mismatch for {side}")
    exact = float(phase["exact_hardy_energy"])
    upper_by_horizon = {
        int(horizon): float(record["phase_aware_upper"])
        for horizon, record in phase["horizons"].items()
    }
    tail_by_horizon = {
        int(horizon): float(record["tail_sum"])
        for horizon, record in phase["horizons"].items()
    }
    initial_sum = sum(initial_tails)
    geometric_horizons = {}
    observed_horizons = {}
    for tolerance in TOLERANCES:
        key = tolerance_key(tolerance)
        target = tolerance * exact
        geometric_horizons[key] = minimum_geometric_horizon(
            initial_tails, contractions, target
        )
        observed_horizons[key] = observed_horizon(
            upper_by_horizon, exact, tolerance
        )

    horizon_records = {}
    for horizon in sorted(upper_by_horizon):
        envelope = geometric_tail_envelope(
            initial_tails, contractions, horizon
        )
        horizon_records[str(horizon)] = {
            "phase_aware_upper": upper_by_horizon[horizon],
            "phase_upper_over_exact": upper_by_horizon[horizon]
            / max(exact, 1.0e-300),
            "phase_tail_sum": tail_by_horizon[horizon],
            "phase_tail_ratio_to_initial": tail_by_horizon[horizon]
            / max(initial_sum, 1.0e-300),
            "geometric_tail_envelope": envelope,
            "geometric_tail_ratio_to_initial": envelope
            / max(initial_sum, 1.0e-300),
        }

    return {
        "exact_hardy_energy": exact,
        "packet_initial_tails": initial_tails,
        "packet_contractions": contractions,
        "maximum_contraction": max(contractions),
        "contraction_gap": 1.0 - max(contractions),
        "relaxation_time": 1.0 / (-math.log(max(contractions))),
        "initial_tail_sum": initial_sum,
        "geometric_horizons": geometric_horizons,
        "observed_phase_horizons": observed_horizons,
        "horizons": horizon_records,
        "smallest_scale_phase_upper_ratio": upper_by_horizon[
            max(upper_by_horizon)
        ]
        / max(exact, 1.0e-300),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    phase_payload = json.loads(
        (RH60 / "results" / "phase_tail_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    metric_payload = json.loads(
        (RH59 / "results" / "flag_metric_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    metric_rows = {
        float(row["sigma"]): row for row in metric_payload["rows"]
    }
    phase_rows = phase_payload["rows"]
    if args.smoke:
        phase_rows = phase_rows[:2]

    rows = []
    for phase_row in phase_rows:
        sigma = float(phase_row["sigma"])
        metric_row = metric_rows[sigma]
        row = {
            "sigma": sigma,
            "fine_dimension": int(phase_row["fine_dimension"]),
            "left": channel_row(phase_row, metric_row, "left"),
            "right": channel_row(phase_row, metric_row, "right"),
        }
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": sigma,
                    "left_q": row["left"]["maximum_contraction"],
                    "right_q": row["right"]["maximum_contraction"],
                    "left_L05": row["left"]["geometric_horizons"]["0.05"],
                    "right_L05": row["right"]["geometric_horizons"]["0.05"],
                    "left_observed_L05": row["left"][
                        "observed_phase_horizons"
                    ]["0.05"],
                    "right_observed_L05": row["right"][
                        "observed_phase_horizons"
                    ]["0.05"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    fits = {}
    for side in ("left", "right"):
        fits[f"{side}_gap"] = log_power_fit(
            [row["sigma"] for row in rows],
            [row[side]["contraction_gap"] for row in rows],
        )
        fits[f"{side}_relaxation"] = log_power_fit(
            [row["sigma"] for row in rows],
            [row[side]["relaxation_time"] for row in rows],
        )
        fits[f"{side}_geometric_horizon_05"] = log_power_fit(
            [row["sigma"] for row in rows],
            [row[side]["geometric_horizons"]["0.05"] for row in rows],
        )
        observed = [
            row[side]["observed_phase_horizons"]["0.05"] for row in rows
        ]
        if all(value is not None and value > 0 for value in observed):
            fits[f"{side}_observed_horizon_05"] = log_power_fit(
                [row["sigma"] for row in rows], observed
            )

    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    payload = {
        "status": "rh61_archived_horizon_scaling_audit",
        "evidence_level": (
            "archived RH-59/RH-60 binary64 results; exact finite-matrix "
            "algebraic reanalysis, not a continuum or interval theorem"
        ),
        "source_inputs": {
            "rh59_metric_pilot": {
                "path": str(
                    (RH59 / "results" / "flag_metric_pilot.json").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH59 / "results" / "flag_metric_pilot.json"
                ),
            },
            "rh60_phase_tail_pilot": {
                "path": str(
                    (RH60 / "results" / "phase_tail_pilot.json").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH60 / "results" / "phase_tail_pilot.json"
                ),
            },
        },
        "tolerances": list(TOLERANCES),
        "rows": rows,
        "fits": fits,
        "theorem_translation": {
            "packetwise_geometric_envelope": True,
            "slow_mode_horizon_lower_bound": True,
            "physical_family_uniformity": False,
            "directional_tail_profile": False,
        },
        "program_boundary": {
            "stage_A1_closed": False,
            "directional_tail_certificate": False,
            "polylogarithmic_horizon_proved": False,
            "continuum_phase_gram_theorem": False,
            "stage_A4_unconditional_closed": False,
            "self_adjoint_hilbert_polya_operator": False,
            "prime_power_trace_formula": False,
        },
        "limitations": [
            "The five rows are inherited binary64 finite-matrix diagnostics.",
            "Contraction-gap and horizon exponents are fits, not asymptotic theorems.",
            "The geometric envelope is rigorous for the stored packet metrics but can be much looser than the directional tail.",
            "The observed phase-aware horizon grid is censored at the stored horizons.",
            "No production interval audit or physical-family uniform estimate is claimed.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "rows": len(rows)}, sort_keys=True))


if __name__ == "__main__":
    main()
