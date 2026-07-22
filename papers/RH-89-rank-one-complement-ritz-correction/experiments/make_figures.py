"""Make the RH-89 rank-one Ritz correction figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "ritz_correction_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["interval_reference_dividend_fraction_lower"] for channel in channels], marker="o", label=side)
    ax.axhline(0.96, color="black", linestyle="--", label="96% gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("reference dividend fraction")
    ax.set_title("(a) One complement direction captures the dividend"); ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["interval_corrected_contraction_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(0.24, color="black", linestyle="--", label="contraction gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("corrected memory contraction")
    ax.set_title("(b) Small Ritz corrector remains contractive"); ax.legend()

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["binary64_corrected_reference_tail_ratio"] for channel in channels], marker="o", label=side)
    ax.axhline(3.28, color="black", linestyle="--", label="ratio gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("corrected / reference tail")
    ax.set_title("(c) Corrected tail versus full reference"); ax.legend()

    ax = axes[1, 1]
    ax.step(sigma, [row["clock_rank"] for row in rows], where="mid", label="packet rank")
    ax.step(sigma, [row["clock_rank"] + 1 for row in rows], where="mid", label="Ritz dimension")
    ax.plot(sigma, [row["fine_dimension"] for row in rows], marker="o", label="fine dimension")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("dimension")
    ax.set_title("(d) Correction stays logarithmic"); ax.legend(fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "rank_one_complement_ritz_correction"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
