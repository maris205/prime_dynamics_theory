# TPC-7 finite diagnostics

`defect_shift_diagnostics.py` computes two finite checks:

1. the exact split `C_h = C_{h,<=D} + T_{h,>D}` (up to floating-point
   roundoff), with all positive shifts obtained by one FFT convolution;
2. the fraction of the `L^2` energy of `Lambda-1` captured by orthogonal
   projection onto selected periodic spaces.

Run the committed certificate and tests from this directory:

```bash
python defect_shift_diagnostics.py --output data/defect-shift-certificate.json
python -m unittest -v test_defect_shift_diagnostics.py
```

The cutoffs `D=X^theta` are finite-scale diagnostics. They are not a numerical
implementation of the unspecified, non-optimized logarithmic constant in the
theoretical Bombieri--Vinogradov cutoff, and the paper's theorems do not
depend on the observed quantiles.
