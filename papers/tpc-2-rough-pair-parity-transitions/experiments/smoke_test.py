#!/usr/bin/env python3
"""Independent small-range regression test for rough_pair_diagnostics."""

import argparse
import csv
import math
from pathlib import Path
import subprocess
import tempfile


THETAS = "0.34,0.38,0.42,0.46,0.49"
SUMMARY_KEYS = (
    "A",
    "N_PP",
    "N_PS",
    "N_SP",
    "N_SS",
    "L10",
    "L01",
    "L11",
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--binary", default="./rough_pair_diagnostics")
    return parser.parse_args()


def factor_data(n):
    original = n
    omega = 0
    spf = 0
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            if spf == 0:
                spf = divisor
            while n % divisor == 0:
                n //= divisor
                omega += 1
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        if spf == 0:
            spf = n
        omega += 1
    if original < 2:
        return 0, 0
    return spf, omega


def run(binary, prefix, block):
    command = [
        binary,
        "--x",
        "10000",
        "--h",
        "2",
        "--theta",
        THETAS,
        "--block",
        str(block),
        "--factor-bins",
        "16",
        "--output",
        str(prefix),
    ]
    completed = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "diagnostic executable failed:\n{}\n{}".format(
                completed.stdout, completed.stderr
            )
        )


def read_rows(path):
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def independent_counts(y, facts):
    sectors = [0, 0, 0, 0]
    twists = [0, 0, 0]
    for n in range(10000, 20000):
        left = facts[n - 10000]
        right = facts[n + 2 - 10000]
        if min(left[0], right[0]) <= y:
            continue
        left_prime = left[1] == 1
        right_prime = right[1] == 1
        sector = (0 if left_prime else 2) + (0 if right_prime else 1)
        sectors[sector] += 1
        lambda_left = -1 if left[1] % 2 else 1
        lambda_right = -1 if right[1] % 2 else 1
        twists[0] += lambda_left
        twists[1] += lambda_right
        twists[2] += lambda_left * lambda_right
    return [sum(sectors)] + sectors + twists


def factor_bin(spf, upper, bins):
    index = int(math.log(spf) / math.log(upper) * bins / 0.5)
    return min(max(index, 0), bins - 1)


def independent_histograms(y, facts, bins=16, upper=20002):
    histograms = {
        "PS_right": [0] * bins,
        "SP_left": [0] * bins,
        "SS_left": [0] * bins,
        "SS_right": [0] * bins,
    }
    for n in range(10000, 20000):
        left = facts[n - 10000]
        right = facts[n + 2 - 10000]
        if min(left[0], right[0]) <= y:
            continue
        left_prime = left[1] == 1
        right_prime = right[1] == 1
        if left_prime and not right_prime:
            histograms["PS_right"][factor_bin(right[0], upper, bins)] += 1
        elif not left_prime and right_prime:
            histograms["SP_left"][factor_bin(left[0], upper, bins)] += 1
        elif not left_prime and not right_prime:
            histograms["SS_left"][factor_bin(left[0], upper, bins)] += 1
            histograms["SS_right"][factor_bin(right[0], upper, bins)] += 1
    return histograms


def main():
    args = parse_args()
    binary = str(Path(args.binary).resolve())
    facts = [factor_data(n) for n in range(10000, 20002)]
    with tempfile.TemporaryDirectory(prefix="rough-pair-smoke-") as temp:
        root = Path(temp)
        prefix_a = root / "block4096"
        prefix_b = root / "block777"
        run(binary, prefix_a, 4096)
        run(binary, prefix_b, 777)
        summary_a = read_rows(str(prefix_a) + "_summary.csv")
        summary_b = read_rows(str(prefix_b) + "_summary.csv")
        if len(summary_a) != len(summary_b):
            raise AssertionError("summary row count differs by block size")
        for row_a, row_b in zip(summary_a, summary_b):
            for key in SUMMARY_KEYS + ("theta", "y", "inversion_error", "sector_sum_error"):
                if row_a[key] != row_b[key]:
                    raise AssertionError("block-size mismatch in {}".format(key))
            expected = independent_counts(int(row_a["y"]), facts)
            observed = [int(row_a[key]) for key in SUMMARY_KEYS]
            if observed != expected:
                raise AssertionError(
                    "independent mismatch for theta={}: observed={}, expected={}".format(
                        row_a["theta"], observed, expected
                    )
                )
            if int(row_a["inversion_error"]) != 0 or int(row_a["sector_sum_error"]) != 0:
                raise AssertionError("exact identity error is nonzero")

        bins_a = Path(str(prefix_a) + "_factor_bins.csv").read_text(encoding="utf-8")
        bins_b = Path(str(prefix_b) + "_factor_bins.csv").read_text(encoding="utf-8")
        if bins_a != bins_b:
            raise AssertionError("factor histograms differ by block size")

        factor_rows = read_rows(str(prefix_a) + "_factor_bins.csv")
        expected_by_y = {}
        for row in factor_rows:
            y = int(row["y"])
            if y not in expected_by_y:
                expected_by_y[y] = independent_histograms(y, facts)
            series = row["series"]
            bin_index = int(row["bin_index"])
            expected = expected_by_y[y][series][bin_index]
            observed = int(row["count"])
            if observed != expected:
                raise AssertionError(
                    "independent histogram mismatch for y={}, series={}, bin={}: "
                    "observed={}, expected={}".format(
                        y, series, bin_index, observed, expected
                    )
                )

    print(
        "smoke test passed: independent counts and histograms, "
        "exact inversion, and block invariance"
    )


if __name__ == "__main__":
    main()
