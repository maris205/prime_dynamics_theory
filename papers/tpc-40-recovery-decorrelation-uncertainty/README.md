# TPC-40: Recovery-Decorrelation Uncertainty

This directory contains the manuscript

> **Recovery-Decorrelation Uncertainty at the Coherent Mobius Gate:
> Weighted Phase Frames, Sharp Fourier Frontiers, and Equality-Slice
> Rigidity**.

TPC-39 recovers the equality alias exactly with a minimal additive twist
bank, but its positive energy preserves the equality column and the
fixed-alias cross-row form. TPC-40 asks whether a second phase coordinate
can decorrelate the rows while retaining cheap universal recovery.

## Main results

For a unimodular phase bank `Phi`, positive measurement weights `w`, and
recovery coefficients `a`, define

```text
A = sum_j |a_j|^2 / w_j,
G = Phi^* diag(w) Phi.
```

If the bank universally recovers the coherent sum of `R` rows, then

```text
G >= A^{-1} 1 1^*,
A * lambda_max(G) >= R.
```

Consequently:

- Unit recovery amplification `A=1` is rigid: all row phase columns are
  identical, so no row decorrelation occurs.
- Complete decorrelation `G=I_R` costs at least `A=R`.
- For every integer `1 <= r <= R`, `r` selected rows of the `R`-point DFT,
  including the constant row, attain the sharp frontier
  `A=r`, `lambda_max(G)=R/r`.
- The optimum recovery amplification for a fixed bank is
  `1^* G^dagger 1`.
- An `L2` approximate recovery with relative error `epsilon` still obeys
  `A lambda_max(G) >= R(1-epsilon)^2`.
- Tensoring with the minimal `q=L+1` alias bank preserves `A`; on the zero
  alias slice its Gram is exactly `G`.
- Arbitrary coupled row-alias phases obey the same obstruction after
  restriction to the equality slice.
- Unimodular row phasing leaves the complete atomic diagonal invariant.

The physical conclusion is scoped: coefficient-blind positive phase
geometry cannot close the TPC-39 Mobius gate by itself. The paper does not
prove that the actual Mobius vector saturates the coherent mode. A
coefficient-specific signed dispersion theorem remains possible.

## Exact certificate

Run from this directory:

```text
python experiments/tpc40_certificate.py
python -O experiments/tpc40_certificate.py
```

The two commands produce byte-identical canonical JSON. The frozen run
passes `2,230,446` exact checks using integer, rational, modular-character,
and exact cyclotomic arithmetic.

Certificate digest:

```text
d925148e93bc0ecd57a3958bc6ffc0447f5116cfb0f188844e8b1c93b96020a0
```

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-40 proves a sharp recovery-decorrelation law for a declared universal
positive-energy method class. It does **not** prove a twist-stable physical
Mobius estimate, two- or four-Mobius cancellation, a breach of sieve parity,
a Hardy-Littlewood prime-pair asymptotic, or infinitely many twin primes.
