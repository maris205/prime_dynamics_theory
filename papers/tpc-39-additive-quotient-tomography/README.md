# TPC-39: Additive Quotient Tomography of the Identity Bucket

This directory contains the manuscript

> **Additive Quotient Tomography of the Identity Bucket: Minimal Fourier
> Recovery, Folded Parseval, and the Twist-Stable Mobius Gate**.

TPC-38 showed that three-modulus CRT completion leaves a joint-alias sum
rather than the original equality column. TPC-39 constructs the missing exact
linear recovery map on the additive quotient of that identity bucket.

## Main results

- If `L=floor(B/M)` and `q=L+1`, then `qM>B` and
  `1_{M|F} q^{-1} sum_nu e(nu F/(qM))=1_{F=0}` throughout `|F|<=B`.
- Exactly `L+1` regular-polygon twists recover the zero alias with unit
  normalized recovery amplification. No arbitrary phase bank with at most
  `L` nodes can recover that coefficient universally.
- The minimal-bank energy obeys an exact Hilbert-valued folded Parseval
  identity. Its normalized Gram spectrum is `2` (`L` times), `1` (once), and
  `0` (`L` times); the kernel contains only folded antisymmetric alias pairs.
- Positive minimally sampled exact rules are rigid: their weights are equal
  and their nodes form a rotated regular polygon.
- Pure linear combinations of divisibility indicators supported at moduli no
  larger than the determinant window cannot recover exact equality.
- The terminal row-alias map is injective, and under the inherited
  deterministic multiplier ledger its full atomic diagonal is already
  bounded at the inherited target scale.
- The remaining conditional gate is a square-average estimate for the actual
  recombined twisted outputs. The twist preserves scalar face masses, but its
  energy still contains the original equality column and genuine two- and
  four-Mobius correlations.

## Exact certificate

Run from this directory:

~~~text
python experiments/tpc39_certificate.py
python -O experiments/tpc39_certificate.py
~~~

The certificate uses exact integer and rational arithmetic. Roots of unity
are evaluated only through exact finite cyclic orthogonality. It checks zero
recovery, minimal quotient size, folded Parseval, the full collision-Gram
spectrum, partial-bank counterexamples, divisibility-indicator no-go cases,
and the distinct exact variance identities for continuous Haar phases, a
collision-free finite grid, and the folded minimal grid.

## Build

~~~text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
~~~

## Claim boundary

TPC-39 proves an exact and optimally amplified equality-recovery projector. It
does **not** prove the twist-stable physical Mobius estimate needed to bound
the recovered output, a uniform alias-column estimate, affine Chowla, a
breach of sieve parity, a Hardy-Littlewood prime-pair asymptotic, or infinitely
many twin primes.
