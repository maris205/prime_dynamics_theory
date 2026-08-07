# Bridge B V25: corrected Jutila Fourier emitter and the factorable auxiliary reserve

Date: 2026-08-08

Status:

~~~text
EXACT_L0_CORRECTION_AND_CONSTRUCTION
ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

This note continues the V24 literal determinant/Farey atomization at commit
511adfc2e5b6b271faa062faedb57bdd69b2a60b.  It makes two route-level
corrections.

First, the first line of Blomer--Li v1 equation (2.2) is not compatible with
Lemma 1, equation (2.1), or the second line of (2.2): its Fourier phase is
missing a divisor factor.  Second, after repairing that phase, the complete
signed Fourier/Farey emitter closes exactly at L0 and exposes the actual
analytic target.  A separate source-native factorable Jutila ensemble gives a
larger L2 margin, but it still does not transfer the published 41/42 theorem
to the literal TPC coefficients.

## 1. Frozen physical object and source boundary

Keep fixed

\[
h_0=2,\qquad x=2X,\qquad I_x=\{t\in\mathbb Z:x/2<t\le x\}.
\]

The literal V19/V24 atoms are

\[
G_x(\alpha)=\sum_\nu A_x(\nu)e(\alpha D_x(\nu)),
\qquad
S_x=\int_0^1G_x(\alpha)\,d\alpha.
\tag{1.1}
\]

For a prime-channel occurrence,

\[
A_x(\nu_p)=a_o\mu(d_{\rm phys})\log r_p,\qquad
D_x(\nu_p)=d_{\rm phys}r_p-T_o-2,
\tag{1.2}
\]

and for a hybrid-channel occurrence,

\[
A_x(\nu_h)
=-a_oC_zW_zg_z(d_{\rm rough})\mu(e_{\rm sieve}),\qquad
D_x(\nu_h)=e_{\rm sieve}r_h-T_o-2.
\tag{1.3}
\]

Here \(a_o\) retains the ordered V19 coefficients \(+2,-1\), every
occurrence multiplicity, and the physical \(1/\log T_o\) normalization.
The shell restrictions imply

\[
H_x:=\max_\nu |D_x(\nu)|<x/2.
\tag{1.4}
\]

The primary source locks are:

1. Ford--Maynard Lemma 5.2 for the literal ordered HB2 emitters;
2. Blomer--Li, arXiv:2511.03294v1, Lemma 1 and equations (2.1)--(2.2);
3. the source Farey partition and neighbor relations underlying Lemma 2,
   but not its false printed max/fixed-plus display;
4. Blomer--Pascadi arXiv:2607.24311v1, Theorems 1.1 and 5.5, only as
   post-transform fixed-modulus engines.

As of 2026-08-08 arXiv lists only v1 of the Blomer--Li paper.  The author
publication pages and the public Blomer corrections list contain no posted
repair of the defect below.  The correction in this note is therefore a
repository derivation, not an attributed source erratum.

## 2. The second printed source defect

Use the convention

\[
\widehat\psi_+(\xi)=\int_{\mathbb R}\psi(v)e(\xi v)\,dv,
\qquad
\chi(\alpha)=\sum_{n\in\mathbb Z}\kappa(n)e(-n\alpha).
\tag{2.1}
\]

Lemma 1 and equation (2.1) give

\[
\kappa(n)=\frac{\widehat\psi_+(\delta n)}{L}
\sum_q\omega(q)r_q(n),
\qquad
r_q(n)=\sum_{d\mid(q,n)}d\mu(q/d).
\tag{2.2}
\]

Writing \(n=dm\) forces the divisor-resolved identity

\[
\chi(\alpha)
=\frac1L\sum_q\omega(q)\sum_{d\mid q}d\mu(q/d)
\sum_{m\in\mathbb Z}
\widehat\psi_+(\delta dm)e(-\alpha dm).
\tag{2.3}
\]

Blomer--Li v1 (2.2), and consequently V24 (5.1), print
\(e(-\alpha m)\) instead of \(e(-\alpha dm)\).  The missing \(d\) is
substantive.  Only (2.3) Poisson-inverts to the printed second line

\[
\chi\!\left(\frac bc+z\right)
=\frac1{\delta L}\sum_q\omega(q)\sum_{d\mid q}\mu(q/d)
\sum_{\lambda\equiv bd\;({\rm mod}\ c)}
\psi\!\left(\delta^{-1}
\left(\frac{\lambda}{cd}+z\right)\right).
\tag{2.4}
\]

