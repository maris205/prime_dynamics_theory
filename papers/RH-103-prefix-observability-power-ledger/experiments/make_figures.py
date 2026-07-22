"""Create the RH-103 power-ledger figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "prefix_observability_power_ledger.json"


def main() -> None:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    rows = payload["rows"]
    levels = [row["level"] for row in rows]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.2))
    ax = axes[0]
    ax.semilogy(levels, [row["finite_prefix_energy_upper"] for row in rows], marker="o", linewidth=2.0, label="finite prefix")
    ax.semilogy(levels, [row["conditional_zero_power_hardy_upper"] for row in rows], marker="s", linewidth=2.0, label="conditional Hardy")
    ax.semilogy(levels, [row["future_observability_sqrt_upper"] for row in rows], marker="^", linewidth=2.0, label=r"$\|O\|^{1/2}$")
    ax.semilogy(levels, [row["clock_future_residual_upper"] for row in rows], marker="D", linewidth=1.8, label="observed residual product")
    ax.semilogy(levels, [row["upstream_bridge_upper"] for row in rows], marker="v", linewidth=1.8, label="upstream bridge")
    ax.set_xlabel("dyadic anchor level $k$")
    ax.set_ylabel("certified finite-anchor quantity")
    ax.set_title("Why factors must stay separate")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=7.7)

    ax = axes[1]
    for key, color, marker in (
        ("prefix_transient", "tab:red", "o"),
        ("observation_scaling", "tab:purple", "s"),
    ):
        item = payload["counterexamples"][key]
        sigmas = [row["sigma"] for row in item["rows"]]
        energies = [row["hardy_energy"] for row in item["rows"]]
        label = f"{key.replace('_', ' ')}: power {item['fitted_hardy_power']:.2f}"
        ax.loglog(sigmas, energies, marker=marker, linewidth=2.0, color=color, label=label)
    ax.invert_xaxis()
    ax.set_xlabel(r"$\sigma$")
    ax.set_ylabel("Hardy energy")
    ax.set_title("Perfect packets, arbitrary Hardy power")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    ax.text(0.04, 0.06, "normalized Gram = 1\npacket relative tail = 0", transform=ax.transAxes, fontsize=8.5)

    fig.tight_layout()
    output = ROOT / "figures" / "prefix_observability_power_ledger"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
