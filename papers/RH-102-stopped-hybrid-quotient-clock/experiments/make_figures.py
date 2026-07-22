"""Create the RH-102 stopped-clock audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "stopped_hybrid_clock_audit.json"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    summary = payload["audit_summary"]["threshold_summary"]
    keys = [f"{threshold:.0e}" for threshold in payload["thresholds"]]
    labels = [r"$10^{-8}$", r"$10^{-6}$", r"$10^{-4}$"]
    unrestricted = [summary[key]["maximum_unrestricted_endpoint_to_reference_ratio"] for key in keys]
    stopped = [summary[key]["maximum_final_endpoint_to_reference_ratio"] for key in keys]

    stopped_cases = []
    for row in payload["rows"]:
        for channel in row["channels"]:
            for key, chain in channel["chains"].items():
                if chain["stopped"]:
                    rejected = next(event for event in chain["events"] if not event["accepted"])
                    stopped_cases.append(
                        {
                            "label": rf"$\sigma={row['sigma']}$ {channel['side'][0].upper()} {key}",
                            "spent": rejected["spent_before"] / chain["stopped_allowance"],
                            "proposed": (rejected["spent_before"] + rejected["propagated_debit_abs_upper"]) / chain["stopped_allowance"],
                        }
                    )

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.15))
    ax = axes[0]
    x = np.arange(len(keys))
    width = 0.34
    ax.bar(x - width / 2, unrestricted, width, color="tab:red", alpha=0.78, label="unrestricted")
    ax.bar(x + width / 2, stopped, width, color="tab:blue", alpha=0.82, label="stopped clock")
    ax.axhline(payload["endpoint_gate"], color="black", linestyle="--", linewidth=1.3, label="1.01 gate")
    ax.set_xticks(x, labels)
    ax.set_ylim(0.998, max(unrestricted) * 1.003)
    ax.set_xlabel("relative quotient threshold")
    ax.set_ylabel("worst endpoint / reference tail")
    ax.set_title("Endpoint gate under stress")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    x = np.arange(len(stopped_cases))
    spent = [case["spent"] for case in stopped_cases]
    proposed = [case["proposed"] for case in stopped_cases]
    ax.bar(x, spent, color="tab:blue", alpha=0.8, label="spent before proposal")
    ax.scatter(x, proposed, color="tab:red", marker="x", s=70, linewidths=2.2, label="spent + rejected debit")
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1.3, label="allowance")
    ax.set_xticks(x, [case["label"] for case in stopped_cases], rotation=18, ha="right")
    ax.set_ylabel("fraction of stopped allowance")
    ax.set_title("Three exact stopping events")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "stopped_hybrid_quotient_clock"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
