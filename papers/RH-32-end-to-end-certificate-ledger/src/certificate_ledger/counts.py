"""Arb eigenvalue-ball certificates for stored rational Feshbach models."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import time
from typing import Iterable

import numpy as np
from flint import acb, acb_mat, arb, ctx


class AmbiguousCircleError(RuntimeError):
    """Raised when a verified eigenvalue ball intersects the test circle."""


def exact_arb(value: float) -> arb:
    """Embed one binary64 value as an exact dyadic Arb number."""

    return arb(float(value))


def exact_acb(value: complex) -> acb:
    """Embed one complex binary64 value componentwise as exact dyadics."""

    zeta = complex(value)
    return acb(exact_arb(zeta.real), exact_arb(zeta.imag))


def lower_float(value: arb) -> float:
    """Return a binary64 lower bound for an Arb real ball."""

    return math.nextafter(float(value.lower()), -math.inf)


def upper_float(value: arb) -> float:
    """Return a binary64 upper bound for an Arb real ball."""

    return math.nextafter(float(value.upper()), math.inf)


@dataclass(frozen=True)
class CircleClassification:
    """Classification of verified complex balls relative to one circle."""

    inside_count: int
    outside_count: int
    ambiguous_count: int
    maximum_inside_modulus_upper: arb | None
    minimum_outside_modulus_lower: arb | None

    @property
    def complete(self) -> bool:
        return self.ambiguous_count == 0

    def require_complete(self, label: str = "eigenvalue") -> None:
        if not self.complete:
            raise AmbiguousCircleError(
                f"{self.ambiguous_count} {label} ball(s) intersect the circle"
            )


def classify_eigenvalue_balls(
    values: Iterable[acb],
    center: acb,
    radius: arb,
) -> CircleClassification:
    """Classify certified eigenvalue balls using rigorous modulus bounds."""

    if not radius.is_finite() or not radius > 0:
        raise ValueError("the circle radius must be finite and positive")
    inside = 0
    outside = 0
    ambiguous = 0
    maximum_inside: arb | None = None
    minimum_outside: arb | None = None
    for value in values:
        distance = abs(value - center)
        upper = distance.upper()
        lower = distance.lower()
        if upper < radius:
            inside += 1
            if maximum_inside is None or upper > maximum_inside:
                maximum_inside = upper
        elif lower > radius:
            outside += 1
            if minimum_outside is None or lower < minimum_outside:
                minimum_outside = lower
        else:
            ambiguous += 1
    return CircleClassification(
        inside_count=inside,
        outside_count=outside,
        ambiguous_count=ambiguous,
        maximum_inside_modulus_upper=maximum_inside,
        minimum_outside_modulus_lower=minimum_outside,
    )


def _exact_matrix(array: np.ndarray) -> acb_mat:
    values = np.asarray(array, dtype=np.complex128)
    if values.ndim != 2:
        raise ValueError("matrix input must be two-dimensional")
    return acb_mat(
        [
            [
                acb(exact_arb(entry.real), exact_arb(entry.imag))
                for entry in row
            ]
            for row in values
        ]
    )


def load_stored_realization(
    path: Path,
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Load and assemble the RH-24 augmented realization exactly as stored."""

    with np.load(path, allow_pickle=False) as archive:
        reduced = np.asarray(archive["reduced"], dtype=np.complex128)
        forcing_norms = np.asarray(archive["forcing_norms"], dtype=np.float64)
        rank = int(reduced.shape[0])
        if reduced.shape != (rank, rank) or forcing_norms.shape != (rank,):
            raise ValueError("invalid reduced realization dimensions")
        hessenbergs = []
        couplings = []
        for column in range(rank):
            hbar = np.asarray(
                archive[f"hessenberg_{column}"], dtype=np.complex128
            )
            coupling = np.asarray(
                archive[f"coupling_{column}"], dtype=np.complex128
            )
            if hbar.ndim != 2 or hbar.shape[0] != hbar.shape[1] + 1:
                raise ValueError("invalid stored Arnoldi Hessenberg matrix")
            depth = int(hbar.shape[1])
            if coupling.shape != (rank, depth):
                raise ValueError("invalid stored output coupling")
            hessenbergs.append(hbar[:depth, :depth])
            couplings.append(coupling)
    depths = {matrix.shape[0] for matrix in hessenbergs}
    if len(depths) != 1:
        raise ValueError("all stored column realizations must have one depth")
    depth = depths.pop()
    dimension = rank + rank * depth
    augmented = np.zeros((dimension, dimension), dtype=np.complex128)
    augmented[:rank, :rank] = reduced
    for column, (hessenberg, coupling) in enumerate(
        zip(hessenbergs, couplings)
    ):
        start = rank + column * depth
        stop = start + depth
        augmented[:rank, start:stop] = coupling
        augmented[start, column] = forcing_norms[column]
        augmented[start:stop, start:stop] = hessenberg
    return augmented, tuple(hessenbergs)


