"""Create the RH-95 reduced-factorization conditioning figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "reduced_cross_factorization_audit.json"
PDF = ROOT / "figures" / "reduced_cross_moment_factorization.pdf"
PNG = ROOT / "figures" / "reduced_cross_moment_factorization.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    channels = [channel for row in audit["rows"] for channel in row["channels"]]
    labels = [f"{row['sigma']:.2g}{channel['side'][0].upper()}" for row in audit["rows"] for channel in row["channels"]]
    steps = [step for channel in channels for step in channel["steps"]]
    cutoff = np.array([step["cutoff_to_leading_singular_ratio"] for step in steps])
    moment = np.array([step["compressed_moment_relative_error"] for step in steps])
    tail = np.array([step["interval_reduced_to_ambient_tail_upper"] - 1.0 for step in steps])
    direction = np.array([step["stabilized_direction_projector_distance"] for step in steps])
    endpoint = np.array([channel["interval_endpoint_to_reference_upper"] for channel in channels])
    weak = np.array([sum(step["weak_cutoff_mode"] for step in channel["steps"]) for channel in channels])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.semilogy(np.sort(cutoff), "o", markersize=3.5, color="#d95f02")
    ax.axhline(1e-8, color="#222222", linestyle=":", label="weak-mode threshold")
    ax.set_xlabel("sorted update")
    ax.set_ylabel(r"$s_4(K)/s_1(K)$")
    ax.set_title("(a) The fourth mode can be nearly singular")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    ax.loglog(np.maximum(cutoff, 1e-20), np.maximum(moment, 1e-20), "o", markersize=3.8, color="#7570b3", alpha=0.75)
    ax.axhline(1e-3, color="#222222", linestyle=":", label="moment failure threshold")
    ax.set_xlabel(r"$s_4(K)/s_1(K)$")
    ax.set_ylabel("moment-compression relative error")
    ax.set_title("(b) Normal equations expose cancellation")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    ax.semilogy(np.sort(np.maximum(direction, 1e-18)), "o", markersize=3.5, color="#e7298a", label="direction projector")
    ax.semilogy(np.sort(np.maximum(tail, 1e-18)), "s", markersize=3.2, color="#1b9e77", label="tail excess")
    ax.set_xlabel("sorted update")
    ax.set_ylabel("reduced-versus-ambient discrepancy")
    ax.set_title("(c) Direction loss is larger than tail loss")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 1]
    x = np.arange(len(channels))
    ax.plot(x, endpoint, "o-", color="#1b9e77", label="endpoint/reference")
    ax.axhline(1.01, color="#222222", linestyle=":", label="RH-94 gate")
    ax2 = ax.twinx()
    ax2.bar(x, weak, width=0.45, color="#66c2a5", alpha=0.35, label="weak updates")
    ax.set_xticks(x, labels, rotation=45, ha="right")
    ax.set_ylabel("endpoint tail ratio")
    ax2.set_ylabel("weak fourth-mode count")
    ax.set_title("(d) QR stabilization preserves every endpoint")
    ax.grid(alpha=0.25)
    handles, legends = ax.get_legend_handles_labels()
    handles2, legends2 = ax2.get_legend_handles_labels()
    ax.legend(handles + handles2, legends + legends2, frameon=False, fontsize=8)

    figure.suptitle("RH-95: exact reduced factorization meets a weak-mode conditioning barrier", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "updates": len(steps)}, sort_keys=True))


if __name__ == "__main__":
    main()
