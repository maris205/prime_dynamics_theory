# TPC-38: Target-Coupled CRT Projectors and the Identity Bucket

This directory contains the manuscript

> **Target-Coupled CRT Projectors and the Identity Bucket: Shifted Jacobi
> Grams, Alias Coherence, and the Equality-Recovery Obstruction**.

TPC-38 analyzes the target-coupled shifted-fiber continuation isolated in
TPC-37. On the regular physical subpacket `(N,M)=1`, zero extension handles
nonunit `N+F`; on the doubly-unit subset, it proves that the moving target is
exactly diagonalized by the ratio `(N+F)/N` in the multiplicative character
basis, and computes the
resulting target Gram and synthesis spectra, and localizes the congruence
completion to the joint aliases `F=kM`. It then proves that controlling this
completed alias sum does not, by itself, recover the original `F=0` output.

## Main results

- Every regular-target CRT coordinate face is an exact target-coupled
  character projector.
- Fixed-target Parseval becomes a shifted Jacobi Gram when the target moves.
- The exact fixed-`F` target collision multiplicity is
  `prod_{q_i | F}(q_i-1)`; for `q_i` of order `J`, its scales are
  `1,J,J^2,J^3`.
- The full target-synthesis operator has squared norm asymptotic to `J^3`;
  the proper operator has squared norm asymptotic to `J^2`.
- Recombining full and proper faces cancels every nonjoint ghost exactly and
  leaves `O(K_X)` joint aliases, where `K_X=X^(1/400+o(1))` at the endpoint.
- Character orthogonality is blind on that identity bucket. Under a moving-
  shift column estimate, coefficient-free Cauchy loses the exact finite
  alias count `K_B`, of endpoint order `K_X`.
- The recombined alias sum is a congruence completion, not the original
  equality output. Two opposite alias columns make both completed full and
  proper outputs vanish while leaving the `F=0` column arbitrary.
- A full alias-Gram bound controls `F=0` directly through its zero-column
  diagonal entry, and already implies the stronger `Q^2 J` column bound. A
  target-scale route needs a separate nonzero-alias
  aggregate estimate or another exact recovery mechanism.
- A hereditary all-field operator theorem is strictly stronger than the two
  prescribed-field estimates proposed in TPC-37: its terminal restriction
  would imply a diagonal-scale affine-Mobius/four-Mobius operator estimate.

## Exact certificate

Run from this directory:

~~~text
python experiments/tpc38_certificate.py
python -O experiments/tpc38_certificate.py
~~~

The certificate uses exact integer and rational arithmetic only. It checks
the face recombination, fixed-target norms, target Grams and spectra,
ratio-fiber multiplicities, determinant strata, the sharp joint-alias
coherence witness, and the equality-nonrecoverability witness.

## Build

~~~text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
~~~

## Claim boundary

TPC-38 does **not** prove a positive physical equality-recovery estimate, the moving-shift diagonal
input, the joint-alias Gram estimate, the full physical orbit gate, a Mobius
autocorrelation estimate, affine Chowla, a breach of sieve parity, a
Hardy-Littlewood prime-pair asymptotic, or infinitely many twin primes. Its
main output is an exact spectral reduction, a correction of the logical
gate, and a sharp method boundary.
