# Round-4 diagnostic receipt — current checker

Date: 2026-09-09. Read-only finite checks, not an arithmetic or asymptotic
certificate. All earlier diagnostics are retained; this is the current
checker output after realification checks and precise cutoff-field labels.

Both commands exited 0 with byte-identical stdout:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -O -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
```

The two finite matrix cases use a diagnostic shifted Gaussian, not the
source profile. Realification tests compare complex-band and real-basis
projectors/traces and the real symmetric quadratic restriction. At x=512
the cutoff is zero: its reported cutoff-subspace dimension does NOT mean
a strictly negative subspace or a valid asymptotic theorem threshold.
The rational one-scale check at x=8,000,000,000 does not materialize the
physical matrix and does not establish a uniform threshold for all larger x.

Complete stdout, both modes:

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
      "constant_rayleigh_diagnostic": -19.809395870070688,
      "boundary_expansion_abs_error": 1.399606873320082e-13,
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes",
      "realification_trace_abs_error": 1.788611381267425e-15,
      "real_cutoff_subspace_dimension_diagnostic": 1,
      "real_cutoff_threshold_diagnostic": 0.0
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
      "constant_rayleigh_diagnostic": -51.74435867848598,
      "boundary_expansion_abs_error": 6.022452254347028e-13,
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes",
      "realification_trace_abs_error": 3.552723585266596e-15,
      "real_cutoff_subspace_dimension_diagnostic": 15,
      "real_cutoff_threshold_diagnostic": 10.908333333333333
    }
  ],
  "lane_arithmetic_checks": {
    "semiprime_counts": {
      "1000": 12,
      "10000": 113,
      "100000": 878
    },
    "divisor_exponent_cases": 101
  },
  "one_sided_gram": [
    {
      "q": 3,
      "gram_abs_error": 1.7763568394002505e-15,
      "saturation_abs_error": 8.881784197001252e-16
    },
    {
      "q": 5,
      "gram_abs_error": 7.105427357601002e-15,
      "saturation_abs_error": 3.944304526105059e-31
    },
    {
      "q": 7,
      "gram_abs_error": 4.5456551220798253e-14,
      "saturation_abs_error": 4.440892098500626e-15
    },
    {
      "q": 11,
      "gram_abs_error": 2.1430679739491575e-13,
      "saturation_abs_error": 1.7763568394002505e-15
    },
    {
      "q": 17,
      "gram_abs_error": 9.987643287942924e-13,
      "saturation_abs_error": 7.105427357601002e-15
    },
    {
      "q": 31,
      "gram_abs_error": 5.012486647845312e-12,
      "saturation_abs_error": 3.552713678800501e-15
    }
  ],
  "smooth_partition": {
    "cases": 100,
    "sampled_points": 10100,
    "max_mass_error": 2.220446049250313e-16,
    "max_boundary_labels": 6
  },
  "growing_rank_sufficient_inequalities": {
    "scope": "ONE_SCALE_SUFFICIENT_INEQUALITIES_ONLY_NOT_UNIFORM_THRESHOLD",
    "x": 8000000000,
    "Q": 2000,
    "N": 4000000000,
    "shell_prime_count": 247,
    "H_floor_exact": 3154298,
    "J_exact": 498731,
    "d_exact": 997463,
    "k_exact": 997428,
    "C0_upper_rational": "841/49",
    "log_Q_lower_rational": "20/3",
    "D_star_at_least_tau_upper": true,
    "trace_cutoff_ratio_strictly_below_35": true,
    "physical_matrix_materialized": false
  }
}
```

