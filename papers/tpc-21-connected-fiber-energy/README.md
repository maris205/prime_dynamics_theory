# TPC-21 — Connected fiber energy

This directory contains:

> **Connected Fiber Energy in a Primitive Möbius Tail: Ramanujan-Mean
> Closure, Divisor-Lattice Reassembly, and a Shared-Factor Character Gate**

TPC-21 advances the short–short branch left open by TPC-20. It closes the
Ramanujan mean packet unconditionally, proves a deterministic row-occupancy
bound, and identifies the remaining centered discrepancy as an exact masked
shared-factor character moment. It does **not** prove the long connected
moment, the full TPC-18 residual-dispersion estimate, a parity breakthrough,
a fixed-shift Hardy–Littlewood asymptotic, or a twin-prime lower bound.

Throughout, \(H=\operatorname{rad}|h|\), \(QJ\asymp X\), and the divisor
variables \(u,v\le R\) form the selected compatible short–short packet.

## Main results

- The Ramanujan-frequency mean has the exact physical-space form
  \[
  \frac JM\sum_{r\ne0}c_M(r)\widehat F(rJ/M)
  =
  \sum_{(n,M)=1}F(n/J)
  -J\frac{\varphi(M)}M\widehat F(0),
  \]
  and is uniformly \(O_F(\tau(M))\). Under the standard separated-packet
  bound \(\mathcal Z_1\ll Q^2X^\varepsilon\), summing every lcm layer
  absolutely gives
  \[
  \sum_q|\mathcal L_q^{\mathrm{mean}}|
  \ll_\varepsilon Q^2X^\varepsilon.
  \]
  Hence the separate TPC-20 mean gate is closed with fixed-power, and
  therefore arbitrary logarithmic, saving throughout its strict single-leg
  range.

- The actual row geometry \(m=\ell d\), with \(L>2R\), gives
  \[
  \|D_q\|_2
  \ll
  W_xW_y\Theta_R^2Q^2q^{-1/2}
  \prod_{p\mid q}\left(2+\frac1p\right)
  \]
  even with the generic Schur mask retained. On \(q\asymp Y\), this has
  relative cost \(X^{o(1)}\sqrt{Y/J}\). It closes only \(Y<J\) with a fixed
  margin and does not enter the genuinely long-lcm range.

- For an unmasked rank-one packet, every lcm layer is an exact divisor-lattice
  Möbius difference:
  \[
  Z_q^1(\kappa)
  =
  \sum_{s\mid q}\mu(q/s)
  B_s^x(\kappa\bmod s)B_s^y(\kappa\bmod s).
  \]
  The paper derives its exact centered covariance and additive CRT lift.
  At additive frequencies coprime to \(q\), all outer Möbius signs disappear;
  this is a structural identity, not a cancellation estimate.

- For the actual generic mask, write \(u=ga\), \(v=gb\), and \(q=gab\).
  Multiplicative Fourier analysis gives the exact shared-factor projector
  \[
  \widehat Z_{u,v}^{\,\mathfrak m,\times}(\chi)
  =
  \frac{\overline{\chi(-h)}}{\varphi(g)}
  \sum_{\psi\bmod g}
  \mathcal B_{\mathfrak m}^{u,v}
  \bigl((\chi_g\psi)\boxtimes\chi_a,\,
        \overline\psi\boxtimes\chi_b\bigr).
  \]
  The factor \(1/\varphi(g)\) is essential. After lcm aggregation,
  nonprincipal multiplicative Parseval identifies
  \(\|D_q^{\mathfrak m}\|_2^2\) exactly with the corresponding masked
  connected four-row moment.

- If a character modulo squarefree \(q\) has conductor \(f\mid q\), then
  \[
  G_q(\chi;t)
  =
  \begin{cases}
  \overline{\chi^*(t)}\chi^*(q/f)\tau_f(\chi^*)c_{q/f}(t),
    &(t,f)=1,\\
  0,&(t,f)>1.
  \end{cases}
  \]
  Thus at primitive additive frequencies its magnitude is \(\sqrt f\), not
  automatically \(\sqrt q\). The exact conductor mass is
  \(\sum_{\chi\bmod q}\operatorname{cond}(\chi)=\varphi(q)^2\), so ordinary
  character Cauchy–Schwarz contains no hidden generic gain.

- A single row diagonal is an exact one-fiber spike. Its centered norm equals
  its coefficient amplitude times
  \(\sqrt{1-1/\varphi(q)}\). Therefore scalar degenerate removal alone
  supplies no coefficientwise saving inside the nonlinear fiber norm.
  This does not assert that the actual summed diagonal norm is large; it
  rules out only the unjustified interchange of scalar subtraction and a
  nonlinear norm.

- If a future estimate on \(q\asymp Y=X^y\) improves occupancy by
  \(X^{-\omega}\), this sufficient TPC-20 norm bound yields a fixed-power
  saving when
  \[
  \omega>\frac{y-j}{2},\qquad J=X^{j+o(1)},
  \]
  with a fixed margin. This is a quantified target for one sufficient
  route, not a lower bound on all possible scalar methods.

## Files

- `main.tex` — paper entry point
- `sections/` — section sources
- `references.bib` — bibliography
- `main.pdf` — compiled paper
- `experiments/tpc21_certificate.py` — deterministic exact certificate
- `experiments/tpc21_certificate.json` — certificate output

## Reproduce the exact certificate

From this directory:

~~~powershell
python experiments\tpc21_certificate.py
python -O experiments\tpc21_certificate.py
~~~

Both modes must pass and regenerate byte-identical JSON. In the archived
version:

- JSON SHA-256:
  **21AB51D5A8775832D8C44D90B4E21917C11FADAD1F150B896D234835740D5F74**
- script SHA-256:
  **26268E848E0D66A3B50B6FD628E95D8AF6931DE3FA9FA31D55C722FB8BFB3CB3**

The standard-library certificate performs 1,149 exact equality checks using
integers, `fractions.Fraction`, and exact roots of unity in
\(\mathbf F_{61}\). It checks compatible fiber totals and means, squarefree
lcm occupancy, divisor-lattice reassembly and covariance, additive CRT
lifting and primitive sign loss, multiplicative Parseval, the masked
shared-\(g\) projector, row phases, induced-character Gauss factors, the
additive–multiplicative bridge, the diagonal spike, and the rational gain
ledger. It also verifies that omitting \(1/\varphi(5)\) fails in the explicit
shared-factor example. With \(h=H=47\), it separately detects an omitted
\(\overline H\) additive phase, the wrong unconjugated character phase, and
omission of either exclusive character leg. All twin-prime,
residual-dispersion, parity, and asymptotic evidence flags are false.

## Build the paper

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~
