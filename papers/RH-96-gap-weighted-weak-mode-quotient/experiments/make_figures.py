"""Create the RH-96 weak-mode quotient figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "weak_mode_quotient_audit.json"
PDF = ROOT / "figures" / "gap_weighted_weak_mode_quotient.pdf"
PNG = ROOT / "figures" / "gap_weighted_weak_mode_quotient.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    keys = ["1e-08", "1e-06", "1e-04"]
    colors = ["#1b9e77", "#7570b3", "#d95f02"]
    markers = ["o", "s", "^"]
    endpoints = {key: np.array([channel["chains"][key]["interval_endpoint_to_reference_upper"] for channel in channels]) for key in keys}
    primary_steps = [step for channel in channels for step in channel["chains"]["1e-08"]["steps"]]
    omitted = [step for step in primary_steps if step["omitted_width"] > 0]

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)
    x = np.arange(len(channels))

    ax = axes[0, 0]
    for offset, key, color, marker in zip((-0.2, 0.0, 0.2), keys, colors, markers):
        ax.plot(x + offset, endpoints[key], marker, color=color, label=key)
    ax.axhline(1.01, color="#222222", linestyle=":", label="endpoint gate")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("endpoint tail / reference tail")
    ax.set_title("(a) Only the conservative cutoff closes all endpoints")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    summaries = audit["audit_summary"]["threshold_summaries"]
    width_counts = np.array([[summaries[key][f"width_{name}_update_count"] for name in ("two", "three", "four")] for key in keys])
    bottom = np.zeros(len(keys))
    for column, (name, color) in enumerate(zip(("width 2", "width 3", "width 4"), ("#d95f02", "#7570b3", "#1b9e77"))):
        ax.bar(np.arange(len(keys)), width_counts[:, column], bottom=bottom, color=color, label=name)
        bottom += width_counts[:, column]
    ax.set_xticks(np.arange(len(keys)), keys)
    ax.set_ylabel("update count")
    ax.set_title("(b) Adaptive width distribution")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    actual = np.array([max(step["interval_actual_tail_loss_upper"], 1e-30) for step in omitted])
    bound = np.array([step["gap_weighted_tail_loss_bound"] for step in omitted])
    ax.loglog(actual, bound, "o", color="#e7298a", markersize=5)
    low = min(actual.min(), bound.min())
    high = max(actual.max(), bound.max())
    ax.plot([low, high], [low, high], color="#222222", linestyle=":", label="exact loss")
    ax.set_xlabel("validated actual one-step loss")
    ax.set_ylabel("gap-weighted upper bound")
    ax.set_title("(c) All five omitted losses are certified")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    threshold = np.array([summaries[key]["threshold"] for key in keys])
    local = np.array([summaries[key]["maximum_adaptive_to_full_tail_ratio"] - 1.0 for key in keys])
    endpoint_excess = np.array([summaries[key]["maximum_endpoint_to_reference_ratio"] - 1.0 for key in keys])
    ax.loglog(threshold, local, "o-", color="#66a61e", label="largest local excess")
    ax.loglog(threshold, endpoint_excess, "s-", color="#1f78b4", label="largest endpoint excess")
    ax.axhline(0.01, color="#222222", linestyle=":", label="1% endpoint budget")
    ax.set_xlabel("relative singular cutoff")
    ax.set_ylabel("tail-ratio excess")
    ax.set_title("(d) Certified local losses still accumulate")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    figure.suptitle("RH-96: weak modes are quotientable, but quotient losses need a horizon budget", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "omitted_primary_updates": len(omitted)}, sort_keys=True))


if __name__ == "__main__":
    main()
