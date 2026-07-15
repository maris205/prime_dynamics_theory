# TPC-18 — Möbius-Tail Determinant Dispersion

Paper title:

> *Two Quadraticizations of a Möbius Tail: LCM Cutoff Return, Generic
> Row Determinants, and Nonprimitive Endpoint Collapse*

## Main results

- Derives a `TT*` theory directly for the symmetric TPC-17 Möbius tail;
  it does not splice in TPC-17's different asymmetric packet.
- Proves the exact lcm transform
  `beta_I(k)^2 = sum_{q|k} Gamma_I(q)`. Since `V^2 <= R`, every lcm row
  returns inside the finite Ramanujan cutoff.
- When `D0 < V/2`, uses the classical Selberg divisor Gram factorization
  to prove a positive terminal-octave Gram floor and, when
  `K/V^2 -> infinity` as in the explicit TPC-17 profiles, natural
  `k`-space `L2` mass. The
  sharp tail cannot then be removed by coefficient smallness or a
  balanced factorization shortcut.
- Opens `k=dj` and proves that same-source, small-determinant, and
  large-`gcd(d1,d2)` channels are negligible. A failed dyadic slice
  forces a distinct-source, large-determinant, low-gcd correlation.
- Splits by `s=gcd(k,h)`. For every `s>1`, the entire interior Möbius
  tail cancels exactly and only two endpoint bands survive.
- Reduces nonprimitive residual pairs, up to a negligible prime-power
  term, to a finite-model correlation with three explicit CRT
  compatibility conditions.
- States, but does not assume as known, the generic determinant
  dispersion estimate that would close the primitive tail. Under an
  explicit additional all-block cover hypothesis, uniform closure plus
  TPC-16/17 reaches fixed-shift Hardy–Littlewood, explaining why this is
  the real parity-sensitive gate.

The paper does **not** prove the twin-prime conjecture, a fixed-shift
Hardy–Littlewood asymptotic, a new distribution level, or a breach of
sieve parity.

## Files

- `main.tex` and `sections/*.tex`: paper source.
- `references.bib`: bibliography.
- `experiments/tpc18_certificate.py`: exact finite identity checks.
- `experiments/tpc18_certificate.json`: deterministic certificate.
- `mobius-tail-determinant-dispersion.pdf`: compiled paper.

## Reproduce the certificate

```bash
python experiments/tpc18_certificate.py
```

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