def _classification_record(
    result: CircleClassification,
    radius: arb,
) -> dict[str, float | int | None]:
    inside_clearance = None
    if result.maximum_inside_modulus_upper is not None:
        inside_clearance = lower_float(
            radius - result.maximum_inside_modulus_upper
        )
    outside_clearance = None
    if result.minimum_outside_modulus_lower is not None:
        outside_clearance = lower_float(
            result.minimum_outside_modulus_lower - radius
        )
    return {
        "inside_count": result.inside_count,
        "outside_count": result.outside_count,
        "ambiguous_count": result.ambiguous_count,
        "maximum_inside_modulus_upper": (
            None
            if result.maximum_inside_modulus_upper is None
            else upper_float(result.maximum_inside_modulus_upper)
        ),
        "minimum_outside_modulus_lower": (
            None
            if result.minimum_outside_modulus_lower is None
            else lower_float(result.minimum_outside_modulus_lower)
        ),
        "inside_boundary_clearance_lower": inside_clearance,
        "outside_boundary_clearance_lower": outside_clearance,
    }


def certify_projected_model(
    model_path: Path,
    center: complex,
    radius: float,
    *,
    precision: int = 256,
) -> tuple[dict[str, object], dict[str, float]]:
    """Certify augmented-zero and projected-pole counts in one circle.

    The serialized binary64 entries are treated as exact dyadic inputs.  Arb
    returns enclosing eigenvalue balls, including multiplicity.  A result is
    accepted only when every ball is strictly inside or strictly outside.
    """

    augmented, hessenbergs = load_stored_realization(model_path)
    rank = len(hessenbergs)
    depth = int(hessenbergs[0].shape[0])
    exact_center = exact_acb(center)
    exact_radius = exact_arb(radius)
    previous_precision = ctx.prec
    timings: dict[str, float] = {}
    try:
        ctx.prec = int(precision)
        started = time.perf_counter()
        augmented_values = _exact_matrix(augmented).eig(multiple=True)
        timings["augmented_eigensolve_seconds"] = time.perf_counter() - started
        augmented_count = classify_eigenvalue_balls(
            augmented_values, exact_center, exact_radius
        )
        augmented_count.require_complete("augmented eigenvalue")

        pole_inside = 0
        pole_outside = 0
        pole_ambiguous = 0
        pole_minimum_outside: arb | None = None
        block_seconds = 0.0
        for hessenberg in hessenbergs:
            started = time.perf_counter()
            values = _exact_matrix(hessenberg).eig(multiple=True)
            block_seconds += time.perf_counter() - started
            classified = classify_eigenvalue_balls(
                values, exact_center, exact_radius
            )
            classified.require_complete("projected-pole")
            pole_inside += classified.inside_count
            pole_outside += classified.outside_count
            pole_ambiguous += classified.ambiguous_count
            candidate = classified.minimum_outside_modulus_lower
            if candidate is not None and (
                pole_minimum_outside is None or candidate < pole_minimum_outside
            ):
                pole_minimum_outside = candidate
        timings["projected_pole_eigensolve_seconds"] = block_seconds
    finally:
        ctx.prec = previous_precision

    pole_clearance = None
    if pole_minimum_outside is not None:
        pole_clearance = lower_float(pole_minimum_outside - exact_radius)
    winding = augmented_count.inside_count - pole_inside
    record: dict[str, object] = {
        "precision_bits": int(precision),
        "packet_rank": rank,
        "arnoldi_depth": depth,
        "augmented_dimension": int(augmented.shape[0]),
        "circle_center_real": float(complex(center).real),
        "circle_center_imag": float(complex(center).imag),
        "circle_radius": float(radius),
        "augmented": _classification_record(augmented_count, exact_radius),
        "projected_poles": {
            "inside_count": pole_inside,
            "outside_count": pole_outside,
            "ambiguous_count": pole_ambiguous,
            "minimum_outside_modulus_lower": (
                None
                if pole_minimum_outside is None
                else lower_float(pole_minimum_outside)
            ),
            "outside_boundary_clearance_lower": pole_clearance,
        },
        "projected_zero_count": augmented_count.inside_count,
        "projected_pole_count": pole_inside,
        "projected_determinant_winding": winding,
        "projected_map_holomorphic_on_closed_disk": pole_inside == 0,
        "status": (
            "rigorous_exact_binary64_projected_count"
            if winding == 1
            and augmented_count.inside_count == 1
            and pole_inside == 0
            else "rigorous_exact_binary64_count_nonunit"
        ),
    }
    return record, timings
