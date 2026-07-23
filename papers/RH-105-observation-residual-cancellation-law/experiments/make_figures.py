"""Create the RH-105 observation/residual cancellation figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "observation_residual_audit.json").read_text(encoding="utf-8"))
    levels = [row["level"] for row in data["rows"]]
    observation = [max(c["observation_factor_upper"] for c in row["channels"]) for row in data["rows"]]
    residual = [max(c["clock_residual_frobenius_upper"] for c in row["channels"]) for row in data["rows"]]
    weighted = [max(c["weighted_residual_upper"] for c in row["channels"]) for row in data["rows"]]
    scaled_observation = [max(c["sqrt_sigma_observation_factor"] for c in row["channels"]) for row in data["rows"]]
    scaled_residual = [max(c["residual_over_sqrt_sigma"] for c in row["channels"]) for row in data["rows"]]

    fig, axes = plt.subplots(1, 2, figsize=(10.6, 4.15))
    ax = axes[0]
    ax.semilogy(levels, scaled_observation, marker="o", linewidth=2.2, label=r"$\sqrt{\sigma}\,\Omega$")
    ax.semilogy(levels, scaled_residual, marker="s", linewidth=2.2, label=r"$\tau/\sqrt{\sigma}$")
    ax.set_xlabel("dyadic anchor level $k$")
    ax.set_ylabel("matched factor")
    ax.set_title("Square-root factorization")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    ax.semilogy(levels, weighted, marker="o", linewidth=2.2, label=r"$\Omega\tau$")
    ax.axhline(1.0e-8, color="tab:red", linestyle="--", linewidth=1.7, label=r"$10^{-8}$ audit gate")
    ax.set_xlabel("dyadic anchor level $k$")
    ax.set_ylabel("full-future perturbation upper")
    ax.set_title("Observation growth is canceled")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)
    ax.text(0.04, 0.07, r"power$(\Omega\tau)=\max(0,o-\rho)$", transform=ax.transAxes, fontsize=9)

    fig.tight_layout()
    output = ROOT / "figures" / "observation_residual_cancellation"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
