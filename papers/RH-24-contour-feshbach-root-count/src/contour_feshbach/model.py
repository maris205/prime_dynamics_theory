"""Shift-invariant contour Feshbach models and argument-principle audits.

The numerical model in this module is deliberately holomorphic in the
spectral parameter.  Each right-hand side is reduced by an Arnoldi--FOM
projection.  Unlike a least-squares solve performed independently at every
shift, the resulting rational matrix can therefore be used in a legitimate
finite-dimensional argument-principle calculation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


ObservedAction = Callable[[np.ndarray], tuple[np.ndarray, np.ndarray]]


@dataclass(frozen=True)
class FeshbachEvaluation:
    """One evaluation of a projected rational Feshbach matrix."""

    spectral_parameter: complex
    self_energy: np.ndarray
    feshbach: np.ndarray
    derivative: np.ndarray
    relative_column_residuals: np.ndarray
    relative_column_residual_bounds: np.ndarray
    relative_frobenius_residual: float
    relative_frobenius_projected_residual: float
    determinant_logabs: float
    determinant_phase: float
    smallest_singular_value: float
    largest_singular_value: float


@dataclass(frozen=True)
class ContourAudit:
    """Argument-principle diagnostics on one counterclockwise circle."""

    center: complex
    radius: float
    depth: int
    points: np.ndarray
    determinant_logabs: np.ndarray
    determinant_phase: np.ndarray
    smallest_singular_values: np.ndarray
    relative_residuals: np.ndarray
    winding_float: float
    winding_integer: int
    projected_pole_count: int
    projected_zero_count: int
    cauchy_count: complex
    cauchy_first_moment: complex
    maximum_phase_increment: float
    minimum_pole_boundary_distance: float

    @property
    def cauchy_centroid(self) -> complex:
        """Return the first-moment centroid when the Cauchy count is nonzero."""

        if abs(self.cauchy_count) < 1.0e-12:
            return complex(np.nan, np.nan)
        return complex(self.cauchy_first_moment / self.cauchy_count)


@dataclass(frozen=True)
class RootResult:
    """Newton refinement of a simple projected Feshbach zero."""

    root: complex
    converged: bool
    iterations: int
    final_step: float
    relative_smallest_singular_value: float


@dataclass(frozen=True)
class SampledRoucheAudit:
    """A sampled, floating-point comparison of two projected maps."""

    maximum_relative_perturbation: float
    minimum_base_singular_value: float
    base_pole_count: int
    comparison_pole_count: int
    criterion_satisfied_on_mesh: bool


@dataclass(frozen=True)
class BatchedArnoldiFeshbach:
    r"""Independent Arnoldi reductions for all columns of ``Q A V``.

    If ``D=WAV``, the represented rational matrix is

    ``F_J(z) = z I - D - G_J (z I-H_J)^(-1) B_J``.

    Here ``H_J`` is block diagonal only as a bookkeeping device: every
    packet forcing column has its own scalar Arnoldi space.  This avoids the
    quadratic orthogonalization cost of a large block-Arnoldi basis while
    retaining one shift-invariant, holomorphic model for the entire contour.
    """

    reduced: np.ndarray
    forcing_norms: np.ndarray
    hessenbergs: tuple[np.ndarray, ...]
    output_couplings: tuple[np.ndarray, ...]
    arnoldi_orthogonality_errors: np.ndarray
    arnoldi_relation_defect_norms: tuple[np.ndarray, ...] | None = None
    retained_bases: tuple[np.ndarray, ...] | None = None

    def __post_init__(self) -> None:
        reduced = np.asarray(self.reduced, dtype=np.complex128)
        if reduced.ndim != 2 or reduced.shape[0] != reduced.shape[1]:
            raise ValueError("reduced must be square")
        rank = reduced.shape[0]
        norms = np.asarray(self.forcing_norms, dtype=np.float64)
        if norms.shape != (rank,) or np.any(norms <= 0.0):
            raise ValueError("one positive forcing norm is required per column")
        if len(self.hessenbergs) != rank or len(self.output_couplings) != rank:
            raise ValueError("one Arnoldi model is required per packet column")
        if self.arnoldi_relation_defect_norms is not None and len(
            self.arnoldi_relation_defect_norms
        ) != rank:
            raise ValueError("one relation-defect history is required per column")
        step_counts = []
        for hessenberg, coupling in zip(self.hessenbergs, self.output_couplings):
            hbar = np.asarray(hessenberg, dtype=np.complex128)
            output = np.asarray(coupling, dtype=np.complex128)
            if hbar.ndim != 2 or hbar.shape[0] != hbar.shape[1] + 1:
                raise ValueError("each Arnoldi Hessenberg matrix must be (J+1)-by-J")
            if output.shape != (rank, hbar.shape[1]):
                raise ValueError("output coupling has incompatible shape")
            if self.arnoldi_relation_defect_norms is not None:
                defects = np.asarray(
                    self.arnoldi_relation_defect_norms[len(step_counts)]
                )
                if defects.shape != (hbar.shape[1],) or np.any(defects < 0.0):
                    raise ValueError("Arnoldi relation defects have incompatible shape")
            step_counts.append(hbar.shape[1])
        if len(set(step_counts)) != 1:
            raise ValueError("all Arnoldi columns must currently use the same depth")

    @property
    def packet_rank(self) -> int:
        return int(np.asarray(self.reduced).shape[0])

    @property
    def maximum_depth(self) -> int:
        return int(np.asarray(self.hessenbergs[0]).shape[1])

    def _checked_depth(self, depth: int | None) -> int:
        selected = self.maximum_depth if depth is None else int(depth)
        if selected < 1 or selected > self.maximum_depth:
            raise ValueError("depth must lie between one and maximum_depth")
        return selected

    def evaluate(
        self,
        spectral_parameter: complex,
        *,
        depth: int | None = None,
    ) -> FeshbachEvaluation:
        """Evaluate the rational Feshbach map and exact Arnoldi residuals."""

        selected = self._checked_depth(depth)
        zeta = complex(spectral_parameter)
        rank = self.packet_rank
        self_energy = np.empty((rank, rank), dtype=np.complex128)
        derivative = np.eye(rank, dtype=np.complex128)
        relative_residuals = np.empty(rank, dtype=np.float64)
        relative_residual_bounds = np.empty(rank, dtype=np.float64)
        for column in range(rank):
            hbar = np.asarray(self.hessenbergs[column], dtype=np.complex128)
            hessenberg = hbar[:selected, :selected]
            coupling = np.asarray(
                self.output_couplings[column], dtype=np.complex128
            )[:, :selected]
            right_hand_side = np.zeros(selected, dtype=np.complex128)
            right_hand_side[0] = float(self.forcing_norms[column])
            shifted = zeta * np.eye(selected, dtype=np.complex128) - hessenberg
            coordinates = np.linalg.solve(shifted, right_hand_side)
            second_coordinates = np.linalg.solve(shifted, coordinates)
            self_energy[:, column] = coupling @ coordinates
            derivative[:, column] += coupling @ second_coordinates
            tail = hbar[selected, selected - 1]
            forcing_norm = float(self.forcing_norms[column])
            projected_residual = abs(tail * coordinates[-1])
            relative_residuals[column] = projected_residual / forcing_norm
            if self.arnoldi_relation_defect_norms is None:
                relation_bound = 0.0
            else:
                defects = np.asarray(
                    self.arnoldi_relation_defect_norms[column], dtype=np.float64
                )[:selected]
                relation_bound = float(np.dot(np.abs(coordinates), defects))
            relative_residual_bounds[column] = (
                projected_residual + relation_bound
            ) / forcing_norm
        feshbach = (
            zeta * np.eye(rank, dtype=np.complex128)
            - np.asarray(self.reduced, dtype=np.complex128)
            - self_energy
        )
        singular_values = np.linalg.svd(feshbach, compute_uv=False)
        determinant_sign, determinant_logabs = np.linalg.slogdet(feshbach)
        determinant_phase = (
            float(np.angle(determinant_sign))
            if determinant_sign != 0.0
            else float("nan")
        )
        absolute_residuals = relative_residuals * np.asarray(self.forcing_norms)
        absolute_bounds = relative_residual_bounds * np.asarray(self.forcing_norms)
        forcing_frobenius = np.linalg.norm(self.forcing_norms)
        frobenius_projected = np.linalg.norm(absolute_residuals) / forcing_frobenius
        frobenius_bound = np.linalg.norm(absolute_bounds) / forcing_frobenius
        return FeshbachEvaluation(
            spectral_parameter=zeta,
            self_energy=self_energy,
            feshbach=feshbach,
            derivative=derivative,
            relative_column_residuals=relative_residuals,
            relative_column_residual_bounds=relative_residual_bounds,
            relative_frobenius_residual=float(frobenius_bound),
            relative_frobenius_projected_residual=float(frobenius_projected),
            determinant_logabs=float(determinant_logabs),
            determinant_phase=determinant_phase,
            smallest_singular_value=float(singular_values[-1]),
            largest_singular_value=float(singular_values[0]),
        )

    def projected_poles(self, *, depth: int | None = None) -> np.ndarray:
        """Return all poles of the column-wise projected external resolvents."""

        selected = self._checked_depth(depth)
        values = [
            np.linalg.eigvals(
                np.asarray(hessenberg, dtype=np.complex128)[:selected, :selected]
            )
            for hessenberg in self.hessenbergs
        ]
        return np.concatenate(values)

    def augmented_matrix(self, *, depth: int | None = None) -> np.ndarray:
        r"""Return the matrix whose Schur complement is ``F_J(z)``.

        The exact identity

        ``det(zI-M_J)=prod_i det(zI-H_i) det(F_J(z))``

        makes projected winding counts independently checkable by ordinary
        finite-dimensional eigenvalue counts.
        """

        selected = self._checked_depth(depth)
        rank = self.packet_rank
        external_dimension = rank * selected
        augmented = np.zeros(
            (rank + external_dimension, rank + external_dimension),
            dtype=np.complex128,
        )
        augmented[:rank, :rank] = np.asarray(self.reduced, dtype=np.complex128)
        for column in range(rank):
            start = rank + column * selected
            stop = start + selected
            hessenberg = np.asarray(
                self.hessenbergs[column], dtype=np.complex128
            )[:selected, :selected]
            coupling = np.asarray(
                self.output_couplings[column], dtype=np.complex128
            )[:, :selected]
            augmented[:rank, start:stop] = coupling
            augmented[start, column] = float(self.forcing_norms[column])
            augmented[start:stop, start:stop] = hessenberg
        return augmented

    def determinant_factorization_residual(
        self,
        spectral_parameter: complex,
        *,
        depth: int | None = None,
    ) -> float:
        """Check the projected Schur determinant identity at one point."""

        selected = self._checked_depth(depth)
        zeta = complex(spectral_parameter)
        evaluation = self.evaluate(zeta, depth=selected)
        augmented = self.augmented_matrix(depth=selected)
        left = np.linalg.det(zeta * np.eye(augmented.shape[0]) - augmented)
        external = 1.0 + 0.0j
        for hbar in self.hessenbergs:
            hessenberg = np.asarray(hbar)[:selected, :selected]
            external *= np.linalg.det(
                zeta * np.eye(selected, dtype=np.complex128) - hessenberg
            )
        right = external * np.linalg.det(evaluation.feshbach)
        scale = max(abs(left), abs(right), np.finfo(float).tiny)
        return float(abs(left - right) / scale)


def build_batched_arnoldi_feshbach(
    observed_action: ObservedAction,
    forcing: np.ndarray,
    reduced: np.ndarray,
    *,
    steps: int,
    reorthogonalizations: int = 2,
    breakdown_tolerance: float = 2.0e-13,
    retain_bases: bool = False,
) -> BatchedArnoldiFeshbach:
    """Build simultaneous independent Arnoldi reductions for every forcing.

    ``observed_action(X)`` must return ``(B X, E X)`` for a matrix ``X``.
    Sparse applications are consequently batched across all packet columns,
    while orthogonalization remains column-wise and inexpensive.
    """

    source = np.asarray(forcing, dtype=np.complex128)
    direct = np.asarray(reduced, dtype=np.complex128)
    if source.ndim != 2 or direct.shape != (source.shape[1], source.shape[1]):
        raise ValueError("forcing and reduced matrix have incompatible shapes")
    if int(steps) < 1:
        raise ValueError("steps must be positive")
    if int(reorthogonalizations) < 1:
        raise ValueError("at least one orthogonalization pass is required")
    ambient, rank = source.shape
    depth = int(steps)
    forcing_norms = np.linalg.norm(source, axis=0)
    if np.any(forcing_norms <= np.finfo(float).tiny):
        raise ValueError("every forcing column must be nonzero")
    bases = [np.empty((ambient, depth + 1), dtype=np.complex128) for _ in range(rank)]
    hessenbergs = [np.zeros((depth + 1, depth), dtype=np.complex128) for _ in range(rank)]
    couplings = [np.empty((rank, depth), dtype=np.complex128) for _ in range(rank)]
    relation_defects = [np.empty(depth, dtype=np.float64) for _ in range(rank)]
    for column in range(rank):
        bases[column][:, 0] = source[:, column] / forcing_norms[column]

    for step in range(depth):
        current = np.column_stack([basis[:, step] for basis in bases])
        external_values, observed_values = observed_action(current)
        external_values = np.asarray(external_values, dtype=np.complex128)
        observed_values = np.asarray(observed_values, dtype=np.complex128)
        if external_values.shape != current.shape:
            raise ValueError("external action returned an incompatible shape")
        if observed_values.shape != (rank, rank):
            raise ValueError("observed action must return packet-rank rows")
        for column in range(rank):
            couplings[column][:, step] = observed_values[:, column]
            candidate = np.array(external_values[:, column], copy=True)
            original_norm = np.linalg.norm(candidate)
            basis = bases[column][:, : step + 1]
            coefficients = np.zeros(step + 1, dtype=np.complex128)
            for _ in range(int(reorthogonalizations)):
                correction = basis.conj().T @ candidate
                coefficients += correction
                candidate -= basis @ correction
            tail = np.linalg.norm(candidate)
            hessenbergs[column][: step + 1, step] = coefficients
            hessenbergs[column][step + 1, step] = tail
            threshold = float(breakdown_tolerance) * max(original_norm, 1.0)
            if tail <= threshold:
                raise RuntimeError(
                    f"Arnoldi breakdown in forcing column {column} at step {step + 1}"
                )
            bases[column][:, step + 1] = candidate / tail
            reconstructed = basis @ coefficients + tail * bases[column][:, step + 1]
            relation_defects[column][step] = np.linalg.norm(
                external_values[:, column] - reconstructed
            )

    orthogonality = np.asarray(
        [
            np.linalg.norm(
                basis[:, :depth].conj().T @ basis[:, :depth]
                - np.eye(depth),
                ord=2,
            )
            for basis in bases
        ],
        dtype=np.float64,
    )
    retained = tuple(np.asarray(basis) for basis in bases) if retain_bases else None
    return BatchedArnoldiFeshbach(
        reduced=direct,
        forcing_norms=np.asarray(forcing_norms),
        hessenbergs=tuple(np.asarray(hessenberg) for hessenberg in hessenbergs),
        output_couplings=tuple(np.asarray(coupling) for coupling in couplings),
        arnoldi_orthogonality_errors=orthogonality,
        arnoldi_relation_defect_norms=tuple(
            np.asarray(defects) for defects in relation_defects
        ),
        retained_bases=retained,
    )


def circle_contour_audit(
    model: BatchedArnoldiFeshbach,
    center: complex,
    radius: float,
    *,
    nodes: int = 128,
    depth: int | None = None,
) -> ContourAudit:
    """Evaluate winding, Cauchy moments, poles, and residuals on a circle."""

    if float(radius) <= 0.0:
        raise ValueError("radius must be positive")
    if int(nodes) < 8:
        raise ValueError("at least eight contour nodes are required")
    selected = model._checked_depth(depth)
    angles = 2.0 * np.pi * np.arange(int(nodes), dtype=np.float64) / int(nodes)
    directions = np.exp(1.0j * angles)
    points = complex(center) + float(radius) * directions
    evaluations = [model.evaluate(point, depth=selected) for point in points]
    phases = np.asarray([item.determinant_phase for item in evaluations])
    logabs = np.asarray([item.determinant_logabs for item in evaluations])
    smallest = np.asarray([item.smallest_singular_value for item in evaluations])
    residuals = np.asarray([item.relative_frobenius_residual for item in evaluations])
    phase_increments = np.angle(
        np.exp(1.0j * (np.roll(phases, -1) - phases))
    )
    winding_float = float(np.sum(phase_increments) / (2.0 * np.pi))
    winding_integer = int(np.rint(winding_float))
    logarithmic_derivatives = np.asarray(
        [
            np.trace(np.linalg.solve(item.feshbach, item.derivative))
            for item in evaluations
        ]
    )
    differential = (
        1.0j * float(radius) * directions * (2.0 * np.pi / int(nodes))
    )
    cauchy_count = np.sum(logarithmic_derivatives * differential) / (
        2.0j * np.pi
    )
    first_moment = np.sum(
        points * logarithmic_derivatives * differential
    ) / (2.0j * np.pi)
    poles = model.projected_poles(depth=selected)
    pole_distances = np.abs(poles - complex(center))
    pole_count = int(np.count_nonzero(pole_distances < float(radius)))
    boundary_distance = float(np.min(np.abs(pole_distances - float(radius))))
    return ContourAudit(
        center=complex(center),
        radius=float(radius),
        depth=selected,
        points=points,
        determinant_logabs=logabs,
        determinant_phase=phases,
        smallest_singular_values=smallest,
        relative_residuals=residuals,
        winding_float=winding_float,
        winding_integer=winding_integer,
        projected_pole_count=pole_count,
        projected_zero_count=winding_integer + pole_count,
        cauchy_count=complex(cauchy_count),
        cauchy_first_moment=complex(first_moment),
        maximum_phase_increment=float(np.max(np.abs(phase_increments))),
        minimum_pole_boundary_distance=boundary_distance,
    )


def determinant_newton_root(
    model: BatchedArnoldiFeshbach,
    initial: complex,
    *,
    depth: int | None = None,
    maximum_iterations: int = 30,
    step_tolerance: float = 2.0e-12,
    singular_tolerance: float = 2.0e-11,
    trust_radius: float | None = None,
) -> RootResult:
    """Refine a simple zero using ``(det F)'/det F=tr(F^{-1}F')``."""

    selected = model._checked_depth(depth)
    value = complex(initial)
    final_step = float("inf")
    relative_singular = float("inf")
    for iteration in range(1, int(maximum_iterations) + 1):
        evaluation = model.evaluate(value, depth=selected)
        relative_singular = evaluation.smallest_singular_value / max(
            evaluation.largest_singular_value, abs(value), 1.0
        )
        logarithmic_derivative = np.trace(
            np.linalg.solve(evaluation.feshbach, evaluation.derivative)
        )
        step = 1.0 / logarithmic_derivative
        if trust_radius is not None and abs(step) > float(trust_radius):
            step *= float(trust_radius) / abs(step)
        value -= step
        final_step = float(abs(step))
        if final_step <= float(step_tolerance) * max(1.0, abs(value)):
            final = model.evaluate(value, depth=selected)
            relative_singular = final.smallest_singular_value / max(
                final.largest_singular_value, abs(value), 1.0
            )
            return RootResult(
                root=value,
                converged=relative_singular <= float(singular_tolerance),
                iterations=iteration,
                final_step=final_step,
                relative_smallest_singular_value=float(relative_singular),
            )
    return RootResult(
        root=value,
        converged=False,
        iterations=int(maximum_iterations),
        final_step=final_step,
        relative_smallest_singular_value=float(relative_singular),
    )


def sampled_rouche_audit(
    base: BatchedArnoldiFeshbach,
    comparison: BatchedArnoldiFeshbach,
    center: complex,
    radius: float,
    *,
    nodes: int = 128,
    base_depth: int | None = None,
    comparison_depth: int | None = None,
) -> SampledRoucheAudit:
    r"""Compute sampled values of ``||F_base^{-1}(F_cmp-F_base)||_2``.

    A value below one is a rigorous matrix-Rouch\'e criterion only when the
    supremum on the full contour is controlled and both maps are analytic in
    its interior.  This routine intentionally reports the weaker sampled,
    floating-point statement.
    """

    angles = 2.0 * np.pi * np.arange(int(nodes), dtype=np.float64) / int(nodes)
    points = complex(center) + float(radius) * np.exp(1.0j * angles)
    perturbations = []
    singular_values = []
    for point in points:
        first = base.evaluate(point, depth=base_depth)
        second = comparison.evaluate(point, depth=comparison_depth)
        relative = np.linalg.solve(
            first.feshbach, second.feshbach - first.feshbach
        )
        perturbations.append(np.linalg.norm(relative, ord=2))
        singular_values.append(first.smallest_singular_value)
    base_poles = base.projected_poles(depth=base_depth)
    comparison_poles = comparison.projected_poles(depth=comparison_depth)
    base_count = int(np.count_nonzero(np.abs(base_poles - center) < radius))
    comparison_count = int(
        np.count_nonzero(np.abs(comparison_poles - center) < radius)
    )
    maximum = float(max(perturbations))
    return SampledRoucheAudit(
        maximum_relative_perturbation=maximum,
        minimum_base_singular_value=float(min(singular_values)),
        base_pole_count=base_count,
        comparison_pole_count=comparison_count,
        criterion_satisfied_on_mesh=(
            maximum < 1.0 and base_count == 0 and comparison_count == 0
        ),
    )
