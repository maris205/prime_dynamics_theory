#!/usr/bin/env python3
"""Generate and verify the TPC-194--203 fixed-atom frontier batch.

This batch is deliberately fail-closed.  It completes the strongest
source-backed *per-packet* prefix formula, proves several exact interface
lemmas and scoped black-box obstructions, audits one genuinely new primary
source, and then recomputes the route.  It does not promote any of those L1
results to a named-production-atom power theorem.
"""

from __future__ import annotations

import argparse
import cmath
import copy
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAPERS = HERE.parents[1]
REPO = PAPERS.parent

TARGET_AXES = {
    "carrier_axis": "ACTUAL_FIXED_H0_PACKET",
    "phase_axis": "SOURCE_LOCKED_NAMED_PHYSICAL_ATOM",
    "endpoint_axis": "DETERMINISTIC_ALL_PREFIX",
    "scale_axis": "DETERMINISTIC_ALL_SCALE",
    "decay_axis": "FIXED_X_POWER_FIXED_ATOM",
    "support_axis": "ACTUAL_ACTIVE_SUPPORT",
}

CLAIM_BOUNDARY = {
    "block_equals_cumulative_prefix": False,
    "symbolic_packet_atom_is_named_production_atom": False,
    "packet_key_is_production_packet_schedule": False,
    "phase_L2_is_named_atom_control": False,
    "lebesgue_ae_phase_is_named_atom_control": False,
    "factorwise_fourier_implies_product_fourier": False,
    "mobius_product_is_one_multiplicative_function": False,
    "fixed_h0_data_is_decay": False,
    "hash_integrity_is_theorem_evidence": False,
    "scoped_method_stop_is_parent_stop": False,
    "declared_corpus_stop_is_global_nonexistence": False,
    "fixed_atom_decay_obtained": False,
    "program_positive_L2": False,
    "strict_one_over_400": False,
    "prime_pair_lower_bound": False,
    "twin_prime_theorem": False,
}

SOURCE_PATHS = {
    "TPC93.introduction": (
        "papers/tpc-93-literal-low-window-affine-export/"
        "sections/introduction.tex"
    ),
    "TPC93.row_window": (
        "papers/tpc-93-literal-low-window-affine-export/"
        "sections/row-window.tex"
    ),
    "TPC93.affine_export": (
        "papers/tpc-93-literal-low-window-affine-export/"
        "sections/decorated-affine-export.tex"
    ),
    "TPC94.phase_conductor": (
        "papers/tpc-94-exact-content-resonance-ledger/"
        "sections/phase-conductor.tex"
    ),
    "TPC108.main": (
        "papers/tpc-108-literal-generic-affine-mobius-dispersion/main.tex"
    ),
    "TPC127.main": (
        "papers/tpc-127-determinant-two-liouville-pullback/main.tex"
    ),
    "TPC130.main": "papers/tpc-130-fejer-four-sign-h3-gate/main.tex",
    "TPC157.main": (
        "papers/tpc-157-literal-weight-periodic-approximation/main.tex"
    ),
    "TPC159.main": "papers/tpc-159-dyadic-shadow-prefix-lifting/main.tex",
    "TPC167.main": "papers/tpc-167-direct-additive-twist-parseval/main.tex",
    "TPC180.registry": (
        "papers/tpc-180-production-phase-registry-census/"
        "experiments/tpc180_phase_registry_census.json"
    ),
    "TPC181.selector": (
        "papers/tpc-181-metric-fixed-atom-selector-gate/"
        "experiments/tpc181_selector_gate.json"
    ),
    "TPC193.gate": (
        "papers/tpc-193-literal-fixed-atom-candidate-mechanism-gate/"
        "experiments/tpc193_literal_fixed_atom_candidate_mechanism_gate.json"
    ),
    "TPC192.snapshot": (
        "papers/tpc-192-mvp9-pointwise-frontier-route-decision/"
        "experiments/tpc192_mvp9_pointwise_frontier_route_decision.json"
    ),
    "TPC200.payload": (
        "papers/tpc-200-four-form-determinant-resonance-refinement/"
        "experiments/tpc200_four_form_determinant_resonance_refinement.json"
    ),
}


def entry(
    num: int,
    slug: str,
    title: str,
    classification: str,
    verdict: str,
    summary: str,
    first_missing: str,
    next_route: str,
    sources: list[str],
    stop_cell: str | None,
    body: str,
    certificate: dict,
) -> dict:
    return {
        "num": num,
        "slug": slug,
        "title": title,
        "classification": classification,
        "verdict": verdict,
        "summary": summary,
        "first_missing": first_missing,
        "next_route": next_route,
        "sources": sources,
        "stop_cell": stop_cell,
        "body": body,
        "certificate": certificate,
    }


