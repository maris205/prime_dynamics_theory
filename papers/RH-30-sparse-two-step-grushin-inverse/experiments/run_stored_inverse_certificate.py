"""Outward stored-factor certificate for the lifted physical inverse.

The sparse bordered solve is used only to generate a binary64 approximate
right inverse.  The final theorem is obtained independently by applying the
exact stored-factor graph with componentwise outward radii and a
Frobenius--Neumann argument.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
import flint
from flint import arb, ctx
from scipy.sparse.linalg import splu


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH27 = PAPERS / "RH-27-outward-rounded-primal-dual-residuals"
RH29 = PAPERS / "RH-29-deflated-complement-resolvent"
sys.path[:0] = [
    str(ROOT / "src"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
    str(RH27 / "src"),
    str(RH29 / "src"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402
from deflated_resolvent import lifted_full_inverse_upper  # noqa: E402
from outward_residuals import (  # noqa: E402
    ComponentwiseBall,
    ComponentwiseStoredFactorGraph,
    componentwise_add,
    componentwise_dense_exact_matmul,
    componentwise_scalar_multiply,
    componentwise_subtract,
    frobenius_upper_array,
    magnitude_upper,
)
from sparse_grushin import (  # noqa: E402
    build_sparse_grushin_system,
    combine_frobenius_bounds,
    neumann_inverse_certificate,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def selected_row(sigma: float) -> dict[str, str]:
    rows = read_csv(RH29 / "results" / "deflated_scale_summary.csv")
    return min(rows, key=lambda row: abs(float(row["sigma"]) - float(sigma)))


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _arb_exact_norm(values: np.ndarray) -> arb:
    total = arb(0)
    for value in np.asarray(values).reshape(-1):
        if np.iscomplexobj(values):
            real = arb(float(np.real(value)))
            imag = arb(float(np.imag(value)))
            total += real * real + imag * imag
        else:
            scalar = arb(float(value))
            total += scalar * scalar
    return total.sqrt()


def normalized_lift_coefficient_interval(
    singular_value: float,
    left: np.ndarray,
    right: np.ndarray,
    *,
    lift: float,
    precision: int = 160,
) -> tuple[float, float]:
    previous = ctx.prec
    ctx.prec = int(precision)
    try:
        coefficient = (arb(float(lift)) - arb(float(singular_value))) / (
            _arb_exact_norm(left) * _arb_exact_norm(right)
        )
        lower = float(np.nextafter(float(coefficient.lower()), -np.inf))
        upper = float(np.nextafter(float(coefficient.upper()), np.inf))
    finally:
        ctx.prec = previous
    if not (0.0 < lower <= upper):
        raise ValueError("normalized lift coefficient must be positive")
    return lower, upper


def interval_scalar_multiply(
    lower: float,
    upper: float,
    ball: ComponentwiseBall,
) -> ComponentwiseBall:
    """Multiply a componentwise ball by an exact real scalar interval."""

    midpoint = float(0.5 * (float(lower) + float(upper)))
    half_width = float(
        np.nextafter(
            max(midpoint - float(lower), float(upper) - midpoint), np.inf
        )
    )
    central = componentwise_scalar_multiply(midpoint, ball)
    magnitude = np.nextafter(
        magnitude_upper(ball.center) + np.asarray(ball.radius), np.inf
    )
    uncertainty_radius = np.nextafter(half_width * magnitude, np.inf)
    uncertainty = ComponentwiseBall(
        np.zeros_like(ball.center), uncertainty_radius
    )
    return componentwise_add(central, uncertainty)


def lifted_shift_action(
    graph: ComponentwiseStoredFactorGraph,
    source: ComponentwiseBall,
    spectral_parameter: complex,
    dangerous_left: np.ndarray,
    dangerous_right: np.ndarray,
    coefficient_interval: tuple[float, float],
) -> ComponentwiseBall:
    shifted = componentwise_subtract(
        componentwise_scalar_multiply(spectral_parameter, source),
        graph.action(source),
    )
    coefficient = componentwise_dense_exact_matmul(
        np.asarray(dangerous_right).conj()[None, :], source
    )
    outer = componentwise_dense_exact_matmul(
        np.asarray(dangerous_left)[:, None], coefficient
    )
    lifted = interval_scalar_multiply(*coefficient_interval, outer)
    return componentwise_add(shifted, lifted)


def upward_square_sum(values: list[float]) -> float:
    return combine_frobenius_bounds(values)


def arc_inverse_upper(center_inverse_upper: float, radius_upper: float) -> float:
    inverse = float(center_inverse_upper)
    radius = float(radius_upper)
    product = float(np.nextafter(inverse * radius, np.inf))
    if product >= 1.0:
        return float("inf")
    denominator = float(np.nextafter(1.0 - product, 0.0))
    return float(np.nextafter(inverse / denominator, np.inf))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--lift", type=float, default=1.0)
    parser.add_argument("--auxiliary-scale", type=float, default=1.0)
    parser.add_argument("--chunk-size", type=int, default=128)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--print-json", action="store_true")
    arguments = parser.parse_args()

    sigma = float(arguments.sigma)
    row = selected_row(sigma)
    if abs(float(row["sigma"]) - sigma) > 1.0e-14:
        raise ValueError(f"sigma={sigma:g} is not an archived RH-29 scale")
    setting = rh24.physical_settings()[sigma]
    point = complex(
        float(row["spectral_parameter_real"]),
        float(row["spectral_parameter_imag"]),
    )
    triplet_path = RH29 / row["triplet_file"]

    begun = time.time()
    environment = rh25_global.build_environment(sigma, setting)
    spectrum = environment["spectrum"]
    with np.load(triplet_path) as archive:
        singular_value = float(archive["singular_value"][0])
        dangerous_left = np.asarray(archive["left"])
        dangerous_right = np.asarray(archive["right"])
    coefficient_interval = normalized_lift_coefficient_interval(
        singular_value,
        dangerous_left,
        dangerous_right,
        lift=float(arguments.lift),
    )
    graph = ComponentwiseStoredFactorGraph(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
    )
    system = build_sparse_grushin_system(
        environment["matrix"],
        spectrum["right_modes"],
        spectrum["left_modes"],
        spectrum["peripheral_values"],
        environment["synthesis"],
        environment["analysis"],
        dangerous_left,
        dangerous_right,
        singular_value,
        point,
        lift=float(arguments.lift),
        auxiliary_scale=float(arguments.auxiliary_scale),
    )
    factor_started = time.time()
    factor = splu(
        system.matrix,
        permc_spec="COLAMD",
        diag_pivot_thresh=1.0,
        options={"Equil": False, "IterRefine": "DOUBLE"},
    )
    factor_seconds = time.time() - factor_started

    dimension = int(system.physical_dimension)
    total_dimension = int(system.bordered_dimension)
    chunk_size = int(arguments.chunk_size)
    inverse_chunk_bounds: list[float] = []
    residual_chunk_bounds: list[float] = []
    residual_center_chunk_bounds: list[float] = []
    residual_radius_chunk_bounds: list[float] = []
    chunk_rows: list[dict[str, object]] = []
    inverse_hash = hashlib.sha256()
    residual_center_hash = hashlib.sha256()
    residual_radius_hash = hashlib.sha256()
    solve_started = time.time()
    for start in range(0, dimension, chunk_size):
        stop = min(start + chunk_size, dimension)
        width = stop - start
        source = np.zeros((total_dimension, width), dtype=np.complex128)
        source[np.arange(start, stop), np.arange(width)] = 1.0
        solution = factor.solve(source)
        approximate = np.ascontiguousarray(solution[:dimension, :])
        inverse_hash.update(approximate.view(np.uint8))
        approximate_upper = frobenius_upper_array(approximate)

        target = lifted_shift_action(
            graph,
            ComponentwiseBall.exact(approximate),
            point,
            dangerous_left,
            dangerous_right,
            coefficient_interval,
        )
        identity = np.zeros((dimension, width), dtype=np.complex128)
        identity[np.arange(start, stop), np.arange(width)] = 1.0
        residual = componentwise_subtract(
            ComponentwiseBall.exact(identity), target
        )
        residual_center = np.ascontiguousarray(residual.center)
        residual_radius = np.ascontiguousarray(residual.radius)
        residual_center_hash.update(residual_center.view(np.uint8))
        residual_radius_hash.update(residual_radius.view(np.uint8))
        center_upper = frobenius_upper_array(residual_center)
        radius_upper = frobenius_upper_array(residual_radius)
        residual_upper = residual.norm_upper

        inverse_chunk_bounds.append(approximate_upper)
        residual_chunk_bounds.append(residual_upper)
        residual_center_chunk_bounds.append(center_upper)
        residual_radius_chunk_bounds.append(radius_upper)
        chunk_rows.append(
            {
                "first_column": start,
                "last_column_exclusive": stop,
                "approximate_inverse_frobenius_upper": approximate_upper,
                "residual_center_frobenius_upper": center_upper,
                "residual_radius_frobenius_upper": radius_upper,
                "residual_frobenius_upper": residual_upper,
            }
        )
        print(
            f"  certified columns {stop}/{dimension}: "
            f"R_F={approximate_upper:.3e}, E_F={residual_upper:.3e}",
            flush=True,
        )

    inverse_upper = upward_square_sum(inverse_chunk_bounds)
    residual_upper = upward_square_sum(residual_chunk_bounds)
    residual_center_upper = upward_square_sum(residual_center_chunk_bounds)
    residual_radius_upper = upward_square_sum(residual_radius_chunk_bounds)
    certificate = neumann_inverse_certificate(inverse_upper, residual_upper)
    budget = float(row["lifted_inverse_budget_lower"])
    closes_budget = bool(
        certificate.admissible and certificate.inverse_two_norm_upper < budget
    )
    original = lifted_full_inverse_upper(
        certificate.inverse_two_norm_upper,
        singular_value,
        float(row["normalized_right_residual_norm_upper"]),
        float(row["normalized_left_residual_norm_upper"]),
        lift=float(arguments.lift),
    )
    selected_arc_upper = arc_inverse_upper(
        original.full_inverse_upper, float(row["arc_disc_radius"])
    )
    closes_selected_arc = bool(
        closes_budget
        and original.admissible
        and selected_arc_upper < float(row["rh28_arc_resolvent_budget_lower"])
    )
    payload = {
        "status": (
            "rigorous_selected_arc_stored_model_closure"
            if closes_selected_arc
            else "stored_model_certificate_does_not_close_budget"
        ),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "sigma": sigma,
        "physical_dimension": dimension,
        "bordered_dimension": total_dimension,
        "border_rank": int(system.update.rank),
        "matrix_nnz": int(system.matrix.nnz),
        "factor_nnz": int(factor.L.nnz + factor.U.nnz),
        "factor_fill_ratio": float(
            (factor.L.nnz + factor.U.nnz) / system.matrix.nnz
        ),
        "factor_seconds": factor_seconds,
        "certificate_seconds": time.time() - solve_started,
        "total_seconds": time.time() - begun,
        "chunk_size": chunk_size,
        "spectral_parameter_real": point.real,
        "spectral_parameter_imag": point.imag,
        "stored_singular_value": singular_value,
        "lift": float(arguments.lift),
        "normalized_lift_coefficient_lower": coefficient_interval[0],
        "normalized_lift_coefficient_upper": coefficient_interval[1],
        "approximate_inverse_frobenius_upper": inverse_upper,
        "residual_center_frobenius_upper": residual_center_upper,
        "residual_radius_frobenius_upper": residual_radius_upper,
        "residual_frobenius_upper": residual_upper,
        "lifted_inverse_two_norm_upper": certificate.inverse_two_norm_upper,
        "lifted_inverse_budget_lower": budget,
        "certified_budget_margin": (
            float(budget / certificate.inverse_two_norm_upper)
            if np.isfinite(certificate.inverse_two_norm_upper)
            else 0.0
        ),
        "rh29_floating_lifted_inverse_candidate": float(
            row["lifted_bulk_inverse_candidate"]
        ),
        "normalized_right_residual_norm_upper": float(
            row["normalized_right_residual_norm_upper"]
        ),
        "normalized_left_residual_norm_upper": float(
            row["normalized_left_residual_norm_upper"]
        ),
        "original_center_inverse_two_norm_upper": original.full_inverse_upper,
        "original_lift_formula_denominator_lower": original.denominator_lower,
        "arc_disc_radius_upper": float(row["arc_disc_radius"]),
        "selected_arc_inverse_two_norm_upper": selected_arc_upper,
        "rh28_selected_arc_resolvent_budget_lower": float(
            row["rh28_arc_resolvent_budget_lower"]
        ),
        "selected_arc_budget_margin": float(
            float(row["rh28_arc_resolvent_budget_lower"]) / selected_arc_upper
        ),
        "inverse_sha256": inverse_hash.hexdigest(),
        "residual_center_sha256": residual_center_hash.hexdigest(),
        "residual_radius_sha256": residual_radius_hash.hexdigest(),
        "triplet_sha256": source_hash(triplet_path),
        "source_sha256": {
            "run_stored_inverse_certificate.py": source_hash(
                ROOT / "experiments" / "run_stored_inverse_certificate.py"
            ),
            "linearization.py": source_hash(
                ROOT / "src" / "sparse_grushin" / "linearization.py"
            ),
            "certification.py": source_hash(
                ROOT / "src" / "sparse_grushin" / "certification.py"
            ),
            "componentwise_graph.py": source_hash(
                RH27 / "src" / "outward_residuals" / "componentwise_graph.py"
            ),
            "componentwise.py": source_hash(
                RH27 / "src" / "outward_residuals" / "componentwise.py"
            ),
            "enclosures.py": source_hash(
                RH27 / "src" / "outward_residuals" / "enclosures.py"
            ),
            "rh29_algebra.py": source_hash(
                RH29 / "src" / "deflated_resolvent" / "algebra.py"
            ),
            "rh29_scale_summary.csv": source_hash(
                RH29 / "results" / "deflated_scale_summary.csv"
            ),
        },
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "python_flint": flint.__version__,
        },
        "chunks": chunk_rows,
        "assumptions": [
            "stored binary64 factors are exact inputs",
            "IEEE round-to-nearest with no overflow or harmful underflow",
            "the archived triplet hash matches RH-29",
        ],
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if arguments.print_json:
        print(rendered, flush=True)
    else:
        print(
            "certificate status={}, lifted_upper={:.8e}, residual={:.3e}, "
            "lifted_margin={:.2f}, arc_upper={:.8e}".format(
                payload["status"],
                payload["lifted_inverse_two_norm_upper"],
                payload["residual_frobenius_upper"],
                payload["certified_budget_margin"],
                payload["selected_arc_inverse_two_norm_upper"],
            ),
            flush=True,
        )
    output = arguments.output
    if output is None:
        output = RESULTS / f"stored_inverse_certificate_sigma_{sigma:.0e}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
