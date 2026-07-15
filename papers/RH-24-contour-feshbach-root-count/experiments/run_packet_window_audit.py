"""Packet-window robustness for the contour-Feshbach root prediction."""

from __future__ import annotations

import argparse
import json
import platform
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

import run_contour_feshbach_audit as base
from contour_feshbach import (
    build_batched_arnoldi_feshbach,
    circle_contour_audit,
    determinant_newton_root,
)


SIGMAS = (1.0e-3, 1.0e-4)
WINDOWS = (5.0, 6.0, 7.0)
WINDOW_MODELS = base.RESULTS / "window_models"


def build_window_model(
    matrix,
    spectrum,
    sigma: float,
    dimension: int,
    period: int,
    window: float,
):
    trial = base.packet_trial(
        matrix,
        sigma,
        dimension,
        period,
        window_multiple=window,
    )
    pair = base.canonical_biorthogonal_pair(
        trial, spectrum["right_modes"], spectrum["left_modes"]
    )
    _, two_step = base.bulk_operator(matrix, spectrum)
    synthesis = np.asarray(pair.synthesis)
    analysis = np.asarray(pair.analysis)

    def external(values):
        array = np.asarray(values)
        return array - synthesis @ (analysis @ array)

    reduced = analysis @ two_step(synthesis)
    forcing = external(two_step(synthesis))
    depth = base.ARNOLDI_DEPTHS[sigma]
    counter = 0

    def observed_action(values):
        nonlocal counter
        counter += 1
        source = external(values)
        applied = two_step(source)
        if counter == 1 or counter % 10 == 0 or counter == depth:
            print(
                f"    window={window:g}, Arnoldi {counter}/{depth}",
                flush=True,
            )
        return external(applied), analysis @ applied

    model = build_batched_arnoldi_feshbach(
        observed_action,
        forcing,
        reduced,
        steps=depth,
        reorthogonalizations=2,
    )
    return model, pair


def analyze_window_model(
    model,
    sigma: float,
    window: float,
    reference_root: complex,
    gram_condition: float,
    build_seconds: float,
):
    center, direct_roots = base.select_direct_center(model.reduced)
    center_scale = abs(center)
    candidates = []
    for factor in base.RADIUS_FACTORS:
        audit = circle_contour_audit(
            model,
            center,
            factor * center_scale,
            nodes=base.SCAN_NODES,
        )
        if (
            audit.winding_integer == 1
            and audit.projected_pole_count == 0
            and audit.projected_zero_count == 1
            and audit.maximum_phase_increment < 0.85 * np.pi
        ):
            candidates.append((factor, audit))
    if not candidates:
        raise RuntimeError(f"no discovery contour for sigma={sigma:g}, window={window:g}")
    discovery_factor, discovery = max(
        candidates,
        key=lambda item: float(np.min(item[1].smallest_singular_values)),
    )
    root = determinant_newton_root(
        model,
        discovery.cauchy_centroid,
        trust_radius=discovery.radius,
    )
    if not root.converged:
        raise RuntimeError("window-model Newton solve failed")
    augmented_values = np.linalg.eigvals(model.augmented_matrix())
    poles = model.projected_poles()
    root_radius = abs(root.root - center)
    root_index = int(np.argmin(np.abs(augmented_values - root.root)))
    zero_radii = np.delete(np.abs(augmented_values - center), root_index)
    zero_radii = zero_radii[zero_radii > root_radius + 1.0e-9]
    pole_radii = np.abs(poles - center)
    pole_radii = pole_radii[pole_radii > root_radius + 1.0e-9]
    next_zero = float(np.min(zero_radii)) if zero_radii.size else float("inf")
    next_pole = float(np.min(pole_radii)) if pole_radii.size else float("inf")
    next_event = min(next_zero, next_pole)
    if not np.isfinite(next_event):
        next_event = discovery.radius
    radius = 0.5 * (root_radius + next_event)
    selected = circle_contour_audit(
        model,
        center,
        radius,
        nodes=base.FINAL_CONTOUR_NODES,
    )
    root = determinant_newton_root(
        model,
        selected.cauchy_centroid,
        trust_radius=radius,
    )
    if not root.converged:
        raise RuntimeError("optimized window-model Newton solve failed")
    return {
        "sigma": sigma,
        "window_multiple": window,
        "packet_rank": model.packet_rank,
        "packet_gram_condition": gram_condition,
        "arnoldi_depth": model.maximum_depth,
        "direct_lower_half_root_count": int(
            np.count_nonzero(direct_roots.imag < -1.0e-9)
        ),
        "direct_center_real": center.real,
        "direct_center_imag": center.imag,
        "discovery_radius_factor": discovery_factor,
        "selected_radius_factor": radius / center_scale,
        "winding_integer": selected.winding_integer,
        "projected_pole_count": selected.projected_pole_count,
        "projected_zero_count": selected.projected_zero_count,
        "predicted_root_real": root.root.real,
        "predicted_root_imag": root.root.imag,
        "direct_reference_error": abs(center - reference_root),
        "feshbach_reference_error": abs(root.root - reference_root),
        "root_radial_distance": root_radius,
        "isolation_corridor_width": next_event - root_radius,
        "maximum_relative_arnoldi_residual": float(
            np.max(selected.relative_residuals)
        ),
        "cauchy_count_error": abs(selected.cauchy_count - 1.0),
        "maximum_phase_increment": selected.maximum_phase_increment,
        "maximum_arnoldi_orthogonality_error": float(
            np.max(model.arnoldi_orthogonality_errors)
        ),
        "model_build_seconds": build_seconds,
    }


