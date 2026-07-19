"""Build the RH-47 four-panel publication figure."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from peripheral_conditioning import anchored_bulk_ledger  # noqa: E402


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    pilot = load(ROOT / "results" / "small_noise_peripheral_factor_pilot.json")
    rows = pilot["rows"]
    sigma = np.asarray([float(row["sigma"]) for row in rows])
    log_clock_square = np.log(1.0 / sigma)
    perron_square = np.asarray(
        [float(row["perron_projector_norm"]) ** 2 for row in rows]
    )
    parity_square = np.asarray(
        [float(row["parity_projector_norm"]) ** 2 for row in rows]
    )
    rank_two_square = np.asarray(
        [float(row["weighted_rank_two_frobenius"]) ** 2 for row in rows]
    )

    figure, axes = plt.subplots(2, 2, figsize=(11.2, 7.8))
    axis = axes[0, 0]
    for values, fit, label, marker in (
        (perron_square, pilot["perron_log_fit"], "Perron projector", "o"),
        (parity_square, pilot["parity_log_fit"], "parity projector", "s"),
        (rank_two_square, pilot["rank_two_log_fit"], "rank-two weighted term", "^"),
    ):
        axis.plot(log_clock_square, values, marker=marker, label=label)
        fitted = float(fit["slope"]) * log_clock_square + float(
            fit["intercept"]
        )
        axis.plot(log_clock_square, fitted, linestyle="--", alpha=0.65)
    axis.set_xlabel(r"$\log(1/\sigma)$")
    axis.set_ylabel("squared Hilbert--Schmidt norm")
    axis.set_title("(a) Logarithmic peripheral growth")
    axis.grid(True, alpha=0.3)
    axis.legend(fontsize=8)

    axis = axes[0, 1]
    axis.semilogx(
        sigma,
        perron_square / log_clock_square,
        marker="o",
        label="Perron",
    )
    axis.semilogx(
        sigma,
        parity_square / log_clock_square,
        marker="s",
        label="parity",
    )
    axis.semilogx(
        sigma,
        rank_two_square / log_clock_square,
        marker="^",
        label="rank two",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel(r"norm$^2/\log(1/\sigma)$")
    axis.set_title("(b) Regular-variation index zero")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=8)

    axis = axes[1, 0]
    selected = [
        row
        for row in rows
        if row["endpoint_perron_tail_coefficient"] is not None
    ]
    selected_sigma = np.asarray([float(row["sigma"]) for row in selected])
    axis.semilogx(
        selected_sigma,
        [float(row["endpoint_perron_tail_coefficient"]) for row in selected],
        marker="o",
        label="stationary density",
    )
    axis.semilogx(
        selected_sigma,
        [float(row["endpoint_parity_tail_coefficient"]) for row in selected],
        marker="s",
        label="signed parity density",
    )
    axis.axhline(
        float(pilot["analytic_endpoint_tail_constant"]),
        color="black",
        linestyle="--",
        label=r"$\rho_c/(2\sqrt{u_c})$",
    )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel(r"median $\sqrt{t}\,|g(1-t)|$")
    axis.set_title("(c) Mesoscopic endpoint coefficient")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=8)

    axis = axes[1, 1]
    schedule_sigmas = np.logspace(-4, -2, 80)
    for power, marker in ((1.5, "o"), (2.0, "s"), (2.25, "^"), (2.5, "d")):
        errors = []
        for width in schedule_sigmas:
            dimension = max(
                2,
                int(np.ceil(65536.0 * (0.01 / width) ** power)),
            )
            errors.append(
                anchored_bulk_ledger(width, dimension)
                .anchored_square_trace_norm_error_upper
            )
        axis.loglog(
            schedule_sigmas,
            errors,
            label=fr"$p={power:g}$",
            marker=marker,
            markevery=18,
            markersize=3,
        )
    axis.invert_xaxis()
    axis.set_xlabel(r"noise width $\sigma$")
    axis.set_ylabel("normalized square trace-error upper")
    axis.set_title("(d) Anchored bulk retains the $p>2$ gate")
    axis.grid(True, which="both", alpha=0.3)
    axis.legend(fontsize=8)

    figure.suptitle(
        "Endpoint spikes, logarithmic peripheral conditioning, and anchored deflation",
        fontsize=12,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.96))
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "logarithmic_peripheral_conditioning.png", dpi=220)
    figure.savefig(output / "logarithmic_peripheral_conditioning.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
