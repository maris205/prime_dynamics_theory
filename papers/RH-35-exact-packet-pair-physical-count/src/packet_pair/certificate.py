"""Exact dyadic packet Grams and outward scalar transfer certificates."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

from flint import arb, ctx
import numpy as np


def _upper_float(value: arb) -> float:
    return math.nextafter(float(value.upper()), math.inf)


def _lower_float(value: arb) -> float:
    return math.nextafter(float(value.lower()), -math.inf)


def _fraction_sqrt_upper(value: Fraction, *, precision: int) -> float:
    if value < 0:
        raise ValueError("a squared norm must be nonnegative")
    if value == 0:
        return 0.0
    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        enclosure = arb(value.numerator) / arb(value.denominator)
        return _upper_float(enclosure.sqrt().upper())
    finally:
        ctx.prec = previous_precision


@dataclass(frozen=True)
class ExactRealGram:
    """An exact real Gram matrix and rigorous small-matrix norm bounds."""

    rows: int
    columns: int
    entries: tuple[tuple[Fraction, ...], ...]
    frobenius_upper: float
    spectral_upper: float
    factor_spectral_upper: float

    def serializable_entries(self) -> list[list[dict[str, int]]]:
        return [
            [
                {
                    "numerator": value.numerator,
                    "denominator": value.denominator,
                }
                for value in row
            ]
            for row in self.entries
        ]


def exact_real_gram(
    left: np.ndarray,
    right: np.ndarray,
    *,
    subtract_identity: bool = False,
    precision: int = 256,
) -> ExactRealGram:
    """Form an exact Gram-like product from stored real binary64 arrays."""

    first = np.asarray(left)
    second = np.asarray(right)
    if np.iscomplexobj(first) or np.iscomplexobj(second):
        raise ValueError("the RH-35 exact Gram path expects real stored arrays")
    if first.ndim != 2 or second.ndim != 2:
        raise ValueError("exact Gram inputs must be matrices")
    if first.shape[1] != second.shape[0]:
        raise ValueError("exact Gram shapes do not align")
    rows, inner = first.shape
    columns = second.shape[1]
    if subtract_identity and rows != columns:
        raise ValueError("identity subtraction requires a square product")

    left_fractions = [
        [Fraction.from_float(float(first[row, index])) for index in range(inner)]
        for row in range(rows)
    ]
    right_fractions = [
        [
            Fraction.from_float(float(second[index, column]))
            for column in range(columns)
        ]
        for index in range(inner)
    ]
    entries: list[tuple[Fraction, ...]] = []
    for row in range(rows):
        output_row = []
        for column in range(columns):
            value = sum(
                (
                    left_fractions[row][index]
                    * right_fractions[index][column]
                    for index in range(inner)
                ),
                Fraction(0),
            )
            if subtract_identity and row == column:
                value -= 1
            output_row.append(value)
        entries.append(tuple(output_row))
    exact_entries = tuple(entries)
    frobenius_square = sum(
        (value * value for row in exact_entries for value in row),
        Fraction(0),
    )
    row_sum_upper = max(
        (sum((abs(value) for value in row), Fraction(0)) for row in exact_entries),
        default=Fraction(0),
    )
    column_sum_upper = max(
        (
            sum(
                (abs(exact_entries[row][column]) for row in range(rows)),
                Fraction(0),
            )
            for column in range(columns)
        ),
        default=Fraction(0),
    )
    spectral_square_upper = row_sum_upper * column_sum_upper
    product_spectral_upper = _fraction_sqrt_upper(
        spectral_square_upper, precision=precision
    )
    factor_spectral_upper = _fraction_sqrt_upper(
        Fraction.from_float(product_spectral_upper), precision=precision
    )
    return ExactRealGram(
        rows=rows,
        columns=columns,
        entries=exact_entries,
        frobenius_upper=_fraction_sqrt_upper(
            frobenius_square, precision=precision
        ),
        spectral_upper=product_spectral_upper,
        factor_spectral_upper=factor_spectral_upper,
    )


@dataclass(frozen=True)
class PairCorrectionMajorant:
    """Global exact-pair and stored-block perturbation bounds."""

    pair_defect_upper: float
    corrected_gram_inverse_upper: float
    synthesis_upper: float
    analysis_upper: float
    analysis_correction_upper: float
    external_correction_upper: float
    physical_on_packet_upper: float
    physical_on_external_upper: float
    stored_direct_upper: float
    stored_forcing_upper: float
    stored_observation_upper: float
    direct_correction_upper: float
    forcing_correction_upper: float
    observation_correction_upper: float
    complement_correction_upper: float
    corrected_forcing_upper: float


def pair_correction_majorant(
    *,
    pair_defect_upper: float,
    synthesis_upper: float,
    analysis_upper: float,
    physical_on_packet_upper: float,
    physical_on_external_upper: float,
    stored_direct_upper: float,
    stored_forcing_upper: float,
    stored_observation_upper: float,
    precision: int = 256,
) -> PairCorrectionMajorant:
    """Build the structured norm majorant for the exact dual correction."""

    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        h = arb(float(pair_defect_upper)).upper()
        v = arb(float(synthesis_upper)).upper()
        w = arb(float(analysis_upper)).upper()
        x = arb(float(physical_on_packet_upper)).upper()
        y = arb(float(physical_on_external_upper)).upper()
        direct = arb(float(stored_direct_upper)).upper()
        forcing = arb(float(stored_forcing_upper)).upper()
        observation = arb(float(stored_observation_upper)).upper()
        if not h < 1:
            raise ValueError("the exact packet Gram is not certified invertible")
        gram_inverse = (1 / (1 - h)).upper()
        delta_w = (gram_inverse * h * w).upper()
        delta_q = (v * delta_w).upper()
        delta_d = (delta_w * x).upper()
        delta_c = (v * delta_w * x).upper()
        delta_e = (
            delta_w * y
            + direct * delta_w
            + delta_w * x * delta_w
        ).upper()
        delta_b = (
            v * delta_w * y
            + forcing * delta_w
            + v * delta_w * x * delta_w
        ).upper()
        corrected_forcing = (forcing + delta_c).upper()
        return PairCorrectionMajorant(
            pair_defect_upper=float(pair_defect_upper),
            corrected_gram_inverse_upper=_upper_float(gram_inverse),
            synthesis_upper=float(synthesis_upper),
            analysis_upper=float(analysis_upper),
            analysis_correction_upper=_upper_float(delta_w),
            external_correction_upper=_upper_float(delta_q),
            physical_on_packet_upper=float(physical_on_packet_upper),
            physical_on_external_upper=float(physical_on_external_upper),
            stored_direct_upper=float(stored_direct_upper),
            stored_forcing_upper=float(stored_forcing_upper),
            stored_observation_upper=float(stored_observation_upper),
            direct_correction_upper=_upper_float(delta_d),
            forcing_correction_upper=_upper_float(delta_c),
            observation_correction_upper=_upper_float(delta_e),
            complement_correction_upper=_upper_float(delta_b),
            corrected_forcing_upper=_upper_float(corrected_forcing),
        )
    finally:
        ctx.prec = previous_precision


@dataclass(frozen=True)
class LeafTransferCertificate:
    """Complement and Feshbach correction bounds on one inherited leaf."""

    stored_complement_inverse_upper: float
    projected_feshbach_inverse_upper: float
    stored_feshbach_computed_ratio_upper: float
    stored_feshbach_remainder_coefficient_upper: float
    stored_feshbach_full_ratio_upper: float
    stored_feshbach_inverse_upper: float
    complement_neumann_product_upper: float
    corrected_complement_inverse_upper: float
    corrected_feshbach_difference_upper: float
    feshbach_rouche_product_upper: float
    complement_homotopy_denominator_lower: float
    feshbach_homotopy_denominator_lower: float
    complement_homotopy_certified: bool
    feshbach_homotopy_certified: bool


def certify_leaf_transfer(
    majorant: PairCorrectionMajorant,
    *,
    stored_complement_inverse_upper: float,
    projected_feshbach_inverse_upper: float,
    stored_feshbach_computed_ratio_upper: float,
    stored_feshbach_remainder_coefficient_upper: float,
    precision: int = 256,
) -> LeafTransferCertificate:
    """Certify corrected complement and Feshbach homotopies on one leaf."""

    previous_precision = ctx.prec
    try:
        ctx.prec = int(precision)
        complement_inverse = arb(
            float(stored_complement_inverse_upper)
        ).upper()
        projected_inverse = arb(
            float(projected_feshbach_inverse_upper)
        ).upper()
        computed_ratio = arb(
            float(stored_feshbach_computed_ratio_upper)
        ).upper()
        remainder_coefficient = arb(
            float(stored_feshbach_remainder_coefficient_upper)
        ).upper()
        delta_b = arb(majorant.complement_correction_upper).upper()
        delta_c = arb(majorant.forcing_correction_upper).upper()
        delta_d = arb(majorant.direct_correction_upper).upper()
        delta_e = arb(majorant.observation_correction_upper).upper()
        forcing_corrected = arb(majorant.corrected_forcing_upper).upper()
        observation = arb(majorant.stored_observation_upper).upper()
        stored_ratio = (
            computed_ratio + complement_inverse * remainder_coefficient
        ).upper()
        if not stored_ratio < 1:
            raise ValueError("the inherited stored Feshbach gate is open")
        stored_feshbach_inverse = (
            projected_inverse / (1 - stored_ratio)
        ).upper()
        complement_product = (complement_inverse * delta_b).upper()
        complement_closed = bool(complement_product < 1)
        if complement_closed:
            corrected_complement_inverse = (
                complement_inverse / (1 - complement_product)
            ).upper()
            feshbach_difference = (
                delta_d
                + delta_e
                * corrected_complement_inverse
                * forcing_corrected
                + observation
                * corrected_complement_inverse
                * delta_b
                * complement_inverse
                * forcing_corrected
                + observation * complement_inverse * delta_c
            ).upper()
            feshbach_product = (
                stored_feshbach_inverse * feshbach_difference
            ).upper()
            feshbach_closed = bool(feshbach_product < 1)
        else:
            corrected_complement_inverse = arb("inf")
            feshbach_difference = arb("inf")
            feshbach_product = arb("inf")
            feshbach_closed = False
        complement_denominator = (
            (1 - complement_product).lower()
            if complement_closed
            else arb(0)
        )
        feshbach_denominator = (
            (1 - feshbach_product).lower() if feshbach_closed else arb(0)
        )
        return LeafTransferCertificate(
            stored_complement_inverse_upper=float(
                stored_complement_inverse_upper
            ),
            projected_feshbach_inverse_upper=float(
                projected_feshbach_inverse_upper
            ),
            stored_feshbach_computed_ratio_upper=float(
                stored_feshbach_computed_ratio_upper
            ),
            stored_feshbach_remainder_coefficient_upper=float(
                stored_feshbach_remainder_coefficient_upper
            ),
            stored_feshbach_full_ratio_upper=_upper_float(stored_ratio),
            stored_feshbach_inverse_upper=_upper_float(
                stored_feshbach_inverse
            ),
            complement_neumann_product_upper=_upper_float(
                complement_product
            ),
            corrected_complement_inverse_upper=_upper_float(
                corrected_complement_inverse
            ),
            corrected_feshbach_difference_upper=_upper_float(
                feshbach_difference
            ),
            feshbach_rouche_product_upper=_upper_float(feshbach_product),
            complement_homotopy_denominator_lower=(
                max(0.0, _lower_float(complement_denominator))
                if complement_closed
                else 0.0
            ),
            feshbach_homotopy_denominator_lower=(
                max(0.0, _lower_float(feshbach_denominator))
                if feshbach_closed
                else 0.0
            ),
            complement_homotopy_certified=complement_closed,
            feshbach_homotopy_certified=feshbach_closed,
        )
    finally:
        ctx.prec = previous_precision
