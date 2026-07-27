# TPC-140: Exceptional-scale selector power gate

Paper title:

> *Exceptional-Scale Selection and the Actual Fixed-Two Power Gate:
> A Carleson Return Interface for H3*

An almost-all-scales arithmetic theorem does not control a
deterministically selected prefix. This paper gives two legal return
interfaces:

1. a direct pointwise all-prefix theorem; or
2. a selector measure \(\nu_X\) dominated by normalized logarithmic
   measure \(m_X\):

\[
\nu_X(E)\le K_Xm_X(E)
\quad\text{for every Borel }E.
\]

If the arithmetic scale-average error is \(\varepsilon_X\), the
second interface gives

\[
\int |C_X(t)|\,d\nu_X(t)\le K_X\varepsilon_X.
\]

At power scale, with selector, census, and BV losses, the raw
amplitude exponent is

\[
\sigma_{\rm raw}
=
\min\{\eta_{\rm tail},
\sigma_{\rm aff}-\ell_{\rm sel}-\ell_{\rm cen}-\ell_{\rm BV}\}.
\]

TPC-131 can close only when
\(\sigma_{\rm raw}>\Lambda_{\rm phys}\). An atomic selector cannot
be dominated by continuous logarithmic measure, so an actual
discrete all-prefix family still requires a pointwise theorem or a
proved smoothing crosswalk.

The 2026 Tao--Teräväinen theorem adds a real small-polylog,
almost-scale input. Its power-of-log losses obey the parallel ledger

\[
\kappa_{\rm raw}
=
\min\{\kappa_{\rm tail},
\kappa_{\rm aff}-\kappa_{\rm sel}-\kappa_{\rm cen}-\kappa_{\rm BV}\}.
\]

A source bound of the form

\[
\frac1{\log x}\int_{[1,x]\cap\mathcal E}\frac{dt}{t}
\ll(\log x)^{-c}
\]

only gives, on \(J=[x/\omega,x]\),

\[
m_J(\mathcal E)
\ll
\min\left\{1,\frac{(\log x)^{1-c}}{\log\omega}\right\}.
\]

Thus the effective arithmetic log exponent is the minimum of the
nonexceptional correlation exponent and a separately proved
exceptional-window exponent. The global exponent cannot be copied
unchanged onto an arbitrary terminal window.

A positive \(\kappa_{\rm raw}\) can yield qualitative cancellation
after a valid selector return, but still corresponds to
\(\sigma_{\rm raw}=0\) in the \(X\)-power ledger and cannot pay a
fixed positive physical endpoint loss.

Current status:

- selector and exponent implications: **conditional L1**;
- small-polylog affine almost-scale rate: **proved external input**;
- growing power-scale determinant-two rate: **OPEN**;
- actual selector/all-prefix certificate: **OPEN / not supplied**;
- fixed positive L2, H3, and the \(1/400\) endpoint: **not proved**.

Reproduce:

```powershell
python experiments/tpc140_selector_power_audit.py
python experiments/tpc140_selector_power_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-140-exceptional-scale-selector-power-gate.pdf`