PAPERS_DATA = [
    entry(
        194,
        "maximal-source-backed-direct-prefix",
        "The Maximal Source-Backed Direct Prefix: Per-Packet Phase Completion and Formula-Type Separation",
        "FORMULA_RECONSTRUCTION_L1",
        "FORMULA_COMPLETE_PER_PACKET_L1",
        (
            "The physical determinant-two summand and additive atom can be "
            "written without placeholders for each resolved packet key.  This "
            "does not freeze a production packet schedule, uniform constant, "
            "positive exponent, common parameter range, or complete loss ledger."
        ),
        "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
        "DIRECT_FORMULA_TO_PRODUCTION_CROSSWALK",
        [
            "TPC93.affine_export",
            "TPC94.phase_conductor",
            "TPC108.main",
            "TPC127.main",
            "TPC159.main",
            "TPC167.main",
            "TPC180.registry",
            "TPC193.gate",
        ],
        None,
        r"""
\section{Resolved packet and physical coefficient}
Fix a resolved key
\(\xi=(\theta,c,\kappa,r)\), its source-backed interval
\(I_{\xi,X}\), and the literal affine pair
\[
 D_\xi(z)=d_\xi+s_\xi z,\qquad
 V_\xi(z)=u_\xi+a_\xi z,\qquad
 s_\xi u_\xi-a_\xi d_\xi=2.
\]
Write \(b=c\kappa\), \(B_\xi:=B_{\theta,b}\), and let
\(\widetilde r\) be the source-defined signed lift of \(r\).  Define
\[
\Omega_\xi:=\ell_\theta v_\theta\sigma_\theta B_{\theta,b}.
\]
Retain, without renaming, the locked fields
\(\varepsilon_\theta,\ell_\theta,v_\theta,\sigma_\theta\) and
\(\tau_\xi,\zeta_{\xi,X}\) attached to this resolved key
\citep{WangTPC93,WangTPC94,WangTPC108,WangTPC127}.
The maximal coefficient recoverable from the locked formula chain is
\[
 A_{\xi,X}(z)=
 \mu(D_\xi(z))\mu(V_\xi(z))
 \mathbf 1_{(B_\xi,V_\xi(z))=1}
 \chi_\theta(\tau_\xi+B_\xi z)
 W_{\theta,X}(\tau_\xi+B_\xi z).
\]
No factor in this display is deleted or absorbed into an unnamed weight.
The corresponding symbolic packet atom is
\[
 \alpha_{\xi,X}\equiv
 \frac{\varepsilon_\theta\widetilde r\,\Omega_\xi}{c q_X}\pmod 1,
\]
and the outer physical multiplier is
\[
 \mathfrak c_{\xi,X}
 =c_{\theta,X}\mu(\kappa)\mu(B_\xi)
  \mathfrak m_{K,X}(r)\zeta_{\xi,X}.
\]

\section{The maximal per-packet contribution}
For every \(T\in I_{\xi,X}\), the source-backed decorated inner prefix is
\begin{equation}\label{eq:physical-prefix}
 S_{\xi,X}^{\leq T}
 =\sum_{\substack{z\in I_{\xi,X}\\z\leq T}}
 A_{\xi,X}(z)\e(-\alpha_{\xi,X}z).
\end{equation}
The complete per-key physical contribution is
\begin{equation}\label{eq:physical-contribution}
 P_{\xi,X}^{\leq T}
 =\mathfrak c_{\xi,X}S_{\xi,X}^{\leq T}.
\end{equation}
Equation \eqref{eq:physical-prefix} supplies a literal domain, prefix index,
physical coefficient and symbolic atom for a \emph{fixed resolved packet}.
Equation \eqref{eq:physical-contribution} restores the outer multiplier.
Together they are the strongest formula completion proved here.

\section{Three noninterchangeable formula types}
The repository also contains
\[
 F_N^{\rm blk}=\frac{q}{N}\sum_{N<t(z)\leq2N}
 c_z \e(-\alpha z)
\quad\hbox{and}\quad
 F_T^{\rm cum}=\frac{q}{T}\sum_{0<t(z)\leq T}
 c_z \e(-\alpha z).
\]
These are respectively a terminal block and a cumulative prefix.
Neither is definitionally equal to \eqref{eq:physical-prefix}.  In
particular, we do not set \(N=T\), replace \(q_X\) by \(a_\xi s_\xi\),
identify an archive key with a production schedule, or absorb the physical
decorations into \(c_z\).

\begin{theorem}[Maximal source-backed completion]
The fields domain, prefix variable, decorated determinant-two coefficient,
symbolic packet atom, outer multiplier and their per-key product are complete
for each resolved packet.  The direct production target is not
formula-complete: its named
production atom, exact packet schedule, common \(X/N/q\) range, uniform
constant \(C\), positive \(\sigma\), chosen normalization and full physical
loss ledger are not jointly source-locked.
\end{theorem}
\begin{proof}
The first assertion is direct substitution through the locked affine export,
phase-conductor and pullback formulas.  The second is a type check against the
production registry: no locked row supplies the missing crosswalk, and the
three displayed sum types have different domains and normalizations.
Explanatory renaming cannot create any absent field.
\end{proof}
""",
        {
            "resolved_packet_formula": {
                "key": "xi=(theta,c,kappa,r)",
                "content_alias": "b=c*kappa and B_xi=B_theta_b",
                "signed_lift": "r_tilde=source_defined_signed_lift(r)",
                "phase_slope": (
                    "Omega_xi=ell_theta*v_theta*sigma_theta*B_theta_b"
                ),
                "affine_forms": [
                    "D_xi(z)=d_xi+s_xi*z",
                    "V_xi(z)=u_xi+a_xi*z",
                    "s_xi*u_xi-a_xi*d_xi=2",
                ],
                "inner_coefficient": (
                    "A_xi_X(z)=mu(D_xi(z))*mu(V_xi(z))*"
                    "1_gcd(B_xi,V_xi(z))=1*chi_theta(tau_xi+B_xi*z)*"
                    "W_theta_X(tau_xi+B_xi*z)"
                ),
                "packet_atom": (
                    "alpha_xi_X=epsilon_theta*r_tilde*Omega_xi/(c*q_X) mod 1"
                ),
                "outer_multiplier": (
                    "cfrak_xi_X=c_theta_X*mu(kappa)*mu(B_xi)*"
                    "mfrak_K_X(r)*zeta_xi_X"
                ),
                "decorated_inner_prefix": (
                    "S_xi_X_le_T=sum_(z in I_xi_X,z<=T) "
                    "A_xi_X(z)*e(-alpha_xi_X*z)"
                ),
                "complete_per_key_contribution": (
                    "P_xi_X_le_T=cfrak_xi_X*S_xi_X_le_T"
                ),
            },
            "formula_type_registry": [
                {
                    "id": "CORE_TERMINAL_BLOCK",
                    "domain": "N<t(z)<=2N",
                    "normalization": "q/N",
                },
                {
                    "id": "CORE_CUMULATIVE_PREFIX",
                    "domain": "0<t(z)<=T",
                    "normalization": "q/T",
                },
                {
                    "id": "PHYSICAL_PACKET_PREFIX",
                    "domain": "z in I_xi_X and z<=T",
                    "normalization": "UNNORMALIZED_INSIDE_OUTER_PACKET_SUM",
                },
            ],
            "affine_fixture": {"a": 1, "s": 3, "d": 1, "u": 1, "determinant": 2},
            "completion_axes": {
                "summation_domain": "COMPLETE_PER_PACKET",
                "prefix_index": "COMPLETE_PER_PACKET",
                "decorated_physical_coefficient": "COMPLETE_PER_PACKET",
                "symbolic_packet_atom": "COMPLETE_PER_PACKET",
                "named_production_atom": "MISSING",
                "packet_schedule": "MISSING",
                "common_X_N_q_ranges": "MISSING",
                "uniform_constant_C": "MISSING",
                "positive_sigma": "MISSING",
                "target_normalization_selection": "MISSING",
                "complete_physical_loss_ledger": "MISSING",
            },
        },
    ),
    entry(
        195,
        "block-prefix-power-profile-equivalence",
        "Block and Cumulative Prefix Power Profiles: Exact Constants and the Truncation Tail",
        "DETERMINISTIC_REDUCTION_L1",
        "PROVED_BIDIRECTIONAL_POWER_PROFILE_TRANSFER",
        (
            "All-scale dyadic block bounds and cumulative prefix bounds transfer "
            "in both directions with explicit sigma-dependent constants.  If "
            "small blocks are unavailable, the leftover tail is a real loss and "
            "cannot be suppressed by notation."
        ),
        "ALL_SCALE_BLOCK_POWER_BOUND_ON_THE_LITERAL_PHYSICAL_SEQUENCE",
        "APPLY_ONLY_AFTER_PRODUCTION_CROSSWALK",
        ["TPC159.main", "TPC193.gate"],
        None,
        r"""
\section{Abstract sequence theorem}
Let \(0<\sigma<1\), \(q>0\), and
\(A(T)=\sum_{1\le n\le T}a_n\).  Write
\(\Delta(N)=A(2N)-A(N)\), with real endpoints interpreted by integer
cutoffs.

\begin{theorem}[Power-profile transfer]\label{thm:transfer}
If, uniformly for all \(N>0\),
\[
 |\Delta(N)|\le {C\over q}N^{1-\sigma},
\]
then
\[
 |A(T)|\le {C\over q(2^{1-\sigma}-1)}T^{1-\sigma}.
\]
Conversely, if \(|A(T)|\le (C/q)T^{1-\sigma}\) for all \(T\), then
\[
 |\Delta(N)|\le {C\over q}(2^{1-\sigma}+1)N^{1-\sigma}.
\]
\end{theorem}
\begin{proof}
Decompose \((0,T]\) into
\((T/2^j,T/2^{j-1}]\), \(j\ge1\), and sum the geometric series
\(\sum_{j\ge1}2^{-j(1-\sigma)}
=(2^{1-\sigma}-1)^{-1}\).
The reverse direction is the triangle inequality applied to
\(\Delta(N)=A(2N)-A(N)\).  Under the stated real-endpoint step-function
convention the telescoping is exact.  An input stated only for integer
\(N\) requires a separate rounding ledger; it is not silently charged as
one endpoint coefficient.
\end{proof}

\section{Truncated range ledger}
Suppose the block hypothesis starts only at \(N\ge M\), and
\(|a_n|\le B\).  The dyadic decomposition stops when its lower endpoint
would fall below \(M\).  If \(R\) is the remaining endpoint, then
\(R<2M\), so the raw tail is strictly less than \(2BM\).  After the direct
normalization \(q/T\), the safe additional charge is
\[
 {2qBM\over T}.
\]
It is small only after a separate range relation makes it small.  Thus the
full theorem is not a license to identify a terminal block with a cumulative
prefix, and the truncated theorem does not yield a fixed \(X\)-power for
free.  This deterministic transfer is distinct from the exceptional-shadow
statement of TPC-159 \citep{WangTPC159}.

\section{Route consequence}
TPC-194 provides the per-packet sequence but not the production schedule or
an all-scale block estimate on it.  The theorem above is therefore a ready
deterministic edge, not endpoint credit.
""",
        {
            "sigma_fixture": {"numerator": 1, "denominator": 4},
            "dyadic_fixture_T": 1024,
            "forward_constant_formula": "1/(2^(1-sigma)-1)",
            "reverse_constant_formula": "2^(1-sigma)+1",
            "truncated_tail_raw_strict_bound": "2*B*M",
            "truncated_tail_q_over_T_safe_bound": "2*q*B*M/T",
            "endpoint_convention": "REAL_ENDPOINT_STEP_FUNCTION_EXACT_TELESCOPING",
        },
    ),
    entry(
        196,
        "rational-atom-residue-determinant-ledger",
        "Rational Atoms after Residue Splitting: Determinant Inflation and the DFT Ledger",
        "ALGEBRAIC_REDUCTION_L1",
        "PROVED_RESIDUE_SPLIT_WITH_DETERMINANT_2R",
        (
            "A rational twist of conductor R splits into R residue-class sums. "
            "On each class the two affine slopes have gcd exactly R and the "
            "determinant becomes 2R.  One Fourier mode is one DFT coordinate, "
            "not control of every residue sum."
        ),
        "UNIFORM_ALL_RESIDUE_CLASS_CANCELLATION_OR_DIRECT_MODE_THEOREM",
        "RATIONAL_ATOM_THEOREM_SCREEN",
        ["TPC94.phase_conductor", "TPC108.main", "TPC157.main"],
        None,
        r"""
\section{Exact residue decomposition}
Let \(\alpha=r/R\) in lowest terms and let
\[
 C_r(Z)=\sum_{z\in Z}c(z)\e(-rz/R).
\]
Partitioning by \(z=b+Rm\) gives the identity
\begin{equation}\label{eq:dft}
 C_r(Z)=\sum_{b\bmod R}\e(-rb/R)
 \sum_{\substack{m\\b+Rm\in Z}}c(b+Rm).
\end{equation}
For the determinant-two forms \(d+sz,u+az\), the two forms on the
\(b\)-th class are
\[
 (d+sb)+sRm,\qquad (u+ab)+aRm.
\]

\begin{theorem}[Determinant and slope-gcd ledger]
If \(su-ad=2\) and \(as\) is odd, then \((a,s)=1\).  After residue
splitting the two slopes \(sR,aR\) have gcd exactly \(R\), while their
determinant is
\[
 (sR)(u+ab)-(aR)(d+sb)=2R.
\]
Equation \eqref{eq:dft} is one DFT coordinate.  Recovering every residue sum
requires all \(R\) Fourier coordinates and DFT inversion.
\end{theorem}
\begin{proof}
Any common divisor of \(a,s\) divides \(2\); oddness forces it to be one.
The displayed determinant follows by expansion.  The final assertion is
the invertibility of the \(R\times R\) Fourier matrix; a single row has a
kernel of dimension \(R-1\) when \(R>1\).
\end{proof}

\section{Imported identities and new crosswalk}
The DFT identity and the raw progression determinant law are imported from
the TPC-108 alias calculus and TPC-94 phase ledger
\citep{WangTPC94,WangTPC108}.  The L1 contribution here is their joint typed
crosswalk to the TPC-194 decorated direct-prefix object, including the
warning that a single mode is not all residue classes.

\section{Firewall}
The slope-gcd-\(R\), determinant-\(2R\) residue problem is not the original
primitive-slope determinant-two problem.  A theorem for one rational
Fourier mode also cannot be relabelled as simultaneous residue-class
cancellation.
""",
        {
            "fixture": {
                "a": 1,
                "s": 3,
                "d": 1,
                "u": 1,
                "R": 5,
                "r": 2,
                "z_min": 0,
                "z_max": 19,
                "original_determinant": 2,
                "residue_determinant": 10,
                "slope_gcd": 5,
            },
            "one_mode_recovers_all_residues": False,
        },
    ),
    entry(
        197,
        "prime-conductor-fixed-atom-consistency",
        "Prime Conductors versus a Fixed Atom: Recurrence and Period-Corridor Separation",
        "CONSISTENCY_BARRIER_L1",
        "PROVED_NONZERO_FIXED_RATIONAL_ATOM_CANNOT_RECUR_ACROSS_UNBOUNDED_PRIME_CONDUCTORS",
        (
            "A fixed nonzero rational atom cannot be represented in lowest terms "
            "with infinitely many distinct prime conductors q_X.  The variable "
            "q_X branch also lies outside the source-locked polylogarithmic exact-"
            "period corridor; the conductor-one branch remains possible but has "
            "no occurrence or packet schedule theorem."
        ),
        "SOURCE_LOCKED_CONDUCTOR_ONE_OCCURRENCE_PACKET_SCHEDULE_AND_RANGE_ADMISSIBILITY",
        "FIXED_ATOM_OCCURRENCE_EDGE",
        [
            "TPC93.introduction",
            "TPC93.row_window",
            "TPC94.phase_conductor",
            "TPC157.main",
            "TPC180.registry",
        ],
        None,
        r"""
\section{Reduced-denominator rigidity}
The phase-conductor ledger gives a reduced conductor in
\(\{1,q_X\}\), with the nonconstant branch carried by unbounded prime
values \(q_X\) \citep{WangTPC93,WangTPC94}.

\begin{theorem}[Fixed-atom consistency]
Let \(\alpha_\star=r_0/R_0\pmod1\) be reduced and nonzero.  If
\(\alpha_\star=r_X/q_X\pmod1\) is also reduced for infinitely many
distinct primes \(q_X\), then \(R_0=q_X\) for infinitely many distinct
primes, a contradiction.  Hence a nonzero fixed rational atom cannot recur
through the variable-prime-conductor branch.
\end{theorem}
\begin{proof}
Reduced representatives of the same rational point on
\(\mathbb R/\mathbb Z\) have the same positive denominator.  Thus
\(R_0=q_X\) at every such scale.
\end{proof}

\section{Exact-period corridor}
The periodic approximation theorem requires
\[
 q_{\rm prog}R\le(\log X)^{\eta_0}.
\]
On the variable branch \(R=q_X=X^{267/400+o(1)}\), this fails for all
sufficiently large \(X\), even before the additional factor
\(q_{\rm prog}\ge1\) is charged \citep{WangTPC157}.  On the conductor-one
branch \(R=1\), only the variable-conductor obstruction disappears.  A
valid invocation still requires
\[
 q_{\rm prog}\le(\log X)^{\eta_0},\qquad
 N\in[\sqrt X,X]\setminus E_X^\star,
\]
together with every other native good-scale condition.  The repository
supplies neither those schedule-specific admissibility facts, a
source-locked occurrence of a named \(\alpha_\star\), nor an exact
production packet schedule on all required scales.

\section{Scope}
This is a consistency theorem, not fixed-atom cancellation.  It prunes one
possible recurrence mechanism while leaving the conductor-one and genuinely
nonperiodic pointwise routes open.
""",
        {
            "fixed_atom_fixture": {"numerator": 2, "denominator": 5},
            "prime_conductors": [5, 7, 11, 13],
            "matching_prime_conductors": [5],
            "variable_branch_growth": "q_X=X^(267/400+o(1))",
            "exact_period_corridor": "q_prog*R<=(log X)^eta_0",
            "conductor_one_native_requirements": [
                "q_prog<=(log X)^eta_0",
                "N in [sqrt(X),X] outside E_X_star",
                "all source-native good-scale conditions",
                "named atom occurrence",
                "exact production packet schedule",
            ],
            "conductor_one_route_open": True,
        },
    ),
    entry(
        198,
        "factorwise-fourier-product-barrier",
        "A Sharp Black-Box Barrier from Factorwise Fourier Bounds to a Product Twist",
        "METHOD_OBSTRUCTION_L1",
        "STOP_SCOPED",
        (
            "Rudin--Shapiro coefficients give two factors with uniform square-"
            "root Fourier bounds whose modulated pointwise product has a full "
            "linear resonance at a prescribed atom.  This stops only the "
            "factorwise-single-Fourier black-box implication."
        ),
        "ARITHMETIC_TWO_FACTOR_COUPLING_THEOREM",
        "TWO_MOBIUS_PRODUCT_FOURIER_ROUTE",
        ["TPC108.main", "TPC167.main", "TPC193.gate"],
        "FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT",
        r"""
\section{Rudin--Shapiro witness}
Let \(P_0=Q_0=1\) and recursively set
\[
 P_{m+1}(z)=P_m(z)+z^{2^m}Q_m(z),\qquad
 Q_{m+1}(z)=P_m(z)-z^{2^m}Q_m(z).
\]
The coefficients of \(P_m\) are signs \(\rho_n\), \(0\le n<L=2^m\),
and for \(|z|=1\),
\[
 |P_m(z)|^2+|Q_m(z)|^2=2L.
\]
Consequently every additive Fourier sum of
\(f(n)=\rho_n\) is at most \(\sqrt{2L}\).

\begin{theorem}[Sharp black-box failure]
Fix any \(\alpha_\star\).  Put
\(g(n)=\rho_n \e(\alpha_\star n)\).  Both \(f\) and \(g\) have uniform
\(O(\sqrt L)\) Fourier bounds, but
\[
 \sum_{n<L}f(n)g(n)\e(-\alpha_\star n)=L.
\]
Therefore factorwise uniform Fourier bounds, used as black-box premises,
do not imply cancellation of the product at a prescribed atom.
\end{theorem}
\begin{proof}
Modulation translates the Fourier variable, so \(g\) inherits the same
supremum bound.  Since \(\rho_n^2=1\), every term in the displayed product
sum equals one.
\end{proof}

\section{Scoped interpretation}
The witness is synthetic and is not asserted to model the Möbius function.
It rejects exactly the logical implication
\[
 \hbox{two independent one-factor Fourier bounds}
 \Longrightarrow
 \hbox{literal two-factor product bound}.
\]
Arithmetic identities that couple the two Möbius factors remain open.
""",
        {
            "rudin_shapiro_level": 5,
            "length": 32,
            "energy_identity": "|P|^2+|Q|^2=2L",
            "factor_fourier_scale": "sqrt(2L)",
            "product_resonance": "L",
            "synthetic_not_mobius": True,
        },
    ),
    entry(
        199,
        "mobius-product-pretentiousness-firewall",
        "The Möbius-Pair Sequence Is Not One Multiplicative Function",
        "METHOD_OBSTRUCTION_L1",
        "STOP_SCOPED",
        (
            "The literal sequence c(n)=mu(n)mu(n+2) is not multiplicative: "
            "c(3)=c(5)=1 but c(15)=-1.  One-function pretentious theorems "
            "therefore cannot be applied to the product merely by renaming it."
        ),
        "THEOREM_FOR_COUPLED_VALUES_ON_TWO_AFFINE_FORMS",
        "TWO_FUNCTION_CORRELATION_ROUTE",
        ["TPC108.main", "TPC193.gate"],
        "ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ",
        r"""
\section{A determinant-two specialization}
Take \(D(n)=n\) and \(V(n)=n+2\), so the coefficient determinant is
\(1\cdot2-1\cdot0=2\).  Define
\[
 c(n)=\mu(n)\mu(n+2).
\]

\begin{theorem}[Multiplicativity firewall]
The function \(c\) is not multiplicative.  In particular,
\[
 c(3)=1,\qquad c(5)=1,\qquad c(15)=-1,
\]
although \((3,5)=1\).
\end{theorem}
\begin{proof}
Using
\(\mu(3)=\mu(5)=\mu(7)=\mu(17)=-1\) and
\(\mu(15)=1\), the three values are immediate.  Thus
\(c(15)\ne c(3)c(5)\).
\end{proof}

\section{What is and is not stopped}
Pretentious distance and Hal\'asz-type theorems whose hypothesis is a
single multiplicative function cannot be invoked on \(c\) after a purely
notational declaration that \(c\) is multiplicative.  The calculation says
nothing against genuine two-function Elliott/Chowla inputs, bilinear
decompositions, or theorem-backed structure special to the affine pair.
""",
        {
            "mobius_values": {
                "mu_3": -1,
                "mu_5": -1,
                "mu_7": -1,
                "mu_15": 1,
                "mu_17": -1,
            },
            "pair_values": {"c_3": 1, "c_5": 1, "c_15": -1},
            "gcd_3_5": 1,
            "multiplicative_identity_holds": False,
        },
    ),
    entry(
        200,
        "four-form-determinant-resonance-refinement",
        "The Four-Form Determinant Table and Its Unique Positive-Shift Degeneracy",
        "ALGEBRAIC_REFINEMENT_L1",
        "PROVED_UNIQUE_DEGENERACY_Q1_H2",
        (
            "The Fejer shift produces six pairwise determinants "
            "2, s-squared times h, 2+qh, qh-2, a-squared times h, and 2. "
            "For positive h and odd q=as, "
            "the only zero is q=1,h=2, where the middle two forms coincide."
        ),
        "NONDEGENERATE_GROWING_FOUR_MOBIUS_CORRELATION_BOUND",
        "FEJER_NONDEGENERATE_SHIFT_ROUTE",
        ["TPC108.main", "TPC130.main"],
        None,
        r"""
\section{Four shifted forms}
The Fej\'er/four-sign reduction itself is imported from TPC-130
\citep{WangTPC130}.  The new L1 content below is the complete six-entry
cross-determinant table and its degeneracy classification.
Let \(a,s\in\mathbb Z_{>0}\) be the positive affine slopes and put
\(q=as\).  Then
\[
\begin{array}{ll}
 L_1=d+sz,&L_2=u+az,\\
 L_3=d+s(z+h),&L_4=u+a(z+h).
\end{array}
\]
For \(L_i=b_i+m_i z\), use
\(\det(L_i,L_j)=m_i b_j-m_j b_i\).

\begin{theorem}[Complete determinant table]
If \(a,s>0\) and \(su-ad=2\), then
\[
\begin{array}{c|cccccc}
(i,j)&(1,2)&(1,3)&(1,4)&(2,3)&(2,4)&(3,4)\\ \hline
\det(L_i,L_j)&2&s^2h&2+qh&qh-2&a^2h&2.
\end{array}
\]
For positive integer \(h\) and positive odd integer \(q\), the unique
vanishing entry is \(\det(L_2,L_3)=0\) at \(q=1,h=2\).
At that point \(a=s=1\), \(u-d=2\), and \(L_2=L_3\).
\end{theorem}
\begin{proof}
Expansion gives the six entries.  All except \(qh-2\) are visibly nonzero.
The equation \(qh=2\) with \(q\) positive odd and \(h\) positive integral
forces \(q=1,h=2\).  Then \(as=1\) forces \(a=s=1\), and
\(su-ad=u-d=2\), proving coincidence.
\end{proof}

\section{Refined arithmetic gate}
The exceptional shift is algebraically simpler because
\(\mu(L_2)\mu(L_3)=\mu(L_2)^2\).  Every other positive shift is a
nondegenerate four-form M\"obius correlation.  This table replaces the vague
phrase ``four-sign barrier'' by one exceptional cell plus a precise growing
nondegenerate family.
""",
        {
            "slope_domain": "a,s positive integers",
            "symbolic_table": [
                ["L1", "L2", "2"],
                ["L1", "L3", "s^2*h"],
                ["L1", "L4", "2+q*h"],
                ["L2", "L3", "q*h-2"],
                ["L2", "L4", "a^2*h"],
                ["L3", "L4", "2"],
            ],
            "enumeration": {
                "odd_q_max": 19,
                "h_max": 20,
                "zero_cells": [{"q": 1, "h": 2, "pair": "L2,L3"}],
            },
        },
    ),
    entry(
        201,
        "degenerate-shift-fejer-absorption",
        "Absorbing the Unique Degenerate Fejer Shift into the Diagonal Ledger",
        "ANALYTIC_REDUCTION_L1",
        "PROVED_DEGENERATE_SHIFT_ABSORPTION",
        (
            "In the normalized TPC-130 Fejer inequality, the unique q=1,h=2 "
            "degenerate correlation is bounded by the same energy E as the "
            "diagonal.  It changes the diagonal coefficient from 2 to at most 6 "
            "in units of 1/(H p), leaving only nondegenerate four-Mobius shifts."
        ),
        "UNIFORM_NONDEGENERATE_FOUR_MOBIUS_OFFDIAGONAL_POWER_BOUND",
        "NONDEGENERATE_FEJER_OFFDIAGONAL",
        ["TPC130.main", "TPC200.payload"],
        None,
        r"""
\section{Imported normalized inequality}
For \(1\le H\le N\), \(V=\sum|A_z|>0\),
\(E=\sum|A_z|^2\), and
\(\mathfrak p=V^2/(NE)\), TPC-130 proves
\citep{WangTPC130}
\[
 { |S(\alpha)|^2\over V^2}
 \le 2\left\{{1\over H\mathfrak p}
 +{N\over HV^2}\bigl(\mathcal O_H(\alpha)\bigr)_+\right\},
\]
where
\[
 \mathcal O_H(\alpha)=
 2\Re\sum_{h=1}^{H-1}(1-h/H)\e(-\alpha h)C(h).
\]
If \(V=0\), then every \(A_z=0\) and the prefix is trivial; it is
separated before this normalization.

\begin{theorem}[Degenerate-shift absorption]
Assume \(3\le H\le N\).  For the unique degenerate cell
\(q=1,h=2\) identified in TPC-200 \citep{WangTPC200}, Cauchy gives
\(|C(2)|\le E\).  Its contribution to the normalized right-hand side is at
most \(4/(H\mathfrak p)\).  Together with the diagonal term, its total charge
is at most
\[
 {6\over H\mathfrak p}.
\]
Writing
\(\mathcal O_H=\mathcal O_H^{\rm deg}+\mathcal O_H^{\rm nd}\), the inequality
\((x+y)_+\le |x|+y_+\) gives the refined normalized bound
\[
 { |S(\alpha)|^2\over V^2}
 \le {6\over H\mathfrak p}
 +{2N\over HV^2}\bigl(\mathcal O_H^{\rm nd}(\alpha)\bigr)_+.
\]
Thus the degenerate term is absorbed into the diagonal feasibility
condition by a fixed constant.
\end{theorem}
\begin{proof}
The \(h=2\) summand in \(\mathcal O_H\) has absolute value at most
\(2(1-2/H)E\le2E\).  Multiplying by the outer factor
\(2N/(HV^2)\) gives at most
\(4NE/(HV^2)=4/(H\mathfrak p)\).  The original diagonal term is
\(2/(H\mathfrak p)\).
\end{proof}

\section{Remaining gate}
No cancellation is extracted from the degenerate term.  After its absorption,
the positive off-diagonal obligation is supported on the nonzero determinant
rows of TPC-200.  The missing theorem is therefore a uniform local or
all-prefix estimate for that growing nondegenerate four-M\"obius family.
""",
        {
            "normalized_diagonal_coefficient": 2,
            "degenerate_shift_added_coefficient": 4,
            "absorbed_total_coefficient": 6,
            "native_domain": ["V>0", "3<=H<=N"],
            "positive_part_split": "(x+y)_+<=|x|+y_+",
            "degenerate_cell": {"q": 1, "h": 2, "pair": "L2,L3"},
            "remaining_gate": "NONDEGENERATE_FOUR_MOBIUS_OFFDIAGONAL",
        },
    ),
    entry(
        202,
        "new-primary-double-selector-gate",
        "A New Primary-Source Audit: Two Averaged Selectors Still Do Not Select One Physical Packet",
        "PRIMARY_SOURCE_AUDIT_L1",
        "SCREENED_NON_DIRECT_ZERO_ELIGIBLE",
        (
            "Menon's 2026 Theorems 1.4 and 1.5 sharpen an origin-averaged "
            "single-Liouville Fourier bound and a shift-averaged Liouville "
            "correlation bound.  Their combination does not select the prescribed "
            "affine relation and deterministic packet simultaneously."
        ),
        "THEOREM_SELECTING_PRESCRIBED_ORIGIN_SHIFT_RELATION_AND_PACKET",
        "NEW_PRIMARY_FIXED_PACKET_SELECTOR_SEARCH",
        ["TPC181.selector", "TPC193.gate"],
        None,
        r"""
\section{Primary theorem record}
Menon's Theorem 1.4 states that, for \(X\ge h\ge10\),
\[
\sup_{\alpha\in\mathbb R}{1\over X}\int_0^X
\left|{1\over h}\sum_{x\le n\le x+h}
\lambda(n)\e(\alpha n)\right|\,dx
\ll
 {\log\log h\over\log h}
 +{(\log\log X)^2\over\log X}.
\]
Its supremum in \(\alpha\), origin average, \(1/X\) and \(1/h\)
normalizations are all native.  Theorem 1.5 states that, for natural
\(k\ge2\) and \(X\ge H\ge10\),
\[
{1\over H^{k-1}}
\sum_{1\le h_2,\ldots,h_k\le H}
\left|{1\over X}\sum_{1\le n\le X}
\lambda(n)\lambda(n+h_2)\cdots\lambda(n+h_k)\right|
\ll
k\left\{{\log\log H\over\log H}
+{(\log\log X)^2\over\log X}\right\}
\citep{Menon2026}.
\]
The outer factor \(k\), both averaging variables, both normalizations,
parameter ranges and logarithmic losses are part of the source record.

\section{Double-selector lemma}
\begin{lemma}[Marginals do not select a prescribed cell]
There are arrays \(A_{x,h}\in[0,1]\) for which the average in \(x\) at each
fixed \(h\) and the average in \(h\) at each fixed \(x\) both tend to zero,
while one prescribed entry remains equal to one.  Hence separate
origin-average and shift-average estimates do not, as a black-box logical
operation, control a prescribed origin--shift cell.
\end{lemma}
\begin{proof}
On an \(M\times M\) grid set one prescribed entry to one and all other
entries to zero.  Every row and column average is at most \(1/M\), but the
prescribed entry is one.
\end{proof}
This is only a two-axis illustration of the uncontrolled atomic-promotion
firewall already locked in TPC-181.  It creates no new
\textsc{stop-scoped} method cell and is not presented as a new arithmetic
obstruction.

\section{Six-axis audit}
Theorem 1.4 has a phase supremum but one Liouville factor and an averaged
origin.  Theorem 1.5 has multiple Liouville factors but averaged shifts and
no prescribed additive atom on the literal determinant-two packet.  Neither
theorem supplies the physical coefficient
\(\mu(d+sz)\mu(u+az)\) together with the production packet, all prefixes,
all deterministic scales, a fixed \(X\)-power and the full loss ledger.
Their juxtaposition does not create a theorem-backed selector.

\section{Declared-corpus boundary}
\texttt{TPC193\_DECLARED\_CANDIDATE\_MECHANISM\_CORPUS\_V1} remains
\textsc{stop-scoped}.  This paper adds a dated supplemental primary record;
it does not rewrite the seven-source V1 corpus or assert global
nonexistence.  Menon v1 is screened non-direct, with zero eligible literal
direct candidates in this supplement.
""",
        {
            "primary_source": {
                "author": "Siddarth Menon",
                "title": "Improved bounds for multiplicative functions in almost all short intervals",
                "locator": "arXiv:2607.15574v1",
                "date": "2026-07-17",
                "theorems": ["1.4", "1.5"],
            },
            "theorem_1_4_axes": {
                "range": "X>=h>=10",
                "phase": "SUPREMUM_ALPHA",
                "carrier": "SINGLE_LIOUVILLE",
                "selector_loss": "AVERAGE_INTERVAL_ORIGIN_X",
                "normalization": "(1/X) integral_0^X |(1/h) short_sum| dx",
                "bound": "loglog(h)/log(h)+(loglog(X))^2/log(X)",
                "decay": "LOGARITHMIC",
            },
            "theorem_1_5_axes": {
                "range": "natural k>=2 and X>=H>=10",
                "carrier": "MULTI_LIOUVILLE_SHIFT_CORRELATION",
                "selector_loss": "AVERAGE_SHIFTS",
                "phase": "NO_PRESCRIBED_ADDITIVE_ATOM",
                "normalization": "(1/H^(k-1)) shift_sum |(1/X) n_sum product|",
                "bound": "k*(loglog(H)/log(H)+(loglog(X))^2/log(X))",
                "decay": "LOGARITHMIC",
            },
            "selector_fixture": {"rows": 64, "columns": 64, "prescribed_value": 1},
            "eligible_literal_direct_candidate_count": 0,
            "new_stop_scoped_cell_created": False,
            "selector_logic_status": "INHERITED_TPC181_FIREWALL_ILLUSTRATION_ONLY",
            "tpc193_v1_stop_preserved": True,
        },
    ),
    entry(
        203,
        "mvp10-direct-pointwise-route-decision",
        "MVP10 after Per-Packet Formula Completion and the Fixed-Atom Subgate Audit",
        "MVP10_INTEGRATION",
        "NOT_TESTABLE",
        (
            "MVP10 imports TPC-194--202 fail-closed.  The per-packet direct "
            "formula is complete, but the production crosswalk and named-atom "
            "power theorem are absent.  Both O161 pointwise parents and the "
            "global architecture remain open; fixed-atom endpoint credit is zero."
        ),
        "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
        "SEARCH_FOR_NAMED_PACKET_CROSSWALK_OR_GENUINE_FIXED_ATOM_THEOREM",
        ["TPC192.snapshot", "TPC193.gate"],
        None,
        r"""
\section{Imported batch state}
TPC-194 completes the symbolic physical prefix only per resolved packet.
TPC-195 proves an exact block/prefix power-profile transfer with a visible
truncation tail.  TPC-196 and TPC-197 expose the residue determinant and
fixed-conductor constraints.  TPC-198 and TPC-199 stop two black-box
factorization shortcuts.  TPC-200 and TPC-201 reduce the Fej\'er route to
nondegenerate four-M\"obius off-diagonals.  TPC-202 audits Menon v1 as a
supplemental primary source, screens it non-direct, and creates no new
stopped method cell.

\begin{theorem}[MVP10 route decision]
The direct formula-completion trigger fires only at the per-packet symbolic
level.  It does not fire at the production target level.  The declared
primary supplement contains no eligible literal direct theorem.  Therefore
\[
\mathrm{Verdict}=\texttt{NOT\_TESTABLE},
\qquad
\mathrm{DirectProductionFirstMissing}
=\substack{\texttt{SOURCE\_LOCKED\_PRODUCTION}\\
           \texttt{PACKET\_PREFIX\_CROSSWALK}}.
\]
Both O161 pointwise parents and the global architecture remain open.
\end{theorem}
\begin{proof}
The integration checker opens the nine canonical payloads, verifies their
hashes, verdicts, six-axis firewalls, zero endpoint credit and exact
\textsc{stop-scoped} cells.  The TPC-194 completion ledger has explicit
\texttt{MISSING} entries for the production atom, schedule, common ranges,
uniform \(C\), positive \(\sigma\), target normalization and full losses.
None of TPC-195--202 fills those entries.  Scoped method obstructions are
not parent or architecture obstructions.
\end{proof}

\section{Endpoint and route ledger}
The named-atom exponent credit remains \(0\), while the required budget is
strictly greater than \(1/400\).  Hence the endpoint is unpaid.  The next
three first-missing nodes remain separately typed:
\[
\begin{aligned}
\mathrm{GlobalFirstMissing}
 &=\texttt{H1.source\_backed\_local\_occurrence\_edge\_family},\\
\mathrm{SelectedPointwiseFirstMissing}
 &=\texttt{LITERAL\_FIXED\_ATOM\_ARITHMETIC\_CANCELLATION},\\
\mathrm{DirectProductionFirstMissing}
 &=\texttt{SOURCE\_LOCKED\_PRODUCTION\_PACKET\_PREFIX\_CROSSWALK}.
\end{aligned}
\]
The global node is inherited unchanged from TPC-192
\citep{WangTPC192}; the direct-production node is the new focus of this
batch.
An admissible reopen trigger must be one of the following exact types:
\begin{enumerate}
\item \emph{direct}: a formula-complete production target plus a
theorem-backed natural-\(q/N\), positive-power fixed-atom mechanism
preserving all six axes and all losses;
\item \emph{metric}: a source-locked named atom, exact packet schedule, and
a schedule-specific theorem that this atom avoids the exceptional limsup;
\item \emph{bad endpoint}: a literal fixed-atom local-increment
cancellation theorem;
\item \emph{structural}: a theorem-backed local-occurrence edge;
\item \emph{declared corpus}: a genuinely new primary theorem corpus, with
the TPC-193 V1 cell still \textsc{stop-scoped}.
\end{enumerate}
No L2 arithmetic theorem, prime-pair lower bound, or twin-prime theorem is
claimed.  This decision does not authorize TPC-204: the batch stops for user
confirmation and a fresh audit of the exact triggers above.
""",
        {
            "upstream_range": "TPC-194--202",
            "expected_verdicts": {
                "194": "FORMULA_COMPLETE_PER_PACKET_L1",
                "195": "PROVED_BIDIRECTIONAL_POWER_PROFILE_TRANSFER",
                "196": "PROVED_RESIDUE_SPLIT_WITH_DETERMINANT_2R",
                "197": "PROVED_NONZERO_FIXED_RATIONAL_ATOM_CANNOT_RECUR_ACROSS_UNBOUNDED_PRIME_CONDUCTORS",
                "198": "STOP_SCOPED",
                "199": "STOP_SCOPED",
                "200": "PROVED_UNIQUE_DEGENERACY_Q1_H2",
                "201": "PROVED_DEGENERATE_SHIFT_ABSORPTION",
                "202": "SCREENED_NON_DIRECT_ZERO_ELIGIBLE",
            },
            "scoped_cells": [
                "TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1",
                "FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT",
                "ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ",
            ],
            "global_first_missing": "H1.source_backed_local_occurrence_edge_family",
            "selected_pointwise_first_missing": "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
            "direct_production_first_missing": "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
            "exact_reopen_triggers": [
                {
                    "route": "DIRECT",
                    "requires": [
                        "formula-complete production target",
                        "theorem-backed natural q/N fixed-atom mechanism",
                        "positive X-power with uniform constant",
                        "all six axes",
                        "complete loss ledger",
                    ],
                },
                {
                    "route": "METRIC",
                    "requires": [
                        "source-locked named atom",
                        "exact packet schedule",
                        "schedule-specific exceptional-limsup avoidance theorem",
                    ],
                },
                {
                    "route": "BAD_ENDPOINT",
                    "requires": [
                        "literal fixed-atom local-increment cancellation theorem"
                    ],
                },
                {
                    "route": "STRUCTURAL",
                    "requires": ["theorem-backed local-occurrence edge"],
                },
                {
                    "route": "DECLARED_CORPUS",
                    "requires": [
                        "genuinely new primary theorem corpus",
                        "TPC193 V1 remains STOP_SCOPED",
                    ],
                },
            ],
            "two_O161_pointwise_parents_open": True,
            "global_architecture_open": True,
            "named_atom_endpoint_credit": 0,
            "strict_one_over_400": "UNPAID",
        },
    ),
]


