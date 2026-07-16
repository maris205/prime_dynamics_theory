from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp
import numpy as np
from scipy.sparse import csc_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path[:0] = [
    str(ROOT / "experiments"),
    str(PAPERS / "RH-27-outward-rounded-primal-dual-residuals" / "src"),
    str(PAPERS / "RH-30-sparse-two-step-grushin-inverse" / "src"),
]

from enclosed_grushin import (  # noqa: E402
    _power_of_two_balance,
    build_enclosed_grushin_system,
)
from sparse_grushin import dense_lifted_complement  # noqa: E402
from threshold_inertia import (
    asymmetric_inertia_bracket,
    build_threshold_inertia_system,
    dense_inertia,
    hermitian_ldl_backward_error_upper,
    inertia_bracket,
    paired_hadamard_congruence,
    shifted_hermitian_dilation,
)


def synthetic_channel_factors(seed: int = 20260717):
    rng = np.random.default_rng(seed)
    dimension = 5
    peripheral_rank = 2
    packet_rank = 2

    def complex_random(shape, scale=1.0):
        return scale * (
            rng.standard_normal(shape) + 1.0j * rng.standard_normal(shape)
        )

    matrix = complex_random((dimension, dimension), 0.12)
    right = complex_random((dimension, peripheral_rank), 0.3)
    left = complex_random((dimension, peripheral_rank), 0.25)
    values = np.array([0.31 + 0.07j, -0.23 + 0.04j])
    synthesis = complex_random((dimension, packet_rank), 0.2)
    analysis = complex_random((packet_rank, dimension), 0.18)
    dangerous_left = complex_random(dimension)
    dangerous_right = complex_random(dimension)
    return (
        matrix,
        right,
        left,
        values,
        synthesis,
        analysis,
        dangerous_left,
        dangerous_right,
    )


def mp_real(value: float) -> mp.mpf:
    numerator, denominator = float(value).as_integer_ratio()
    return mp.mpf(numerator) / mp.mpf(denominator)


def mp_complex(value: complex) -> mp.mpc:
    scalar = complex(value)
    return mp.mpc(mp_real(scalar.real), mp_real(scalar.imag))


def mp_matrix(values: np.ndarray) -> mp.matrix:
    array = np.asarray(values)
    return mp.matrix(
        [
            [mp_complex(array[row, column]) for column in range(array.shape[1])]
            for row in range(array.shape[0])
        ]
    )


def exact_balanced_channels(factors, singular: float, scales: np.ndarray):
    matrix, right, left, values, synthesis, analysis, u0, v0 = factors
    dimension = matrix.shape[0]
    stored = mp_matrix(matrix)
    right_mp = mp_matrix(right)
    left_mp = mp_matrix(left)
    synthesis_mp = mp_matrix(synthesis)
    analysis_mp = mp_matrix(analysis)
    values_mp = [mp_complex(value) for value in values]
    bulk = stored - right_mp * mp.diag(values_mp) * left_mp.T
    uv = bulk * synthesis_mp
    wu = analysis_mp * bulk
    u_mp = [mp_complex(value) for value in u0]
    v_mp = [mp_complex(value) for value in v0]
    u_norm = mp.sqrt(mp.fsum(abs(value) ** 2 for value in u_mp))
    v_norm = mp.sqrt(mp.fsum(abs(value) ** 2 for value in v_mp))
    coefficient = (mp.mpf(1) - mp_real(singular)) / (u_norm * v_norm)

    columns: list[list[mp.mpc]] = []
    rows: list[list[mp.mpc]] = []
    labels: list[str] = []

    def append(column, row, label):
        columns.append(list(column))
        rows.append(list(row))
        labels.append(label)

    zeros = [mp.mpc(0) for _ in range(2 * dimension)]
    append(
        u_mp + zeros[dimension:],
        [coefficient * mp.conj(value) for value in v_mp] + zeros[dimension:],
        "lift",
    )
    for index in range(right.shape[1]):
        append(
            [right_mp[row, index] for row in range(dimension)] + zeros[dimension:],
            zeros[:dimension]
            + [values_mp[index] * left_mp[row, index] for row in range(dimension)],
            f"top_peripheral_{index}",
        )
    for index in range(synthesis.shape[1]):
        append(
            [synthesis_mp[row, index] for row in range(dimension)]
            + zeros[dimension:],
            zeros[:dimension] + [wu[index, row] for row in range(dimension)],
            f"top_packet_{index}",
        )
    for index in range(right.shape[1]):
        append(
            zeros[:dimension]
            + [right_mp[row, index] for row in range(dimension)],
            [values_mp[index] * left_mp[row, index] for row in range(dimension)]
            + zeros[dimension:],
            f"bottom_peripheral_{index}",
        )
    for index in range(synthesis.shape[1]):
        append(
            zeros[:dimension] + [uv[row, index] for row in range(dimension)],
            [analysis_mp[index, row] for row in range(dimension)]
            + zeros[dimension:],
            f"bottom_packet_{index}",
        )

    for index, stored_scale in enumerate(scales):
        scale = mp_real(float(stored_scale))
        columns[index] = [scale * value for value in columns[index]]
        rows[index] = [value / scale for value in rows[index]]
    return columns, rows, labels, coefficient


