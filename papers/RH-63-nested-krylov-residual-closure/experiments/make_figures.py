"""Render the RH-63 nested residual figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "nested_krylov_pilot.json"
PDF = ROOT / "figures" / "nested_krylov_closure.pdf"
PNG = ROOT / "figures" / "nested_krylov_closure.png"


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    figure, axes = plt.subplots(1, 2, figsize=(10.0, 4.2))
    colors = ("#1f77b4", "#d62728", "#2ca02c", "#9467bd")

    axis = axes[0]
    for index, model in enumerate(payload["models"]):
        endpoint = model["horizons"]["32"]
        schedules = list(endpoint)
        values = [endpoint[key]["upper_over_exact"] for key in schedules]
        axis.semilogy(
            range(len(schedules)),
            values,
            "o-",
            color=colors[index],
            label=model["name"].replace("_", " "),
        )
        axis.set_xticks(range(len(schedules)), schedules)
    axis.set_xlabel("nested schedule")
    axis.set_ylabel("upper / exact at $L=32$")
    axis.set_title("Coherent residual closure")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, fontsize=7)

    axis = axes[1]
    model = payload["models"][1]
    horizons = [int(value) for value in payload["horizons"]]
    for key, marker, color in (("1", "o", "#1f77b4"), ("1x1", "s", "#d62728")):
        values = [
            model["horizons"][str(horizon)][key]["upper_over_exact"]
            for horizon in horizons
        ]
        axis.semilogy(
            horizons,
            values,
            marker=marker,
            color=color,
            label=f"schedule {key}",
        )
    axis.set_xlabel("horizon $L$")
    axis.set_ylabel("upper / exact power norm")
    axis.set_title("RH-60 two-block repair")
    axis.grid(True, which="both", alpha=0.25)
    axis.legend(frameon=False, fontsize=8)

    figure.tight_layout(pad=1.0)
    PDF.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(PDF, bbox_inches="tight")
    figure.savefig(PNG, dpi=180, bbox_inches="tight")
    print(
        json.dumps(
            {"pdf": str(PDF.relative_to(ROOT)), "png": str(PNG.relative_to(ROOT))},
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
