"""Render the RH-34 Schur-similarity closure figure."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RH33 = ROOT.parent / "RH-33-certified-complement-resolvent-atlas"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def scientific_latex(value: float) -> str:
    mantissa, exponent = f"{float(value):.3e}".split("e")
    return rf"{mantissa}\times 10^{{{int(exponent)}}}"


def main() -> None:
    summary = json.loads(
        (ROOT / "results" / "summary.json").read_text(encoding="utf-8")
    )
    certificate = json.loads(
        (ROOT / "results" / "schur_similarity_sigma_1e-02.json").read_text(
            encoding="utf-8"
        )
    )
    diagonal = read_csv(ROOT / "results" / "schur_diagonal_sigma_1e-02.csv")
    homotopy = read_csv(
        ROOT / "results" / "schur_homotopy_leaves_sigma_1e-02.csv"
    )
    atlas = read_csv(
        RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    )
    if len(homotopy) != len(atlas):
        raise RuntimeError("homotopy and atlas ledgers do not align")

    real = np.asarray([float(row["diagonal_real"]) for row in diagonal])
    imag = np.asarray([float(row["diagonal_imag"]) for row in diagonal])
    distances = np.asarray(
        [float(row["floating_signed_boundary_distance"]) for row in diagonal]
    )
    theta = np.asarray([float(row["theta_midpoint"]) for row in atlas])
    inverse = np.asarray(
        [float(row["complement_resolvent_upper"]) for row in homotopy]
    )
    products = np.asarray(
        [float(row["homotopy_neumann_product_upper"]) for row in homotopy]
    )
    center = complex(
        float(certificate["contour_center_real"]),
        float(certificate["contour_center_imag"]),
    )
    radius = float(certificate["contour_radius"])

    plt.rcParams.update({"font.size": 9, "axes.titlesize": 10})
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.5))
    first, second, third, fourth = axes.reshape(-1)

    first.scatter(real, imag, s=8, alpha=0.45, color="#356aa0", linewidths=0)
    angle = np.linspace(0.0, 2.0 * np.pi, 600)
    first.plot(
        center.real + radius * np.cos(angle),
        center.imag + radius * np.sin(angle),
        color="#b13b32",
        linewidth=1.6,
        label=r"counting circle $\Gamma$",
    )
    nearest = int(certificate["nearest_diagonal_index"])
    first.scatter(
        [real[nearest]],
        [imag[nearest]],
        marker="*",
        s=90,
        color="#e28b21",
        edgecolor="black",
        linewidth=0.4,
        zorder=4,
        label="nearest stored diagonal",
    )
    first.set_aspect("equal", adjustable="box")
    first.set_xlabel(r"$\Re \tau_j$")
    first.set_ylabel(r"$\Im \tau_j$")
    first.set_title("Exact stored triangular diagonal: 2048/2048 outside")
    first.legend(loc="upper right", fontsize=8)

    order = np.argsort(distances)
    second.semilogy(
        np.arange(distances.size),
        distances[order],
        color="#356aa0",
        linewidth=1.1,
    )
    second.axhline(
        float(summary["minimum_floating_diagonal_boundary_distance"]),
        color="#e28b21",
        linestyle="--",
        linewidth=1.0,
    )
    second.set_xlabel("diagonal index after sorting by clearance")
    second.set_ylabel("floating boundary clearance")
    second.set_title("Dyadic signs are exact; distances are diagnostics")
    second.grid(alpha=0.2, which="both")

    turns = theta / (2.0 * np.pi)
    third.semilogy(
        turns,
        inverse,
        color="#356aa0",
        linewidth=1.0,
        label=r"RH-33 $\|(zI-B)^{-1}\|_2$ upper",
    )
    twin = third.twinx()
    twin.semilogy(
        turns,
        products,
        color="#b13b32",
        linewidth=1.0,
        label="Schur homotopy product",
    )
    twin.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
    third.set_xlabel("contour turn")
    third.set_ylabel("complement resolvent upper", color="#356aa0")
    twin.set_ylabel("homotopy product", color="#b13b32")
    third.set_title("All 949 inherited rational leaves remain invertible")
    third.grid(alpha=0.2, which="both")

    fourth.axis("off")
    residual_text = scientific_latex(
        float(summary["schur_residual_frobenius_upper"])
    )
    defect_text = scientific_latex(
        float(summary["unitarity_defect_frobenius_upper"])
    )
    product_text = scientific_latex(
        float(summary["maximum_homotopy_neumann_product_upper"])
    )
    lines = [
        r"Certified stored-model ledger",
        "",
        rf"$\Vert BZ-ZT\Vert_F \leq {residual_text}$",
        rf"$\Vert Z^*Z-I\Vert_F \leq {defect_text}$",
        rf"$\max_{{\Gamma}} q(z) \leq {product_text}<1$",
        rf"$N_\Gamma(T)=0 \Longrightarrow N_\Gamma(B)=0$",
        rf"RH-33: $N_\Gamma(\mathcal{{M}}_{{\rm st}})-N_\Gamma(B)=1$",
        "",
        rf"$N_\Gamma(\mathcal{{M}}_{{\rm st}})=1$",
        rf"$\operatorname{{wind}}_\Gamma\det F=1$ with no complement poles",
    ]
    fourth.text(
        0.04,
        0.96,
        "\n".join(lines),
        transform=fourth.transAxes,
        va="top",
        ha="left",
        fontsize=11,
        linespacing=1.5,
        bbox={
            "boxstyle": "round,pad=0.7",
            "facecolor": "#f7f5ef",
            "edgecolor": "#9a9587",
        },
    )
    fourth.set_title("Count closure", pad=6)

    figure.suptitle(
        "RH-34: certified Schur-similarity closure of the interior complement count",
        fontsize=12,
    )
    figure.tight_layout(rect=(0.0, 0.0, 1.0, 0.965))
    output = ROOT / "figures"
    output.mkdir(parents=True, exist_ok=True)
    figure.savefig(output / "schur_similarity_closure.pdf", bbox_inches="tight")
    figure.savefig(
        output / "schur_similarity_closure.png",
        dpi=220,
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