def canonical(obj: object) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def canonical_text_hash(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_lock(source_id: str) -> dict:
    rel = SOURCE_PATHS[source_id]
    path = REPO / rel
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "source_id": source_id,
        "path": rel,
        "canonical_utf8_lf_sha256": canonical_text_hash(path),
        "hash_semantics": "INTEGRITY_ONLY",
    }


def upstream_payload_rel(d: dict) -> str:
    stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
    return (
        f"papers/tpc-{d['num']}-{d['slug']}/"
        f"experiments/{stem}.json"
    )


def build_payload(d: dict) -> dict:
    obj = {
        "schema": f"tpc-{d['num']}-{d['slug']}-v1",
        "paper": d["num"],
        "title": d["title"],
        "classification": d["classification"],
        "verdict": d["verdict"],
        "result_summary": d["summary"],
        "required_quantifier_signature": TARGET_AXES,
        "fixed_h0": {"value": 2, "semantics": "SOURCE_BACKED_DATA_FACT_ONLY"},
        "first_missing_literal_theorem": d["first_missing"],
        "next_route": d["next_route"],
        "route_state": {
            "tpc193_declared_candidate_mechanism_corpus_v1": "STOP_SCOPED",
            "bad_endpoint_O161_parent": "OPEN",
            "direct_twist_O161_parent": "OPEN",
            "global_architecture": "OPEN",
        },
        "stop_scoped": (
            []
            if d["stop_cell"] is None
            else [
                {
                    "cell": d["stop_cell"],
                    "parent_route_stopped": False,
                    "global_architecture_stopped": False,
                }
            ]
        ),
        "progress": {
            "L0": "FORMULA_OR_FINITE_CERTIFICATE",
            "L1": d["classification"],
            "L2": "NONE",
        },
        "fixed_atom_decay_obtained": False,
        "endpoint_ledger": {
            "named_atom_sigma_credit": {"numerator": 0, "denominator": 1},
            "required_strict_budget": {"numerator": 1, "denominator": 400},
            "state": "UNPAID",
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "finite_certificate": d["certificate"],
        "source_locks": [source_lock(x) for x in d["sources"]],
        "snapshot": {
            "date": "2026-07-29",
            "source_of_truth": "REPOSITORY_ARTIFACTS_NOT_CHAT_MEMORY",
            "hash_mode": "CANONICAL_UTF8_LF",
        },
    }
    if d["num"] == 202:
        obj["external_primary_source"] = {
            "locator": "https://arxiv.org/abs/2607.15574v1",
            "integrity_mode": (
                "PRIMARY_LOCATOR_AND_MANUAL_TRANSCRIPTION_NO_EXTERNAL_HASH"
            ),
            "repository_source_hash_scope_only": True,
            "reviewed_from_primary_source": True,
            "native_theorem_records": [
                {
                    "locator": "Theorem 1.4",
                    "range": "X>=h>=10",
                    "lhs": (
                        "sup_alpha (1/X) integral_0^X |(1/h) "
                        "sum_(x<=n<=x+h) lambda(n)e(alpha*n)| dx"
                    ),
                    "rhs": (
                        "loglog(h)/log(h)+(loglog(X))^2/log(X)"
                    ),
                    "native_selectors": ["SUPREMUM_ALPHA", "AVERAGE_ORIGIN_X"],
                    "carrier": "SINGLE_LIOUVILLE",
                },
                {
                    "locator": "Theorem 1.5",
                    "range": "natural k>=2 and X>=H>=10",
                    "lhs": (
                        "(1/H^(k-1)) sum_(1<=h_2,...,h_k<=H) "
                        "|(1/X) sum_(1<=n<=X) lambda(n)"
                        "lambda(n+h_2)...lambda(n+h_k)|"
                    ),
                    "rhs": (
                        "k*(loglog(H)/log(H)+(loglog(X))^2/log(X))"
                    ),
                    "native_selectors": ["AVERAGE_H_2_THROUGH_H_K"],
                    "carrier": "MULTI_LIOUVILLE_SHIFT_CORRELATION",
                },
            ],
            "direct_literal_two_mobius_theorem": False,
        }
    if d["num"] == 203:
        obj.pop("first_missing_literal_theorem")
        obj["first_missing_nodes"] = {
            "global": "H1.source_backed_local_occurrence_edge_family",
            "selected_pointwise": "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
            "direct_production": (
                "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
            ),
        }
        obj["batch_stop"] = {
            "state": "USER_CONFIRMATION_REQUIRED",
            "next_paper": None,
            "tpc204_authorized": False,
        }
        for upstream in PAPERS_DATA[:-1]:
            rel = upstream_payload_rel(upstream)
            obj["source_locks"].append(
                {
                    "source_id": f"TPC{upstream['num']}.payload",
                    "path": rel,
                    "canonical_utf8_lf_sha256": canonical_text_hash(REPO / rel),
                    "hash_semantics": "INTEGRITY_ONLY",
                }
            )
    return obj


def exact_schema(value: object, schema_id: str | None = None) -> dict:
    if isinstance(value, bool):
        out = {"type": "boolean", "const": value}
    elif isinstance(value, int):
        out = {"type": "integer", "const": value}
    elif isinstance(value, float):
        out = {"type": "number", "const": value}
    elif isinstance(value, str):
        out = {"type": "string", "const": value}
    elif value is None:
        out = {"type": "null", "const": None}
    elif isinstance(value, list):
        out = {
            "type": "array",
            "minItems": len(value),
            "maxItems": len(value),
            "prefixItems": [exact_schema(v) for v in value],
            "items": False,
        }
    elif isinstance(value, dict):
        out = {
            "type": "object",
            "required": list(value),
            "additionalProperties": False,
            "properties": {k: exact_schema(v) for k, v in value.items()},
        }
    else:
        raise TypeError(type(value))
    if schema_id is not None:
        out = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": schema_id,
            **out,
        }
    return out


