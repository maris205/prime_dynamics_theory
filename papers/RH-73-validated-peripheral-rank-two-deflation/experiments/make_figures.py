"""Figures for the validated peripheral rank-two audit."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    payload = json.loads(
        (ROOT / "results" / "peripheral_validation_audit.json").read_text(
            encoding="utf-8"
        )
    )
    sigmas = np.asarray([row["sigma"] for row in payload["rows"]])
    fine = [row["channels"][0] for row in payload["rows"]]
    coarse = [row["channels"][1] for row in payload["rows"]]

    plt.rcParams.update({"font.size": 9, "axes.grid": True, "grid.alpha": 0.25})
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.6), constrained_layout=True)

    ax = axes[0, 0]
    ax.semilogx(sigmas, [x["parity_value_center"] for x in fine], "o-", label="fine")
    ax.semilogx(sigmas, [x["parity_value_center"] for x in coarse], "s--", label="coarse")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"validated center $\lambda_-$")
    ax.set_title("Negative parity branch")
    ax.legend()

    ax = axes[0, 1]
    for label, key, marker in (
        ("stationary", ("stationary", "stationary_two_norm_error_upper"), "o"),
        ("right", ("parity_right", "newton_radius_upper"), "s"),
        ("left", ("parity_left", "left_two_norm_error_upper"), "^"),
    ):
        ax.loglog(sigmas, [x[key[0]][key[1]] for x in fine], marker + "-", label=label)
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("certified Euclidean error")
    ax.set_title("Fine-channel vector balls")
    ax.legend()

    ax = axes[1, 0]
    for channels, style, label in ((fine, "o-", "fine"), (coarse, "s--", "coarse")):
        ax.loglog(sigmas, [x["rank_two_projector_two_norm_error_upper"] for x in channels], style, label=label + " rank two")
        ax.loglog(sigmas, [x["deflated_bulk_two_norm_error_upper"] for x in channels], style, alpha=0.55, label=label + " bulk")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("certified operator error")
    ax.set_title("Projector and deflated-bulk enclosure")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    width = 0.36
    positions = np.arange(len(sigmas))
    ax.bar(positions - width / 2, [x["parity_contour"]["center_transport_product_upper"] for x in fine], width, label="fine")
    ax.bar(positions + width / 2, [x["parity_contour"]["center_transport_product_upper"] for x in coarse], width, label="coarse")
    ax.axhline(1.0, color="black", linewidth=1.0, linestyle=":", label="Neumann gate")
    ax.set_xticks(positions, [f"{value:g}" for value in sigmas])
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"$0.01\,\|E_0\|_2$ upper")
    ax.set_ylim(0.0, 1.05)
    ax.set_title("Parity contour transport")
    ax.legend(fontsize=7)

    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "png"):
        fig.savefig(output / f"validated_peripheral_rank_two.{suffix}", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
