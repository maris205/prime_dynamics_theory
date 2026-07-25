# TPC-99: Multiplicative resonance incidence

Paper title:

> *Multiplicative Resonance Incidence at the No-Wrap Prime:
> Exact Character Spectrum, Parity Nullspace, and the Native
> Dispersion Gate*

## Main result

For an odd prime `q` and

\[
E_H=\{\pm1,\ldots,\pm H\}\subset\mathbb F_q^\times,
\]

the resonance carrier is

\[
(K_Hb)(\omega)
=\sum_r b(r)1_{E_H}(r\omega).
\]

The paper proves its complete multiplicative-character spectrum:

\[
\widehat{1_{E_H}}(\chi)
=
(1+\overline{\chi(-1)})
\sum_{n\le H}\overline{\chi(n)}.
\]

Consequences:

- every odd multiplicative character is an exact null mode;
- the principal singular value is `2H`;
- the nonprincipal squared singular mass is exactly
  `2H(q-1-2H)`;
- even nonprincipal modes are bounded by
  `O(sqrt(q) log q)` via Polya--Vinogradov;
- every incidence bilinear form has an exact principal/nonprincipal
  decomposition.

For a frequency-free literal branch `beta=(theta,c,kappa)` with
resolved z-fiber length `1 <= N_beta <= q_X`, resonance is exactly

\[
r\omega_\beta\in E_{H_{q_X}(N_\beta)},\qquad
H_q(N)=\min\{(q-1)/2,\lfloor q/N\rfloor\}.
\]

Branches with `N_beta > q_X` have no resonant nonzero frequency.
Grouping the frequency-independent weights
`w_beta=|A_beta| mathcal A_beta` by exact width and native phase
multiplier gives two explicit sufficient conditions: an
affordable principal mass and centered multiplier dispersion at
roughly the `Q_X^(3/2)` scale. These conditions are not proved here.

A sharp delta example shows that conductor `q_X` alone gives no
saving: all low frequencies can remain resonant.

## Claim boundary

The incidence spectrum is L0. The positive literal majorant and its
lossless frequency-free key crosswalk are an L1 certificate
interface. No L2 bound for the growing fixed-`h0`
coefficient, affine Mobius cancellation theorem, parity
breakthrough, or prime-pair result is claimed.

The paper retains one prescribed nonzero `h0`, all native keys,
actual masks and support, both polarizations, and global
normalization. It does not specialize to `h0 = 2`.

## Reproduce

```powershell
python experiments/tpc99_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`multiplicative-resonance-incidence.pdf`
