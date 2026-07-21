"""Create the RH-59 flag-metric packet audit figure."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    payload = load(ROOT / "results" / "flag_metric_pilot.json")
    rows = payload["rows"]
    sigma = np.asarray([row["sigma"] for row in rows])
    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.3))
    styles = {
        "left": ("#174a7e", "o"),
        "right": ("#c44e52", "s"),
    }

    ax = axes[0, 0]
    for side, (color, marker) in styles.items():
        ax.semilogx(
            sigma,
            [row[side]["exact_hardy_energy"] for row in rows],
            marker + "-",
            color=color,
            label=side + " exact",
        )
        ax.semilogx(
            sigma,
            [row[side]["metric_absolute_upper"] for row in rows],
            marker + "--",
            color=color,
            alpha=0.82,
            label=side + " flag metric",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"Hardy magnitude at $r=0.85$")
    ax.set_title("(a) Packetwise positive Stein upper")
    ax.legend(fontsize=7)

    ax = axes[0, 1]
    for side, (color, marker) in styles.items():
        ax.loglog(
            sigma,
            [row[side]["metric_absolute_upper"] for row in rows],
            marker + "-",
            color=color,
            label=side + " RH-59 metric",
        )
        ax.loglog(
            sigma,
            [
                row[side]["inherited_rh58"]["scalar_path_upper"]
                for row in rows
            ],
            marker + ":",
            color=color,
            alpha=0.72,
            label=side + " RH-58 paths",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("sufficient upper")
    ax.set_title("(b) Exact dissipation removes path proliferation")
    ax.legend(fontsize=7)

    ax = axes[1, 0]
    for side, (color, marker) in styles.items():
        ax.loglog(
            sigma,
            [row[side]["packets"][-1]["exact_packet_energy"] for row in rows],
            marker + "-",
            color=color,
            label=side + " outer exact",
        )
        ax.loglog(
            sigma,
            [
                row[side]["packets"][-1]["metric_energy_upper"]
                for row in rows
            ],
            marker + "--",
            color=color,
            alpha=0.82,
            label=side + " outer metric",
        )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("outer-packet magnitude")
    ax.set_title("(c) Growth localizes in the outer packet")
    ax.legend(fontsize=7)

    ax = axes[1, 1]
    smallest = rows[-1]
    labels = [packet["name"] for packet in smallest["left"]["packets"]]
    positions = np.arange(len(labels), dtype=float)
    width = 0.36
    for offset, (side, (color, _)) in zip(
        (-width / 2.0, width / 2.0), styles.items()
    ):
        ax.bar(
            positions + offset,
            [
                packet["metric_upper_over_exact"]
                for packet in smallest[side]["packets"]
            ],
            width,
            color=color,
            alpha=0.84,
            label=side,
        )
    ax.set_yscale("log")
    ax.axhline(1.0, color="#333333", linewidth=0.8)
    ax.set_xticks(positions, ["central", "inner", "middle", "edge"])
    ax.set_ylabel("metric upper / exact packet")
    ax.set_title(r"(d) Endpoint loss at $\sigma=0.01$")
    ax.legend(fontsize=7)

    figure.tight_layout()
    output = ROOT / "figures" / "flag_adapted_schur_stein"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
