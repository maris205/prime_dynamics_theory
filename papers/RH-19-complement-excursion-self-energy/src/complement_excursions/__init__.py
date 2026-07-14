"""Complement excursions and time-unfolded Feshbach diagnostics."""

from .deflation import (
    PeripheralProjector,
    apply_deflated,
    resolve_peripheral_projectors,
)
from .floquet import (
    cyclic_time_lift,
    feshbach_map,
    phase_projection,
    time_fourier_blocks,
)
from .returns import (
    PowerEigenpair,
    apply_endpoint_return,
    apply_restricted_return,
    critical_branch_masks,
    power_eigenpair,
)

__all__ = [
    "PeripheralProjector",
    "PowerEigenpair",
    "apply_deflated",
    "apply_endpoint_return",
    "apply_restricted_return",
    "critical_branch_masks",
    "cyclic_time_lift",
    "feshbach_map",
    "phase_projection",
    "power_eigenpair",
    "resolve_peripheral_projectors",
    "time_fourier_blocks",
]
