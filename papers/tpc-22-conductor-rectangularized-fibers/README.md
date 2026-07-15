# TPC-22 — Conductor-rectangularized fibers

This directory contains:

> **Conductor-Rectangularized Fibers in a Primitive Möbius Tail:
> Tensor Large Sieve, Gauss Complementarity, and Selected Short–Short
> Closure**

Subject to the inherited no-wrap, polynomial tail-mass, and single-leg
conditions, TPC-22 closes the centered connected discrepancy left by
TPC-21 for the selected short–short packet with its actual
row-pair-only generic mask. TPC-21 already closed the Ramanujan mean of
the same packet, so the selected packet is closed in the stated
parameter profiles.

This is not a proof of the full TPC-18 residual-dispersion theorem. The
large-divisor legs, full residual reassembly, sieve parity barrier,
Hardy–Littlewood asymptotic, and twin-prime lower bound remain outside
the result.

## Main results

- For a squarefree divisor pair, write
  \[
  g=(u,v),\qquad u=ga,\qquad v=gb,\qquad q=gab.
  \]
  The shared-\(g\) character convolution of TPC-21 rectangularizes
  exactly:
  \[
  \frac1{\varphi(g)}\sum_{\psi\bmod g}
  \mathcal B_{\mathfrak m}
  ((\chi_g\psi)\boxtimes\chi_a,\bar\psi\boxtimes\chi_b)
  =
  \sum_{m,n}c_{m,n}\mathbf1_{m\equiv n\pmod g}
  (\chi_g\boxtimes\chi_a)(m)\chi_b(n).
  \]
  The mask stays inside the coefficient matrix. There is no extra
  \(1/\varphi(g)\) after rectangularization and no conjugation on the
  second row character.

- For each fixed divisor pair,
  \[
  \mathfrak X(q)\simeq\mathfrak X(u)\times\mathfrak X(b),
  \qquad
  \operatorname{cond}\chi
  =\operatorname{cond}\alpha\,\operatorname{cond}\beta.
  \]
  Different divisor pairs do not share one global rectangle. The proof
  splits pairs first; the \(3^{\omega(q)}=X^{o(1)}\) cost is harmless.

- The actual off-diagonal mask gives the total compatibility-matrix
  energy
  \[
  \sum_g\sum_{m,n}|c_{m,n}^{(g)}|^2
  \ll_\varepsilon Q^2X^\varepsilon.
  \]

- The weighted exact-conductor large sieve is
  \[
  \sum_{\substack{s\asymp S\\s\ \mathrm{squarefree}}}
  \frac1{\varphi(s)}
  \sum_{\operatorname{cond}\chi\asymp F}
  \left|\sum_na_n\chi(n)\right|^2
  \ll_\varepsilon
  X^\varepsilon\left(F+\frac NF\right)\sum_n|a_n|^2.
  \]
  Conductor one is included, so induced principal and one-sided
  principal modes are retained correctly.

- Tensorizing the one-dimensional estimate bounds an arbitrary masked
  matrix:
  \[
  \mathcal E_Y(F_1,F_2)
  \ll_\varepsilon Q^2X^\varepsilon
  \mathcal K_Q(F_1)\mathcal K_Q(F_2),
  \qquad
  \mathcal K_Q(F)=F+\frac QF.
  \]

- For the common pair-separated scalar cell
  \(\mathfrak L_Y(F_1,F_2)\), the inherited norm route gives
  \[
  \mathfrak L_Y(F_1,F_2)
  \ll_\varepsilon
  QX^\varepsilon
  \sqrt{JY\mathcal K_Q(F_1)\mathcal K_Q(F_2)}.
  \]

- The exact induced-Gauss route estimates the same scalar cell at every
  nonzero additive frequency, not only \((r,q)=1\), and gives
  \[
  \mathfrak L_Y(F_1,F_2)
  \ll_\varepsilon
  QF_1F_2X^\varepsilon
  \sqrt{\mathcal K_Q(F_1)\mathcal K_Q(F_2)}.
  \]
  The Ramanujan weighted-frequency estimate is
  \[
  \sum_{r\ne0}|c_d(r)|
  \left|\widehat F\left(\frac{rJ}{Hq}\right)\right|
  \ll_\varepsilon X^\varepsilon\frac qJ\tau(d).
  \]

- Writing \(Q=X^\beta\) and \(R=X^{1/2-\delta}\), every conductor
  block receives the certified saving
  \[
  \eta_*=
  \min\left\{
  1-\frac{3\beta}{2},
  \frac{\beta+4\delta-1}{2},
  \frac{6\delta-\beta}{4}
  \right\}>0
  \]
  when
  \[
  1-4\delta<\beta<\min\left\{\frac23,6\delta\right\}
  \]
  with fixed margins. Selected-packet closure additionally assumes the
  inherited no-wrap and polynomial tail-mass hypotheses and the strict
  single-leg condition \(\beta<1/2+\delta\). For
  \(\beta<2\delta\), the earlier occupancy estimate closes every
  \(Y\le R^2\), with the top block being the worst case, subject to the
  same inherited interface conditions.

- The actual \(D>D_0\) tail profiles have uniform endpoint ledgers:

  \[
  \text{published: }
  \left(
  \frac1{42}+\sigma+\frac{3t}{4},
  \frac4{63}-\frac{7\sigma}{3}+2t,
  \frac4{63}-\frac{5\sigma}{6}+\frac{13t}{8}
  \right),
  \]
  \[
  \text{Li-v6: }
  \left(
  \frac1{34}+\sigma+\frac{3t}{4},
  \frac1{17}-\frac{19\sigma}{12}+2t,
  \frac1{17}-\frac{5\sigma}{6}+\frac{13t}{8}
  \right).
  \]
  The inherited ranges \(\sigma<1/100\) and \(\sigma<1/1000\) lie
  strictly inside the new closure region.

## Exact certificate

From this directory, run:

~~~powershell
python experiments\tpc22_certificate.py
python -O experiments\tpc22_certificate.py
~~~

Both modes perform 346 exact checks and regenerate byte-identical JSON.
The certificate uses integers, Fraction, and exact roots of unity in
\(\mathbf F_{61}\). It checks the \(q=30\) rectangularizations in both
orientations, conductor products, principal-coordinate bookkeeping,
all-frequency induced Gauss identities, hard-failure variants, and the
exact profile ledger.

- JSON SHA-256:
  772aa4a68009d2ffb7960f2d27db287e52c7a80aa7cd915293e4fc8dea3fa934
- source SHA-256:
  2cc5e3fcdab3a51950f60c726ba8d64a96542c5fde115ac32545834be54e2964
- certificate digest:
  c93ff8e6755ab0db536621e3b2c2b3f8332950da0a5784f60138912a2159fab8

Every asymptotic, full-residual, Hardy–Littlewood, parity-breakthrough,
and twin-prime evidence flag is false.

## Files

- main.tex — paper entry point
- sections/ — section sources
- references.bib — bibliography
- main.pdf — compiled paper
- experiments/tpc22_certificate.py — exact certificate
- experiments/tpc22_certificate.json — archived output

## Build

~~~powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
~~~
