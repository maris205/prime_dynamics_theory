"""Make the RH-88 predictor-corrector figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "predictor_corrector_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["interval_tested_global_coefficient_lower"] + audit["eta"] for channel in channels], marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", label="contraction threshold")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("tested global coefficient")
    ax.set_title("(a) Global-norm sufficient route fails"); ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["interval_point_rayleigh_coefficient_upper"] + audit["eta"] for channel in channels], marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", label="contraction threshold")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel(r"$\chi_j+\eta$")
    ax.set_title("(b) Point-packet predictor is mixed"); ax.legend()

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["binary64_memory_predictor_coefficient"] for channel in channels], marker="o", label=f"predictor {side}")
        ax.plot(sigma, [channel["binary64_actual_memory_contraction"] for channel in channels], marker="s", linestyle="--", label=f"corrected {side}")
    ax.axhline(1.0, color="black", linestyle="--")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("memory contraction factor")
    ax.set_title("(c) Reoptimization restores all channels"); ax.legend(fontsize=7)

    ax = axes[1, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.semilogy(sigma, [channel["binary64_reoptimization_factor"] for channel in channels], marker="o", label=side)
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel(r"reoptimization $\gamma_{j+1}$")
    ax.set_title("(d) Variational correction dividend"); ax.legend()

    fig.tight_layout()
    output = ROOT / "figures" / "predictor_corrector_energy_contraction"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