def plot_rows(rows: list[dict[str, object]]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.8))
    for sigma in SIGMAS:
        selected = sorted(
            [row for row in rows if float(row["sigma"]) == sigma],
            key=lambda row: float(row["window_multiple"]),
        )
        window = np.asarray([float(row["window_multiple"]) for row in selected])
        direct = np.asarray([float(row["direct_reference_error"]) for row in selected])
        prediction = np.asarray(
            [float(row["feshbach_reference_error"]) for row in selected]
        )
        corridor = np.asarray(
            [float(row["isolation_corridor_width"]) for row in selected]
        )
        radius = np.asarray([float(row["selected_radius_factor"]) for row in selected])
        residual = np.asarray(
            [float(row["maximum_relative_arnoldi_residual"]) for row in selected]
        )
        label = rf"$\sigma={sigma:.0e}$"
        axes[0, 0].semilogy(window, direct, "s--", label=f"direct, {label}")
        axes[0, 0].semilogy(window, prediction, "o-", label=f"Feshbach, {label}")
        axes[0, 1].plot(window, corridor, "o-", label=label)
        axes[1, 0].plot(window, radius, "o-", label=label)
        axes[1, 1].semilogy(window, residual, "o-", label=label)
    axes[0, 0].set(
        xlabel="packet half-width in local standard deviations",
        ylabel="error against frozen blind reference",
        title="The predicted root is packet-window stable",
    )
    axes[0, 1].set(
        xlabel="packet half-width in local standard deviations",
        ylabel="pole-free corridor width",
        title="The isolation corridor changes but remains open",
    )
    axes[1, 0].set(
        xlabel="packet half-width in local standard deviations",
        ylabel=r"selected radius / $|z_{\rm direct}|$",
        title="Contour renormalization absorbs packet changes",
    )
    axes[1, 1].set(
        xlabel="packet half-width in local standard deviations",
        ylabel="maximum residual bound",
        title="Shifted solves remain converged",
    )
    for axis in axes.flat:
        axis.grid(alpha=0.2, which="both")
        axis.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(base.FIGURES / "packet_window_root_stability.pdf")
    fig.savefig(base.FIGURES / "packet_window_root_stability.png", dpi=220)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse", action="store_true")
    arguments = parser.parse_args()
    WINDOW_MODELS.mkdir(parents=True, exist_ok=True)
    baseline_rows = base.read_csv(base.RESULTS / "scale_summary.csv")
    baseline = {float(row["sigma"]): row for row in baseline_rows}
    if arguments.reuse:
        rows = base.read_csv(base.RESULTS / "packet_window_stability.csv")
    else:
        settings = base.physical_settings()
        rows = []
        for sigma in SIGMAS:
            setting = settings[sigma]
            dimension = int(setting["dimension"])
            period = int(setting["period"])
            print(
                f"packet-window audit sigma={sigma:g}, n={dimension}",
                flush=True,
            )
            constants = base.critical_constants(130)
            matrix = base.sparse_folded_gaussian_matrix(
                dimension, sigma, u=float(constants.u)
            )
            spectrum = base.resolve_peripheral_modes(matrix)
            reference = complex(
                float(baseline[sigma]["reference_root_real"]),
                float(baseline[sigma]["reference_root_imag"]),
            )
            for window in WINDOWS:
                started = time.time()
                if window == base.WINDOW_MULTIPLE:
                    model = base.load_model(
                        base.MODELS / f"contour_model_sigma_{sigma:.0e}.npz"
                    )
                    trial = base.packet_trial(
                        matrix,
                        sigma,
                        dimension,
                        period,
                        window_multiple=window,
                    )
                    pair = base.canonical_biorthogonal_pair(
                        trial,
                        spectrum["right_modes"],
                        spectrum["left_modes"],
                    )
                else:
                    model, pair = build_window_model(
                        matrix,
                        spectrum,
                        sigma,
                        dimension,
                        period,
                        window,
                    )
                    base.save_model(
                        WINDOW_MODELS
                        / f"window_model_sigma_{sigma:.0e}_w{window:.0f}.npz",
                        model,
                    )
                build_seconds = time.time() - started
                rows.append(
                    analyze_window_model(
                        model,
                        sigma,
                        window,
                        reference,
                        float(np.linalg.cond(pair.gram)),
                        build_seconds,
                    )
                )
                base.write_csv(base.RESULTS / "packet_window_stability.csv", rows)
                del model, pair
                base.release_memory()
            del matrix, spectrum
            base.release_memory()
    plot_rows(rows)
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "sigmas": list(SIGMAS),
        "windows": list(WINDOWS),
        "all_windings": [int(float(row["winding_integer"])) for row in rows],
        "maximum_prediction_error": max(
            float(row["feshbach_reference_error"]) for row in rows
        ),
        "maximum_residual_bound": max(
            float(row["maximum_relative_arnoldi_residual"]) for row in rows
        ),
        "minimum_corridor_width": min(
            float(row["isolation_corridor_width"]) for row in rows
        ),
        "source_hashes": {
            "window_audit.py": base.source_hash(Path(__file__)),
            "contour_audit.py": base.source_hash(
                Path(base.__file__).resolve()
            ),
            "model.py": base.source_hash(
                base.ROOT / "src" / "contour_feshbach" / "model.py"
            ),
        },
    }
    with (base.RESULTS / "packet_window_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated packet-window root audit", flush=True)


if __name__ == "__main__":
    main()
