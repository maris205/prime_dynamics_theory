"""Figures for the validated upstream Hardy bridge."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads(
        (ROOT / "results" / "validated_upstream_bridge_audit.json").read_text(
            encoding="utf-8"
        )
    )
    sigmas = np.asarray([row["sigma"] for row in payload["rows"]])
    left = [row["channels"][0] for row in payload["rows"]]
    right = [row["channels"][1] for row in payload["rows"]]

    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.6), constrained_layout=True)

    ax = axes[0, 0]
    for label, key, marker in (
        ("operator", "operator_two_norm_error_upper", "o"),
        ("source", "source_frobenius_error_upper", "s"),
        ("observation", "observation_frobenius_error_upper", "^"),
    ):
        ax.loglog(sigmas, [x["triple_error"][key] for x in left], marker + "-", label=label)
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("certified error")
    ax.set_title("Left upstream triple")
    ax.legend()

    ax = axes[0, 1]
    for label, key, marker in (
        ("operator", "operator_two_norm_error_upper", "o"),
        ("source", "source_frobenius_error_upper", "s"),
        ("observation", "observation_frobenius_error_upper", "^"),
    ):
        ax.loglog(sigmas, [x["triple_error"][key] for x in right], marker + "-", label=label)
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("certified error")
    ax.set_title("Right upstream triple")
    ax.legend()

    ax = axes[1, 0]
    for channels, style, label in ((left, "o-", "left"), (right, "s--", "right")):
        ax.loglog(sigmas, [x["robust_hardy_bridge"]["bridge_energy_upper"] for x in channels], style, label=label + " bridge")
        ax.loglog(sigmas, [x["one_percent_slack_lower"] for x in channels], style, alpha=0.45, label=label + " slack")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"Hardy norm")
    ax.set_title("Bridge versus inherited headroom")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    positions = np.arange(len(sigmas))
    width = 0.36
    ax.bar(positions - width / 2, [100.0 * x["bridge_to_slack_ratio_upper"] for x in left], width, label="left")
    ax.bar(positions + width / 2, [100.0 * x["bridge_to_slack_ratio_upper"] for x in right], width, label="right")
    ax.axhline(100.0, color="black", linestyle=":", linewidth=1.0, label="budget")
    ax.set_xticks(positions, [f"{value:g}" for value in sigmas])
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("slack consumed (%)")
    ax.set_yscale("log")
    ax.set_ylim(0.003, 120.0)
    ax.set_title("Finite-scale closure margin")
    ax.legend(fontsize=7)

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"validated_upstream_hardy_bridge.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
