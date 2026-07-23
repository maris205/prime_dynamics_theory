"""Create RH-111 concentration figures."""
from __future__ import annotations
import json, math
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
ROOT = Path(__file__).resolve().parents[1]

def main() -> None:
    data = json.loads((ROOT / "results/exterior_concentration_audit.json").read_text(encoding="utf-8"))
    fig, axes = plt.subplots(1, 2, figsize=(10.9, 4.25))
    ax = axes[0]
    by_rank = {}
    for row in data["rows"]:
        for channel in row["channels"]:
            for rec in channel["thresholds"]:
                if float(rec["threshold"]) == 1e-8:
                    for step in rec["steps"]:
                        by_rank.setdefault(step["packet_rank"], []).append(step["actual_concentration"])
    ranks = sorted(by_rank)
    ax.boxplot([by_rank[r] for r in ranks], positions=ranks, widths=0.5, showfliers=False)
    ax.plot(ranks, [math.comb(r,4) for r in ranks], "o--", color="tab:red", label=r"universal $\binom{r}{4}$")
    ax.set_yscale("log")
    ax.set_xlabel("packet rank")
    ax.set_ylabel(r"exterior concentration $\kappa_4$")
    ax.set_title("Physical concentration versus worst case")
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(frameon=False)

    ax = axes[1]
    keys = ["1e-08", "1e-06", "1e-04"]
    labels = [r"$10^{-8}$", r"$10^{-6}$", r"$10^{-4}$"]
    x = np.arange(3); width=.25
    generic=[data["threshold_summary"][k]["fine_generic_support_count"] for k in keys]
    refined=[data["threshold_summary"][k]["fine_refined_support_count"] for k in keys]
    spectral=[data["threshold_summary"][k]["fine_spectral_support_count"] for k in keys]
    ax.bar(x-width,generic,width,label=r"generic $\sqrt{D}$")
    ax.bar(x,refined,width,label="tail-energy refined")
    ax.bar(x+width,spectral,width,label="spectral exterior")
    ax.set_xticks(x,labels); ax.set_ylim(0,82)
    ax.set_ylabel("fine certified updates (of 78)")
    ax.set_title("Trace certificate recovery")
    ax.grid(True, axis="y", alpha=.25); ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    out=ROOT/"figures/tail_energy_exterior_concentration"; out.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(out.with_suffix('.pdf'),bbox_inches='tight'); fig.savefig(out.with_suffix('.png'),dpi=220,bbox_inches='tight'); plt.close(fig)
if __name__ == '__main__': main()
