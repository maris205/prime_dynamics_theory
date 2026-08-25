# TPC-256 citation verification

## External arithmetic theorem

The only nontrivial external arithmetic input is the classical prime number
theorem with the de la Vallée Poussin zero-free-region remainder

```text
pi(y)=Li(y)+O(y exp(-c sqrt(log y))).
```

Standard references listed in `paper/references.bib` are:

- Harold Davenport, *Multiplicative Number Theory*, third edition, Springer,
  2000.
- Hugh L. Montgomery and Robert C. Vaughan, *Multiplicative Number Theory I:
  Classical Theory*, Cambridge University Press, 2007.
- Henryk Iwaniec and Emmanuel Kowalski, *Analytic Number Theory*, AMS, 2004.

The repository already source-locks this exact strength in
`papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md`.
TPC-256 uses it only for fixed relative intervals, not a shrinking interval.

## Derived prime-power summatory statement

The paper does not cite a separate theorem for

```text
F(y)=sum_(n<=y)Lambda(n)/log(n).
```

It derives

```text
F(y)=pi(y)+sum_(k>=2)pi(y^(1/k))/k
```

directly from prime powers.  The `k>=2` tail is
`O(sqrt(y)log y)` and is absorbed by the source-locked PNT remainder.

## Internal artifact citations

| Citation key | Frozen artifact | Use in TPC-256 |
|---|---|---|
| `v35` | proper-factor unit-ratio reduction | literal beta and divisor envelope |
| `v43` | proper-factor Poisson transference | combined centered row and first moment |
| `v51` | compensated pair dilation | literal scales and beta formula |
| `v59` | polarized local BDH scalar | literal operator |
| `vtop` | top-prime direct energy floor | weighted-prime shell formula |
| `tpc233` | critical-depth obstruction source lock | strong PNT provenance |
| `tpc253` | source-frozen rank midpoint | real-clock ordered rank and Haar vector |
| `tpc255` | exact adjoint diagonal/boundary compiler | exact four-lane decomposition |

All eight frozen repository blobs are hash-checked by both executable
implementations.  Internal artifacts are cited as repository research
reports, not represented as peer-reviewed external publications.

## Citation firewall

- No cited source is claimed to prove the final TPC-256 theorem verbatim.
- The explicit constants `log(32/27)/sqrt(2)` and
  `9log(32/27)/(2sqrt(2))` are derived in this paper.
- The `1/48` separation is derived from the frozen exponents; it is not a
  quoted literature claim.
- Finite numerical convergence is not used as a citation substitute.