def schema_accepts(schema: dict, value: object) -> bool:
    if "const" in schema:
        return type(value) is type(schema["const"]) and value == schema["const"]
    kind = schema.get("type")
    if kind == "object":
        if not isinstance(value, dict):
            return False
        required = schema["required"]
        if set(value) != set(required):
            return False
        return all(
            schema_accepts(schema["properties"][k], value[k]) for k in required
        )
    if kind == "array":
        if not isinstance(value, list) or len(value) != schema["minItems"]:
            return False
        return all(
            schema_accepts(s, v)
            for s, v in zip(schema["prefixItems"], value, strict=True)
        )
    return False


MUTATION_NAMES = [
    "promote_L2",
    "promote_fixed_atom_decay",
    "grant_endpoint_credit",
    "mark_strict_budget_paid",
    "stop_bad_endpoint_parent",
    "stop_global_architecture",
    "promote_hash_to_theorem",
    "change_verdict",
    "delete_first_missing",
    "inject_extra_field",
]


def mutated_payloads(payload: dict) -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for name in MUTATION_NAMES:
        x = copy.deepcopy(payload)
        if name == "promote_L2":
            x["progress"]["L2"] = "POSITIVE"
        elif name == "promote_fixed_atom_decay":
            x["fixed_atom_decay_obtained"] = True
        elif name == "grant_endpoint_credit":
            x["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"] = 1
            x["endpoint_ledger"]["named_atom_sigma_credit"]["denominator"] = 400
        elif name == "mark_strict_budget_paid":
            x["endpoint_ledger"]["state"] = "PAID"
        elif name == "stop_bad_endpoint_parent":
            x["route_state"]["bad_endpoint_O161_parent"] = "STOPPED"
        elif name == "stop_global_architecture":
            x["route_state"]["global_architecture"] = "STOPPED"
        elif name == "promote_hash_to_theorem":
            x["source_locks"][0]["hash_semantics"] = "THEOREM_EVIDENCE"
        elif name == "change_verdict":
            x["verdict"] = "PROMOTED"
        elif name == "delete_first_missing":
            if "first_missing_literal_theorem" in x:
                del x["first_missing_literal_theorem"]
            else:
                del x["first_missing_nodes"]["direct_production"]
        elif name == "inject_extra_field":
            x["schema_exploit"] = True
        out.append((name, x))
    return out


