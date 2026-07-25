# TPC-100: Invertible ultra-multiplier linearization

Paper title:

> *Invertible Ultra-Divisor Linearization on the Nonconstant Branch:
> Exact Orbit Preimages, Diagonal Cell Energy, and the Cross-Cell
> Gate*

## Provenance correction

The primary resolved object is

\[
\beta=(\theta,c,\kappa),\qquad
\theta=(L,\gamma,\ell,j,\sigma,v,\iota).
\]

Thus `theta` fixes `j` and `sigma`. It does **not** fix the actual
opened divisor or moving source row along the resolved fiber. For

\[
t_{\beta,z}=\tau_\beta+B_\beta z,
\]

the opened source atom is

\[
p=(\beta,z),\qquad
u_p=U_\theta(t_{\beta,z}),\qquad
m_p=M_\theta(t_{\beta,z}),
\]

and

\[
m_pj_\theta+h_0=\sigma_\theta u_p.
\]

The TPC-99 weight is the full branch absolute mass

\[
w_\beta=\sum_{z\in I_\beta^\ast}w_{\beta,z}.
\]

TPC-100 first performs this exact atomization. It then augments every
atom by the TPC-93 child-to-source inverse and forms fine cells by
deleting only `j`. A cell together with `j` restores the unique
`(beta,z)` and its r-free source. In fact, because the cell retains
the physical values `m`, `u`, and `sigma`, the source identity
already recovers

\[
j=(\sigma u-h_0)/m.
\]

Hence every maximally literal fine cell is a singleton. Its
injectivity is exact but vacuous, and no branchwise dispersion is
created. No branch mass is duplicated.

For a nonconstant resonant branch, the resonance width is always

\[
\mathsf H_\beta=H_{q_X}(N_\beta),\qquad
N_\beta=\#I_\beta^\ast.
\]

It is not computed from the number of atoms or orbit points in a
cell. Branches with `N_beta > q_X` have no nonzero resonance and do
not enter the width census.

## Main results

1. The nonconstant opened-atom mass is split by the actual source
   value `u_p`.

   If `q_X | u_p`, then

   \[
   q_X\mid m_pj_\theta+h_0.
   \]

   For each actual moving source row, strong no-wrap leaves at most
   one orbit point. Reassembling both polarizations, projector and
   exact-content children, actual masks, divisor weights, and the
   low-window multiplier gives

   \[
   |\mathcal L^{q\mid u}_{K,R,X}|
   \ll X^{o(1)}Q_X^2.
   \]

2. If `q_X` does not divide the actual opened value `u_p`, the
   branch multiplier has the atomwise finite-field formula

   \[
   \omega_\beta
   =
   A_p(m_pj_\theta+h_0),\qquad
   A_p=\varepsilon_\beta\ell_\beta v_\beta B_\beta
   (c_\beta u_p)^{-1}.
   \]

   Its integer provenance is

   \[
   \frac{\Omega_\beta}{c_\beta}
   =
   \kappa_\beta\ell_\beta v_\beta
   \frac{\sigma_\beta}{g_\beta}\in\mathbb Z.
   \]

   The quotient `ell*v*B/c` need not be integral.

3. The multiplier map is formally injective inside each fine
   provenance cell, but every such cell is a singleton. Resonance
   preimages and cross-cell collisions still have exact affine
   congruence formulas; they are bookkeeping identities rather than
   a within-cell dispersion gain.

4. The exact TPC-99 census is recovered by re-summing the opened
   weights. Its centered energy is

   \[
   \|(a_H^{\rm inv})^\circ\|_2^2
   =
   \mathfrak D_H^\circ+\mathfrak X_H^\circ.
   \]

   Because the cells are singletons, the diagonal term is exactly

   \[
   \mathfrak D_H^\circ
   =
   \frac{q_X-2}{q_X-1}
   \sum_{\substack{p=(\beta,z):\ \mathsf H_\beta=H\\q_X\nmid u_p}}
   w_{\beta,z}^2.
   \]

   The cross-cell term includes different `z` atoms of the same
   branch. Since those atoms retain the same `omega_beta`, atomwise
   linearization does not create branchwise dispersion.

## Claim boundary

The finite provenance, atomwise linearization, preimage and energy
identities are L0. The complete opened `q_X | u_p` return and exact
TPC-99 atom crosswalk are L1, conditional on the upstream literal
source reconstruction and soft envelopes.

The principal, diagonal and cross-cell growth gates are not proved.
The singleton-cell observation makes explicit that the affine
linearization alone does not help those gates.
No L2 fixed-shift estimate, affine Mobius cancellation theorem,
parity breakthrough, or prime-pair result is claimed. Nothing is
specialized to `h0 = 2`.

## Reproduce

```powershell
python experiments/tpc100_certificate.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The corrected certificate constructs `4,096` branches and `6,851`
opened atoms, includes both polarization signs, and completes
`208,811` exact checks.

Archival PDF:

`invertible-ultra-multiplier-linearization.pdf`

Certificate SHA-256:

`EF308431ED63AC09D93B3E45C4B8915FDD851D7C32237AF192CB48DAA9A36E4F`

Archival PDF SHA-256:

`ABB1D07EDA5D50F499FAD6D5EE2A1877E3A8A496A39B2AA008AB5F90ABAA8369`
