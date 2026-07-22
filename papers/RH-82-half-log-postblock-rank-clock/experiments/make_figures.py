"""Make the RH-82 half-log rank-clock figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "half_log_rank_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    model = audit["endpoint_linear_row_model"]["rows"]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    sigma = [row["sigma"] for row in rows]
    ax.plot(sigma, [row["clock"] for row in rows], marker="o", label=r"$H_\sigma$")
    ax.step(sigma, [row["clock_rank"] for row in rows], where="mid", label=r"$\lceil H_\sigma\rceil+2$")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("rank")
    ax.set_title("(a) Half-logarithmic postblock clock")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["relative_residual_upper"] for channel in channels], marker="o", label=f"{side} relative residual")
        ax.semilogy(sigma, [channel["full_future_hardy_perturbation_upper"] for channel in channels], marker="s", linestyle="--", label=f"{side} future error")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("validated upper")
    ax.set_title("(b) Frozen physical postblock audit")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)

    ax = axes[1, 0]
    ax.loglog([row["sigma"] for row in model], [row["optimal_hilbert_schmidt_tail"] for row in model], marker="o", label="optimal HS tail")
    ax.loglog([row["sigma"] for row in model], [row["first_omitted_singular_value"] for row in model], marker="s", label="first omitted singular value")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"tail at $\lceil H_\sigma\rceil+2$")
    ax.set_title("(c) Endpoint linear-row model down to $10^{-12}$")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    excess = np.arange(0, 13)
    for q in (0.35, 0.45, 0.55):
        bound = np.sqrt(2.0 / (1.0 - q * q)) * q**excess
        ax.semilogy(excess, bound, marker="o", label=fr"$q={q}$")
    ax.set_xlabel("rank beyond $J_\sigma$")
    ax.set_ylabel("normalized HS tail majorant")
    ax.set_title("(d) Exponential excess-rank theorem")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    output = ROOT / "figures" / "half_log_postblock_rank_clock"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