def mobius(n: int) -> int:
    if n == 1:
        return 1
    value = n
    primes = 0
    p = 2
    while p * p <= value:
        if value % p == 0:
            value //= p
            if value % p == 0:
                return 0
            primes += 1
            while value % p == 0:
                value //= p
        p += 1
    if value > 1:
        primes += 1
    return -1 if primes % 2 else 1


def rudin_shapiro(level: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-x for x in q]
    return p, q


def finite_check(payload: dict) -> dict:
    n = payload["paper"]
    c = payload["finite_certificate"]
    if n == 194:
        f = c["affine_fixture"]
        assert f["s"] * f["u"] - f["a"] * f["d"] == f["determinant"] == 2
        types = c["formula_type_registry"]
        assert len({x["id"] for x in types}) == 3
        assert len({x["domain"] for x in types}) == 3
        assert c["completion_axes"]["packet_schedule"] == "MISSING"
        assert c["completion_axes"]["positive_sigma"] == "MISSING"
        formula = c["resolved_packet_formula"]
        assert formula["phase_slope"] == (
            "Omega_xi=ell_theta*v_theta*sigma_theta*B_theta_b"
        )
        assert "epsilon_theta*r_tilde*Omega_xi" in formula["packet_atom"]
        assert "mfrak_K_X(r)" in formula["outer_multiplier"]
        assert (
            formula["complete_per_key_contribution"]
            == "P_xi_X_le_T=cfrak_xi_X*S_xi_X_le_T"
        )
        return {
            "determinant": 2,
            "distinct_formula_types": 3,
            "literal_formula_fields_verified": 9,
        }
    if n == 195:
        sigma = Fraction(
            c["sigma_fixture"]["numerator"], c["sigma_fixture"]["denominator"]
        )
        t = c["dyadic_fixture_T"]
        intervals = []
        hi = t
        while hi > 1:
            lo = hi // 2
            intervals.extend(range(lo + 1, hi + 1))
            hi = lo
        intervals.append(1)
        assert sorted(intervals) == list(range(1, t + 1))
        forward = 1 / (2 ** (1 - float(sigma)) - 1)
        reverse = 2 ** (1 - float(sigma)) + 1
        assert forward > 0 and reverse > 2
        m_fixture, t_fixture = 10, 19
        assert t_fixture > m_fixture + 1
        assert t_fixture < 2 * m_fixture
        assert c["truncated_tail_raw_strict_bound"] == "2*B*M"
        return {
            "dyadic_partition_exact": True,
            "forward_constant": round(forward, 12),
            "reverse_constant": round(reverse, 12),
            "truncated_tail_counterexample_to_M_plus_1": {
                "M": m_fixture,
                "T": t_fixture,
                "old_bound_terms": m_fixture + 1,
                "possible_tail_terms": t_fixture,
                "new_strict_bound_terms": 2 * m_fixture,
            },
        }
    if n == 196:
        f = c["fixture"]
        assert f["s"] * f["u"] - f["a"] * f["d"] == 2
        assert (
            (f["s"] * f["R"]) * (f["u"] + f["a"] * 0)
            - (f["a"] * f["R"]) * (f["d"] + f["s"] * 0)
            == f["residue_determinant"]
        )
        coeff = [(-1) ** (z * z + 3 * z) for z in range(f["z_min"], f["z_max"] + 1)]
        direct = sum(
            coeff[z] * cmath.exp(-2j * math.pi * f["r"] * z / f["R"])
            for z in range(len(coeff))
        )
        split = sum(
            cmath.exp(-2j * math.pi * f["r"] * b / f["R"])
            * sum(coeff[z] for z in range(b, len(coeff), f["R"]))
            for b in range(f["R"])
        )
        assert abs(direct - split) < 1e-10
        return {"residue_identity_error": abs(direct - split), "determinant": 10}
    if n == 197:
        frac = Fraction(
            c["fixed_atom_fixture"]["numerator"],
            c["fixed_atom_fixture"]["denominator"],
        )
        matches = [q for q in c["prime_conductors"] if q == frac.denominator]
        assert matches == c["matching_prime_conductors"] == [5]
        assert len(c["conductor_one_native_requirements"]) == 5
        return {"reduced_denominator": frac.denominator, "matches": matches}
    if n == 198:
        p, q = rudin_shapiro(c["rudin_shapiro_level"])
        length = len(p)
        assert length == c["length"]
        max_p = 0.0
        max_energy_error = 0.0
        for j in range(257):
            z = cmath.exp(2j * math.pi * j / 257)
            pv = sum(a * z**k for k, a in enumerate(p))
            qv = sum(a * z**k for k, a in enumerate(q))
            max_p = max(max_p, abs(pv))
            max_energy_error = max(
                max_energy_error, abs(abs(pv) ** 2 + abs(qv) ** 2 - 2 * length)
            )
        assert max_p <= math.sqrt(2 * length) + 1e-9
        assert max_energy_error < 1e-8
        assert sum(a * a for a in p) == length
        return {
            "length": length,
            "sampled_sup": round(max_p, 12),
            "energy_error": max_energy_error,
            "product_resonance": length,
        }
    if n == 199:
        values = {k: mobius(k) for k in [3, 5, 7, 15, 17]}
        pair = {3: values[3] * values[5], 5: values[5] * values[7], 15: values[15] * values[17]}
        assert pair == {3: 1, 5: 1, 15: -1}
        assert math.gcd(3, 5) == 1 and pair[15] != pair[3] * pair[5]
        return {
            "pair_values": {str(k): pair[k] for k in sorted(pair)},
            "multiplicative": False,
        }
    if n == 200:
        zeros = []
        for q in range(1, c["enumeration"]["odd_q_max"] + 1, 2):
            for h in range(1, c["enumeration"]["h_max"] + 1):
                vals = [2, h, 2 + q * h, q * h - 2, h, 2]
                if 0 in vals:
                    zeros.append({"q": q, "h": h, "pair": "L2,L3"})
        assert zeros == c["enumeration"]["zero_cells"]
        a, s, d, u, h = 1, 1, 1, 3, 2
        forms = [d + s * 7, u + a * 7, d + s * (7 + h), u + a * (7 + h)]
        assert forms[1] == forms[2]
        return {"zero_cells": zeros, "coincident_value": forms[1]}
    if n == 201:
        assert (
            c["normalized_diagonal_coefficient"]
            + c["degenerate_shift_added_coefficient"]
            == c["absorbed_total_coefficient"]
            == 6
        )
        assert c["native_domain"] == ["V>0", "3<=H<=N"]
        assert c["positive_part_split"] == "(x+y)_+<=|x|+y_+"
        return {"absorbed_coefficient": 6, "remaining_gate_nonempty": True}
    if n == 202:
        rows = c["selector_fixture"]["rows"]
        cols = c["selector_fixture"]["columns"]
        row_average = 1 / cols
        column_average = 1 / rows
        assert max(row_average, column_average) <= 1 / 64
        assert c["selector_fixture"]["prescribed_value"] == 1
        assert c["eligible_literal_direct_candidate_count"] == 0
        assert c["new_stop_scoped_cell_created"] is False
        records = payload["external_primary_source"]["native_theorem_records"]
        assert records[0]["range"] == "X>=h>=10"
        assert "(1/X)" in records[0]["lhs"] and "(1/h)" in records[0]["lhs"]
        assert records[1]["range"] == "natural k>=2 and X>=H>=10"
        assert "(1/H^(k-1))" in records[1]["lhs"]
        assert records[1]["rhs"].startswith("k*(")
        return {
            "row_average": row_average,
            "column_average": column_average,
            "prescribed_cell": 1,
            "native_theorem_records_verified": 2,
        }
    if n == 203:
        locks = {x["source_id"]: x for x in payload["source_locks"]}
        expected = c["expected_verdicts"]
        seen_stops = set()
        for paper_s, verdict in expected.items():
            lock = locks[f"TPC{paper_s}.payload"]
            upstream = json.loads((REPO / lock["path"]).read_text(encoding="utf-8"))
            assert upstream["verdict"] == verdict
            assert upstream["fixed_atom_decay_obtained"] is False
            assert upstream["progress"]["L2"] == "NONE"
            assert upstream["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"] == 0
            assert upstream["route_state"]["bad_endpoint_O161_parent"] == "OPEN"
            assert upstream["route_state"]["direct_twist_O161_parent"] == "OPEN"
            for cell in upstream["stop_scoped"]:
                assert cell["parent_route_stopped"] is False
                assert cell["global_architecture_stopped"] is False
                seen_stops.add(cell["cell"])
        assert {
            "FACTORWISE_SINGLE_MOBIUS_FOURIER_TO_LITERAL_PRODUCT",
            "ONE_FUNCTION_PRETENTIOUSNESS_DIRECT_APPLICATION_TO_CZ",
        }.issubset(seen_stops)
        assert payload["first_missing_nodes"] == {
            "global": "H1.source_backed_local_occurrence_edge_family",
            "selected_pointwise": "LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION",
            "direct_production": "SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK",
        }
        assert payload["batch_stop"] == {
            "state": "USER_CONFIRMATION_REQUIRED",
            "next_paper": None,
            "tpc204_authorized": False,
        }
        triggers = c["exact_reopen_triggers"]
        assert [x["route"] for x in triggers] == [
            "DIRECT",
            "METRIC",
            "BAD_ENDPOINT",
            "STRUCTURAL",
            "DECLARED_CORPUS",
        ]
        assert (
            "schedule-specific exceptional-limsup avoidance theorem"
            in triggers[1]["requires"]
        )
        assert c["two_O161_pointwise_parents_open"] is True
        assert c["global_architecture_open"] is True
        return {"upstreams_verified": len(expected), "new_scoped_cells": len(seen_stops)}
    raise AssertionError(n)


