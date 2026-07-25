# TPC-94: Exact-Content Progression Normalization and Resonance

This note audits the progression selected by the exact-content
condition in TPC-93.

Main exact results:

- the raw pair after `t = tau + B z` has determinant `B h0`;
- extracting the forced factor `U = B V` restores determinant `h0`;
- in a general noncanonical extension, the remaining first-form
  content is exactly `H = gcd(B,h0)`, and the primitive determinant
  is `h0/H`;
- on literal canonical TPC-32 support, `(b,h0)=1`, hence `H=1`;
- squareful `B` branches vanish, while squarefree branches retain
  the exact Mobius sign and coprimality mask;
- the source orientation `epsilon_theta` is retained on both
  polarizations, and every class `r mod q_X` uses its unique
  least-absolute signed lift in characters modulo `c q_X`;
- the additive phase has an exact reduced conductor with a prime
  modulus gap: at most `c` or at least `q_X`;
- literal common-target provenance forces `b | Omega`, so the actual
  conductor collapses further to exactly `1` or `q_X`, and every
  nonconstant low-conductor sector is empty;
- short, constant, low-conductor, resonant, and generic sectors are
  partitioned without overlap or deletion; and
- exceptional sectors are charged by reconstruction-multiplier mass,
  not by frequency count.

The algebra and partition are L0.  Their attachment to the literal
TPC-93 packet is an L1 corollary obtained by importing the established
inverse ledger in TPC-93, Theorem 3.3, Corollary 3.4, and Theorem 3.5
(Complete Decorated Affine Export), including its explicit inverse
provenance and multiplicity reconstruction.  No L2 cancellation or
prime-pair theorem is claimed.

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The stable archived PDF name is:

`exact-content-resonance-ledger.pdf`

## Reproducible finite certificate

Run from this directory:

```text
python experiments/tpc94_certificate.py
```

The deterministic certificate performs `2,275,219` exact integer
checks:

- `205,885` progression-normalization and two-stage Mobius checks;
- `1,989,680` two-polarization phase-splitting checks;
- `57,954` signed-lift and conductor checks;
- `21,600` exact progression-length and integer-threshold checks; and
- `100` sector-boundary checks.

It also records the abstract lift-ambiguity witness
`(q,c,Omega)=(3,2,1)`, for which representatives `2` and `-1`
would give conductors `3` and `6` without the signed-lift convention.
These are finite identity regressions only.  They do not test
asymptotic cancellation or independently re-run the upstream TPC-93
source--child inverse certificate.
