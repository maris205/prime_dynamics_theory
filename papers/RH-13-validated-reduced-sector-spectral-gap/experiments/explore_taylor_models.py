"""Explore finite Taylor models before adding interval certification."""

from __future__ import annotations

from validated_gap import (
    LAMBDA_FIXED,
    leading_eigenvalues,
    reduced_beta_one_matrix,
    sector_matrices,
    weighted_absolute_radius,
)


def main() -> None:
    print("threshold", LAMBDA_FIXED ** -2)
    for radius in (0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95):
        degree = 80
        reduced = reduced_beta_one_matrix(degree, radius)
        _, odd_second = sector_matrices(degree, radius)
        print(
            radius,
            "beta1", leading_eigenvalues(reduced, 3),
            "beta2", leading_eigenvalues(odd_second, 3),
            "abs-radii", weighted_absolute_radius(reduced),
            weighted_absolute_radius(odd_second),
        )


if __name__ == "__main__":
    main()
