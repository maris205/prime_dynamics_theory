from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "spectral_packet_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    rank4 = [row for row in rows if row["rank"] == 4]
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))
    for side, marker in (("left", "o"), ("right", "s")):
        group = [row for row in rank4 if row["side"] == side]
        axes[0, 0].loglog([row["sigma"] for row in group], [row["approximate_gap"] for row in group], marker=marker, label=f"gap, {side}")
        axes[0, 0].loglog([row["sigma"] for row in group], [2.0 * row["universal_snapshot_radius"] for row in group], marker=marker, linestyle="--", label=f"2 radius, {side}")
    axes[0, 0].invert_xaxis()
    axes[0, 0].set_xlabel(r"scale $\sigma$")
    axes[0, 0].set_ylabel("rank-four gap / crossing radius")
    axes[0, 0].set_title("Universal enclosure crosses only four packet gates")
    axes[0, 0].legend(frameon=False, fontsize=7, ncol=2)
    axes[0, 0].grid(True, which="both", alpha=0.2)

    x = np.arange(len(rank4))
    labels = [f"{row['sigma']:.2f}\n{row['side'][0]}" for row in rank4]
    axes[0, 1].semilogy(x, [row["universal_gap_ratio"] for row in rank4], "o-", label="universal")
    axes[0, 1].semilogy(x, [row["ideal_svd_gap_ratio"] for row in rank4], "s--", label="quadratic SVD diagnostic")
    axes[0, 1].axhline(1.0, color="black", linestyle=":", label="crossing threshold")
    axes[0, 1].set_xticks(x, labels)
    axes[0, 1].set_ylabel(r"gap / $(2\varepsilon)$")
    axes[0, 1].set_title("Quadratic cancellation would cross all ten")
    axes[0, 1].legend(frameon=False, fontsize=8)
    axes[0, 1].grid(True, which="both", alpha=0.2)

    stable = [row for row in rank4 if row["universal_enclosure"]["stable"]]
    axes[1, 0].bar(
        [f"{row['sigma']:.2f}-{row['side'][0]}" for row in stable],
        [row["universal_enclosure"]["projector_radius"] for row in stable],
        color="tab:blue", label="projector",
    )
    axes[1, 0].plot(
        [f"{row['sigma']:.2f}-{row['side'][0]}" for row in stable],
        [row["universal_enclosure"]["frame_radius"] for row in stable],
        "s", color="tab:orange", label="polar-aligned frame",
    )
    axes[1, 0].set_ylabel("certified operator radius")
    axes[1, 0].set_title("Four stable packets and their frame balls")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    epsilon = np.linspace(0.0, 0.75, 400)
    gap = 1.0
    bound = np.where(epsilon < 0.5, epsilon / (gap - epsilon), np.nan)
    axes[1, 1].plot(epsilon, bound, color="tab:blue", label="projector enclosure")
    axes[1, 1].axvline(0.5, color="tab:red", linestyle="--", label=r"$2\varepsilon=g$")
    axes[1, 1].fill_between(epsilon, 0, 1, where=epsilon >= 0.5, alpha=0.15, color="tab:red", label="swap/degeneracy possible")
    axes[1, 1].set_ylim(0, 1.05)
    axes[1, 1].set_xlabel(r"operator radius $\varepsilon$ for unit gap")
    axes[1, 1].set_ylabel("principal-angle sine bound")
    axes[1, 1].set_title("The two-radius crossing threshold is sharp")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "gap_stable_spectral_packet"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

