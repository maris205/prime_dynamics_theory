"""Make the RH-83 singular-factorization figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "singular_factorization_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["optimal_factor_constant_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", linewidth=1, label="unit factor")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("optimal factor constant upper")
    ax.set_title("(a) Endpoint singular majorization")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["optimal_remainder_upper"] for channel in channels], marker="o", label=f"{side} absolute")
        ax.semilogy(sigma, [channel["optimal_relative_remainder_upper"] for channel in channels], marker="s", linestyle="--", label=f"{side} relative")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("validated remainder upper")
    ax.set_title("(b) Optimal clock-rank remainder")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7)

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["coordinate_dictionary_relative_residual_lower"] for channel in channels], marker="o", label=side)
    ax.axhline(0.25, color="black", linestyle="--", linewidth=1, label="25% barrier gate")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("coordinate residual lower")
    ax.set_title("(c) Identity coordinate embedding fails")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    ax.step(sigma, [row["clock_rank"] for row in rows], where="mid", label="clock-plus-two")
    ax.step(sigma, [row["certified_factor_rank"] for row in rows], where="mid", label="certified factor rank")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("rank")
    ax.set_title("(d) Interval-resolved mediator modes")
    ax.grid(alpha=0.25)
    ax.legend()

    fig.tight_layout()
    output = ROOT / "figures" / "optimal_endpoint_singular_factorization"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

