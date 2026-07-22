"""Make the RH-80 route figure from the archived audit."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "results" / "cloud_renormalization_audit.json"


def main() -> None:
    data = json.loads(AUDIT.read_text(encoding="utf-8"))
    ideal = data["ideal_model"]
    clouds = data["archived_cloud_rows"]
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 7.4))

    ax = axes[0, 0]
    for radius in (0.5, 0.8, 0.95):
        rows = [row for row in ideal["interior_rows"] if row["radius_ratio"] == radius]
        ax.semilogy([row["degree"] for row in rows], [row["uniform_error_upper"] for row in rows], marker="o", label=fr"$r={radius}$")
    ax.set_xlabel("cloud degree $N$")
    ax.set_ylabel("uniform cancellation error")
    ax.set_title("(a) Fixed factor works strictly inside")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    for point in (1.02, 1.05, 1.1):
        rows = [row for row in ideal["exterior_rows"] if row["point_ratio"] == point]
        ax.semilogy([row["degree"] for row in rows], [row["fixed_cancellation_magnitude_lower"] for row in rows], marker="o", label=fr"$q={point}$")
    ax.set_xlabel("cloud degree $N$")
    ax.set_ylabel(r"$|(1-q^{N+1})^2|$")
    ax.set_title("(b) Fixed factor blows up outside")
    ax.grid(alpha=0.25)
    ax.legend()

    ax = axes[1, 0]
    sigmas = [row["sigma"] for row in clouds]
    centers = [row["edge_center_upper"] for row in clouds]
    low = [row["zero_radius_min_lower"] for row in clouds]
    high = [row["zero_radius_max_upper"] for row in clouds]
    ax.fill_between(sigmas, low, high, alpha=0.25, label="observed zero-radius band")
    ax.plot(sigmas, centers, marker="o", label="radially centered cloud")
    ax.axhline(data["deterministic_double_pole"], color="black", linestyle="--", label=r"$\lambda$")
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel(r"two-step zero radius $|w|$")
    ax.set_title("(c) The spectral factor must move")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    means = [row["central_profile_mean_error_upper"] for row in clouds]
    maxima = [row["central_profile_max_error_upper"] for row in clouds]
    ax.plot(sigmas, means, marker="o", label=r"mean on $|s|\leq1$")
    ax.plot(sigmas, maxima, marker="s", label=r"maximum on $|s|\leq1$")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"noise $\sigma$")
    ax.set_ylabel("profile error")
    ax.set_title("(d) Recentered archived cloud audit")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)

    fig.tight_layout()
    output = ROOT / "figures" / "moving_cloud_relative_determinant"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output.with_suffix(".png"), dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()

