"""Parallel multiprecision audit of the small postcritical remainder."""

from __future__ import annotations

import argparse
import csv
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import mpmath as mp

from postcritical_zeta import (
    component_weighted_trace_mp_range,
    multiprecision_constants,
)


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def compute_range(arguments: tuple[int, int, int, int]) -> str:
    length, start, stop, decimal_places = arguments
    value = component_weighted_trace_mp_range(
        length,
        start,
        stop,
        decimal_places=decimal_places,
    )
    return mp.nstr(value, decimal_places)


def trace_parallel(
    length: int,
    *,
    workers: int,
    decimal_places: int,
) -> mp.mpf:
    count = 1 << length
    task_count = min(count, 4 * workers)
    chunk_size = (count + task_count - 1) // task_count
    tasks = [
        (length, start, min(start + chunk_size, count), decimal_places)
        for start in range(0, count, chunk_size)
    ]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        pieces = list(executor.map(compute_range, tasks))
    with mp.workdps(decimal_places):
        return +mp.fsum(mp.mpf(piece) for piece in pieces)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimum-length", type=int, default=14)
    parser.add_argument("--maximum-length", type=int, default=20)
    parser.add_argument("--decimal-places", type=int, default=50)
    parser.add_argument(
        "--workers",
        type=int,
        default=min(64, os.cpu_count() or 1),
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.minimum_length < 1:
        raise ValueError("minimum length must be positive")
    if arguments.maximum_length < arguments.minimum_length:
        raise ValueError("maximum length must not be smaller than minimum length")
    constants = multiprecision_constants(arguments.decimal_places)
    rows: list[dict[str, object]] = []
    previous_remainder: mp.mpf | None = None
    for length in range(arguments.minimum_length, arguments.maximum_length + 1):
        print(
            f"parallel multiprecision trace {length}/{arguments.maximum_length}",
            flush=True,
        )
        trace = trace_parallel(
            length,
            workers=arguments.workers,
            decimal_places=arguments.decimal_places,
        )
        with mp.workdps(arguments.decimal_places):
            model = 1 - constants.lam ** (-length) + constants.lam ** (-2 * length)
            remainder = trace - model
            ratio = "" if previous_remainder is None else mp.nstr(
                remainder / previous_remainder, 30
            )
            rows.append(
                {
                    "two_step_length": length,
                    "fixed_point_count": 1 << length,
                    "multiprecision_trace": mp.nstr(trace, 45),
                    "perron_postcritical_model": mp.nstr(model, 45),
                    "postcritical_remainder": mp.nstr(remainder, 35),
                    "successive_remainder_ratio": ratio,
                    "decimal_places": arguments.decimal_places,
                    "workers": arguments.workers,
                }
            )
            previous_remainder = remainder
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / "multiprecision_postcritical_tail.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)


if __name__ == "__main__":
    main()
