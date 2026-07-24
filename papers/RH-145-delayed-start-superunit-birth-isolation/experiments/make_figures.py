from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "delayed_start_audit.json").read_text(encoding="utf-8"))
    suffixes = data["suffixes"]
    events = data["superunit_events"]
    fig, axes = plt.subplots(2, 2, figsize=(12.4, 8.2))
    x = np.arange(len(suffixes))
    labels = [str(row["cutoff_sigma"]) for row in suffixes]
    axes[0, 0].bar(x - 0.18, [row["outward_positive_count"] for row in suffixes], 0.36, label="positive", color="tab:blue")
    axes[0, 0].bar(x + 0.18, [row["outward_chain_count"] for row in suffixes], 0.36, label="total", color="tab:gray", alpha=0.55)
    axes[0, 0].set_xticks(x, labels)
    axes[0, 0].set_xlabel("delayed-start cutoff sigma")
    axes[0, 0].set_ylabel("outward chains")
    axes[0, 0].set_title("The first completely clean suffix begins at 0.04")
    axes[0, 0].legend(frameon=False, fontsize=8)
    axes[0, 0].grid(True, axis="y", alpha=0.2)

    axes[0, 1].semilogy(labels, [row["minimum_positive_outward_terminal_floor"] for row in suffixes], "o-", color="tab:green")
    axes[0, 1].set_xlabel("delayed-start cutoff sigma")
    axes[0, 1].set_ylabel("minimum positive terminal floor")
    axes[0, 1].set_title("Finer suffixes have stronger finite terminal support")
    axes[0, 1].grid(True, which="both", alpha=0.2)

    ex = np.arange(len(events))
    axes[1, 0].bar(ex - 0.18, [row["birth"] for row in events], 0.36, label="birth q", color="tab:orange")
    axes[1, 0].bar(ex + 0.18, [row["candidate_family_minimum_floor"] for row in events], 0.36, label="least F(0)", color="tab:red")
    axes[1, 0].axhline(1.0, color="black", linestyle=":")
    axes[1, 0].set_xticks(ex, [f"{row['threshold']:.0e}" for row in events])
    axes[1, 0].set_ylabel("tail-envelope floor")
    axes[1, 0].set_title("Two events at one anchor are unavoidably superunit")
    axes[1, 0].legend(frameon=False, fontsize=8)
    axes[1, 0].grid(True, axis="y", alpha=0.2)

    n = np.arange(1, 21)
    finite = np.where(n == 3, 1.2, 0.4)
    recurrent = np.where(n % 4 == 0, 1.2, 0.4)
    axes[1, 1].step(n, finite, where="mid", label="one finite wall", color="tab:blue")
    axes[1, 1].step(n, recurrent, where="mid", label="recurrent walls", color="tab:red")
    axes[1, 1].axhline(1.0, color="black", linestyle=":")
    axes[1, 1].set_xlabel("level")
    axes[1, 1].set_ylabel("zero-state floor")
    axes[1, 1].set_title("Finite deletion is harmless; recurrent walls are fatal")
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "delayed_start_birth_isolation"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

