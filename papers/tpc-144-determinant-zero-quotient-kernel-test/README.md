# TPC-144: Determinant/zero quotient kernel test

This paper gives an exact simultaneous-lift criterion for the
determinant quotient `Q_D` and the ordered zero-mode quotient `Q_Z`.
For surjective finite maps, an isomorphism `J` with

```text
J Q_D = Q_Z
```

exists exactly when the two kernels are equal.  A literal relabeling
requires an allowed metadata-preserving output permutation for which
the complete weighted rows agree.  Equal zero kernels can still fail
that test (for example, the identity and a non-permutation shear).

The full-space kernel criterion assumes surjectivity.  If the
occurrence map `M` is not onto, the TPC-124 interface is tested on
`Ran(M)` and the kernels of the restricted quotients must be compared
with their codomains replaced by their images.

The theorem is executable on a completed occurrence archive.  The
current archive has no cut-to-occurrence lift and therefore supplies
neither literal quotient:

```text
H1.frontier_QD_totality = NOT_TESTABLE
H1.frontier_QZ_totality = NOT_TESTABLE
H1.frontier_QD_QZ_intertwining = NOT_TESTABLE
```

The scoped stop applies only to deriving these quotients from the
current cut schema or from equality of one scalar sum.  It does not
stop an augmented occurrence route.

Run:

```bash
python experiments/tpc144_quotient_kernel_audit.py
python experiments/tpc144_quotient_kernel_audit.py --check
```

Synthetic matrices test surjectivity, the finite theorem, the
scalar-counterexample, and the same-kernel/nonliteral-relabeling
counterexample.  They are explicitly separated from the actual
`NOT_TESTABLE` manifest.
