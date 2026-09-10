# Diagnostic receipt

Date: 2026-09-09. Finite debugging only; no arithmetic/asymptotic certificate.

Commands (both exit 0, byte-identical stdout):

```sh
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
env PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -O -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
```

No repository files are written by the program. Explicit runtime checks survive optimization.
The two matrix examples use a fixed shifted Gaussian diagnostic kernel, not the source
compact-profile kernel. x=512 has two zero-energy rows, which illustrates why the proof's
eventual lower-bound threshold must not be replaced by a small-x assertion.

Raw stdout:

```json
{
  "scope": "FINITE_DIAGNOSTICS_ONLY_NO_ARITHMETIC_OR_ASYMPTOTIC_CREDIT",
  "files_written": [],
  "exact_projection_entries": 662,
  "emission": {
    "packets": 80,
    "max_abs_error": 1.847752688483104e-13
  },
  "operators": [
    {
      "x": 512,
      "N": 256,
      "Q": 7.999999999999999,
      "H": 59.9733642915296,
      "primes": [
        11,
        13
      ],
      "errors": {
        "hermitian": 0.0,
        "diagonal_deletion": 0.0,
        "projection_decomposition": 1.7763568394002505e-15,
        "row_energy": 2.2737367544323206e-13
      },
      "zero_row_energies": 2,
      "operator_norm_diagnostic": 76.24660868046868,
      "constant_rayleigh_diagnostic": -19.809395870070688
    },
    {
      "x": 1000,
      "N": 500,
      "Q": 9.999999999999998,
      "H": 93.0572040929699,
      "primes": [
        11,
        13,
        17,
        19
      ],
      "errors": {
        "hermitian": 0.0,
        "diagonal_deletion": 0.0,
        "projection_decomposition": 7.105427357601002e-15,
        "row_energy": 9.094947017729282e-13
      },
      "zero_row_energies": 0,
      "operator_norm_diagnostic": 119.41847014388311,
      "constant_rayleigh_diagnostic": -51.74435867848598
    }
  ],
  "lane_arithmetic_checks": {
    "semiprime_counts": {
      "1000": 12,
      "10000": 113,
      "100000": 878
    },
    "divisor_exponent_cases": 101
  }
}
```

