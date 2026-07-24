from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "threshold_branch_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))
    colors = {1e-8: "tab:blue", 1e-6: "tab:orange", 1e-4: "tab:green"}
    for tau in (1e-8, 1e-6, 1e-4):
        group = [row for row in rows if row["threshold"] == tau]
        axes[0, 0].hist(np.log10([row["relative_branch_radius"] for row in group]), bins=28, alpha=0.5, color=colors[tau], label=f"tau={tau:.0e}")
    axes[0, 0].set_xlabel("log10 relative branch radius")
    axes[0, 0].set_ylabel("updates")
    axes[0, 0].set_title("Every archived threshold branch has positive margin")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, alpha=0.2)

    labels = [r"$10^{-8}$", r"$10^{-6}$", r"$10^{-4}$"]
    width = 0.24
    x = np.arange(3)
    for index, selected in enumerate((2, 3, 4)):
        values = []
        for tau in (1e-8, 1e-6, 1e-4):
            values.append(sum(row["archived_selected_width"] == selected for row in rows if row["threshold"] == tau))
        axes[0, 1].bar(x + (index - 1) * width, values, width, label=f"width {selected}")
    axes[0, 1].set_xticks(x, labels)
    axes[0, 1].set_ylabel("updates / 120")
    axes[0, 1].set_title("Clipped branch populations")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, axis="y", alpha=0.2)

    minimum = []
    median = []
    for tau in (1e-8, 1e-6, 1e-4):
        group = [row for row in rows if row["threshold"] == tau]
        minimum.append(min(row["branch_radius_to_fp64_budget"] for row in group))
        median.append(float(np.median([row["branch_radius_to_fp64_budget"] for row in group])))
    axes[1, 0].semilogy(labels, minimum, "o-", label="minimum")
    axes[1, 0].semilogy(labels, median, "s--", label="median")
    axes[1, 0].axhline(1.0, color="black", linestyle=":")
    axes[1, 0].set_ylabel("branch radius / local fp64 proxy")
    axes[1, 0].set_title("All local floating branches have wide roundoff margin")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, which="both", alpha=0.2)

    tau = 1e-8
    s1 = 1.0
    omitted = np.linspace(0.0, 2.0 * tau, 400)
    radius = np.abs(tau * s1 - omitted) / (1.0 + tau)
    axes[1, 1].plot(omitted / tau, radius / tau, color="tab:red")
    axes[1, 1].axvline(1.0, color="black", linestyle=":", label="threshold contact")
    axes[1, 1].set_xlabel(r"candidate ratio / $\tau$")
    axes[1, 1].set_ylabel(r"normalized branch radius / $\tau$")
    axes[1, 1].set_title("Branch radius vanishes sharply at contact")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "threshold_branch_stability"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

