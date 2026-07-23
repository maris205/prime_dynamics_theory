"""Create the RH-104 prefix-transient figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "prefix_transient_audit.json").read_text(encoding="utf-8"))
    levels = [row["level"] for row in data["rows"]]
    actual = [max(c["actual_directional_prefix_energy_upper"] for c in row["channels"]) for row in data["rows"]]
    crude = [max(c["crude_norm_product_prefix_upper"] for c in row["channels"]) for row in data["rows"]]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    ax = axes[0]
    ax.plot(levels, actual, marker="o", linewidth=2.2, label="directional prefix")
    ax.plot(levels, crude, marker="s", linewidth=2.2, label="crude norm product")
    ax.set_yscale("log")
    ax.set_xlabel("dyadic anchor level $k$")
    ax.set_ylabel("prefix energy upper")
    ax.set_title("Physical directionality matters")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    rows = data["barrier"]["rows"]
    ax.loglog([r["sigma"] for r in rows], [r["prefix_energy"] for r in rows], marker="o", linewidth=2.2, color="tab:red")
    ax.invert_xaxis()
    ax.set_xlabel(r"$\sigma$")
    ax.set_ylabel("prefix Hardy energy")
    ax.set_title("Block contraction does not control prefix")
    ax.grid(True, which="both", alpha=0.25)
    ax.text(0.05, 0.08, "A² = 0\npacket tail = 0\nprefix power = 1.5", transform=ax.transAxes, fontsize=9)
    fig.tight_layout()
    out = ROOT / "figures" / "source_weighted_prefix_law"
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(out.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
