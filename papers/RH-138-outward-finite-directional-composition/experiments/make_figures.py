from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "outward_composition_audit.json").read_text(encoding="utf-8"))
    tagged = [(row["sigma"], step) for row in data["rows"] for step in row["steps"]]
    steps = [step for _, step in tagged]
    positive = [step for step in steps if step["exact_candidate"]["value"] > 0]

    fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4))
    grid = np.logspace(-11, 0, 300)
    axes[0, 0].loglog(
        [step["exact_candidate"]["value"] for step in positive],
        [step["support_lower"]["value"] for step in positive],
        "o", markersize=4.5, alpha=0.6, color="tab:blue",
    )
    axes[0, 0].plot(grid, grid, color="black", linestyle=":", label="exact candidate diagonal")
    axes[0, 0].set_xlabel("direct reference directional candidate")
    axes[0, 0].set_ylabel("outward-composed lower")
    axes[0, 0].set_title("All finite support lowers are dominated")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, which="both", alpha=0.18)

    sigmas = sorted({sigma for sigma, _ in tagged}, reverse=True)
    thresholds = [0.0, 1e-8, 1e-6, 1e-4]
    labels = [">0", r"$\geq10^{-8}$", r"$\geq10^{-6}$", r"$\geq10^{-4}$"]
    x = np.arange(len(sigmas))
    width = 0.19
    colors = ["tab:blue", "tab:green", "tab:orange", "tab:red"]
    for index, (cutoff, label, color) in enumerate(zip(thresholds, labels, colors)):
        counts = []
        for sigma in sigmas:
            group = [step for value, step in tagged if value == sigma]
            if cutoff == 0.0:
                counts.append(sum(step["support_lower"]["value"] > 0 for step in group))
            else:
                counts.append(sum(step["support_lower"]["value"] >= cutoff for step in group))
        axes[0, 1].bar(x + (index - 1.5) * width, counts, width, label=label, color=color)
    axes[0, 1].set_xticks(x, [str(value) for value in sigmas])
    axes[0, 1].set_xlabel(r"scale $\sigma$")
    axes[0, 1].set_ylabel("certified transitions")
    axes[0, 1].set_title("Directional lower by scale and cutoff")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, axis="y", alpha=0.2)

    precision_labels = ["fp64", "decimal 16", "decimal 18", "decimal 20", "decimal 40"]
    precision_counts = [
        sum(step["fp64_base_positive"] for step in steps),
        sum(step["decimal_precision_base_positive"]["16"] for step in steps),
        sum(step["decimal_precision_base_positive"]["18"] for step in steps),
        sum(step["decimal_precision_base_positive"]["20"] for step in steps),
        len(steps),
    ]
    axes[1, 0].bar(precision_labels, precision_counts, color=["tab:gray", "tab:red", "tab:orange", "tab:green", "tab:blue"])
    axes[1, 0].axhline(len(steps), color="black", linestyle=":")
    axes[1, 0].set_ylim(300, 332)
    axes[1, 0].set_ylabel("positive outward base certificates / 330")
    axes[1, 0].set_title("Weak Gram directions impose a precision gate")
    axes[1, 0].tick_params(axis="x", rotation=18)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    padding = [step["forcing_padding"]["value"] for step in steps if step["forcing_padding"]["value"] > 0]
    inflation = [step["bound_additive_inflation"]["value"] for step in steps if step["bound_additive_inflation"]["value"] > 0]
    axes[1, 1].hist(np.log10(padding), bins=28, alpha=0.72, color="tab:purple", label="forcing padding")
    axes[1, 1].hist(np.log10(inflation), bins=28, alpha=0.55, color="tab:cyan", label="tail-bound inflation")
    axes[1, 1].set_xlabel("log10 outward correction")
    axes[1, 1].set_ylabel("transitions")
    axes[1, 1].set_title("Outward corrections are negligible on the archive")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "outward_finite_directional_composition"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
