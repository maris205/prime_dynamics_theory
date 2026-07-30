from fourier_defect import BETA, common_shift_moment, ideal_roots, moment_error_bound


def test_unshifted_odd_moments_vanish():
    for N in range(2, 10):
        for n in (1, 3, 5):
            assert abs(sum(z**n for z in ideal_roots(N))) < 1e-12


def test_common_shift_can_grow_third_moment():
    small = abs(common_shift_moment(63, 3, 64 ** -0.5))
    large = abs(common_shift_moment(255, 3, 256 ** -0.5))
    assert large > 1.8 * small
    assert BETA < 1


def test_radial_bound_counts_both_conjugate_atoms():
    delta = 0.01
    perturbed = ideal_roots(1, BETA + delta)
    reference = ideal_roots(1, BETA)
    actual_error = abs(sum(z**2 for z in perturbed) - sum(z**2 for z in reference))
    bound = moment_error_bound(
        2,
        BETA,
        phase_l1=0.0,
        radial_l1=delta,
        radius_cap=BETA + delta,
    )
    assert actual_error <= bound
