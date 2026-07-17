"""Archive and exact-partition utilities for the RH-33 atlas."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def center_identifier(record: dict[str, object]) -> str:
    if "center_id" in record:
        return str(record["center_id"])
    return f"arc_{int(record['source_arc']):05d}"


def verify_leaf_ledger(path: Path) -> dict[str, object]:
    with Path(path).open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    intervals = sorted(
        (
            Fraction(int(row["start_numerator"]), int(row["turn_denominator"])),
            Fraction(int(row["end_numerator"]), int(row["turn_denominator"])),
        )
        for row in rows
    )
    exact_partition = bool(
        intervals
        and intervals[0][0] == 0
        and intervals[-1][1] == 1
        and all(
            left[1] == right[0]
            for left, right in zip(intervals, intervals[1:])
        )
    )
    closed = [row for row in rows if row["status"] == "closed"]
    products = [float(row["neumann_product_upper"]) for row in closed]
    ratios = [float(row["budget_ratio_upper"]) for row in closed]
    transported = [float(row["transported_inverse_upper"]) for row in closed]
    budgets = [float(row["budget_lower"]) for row in closed]
    return {
        "leaf_count": len(rows),
        "closed_leaf_count": len(closed),
        "unresolved_leaf_count": len(rows) - len(closed),
        "exact_rational_partition_verified": exact_partition,
        "maximum_neumann_product_upper": max(products, default=None),
        "maximum_budget_ratio_upper": max(ratios, default=None),
        "minimum_transported_inverse_upper": min(transported, default=None),
        "maximum_transported_inverse_upper": max(transported, default=None),
        "minimum_budget_lower": min(budgets, default=None),
        "maximum_budget_lower": max(budgets, default=None),
        "used_center_ids": sorted({row["center_id"] for row in closed}),
    }
