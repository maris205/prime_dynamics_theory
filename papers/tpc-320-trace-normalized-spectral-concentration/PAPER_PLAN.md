# TPC-320 paper plan

## Title

**Scale-invariant spectral concentration and participation growth for a literal
prime-shell operator**

## Parent and research question

TPC-319 showed that every tested Ky Fan mass grows before source-count
normalization and falls after division by the number of source columns.  That
identity is a useful firewall, but it leaves open whether the spectral shape
itself changes.  TPC-320 asks:

1. If the Gram spectrum is normalized by its own trace, do the top-\(k\)
   cumulative shares still move monotonically across the finite scale panel?
2. Do stable rank and participation rank provide a compatible, amplitude-free
   diagnostic?
3. Does an entropy control expose a false inference from any one scalar
   concentration statistic?

The literal operator, source intervals, shell rule, height, and exponents are
all inherited unchanged.  This is one dynamical-system family.

## Planned contribution

For a positive-semidefinite Gram matrix with eigenvalues
\(\lambda_1\geq\cdots\geq\lambda_N\), define

\[
C_k=\frac{\sum_{j\leq k}\lambda_j}{\operatorname{tr}G},\qquad
r_{\rm st}=\frac{\operatorname{tr}G}{\lambda_1},\qquad
r_{\rm part}=\frac{\operatorname{tr}(G)^2}{\operatorname{tr}(G^2)}.
\]

The paper will prove the exact scalar-invariance identities and certify the
finite \(C_k\) comparisons using dual shell-order accumulation, dual spectral
paths, and an outward quotient interval.  Stable rank, participation rank, and
normalized entropy remain explicitly labeled finite observations.

## Claim discipline

- PROVED_EXACT: scalar invariance, spectral-measure definitions, and finite
  PSD identities.
- NUMERICALLY_CERTIFIED_FINITE: 24 rows, five \(k\)-values, 120 intervals,
  and 80 strict concentration decreases under the declared guard.
- NUMERICAL_OBSERVATION: 16/16 stable-rank and participation-rank growth
  transitions, metric ranges, and mixed entropy behavior.
- OPEN: any uniform concentration law, asymptotic exponent, signed
  prime-shell reassembly, arithmetic cancellation, fixed-power credit, and
  twin-prime endpoint.

## Follow-up selection rule

If the trace-normalized trend survives, the next project should test whether
the full spectral profile is stable across shell choices.  If it does not,
the finite obstruction should be recorded before any arithmetic claim.
