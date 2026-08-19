#!/usr/bin/env python3
"""Print the central TPC-213 finite coupling diagnostics."""

from __future__ import annotations

import sys


PROJECT = __import__("pathlib").Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "code"))

from profile_cross_gram import build_certificate  # noqa: E402


def main() -> int:
    certificate = build_certificate()
    joint = certificate["joint_lift"]
    print(f"joint_lift_rows={joint['row_count']}")
    print(f"joint_lift_columns={joint['column_count']}")
    print(f"joint_lift_rank={joint['rank']}")
    print(f"codomain_dependency_dimension={joint['codomain_dependency_dimension']}")
    for row in certificate["cross_gram_cases"]:
        print(
            "cross_gram="
            f"{row['left']}:{row['right']} "
            f"value={row['cross_gram']} "
            f"nonzero={row['cross_gram_nonzero']} "
            f"normalized_squared={row['normalized_cross_gram_squared']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
