"""Make the RH-87 Rayleigh-injection figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "injection_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["interval_last_injection_relative_norm_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(5e-4, color="black", linestyle="--", label="injection gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("last injection relative norm")
    ax.set_title("(a) 192-bit one-step injection"); ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["last_injection_energy_ratio"] for channel in channels], marker="o", label=side)
    ax.axhline(0.18, color="black", linestyle="--", label="last-step gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel(r"$\iota_j/\iota_{j-1}$")
    ax.set_title("(b) Last injection-energy contraction"); ax.legend()

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["final_recursion_utilization"] for channel in channels], marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", label="recursion bound")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel(r"$E_j/(\iota_j+\eta E_{j-1})$")
    ax.set_title("(c) Gap-free recursion utilization"); ax.legend(fontsize=8)

    ax = axes[1, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["interval_lagged_terminal_relative_residual_upper"] for channel in channels], marker="o", label=f"lagged {side}")
    ax.axhline(0.0012, color="black", linestyle="--", label="lagged gate")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("terminal residual")
    ax.set_title("(d) One-update-lagged prediction"); ax.legend(fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "rayleigh_injection_recursion"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