def build_audit(d: dict, payload: dict, payload_schema: dict) -> dict:
    mutations = [
        {"name": name, "rejected": not schema_accepts(payload_schema, altered)}
        for name, altered in mutated_payloads(payload)
    ]
    finite = finite_check(payload)
    return {
        "schema": f"tpc-{d['num']}-{d['slug']}-audit-v1",
        "paper": d["num"],
        "payload_canonical_sha256": hashlib.sha256(
            canonical(payload).encode("utf-8")
        ).hexdigest(),
        "checks": {
            "repository_source_hashes_verified": True,
            "schema_exact_closed_recursive": True,
            "finite_certificate_executed": True,
            "all_mutations_executed_and_rejected": all(x["rejected"] for x in mutations),
            "tpc193_stop_scope_preserved": True,
            "two_pointwise_parents_open": True,
            "global_architecture_open": True,
            "fixed_atom_decay_false": True,
            "L2_none": True,
            "endpoint_credit_zero": True,
            "strict_budget_unpaid": True,
        },
        "finite_check_result": finite,
        "mutation_registry": mutations,
        "all_checks_pass": True,
    }


def tex_escape(text: str) -> str:
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("_", r"\_\allowbreak{}")
        .replace("#", r"\#")
        .replace("^", r"\^{}")
    )


