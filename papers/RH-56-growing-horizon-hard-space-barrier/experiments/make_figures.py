"""Create the RH-56 four-panel audit figure."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from hardy_barrier import strong_space_ledger  # noqa: E402


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(ROOT / "results" / "hardy_barrier_pilot.json")
    rows = pilot["all_column_dense_audit"]
    production = pilot["production_directional_audit"]
    tails = pilot["deterministic_tail_audit"]
    radius = pilot["hardy_radius"]

    figure, axes = plt.subplots(2, 2, figsize=(10.8, 7.3))

    ax = axes[0, 0]
    theta = np.linspace(0.08, radius - 0.01, 500)
    total = [
        2.0 * strong_space_ledger(radius, value, 1.0).energy_power
        for value in theta
    ]
    ax.plot(theta, total, color="#174a7e", linewidth=2.2)
    ax.axhline(0.25, color="#c44e52", linestyle="--", label="RH-54 budget")
    ax.axvline(
        pilot["strong_space_barrier"]["common_rate_threshold"],
        color="#55a868",
        linestyle=":",
        label=r"$r^{8}$ threshold",
    )
    ax.axvline(
        pilot["deterministic_edge_radius"],
        color="#8172b2",
        linestyle="-.",
        label="deterministic edge",
    )
    ax.set_ylim(0.0, 4.2)
    ax.set_xlabel(r"strong decay rate $\theta$")
    ax.set_ylabel(r"two-direction power $\alpha_B+\alpha_C$")
    ax.set_title("(a) Black-box exponent wall")
    ax.legend(fontsize=8, loc="upper left")

    ax = axes[0, 1]
    sigma = np.asarray([row["sigma"] for row in rows])
    ax.semilogx(
        sigma,
        [row["left_exact_hardy_energy"] for row in rows],
        "o-",
        label="left all-column",
    )
    ax.semilogx(
        sigma,
        [row["right_exact_hardy_energy"] for row in rows],
        "s-",
        label="right all-column",
    )
    ax.semilogx(
        sigma,
        [row["radial_hardy_clock"] for row in rows],
        "^-",
        label="radial clock",
    )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("magnitude")
    ax.set_title("(b) Deterministic full-column audit")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    psigma = np.asarray([row["sigma"] for row in production])
    ax.semilogx(
        psigma,
        [row["left_truncated_energy_r085"] for row in production],
        "o-",
        label="left",
    )
    ax.semilogx(
        psigma,
        [row["right_truncated_energy_r085"] for row in production],
        "s-",
        label="right",
    )
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"truncated $\mathcal{E}(0.85)$")
    ax.set_title("(c) Production directional evidence")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    horizon = np.asarray([row["horizon"] for row in tails])
    ax.semilogy(
        horizon,
        [row["left_block_power_norm"] for row in tails],
        "o-",
        label="left block norm",
    )
    ax.semilogy(
        horizon,
        [row["right_block_power_norm"] for row in tails],
        "s-",
        label="right block norm",
    )
    ax.semilogy(
        horizon,
        [row["maximum_relative_energy_excess"] for row in tails],
        "^-",
        label="relative tail excess",
    )
    ax.set_xlabel("growing horizon")
    ax.set_ylabel("binary64 diagnostic")
    ax.set_title("(d) Block-tail mechanism")
    ax.legend(fontsize=8)

    figure.tight_layout()
    output = ROOT / "figures" / "growing_horizon_hard_space_barrier"
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    figure.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(figure)
    print(str(output.relative_to(ROOT)))


if __name__ == "__main__":
    main()