For \(q=2\), regard the values
\(\widehat\psi_+(\delta),\widehat\psi_+(2\delta)\) as independent formal
symbols.  At Fourier frequency one the printed first line gives

\[
-\widehat\psi_+(\delta)+2\widehat\psi_+(2\delta),
\tag{2.5}
\]

whereas the true coefficient is

\[
r_2(1)\widehat\psi_+(\delta)=-\widehat\psi_+(\delta).
\tag{2.6}
\]

For every sufficiently small legal \(\delta\),
\(\widehat\psi_+(2\delta)\ne0\), since \(\widehat\psi_+(0)=1\).
Thus this is a literal counterexample, not a harmless renaming.

The source-backed Lemma 1, its true coefficient formula (2.2), the rational
second line (2.4), and the V24 corrected Farey identity survive.  What stops
is only the first line as printed and any compiler that uses its wrong
frequency.

## 3. The two Poisson-dual indices are different types

The corrected Fourier and rational forms use distinct dummy variables:

~~~text
m_J                 divisor-resolved Fourier dummy,
n_J=d_J m_J         actual Fourier frequency,
lambda_J^rat        rational/spatial Poisson dummy,
lambda_J^rat = b_F d_J (mod c_F).
~~~

There is no termwise identification \(m_J=\lambda_J^{\rm rat}\).  In
particular:

- \(n_J=0\) is the global Fourier mean of \(\chi\);
- \(\lambda_J^{\rm rat}=0\) is a local rational cell and requires
  \(c_F\mid d_J\);
- the rational zero cell cannot be cancelled against the identity branch.

This repairs the overloaded V24 symbol \(\ell_J\).

## 4. Full-ensemble zero cancellation and the finite shift emitter

Let the corrected signed Farey functional be

\[
\begin{aligned}
\mathcal F_C(a):={}&
\sum_{c\le C}\int_{-1/(cC)}^{1/(cC)}\frac{e(za)}c
\sum_{u\bmod c}
\sum_{t\in I_C^{\rm corr}(c,z)}
\sum_{b\bmod c}^{*}\\
&e_c\!\left(ut+\sigma(z)u\overline b+ba\right)\,dz .
\end{aligned}
\tag{4.1}
\]

The repository-derived V24 Farey identity gives, monomial by monomial,

\[
\mathcal F_C(a)=\mathbf 1_{a=0}.
\tag{4.2}
\]

The zero Fourier coefficient satisfies

\[
\kappa(0)=
\frac1L\sum_q\omega(q)\sum_{d\mid q}d\mu(q/d)
=\frac1L\sum_q\omega(q)\phi(q)=1.
\tag{4.3}
\]

Therefore the identity branch and the negative-\(\chi\) zero mode cancel
only after the complete \(q,d\) ensemble is assembled.  They do not cancel
at fixed \(q\), fixed \(d\), a rational zero cell, or a Farey cell.

The exact finite normal form for the Jutila error is

\[
\boxed{
E_x=
-\frac1L\sum_\nu A_x(\nu)
\sum_q\omega(q)
\sum_{0<|n|\le H_x}\widehat\psi_+(\delta n)
\sum_{d\mid(q,n)}d\mu(q/d)\,
\mathcal F_C(D_x(\nu)-n).
}
\tag{4.4}
\]

Equivalently, with

\[
B_x(D)=\sum_{\nu:D_x(\nu)=D}A_x(\nu),
\tag{4.5}
\]

complete Farey reassembly gives the transparent multiplier identity

\[
\boxed{
E_x=-\sum_{D\ne0}B_x(D)\kappa(D).
}
\tag{4.6}
\]

Formula (4.4) is a genuine exact L0 emitter.  Formula (4.6) also shows its
limit: it is an exact rewrite of the Jutila error, not a cancellation
theorem.

## 5. Complete Kloosterman atoms and the axis firewall

Expanding \(\mathcal F_C\) in (4.4), the complete \(b\)-sum is

\[
\sum_{b\bmod c}^{*}
e_c\!\left(b(D-n)+\sigma(z)u\overline b\right)
=S(D-n,\sigma(z)u;c),
\tag{5.1}
\]

and the archimedean phase is exactly \(e(z(D-n))\).  In
divisor-resolved variables the same atom is

\[
S(D-dm,\sigma(z)u;c)e(z(D-dm)),
\tag{5.2}
\]