def random_matrix(seed: int = 20260716) -> np.ndarray:
    rng = np.random.default_rng(seed)
    matrix = rng.standard_normal((6, 6)) + 1.0j * rng.standard_normal((6, 6))
    matrix += (2.0 - 0.7j) * np.eye(6)
    return matrix


def test_paired_hadamard_congruence_preserves_inertia() -> None:
    matrix = random_matrix()
    threshold = 0.17
    dilation = shifted_hermitian_dilation(csc_matrix(matrix), threshold).toarray()
    paired = paired_hadamard_congruence(csc_matrix(matrix), threshold).toarray()
    assert dense_inertia(dilation) == dense_inertia(paired)


def test_threshold_inertia_is_equivalent_to_smallest_singular_value() -> None:
    matrix = random_matrix(9)
    smallest = float(np.linalg.svd(matrix, compute_uv=False)[-1])
    below = build_threshold_inertia_system(csc_matrix(matrix), 0.8 * smallest)
    above = build_threshold_inertia_system(csc_matrix(matrix), 1.2 * smallest)
    assert dense_inertia(below.matrix.toarray()) == (6, 6, 0)
    positive, negative, zero = dense_inertia(above.matrix.toarray())
    assert positive < 6
    assert negative > 6
    assert zero == 0


def test_pair_permutation_preserves_hermitian_structure() -> None:
    system = build_threshold_inertia_system(csc_matrix(random_matrix(17)), 0.11)
    defect = system.matrix - system.matrix.conj().T
    assert np.linalg.norm(defect.toarray()) < 1.0e-13
    np.testing.assert_array_equal(
        np.sort(system.scalar_permutation), np.arange(system.dimension)
    )


def test_two_shift_bracket_recovers_exact_inertia() -> None:
    matrix = paired_hadamard_congruence(csc_matrix(random_matrix(31)), 0.05)
    shift = 0.02
    bounds = []
    from scipy.sparse import eye
    from scipy.sparse.linalg import splu

    for sign in (-1.0, 1.0):
        shifted = matrix + sign * shift * eye(
            matrix.shape[0], format="csc", dtype=np.complex128
        )
        factor = splu(
            shifted,
            permc_spec="NATURAL",
            diag_pivot_thresh=0.0,
            options={"SymmetricMode": True, "Equil": False},
        )
        bounds.append(
            hermitian_ldl_backward_error_upper(factor.L, factor.U)
        )
    bracket = inertia_bracket(shift, bounds[0], bounds[1])
    assert bracket.admissible
    assert (bracket.positive_count, bracket.negative_count) == dense_inertia(
        matrix.toarray()
    )[:2]


def test_default_complex_elimination_bound_dominates_observed_defect() -> None:
    matrix = paired_hadamard_congruence(csc_matrix(random_matrix(73)), 0.06)
    from scipy.sparse.linalg import splu

    factor = splu(
        matrix,
        permc_spec="NATURAL",
        diag_pivot_thresh=0.0,
        options={"SymmetricMode": True, "Equil": False},
    )
    bound = hermitian_ldl_backward_error_upper(factor.L, factor.U)
    diagonal = np.asarray(factor.U.diagonal().real)
    exact_ldl_center = factor.L @ (
        factor.L.conj().T.multiply(diagonal[:, None])
    )
    observed = np.linalg.norm((matrix - exact_ldl_center).toarray(), 2)
    assert bound.elimination_operation_factor == 24
    assert observed < bound.total_error_upper


def test_asymmetric_two_shift_bracket_recovers_exact_inertia() -> None:
    matrix = paired_hadamard_congruence(csc_matrix(random_matrix(55)), 0.04)
    distances = (0.013, 0.027)
    bounds = []
    from scipy.sparse import eye
    from scipy.sparse.linalg import splu

    for sign, distance in ((-1.0, distances[0]), (1.0, distances[1])):
        shifted = matrix + sign * distance * eye(
            matrix.shape[0], format="csc", dtype=np.complex128
        )
        factor = splu(
            shifted,
            permc_spec="NATURAL",
            diag_pivot_thresh=0.0,
            options={"SymmetricMode": True, "Equil": False},
        )
        bounds.append(hermitian_ldl_backward_error_upper(factor.L, factor.U))
    bracket = asymmetric_inertia_bracket(
        distances[0], distances[1], bounds[0], bounds[1]
    )
    assert bracket.admissible
    assert bracket.shift is None
    assert bracket.lower_shift == distances[0]
    assert bracket.upper_shift == distances[1]
    assert (bracket.positive_count, bracket.negative_count) == dense_inertia(
        matrix.toarray()
    )[:2]


