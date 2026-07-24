from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "support_rayleigh_audit.json").read_text(encoding="utf-8"))
    application = data["rh130_application"]
    compatible = data["compatible_samples"]
    leakage = data["kernel_leakage_samples"]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    scales = ["0.16", "0.08", "0.04", "0.02", "0.01"]
    zero = [application["tail_rank_by_scale"][scale]["rank_0"] for scale in scales]
    full = [application["tail_rank_by_scale"][scale]["rank_4"] for scale in scales]
    axes[0].bar(scales, zero, color="tab:gray", label="tail rank 0")
    axes[0].bar(scales, full, bottom=zero, color="tab:blue", label="tail rank 4")
    axes[0].set_xlabel(r"scale $\sigma$")
    axes[0].set_ylabel("states")
    axes[0].set_title("RH-130 semidefinite tail support")
    axes[0].legend(frameon=False)
    axes[0].grid(True, axis="y", alpha=0.2)

    axes[1].hist([max(row["outward_margin"], 1e-18) for row in compatible], bins=35, color="tab:green", alpha=0.8)
    axes[1].set_xscale("log")
    axes[1].set_xlabel("outward squared-Rayleigh reserve")
    axes[1].set_ylabel("synthetic instances")
    axes[1].set_title("4,096 outward support bounds")
    axes[1].grid(True, alpha=0.2)

    axes[2].scatter(
        [row["epsilon"] for row in leakage],
        [row["kernel_leakage_norm"] for row in leakage],
        s=18, alpha=0.55, color="tab:red",
    )
    axes[2].plot([1e-8, 1e-3], [1e-8, 1e-3], color="black", linestyle="--", linewidth=1)
    axes[2].set_xscale("log")
    axes[2].set_yscale("log")
    axes[2].set_xlabel("injected kernel mass")
    axes[2].set_ylabel("detected leakage norm")
    axes[2].set_title("Any kernel leakage makes the full quotient infinite")
    axes[2].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "singular_gram_support_rayleigh"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
