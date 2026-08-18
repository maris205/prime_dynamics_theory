# Derivation Package

## Target

Determine what the complete nonzero-additive-frequency edge frame from
TPC-208 becomes when a Möbius-factor component is transformed by Poisson
summation before any edge, fiber, block, or prime-modulus triangle inequality.
The immediate question is whether all divisor components share one legitimate
dual variable and whether that identity itself creates a source-valid
Kloosterman emitter.

## Status

COHERENT AFTER REFRAMING

The exact result is a frame-level Poisson reindexing theorem plus a sharp
vector-valued obstruction.  A shared dual integer exists for each fixed
divisor component, but the divisor survives as a permutation of the dual
nonzero residue coordinates.  Diagonalizing those permutations returns the
nonprincipal multiplicative-character representation already present in V59.
No arithmetic saving follows from the frame identity alone.

## Invariant Object

The invariant is the TPC-208 edge bilinear form

\[
 \mathcal E_q(Y,Z)=\frac1{q-1}\sum_{\{k,l\}\subset\mathbb F_q^\times}
 (Y(k)-Y(l))\overline{(Z(k)-Z(l))}
 =\langle P_qY,P_qZ\rangle,
\]

where \(P_q=I-(q-1)^{-1}{\bf1}{\bf1}^*\).  This is the object retained
through every transformation; a one-dimensional scalar dual sum is only a
possible representation and is not assumed to exist.

## Assumptions

- \(q\) is prime and \(q>2\); the \(q=2\) frame is zero and is checked
  separately.
- \(D\) ranges over a finite set of integers with \((D,q)=1\).
- The Poisson-ready component \(F_D\) is Schwartz on \(\mathbb R\), with
  \(\widehat F_D(\xi)=\int F_D(x)e(-x\xi)\,dx\).
- Coefficients \(c_D,d_E\) are arbitrary complex scalars.  The actual V59
  packet corresponds to Möbius-weighted components, but no cancellation of
  those weights is assumed.
- Nonunit rows, the exact \(q-2\) diagonal subtraction, the prime shell,
  and physical block reassembly remain external bookkeeping layers.  This
  package does not silently replace them by a full-lattice model.

## Notation

- \(G=\mathbb F_q^\times\), \(N=q-1\), and \(P=I-N^{-1}{\bf1}{\bf1}^*\).
- \(U_D\) is the multiplicative permutation
  \((U_D b)(k)=b(kD)\) on vectors indexed by \(G\).
- \(Y_D(k)=\sum_{m\in\mathbb Z}F_D(m)e_q(-kDm)\).
- \(B_D(s)=\sum_{n\equiv s\pmod q}\widehat F_D(n/q)\) for \(s\in G\).
- \(\mathcal M\) is the unitary multiplicative Fourier transform on \(G\),
  indexed by multiplicative characters \(\chi\).

## Derivation Strategy

1. Apply Poisson to one factorized component while retaining the complete
   additive vertex set.
2. Reindex \((k,r)\) by the single integer \(n=qr+kD\); this tests the
   shared-dual-variable hypothesis without taking an edge absolute value.
3. Insert the resulting vectors into the graph-Laplacian identity.
4. Diagonalize the remaining divisor permutations by multiplicative Fourier
   analysis.
5. Test whether the resulting expression is a scalar common-packet emitter
   or a genuinely vector-valued profile problem.
6. Use an exact alignment construction to determine the strongest obstruction
   available from frame geometry alone.

## Derivation Map

1. Poisson gives
   \(Y_D(k)=\sum_r\widehat F_D(r+kD/q)\) (identity).
2. The bijection \(n=qr+kD\) gives
   \(Y_D(k)=B_D(kD)=(U_DB_D)(k)\) (identity).
3. Summing the complete edge frame gives
   \(\mathcal E_q(Y,Z)=\langle PY,PZ\rangle\) (identity).
4. A divisor sum therefore has the exact form
   \(Y=\sum_Dc_DU_DB_D\) (identity).
5. Multiplicative Fourier turns \(U_D\) into the scalar \(\chi(D)\),
   producing one shared character coordinate but divisor-dependent profiles
   \(\mathcal MB_D(\chi)\) (identity).
6. For a physical additive Fourier vector, a Gauss-sum calculation identifies
   those character coordinates with the V59 nonprincipal character packets
   (identity / exact crosswalk).
7. Independent profiles can align after the permutations, so a scalar common
   packet is not implied and frame geometry supplies no further cancellation
   (proposition / obstruction).

## Main Derivation

### Step 1. One-component Poisson reindexing

For \(k\in G\), Poisson summation gives

\[
 Y_D(k)=\sum_{r\in\mathbb Z}\widehat F_D\!\left(r+\frac{kD}{q}\right).
\]

For fixed \(D\), the map

