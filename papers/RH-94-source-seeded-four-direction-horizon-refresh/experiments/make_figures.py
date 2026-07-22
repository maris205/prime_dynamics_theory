"""Create the RH-94 full-prefix source-seed figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "source_seeded_horizon_audit.json"
PDF = ROOT / "figures" / "source_seeded_four_direction_horizon.pdf"
PNG = ROOT / "figures" / "source_seeded_four_direction_horizon.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    endpoint = {width: np.array([channel["chains"][str(width)]["interval_endpoint_to_reference_upper"] for channel in channels]) for width in (2, 3, 4)}
    intermediate = np.array([channel["chains"]["4"]["maximum_intermediate_reference_ratio_upper"] for channel in channels])
    captures = {width: np.array([channel["chains"][str(width)]["minimum_selected_cross_energy_fraction"] for channel in channels]) for width in (2, 3, 4)}
    projector = np.array([channel["source_svd_to_gram_projector_distance"] for channel in channels])
    primary_steps = [step for channel in channels for step in channel["chains"]["4"]["steps"]]
    gains = np.array([step["interval_generalized_frame_gain_lower"] for step in primary_steps])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)
    x = np.arange(len(channels))

    ax = axes[0, 0]
    ax.semilogy(x - 0.18, endpoint[2], "o", color="#d95f02", label="width 2")
    ax.semilogy(x, endpoint[3], "s", color="#7570b3", label="width 3")
    ax.semilogy(x + 0.18, endpoint[4], "^", color="#1b9e77", label="width 4")
    ax.axhline(1.01, color="#222222", linestyle=":", linewidth=1.2, label="1.01 gate")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("endpoint tail / reference tail")
    ax.set_title("(a) Width four closes every full prefix")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    width = 0.24
    for offset, selected, color, marker in ((-width, 2, "#d95f02", "o"), (0.0, 3, "#7570b3", "s"), (width, 4, "#1b9e77", "^")):
        ax.plot(x + offset, captures[selected], marker, color=color, label=f"width {selected}")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylim(0.75, 1.01)
    ax.set_ylabel("minimum cross-energy capture")
    ax.set_title("(b) The fourth direction absorbs the cross tail")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    ax.plot(x, intermediate, "o-", color="#e7298a", label="worst intermediate")
    ax.plot(x, endpoint[4], "s-", color="#1b9e77", label="endpoint")
    ax.axhline(1.0, color="#222222", linestyle=":", linewidth=1.2)
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("width-4 tail / reference tail")
    ax.set_title("(c) Endpoint recovery need not be stepwise optimal")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    ax.semilogy(np.sort(projector), "o", color="#66a61e", label="seed projector defect")
    ax.semilogy(np.sort(gains), ".", color="#1f78b4", alpha=0.75, label="certified frame gain")
    ax.set_xlabel("sorted certificate")
    ax.set_ylabel("validated diagnostic")
    ax.set_title("(d) Source equivalence and positive Ritz gains")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    figure.suptitle("RH-94: one source seed survives the complete frozen prefix", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "channels": len(channels)}, sort_keys=True))


if __name__ == "__main__":
    main()
