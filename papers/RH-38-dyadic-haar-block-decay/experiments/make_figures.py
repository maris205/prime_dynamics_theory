"""Render the analytic and stored-model quarter/half-law summary."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def coordinate_matrices(dimension: int):
    identity = np.eye(dimension)
    j = np.repeat(identity, 2, axis=0)
    k = np.empty_like(j)
    k[0::2] = identity
    k[1::2] = -identity
    return j, k, 0.5 * j.T, 0.5 * k.T


def smooth_kernel(x, y):
    return 1.0 + 0.2 * x + 0.1 * y + 0.05 * x * y + 0.04 * x * x + 0.03 * y * y


def ideal_matrix(dimension: int):
    h = 1.0 / dimension
    nodes = (np.arange(dimension) + 0.5) * h
    return h * smooth_kernel(nodes[:, None], nodes[None, :])


def demonstration_blocks(dimension: int):
    coarse = ideal_matrix(dimension)
    fine = ideal_matrix(2 * dimension)
    j, k, r, s = coordinate_matrices(dimension)
    return {
        "coarse_consistency": np.linalg.norm(r @ fine @ j - coarse, 2),
        "coarse_to_detail": np.linalg.norm(s @ fine @ j, 2),
        "detail_to_coarse": np.linalg.norm(r @ fine @ k, 2),
        "detail_block": np.linalg.norm(s @ fine @ k, 2),
    }


def main() -> None:
    pilot = load(ROOT / "results" / "component_scaling_pilot_sigma_1e-02.json")
    certificate = load(ROOT / "results" / "dyadic_haar_block_decay_certificate.json")
    blocks = (
        "coarse_consistency",
        "coarse_to_detail",
        "detail_to_coarse",
        "detail_block",
    )
    labels = [r"$E$", r"$C$", r"$B$", r"$D$"]
    components = (
        "markov",
        "peripheral",
        "bulk_one_step",
        "physical_two_step",
    )
    component_labels = [r"$P$", r"$Q$", r"$U=P-Q$", r"$A=U^2$"]
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red"]
    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "figure.dpi": 160,
        }
    )
    figure, axes = plt.subplots(2, 2, figsize=(10.2, 7.2), constrained_layout=True)

    axis = axes[0, 0]
    x = np.arange(len(blocks))
    width = 0.19
    first = pilot["levels"]["2048_to_4096"]["components"]
    for index, (component, label, color) in enumerate(
        zip(components, component_labels, colors)
    ):
        values = [first[component][block]["largest_singular_value"] for block in blocks]
        axis.bar(x + (index - 1.5) * width, values, width, label=label, color=color)
    axis.set_yscale("log")
    axis.set_xticks(x, labels)
    axis.set_ylabel("floating leading singular value")
    axis.set_title(r"(a) The law is present before and after extraction")
    axis.legend(frameon=False, ncol=2)

    axis = axes[0, 1]
    ratios = pilot["second_to_first_ratios"]
    for index, (component, label, color) in enumerate(
        zip(components, component_labels, colors)
    ):
        values = [ratios[component][block] for block in blocks]
        offset = (index - 1.5) * 0.035
        axis.plot(
            x + offset,
            values,
            marker="o",
            linewidth=1.0,
            label=label,
            color=color,
        )
    axis.axhline(0.25, color="black", linestyle="--", linewidth=0.8)
    axis.axhline(0.5, color="black", linestyle=":", linewidth=0.8)
    axis.set_xticks(x, labels)
    axis.set_ylim(0.23, 0.52)
    axis.set_ylabel("second refinement / first refinement")
    axis.set_title("(b) Floating component quarter/half ratios")
    axis.legend(frameon=False, ncol=2)

    axis = axes[1, 0]
    levels = certificate["rigorous_physical_levels"]
    first_scaled = levels["2048_to_4096"]["renormalized_uppers"]
    second_scaled = levels["4096_to_8192"]["renormalized_uppers"]
    axis.bar(x - 0.18, [first_scaled[b] for b in blocks], 0.36, label=r"$2048\to4096$")
    axis.bar(x + 0.18, [second_scaled[b] for b in blocks], 0.36, label=r"$4096\to8192$")
    axis.set_yscale("log")
    axis.set_xticks(x, labels)
    axis.set_ylabel(r"rigorous upper after dividing by $h^p$")
    axis.set_title("(c) Renormalized physical uppers are stable")
    axis.legend(frameon=False)

    axis = axes[1, 1]
    dimensions = np.asarray([16, 32, 64, 128, 256])
    h = 1.0 / dimensions
    demos = [demonstration_blocks(int(n)) for n in dimensions]
    for block, label, color in zip(blocks, labels, colors):
        values = np.asarray([row[block] for row in demos])
        axis.loglog(h, values, marker="o", linewidth=1.1, label=label, color=color)
    reference_h = np.asarray([h[-1], h[0]])
    axis.loglog(reference_h, 0.08 * reference_h, color="gray", linestyle=":", label=r"$h$")
    axis.loglog(reference_h, 0.08 * reference_h**2, color="black", linestyle="--", label=r"$h^2$")
    axis.set_xlabel("coarse mesh $h$")
    axis.set_ylabel("exact dense test-kernel block norm")
    axis.set_title("(d) Haar cancellation gives first/second order")
    axis.legend(frameon=False, ncol=2)

    output_dir = ROOT / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "dyadic_haar_block_decay.png", dpi=220)
    figure.savefig(output_dir / "dyadic_haar_block_decay.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
