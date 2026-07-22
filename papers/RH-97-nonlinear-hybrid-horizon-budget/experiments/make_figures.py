"""Create the RH-97 nonlinear hybrid horizon budget figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "hybrid_horizon_budget_audit.json"
PDF = ROOT / "figures" / "nonlinear_hybrid_horizon_budget.pdf"
PNG = ROOT / "figures" / "nonlinear_hybrid_horizon_budget.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    keys = ["1e-08", "1e-06", "1e-04"]
    colors = ["#1b9e77", "#7570b3", "#d95f02"]
    summaries = audit["audit_summary"]["threshold_summaries"]
    primary = [channel["chains"]["1e-08"] for channel in channels]
    records = [record for chain in primary for record in chain["contributions"]]

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)
    x = np.arange(len(channels))

    ax = axes[0, 0]
    width = 0.22
    for offset, key, color in zip((-width, 0.0, width), keys, colors):
        values = [channel["chains"][key]["absolute_horizon_budget_to_reference"] for channel in channels]
        ax.semilogy(x + offset, np.maximum(values, 1e-16), "o", color=color, label=key)
    ax.axhline(0.01, color="#222222", linestyle=":", label="1% budget")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("absolute hybrid budget / reference tail")
    ax.set_title("(a) Hybrid budgets locate the endpoint frontier")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    absolute = np.array([summaries[key]["maximum_absolute_horizon_budget_to_reference"] for key in keys])
    signed = np.array([summaries[key]["maximum_signed_endpoint_shift_to_reference"] for key in keys])
    positions = np.arange(len(keys))
    ax.bar(positions - 0.18, absolute, width=0.36, color="#e7298a", label="absolute budget")
    ax.bar(positions + 0.18, signed, width=0.36, color="#66a61e", label="signed shift")
    ax.axhline(0.01, color="#222222", linestyle=":")
    ax.set_xticks(positions, keys)
    ax.set_ylabel("worst relative endpoint effect")
    ax.set_title("(b) Cancellation is small in the failing channel")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    local = np.array([max(record["interval_local_quotient_loss_upper"], 1e-30) for record in records])
    propagated = np.array([max(record["propagated_endpoint_contribution_abs_upper"], 1e-30) for record in records])
    ax.loglog(local, propagated, "o", color="#1f78b4", markersize=5)
    low = min(local.min(), propagated.min())
    high = max(local.max(), propagated.max())
    ax.plot([low, high], [low, high], color="#222222", linestyle=":", label="unit propagation")
    ax.set_xlabel("local quotient loss")
    ax.set_ylabel("absolute endpoint contribution")
    ax.set_title("(c) Primary injections do not amplify")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    signs = np.array([float(record["signed_propagation_multiplier"]) for record in records])
    ax.bar(np.arange(len(signs)), signs, color=np.where(signs >= 0.0, "#1b9e77", "#d95f02"))
    ax.axhline(0.0, color="#222222", linewidth=0.8)
    ax.set_xlabel("primary omission")
    ax.set_ylabel("signed endpoint / local multiplier")
    ax.set_title("(d) Nonlinear future refresh can reverse a loss")
    ax.grid(alpha=0.25)

    figure.suptitle("RH-97: exact hybrid telescoping turns local quotient losses into endpoint budgets", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "primary_contributions": len(records)}, sort_keys=True))


if __name__ == "__main__":
    main()
