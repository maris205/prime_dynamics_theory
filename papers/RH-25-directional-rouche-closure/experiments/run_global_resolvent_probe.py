"""Global-resolvent stress test and direct full-Feshbach cross-check.

The singular values produced here are floating-point candidates, not
validated lower bounds.  The fixed-budget small-noise probes diagnose the
scalability of one certification route; nonconvergence is not spectral
evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.sparse.linalg import ArpackNoConvergence, LinearOperator, gmres, svds


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
sys.path[:0] = [
    str(ROOT / "src"),
    str(ROOT / "experiments"),
    str(RH24 / "src"),
    str(RH24 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_directional_closure_audit as directional  # noqa: E402
from directional_rouche import (  # noqa: E402
    circular_lipschitz_lower_bound,
    determinant_winding,
    fom_external_solution,
    global_scalar_majorant,
    matrix_rouche_ratio,
)


GLOBAL_SIGMA = 1.0e-2
BARRIER_SIGMA = 1.0e-3
GLOBAL_NODES = 32
DIRECT_NODES = 64
GLOBAL_TOLERANCE = 1.0e-10
GLOBAL_MAXIMUM_ITERATIONS = 6000
GLOBAL_NCV = 40
BARRIER_NODES = 4
BARRIER_MAXIMUM_ITERATIONS = 120
BARRIER_NCV = 24
BARRIER_WALL_SECONDS = 20.0
DIRECT_ATOL_FACTOR = 2.0e-12


class WallTimeBudgetExpired(RuntimeError):
    """Raised when one deliberately bounded stress probe exhausts its budget."""


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_row(sigma: float) -> dict[str, str]:
    rows = directional.baseline_rows()
    return rows[float(sigma)]


def deterministic_start(dimension: int, phase: float = 0.0) -> np.ndarray:
    index = np.arange(int(dimension), dtype=np.float64)
    vector = np.sin(np.sqrt(2.0) * (index + 0.5) + phase)
    vector += 0.31 * np.cos(np.sqrt(5.0) * (index + 0.5) - phase)
    return np.asarray(vector / np.linalg.norm(vector), dtype=np.complex128)


def build_environment(sigma: float, setting: dict[str, int]) -> dict[str, object]:
    """Build the physical packet/complement operator without Arnoldi."""

    dimension = int(setting["dimension"])
    period = int(setting["period"])
    constants = rh24.critical_constants(130)
    matrix = rh24.sparse_folded_gaussian_matrix(
        dimension,
        float(sigma),
        u=float(constants.u),
    )
    spectrum = rh24.resolve_peripheral_modes(matrix)
    trial = rh24.packet_trial(matrix, float(sigma), dimension, period)
    pair = rh24.canonical_biorthogonal_pair(
        trial,
        spectrum["right_modes"],
        spectrum["left_modes"],
    )
    synthesis = np.asarray(pair.synthesis)
    analysis = np.asarray(pair.analysis)
    _, two_step = rh24.bulk_operator(matrix, spectrum)

    def packet(values):
        array = np.asarray(values)
        return synthesis @ (analysis @ array)

    def external(values):
        array = np.asarray(values)
        return array - packet(array)

    def external_action(values):
        return external(two_step(external(values)))

    def observation(values):
        return analysis @ two_step(external(values))

    return {
        "matrix": matrix,
        "spectrum": spectrum,
        "synthesis": synthesis,
        "analysis": analysis,
        "forcing": external(two_step(synthesis)),
        "reduced": analysis @ two_step(synthesis),
        "external_action": external_action,
        "observation": observation,
    }


def add_adjoint_actions(environment: dict[str, object]) -> dict[str, object]:
    """Attach exact Euclidean adjoints of B and E to an environment."""

    matrix = environment["matrix"]
    spectrum = environment["spectrum"]
    synthesis = np.asarray(environment["synthesis"])
    analysis = np.asarray(environment["analysis"])
    right = np.asarray(spectrum["right_modes"])
    left = np.asarray(spectrum["left_modes"])
    values = np.asarray(spectrum["peripheral_values"])

    def external_adjoint(source):
        array = np.asarray(source)
        return array - analysis.conj().T @ (synthesis.conj().T @ array)

    def one_step_adjoint(source):
        array = np.asarray(source)
        coefficients = right.conj().T @ array
        if array.ndim == 1:
            correction = left.conj() @ (values.conj() * coefficients)
        else:
            correction = left.conj() @ (values.conj()[:, None] * coefficients)
        return matrix.conj().T @ array - correction

    def two_step_adjoint(source):
        return one_step_adjoint(one_step_adjoint(source))

    def external_action_adjoint(source):
        return external_adjoint(two_step_adjoint(external_adjoint(source)))

    def observation_adjoint(source):
        array = np.asarray(source)
        return external_adjoint(two_step_adjoint(analysis.conj().T @ array))

    environment["external_action_adjoint"] = external_action_adjoint
    environment["observation_adjoint"] = observation_adjoint
    rank = analysis.shape[0]
    environment["observation_matrix"] = observation_adjoint(
        np.eye(rank, dtype=np.complex128)
    ).conj().T
    return environment


def shifted_operator(environment: dict[str, object], zeta: complex) -> LinearOperator:
    dimension = environment["matrix"].shape[0]
    action = environment["external_action"]
    adjoint = environment["external_action_adjoint"]
    point = complex(zeta)
    return LinearOperator(
        (dimension, dimension),
        matvec=lambda vector: point * vector - action(vector),
        matmat=lambda values: point * values - action(values),
        rmatvec=lambda vector: np.conj(point) * vector - adjoint(vector),
        rmatmat=lambda values: np.conj(point) * values - adjoint(values),
        dtype=np.complex128,
    )


def adjoint_defect(environment: dict[str, object]) -> float:
    dimension = environment["matrix"].shape[0]
    first = deterministic_start(dimension, 0.17)
    second = deterministic_start(dimension, 0.73) * np.exp(
        1.0j * np.arange(dimension) / max(dimension, 1)
    )
    action = environment["external_action"]
    adjoint = environment["external_action_adjoint"]
    left = np.vdot(action(first), second)
    right = np.vdot(first, adjoint(second))
    return float(abs(left - right) / max(abs(left), abs(right), 1.0))


def smallest_singular_candidate(
    operator: LinearOperator,
    start: np.ndarray,
    *,
    tolerance: float,
    maximum_iterations: int,
    ncv: int,
) -> dict[str, object]:
    begun = time.time()
    try:
        left, singular, right_h = svds(
            operator,
            k=1,
            ncv=min(int(ncv), operator.shape[0] - 1),
            tol=float(tolerance),
            which="SM",
            v0=np.asarray(start),
            maxiter=int(maximum_iterations),
            return_singular_vectors=True,
            solver="arpack",
        )
    except ArpackNoConvergence as error:
        return {
            "status": "not_converged",
            "seconds": time.time() - begun,
            "message": str(error).replace("\n", " "),
        }
    except Exception as error:  # keep a stress audit reproducible across SciPy builds
        return {
            "status": f"error:{type(error).__name__}",
            "seconds": time.time() - begun,
            "message": str(error).replace("\n", " "),
        }
    index = int(np.argmin(singular))
    value = float(singular[index])
    u = np.asarray(left[:, index])
    v = np.asarray(right_h.conj().T[:, index])
    first_residual = np.linalg.norm(operator @ v - value * u)
    second_residual = np.linalg.norm(operator.H @ u - value * v)
    return {
        "status": "converged",
        "seconds": time.time() - begun,
        "smallest_singular_candidate": value,
        "resolvent_norm_candidate": 1.0 / value,
        "singular_triplet_residual": float(max(first_residual, second_residual)),
        "right_vector": v,
        "message": "",
    }


def contour_geometry(sigma: float, nodes: int) -> tuple[complex, float, np.ndarray, np.ndarray]:
    baseline = baseline_row(sigma)
    center = complex(
        float(baseline["direct_center_real"]),
        float(baseline["direct_center_imag"]),
    )
    radius = float(baseline["selected_contour_radius"])
    angles = 2.0 * np.pi * np.arange(int(nodes)) / int(nodes)
    points = center + radius * np.exp(1.0j * angles)
    return center, radius, angles, points


def run_global_nodes(data: dict[str, object], nodes: int) -> tuple[list[dict[str, object]], dict[str, object]]:
    sigma = GLOBAL_SIGMA
    environment = add_adjoint_actions(
        {
            "matrix": data["matrix"],
            "spectrum": data["spectrum"],
            "synthesis": np.asarray(data["pair"].synthesis),
            "analysis": np.asarray(data["pair"].analysis),
            "forcing": data["forcing"],
            "reduced": data["reduced"],
            "external_action": data["external_action"],
            "observation": data["observation"],
        }
    )
    model = data["model"]
    depth = int(data["base_depth"])
    _, radius, angles, points = contour_geometry(sigma, nodes)
    observation_norm = float(np.linalg.norm(environment["observation_matrix"], 2))
    start = deterministic_start(environment["matrix"].shape[0], 0.29)
    rows: list[dict[str, object]] = []
    for index, (theta, zeta) in enumerate(zip(angles, points)):
        operator = shifted_operator(environment, zeta)
        candidate = smallest_singular_candidate(
            operator,
            start,
            tolerance=GLOBAL_TOLERANCE,
            maximum_iterations=GLOBAL_MAXIMUM_ITERATIONS,
            ncv=GLOBAL_NCV,
        )
        if candidate["status"] != "converged":
            raise RuntimeError(
                f"global probe failed at node {index}: {candidate['message']}"
            )
        start = np.asarray(candidate.pop("right_vector"))
        evaluation = model.evaluate(zeta, depth=depth)
        solution = fom_external_solution(model, zeta, depth=depth)
        residual, _ = directional.relative_external_residual(
            environment["external_action"],
            environment["forcing"],
            solution,
            zeta,
        )
        inverse_feshbach_norm = float(
            np.linalg.norm(np.linalg.inv(evaluation.feshbach), 2)
        )
        residual_norm = float(np.linalg.norm(residual, 2))
        majorant = global_scalar_majorant(
            inverse_feshbach_norm,
            observation_norm,
            float(candidate["resolvent_norm_candidate"]),
            residual_norm,
        )
        rows.append(
            {
                "sigma": sigma,
                "node": index,
                "theta": theta,
                "z_real": zeta.real,
                "z_imag": zeta.imag,
                "svds_status": candidate["status"],
                "smallest_singular_candidate": candidate[
                    "smallest_singular_candidate"
                ],
                "resolvent_norm_candidate": candidate["resolvent_norm_candidate"],
                "singular_triplet_residual": candidate[
                    "singular_triplet_residual"
                ],
                "svds_seconds": candidate["seconds"],
                "inverse_feshbach_norm": inverse_feshbach_norm,
                "observation_norm": observation_norm,
                "arnoldi_residual_matrix_norm": residual_norm,
                "global_scalar_rouche_candidate": majorant,
            }
        )
        print(
            f"  global node {index + 1}/{nodes}: "
            f"s_min={candidate['smallest_singular_candidate']:.4e}, "
            f"M={majorant:.4e}",
            flush=True,
        )
    sampled = np.asarray(
        [float(row["smallest_singular_candidate"]) for row in rows]
    )
    summary = {
        "sigma": sigma,
        "global_nodes": nodes,
        "minimum_sampled_singular_candidate": float(np.min(sampled)),
        "maximum_sampled_resolvent_candidate": max(
            float(row["resolvent_norm_candidate"]) for row in rows
        ),
        "maximum_singular_triplet_residual": max(
            float(row["singular_triplet_residual"]) for row in rows
        ),
        "maximum_global_scalar_rouche_candidate": max(
            float(row["global_scalar_rouche_candidate"]) for row in rows
        ),
        "sampled_lipschitz_circle_lower_candidate": circular_lipschitz_lower_bound(
            sampled, radius
        ),
        "observation_norm": observation_norm,
        "external_adjoint_defect": adjoint_defect(environment),
    }
    return rows, summary


def direct_full_feshbach(
    data: dict[str, object], nodes: int
) -> tuple[list[dict[str, object]], dict[str, object]]:
    sigma = GLOBAL_SIGMA
    model = data["model"]
    depth = int(data["base_depth"])
    _, _, angles, points = contour_geometry(sigma, nodes)
    forcing = np.asarray(data["forcing"])
    rank = forcing.shape[1]
    rows: list[dict[str, object]] = []
    phases = []
    for index, (theta, zeta) in enumerate(zip(angles, points)):
        operator = LinearOperator(
            (forcing.shape[0], forcing.shape[0]),
            matvec=lambda vector, point=zeta: point * vector
            - data["external_action"](vector),
            dtype=np.complex128,
        )
        solution = np.zeros_like(forcing, dtype=np.complex128)
        total_iterations = 0
        maximum_iterations = 0
        converged = True
        for column in range(rank):
            history: list[float] = []
            source_norm = np.linalg.norm(forcing[:, column])
            vector, info = gmres(
                operator,
                forcing[:, column],
                rtol=0.0,
                atol=DIRECT_ATOL_FACTOR * source_norm,
                restart=100,
                maxiter=30,
                callback=lambda value: history.append(float(value)),
                callback_type="pr_norm",
            )
            solution[:, column] = vector
            total_iterations += len(history)
            maximum_iterations = max(maximum_iterations, len(history))
            converged = converged and int(info) == 0
        residual = forcing - (zeta * solution - data["external_action"](solution))
        exact_feshbach = (
            zeta * np.eye(rank)
            - data["reduced"]
            - data["observation"](solution)
        )
        approximate = model.evaluate(zeta, depth=depth).feshbach
        perturbation = exact_feshbach - approximate
        sign, _ = np.linalg.slogdet(exact_feshbach)
        phases.append(float(np.angle(sign)))
        rows.append(
            {
                "sigma": sigma,
                "node": index,
                "theta": theta,
                "z_real": zeta.real,
                "z_imag": zeta.imag,
                "all_gmres_solves_converged": int(converged),
                "total_gmres_iterations": total_iterations,
                "maximum_column_gmres_iterations": maximum_iterations,
                "true_residual_to_forcing": float(
                    np.linalg.norm(residual) / np.linalg.norm(forcing)
                ),
                "full_minus_arnoldi_norm": float(np.linalg.norm(perturbation, 2)),
                "directional_rouche_ratio": matrix_rouche_ratio(
                    approximate, perturbation
                ),
                "full_feshbach_smallest_singular": float(
                    np.linalg.svd(exact_feshbach, compute_uv=False)[-1]
                ),
                "determinant_phase": phases[-1],
            }
        )
        if index % 8 == 0:
            print(
                f"  direct node {index + 1}/{nodes}: "
                f"eta={rows[-1]['directional_rouche_ratio']:.4e}",
                flush=True,
            )
    winding = determinant_winding(np.asarray(phases))
    summary = {
        "direct_nodes": nodes,
        "direct_full_winding_float": winding[0],
        "direct_full_winding_integer": winding[1],
        "direct_maximum_phase_increment": winding[2],
        "maximum_direct_directional_rouche_ratio": max(
            float(row["directional_rouche_ratio"]) for row in rows
        ),
        "maximum_full_minus_arnoldi_norm": max(
            float(row["full_minus_arnoldi_norm"]) for row in rows
        ),
        "maximum_direct_true_residual_to_forcing": max(
            float(row["true_residual_to_forcing"]) for row in rows
        ),
        "minimum_full_feshbach_singular": min(
            float(row["full_feshbach_smallest_singular"]) for row in rows
        ),
        "minimum_total_gmres_iterations": min(
            int(row["total_gmres_iterations"]) for row in rows
        ),
        "maximum_total_gmres_iterations": max(
            int(row["total_gmres_iterations"]) for row in rows
        ),
        "all_direct_solves_converged": int(
            all(int(row["all_gmres_solves_converged"]) == 1 for row in rows)
        ),
    }
    return rows, summary


def run_fixed_budget_barrier(
    nodes: int, maximum_iterations: int, wall_seconds: float
) -> list[dict[str, object]]:
    settings = rh24.physical_settings()
    sigma = BARRIER_SIGMA
    print(f"fixed-budget global probe sigma={sigma:g}", flush=True)
    environment = add_adjoint_actions(build_environment(sigma, settings[sigma]))
    _, _, angles, points = contour_geometry(sigma, 4 * int(nodes))
    selected = np.arange(int(nodes)) * 4
    start = deterministic_start(environment["matrix"].shape[0], 0.41)
    rows: list[dict[str, object]] = []
    for probe, index in enumerate(selected):
        def expire_budget(_signum, _frame):
            raise WallTimeBudgetExpired(
                f"wall-clock budget of {float(wall_seconds):g} seconds exhausted"
            )

        previous_handler = signal.signal(signal.SIGALRM, expire_budget)
        signal.setitimer(signal.ITIMER_REAL, float(wall_seconds))
        try:
            candidate = smallest_singular_candidate(
                shifted_operator(environment, points[index]),
                start,
                tolerance=GLOBAL_TOLERANCE,
                maximum_iterations=maximum_iterations,
                ncv=BARRIER_NCV,
            )
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0.0)
            signal.signal(signal.SIGALRM, previous_handler)
        if candidate["status"] == "error:WallTimeBudgetExpired":
            candidate["status"] = "wall_time_budget_exhausted"
        vector = candidate.pop("right_vector", None)
        if vector is not None:
            start = np.asarray(vector)
        rows.append(
            {
                "sigma": sigma,
                "probe": probe,
                "contour_node": int(index),
                "theta": angles[index],
                "z_real": points[index].real,
                "z_imag": points[index].imag,
                "dimension": environment["matrix"].shape[0],
                "maximum_iterations": maximum_iterations,
                "ncv": BARRIER_NCV,
                "wall_time_budget_seconds": wall_seconds,
                "status": candidate["status"],
                "seconds": candidate["seconds"],
                "smallest_singular_candidate": candidate.get(
                    "smallest_singular_candidate", ""
                ),
                "singular_triplet_residual": candidate.get(
                    "singular_triplet_residual", ""
                ),
                "message": candidate["message"],
            }
        )
        print(
            f"  barrier probe {probe + 1}/{nodes}: {candidate['status']} "
            f"in {candidate['seconds']:.2f}s",
            flush=True,
        )
    del environment
    rh24.release_memory()
    return rows


def plot_results(
    global_rows: list[dict[str, str]], direct_rows: list[dict[str, str]]
) -> None:
    theta = np.asarray([float(row["theta"]) for row in global_rows])
    singular = np.asarray(
        [float(row["smallest_singular_candidate"]) for row in global_rows]
    )
    resolvent = np.asarray(
        [float(row["resolvent_norm_candidate"]) for row in global_rows]
    )
    majorant = np.asarray(
        [float(row["global_scalar_rouche_candidate"]) for row in global_rows]
    )
    direct_theta = np.asarray([float(row["theta"]) for row in direct_rows])
    direct_ratio = np.asarray(
        [float(row["directional_rouche_ratio"]) for row in direct_rows]
    )
    direct_residual = np.asarray(
        [float(row["true_residual_to_forcing"]) for row in direct_rows]
    )

    fig, axes = plt.subplots(1, 3, figsize=(12.2, 3.7))
    axes[0].semilogy(theta, singular, "o-")
    axes[0].set(
        xlabel=r"contour angle $\theta$",
        ylabel=r"sampled $s_{\min}(zI-QAQ)$",
        title="Global singular-value candidates",
    )
    axes[1].semilogy(theta, resolvent, "o-", label="resolvent candidate")
    twin = axes[1].twinx()
    twin.semilogy(theta, majorant, "s--", color="#b24a33", label="scalar majorant")
    axes[1].set(
        xlabel=r"contour angle $\theta$",
        ylabel="candidate resolvent norm",
        title="Global scalar route at $\sigma=10^{-2}$",
    )
    twin.set_ylabel("candidate Rouché majorant", color="#b24a33")
    axes[2].semilogy(direct_theta, direct_ratio, "o-", ms=3, label="directional ratio")
    axes[2].semilogy(
        direct_theta,
        direct_residual,
        "s--",
        ms=3,
        label="GMRES residual",
    )
    axes[2].axhline(1.0, color="0.4", lw=0.8)
    axes[2].set(
        xlabel=r"contour angle $\theta$",
        ylabel="relative scale",
        title="Direct full-Feshbach cross-check",
    )
    axes[2].legend(frameon=False, fontsize=8)
    for axis in axes:
        axis.grid(alpha=0.2, which="both")
    fig.tight_layout()
    fig.savefig(FIGURES / "global_resolvent_probe.pdf")
    fig.savefig(FIGURES / "global_resolvent_probe.png", dpi=220)
    plt.close(fig)


def regenerate() -> None:
    plot_results(
        read_csv(RESULTS / "global_resolvent_nodes.csv"),
        read_csv(RESULTS / "direct_full_feshbach_nodes.csv"),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reuse", action="store_true")
    parser.add_argument("--barrier-only", action="store_true")
    parser.add_argument("--skip-barrier", action="store_true")
    parser.add_argument("--global-nodes", type=int, default=GLOBAL_NODES)
    parser.add_argument("--direct-nodes", type=int, default=DIRECT_NODES)
    parser.add_argument("--barrier-nodes", type=int, default=BARRIER_NODES)
    parser.add_argument(
        "--barrier-maxiter", type=int, default=BARRIER_MAXIMUM_ITERATIONS
    )
    parser.add_argument(
        "--barrier-seconds", type=float, default=BARRIER_WALL_SECONDS
    )
    arguments = parser.parse_args()
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    if arguments.barrier_only:
        barrier = run_fixed_budget_barrier(
            int(arguments.barrier_nodes),
            int(arguments.barrier_maxiter),
            float(arguments.barrier_seconds),
        )
        write_csv(RESULTS / "fixed_budget_global_barrier.csv", barrier)
    elif not arguments.reuse:
        settings = rh24.physical_settings()
        print(f"global and direct probes sigma={GLOBAL_SIGMA:g}", flush=True)
        data = directional.build_physical_extended_model(
            GLOBAL_SIGMA, settings[GLOBAL_SIGMA]
        )
        global_rows, global_summary = run_global_nodes(
            data, int(arguments.global_nodes)
        )
        direct_rows, direct_summary = direct_full_feshbach(
            data, int(arguments.direct_nodes)
        )
        combined = {**global_summary, **direct_summary}
        write_csv(RESULTS / "global_resolvent_nodes.csv", global_rows)
        write_csv(RESULTS / "direct_full_feshbach_nodes.csv", direct_rows)
        write_csv(RESULTS / "global_resolvent_summary.csv", [combined])
        del data
        rh24.release_memory()
        if not arguments.skip_barrier:
            barrier = run_fixed_budget_barrier(
                int(arguments.barrier_nodes),
                int(arguments.barrier_maxiter),
                float(arguments.barrier_seconds),
            )
            write_csv(RESULTS / "fixed_budget_global_barrier.csv", barrier)

    regenerate()
    metadata = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "global_sigma": GLOBAL_SIGMA,
        "barrier_sigma": BARRIER_SIGMA,
        "global_nodes": GLOBAL_NODES,
        "direct_nodes": DIRECT_NODES,
        "global_tolerance": GLOBAL_TOLERANCE,
        "global_maximum_iterations": GLOBAL_MAXIMUM_ITERATIONS,
        "global_ncv": GLOBAL_NCV,
        "barrier_nodes": BARRIER_NODES,
        "barrier_maximum_iterations": BARRIER_MAXIMUM_ITERATIONS,
        "barrier_ncv": BARRIER_NCV,
        "barrier_wall_seconds": BARRIER_WALL_SECONDS,
        "direct_atol_factor": DIRECT_ATOL_FACTOR,
        "source_hashes": {
            "probe.py": source_hash(Path(__file__)),
            "directional_audit.py": source_hash(
                ROOT / "experiments" / "run_directional_closure_audit.py"
            ),
            "algebra.py": source_hash(
                ROOT / "src" / "directional_rouche" / "algebra.py"
            ),
        },
    }
    with (RESULTS / "global_probe_metadata.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print("generated global resolvent and direct directional probes", flush=True)


if __name__ == "__main__":
    main()
