"""Render the RH-35 exact packet-pair count-transfer figure."""

from __future__ import annotations

from fractions import Fraction
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def scientific_latex(value: float) -> str:
    mantissa, exponent = f"{float(value):.3e}".split("e")
    return rf"{mantissa}\times10^{{{int(exponent)}}}"


def main() -> None:
    summary = json.loads(
        (ROOT / "results" / "summary.json").read_text(encoding="utf-8")
    )
    defect = json.loads(
        (ROOT / "results" / "exact_packet_defect_sigma_1e-02.json").read_text(
            encoding="utf-8"
        )
    )
    transfer = read_csv(
        ROOT / "results" / "packet_pair_transfer_sigma_1e-02.csv"
    )
    with np.load(
        ROOT / "results" / "floating_packet_pair_sigma_1e-02.npz"
    ) as archive:
        physical_values = np.asarray(archive["physical_eigenvalues"])
        center = complex(archive["contour_center"].item())
        radius = float(archive["contour_radius"].item())
    defect_matrix = np.asarray(
        [
            [
                float(Fraction(item["numerator"], item["denominator"]))
                for item in row
            ]
            for row in defect["pair_defect_entries"]
        ]
    )
    theta = np.asarray([float(row["theta_midpoint"]) for row in transfer])
    complement_products = np.asarray(
        [float(row["complement_neumann_product_upper"]) for row in transfer]
    )
    feshbach_products = np.asarray(
        [float(row["feshbach_rouche_product_upper"]) for row in transfer]
    )

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10})
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.5))
    first, second, third, fourth = axes.reshape(-1)

    first.scatter(
        physical_values.real,
        physical_values.imag,
        s=8,
        alpha=0.45,
        color="#356aa0",
        linewidths=0,
    )
    angle = np.linspace(0.0, 2.0 * np.pi, 600)
    first.plot(
        center.real + radius * np.cos(angle),
        center.imag + radius * np.sin(angle),
        color="#b13b32",
        linewidth=1.5,
        label=r"counting circle $\Gamma$",
    )
    inside = np.abs(physical_values - center) < radius
    first.scatter(
        physical_values.real[inside],
        physical_values.imag[inside],
        marker="*",
        s=90,
        color="#e28b21",
        edgecolor="black",
        linewidth=0.4,
        zorder=4,
        label="floating interior candidate",
    )
    first.set_aspect("equal", adjustable="box")
    first.set_xlabel(r"$\Re\lambda$")
    first.set_ylabel(r"$\Im\lambda$")
    first.set_title("Physical two-step floating spectrum (diagnostic)")
    first.legend(loc="upper right", fontsize=8)

    image = second.imshow(
        np.log10(np.maximum(np.abs(defect_matrix), np.finfo(float).tiny)),
        cmap="magma",
        aspect="equal",
    )
    second.set_xticks(range(defect_matrix.shape[1]))
    second.set_yticks(range(defect_matrix.shape[0]))
    second.set_xlabel("packet column")
    second.set_ylabel("packet row")
    second.set_title(r"Exact dyadic $WV-I_4$: $\log_{10}|\cdot|$")
    figure.colorbar(image, ax=second, fraction=0.046, pad=0.04)

    turns = theta / (2.0 * np.pi)
    third.semilogy(
        turns,
        complement_products,
        color="#356aa0",
        linewidth=1.0,
        label="corrected-complement Neumann product",
    )
    third.semilogy(
        turns,
        feshbach_products,
        color="#b13b32",
        linewidth=1.0,
        label=r"$F\to\widehat F$ Rouché product",
    )
    third.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
    third.set_xlabel("contour turn")
    third.set_ylabel("rigorous product upper")
    third.set_title("All 949 leaves close both homotopies")
    third.grid(alpha=0.2, which="both")
    third.legend(loc="lower right", fontsize=8)

    fourth.axis("off")
    pair_text = scientific_latex(summary["pair_defect_frobenius_upper"])
    complement_text = scientific_latex(
        summary["maximum_complement_neumann_product_upper"]
    )
    feshbach_text = f"{summary['maximum_feshbach_rouche_product_upper']:.6f}"
    lines = [
        "Certified exact packet-pair bridge",
        "",
        rf"$\|WV-I_4\|_F\leq {pair_text}$",
        rf"$\widehat W=(WV)^{{-1}}W,\quad \widehat W V=I_4$",
        rf"$\max_\Gamma q_B\leq {complement_text}<1$",
        rf"$\max_\Gamma q_F\leq {feshbach_text}<1$",
        "",
        rf"$N_\Gamma(\widehat B)=0$",
        rf"$\operatorname{{wind}}_\Gamma\det\widehat F=1$",
        rf"$z^4\det(zI-U^2)=\det(zI-\widehat B)\det\widehat F$",
        "",
        rf"$N_\Gamma(U^2)=1$",
    ]
    fourth.text(
        0.03,
        0.96,
        "\n".join(lines),
        transform=fourth.transAxes,
        va="top",
        ha="left",
        fontsize=10.5,
        linespacing=1.45,
        bbox={
            "boxstyle": "round,pad=0.65",
            "facecolor": "#f7f5ef",
            "edgecolor": "#9a9587",
        },
    )
    fourth.set_title("Exact count transfer", pad=6)

    figure.suptitle(
        "RH-35: exact packet-pair correction and physical two-step count",
        fontsize=12,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "packet_pair_physical_count.pdf", bbox_inches="tight")
    figure.savefig(
        output / "packet_pair_physical_count.png",
        dpi=220,
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
