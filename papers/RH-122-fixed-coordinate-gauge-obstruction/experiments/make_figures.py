import json
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "fixed_coordinate_audit.json").read_text())
    eps = [r["epsilon"] for r in data["records"]]
    factor = [r["fixed_transfer_factor"] for r in data["records"]]
    upper = [r["fixed_gamma_upper"] for r in data["records"]]
    target = [r["target_gamma"] for r in data["records"]]
    fig, axes = plt.subplots(1, 2, figsize=(10.7, 4.2))
    axes[0].loglog(eps, factor, color="tab:red", lw=2, label=r"fixed $\sqrt{b/a}$")
    axes[0].loglog(eps, [1.0] * len(eps), color="tab:green", ls="--", label="exact gauge")
    axes[0].invert_xaxis(); axes[0].set_xlabel(r"anisotropy $\varepsilon$"); axes[0].set_ylabel("transfer factor")
    axes[0].set_title("Coordinate loss is unbounded"); axes[0].legend(frameon=False); axes[0].grid(True, which="both", alpha=.22)
    axes[1].loglog(eps, upper, color="tab:orange", lw=2, label="fixed-coordinate upper")
    axes[1].loglog(eps, target, color="black", ls="--", label="actual target gamma")
    axes[1].invert_xaxis(); axes[1].set_xlabel(r"anisotropy $\varepsilon$"); axes[1].set_ylabel(r"$\gamma$")
    axes[1].set_title("Invariant pair, divergent certificate"); axes[1].legend(frameon=False); axes[1].grid(True, which="both", alpha=.22)
    fig.tight_layout()
    output = ROOT / "figures" / "fixed_coordinate_gauge_obstruction"
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=220, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__": main()

