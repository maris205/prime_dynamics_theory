# Citation Verification

## Verified local evidence

The local source
`papers/tpc-61-cofactor-exposure-parity-kernel/sections/cofactor-ladder.tex`
states at lines 118--120 that the prime coordinate lies in one reduced residue
class and that Brun--Titchmarsh saves a logarithm. Its proposition at lines
124--167 invokes the interval form of the theorem and cites
`MontgomeryVaughan2007`.

The local bibliography entry at lines 65--71 is:

```bibtex
@book{MontgomeryVaughan2007,
  author = {Hugh L. Montgomery and Robert C. Vaughan},
  title = {Multiplicative Number Theory I: Classical Theory},
  publisher = {Cambridge University Press},
  address = {Cambridge},
  year = {2007}
}
```

TPC-239 copies this metadata exactly and cites no other work.

## Citation boundary

The repository contains neither a local scan of the book nor a page-level
theorem locator. Therefore the following are locally verified:

- the TPC-61 source's explicit use of interval Brun--Titchmarsh;
- its attribution to Montgomery and Vaughan;
- the bibliography metadata above;
- the exact TPC-239 specialization
  `pi(2Q;h,b)<=4Q/[phi(h)log(2Q/h)]` supplied by the task source lock.

Page-level verification against the printed book is not claimed. This boundary
does not turn the finite computation into citation evidence.
