"""Build analytic and exact-stored weighted Riesz-projector ledgers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from flint import arb, ctx


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH6 = PAPERS / "RH-6-continuum-spectral-double-limits"
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH36 = PAPERS / "RH-36-nested-grid-physical-count"
RH37 = PAPERS / "RH-37-iterated-dyadic-physical-count"
RH38 = PAPERS / "RH-38-dyadic-haar-block-decay"
RH39 = PAPERS / "RH-39-uniform-gaussian-cutoff-bridge"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def upper_float(value: arb) -> float:
    return float(np.nextafter(float(value.upper()), np.inf))


def lower_float(value: arb) -> float:
    return float(np.nextafter(float(value.lower()), -np.inf))


def transformed_rows(
    values: np.ndarray,
    mode: str,
    scalars: np.ndarray | None = None,
) -> list[list[arb]]:
    array = np.asarray(values)
    if mode == "identity":
        row_count = array.shape[0]
    else:
        if array.shape[0] % 2:
            raise ValueError("paired transforms require an even row count")
        row_count = array.shape[0] // 2
    scalar_values = (
        np.ones(array.shape[1], dtype=np.float64)
        if scalars is None
        else np.asarray(scalars, dtype=np.float64)
    )
    rows: list[list[arb]] = []
    for row in range(row_count):
        output = []
        for column in range(array.shape[1]):
            if mode == "identity":
                value = arb(float(array[row, column]))
            else:
                even = arb(float(array[2 * row, column]))
                odd = arb(float(array[2 * row + 1, column]))
                if mode == "average":
                    value = (even + odd) / 2
                elif mode == "difference":
                    value = (even - odd) / 2
                elif mode == "sum":
                    value = even + odd
                elif mode == "pair_difference":
                    value = even - odd
                else:
                    raise ValueError(mode)
            output.append(value * arb(float(scalar_values[column])))
        rows.append(output)
    return rows


def concatenate_rows(*parts: list[list[arb]]) -> list[list[arb]]:
    if not parts or len({len(part) for part in parts}) != 1:
        raise ValueError("all factor parts must have the same row count")
    return [
        [entry for part in parts for entry in part[row]]
        for row in range(len(parts[0]))
    ]


def gram(rows: list[list[arb]]) -> list[list[arb]]:
    rank = len(rows[0])
    result = [[arb(0) for _ in range(rank)] for _ in range(rank)]
    for row in rows:
        for left in range(rank):
            for right in range(left, rank):
                result[left][right] += row[left] * row[right]
    for left in range(rank):
        for right in range(left):
            result[left][right] = result[right][left]
    return result


def frobenius_ball(
    left_rows: list[list[arb]], right_rows: list[list[arb]]
) -> arb:
    left_gram = gram(left_rows)
    right_gram = gram(right_rows)
    rank = len(left_gram)
    square = arb(0)
    for left in range(rank):
        for right in range(rank):
            square += left_gram[left][right] * right_gram[right][left]
    return square.sqrt()


def block_factor_rows(
    coarse_right: np.ndarray,
    coarse_left: np.ndarray,
    coarse_values: np.ndarray,
    fine_right: np.ndarray,
    fine_left: np.ndarray,
    fine_values: np.ndarray,
) -> dict[str, tuple[list[list[arb]], list[list[arb]]]]:
    fine_average = transformed_rows(fine_right, "average", fine_values)
    fine_difference = transformed_rows(fine_right, "difference", fine_values)
    fine_left_sum = transformed_rows(fine_left, "sum")
    fine_left_difference = transformed_rows(fine_left, "pair_difference")
    coarse_weighted = transformed_rows(coarse_right, "identity", -coarse_values)
    coarse_left_rows = transformed_rows(coarse_left, "identity")
    return {
        "coarse_consistency": (
            concatenate_rows(fine_average, coarse_weighted),
            concatenate_rows(fine_left_sum, coarse_left_rows),
        ),
        "coarse_to_detail": (fine_difference, fine_left_sum),
        "detail_to_coarse": (fine_average, fine_left_difference),
        "detail_block": (fine_difference, fine_left_difference),
    }


def block_intervals(
    coarse: tuple[np.ndarray, np.ndarray, np.ndarray],
    fine: tuple[np.ndarray, np.ndarray, np.ndarray],
) -> dict[str, dict[str, object]]:
    factors = block_factor_rows(*coarse, *fine)
    result = {}
    for name, (left_rows, right_rows) in factors.items():
        value = frobenius_ball(left_rows, right_rows)
        result[name] = {
            "frobenius_lower": lower_float(value),
            "frobenius_upper": upper_float(value),
            "spectral_norm_upper": upper_float(value),
            "arb_frobenius_ball": str(value),
        }
    return result


def peripheral_tuple(data, prefix: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    return (
        np.asarray(data[f"{prefix}_right_modes"]),
        np.asarray(data[f"{prefix}_left_modes"]),
        np.asarray(data[f"{prefix}_peripheral_values"]),
    )


def biorthogonality_interval(
    right: np.ndarray, left: np.ndarray
) -> dict[str, object]:
    rank = right.shape[1]
    square = arb(0)
    entries = []
    for row in range(rank):
        row_entries = []
        for column in range(rank):
            value = arb(0)
            for index in range(right.shape[0]):
                value += arb(float(left[index, row])) * arb(
                    float(right[index, column])
                )
            if row == column:
                value -= 1
            square += value * value
            row_entries.append(str(value))
        entries.append(row_entries)
    defect = square.sqrt()
    return {
        "frobenius_defect_upper": upper_float(defect),
        "two_norm_defect_upper": upper_float(defect),
        "arb_defect_ball": str(defect),
        "entry_balls": entries,
    }


def interval_ratio(
    numerator: dict[str, object], denominator: dict[str, object]
) -> dict[str, float]:
    return {
        "lower": float(numerator["frobenius_lower"])
        / float(denominator["frobenius_upper"]),
        "upper": float(numerator["frobenius_upper"])
        / float(denominator["frobenius_lower"]),
    }


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def main() -> None:
    first_snapshot = (
        RH36 / "results" / "nested_grid_snapshot_sigma_1e-02.npz"
    )
    second_snapshot = (
        RH37 / "results" / "second_dyadic_fine_object_sigma_1e-02.npz"
    )
    previous_precision = ctx.prec
    ctx.prec = 224
    try:
        with np.load(first_snapshot) as first, np.load(second_snapshot) as second:
            level_data = {
                "2048": peripheral_tuple(first, "coarse"),
                "4096": peripheral_tuple(first, "fine"),
                "8192": peripheral_tuple(second, "fine"),
            }
            first_blocks = block_intervals(level_data["2048"], level_data["4096"])
            second_blocks = block_intervals(level_data["4096"], level_data["8192"])
            biorthogonality = {
                label: biorthogonality_interval(values[0], values[1])
                for label, values in level_data.items()
            }
            parity = [arb(float(level_data[label][2][1])) for label in ("2048", "4096", "8192")]
            first_increment = parity[1] - parity[0]
            second_increment = parity[2] - parity[1]
            increment_ratio = second_increment / first_increment
            first_richardson = (4 * parity[1] - parity[0]) / 3
            second_richardson = (4 * parity[2] - parity[1]) / 3
            richardson_difference = abs(second_richardson - first_richardson)
            convergence = {
                "first_increment_ball": str(first_increment),
                "second_increment_ball": str(second_increment),
                "increment_ratio_lower": lower_float(increment_ratio),
                "increment_ratio_upper": upper_float(increment_ratio),
                "first_richardson_ball": str(first_richardson),
                "second_richardson_ball": str(second_richardson),
                "richardson_disagreement_upper": upper_float(richardson_difference),
            }
    finally:
        ctx.prec = previous_precision

    ratios = {
        name: interval_ratio(second_blocks[name], first_blocks[name])
        for name in first_blocks
    }
    exponents = {
        "coarse_consistency": 2,
        "coarse_to_detail": 1,
        "detail_to_coarse": 1,
        "detail_block": 2,
    }
    renormalized = {}
    for label, mesh, blocks in (
        ("2048_to_4096", 1.0 / 2048.0, first_blocks),
        ("4096_to_8192", 1.0 / 4096.0, second_blocks),
    ):
        renormalized[label] = {
            name: {
                "lower": float(record["frobenius_lower"]) / mesh ** exponents[name],
                "upper": float(record["frobenius_upper"]) / mesh ** exponents[name],
            }
            for name, record in blocks.items()
        }
    pilot_path = ROOT / "results" / "weighted_projector_pilot_sigma_1e-02.json"
    pilot = load(pilot_path)
    maximum_residual = max(
        float(value)
        for level in pilot["levels"].values()
        for mode in level["residuals"].values()
        for value in mode.values()
    )
    maximum_biorthogonal = max(
        float(record["two_norm_defect_upper"])
        for record in biorthogonality.values()
    )
    ledger_gate = bool(
        ratios["coarse_consistency"]["upper"] < 0.251
        and ratios["detail_block"]["upper"] < 0.251
        and ratios["coarse_to_detail"]["upper"] < 0.501
        and ratios["detail_to_coarse"]["upper"] < 0.501
        and maximum_biorthogonal < 1.0e-13
    )
    payload = {
        "status": (
            "analytic_conditional_weighted_riesz_bridge_with_exact_stored_peripheral_ledger"
            if ledger_gate
            else "weighted_riesz_projector_ledger_incomplete"
        ),
        "scope": (
            "analytic full-kernel Nyström weighted Riesz terms plus exact stored "
            "binary64 peripheral factors at sigma=1e-2"
        ),
        "evidence_levels": {
            "analytic_theorem": (
                "exact weighted-Riesz resolvent stability and second-order simple-branch theorem"
            ),
            "stored_factor_ledger": (
                "224-bit Arb enclosures of exact stored-factor Frobenius identities"
            ),
            "spectral_isolation_audit": "floating leading-spectrum and eigen-residual diagnostic",
        },
        "analytic_statements": {
            "weighted_riesz_definition": (
                "Q(K)=K Pi=(2 pi i)^-1 integral_Gamma z(z-K)^-1 dz"
            ),
            "resolvent_lipschitz": (
                "||Q(A)-Q(B)|| <= length(Gamma)/(2 pi) max|z| M_A M_B ||A-B||"
            ),
            "nystrom_simple_cluster": (
                "smooth simple isolated nonzero branches give ||Q_h-Q_h^circle||_2=O(h^2)"
            ),
            "discrete_row_normalization": (
                "positive C^2 raw kernels preserve the weighted-term O(h^2) bridge"
            ),
            "perron_status": "unconditional for the full positive folded Gaussian kernel",
            "parity_status": (
                "full-kernel bridge conditional on a simple isolated continuum negative "
                "resonance; cutoff transfer additionally needs a uniform Euclidean contour resolvent"
            ),
            "adaptive_cutoff_transfer": (
                "the RH-39 O(h^2) Markov bridge transfers to Q under a uniform contour resolvent"
            ),
        },
        "arb_precision_bits": 224,
        "exact_stored_frobenius_blocks": {
            "2048_to_4096": first_blocks,
            "4096_to_8192": second_blocks,
        },
        "exact_stored_frobenius_ratios": ratios,
        "renormalized_exact_stored_frobenius": renormalized,
        "exact_stored_biorthogonality": biorthogonality,
        "maximum_exact_stored_biorthogonality_upper": maximum_biorthogonal,
        "parity_convergence": convergence,
        "floating_isolation_audit": {
            "minimum_parity_to_observed_bulk_radial_gap": min(
                float(level["parity_to_observed_bulk_radial_gap"])
                for level in pilot["levels"].values()
            ),
            "maximum_eigen_residual": maximum_residual,
            "maximum_projector_two_norm": max(
                float(level["projector_singular_values"][0])
                for level in pilot["levels"].values()
            ),
            "maximum_weighted_term_two_norm": max(
                float(level["weighted_term_singular_values"][0])
                for level in pilot["levels"].values()
            ),
        },
        "stored_ledger_closed": ledger_gate,
        "pilot": {
            "path": str(pilot_path.relative_to(ROOT)),
            "sha256": sha256_file(pilot_path),
        },
        "dependencies": {
            "rh6_continuum_nystrom_manuscript": repository_entry(RH6 / "main.tex"),
            "rh24_peripheral_mode_builder": repository_entry(
                RH24 / "experiments" / "run_contour_feshbach_audit.py"
            ),
            "rh36_factor_snapshot": repository_entry(first_snapshot),
            "rh36_factor_metadata": repository_entry(first_snapshot.with_suffix(".json")),
            "rh37_fine_factor_snapshot": repository_entry(second_snapshot),
            "rh37_fine_factor_metadata": repository_entry(
                RH37 / "results" / "second_dyadic_snapshot_sigma_1e-02.json"
            ),
            "rh38_decay_certificate": repository_entry(
                RH38 / "results" / "dyadic_haar_block_decay_certificate.json"
            ),
            "rh39_cutoff_certificate": repository_entry(
                RH39 / "results" / "uniform_gaussian_cutoff_bridge_certificate.json"
            ),
        },
        "limitations": [
            "The Perron part is analytic and unconditional, but continuum simplicity and isolation of the negative parity resonance are not validated here.",
            "The stored factors are exact binary64 data, while their claim to be exact Riesz modes remains based on floating residuals and spectral diagnostics.",
            "The Arb ledger certifies low-rank Frobenius identities, not the full sparse eigensolver computation.",
            "Only two dyadic refinements are stored; they do not prove an all-level constant without the continuum isolation hypothesis.",
            "Binary64 construction of the underlying sparse Markov matrices is not interval-enclosed.",
            "No zero-noise, zeta-zero, Hilbert-Polya, or Riemann-hypothesis claim is made.",
        ],
    }
    output = ROOT / "results" / "weighted_riesz_projector_bridge_certificate.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    if not ledger_gate:
        raise RuntimeError("the exact stored peripheral ledger did not close")


if __name__ == "__main__":
    main()
