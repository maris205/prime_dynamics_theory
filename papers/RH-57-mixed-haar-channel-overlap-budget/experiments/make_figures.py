"""Create the RH-57 grouped-Riesz audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load(ROOT / "results" / "mixed_overlap_pilot.json")
    rows = payload["rows"]
    sigma = np.asarray([row["sigma"] for row in rows])

    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.3))

    ax = axes[0, 0]
    for side, marker, color in (("left", "o", "#174a7e"), ("right", "s", "#c44e52")):
        ax.loglog(
            sigma,
            [row[side]["exact_hardy_energy"] for row in rows],
            marker + "-",
            color=color,
            label=side + " exact",
        )
        ax.loglog(
            sigma,
            [row[side]["coherence_upper"] for row in rows],
            marker + "--",
            color=color,
            alpha=0.72,
            label=side + " coherence upper",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"Hardy magnitude at $r=0.85$")
    ax.set_title("(a) Aggregate energy versus block budget")
    ax.legend(fontsize=7, ncol=2)

    ax = axes[0, 1]
    for side, marker, color in (("left", "o", "#174a7e"), ("right", "s", "#c44e52")):
        ax.loglog(
            sigma,
            [
                max(block["projector_norm"] for block in row[side]["blocks"])
                for row in rows
            ],
            marker + "-",
            color=color,
            label=side,
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"$\max_j\|P_j\|_2$")
    ax.set_title("(b) Radial Riesz obliqueness")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    for side, color in (("left", "#174a7e"), ("right", "#c44e52")):
        ax.loglog(
            sigma,
            [row[side]["signed_fusion_ratio"] for row in rows],
            "o-" if side == "left" else "s-",
            color=color,
            label=side,
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"signed fusion ratio $\eta$")
    ax.set_title("(c) Aggregate cancellation across radial blocks")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    last = rows[-1]
    gram = np.asarray(last["right"]["normalized_block_gram_real"])
    image = ax.imshow(gram, cmap="RdBu_r", vmin=-1.0, vmax=1.0, aspect="auto")
    ax.set_xlabel("block index")
    ax.set_ylabel("block index")
    ax.set_title(r"(d) Right normalized block Gram at $\sigma=0.01$")
    figure.colorbar(image, ax=ax, fraction=0.046, pad=0.04)

    figure.tight_layout()
    output = ROOT / "figures" / "mixed_haar_channel_overlap"
    figure.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