def test_exact_channel_center_has_the_required_lifted_schur_block() -> None:
    factors = synthetic_channel_factors()
    singular = 0.037
    point = 0.21 - 0.43j
    enclosed = build_enclosed_grushin_system(
        csc_matrix(factors[0]),
        *factors[1:],
        singular,
        point,
        0.013,
    )
    dimension = factors[0].shape[0]
    linearized = (
        enclosed.system.base.toarray()
        + enclosed.system.update.columns @ enclosed.system.update.rows
    )
    schur = (
        linearized[:dimension, :dimension]
        - linearized[:dimension, dimension:]
        @ linearized[dimension:, :dimension]
    )
    target = dense_lifted_complement(
        factors[0],
        *factors[1:],
        singular,
        point,
    )
    np.testing.assert_allclose(schur, target, rtol=2.0e-13, atol=2.0e-13)


def test_power_of_two_channel_balance_preserves_the_exact_product() -> None:
    rng = np.random.default_rng(81)
    columns = rng.standard_normal((8, 3)) + 1.0j * rng.standard_normal((8, 3))
    rows = rng.standard_normal((3, 8)) + 1.0j * rng.standard_normal((3, 8))
    columns[:, 0] = np.ldexp(columns[:, 0].real, -18) + 1.0j * np.ldexp(
        columns[:, 0].imag, -18
    )
    rows[0, :] = np.ldexp(rows[0, :].real, 18) + 1.0j * np.ldexp(
        rows[0, :].imag, 18
    )
    column_radii = np.full(columns.shape, 2.0**-45)
    row_radii = np.full(rows.shape, 2.0**-43)
    balanced = _power_of_two_balance(
        columns, column_radii, rows, row_radii
    )
    balanced_columns, balanced_column_radii, balanced_rows, balanced_row_radii, scales = (
        balanced
    )
    assert np.any(scales != 1.0)
    for index, scale in enumerate(scales):
        exponent = int(np.rint(np.log2(scale)))
        restored_column = np.ldexp(
            balanced_columns[:, index].real, -exponent
        ) + 1.0j * np.ldexp(balanced_columns[:, index].imag, -exponent)
        restored_row = np.ldexp(
            balanced_rows[index, :].real, exponent
        ) + 1.0j * np.ldexp(balanced_rows[index, :].imag, exponent)
        np.testing.assert_array_equal(restored_column, columns[:, index])
        np.testing.assert_array_equal(restored_row, rows[index, :])
        np.testing.assert_array_equal(
            np.ldexp(balanced_column_radii[:, index], -exponent),
            column_radii[:, index],
        )
        np.testing.assert_array_equal(
            np.ldexp(balanced_row_radii[index, :], exponent),
            row_radii[index, :],
        )
    np.testing.assert_allclose(
        balanced_columns @ balanced_rows,
        columns @ rows,
        rtol=3.0e-15,
        atol=3.0e-15,
    )


def test_exact_channels_lie_inside_the_componentwise_grushin_enclosure() -> None:
    factors = synthetic_channel_factors(44)
    singular = 0.029
    enclosed = build_enclosed_grushin_system(
        csc_matrix(factors[0]),
        *factors[1:],
        singular,
        -0.17 - 0.32j,
        0.009,
    )
    with mp.workdps(100):
        exact_columns, exact_rows, labels, coefficient = exact_balanced_channels(
            factors, singular, enclosed.power_of_two_scales
        )
        assert labels == list(enclosed.system.update.channel_labels)
        assert mp_real(enclosed.lift_coefficient_lower) <= coefficient
        assert coefficient <= mp_real(enclosed.lift_coefficient_upper)
        squared_error = mp.mpf(0)
        for channel in range(len(labels)):
            for row, exact in enumerate(exact_columns[channel]):
                distance = abs(
                    exact
                    - mp_complex(enclosed.system.update.columns[row, channel])
                )
                radius = mp_real(enclosed.column_radii[row, channel])
                assert distance <= radius
                squared_error += distance * distance
            for column, exact in enumerate(exact_rows[channel]):
                distance = abs(
                    exact
                    - mp_complex(enclosed.system.update.rows[channel, column])
                )
                radius = mp_real(enclosed.row_radii[channel, column])
                assert distance <= radius
                squared_error += distance * distance
        assert mp.sqrt(squared_error) <= mp_real(
            enclosed.matrix_error_frobenius_upper
        )
