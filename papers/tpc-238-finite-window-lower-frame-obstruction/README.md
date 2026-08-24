# TPC-238: Finite-Window Lower Frame Obstruction

**Title:** A Finite-Window Lower Frame Obstruction for Primitive Rational Frequencies
**Author:** Liang Wang
**Affiliation:** Huazhong University of Science and Technology, Wuhan 430074, P.R. China
**Date:** Aug 24 2026

## One-sentence contribution

For primitive rational frequencies of height at most \(U\), every interval of
\(N\) consecutive integers has normalized Fourier energy at least

\[
\left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+
\]

times the collapsed coefficient energy; at the V59 scale this is
\(1/2-o(1)\), so cancellation between distinct reduced frequencies cannot
provide a fixed-power saving after the \(q\)-collapse.

## Main theorem

Let \(I\) be any interval of \(N\geq 1\) consecutive integers and put
\(L=\lfloor(N+1)/2\rfloor\). Let \(z_{h,a}\) be finitely supported on distinct
primitive fractions \(a/h\pmod 1\), with \(h\leq U\). Then

\[
E_I(z):=\sum_{n\in I}
\left|\sum_{h,a}z_{h,a}e(na/h)\right|^2
\geq
\left[L-\frac{\pi^2U^4}{12L}\right]_+
\sum_{h,a}|z_{h,a}|^2.
\]

Consequently,

\[
\frac{E_I(z)}{N}
\geq
\left[\frac12-\frac{\pi^2U^4}{6N^2}\right]_+
\sum_{h,a}|z_{h,a}|^2.
\]

For \(U=x^{133/400}\) and \(N\asymp x\),
\(U^4/N^2=x^{-67/100+o(1)}\).

## Status markers

    TPC238_ROUTE_ADVANCE = YES
    TPC238_TRIANGULAR_WINDOW_LOWER_FRAME = PROVED_EXACT
    TPC238_PRIMITIVE_FAREY_SPACING = PROVED_U_TO_MINUS_2
    TPC238_FEJER_OFFDIAGONAL = PROVED_LE_1_OVER_4L_DISTANCE_SQUARED
    TPC238_CIRCULAR_PACKING_ROW_SUM = PROVED_LE_PI_SQUARED_U_FOUR_OVER_3
    TPC238_LOWER_FRAME = PROVED_L_MINUS_PI_SQUARED_U_FOUR_OVER_12L_POSITIVE_PART
    TPC238_NORMALIZED_LOWER_FRAME = PROVED_HALF_MINUS_PI_SQUARED_U_FOUR_OVER_6N_SQUARED_POSITIVE_PART
    TPC238_V59_FRAME_DEFECT = PROVED_X_MINUS_67_OVER_100
    TPC238_CROSS_REDUCED_FREQUENCY_FIXED_POWER_SAVING = REFUTED_SCOPED_AFTER_Q_COLLAPSE
    TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN
    TPC238_STATUS = PROVED_STRUCTURAL_OBSTRUCTION_L1
    TPC238_ROUND2_CLUE = MOVE_THE_POWER_SAVING_SEARCH_INSIDE_THE_LITERAL_C_H_WEIGHTED_Q_COLLISION_BUCKETS

## Claim firewall

The result is a structural lower-frame theorem. It applies only after the
\(q\)-variables have been collapsed into one coefficient at each primitive
frequency. It does **not** rule out:

- cancellation inside the \(q\)-bucket defining one collapsed coefficient;
- cancellation in the literal signed construction of \(C_h\);
- cancellation after the signed four-packet projection.

The release ledger is therefore:

    ARITHMETIC_ADVANCE = NO
    C_H_SIGNED_CANCELLATION = NONE
    L2 = NONE
    FULL_GATE_B = OPEN
    STRICT_1_OVER_400 = UNPAID_GLOBAL
    FIXED_ATOM = 0
    ROUTE_A_A0 = FALSE
    ROUTE_A_A1 = FALSE
    ROUTE_A_A2 = FALSE
    ROUTE_A_A3 = FALSE
    ROUTE_A_A4 = FALSE
    SHARPNESS = NOT_CLAIMED

## Project layout

- PAPER_PLAN.md — claims/evidence map and paper structure.
- DERIVATION_PACKAGE.md — formula-level derivation and exponent audit.
- PROOF_PACKAGE.md — complete proof with boundary cases.
- paper/ — LaTeX sources and final paper.pdf.
- code/ — deterministic certificate producer.
- experiments/ — independent checker and Gram/window stress test.
- results/ — machine-readable certificate and validation report.
- notes/ — theorem ledger, route evaluation, and claim firewall.

## Reproduction

From this project directory:

    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc238_lower_frame_certificate.py --write
    PYTHONDONTWRITEBYTECODE=1 python -B code/tpc238_lower_frame_certificate.py --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B code/tpc238_lower_frame_certificate.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc238_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc238_independent_checker.py --check
    PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc238_gram_window_stress.py --check
    PYTHONDONTWRITEBYTECODE=1 python -O -B experiments/tpc238_gram_window_stress.py --check

Build the paper from paper/:

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

## Research extraction

- **Strongest positive result:** an explicit lower frame with defect
  \(\pi^2U^4/(12L)\).
- **Strongest obstruction:** distinct reduced frequencies cannot be the source
  of a fixed-power cancellation saving at V59 after \(q\)-collapse.
- **Open theorem:** prove a fixed-power reduction in the literal
  \(C_h\)-weighted same-frequency \(q\)-collision energy.
- **Reusable structure:** translated triangular window + Farey spacing +
  Fejér off-diagonal decay + circular packing + Schur/Gershgorin.
- **ROUND2 clue:** move the saving search inside the literal
  \(C_h\)-weighted \(q\)-collision buckets.

## Release QA

- Final PDF: paper/paper.pdf
- Pages: 7
- Size: 298148 bytes
- PDF SHA-256:
  4ba2f92970804bdda61bd5ab239107975b001950f8d2e3c2a276f5786051303b
- Final LaTeX log: no warnings, undefined references/citations, overfull
  boxes, or underfull boxes.
- Fonts: all embedded.
- Complex phase-direction regression: `BETA_MINUS_ALPHA_PASS`; the exact
  two-frequency fixture rejects the conjugated `alpha-minus-beta` Gram form.
- Visual inspection: all seven pages passed at 144 dpi; page 6 was also
  checked at 300 dpi.
- Render directory: /tmp/tpc238-render.1bJNV5
