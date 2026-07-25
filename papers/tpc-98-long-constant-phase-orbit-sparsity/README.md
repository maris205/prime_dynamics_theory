# TPC-98: Literal constant-phase orbit sparsity

Paper title:

> *The Literal Constant-Phase Sector at the Strong No-Wrap Prime:
> Orbit Sparsity and an Endpoint-Scale Literal Bound*

## Main result

TPC-94 shows that every literal low-window phase has conductor `1`
or the strong no-wrap prime `q_X`. This paper proves that the entire
conductor-one branch is already affordable.

The auxiliary prime can be chosen, without changing the physical
coefficient, larger than every row, row difference, and orbit
diameter. For a resolved key

\[
\Omega_\xi=\ell_\xi v_\xi\sigma_\xi B_\xi.
\]

- Literal common-target provenance gives
  `B_xi <= b_xi <= |M_xi - n_xi| < q_X`.
- The prime `q_X` also divides neither `ell_xi` nor `v_xi`.
  Thus conductor one is equivalent to `q_X | sigma_xi`.
- Since `m_alpha j + h0 = u sigma_xi`, this forces
  `q_X | m_alpha j + h0`.
- The actual orbit interval is shorter than `q_X`, so each moving
  row has at most one such `j`.

Restoring both polarizations, the actual row coefficients and mask,
all projector/content children, divisor weights, and the bounded
low-window multiplier mass gives

\[
\left|\mathcal L^{\rm const}_{K,R,X}\right|
\ll X^{o(1)}Q_X^2
=X^{o(1)}N_{0,X}/J_X.
\]

This removes the complete conductor-one sector as a polynomial
obstruction. It does not bound the short, nonconstant resonant, or
generic sectors.

## Claim level

The divisibility and one-point theorems are L0. Their literal
attachment and the growing exceptional-sector upper bound are L1.
No new signed Mobius-correlation theorem or L2 estimate for the full
fixed-`h0` coefficient is claimed.

The result preserves one prescribed nonzero `h0`, both
polarizations, actual masks and support, complete native provenance,
and the original global normalization. It does not specialize to
`h0 = 2` and implies no prime-pair or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc98_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`literal-constant-phase-orbit-sparsity.pdf`
