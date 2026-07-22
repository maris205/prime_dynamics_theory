"""Certify RH-70 bridge-slack margins from the archived Arb balls."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
SOURCE = (
    PAPERS
    / "RH-70-frozen-production-block-hardy-audit"
    / "results"
    / "frozen_production_interval_audit.json"
)
OUTPUT = ROOT / "results" / "arb_bridge_slack_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "arb_bridge_slack_smoke.json"
PRECISION_BITS = 256


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lower_float(value: arb) -> float:
    return float(value.lower())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_rows = payload["rows"][:1] if args.smoke else payload["rows"]
    previous_precision = ctx.prec
    ctx.prec = PRECISION_BITS
    rows = []
    try:
        factors = {
            "1_percent": arb(101) / 100,
            "2_percent": arb(102) / 100,
            "5_percent": arb(105) / 100,
        }
        for source_row in source_rows:
            for channel in source_row["channels"]:
                finite = arb(channel["finite_energy_ball"])
                full = arb(channel["full_energy_upper_ball"])
                budgets = {}
                for name, factor in factors.items():
                    slack = factor * finite - full
                    relative = slack / finite
                    budgets[name] = {
                        "slack_ball": str(slack),
                        "slack_lower": lower_float(slack),
                        "relative_slack_ball": str(relative),
                        "relative_slack_lower": lower_float(relative),
                        "strictly_positive_certified": bool(slack.lower() > 0),
                    }
                rows.append(
                    {
                        "sigma": source_row["sigma"],
                        "side": channel["side"],
                        "horizon": channel["horizon"],
                        "finite_energy_ball": str(finite),
                        "frozen_full_upper_ball": str(full),
                        "budgets": budgets,
                    }
                )
    finally:
        ctx.prec = previous_precision
    one_percent = [row["budgets"]["1_percent"] for row in rows]
    output_payload = {
        "status": "rh71_arb_bridge_slack_certificate",
        "precision_bits": PRECISION_BITS,
        "source": str(SOURCE.relative_to(PAPERS.parent)),
        "source_sha256": sha256_file(SOURCE),
        "rows": rows,
        "all_one_percent_slacks_positive": all(
            row["strictly_positive_certified"] for row in one_percent
        ),
        "minimum_one_percent_slack_lower": min(
            row["slack_lower"] for row in one_percent
        ),
        "minimum_one_percent_relative_slack_lower": min(
            row["relative_slack_lower"] for row in one_percent
        ),
        "claim_boundary": (
            "This certifies finite-scale bridge headroom relative to the "
            "archived RH-70 balls; it does not construct the upstream bridge."
        ),
    }
    output = SMOKE_OUTPUT if args.smoke else OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(output_payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "row_count": len(rows),
                "all_one_percent_positive": output_payload[
                    "all_one_percent_slacks_positive"
                ],
                "minimum_relative_slack": output_payload[
                    "minimum_one_percent_relative_slack_lower"
                ],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