never \(S(D-m,\sigma u;c)\).

Although (4.4) is finite after complete reassembly, the Fourier series of
\(\chi\) is not compactly supported.  The terms \(|n|>H_x\) vanish only
after (4.2) is used.  A cellwise theorem cannot discard those terms without
a uniform Schwartz-tail ledger.

The registry must keep separate:

~~~text
FOURIER_ZERO: n=0, cancelled only in the full ensemble;
RATIONAL_ZERO: lambda_J^rat=0, a local nonempty cell;
PHYSICAL_ZERO: D=0, cancelled in the complete error but not cellwise;
LITERAL_SHIFT_AXIS: D-n=0, carrying S(0,sigma u;c);
MODULAR_AXIS: c divides D-n without D-n=0;
U_AXIS: u=0, carrying a Ramanujan sum;
DOUBLE_AXIS: u=0 and D-n=0, carrying phi(c);
NONUNIT_M: gcd(D-n,c)>1;
NONUNIT_U: gcd(u,c)>1;
q/c OVERLAP, hard-shell endpoints, prime powers, perfect powers,
rough tails, hybrid zero modes, and both z half-arcs.
~~~

After complete reassembly the literal-shift axis is exactly the weighted
nonzero-shift family in (4.6).  Bounds only for off-axis Kloosterman sums
cannot pay it.

## 6. Prime-shell kernel and the first unpaid norm

For the V23/V24 prime shell, let

\[
\mathcal Q_{\rm pr}=\{q\ {\rm prime}:Q_{\rm mes}<q\le2Q_{\rm mes}\},
\qquad
R_{\rm pr}=\#\mathcal Q_{\rm pr}.
\]

Then, for every integer \(n\),

\[
\kappa_{\rm pr}(n)
=\frac{\widehat\psi_+(\delta n)}{L_{\rm pr}}
\left(-R_{\rm pr}
+\sum_{\substack{q\in\mathcal Q_{\rm pr}\\q\mid n}}q\right).
\tag{6.1}
\]

The two divisor branches overlap deliberately:

~~~text
d=1:  negative full-frequency branch;
d=q:  positive q-divisible branch.
~~~

They must be recombined into the Ramanujan weight before any theorem credit.
Their effective lengths are

\[
|n|\lesssim\delta^{-1}=x^{21/32},\qquad
|m|\lesssim(\delta q)^{-1}=x^{31/96},
\tag{6.2}
\]

but these are Schwartz-effective, not hard supports.

For

\[
a_m(z)=-e(zm)\sum_{\substack{D-n=m\\n\ne0}}B_x(D)\kappa(n),
\qquad
\mathcal B_{c,z}(u)=\sum_{t\in I_C^{\rm corr}(c,z)}e_c(ut),
\tag{6.3}
\]

the exact Kloosterman normal form is

\[
E_x=\sum_{c\le C}\int\frac{dz}{c}
\sum_{u\bmod c}\mathcal B_{c,z}(u)
\sum_m a_m(z)S(m,\sigma(z)u;c).
\tag{6.4}
\]

The \(u\)-side has the exact finite Parseval identity

\[
\sum_{u\bmod c}|\mathcal B_{c,z}(u)|^2
=c\,|I_C^{\rm corr}(c,z)|\le c^2.
\tag{6.5}
\]

The first unpaid norm is the physical convolution:

\[
\sum_m|a_m(z)|^2
=\int_0^1|(1-\chi(\theta))G_x(\theta)|^2\,d\theta.
\tag{6.6}
\]

Jutila controls \(\|1-\chi\|_2\), not (6.6).  The committed bound
\(\|G_x\|_2\le x^{3/2+o(1)}\) remains insufficient.

## 7. What current Kloosterman theorems do and do not supply

No screened primary theorem accepts (6.4) directly.

- Blomer--Pascadi Theorems 1.1 and 5.5 accept already-emitted arrays in
  intervals of length at most the modulus, with a fixed unit and the stated
  coprimality conditions.  They are valid conditional engines for a fixed
  \(c,z\) coprime short cell.
- Pascadi arXiv:2404.04239v3 Proposition 10 permits a fixed-modulus
  nonunit cell only after a bounded-variation/Fourier-measure
  representation and its variation norm are paid.
- Kuznetsov/Deshouillers--Iwaniec requires a genuine smooth
  modulus/Bessel compiler and modulus-independent coefficient norms.