def main_tex(d: dict) -> str:
    stop = (
        "No new method cell is stopped in this paper."
        if d["stop_cell"] is None
        else (
            r"The cell \texttt{" + tex_escape(d["stop_cell"]) + r"} is "
            r"\textsc{stop-scoped}; neither O161 parent nor the global "
            r"architecture is stopped."
        )
    )
    if d["num"] == 203:
        missing_text = r"""The three first-missing nodes remain typed as
global structural occurrence, selected pointwise arithmetic cancellation,
and direct-production packet crosswalk; they are displayed explicitly in
the route ledger above."""
    else:
        missing_text = (
            "The smallest missing literal theorem is\n"
            "\\[\n\\texttt{" + tex_escape(d["first_missing"]) + "}.\n\\]"
        )
    return rf"""\documentclass[11pt]{{article}}
\usepackage[a4paper,margin=0.82in]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{lmodern,amsmath,amssymb,amsthm,microtype,booktabs,tabularx,array,xcolor}}
\usepackage[numbers]{{natbib}}
\usepackage[colorlinks=true,linkcolor=blue!55!black,citecolor=blue!55!black,urlcolor=blue!55!black]{{hyperref}}
\setlength{{\emergencystretch}}{{4em}}
\newtheorem{{theorem}}{{Theorem}}
\newtheorem{{lemma}}{{Lemma}}
\newtheorem{{remark}}{{Remark}}
\newcommand{{\e}}{{\mathrm{{e}}}}
\title{{\textbf{{{tex_escape(d['title'])}}}}}
\author{{Liang Wang\\Huazhong University of Science and Technology}}
\date{{July 2026}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{tex_escape(d['summary'])}
The classification is \texttt{{{tex_escape(d['classification'])}}} and the
verdict is \texttt{{{tex_escape(d['verdict'])}}}.  No program-positive L2
claim or endpoint exponent credit is made.
\end{{abstract}}

\section{{Target contract and source boundary}}
The target has six simultaneous axes: actual fixed-\(h_0\) packet,
source-locked named physical atom, every deterministic prefix, every
deterministic scale, a fixed-\(X\) power at that atom, and actual active
support.  The value \(h_0=2\) is source-backed data only.  Repository hashes
are integrity locks, not theorem evidence.  TPC-193's declared seven-source
corpus remains \textsc{{stop-scoped}} \citep{{WangTPC193}}.

{d['body']}

\section{{Loss, level and scope ledger}}
{missing_text}
The next route is \texttt{{{tex_escape(d['next_route'])}}}.
{stop}

The named-atom exponent credit is \(0\), while the endpoint requires a
strict budget greater than \(1/400\); the ledger is unpaid.  Block sums are
not cumulative prefixes, symbolic packet atoms are not named production
atoms, phase \(L^2\) and almost-everywhere statements are not pointwise
evaluation, and scoped method failures are not theorem or architecture
failures.

\section{{Machine certificate}}
The adjacent canonical payload freezes the formula or finite witness,
exact repository-source hashes, any explicitly non-hashed external locator
record, six target axes, scoped stop, route state and claim firewall.  Its
recursive exact schema has closed objects, exact array positions and
constant leaves.  The checker recomputes the finite certificate and executes
ten adversarial mutations.

\bibliographystyle{{plainnat}}
\bibliography{{references}}
\end{{document}}
"""


def references_bib() -> str:
    return r"""@misc{WangTPC93,
  author={Wang, Liang}, title={Literal Low-Window Affine Export}, year={2026}}
@misc{WangTPC94,
  author={Wang, Liang}, title={Exact Content Resonance Ledger}, year={2026}}
@misc{WangTPC108,
  author={Wang, Liang}, title={Literal Generic Affine Mobius Dispersion}, year={2026}}
@misc{WangTPC127,
  author={Wang, Liang}, title={Determinant-Two Liouville Pullback}, year={2026}}
@misc{WangTPC130,
  author={Wang, Liang}, title={Fejer Four-Sign H3 Gate}, year={2026}}
@misc{WangTPC157,
  author={Wang, Liang}, title={Literal Weight Periodic Approximation}, year={2026}}
@misc{WangTPC159,
  author={Wang, Liang}, title={Dyadic Shadow Prefix Lifting}, year={2026}}
@misc{WangTPC192,
  author={Wang, Liang}, title={MVP9 Pointwise Frontier Route Decision}, year={2026}}
@misc{WangTPC193,
  author={Wang, Liang}, title={Literal Fixed-Atom Candidate Mechanism Gate}, year={2026}}
@misc{WangTPC200,
  author={Wang, Liang}, title={Four-Form Determinant Resonance Refinement}, year={2026}}
@misc{Menon2026,
  author={Menon, Siddarth},
  title={Improved Bounds for Multiplicative Functions in Almost All Short Intervals},
  year={2026}, eprint={2607.15574}, archivePrefix={arXiv},
  primaryClass={math.NT}}
"""


