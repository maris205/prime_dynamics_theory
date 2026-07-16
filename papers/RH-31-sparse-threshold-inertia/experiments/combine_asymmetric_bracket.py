"""Combine independently verified lower and upper shifted LDL certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


TARGET_FIELDS = (
    "sigma",
    "physical_dimension",
    "grushin_dimension",
    "threshold_dimension",
    "threshold",
    "threshold_factor",
    "exact_channel_enclosure",
    "threshold_matrix_nnz",
    "grushin_matrix_error_frobenius_upper",
    "threshold_transform_error_frobenius_upper",
    "lift_coefficient_lower",
    "lift_coefficient_upper",
    "power_of_two_scales",
    "pair_order",
)


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def selected_factorization(data: dict[str, object], label: str) -> dict[str, object]:
    rows = [
        row
        for row in data.get("shifted_factorizations", [])
        if row.get("label") == label
    ]
    if len(rows) != 1:
        raise ValueError(f"source must contain exactly one {label} factorization")
    return rows[0]


def shift_distance(
    data: dict[str, object], row: dict[str, object], label: str
) -> float:
    if "shift" in row:
        return float(row["shift"])
    distances = data.get("bracket_shifts")
    if isinstance(distances, dict) and label in distances:
        return float(distances[label])
    if "bracket_shift" in data:
        return float(data["bracket_shift"])
    raise ValueError(f"cannot recover the {label} shift distance")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minus-result", type=Path, required=True)
    parser.add_argument("--plus-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    minus_data = load(arguments.minus_result)
    plus_data = load(arguments.plus_result)
    for field in TARGET_FIELDS:
        if minus_data.get(field) != plus_data.get(field):
            raise ValueError(f"source target mismatch in {field}")
    if not bool(minus_data["exact_channel_enclosure"]):
        raise ValueError("the combined target must use exact channel enclosures")

    minus = selected_factorization(minus_data, "minus")
    plus = selected_factorization(plus_data, "plus")
    lower_shift = shift_distance(minus_data, minus, "minus")
    upper_shift = shift_distance(plus_data, plus, "plus")
    lower_error = float(minus["backward_error"]["total_error_upper"])
    upper_error = float(plus["backward_error"]["total_error_upper"])
    if lower_error >= lower_shift or upper_error >= upper_shift:
        raise ValueError("one shifted backward error does not fit inside its shift")
    for row in (minus, plus):
        if not (
            bool(row["row_permutation_is_identity"])
            and bool(row["column_permutation_is_identity"])
        ):
            raise ValueError("a shifted factorization used a nonidentity permutation")

    lower_positive = int(minus["backward_error"]["positive_pivots"])
    lower_negative = int(minus["backward_error"]["negative_pivots"])
    upper_positive = int(plus["backward_error"]["positive_pivots"])
    upper_negative = int(plus["backward_error"]["negative_pivots"])
    dimension = int(minus_data["grushin_dimension"])
    if (lower_positive, lower_negative) != (upper_positive, upper_negative):
        raise ValueError("the shifted exact LDL centres have different inertia")
    if (lower_positive, lower_negative) != (dimension, dimension):
        raise ValueError("the common inertia is not the threshold target")

    result = {
        "status": "rigorous_exact_target_asymmetric_threshold_inertia_certificate",
        **{field: minus_data[field] for field in TARGET_FIELDS},
        "inertia_bracket": {
            "admissible": True,
            "shift": None,
            "lower_shift": lower_shift,
            "upper_shift": upper_shift,
            "lower_shift_error_upper": lower_error,
            "upper_shift_error_upper": upper_error,
            "positive_count": lower_positive,
            "negative_count": lower_negative,
        },
        "shifted_factorizations": [minus, plus],
        "factor_seconds_total": float(minus["factor_seconds"])
        + float(plus["factor_seconds"]),
        "peak_memory_mb_upper_across_runs": max(
            float(minus_data["peak_memory_mb"]), float(plus_data["peak_memory_mb"])
        ),
        "source_results": {
            "minus": {
                "path": str(arguments.minus_result),
                "sha256": digest(arguments.minus_result),
            },
            "plus": {
                "path": str(arguments.plus_result),
                "sha256": digest(arguments.plus_result),
            },
        },
        "theorem": (
            "Weyl monotonicity with independent lower and upper shift distances"
        ),
    }
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
