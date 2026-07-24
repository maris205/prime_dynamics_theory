# TPC-85: Literal zero-mode normalization barrier

This paper isolates the distinguished zero mode in the literal
TPC-32 matched shell and proves several exact normalization barriers.
The physical object is always formed with the same fixed nonzero
integer shift `h0` and the cutoff

```text
C = floor(J).
```

For the actual raw hard post-aggregation determinant coefficient,

```text
A_C(n) = sum of the complete signed matched atoms
         with content <= C and normalized determinant n,

Z_X = sum_n A_C(n),
D_X = sum_n |A_C(n)|^2.
```

The calibrated physical packet has two additional drift legs.  They
are returned only after the raw hard estimate and are charged in the
downstream loss ledger; they are not part of `A_C`, `Z_X`, or `D_X`.

The main unconditional results are:

- `A_C(0) = 0`, caused by the off-diagonal row mask, is a statement
  about the determinant bin `n = 0`; it does not imply the Fourier
  statement `Z_X = Ahat_C,q(0) = 0`.
- Under the strong physical no-wrap padding
  `q > 2 B_D Q + 2`,

  ```text
  A_C = A_C^circ + (Z_X/q) 1,
  D_X = ||A_C^circ||_2^2 + |Z_X|^2/q.
  Z_X = -sum_{r != 0} Ahat_C,q(r).
  ```

  Thus canonical centering alone extracts the unknown zero mode; it
  does not estimate it.  A coherent estimate for the complete
  nonzero-frequency sum is nevertheless an exact alternative route.
  For the literal support,

  ```text
  |Z_X|^2 <= #supp(A_C) D_X <= (q - 1) D_X.
  ```

  The unrestricted cyclic projection bound `q D_X` is therefore not
  called sharp for the physical coefficient.
- For a raw atomic measure with determinant-fiber masses `M_n`,
  conditional expectation onto the determinant sigma-algebra has
  energy

  ```text
  sum_n |A_C(n)|^2 / M_n,
  ```

  not the physical post-bin energy `D_X`.  It also preserves the
  total integral `Z_X`, so it cannot manufacture zero-mode
  cancellation.
- The cumulative content projector has `t = 1` term equal to the
  unrestricted full shell.  All `t > 1` terms reassemble to the
  negative large-content shell.  Hence content inversion does not
  center the zero mode.
- The exact affine-column interface contains correlations

  ```text
  mu(d0 + s r) mu(u0 + a r),
  s u0 - a d0 = h0 != 0,
  ```

  with growing slopes, possibly short fibers, the literal pair mask,
  and a complete outer reassembly.  This expands the raw hard shell;
  calibrated drift is a separate downstream term.
- A dyadic sign sequence gives an explicit black-box obstruction to
  deducing ordinary cancellation from logarithmically averaged
  cancellation.  The example is not multiplicative and is not
  claimed to obstruct a proof using Möbius-specific structure.

The comparison with theorems of Tao,
Matomäki--Radziwiłł--Tao, Tao--Teräväinen, and
Matomäki--Radziwiłł is quantifier-exact: fixed logarithmic forms,
averaged shifts, almost-all scales, and almost-all interval origins
do not automatically provide the literal fixed-`h0`, unweighted,
all-scale physical estimate.

Status: exact L0 identities, one explicit structure-free L0
countermodel, and L1 fixed-shift transfer barriers.
The paper proves no new L2 affine Möbius cancellation estimate, no
fixed-`h0` Chowla theorem, no determinant-energy lower bound, no
parity breach, no prime-pair lower bound, and no twin-prime result.
It does not specialize `h0` to `2`.

The full physical route retains the strict endpoint loss rule

```text
Lambda_phys < 1/400.
```

Equality or excess is a stop condition, not spare margin.

Build with:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The stable archive name is:

```text
literal-zero-mode-normalization-barrier.pdf
```
