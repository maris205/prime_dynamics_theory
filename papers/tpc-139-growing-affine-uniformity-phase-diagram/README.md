# TPC-139: Growing affine uniformity phase diagram

Paper title:

> *From Frozen Affine Pairs to Growing CRT Fibers: Uniformity
> Envelopes, Cutoff Phase Diagrams, and the Fixed-Two Quantifier
> Barrier*

The paper compares two exact squarefree decompositions.

For the magnitude cutoff \(Q_R\):

\[
\text{tail}\ll Y^{o(1)}(N/R+\sqrt Y),\qquad
L_z\le MR_{\rm eff}^4.
\]

For the prime-square cutoff \(\mathsf S_P\):

\[
\text{tail}\ll N/P+\sqrt Y,\qquad
L_z\le M(P^\#)^2,
\]

with at most \(4^{\pi(P)}\) ordered component pairs. The exponent
two is essential: the joint modulus is

\[
M\,\operatorname{lcm}(k,\ell)^2\le M(P^\#)^2.
\]

For each fixed integer data height \(Q\), Tao's fixed-affine theorem
is uniform over the finite set of records of height at most \(Q\).
A countable diagonal therefore supplies, for each fixed terminal
ratio \(\omega\), some non-effective
\(Q_{*,\omega}(x)\to\infty\). It supplies no prescribed growth rate
and is not uniform in \(\omega\).

The paper also records the stronger 2026 source frontier.
Tao--Teräväinen prove a power-of-log two-point estimate outside a
small logarithmic-density exceptional set, uniformly for positive
affine coefficients and constants of sufficiently small
polylogarithmic height. Thus the correct phase diagram has an
explicit small-polylog/almost-scale positive corridor. It still
does not prove that the actual TPC CRT family lies in that corridor,
that all pulled-back exceptional sets remain sparse after
reassembly, or that deterministic physical prefixes avoid them.

Status:

- cutoff phase diagram and fixed-height envelope: **L0/L1**;
- small-polylog affine almost-scale corridor: **proved external
  L1 input**;
- non-effective slow diagonal: **proved**;
- larger prescribed polylog/power uniformity: **OPEN**;
- actual CRT containment and selector return: **OPEN**;
- physical all-prefix power estimate and positive L2: **OPEN / not
  proved**.

Reproduce:

```powershell
python experiments/tpc139_uniformity_phase_audit.py
python experiments/tpc139_uniformity_phase_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-139-growing-affine-uniformity-phase-diagram.pdf`