\[
 (k,r)\longmapsto n=qr+kD
\]

is a bijection from \(G\times\mathbb Z\) to the integers not divisible by
\(q\), with inverse \(k\equiv nD^{-1}\pmod q\).  Hence

\[
 Y_D(k)=\sum_{n\equiv kD\;(q)}\widehat F_D(n/q)=B_D(kD).
\]

This is the exact shared-dual statement.  It is shared across all edges for
one fixed \(D\), not across all divisors.

### Step 2. Whole-frame covariance

Let \(Y=\sum_Dc_DU_DB_D\) and \(Z=\sum_Ed_EU_EC_E\).  Since the complete
graph incidence matrix has Gram matrix \(NP\),

\[
 \mathcal E_q(Y,Z)
 =\langle PY,PZ\rangle
 =\sum_{D,E}c_D\overline{d_E}
   \langle PU_DB_D,PU_EC_E\rangle.
\]

The cross terms are part of the invariant object.  Dropping them is a new
triangle inequality, not a consequence of Poisson summation.

### Step 3. Multiplicative spectral form

For \(\chi\) a multiplicative character, \(\mathcal M(U_Db)(\chi)=
\chi(D)\mathcal M b(\chi)\).  The principal character is exactly the
constant direction removed by \(P\).  Therefore

\[
 \mathcal E_q(Y,Z)=
 \sum_{\chi\ne\chi_0}
 \left(\sum_Dc_D\chi(D)\mathcal MB_D(\chi)\right)
 \overline{\left(\sum_Ed_E\chi(E)\mathcal MC_E(\chi)\right)}.
\]

The repaired whole-frame object is thus a shared multiplicative-character
coordinate with divisor-dependent dual profiles.  It is not a single
scalar Kloosterman array.

### Step 4. Exact return to the V59 character interface

For a physical additive vector
\(Y_a(k)=\sum_na_ne(vn/H)e_q(-kn)\), the nonprincipal coordinate is

\[
 \mathcal MY_a(\chi)=
 \frac{\overline{\chi(-1)}\tau_q(\overline\chi)}{\sqrt{q-1}}
 \sum_{q\nmid n}a_ne(vn/H)\chi(n),
\]

where \(\tau_q(\overline\chi)=\sum_{x\ne0}\overline\chi(x)e_q(x)\).
Thus multiplicative diagonalization of the additive edge frame is exactly a
Gauss-factor re-expression of the nonprincipal Dirichlet-character packets.
It closes the attempted route back to V59; it does not emit the
fixed-modulus Kloosterman arrays accepted by the later Blomer--Pascadi engine.

### Step 5. Sharp vector-valued obstruction

Define

\[
 L_c((B_D)_D)=P\sum_Dc_DU_DB_D.
\]

On \({\bf1}^\perp\), \(L_cL_c^*=\sum_D|c_D|^2I\), so

\[
 \|L_c\|_{\ell^2(G)^{\oplus\mathcal D}\to\ell^2(G)}
 =\left(\sum_D|c_D|^2\right)^{1/2}.
\]

Equality is attained by taking one nonzero \(z\in{\bf1}^\perp\) and
\(B_D=\overline{c_D}U_D^{-1}z/\|c\|_2\).  Consequently the complete frame
does not force divisor cancellation.  In the common-profile special case
\(B_D=B\), the multiplier is
\(\sum_Dc_D\chi(D)\); this can also resonate.  For example, modulo five,
\(c_2=c_3=-1\) and the quadratic character has multiplier \(2\), equal to
the coefficient \(\ell^1\) mass.

## Remarks and Interpretation

- The positive result is a legitimate whole-frame transform: all edge terms
  share the same dual integer within each divisor component.
- The obstruction is not a claim about the actual Möbius sequence at
  asymptotic scale.  It says that Poisson plus frame algebra alone cannot
  collapse divisor-dependent profiles or manufacture a power saving.
- The correct next theorem is profile-aware: it must bound the shared-
  character expression while preserving the exact diagonal, prime shell,
  packet signs, and physical reassembly.

## Boundaries and Non-Claims

- No prime-only BDH estimate, Kloosterman attachment, `1/400` payment, `L2`
  advance, fixed-atom credit, or twin-prime theorem is proved.
- The finite certificate checks exact linear algebra and finite reindexing;
  it is not asymptotic evidence.
- The Gaussian Poisson checks in the experiment are numerical sanity checks,
  not replacements for the Schwartz Poisson theorem.

## Open Risks

- A profile-aware theorem could still exploit arithmetic structure not visible
  in the arbitrary-component alignment obstruction.
- The smooth extension used for a source packet must be chosen canonically in a
  future full compiler; this package does not select that extension.
- Nonunit rows and the exact V59 diagonal must be carried through any future
  source attachment.