- Bettin--Chandee, Drappeau, FKMS, and Milićević--Qin--Wu have different
  reciprocal, trace, support, unit, or normalization inputs.

At the largest Farey block \(c\asymp C=x^{133/400+o(1)}\), the formal
fixed-cell Blomer--Pascadi saving

\[
C^{-1/32}=x^{-133/12800}
\tag{7.1}
\]

has gross margin

\[
\frac{133}{12800}-\frac1{400}
=\frac{101}{12800}.
\tag{7.2}
\]

This is not physical credit: smaller \(c\), the \(m\)-range \(x\gg c\),
long-range subdivision, nonunits, axes, (6.6), the \(c,z\)-dependent
\(\mathcal B\), and the unique outer reassembly remain unpaid.

## 8. A source-native factorable auxiliary ensemble

Define labels independent of the V23 prime shell:

\[
Q_1=x^{4/21},\quad Q_2=x^{8/21},\quad
Q_{\rm aux}=Q_1Q_2=x^{4/7}.
\tag{8.1}
\]

For a fixed smooth nonnegative nonzero
\(\rho\in C_c^\infty([1/2,1])\), set

\[
\omega_{\rm aux}(q)=
\sum_{\substack{Q_1/2\le p\le Q_1\\p\ {\rm prime},\,p\nmid2}}
\sum_{pt=q}\rho(t/Q_2).
\tag{8.2}
\]

The \(t\)-variable is unrestricted smooth.  It is not prime, squarefree, or
confined to an arithmetic progression.  Repeated \((p,t)\) representations
are deliberate multiplicities.  The exact normalizer is

\[
L_{\rm aux}=\sum_q\phi(q)\omega_{\rm aux}(q)
=x^{8/7+o(1)}.
\tag{8.3}
\]

The factorable representation count also gives the required source norm

\[
\|\omega_{\rm aux}\|_\infty
\le \|\rho\|_\infty\tau(q)=x^{o(1)}.
\tag{8.4}
\]

At the macro physical level,

\[
S_x=\sum_{m-n=2}\beta_x^{\rm raw}(n)\,
w_x^{(z)}(m-2),
\tag{8.5}
\]

so the common source parameters are
\((\lambda_1,\lambda_2,h)=(1,1,2)\).  A single common ensemble with
\(p\nmid2\) therefore gives the exact split

\[
S_x=M_{\rm aux}+E_{\rm aux}
\tag{8.6}
\]

and multiplier

\[
K_{\rm aux}(D)=
\frac{\widehat\psi_+(\delta D)}{L_{\rm aux}}
\sum_q\omega_{\rm aux}(q)c_q(D).
\tag{8.7}
\]

Because \(q\) is composite, its Ramanujan kernel cannot be replaced by the
prime two-value formula.

Blomer--Li Lemma 1 gives, with the literal exact-split choice
\(\delta=x^{-1}\),

\[
\|1-\chi_{\rm aux}\|_2^2\ll_{\psi,\rho} x^{-1/7+o(1)},\qquad
\boxed{\|1-\chi_{\rm aux}\|_2\ll_{\psi,\rho} x^{-1/14+o(1)}}.
\tag{8.8}
\]

The crude energy gives only

\[
|E_{\rm aux}|\ll_{\psi,\rho} x^{-1/14+o(1)}x^{3/2+o(1)}
=x^{10/7+o(1)}.
\tag{8.9}
\]

A pure-energy endpoint proof would require

\[
\|G_x\|_2\le x^{1+\theta+o(1)},\qquad
\theta<\frac1{14}-\frac1{400}
=\frac{193}{2800}.
\tag{8.10}
\]

This is a materially wider conditional window than the prime-shell energy
gate, but it is still an unproved physical norm theorem.

## 9. Why the published 41/42 theorem does not transfer

The Blomer--Li proof uses

~~~text
GL(3) Hecke coefficients A(n,1),
the divisor function or a smooth two-divisor convolution,
divisor Voronoi,
GL(3) Voronoi,
an unrestricted smooth t variable,
and an atom-dependent good-prime condition after dualization.
~~~

The literal V19 pair

\[
\beta_x^{\rm raw}(n),\qquad
\Lambda(m)-b_x^{(z)}(m-2)
\tag{9.1}
\]

has no source-backed transforms with the same dual supports, zero modes,
uniform constants, or tails.  Even the finite values
\(\tau(2)=\tau(3)=2\) and
\(\Lambda(2)=\log2,\Lambda(3)=\log3\) rule out a scalar coefficient
substitution.

