"""Re-evaluate archived LDL backward bounds under a stated operation count."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from threshold_inertia.rounding import gamma, upper_add, upper_multiply  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--operation-factor", type=int, default=24)
    arguments = parser.parse_args()
    factor = int(arguments.operation_factor)
    if factor < 24:
        raise ValueError("the complex-operation factor must be at least 24")

    source_bytes = arguments.input.read_bytes()
    result = json.loads(source_bytes)
    rows = result.get("shifted_factorizations", [])
    if not rows:
        raise ValueError("the source contains no shifted factorization")
    for row in rows:
        backward = row["backward_error"]
        dimension = int(backward["matrix_dimension"])
        elimination = upper_multiply(
            gamma(factor * dimension + 64),
            float(backward["absolute_lu_product_frobenius_upper"]),
        )
        total = upper_add(
            float(backward["input_assembly_error_upper"]),
            elimination,
            float(backward["ldl_conversion_error_upper"]),
        )
        backward["gaussian_elimination_backward_error_upper"] = elimination
        backward["total_error_upper"] = total
        backward["elimination_operation_factor"] = factor

    result["derived_from"] = {
        "path": str(arguments.input),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
        "original_operation_factor": 32,
        "rebound_operation_factor": factor,
    }
    if len(rows) == 1:
        row = rows[0]
        label = str(row["label"])
        shift = float(row.get("shift", result["bracket_shifts"][label]))
        backward = row["backward_error"]
        if (
            float(backward["total_error_upper"]) < shift
            and bool(row["row_permutation_is_identity"])
            and bool(row["column_permutation_is_identity"])
        ):
            result["status"] = "rigorous_one_sided_shifted_ldl_certificate"
        else:
            result["status"] = "archived_factorization_rebound_not_admissible"
    elif len(rows) == 2:
        by_label = {str(row["label"]): row for row in rows}
        if set(by_label) != {"minus", "plus"}:
            raise ValueError("a two-sided archive must contain minus and plus rows")
        shifts = {}
        for label, row in by_label.items():
            if "shift" in row:
                shifts[label] = float(row["shift"])
            elif "bracket_shifts" in result:
                shifts[label] = float(result["bracket_shifts"][label])
            elif "inertia_bracket" in result:
                key = "lower_shift" if label == "minus" else "upper_shift"
                shifts[label] = float(result["inertia_bracket"][key])
            else:
                shifts[label] = float(result["bracket_shift"])
        minus_bound = by_label["minus"]["backward_error"]
        plus_bound = by_label["plus"]["backward_error"]
        same_inertia = (
            int(minus_bound["positive_pivots"])
            == int(plus_bound["positive_pivots"])
            and int(minus_bound["negative_pivots"])
            == int(plus_bound["negative_pivots"])
        )
        admissible = bool(
            same_inertia
            and float(minus_bound["total_error_upper"]) < shifts["minus"]
            and float(plus_bound["total_error_upper"]) < shifts["plus"]
            and all(
                bool(row["row_permutation_is_identity"])
                and bool(row["column_permutation_is_identity"])
                for row in rows
            )
        )
        result["inertia_bracket"] = {
            "admissible": admissible,
            "shift": (
                shifts["minus"]
                if shifts["minus"] == shifts["plus"]
                else None
            ),
            "lower_shift": shifts["minus"],
            "upper_shift": shifts["plus"],
            "lower_shift_error_upper": float(
                minus_bound["total_error_upper"]
            ),
            "upper_shift_error_upper": float(plus_bound["total_error_upper"]),
            "positive_count": (
                int(minus_bound["positive_pivots"]) if same_inertia else -1
            ),
            "negative_count": (
                int(minus_bound["negative_pivots"]) if same_inertia else -1
            ),
        }
        dimension = int(result["grushin_dimension"])
        if (
            admissible
            and int(minus_bound["positive_pivots"]) == dimension
            and int(minus_bound["negative_pivots"]) == dimension
        ):
            result["status"] = (
                "rigorous_exact_target_asymmetric_threshold_inertia_certificate"
            )
        else:
            result["status"] = "archived_factorization_rebound_not_admissible"
    rendered = json.dumps(result, indent=2, sort_keys=True)
    print(rendered)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(rendered + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
