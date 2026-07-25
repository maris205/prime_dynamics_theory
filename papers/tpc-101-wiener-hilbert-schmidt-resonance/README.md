# TPC-101: Wiener-to-Hilbert--Schmidt resonance transfer

Paper title:

> *Wiener-to-Hilbert--Schmidt Transfer for Multiplicative
> Resonance: Width-Sensitive Dispersion and the Long-Fiber Gate*

## Main result

Let `q` be an odd prime,

\[
E_H=\{\pm1,\ldots,\pm H\}\subset\mathbb F_q^\times,
\]

and

\[
\mathcal I_H(a,b)
=\sum_{\omega,r}a(\omega)b(r)1_{E_H}(r\omega).
\]

After removing the principal term, the exact norm of the linear
functional in `a` is

\[
\mathfrak S_H(b)^2
=\frac1{q-1}\sum_{\chi\ne\chi_0}
|\widehat{1_{E_H}}(\chi)|^2
|\widehat b(\bar\chi)|^2.
\]

Using only the Wiener mass of the fixed frequency weight gives

\[
|\mathcal R_H(a,b)|
\le
\|b\|_1
\sqrt{\frac{2H(q-1-2H)}{q-1}}\,
\|a^\circ\|_2.
\]

This replaces the previous worst-eigenvalue cost
`sqrt(q) log(q)` by the exact width factor

\[
g_q(H)=\sqrt{\frac{2H(q-1-2H)}{q-1}}.
\]

In particular:

- `g_q((q-1)/2)=0`; one- and two-point resolved fibers have only a
  principal resonance mode;
- for resolved length `N >= 3`,
  `g_q(H_q(N)) <= sqrt(2q/N)`;
- the literal centered gate becomes

  \[
  \sum_H g_{q_X}(H)\|a_H^\circ\|_2
  \ll X^{o(1)}Q_X^2,
  \]

  instead of the stronger uniform target
  `sum_H ||a_H^circ||_2 << X^{o(1)} Q_X^(3/2)`.

After TPC-100 separately returns the `q_X | u` subcarrier, combining
the new bound with its `q_X`-invertible census gives
width-weighted diagonal and cross-cell gates. An abstract transfer
theorem further shows that the invertible diagonal gate follows from
the principal gate if the maximum opened-atom weight is `X^{o(1)}`.
That atomic cap is isolated as a separate literal obligation; it is
not assumed proved. At the maximally literal TPC-100 resolution the
fine cells are singletons, so this is an atom-cap transfer, not an
intra-cell dispersion gain; all distinct-atom collisions remain in
the cross-cell term.

## Claim boundary

The fixed-group norm theorem is L0. Its crosswalk to the corrected
frequency-free TPC-99 census is L1. No growing fixed-`h0` affine
Mobius cancellation theorem, parity breakthrough, prime-pair lower
bound, or twin-prime conclusion is claimed.

## Reproduce

```powershell
python experiments/tpc101_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`wiener-hilbert-schmidt-resonance.pdf`
