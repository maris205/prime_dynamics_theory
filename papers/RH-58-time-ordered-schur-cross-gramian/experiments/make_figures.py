"""Create the RH-58 unitary Schur packet audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load(ROOT / "results" / "schur_fusion_pilot.json")
    rows = payload["rows"]
    sigma = np.asarray([row["sigma"] for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.3))

    ax = axes[0, 0]
    styles = {
        "left": ("#174a7e", "o"),
        "right": ("#c44e52", "s"),
    }
    for side, (color, marker) in styles.items():
        ax.semilogx(
            sigma,
            [row[side]["exact_hardy_energy"] for row in rows],
            marker + "-",
            color=color,
            label=side + " exact",
        )
        ax.semilogx(
            sigma,
            [
                row[side]["source_packet_gram"]["coherence_upper"]
                for row in rows
            ],
            marker + "--",
            color=color,
            alpha=0.78,
            label=side + " input packets",
        )
        ax.semilogx(
            sigma,
            [
                row[side]["state_block_gram"]["coherence_upper"]
                for row in rows
            ],
            marker + ":",
            color=color,
            alpha=0.78,
            label=side + " output blocks",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"Hardy magnitude at $r=0.85$")
    ax.set_title("(a) Dual unitary Schur packet budgets")
    ax.legend(fontsize=7, ncol=2)

    ax = axes[0, 1]
    for side, (color, marker) in styles.items():
        ax.loglog(
            sigma,
            [
                row[side]["scalar_path_majorant"]["energy_upper"]
                for row in rows
            ],
            marker + "-",
            color=color,
            label=side + " scalar paths",
        )
        ax.loglog(
            sigma,
            [
                row[side]["inherited_rh57_radial_riesz"]["coherence_upper"]
                for row in rows
            ],
            marker + "--",
            color=color,
            alpha=0.72,
            label=side + " RH-57 Riesz",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("sufficient upper")
    ax.set_title("(b) Two absolute-value proof losses")
    ax.legend(fontsize=7)

    ax = axes[1, 0]
    for side, (color, marker) in styles.items():
        ax.semilogx(
            sigma,
            [
                row[side]["scalar_path_majorant"][
                    "maximum_terminal_power_norm"
                ]
                for row in rows
            ],
            marker + "-",
            color=color,
            label=side + r" max $\|T_j^8\|$",
        )
        ax.semilogx(
            sigma,
            [
                row[side]["cross_stein_recursion"]["maximum_empirical_gain"]
                for row in rows
            ],
            marker + "--",
            color=color,
            alpha=0.75,
            label=side + " empirical Stein gain",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("binary64 diagnostic")
    ax.set_title("(c) Blocks contract; exact gains stay modest")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    gram = np.asarray(
        rows[-1]["right"]["source_packet_gram"]["normalized_gram_real"]
    )
    image = ax.imshow(
        gram, cmap="RdBu_r", vmin=-1.0, vmax=1.0, aspect="auto"
    )
    ax.set_xlabel("Schur packet index")
    ax.set_ylabel("Schur packet index")
    ax.set_title(r"(d) Right input-packet Gram at $\sigma=0.01$")
    figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    figure.tight_layout()
    output = ROOT / "figures" / "time_ordered_schur_fusion"
    figure.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