The source proof also assumes

\[
\delta\gg x^{-1+\varepsilon}.
\tag{9.2}
\]

Thus \(\delta=x^{-1}\) is legal for Lemma 1 and the exact split, but it
cannot be inserted literally into the source estimates (3.25)/(3.41).
With a source-valid \(x^{-1+\varepsilon}\), those estimates still apply only
to the source coefficients.

At the macro level one common \(p\nmid2\) ensemble is exact.  If the
physical atoms are opened and treated one by one, their moving slopes make
the source good-prime condition atom-dependent.  For every auxiliary prime
in the shell there are active rows with \(d_{\rm phys}=p\).  Taking the
intersection of all atomwise good-prime sets can therefore empty the shell.
Changing \(\omega,L,\chi\) by atom destroys the common split; separating
good/bad rows requires a new collective gcd/nonunit theorem.

The source exponent ledger reaches \(41/42\) for its own object, but no part
of that saving is credited to (9.1).

## 10. Exact status atlas

~~~text
V25_BLOMER_LI_2_2_FIRST_LINE_AS_PRINTED_MISSING_d_PHASE
  = STOP_SCOPED_LITERAL_q2_FOURIER_COUNTEREXAMPLE

V25_CORRECTED_JUTILA_DIVISOR_FOURIER_EXPANSION
  = PROVED_EXACT_L0_REPOSITORY_DERIVATION

V25_FOURIER_RATIONAL_DUMMY_INDEX_IDENTIFICATION
  = STOP_SCOPED_POISSON_DUAL_TYPE_ERROR

V25_FULL_ENSEMBLE_ZERO_MODE_CANCELLATION
  = PROVED_EXACT_L0

V25_NONZERO_SHIFT_SIGNED_FAREY_KLOOSTERMAN_EMITTER
  = PROVED_EXACT_L0

V25_PRIME_SHELL_GROUPED_RAMANUJAN_KERNEL
  = PROVED_EXACT_L0

V25_DIRECT_CELLWISE_BP_FROM_EXACT_EMITTER
  = STOP_SCOPED_OUTER_NORM_LONG_RANGE_AND_REASSEMBLY_UNPAID

V25_FIXED_c_z_COPRIME_SHORT_BP_CELL
  = SOURCE_BACKED_CONDITIONAL_ENGINE

V25_FIXED_c_z_NONUNIT_PASCADI_CELL
  = CONDITIONAL_BV_FOURIER_MEASURE_NORM_UNPAID

V25_FACTORIZABLE_AUXILIARY_JUTILA_SPLIT
  = PROVED_EXACT_L0

V25_FACTORIZABLE_AUXILIARY_L2_GAIN
  = PROVED_SOURCE_BACKED_DERIVED_UPPER_BOUND_X_MINUS_1_OVER_14

V25_DIRECT_BLOMER_LI_41_OVER_42_TO_LITERAL_TPC_TRANSFER
  = STOP_SCOPED_COEFFICIENT_VORONOI_AND_REASSEMBLY_MISMATCH

V25_ATOMWISE_COMMON_GOOD_PRIME_ENSEMBLE
  = STOP_SCOPED_MOVING_SLOPE_GCD_AND_REASSEMBLY_MISMATCH

V25_RAMANUJAN_WEIGHTED_NONZERO_SHIFT_PHYSICAL_THEOREM
  = OPEN_NEW_THEOREM

V25_FACTORIZABLE_LITERAL_TRANSFORM_COMPILER
  = OPEN_NEW_CONSTRUCTION

ARITHMETIC_ADVANCE = NO
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID
L2 = NONE
TPC_207_TRIGGER = false
~~~

The maximum supported claim is

~~~text
EXACT_L0_CORRECTED_JUTILA_FOURIER_AND_FACTORIZABLE_AUXILIARY_EMITTER_WITH_SOURCE_TRANSFER_FIREWALLS
~~~

The next analytic gate is not another cellwise Kloosterman estimate.  It is
a theorem for the Ramanujan-weighted literal nonzero-shift family (4.6), or
an exact factorable transform compiler for (9.1) that keeps one common
ensemble, the good/bad prime rows, all axes, and the unique outer
reassembly.  Until one of those gates changes theorem state, the arithmetic
endpoint remains unpaid and TPC-207 remains false.
