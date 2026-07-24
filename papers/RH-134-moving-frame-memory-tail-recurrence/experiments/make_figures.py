from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "memory_tail_audit.json").read_text(encoding="utf-8"))
    steps = [step for row in data["rows"] for step in row["steps"]]
    nonzero = [step for step in steps if step["total_forcing_norm"] > 0.0]
    recurrent = [step for step in steps if step["weighted_multiplicative_factor"] > 0.0]
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))

    axes[0].hist([step["weighted_multiplicative_factor"] for step in recurrent], bins=28, color="tab:blue", alpha=0.82)
    axes[0].axvline(2.0 / 512.0 * (1.0 + 1.0 / 512.0), color="tab:red", linestyle="--", label="uniform upper")
    axes[0].set_xlabel(r"weighted old-tail coefficient $\rho_t$")
    axes[0].set_ylabel("temporal updates")
    axes[0].set_title("Geometric memory decay is strongly contractive")
    axes[0].legend(frameon=False, fontsize=8)
    axes[0].grid(True, alpha=0.2)

    axes[1].scatter(
        [max(step["frame_forcing_norm"], 1e-40) for step in nonzero],
        [step["birth_forcing_norm"] for step in nonzero],
        s=20, alpha=0.5, color="tab:green",
    )
    low = min(max(step["frame_forcing_norm"], 1e-40) for step in nonzero)
    high = max(step["birth_forcing_norm"] for step in nonzero)
    axes[1].plot([low, high], [low, high], "k--", linewidth=1)
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("frame-change forcing norm")
    axes[1].set_ylabel("boundary-slice forcing norm")
    axes[1].set_title("Birth slice dominates all 240 nonzero forcings")
    axes[1].grid(True, alpha=0.2)

    axes[2].scatter(
        [step["minimum_principal_cosine"] for step in steps],
        [step["frame_defect_norm"] for step in steps],
        s=19, alpha=0.5, color="tab:purple",
    )
    axes[2].set_xlabel("minimum consecutive-frame cosine")
    axes[2].set_ylabel("polar frame-defect norm")
    axes[2].set_title("The recurrence tolerates large frame rotation")
    axes[2].grid(True, alpha=0.2)

    fig.tight_layout()
    output = ROOT / "figures" / "moving_frame_memory_tail_recurrence"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
