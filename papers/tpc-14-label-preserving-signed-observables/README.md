# TPC-14: Label-preserving signed observables

**Paper:** *Label-Preserving Signed Observables after Radial Completion: A
Fixed-Shift Coprime-Shell Law, Uniform Short-Shift Masks, and the Type-II
Gate*

TPC-13 already established joint-label energy and character-phase first
moments. This paper evaluates one fixed-shift aggregate and extends the
short-shift first moment to arbitrary bounded signed label masks.

## Main results

- The exact `k=1` GCD-Mellin shell is evaluated at every fixed nonzero
  shift. If

  ```text
  beta_h = product_(p|h) (1 - p/(p^2-p+1)),
  ```

  then

  ```text
  K_h(X) = (1/zeta(2)-beta_h) X I0(W) log X + O_h,W(X).
  ```

  This uses the published unitary-divisor Titchmarsh theorem. The shell
  still aggregates all primitive orientations and does not isolate the
  endpoint `b=1`.

- At `H >= X^(2/15+epsilon)`, subject to all translated targets remaining
  at height comparable with `X`, the translated prime residual has
  arbitrary logarithmic saving in `l2` over all product centers. This
  controls the complete dual ball of bounded, shift-independent
  GCD-Mellin masks uniformly for `D >= 1`; taking `D=1` includes the
  endpoint, individual radial layers, rays, and signed unions.

- The endpoint mask gives a signed mean prime-pair covariance theorem and
  the expected raw prime-pair average over a growing shift window. The
  even-shift statement uses the correct parity-conditioned center.

- After recentering on the factorized target variable, arbitrary bounded
  masks of Vaughan's hard packet have an explicit short-shift averaged
  model. This is not a fixed-shift Type-II estimate.

- An exact local-data minimax theorem, a square-root divisor-information
  dichotomy, and a prime/semiprime witness show what a balanced bilinear
  row detects that local sieve data miss.

The paper proves no fixed-shift prime-pair asymptotic, twin-prime lower
bound, new level of distribution, or breach of sieve parity.

## Reproduction

From this directory:

    pdflatex main.tex
    bibtex main
    pdflatex main.tex
    pdflatex main.tex
    python experiments/signed_label_certificate.py
    python -m unittest experiments.test_signed_label_certificate

The finite certificate checks exact algebra, masks, unitary-divisor
aggregation, Vaughan packets, and local null witnesses. It does not test
the imported asymptotic theorems.
