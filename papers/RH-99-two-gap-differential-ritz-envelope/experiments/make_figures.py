"""Create the RH-99 two-gap differential envelope figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "two_gap_differential_audit.json"
PDF = ROOT / "figures" / "two_gap_differential_ritz_envelope.pdf"
PNG = ROOT / "figures" / "two_gap_differential_ritz_envelope.png"


def main() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    steps = [step for row in audit["rows"] for channel in row["channels"] for step in channel["steps"]]
    available = [step for step in steps if step["differential_certificate_available"]]
    quotient = [step for step in steps if step["selected_width"] < 4]
    probe = np.array([step["maximum_probe_derivative"] for step in available])
    bound = np.array([step["two_gap_derivative_bound"] for step in available])
    cross_gap = np.array([step["cross_squared_gap"] for step in steps])
    ritz_gap = np.array([step["ritz_gap"] for step in steps])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9})
    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.4), constrained_layout=True)

    ax = axes[0, 0]
    ax.loglog(probe, bound, "o", markersize=4, color="#7570b3", alpha=0.75)
    low = min(probe.min(), bound.min())
    high = max(probe.max(), bound.max())
    ax.plot([low, high], [low, high], color="#222222", linestyle=":", label="exact derivative")
    ax.set_xlabel("largest finite tangent probe")
    ax.set_ylabel("two-gap derivative upper bound")
    ax.set_title("(a) The theorem closes but is extremely conservative")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    ax.semilogy(np.sort(cross_gap), "o", markersize=3.2, color="#1b9e77", label="cross squared gap")
    ax.semilogy(np.sort(np.maximum(ritz_gap, 1e-20)), "s", markersize=3.0, color="#d95f02", label="Ritz gap (clipped)")
    ax.axhline(1e-20, color="#222222", linestyle=":")
    ax.set_xlabel("sorted update")
    ax.set_ylabel("gap diagnostic")
    ax.set_title("(b) Five output Ritz gaps are not certifiably positive")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1, 0]
    labels = [f"t={step['time']}" for step in quotient]
    ratios = [step["full_to_adaptive_bound_ratio"] for step in quotient]
    ax.bar(np.arange(len(quotient)), ratios, color="#66a61e")
    ax.set_yscale("log")
    ax.set_xticks(np.arange(len(quotient)), labels, rotation=45, ha="right")
    ax.set_ylabel("full-width / adaptive derivative bound")
    ax.set_title("(c) Quotienting improves all five formal envelopes")
    ax.grid(alpha=0.25, axis="y", which="both")

    ax = axes[1, 1]
    distance = np.array([step["adaptive_to_full_projector_distance"] for step in quotient])
    radius = np.array([max(step["two_gap_linearized_radius"], 1e-40) for step in quotient])
    positions = np.arange(len(quotient))
    ax.semilogy(positions - 0.12, distance, "o", color="#e7298a", label="quotient displacement")
    ax.semilogy(positions + 0.12, radius, "s", color="#1f78b4", label="first-order radius")
    ax.set_xticks(positions, labels, rotation=45, ha="right")
    ax.set_ylabel("projector scale")
    ax.set_title("(d) No actual quotient lies inside the linearized tube")
    ax.grid(alpha=0.25, which="both")
    ax.legend(frameon=False, fontsize=8)

    figure.suptitle("RH-99: two-gap differential control is local, conservative, and not yet a tube", fontsize=12)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF)
    figure.savefig(PNG, dpi=220)
    plt.close(figure)
    print(json.dumps({"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT)), "updates": len(steps), "available": len(available)}, sort_keys=True))


if __name__ == "__main__":
    main()
