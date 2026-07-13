# Rough-pair parity diagnostics

This directory contains a deterministic numerical experiment for the
prime/semiprime transition of rough shifted pairs. It is a diagnostic for the
survivor-to-prime remainder, not evidence for a twin-prime lower bound.

## Mathematical convention

For each starting value

```text
n in [X, 2X)
```

the program examines `n` and `n+h`. The shifted coordinate is allowed to lie in
`[2X, 2X+h)`, so the factored range is `[X, 2X+h)`.

For a supplied exponent `theta`, set

```text
U = 2X+h,  y = floor(U^theta),  P^-(coordinate) > y.
```

The program requires `1/3 < theta < 1/2` and checks `y^3 > U`. Consequently,
every `y`-rough coordinate in the factored range has either one or two prime
factors counted with multiplicity. Each surviving pair therefore lies in
exactly one of the sectors

```text
PP, PS, SP, SS,
```

where `P` means prime and `S` means semiprime, including prime squares. If
`A` denotes the total number of surviving pairs and

```text
L10 = sum lambda(n),
L01 = sum lambda(n+h),
L11 = sum lambda(n) lambda(n+h),
```

over those pairs, the program verifies the exact integer identity

```text
N_PP = (A - L10 - L01 + L11) / 4.
```

It aborts rather than silently introducing an `Omega >= 3` sector if the
four-sector assumptions fail.

## Build

The implementation uses only the C++ standard library. On Linux or WSL:

```bash
g++ -O3 -std=c++17 -march=native rough_pair_diagnostics.cpp -o rough_pair_diagnostics
```

The source also builds without `-march=native`, which is preferable for a
portable published binary.

Run the independent regression test after building:

```bash
python3 smoke_test.py --binary ./rough_pair_diagnostics
```

It compares two block sizes and independently recomputes all summary counts
and every factor-bin row by trial division.

## Run

A small deterministic run is:

```bash
./rough_pair_diagnostics \
  --x 1000000 \
  --h 2 \
  --theta 0.34,0.38,0.42,0.46,0.49 \
  --block 262144 \
  --factor-bins 32 \
  --output test_x1e6_h2
```

The two outputs are:

- `test_x1e6_h2_summary.csv`: the four sectors, the three Liouville twists,
  the reconstructed `N_PP`, and two exact consistency errors;
- `test_x1e6_h2_factor_bins.csv`: least-prime-factor histograms for the
  semiprime coordinate in `PS`, `SP`, and both coordinates in `SS`.

The factor coordinate is

```text
alpha = log(P^-(m)) / log(2X+h),  0 <= alpha <= 1/2.
```

Values close to the cutoff exponent are the relatively unbalanced factor
range; values close to `1/2` are the balanced range relevant to Type-II
diagnostics.

All counts are exact integers. There is no random seed and no sampling error.
The `elapsed_seconds` field is informational and is the only
machine-dependent output.

## Plot

The plotting program uses only the Python standard library and writes an SVG:

```bash
python plot_diagnostics.py \
  --summary test_x1e6_h2_summary.csv \
  --bins test_x1e6_h2_factor_bins.csv \
  --theta 0.34,0.38,0.42,0.46,0.49 \
  --output test_x1e6_h2.svg
```

The upper panel gives stacked four-sector shares. The lower panel is a
least-factor heatmap on one common row-share color scale. SVG cells contain
exact counts and shares as tooltips.

## Algorithm and practical range

The program performs a segmented complete factorization. For each block it
stores a 64-bit residual, a 64-bit smallest prime factor, and an 8-bit
`Omega`, plus vector overhead. A block of `2^24` starting positions uses well
below 1 GB. The approximate work is `O(X log log X)` and memory is
`O(block size)`.

On a 32 GB workstation, memory is not the limiting resource. Complete dyadic
runs through about `X=10^9` are realistic in optimized C++, while `X=10^10`
is primarily a CPU-time decision and should first be benchmarked on a shorter
run. The current implementation is CPU-oriented; a GPU is not required.

For production runs, record the source commit, compiler version, full command,
and SHA-256 hashes of both CSV files. Run at least one small case with two
different block sizes: the count columns and factor histograms must agree
exactly.

## Interpretation boundary

The experiment can locate contamination by factor size and can falsify a
specific proposed finite-scale cancellation law. Convergence of sector shares,
small inversion error (which is an algebraic identity), or visually random
heatmaps does not imply a uniform Type-II estimate and does not imply the
existence of infinitely many prime pairs.
