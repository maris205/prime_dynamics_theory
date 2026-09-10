# Round-3 diagnostic receipt

The extended checker additionally covers the exact complete Kloosterman Gram
identity, centered one-sided saturation, constructive partition mass/support,
and boundary expansion/norm inequality on arbitrary diagnostic vectors.
No finite computation proves the smooth derivative bounds or asymptotic theorem.
The Gaussian kernel remains diagnostic only, not the source profile.

Both commands exited 0; stdout is byte-identical:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python -O -B research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/check_diagnostics.py
```

Complete stdout (both modes):

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
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes"
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
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes"
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
  }
}
```

## Later round-3 extension: exact one-scale sufficient inequalities

The same commands were rerun after adding the growing-rank prerequisite check;
both exited 0 with byte-identical stdout. It uses rational upper bounds from
pi < 22/7 and log(2) > 2/3, exact prime enumeration through 4000, and integer
32nd-power isolation of the physical H. It checks one scale x=8,000,000,000;
it does not furnish a uniform asymptotic threshold or materialize the physical
four-billion-dimensional matrix. Earlier outputs above are historical snapshots
of the earlier checker version, not the final current stdout.

Complete current stdout (both modes):

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
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes"
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
      "boundary_vectors_scope": "arbitrary real diagnostic vectors, not literal lanes"
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

