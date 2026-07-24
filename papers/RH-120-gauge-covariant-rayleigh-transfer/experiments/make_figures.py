"""Create the RH-120 efficiency and sharpness figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "gauge_transfer_audit.json").read_text(encoding="utf-8"))
    records = data["records"]
    gamma = np.asarray([r["gamma_efficiency"] for r in records])
    volume = np.asarray([r["volume_efficiency"] for r in records])
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))
    axes[0].hist(gamma, bins=45, color="tab:blue", alpha=0.82)
    axes[0].axvline(1.0, color="black", lw=1.2)
    axes[0].set_xlabel(r"actual $\gamma'$ / transferred upper")
    axes[0].set_ylabel("random gauges")
    axes[0].set_title("Relative-tail transfer")
    axes[0].grid(True, alpha=0.23)
    axes[1].hist(volume, bins=45, color="tab:green", alpha=0.82)
    axes[1].axvline(1.0, color="black", lw=1.2)
    axes[1].set_xlabel("certified / actual target four-volume")
    axes[1].set_title("Determinant transfer")
    axes[1].grid(True, alpha=0.23)
    axes[1].text(0.04, 0.94, "scalar-congruence family attains 1", transform=axes[1].transAxes, va="top", fontsize=9)
    fig.tight_layout()
    output = ROOT / "figures" / "gauge_covariant_rayleigh_transfer"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

