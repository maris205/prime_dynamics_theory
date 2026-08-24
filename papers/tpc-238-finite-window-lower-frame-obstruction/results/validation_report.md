# TPC-238 Validation Report

## Status

**PASS**

## Certificate

- Payload SHA-256:
  8af87fa72672eff8b9b5553d620fdbfe4127fdb5ee0fdc7c6b32ef604ec0fe26
- Primitive frequencies: 6
- Shifted fixture windows: 4
- Rejected mutations: 3

## Exact fixture ledger

\[
(U,N,L)=(4,41,21),\qquad
\delta_{\min}=\frac1{12}\geq\frac1{16}=U^{-2}.
\]

The translated triangular window has 41 positive entries and exact mass 21.
For this fixture the theorem lower bound is

\[
21-\frac{64\pi^2}{63}=10.973735211592\ldots,
\]

and the simplified normalized lower bound is

\[
\frac12-\frac{128\pi^2}{5043}
=0.249492491902\ldots.
\]

The symbolic statements and rational identities above are part of the
**EXACT_THEOREM_LEDGER**. Decimal evaluations are finite numerical checks.

## Numerical fixture observations

Across starts \(-20,0,17,103\):

- minimum triangular Gram eigenvalue:
  \(20.571428571429\);
- minimum hard-window Gram eigenvalue:
  \(36\);
- minimum hard normalized frame:
  \(36/41=0.878048780488\);
- maximum inverse-square row sum:
  \(203.76\), below the universal cap \(842.206242226292\).

These values are **NUMERICALLY_CERTIFIED_FINITE_CHECK** outputs. Their excess
over the theorem constants is a **NUMERICAL_OBSERVATION** and does not imply
sharpness.

## Stress experiment

The stress grid used

\[
(U,N)\in\{(2,9),(3,25),(4,41),(5,81)\}
\]

and four interval translations per pair, for 16 windows total.

- smallest triangular-minus-theorem margin:
  \(2.43189450696\);
- smallest hard-minus-triangular margin:
  \(3.2\);
- largest translated-spectrum drift:
  \(1.23350218928\times10^{-11}\).

## Mutation firewalls

The producer and independent checker both reject:

1. a denominator above \(U\);
2. a duplicated reduced frequency;
3. a nonprimitive representation.

## Mode comparison

The producer check, independent check, and stress experiment were each run
under ordinary Python and optimized Python. All six runs exited with status
zero, all stderr files were empty, and each normal/optimized stdout pair was
byte-identical.

The independent checker additionally uses

\[
I=\{0,1,2\},\qquad \mathcal F=\{0,1/3\},\qquad z=(1,i)
\]

to verify the exact Gram phase direction `beta-minus-alpha`.  It reproduces
the weighted energy \(4-\sqrt3/2\) and rejects the conjugated value
\(4+\sqrt3/2\).

Scratch directory:

    /tmp/tpc238-tests.t1rNsX

## PDF QA

- Build sequence: pdflatex, bibtex, pdflatex, pdflatex.
- Final PDF: paper/paper.pdf.
- Pages: 7.
- Size: 298148 bytes.
- SHA-256:
  4ba2f92970804bdda61bd5ab239107975b001950f8d2e3c2a276f5786051303b.
- Final log: no warning, undefined reference/citation, overfull box, or
  underfull box.
- Fonts: every listed font is embedded and subset.
- Text extraction: PASS.
- Visual inspection: all seven pages PASS; page 6 table also PASS at 300 dpi.
- Render directory: /tmp/tpc238-render.1bJNV5.
