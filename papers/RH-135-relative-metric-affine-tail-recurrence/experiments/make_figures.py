from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "relative_affine_audit.json").read_text(encoding="utf-8"))
    steps = [step for row in data["rows"] for step in row["steps"]]
    recurrent = [step for step in steps if step["metric_decay_base"]["value"] not in (None, 0.0)]
    feasible = [step for step in recurrent if step["optimization"]["contractive_feasible"]]
    infeasible = [step for step in recurrent if not step["optimization"]["contractive_feasible"]]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    axes[0].hist(
        [step["metric_decay_base"]["log10"] for step in recurrent], bins=38,
        color="tab:blue", alpha=0.82,
    )
    axes[0].axvline(0.0, color="tab:red", linestyle="--", label=r"$A=1$ contractivity wall")
    axes[0].set_xlabel(r"$\log_{10} A_t$ for $\rho=A_t(1+\tau)$")
    axes[0].set_ylabel("recurrent updates")
    axes[0].set_title("Metric amplification defeats raw decay often")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(True, alpha=0.2)

    axes[1].scatter(
        [step["metric_decay_base"]["log10"] for step in feasible],
        [step["q_birth"]["log10"] for step in feasible],
        s=24, alpha=0.62, color="tab:green", label="contractive",
    )
    axes[1].scatter(
        [step["metric_decay_base"]["log10"] for step in infeasible],
        [step["q_birth"]["log10"] for step in infeasible],
        s=24, alpha=0.52, color="tab:red", label="no subunit rho",
    )
    axes[1].axvline(0.0, color="black", linestyle="--", linewidth=1)
    axes[1].set_xlabel("metric-decay base log10")
    axes[1].set_ylabel("birth forcing q log10")
    axes[1].set_title("Small forcing cannot repair metric mismatch")
    axes[1].legend(frameon=False, fontsize=8)
    axes[1].grid(True, alpha=0.2)

    labels = ["zero tail", "first birth", "recurrent\ncontractive", "recurrent\nblocked"]
    values = [90, 24, 51, 165]
    axes[2].bar(labels, values, color=["tab:gray", "tab:orange", "tab:green", "tab:red"])
    axes[2].set_ylabel("temporal updates")
    axes[2].set_title("Relative-metric classification of 330 updates")
    axes[2].grid(True, axis="y", alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "relative_metric_affine_tail_recurrence"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
