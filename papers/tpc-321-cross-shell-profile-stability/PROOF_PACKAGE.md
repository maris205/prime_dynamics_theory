# TPC-321 proof package and claim firewall

## Proposition 1 — exact normalization identity (PROVED)

If (G\succeq0), (operatorname{tr}(G)>0), and (c>0), then the descending
eigenvalue profile (p_j(G)=\lambda_j(G)/\operatorname{tr}(G)) satisfies
(p_j(cG)=p_j(G)) for every (j).  Consequently (D_{m TV}), (D_{m L}),
and (D_{m int}) are unchanged by a common positive rescaling of either
matrix.

**Proof.** Positive rescaling multiplies every eigenvalue by (c) and the
trace by (c); cancellation gives the identity term by term.  Substitution
in the three definitions gives the metric invariance. \(square)

## Proposition 2 — finite profile separation (NUMERICALLY_CERTIFIED)

For the exact panel

\[
 X\in\{640,1280,2560\},\quad Q\in\{24,36,54,80\},\quad s\in\{1,2\},
\]

all 18 adjacent-(Q) comparisons satisfy

\[
 D_{\rm TV}>0.03,\qquad D_{\rm L}>0.02,
\]

with the producer's outward path intervals.  The independent reverse-order
replay reproduces the estimates and labels.  This proposition is a finite
certificate, not an asymptotic theorem.

## Proposition 3 — no common majorization direction on the panel
 (NUMERICAL OBSERVATION / REFUTED_FINITE_PANEL)

The same 18 comparisons contain three (p_Q\succeq p_{Q'}) labels, two
(p_{Q'}\succeq p_Q) labels, and thirteen mixed labels under
(\tau=10^{-8}).  Therefore the panel does not support a single universal
majorization direction.

## Explicit non-claims

The following remain `OPEN` or `NONE`:

* a uniform full-profile law as (X\to\infty) or as shell anchors vary;
* conversion of an unsigned PSD Gram profile into a signed prime sum;
* arithmetic cancellation or any power saving;
* fixed-power credit and full Gate B;
* the twin-prime conjecture.

The repository lacks the Session-named official evaluator files.  The local
Bridge-B checker is intentionally fail-closed and reports only the finite
certificate status above.
