# RH-212: intrinsic quartic normalization audit

Sixteen small-noise levels are resolved on both physical channels, with eight
levels predeclared for the normalization comparison.  Raw, determinant-radius,
and centered-RMS coefficient flows are compared without levelwise fitting.
Neither intrinsic normalization contracts the adjacent flow: the mean
fine-relative coefficient errors are `0.10661`, `0.19322`, and `0.16592`,
respectively.  Raw coefficients remain the most stable tested representation.

The frozen endpoint ledger is reused by RH-213--RH-220.  Run
`python experiments/run_normalization_audit.py` to rebuild it.
