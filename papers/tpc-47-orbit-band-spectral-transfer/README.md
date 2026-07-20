# TPC-47: Orbit-Band Projection and Mesoscopic Spectral Transfer

This directory contains the source, exact finite certificate, and compiled
paper

> *Orbit-Band Projection and Mesoscopic Spectral Transfer for an
> Actual-Coefficient Determinant Sector*.

## Main result

The paper zero-extends the literal physical orbit coordinate to
`ell^2(Z)` and applies, on every opposite-row and residual-label fiber, the
norm-one Fourier projector onto the full residue comb

```text
B_Omega^(H0) = { beta : dist(beta, H0^(-1) Z) <= Omega }.
```

The physical residual label `s = d(m) r` is left unchanged. For an orbit
profile with coefficient half-bandwidth `Sigma/J`, its canonical low core
has the exact shift-spectral gap

```text
(Omega + Sigma/J)/M_- < ||alpha||_T
                            < (H0^(-1) - Omega - Sigma/J)/M_+.
```

The complete literal coefficient field is split only after signed
reassembly. Its projected frozen shift family has arbitrary-power leakage
on every suitably shrunken subinterval of the same gap. At the inherited
TPC endpoint

```text
Omega = X^(1/400+o(1))/J,     Sigma = X^(1/400+o(1)),
```

this gives, for every `0 < epsilon < 33/200`,

```text
X^(-399/400+epsilon) <= ||alpha||_T
                           <= X^(-267/400-epsilon).
```

For one scalar non-orbit fiber and a physical window of `N` orbit times,
the compressed projector has the exact trace

```text
tr(E_I^* Pi_Omega E_I) = 2 H0 N Omega = X^(1/400+o(1)).
```

The projection is injective on nonzero finitely supported orbit vectors,
but an explicit finite-difference family proves that it need not retain
any uniform fraction of their norm. Thus the theorem produces a nonzero
sector with growing time-bandwidth trace, not a mass lower bound for the
actual arithmetic vector.

## Physical-interface boundary

At the physical intercept `h0`, the field in the theorem is the literal
actual-coefficient residual synthesis `-sum_p U x_p` from the
low-sign-averaged residual Gram route. It is not the native affine physical
Gram face. Away from `h0`, the shift variable belongs to a frozen-coefficient
algebraic family. The paper does not prove control of the complementary
orbit bands, atomic normalization, alias unfolding, a fixed-shift TPC
estimate, a parity-barrier breach, or the twin-prime conjecture.

## Exact certificate

Run from this directory:

```powershell
python experiments/tpc47_certificate.py
```

The deterministic certificate uses only the Python standard library. It
performs **28,428 exact checks**. The principal finite model is on
`Z/60Z` over `F_601`; a rational interval calculation independently checks
the sinc-comb Gram boundary. The cyclic model is an exact finite analogue,
not a numerical proof of the continuous asymptotic theorem.

Expected integrity values:

```text
canonical payload digest
9e01380fae0d684d96b6ed23e5f99b4ba8359667d6182459e36eeaeb1f66fdba

normalized source SHA-256
719fd93d61b75ade58d4817b0b8701343060cadb87c9c9f4aad38c521ad8e356

JSON SHA-256
6b0d0c41b335e437affd5d06f28495f09655e265144253f196d4af9396b17e19
```

The generated report is
[`experiments/tpc47_certificate.json`](experiments/tpc47_certificate.json).

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The final paper is [`main.pdf`](main.pdf). The source is split across
`main.tex`, `references.bib`, and `sections/`.

## Relation to the sequence

TPC-46 isolated four remaining transfer gates. TPC-47 crosses the first
gate on one canonical projected actual-residual sector. The natural next
step is an all-band resonance-tube square-function or large-sieve theorem
that reassembles mutually orthogonal orbit bands without assuming that the
single low band captures a fixed fraction of the vector.
