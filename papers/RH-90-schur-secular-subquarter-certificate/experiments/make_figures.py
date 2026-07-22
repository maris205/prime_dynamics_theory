"""Make the RH-90 Schur-certificate figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    audit = json.loads((ROOT / "results" / "schur_certificate_audit.json").read_text(encoding="utf-8"))
    rows = audit["rows"]
    sigma = [row["sigma"] for row in rows]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["binary64_predictor_factor"] for channel in channels], marker="o", label=side)
    ax.axhline(audit["target_contraction"], color="black", linestyle="--", label="target")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("old-packet predictor factor")
    ax.set_title("(a) Required correction before the Ritz step"); ax.legend()

    ax = axes[0, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        values = [channel["binary64_gain_to_required_ratio"] if channel["binary64_gain_to_required_ratio"] is not None else 1.0 for channel in channels]
        ax.semilogy(sigma, values, marker="o", label=side)
    ax.axhline(1.0, color="black", linestyle="--", label="required gain")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("actual small gain / required gain")
    ax.set_title("(b) Schur gain clears the target"); ax.legend()

    ax = axes[1, 0]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        margins = [max(1e-30, -channel["interval_schur_trial_form_upper"]) for channel in channels]
        ax.semilogy(sigma, margins, marker="o", label=side)
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("certified negative Schur margin")
    ax.set_title("(c) Nine strict small-matrix certificates"); ax.legend()

    ax = axes[1, 1]
    for side in ("left", "right"):
        channels = [next(channel for channel in row["channels"] if channel["side"] == side) for row in rows]
        ax.plot(sigma, [channel["interval_corrected_contraction_upper"] for channel in channels], marker="o", label=side)
    ax.axhline(audit["target_contraction"], color="black", linestyle="--", label="0.24 target")
    ax.set_xscale("log"); ax.invert_xaxis(); ax.grid(alpha=0.25)
    ax.set_xlabel(r"noise $\sigma$"); ax.set_ylabel("direct corrected contraction")
    ax.set_title("(d) Full-reference-free finite closure"); ax.legend()

    fig.tight_layout()
    output = ROOT / "figures" / "schur_secular_subquarter_certificate"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
