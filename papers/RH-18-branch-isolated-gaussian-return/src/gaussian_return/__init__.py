"""Branch-isolated Gaussian return blocks at the band-merging map."""

from .critical import (
    affine_critical_profile,
    conditioned_critical_profile,
    critical_branch_midpoint,
    critical_geometry,
    unconditioned_critical_profile,
)
from .cyclic import (
    bipartite_root_ring,
    block_cyclic_matrix,
    return_product,
    root_ring,
    scalar_cyclic_matrix,
)
from .operators import (
    ReturnEigenpair,
    apply_local_return,
    packet_masks,
    positive_midpoints,
    principal_return_eigenpair,
    sparse_folded_gaussian_matrix,
)
from .riccati import (
    PacketTube,
    balancing_data,
    effective_noise_scales,
    fixed_boundary_width,
    periodic_packet_tube,
    periodic_packet_variances,
)

__all__ = [
    "PacketTube",
    "ReturnEigenpair",
    "affine_critical_profile",
    "apply_local_return",
    "balancing_data",
    "bipartite_root_ring",
    "block_cyclic_matrix",
    "conditioned_critical_profile",
    "critical_branch_midpoint",
    "critical_geometry",
    "effective_noise_scales",
    "fixed_boundary_width",
    "packet_masks",
    "periodic_packet_tube",
    "periodic_packet_variances",
    "positive_midpoints",
    "principal_return_eigenpair",
    "return_product",
    "root_ring",
    "scalar_cyclic_matrix",
    "sparse_folded_gaussian_matrix",
    "unconditioned_critical_profile",
]