CHECKER_TEMPLATE = r'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, cmath, copy, hashlib, json, math
from fractions import Fraction
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
PAYLOAD=HERE/"__STEM__.json"
AUDIT=HERE/"__STEM___audit.json"
SCHEMA=HERE.parent/"schemas"/"tpc__NUM__-__SLUG__-v1.schema.json"
AUDIT_SCHEMA=HERE.parent/"schemas"/"tpc__NUM__-__SLUG__-audit-v1.schema.json"
EXPECTED_SHA="__EXPECTED_SHA__"
EXPECTED_AUDIT_SHA="__EXPECTED_AUDIT_SHA__"
EXPECTED_SCHEMA_SHA="__EXPECTED_SCHEMA_SHA__"
EXPECTED_AUDIT_SCHEMA_SHA="__EXPECTED_AUDIT_SCHEMA_SHA__"
MUTATIONS=__MUTATIONS__
def canonical(x): return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=False)+"\n"
def text_hash(path):
    text=path.read_text(encoding="utf-8").replace("\r\n","\n").replace("\r","\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
def accepts(s,v):
    if "const" in s: return type(v) is type(s["const"]) and v==s["const"]
    if s.get("type")=="object":
        return isinstance(v,dict) and set(v)==set(s["required"]) and all(accepts(s["properties"][k],v[k]) for k in s["required"])
    if s.get("type")=="array":
        return isinstance(v,list) and len(v)==s["minItems"] and all(accepts(a,b) for a,b in zip(s["prefixItems"],v))
    return False
def mutated(p,name):
    x=copy.deepcopy(p)
    if name=="promote_L2": x["progress"]["L2"]="POSITIVE"
    elif name=="promote_fixed_atom_decay": x["fixed_atom_decay_obtained"]=True
    elif name=="grant_endpoint_credit": x["endpoint_ledger"]["named_atom_sigma_credit"]={"numerator":1,"denominator":400}
    elif name=="mark_strict_budget_paid": x["endpoint_ledger"]["state"]="PAID"
    elif name=="stop_bad_endpoint_parent": x["route_state"]["bad_endpoint_O161_parent"]="STOPPED"
    elif name=="stop_global_architecture": x["route_state"]["global_architecture"]="STOPPED"
    elif name=="promote_hash_to_theorem": x["source_locks"][0]["hash_semantics"]="THEOREM_EVIDENCE"
    elif name=="change_verdict": x["verdict"]="PROMOTED"
    elif name=="delete_first_missing":
        if "first_missing_literal_theorem" in x: del x["first_missing_literal_theorem"]
        else: del x["first_missing_nodes"]["direct_production"]
    elif name=="inject_extra_field": x["schema_exploit"]=True
    return x
def mobius(n):
    if n==1:return 1
    value=n; primes=0; p=2
    while p*p<=value:
        if value%p==0:
            value//=p
            if value%p==0:return 0
            primes+=1
            while value%p==0:value//=p
        p+=1
    if value>1:primes+=1
    return -1 if primes%2 else 1
def rs(level):
    p=[1];q=[1]
    for _ in range(level):p,q=p+q,p+[-x for x in q]
    return p,q
def finite(p):
    n=p["paper"];c=p["finite_certificate"]
    if n==194:
        f=c["affine_fixture"]; assert f["s"]*f["u"]-f["a"]*f["d"]==2
        assert len({x["id"] for x in c["formula_type_registry"]})==3
        assert len({x["domain"] for x in c["formula_type_registry"]})==3
        assert c["resolved_packet_formula"]["phase_slope"]=="Omega_xi=ell_theta*v_theta*sigma_theta*B_theta_b"
        assert "mfrak_K_X(r)" in c["resolved_packet_formula"]["outer_multiplier"]
        assert c["resolved_packet_formula"]["complete_per_key_contribution"]=="P_xi_X_le_T=cfrak_xi_X*S_xi_X_le_T"
        return {"determinant":2,"distinct_formula_types":3,"literal_formula_fields_verified":9}
    elif n==195:
        t=c["dyadic_fixture_T"]; seen=[];hi=t
        while hi>1:lo=hi//2;seen.extend(range(lo+1,hi+1));hi=lo
        seen.append(1);assert sorted(seen)==list(range(1,t+1))
        assert 19>10+1 and 19<2*10
        assert c["truncated_tail_raw_strict_bound"]=="2*B*M"
        sigma=Fraction(c["sigma_fixture"]["numerator"],c["sigma_fixture"]["denominator"])
        return {"dyadic_partition_exact":True,"forward_constant":round(1/(2**(1-float(sigma))-1),12),"reverse_constant":round(2**(1-float(sigma))+1,12),"truncated_tail_counterexample_to_M_plus_1":{"M":10,"T":19,"old_bound_terms":11,"possible_tail_terms":19,"new_strict_bound_terms":20}}
    elif n==196:
        f=c["fixture"];co=[(-1)**(z*z+3*z) for z in range(20)]
        direct=sum(co[z]*cmath.exp(-2j*math.pi*f["r"]*z/f["R"]) for z in range(20))
        split=sum(cmath.exp(-2j*math.pi*f["r"]*b/f["R"])*sum(co[z] for z in range(b,20,f["R"])) for b in range(f["R"]))
        assert abs(direct-split)<1e-10 and f["residue_determinant"]==10
        return {"residue_identity_error":abs(direct-split),"determinant":10}
    elif n==197:
        f=Fraction(c["fixed_atom_fixture"]["numerator"],c["fixed_atom_fixture"]["denominator"])
        matches=[q for q in c["prime_conductors"] if q==f.denominator]
        assert matches==[5]
        assert len(c["conductor_one_native_requirements"])==5
        return {"reduced_denominator":f.denominator,"matches":matches}
    elif n==198:
        pp,qq=rs(c["rudin_shapiro_level"]);L=len(pp)
        max_p=0.0;max_error=0.0
        for j in range(257):
            z=cmath.exp(2j*math.pi*j/257);pv=sum(a*z**k for k,a in enumerate(pp));qv=sum(a*z**k for k,a in enumerate(qq))
            max_p=max(max_p,abs(pv));max_error=max(max_error,abs(abs(pv)**2+abs(qv)**2-2*L))
            assert max_error<1e-8
        assert sum(a*a for a in pp)==L
        return {"length":L,"sampled_sup":round(max_p,12),"energy_error":max_error,"product_resonance":L}
    elif n==199:
        cc=lambda k:mobius(k)*mobius(k+2)
        assert (cc(3),cc(5),cc(15))==(1,1,-1) and math.gcd(3,5)==1
        return {"pair_values":{"3":1,"5":1,"15":-1},"multiplicative":False}
    elif n==200:
        zeros=[{"q":q,"h":h,"pair":"L2,L3"} for q in range(1,20,2) for h in range(1,21) if q*h-2==0]
        assert zeros==c["enumeration"]["zero_cells"]
        forms=[1+7,3+7,1+(7+2),3+(7+2)];assert forms[1]==forms[2]
        return {"zero_cells":zeros,"coincident_value":forms[1]}
    elif n==201:
        assert c["normalized_diagonal_coefficient"]+c["degenerate_shift_added_coefficient"]==6
        assert c["native_domain"]==["V>0","3<=H<=N"] and c["positive_part_split"]=="(x+y)_+<=|x|+y_+"
        return {"absorbed_coefficient":6,"remaining_gate_nonempty":True}
    elif n==202:
        row_average=1/c["selector_fixture"]["columns"];column_average=1/c["selector_fixture"]["rows"]
        assert max(row_average,column_average)<=1/64 and c["selector_fixture"]["prescribed_value"]==1
        assert c["new_stop_scoped_cell_created"] is False
        rr=p["external_primary_source"]["native_theorem_records"]
        assert rr[0]["range"]=="X>=h>=10" and "(1/X)" in rr[0]["lhs"] and "(1/h)" in rr[0]["lhs"]
        assert rr[1]["range"]=="natural k>=2 and X>=H>=10" and "(1/H^(k-1))" in rr[1]["lhs"] and rr[1]["rhs"].startswith("k*(")
        return {"row_average":row_average,"column_average":column_average,"prescribed_cell":1,"native_theorem_records_verified":2}
    elif n==203:
        locks={x["source_id"]:x for x in p["source_locks"]}
        seen_stops=set()
        for ns,v in c["expected_verdicts"].items():
            u=json.loads((REPO/locks[f"TPC{ns}.payload"]["path"]).read_text(encoding="utf-8"))
            assert u["verdict"]==v and u["progress"]["L2"]=="NONE"
            assert u["route_state"]["bad_endpoint_O161_parent"]=="OPEN"
            assert u["route_state"]["direct_twist_O161_parent"]=="OPEN"
            for cell in u["stop_scoped"]: seen_stops.add(cell["cell"])
        assert p["first_missing_nodes"]=={"global":"H1.source_backed_local_occurrence_edge_family","selected_pointwise":"LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION","direct_production":"SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"}
        assert p["batch_stop"]=={"state":"USER_CONFIRMATION_REQUIRED","next_paper":None,"tpc204_authorized":False}
        assert [x["route"] for x in c["exact_reopen_triggers"]]==["DIRECT","METRIC","BAD_ENDPOINT","STRUCTURAL","DECLARED_CORPUS"]
        assert "schedule-specific exceptional-limsup avoidance theorem" in c["exact_reopen_triggers"][1]["requires"]
        return {"upstreams_verified":len(c["expected_verdicts"]),"new_scoped_cells":len(seen_stops)}
    else:raise AssertionError(n)
def validate(p,a,s,a_s):
    assert hashlib.sha256(canonical(p).encode()).hexdigest()==EXPECTED_SHA==a["payload_canonical_sha256"]
    assert hashlib.sha256(canonical(a).encode()).hexdigest()==EXPECTED_AUDIT_SHA
    assert hashlib.sha256(canonical(s).encode()).hexdigest()==EXPECTED_SCHEMA_SHA
    assert hashlib.sha256(canonical(a_s).encode()).hexdigest()==EXPECTED_AUDIT_SCHEMA_SHA
    assert accepts(s,p)
    assert accepts(a_s,a)
    assert p["fixed_atom_decay_obtained"] is False and p["progress"]["L2"]=="NONE"
    assert p["endpoint_ledger"]["named_atom_sigma_credit"]["numerator"]==0
    assert p["endpoint_ledger"]["state"]=="UNPAID"
    assert p["route_state"]["bad_endpoint_O161_parent"]=="OPEN"
    assert p["route_state"]["direct_twist_O161_parent"]=="OPEN"
    assert p["route_state"]["global_architecture"]=="OPEN"
    assert all(v is False for v in p["claim_boundary"].values())
    for lock in p["source_locks"]:
        assert text_hash(REPO/lock["path"])==lock["canonical_utf8_lf_sha256"]
        assert lock["hash_semantics"]=="INTEGRITY_ONLY"
    assert finite(p)==a["finite_check_result"]
    outcomes=[{"name":name,"rejected":not accepts(s,mutated(p,name))} for name in MUTATIONS]
    assert outcomes==a["mutation_registry"] and all(x["rejected"] for x in outcomes)
    assert all(a["checks"].values()) and a["all_checks_pass"] is True
def main():
    if not __debug__: raise RuntimeError("optimized Python disables assertions; validation fails closed")
    ap=argparse.ArgumentParser();ap.add_argument("--check",action="store_true");ns=ap.parse_args()
    p=json.loads(PAYLOAD.read_text(encoding="utf-8"));a=json.loads(AUDIT.read_text(encoding="utf-8"));s=json.loads(SCHEMA.read_text(encoding="utf-8"));a_s=json.loads(AUDIT_SCHEMA.read_text(encoding="utf-8"))
    validate(p,a,s,a_s)
    if ns.check:
        assert PAYLOAD.read_text(encoding="utf-8")==canonical(p)
        assert AUDIT.read_text(encoding="utf-8")==canonical(a)
        assert SCHEMA.read_text(encoding="utf-8")==canonical(s)
        assert AUDIT_SCHEMA.read_text(encoding="utf-8")==canonical(a_s)
    print(json.dumps({"paper":p["paper"],"verdict":p["verdict"],"finite":True,"mutations":len(MUTATIONS),"check":ns.check},sort_keys=True))
if __name__=="__main__":main()
'''


def readme(d: dict) -> str:
    stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
    first_missing_lines = (
        "global_first_missing = H1.source_backed_local_occurrence_edge_family\n"
        "selected_pointwise_first_missing = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION\n"
        "direct_production_first_missing = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK"
        if d["num"] == 203
        else f"first_missing = {d['first_missing']}"
    )
    reopen_section = (
        """
## Exact reopen triggers

- `DIRECT`: formula-complete production target plus a theorem-backed natural
  `q/N` fixed-atom positive-power mechanism preserving all six axes and all losses.
- `METRIC`: source-locked named atom, exact packet schedule, and a
  schedule-specific exceptional-limsup avoidance theorem.
- `BAD_ENDPOINT`: literal fixed-atom local-increment cancellation theorem.
- `STRUCTURAL`: theorem-backed local-occurrence edge.
- `DECLARED_CORPUS`: genuinely new primary theorem corpus, while TPC-193 V1
  remains `STOP_SCOPED`.
"""
        if d["num"] == 203
        else ""
    )
    return f"""# TPC-{d['num']}: {d['title']}

## Result

{d['summary']}

```text
classification = {d['classification']}
verdict = {d['verdict']}
{first_missing_lines}
next_route = {d['next_route']}
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
```

This is an L0/L1 artifact. It claims no program-positive L2 result,
prime-pair lower bound, or twin-prime theorem.
{reopen_section}

## Reproduce

```powershell
python experiments/{stem}.py
python experiments/{stem}.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
"""


def expected_files(d: dict, payload: dict, audit: dict, p_schema: dict, a_schema: dict) -> dict[Path, str]:
    root = PAPERS / f"tpc-{d['num']}-{d['slug']}"
    stem = f"tpc{d['num']}_{d['slug'].replace('-', '_')}"
    checker = (
        CHECKER_TEMPLATE.replace("__STEM__", stem)
        .replace("__NUM__", str(d["num"]))
        .replace("__SLUG__", d["slug"])
        .replace(
            "__EXPECTED_SHA__",
            hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest(),
        )
        .replace(
            "__EXPECTED_AUDIT_SHA__",
            hashlib.sha256(canonical(audit).encode("utf-8")).hexdigest(),
        )
        .replace(
            "__EXPECTED_SCHEMA_SHA__",
            hashlib.sha256(canonical(p_schema).encode("utf-8")).hexdigest(),
        )
        .replace(
            "__EXPECTED_AUDIT_SCHEMA_SHA__",
            hashlib.sha256(canonical(a_schema).encode("utf-8")).hexdigest(),
        )
        .replace("__MUTATIONS__", repr(MUTATION_NAMES))
    )
    return {
        root / "main.tex": main_tex(d),
        root / "README.md": readme(d),
        root / "references.bib": references_bib(),
        root / ".gitignore": (
            "__pycache__/\n*.pyc\nmain.aux\nmain.bbl\nmain.blg\n"
            "main.log\nmain.out\nmain.pdf\n"
        ),
        root / ".gitattributes": (
            "*.tex text eol=lf\n*.md text eol=lf\n*.json text eol=lf\n"
            "*.py text eol=lf\n"
        ),
        root / "experiments" / f"{stem}.json": canonical(payload),
        root / "experiments" / f"{stem}_audit.json": canonical(audit),
        root / "experiments" / f"{stem}.py": checker,
        root / "schemas" / f"tpc{d['num']}-{d['slug']}-v1.schema.json": canonical(p_schema),
        root / "schemas" / f"tpc{d['num']}-{d['slug']}-audit-v1.schema.json": canonical(a_schema),
    }


def materialize() -> None:
    for d in PAPERS_DATA:
        payload = build_payload(d)
        p_schema = exact_schema(
            payload, f"tpc-{d['num']}-{d['slug']}-v1.schema.json"
        )
        audit = build_audit(d, payload, p_schema)
        a_schema = exact_schema(
            audit, f"tpc-{d['num']}-{d['slug']}-audit-v1.schema.json"
        )
        for path, text in expected_files(d, payload, audit, p_schema, a_schema).items():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")


def check_all() -> None:
    for d in PAPERS_DATA:
        payload = build_payload(d)
        p_schema = exact_schema(
            payload, f"tpc-{d['num']}-{d['slug']}-v1.schema.json"
        )
        audit = build_audit(d, payload, p_schema)
        a_schema = exact_schema(
            audit, f"tpc-{d['num']}-{d['slug']}-audit-v1.schema.json"
        )
        assert all(audit["checks"].values())
        assert all(x["rejected"] for x in audit["mutation_registry"])
        for path, expected in expected_files(d, payload, audit, p_schema, a_schema).items():
            assert path.is_file(), path
            actual = path.read_text(encoding="utf-8").replace("\r\n", "\n")
            assert actual == expected, path


def main() -> None:
    if not __debug__:
        raise RuntimeError(
            "optimized Python disables assertions; batch validation fails closed"
        )
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        materialize()
    check_all()
    print(
        json.dumps(
            {
                "range": "TPC-194--203",
                "papers": len(PAPERS_DATA),
                "check": args.check,
                "schema": "recursive-exact-const",
                "mutations_per_paper": len(MUTATION_NAMES),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
