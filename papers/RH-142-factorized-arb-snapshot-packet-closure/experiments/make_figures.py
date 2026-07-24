from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "factorized_arb_audit.json").read_text(encoding="utf-8"))
    rows = data["rows"]
    labels = [f"{row['sigma']:.2f}\n{row['side'][0]}" for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))

    axes[0, 0].semilogy(x, [row["factorized_gap_lower"] for row in rows], "o-", label="factorized gap lower")
    axes[0, 0].semilogy(x, [2.0 * row["snapshot_operator_upper"] for row in rows], "s--", label="twice operator radius")
    axes[0, 0].set_xticks(x, labels)
    axes[0, 0].set_ylabel("validated magnitude")
    axes[0, 0].set_title("All ten packet gaps remain open")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, which="both", alpha=0.2)

    colors = ["tab:orange" if row["enclosure_method"] == "interval_eigen" else "tab:blue" for row in rows]
    axes[0, 1].bar(labels, [row["gap_ratio"] for row in rows], color=colors)
    axes[0, 1].set_yscale("log")
    axes[0, 1].axhline(1.0, color="black", linestyle=":")
    axes[0, 1].set_ylabel(r"gap / $(2\varepsilon)$")
    axes[0, 1].set_title("Two coarse channels need interval-eigen rescue")
    axes[0, 1].grid(True, which="both", axis="y", alpha=0.2)

    axes[1, 0].bar(labels, [row["projector_radius"] for row in rows], color="tab:blue", label="projector")
    axes[1, 0].plot(labels, [row["polar_aligned_frame_radius"] for row in rows], "s", color="tab:red", label="polar frame")
    axes[1, 0].set_ylabel("certified operator radius")
    axes[1, 0].set_title("Certification is broad at the coarse right packet")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    rescued = [row for row in rows if row["enclosure_method"] == "interval_eigen"]
    width = 0.34
    rx = np.arange(len(rescued))
    axes[1, 1].bar(rx - width / 2, [row["snapshot_frobenius_upper"] for row in rescued], width, label="Frobenius upper", color="tab:gray")
    axes[1, 1].bar(rx + width / 2, [row["snapshot_interval_eigen_upper"] for row in rescued], width, label="interval eigen upper", color="tab:orange")
    axes[1, 1].set_xticks(rx, [f"{row['sigma']:.2f}-{row['side'][0]}" for row in rescued])
    axes[1, 1].set_yscale("log")
    axes[1, 1].set_ylabel("snapshot operator upper")
    axes[1, 1].set_title("Sharp norm extraction crosses the two thin walls")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, which="both", axis="y", alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "factorized_arb_snapshot_packet"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

