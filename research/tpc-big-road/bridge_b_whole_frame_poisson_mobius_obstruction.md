# Bridge A / Gate B TPC-209: whole-frame Poisson reindexing and the Möbius-dilation obstruction

Date: 2026-08-18

Status: \`PROVED_STRUCTURAL_L1 / STOP_SCOPED_FRAME_ONLY_SAVING\`.

This note tests the TPC-208 \`ROUND2_CLUE\`: apply Poisson to a complete
oriented additive edge frame before taking an edge or fiber triangle, and ask
whether one dual variable is shared across the whole frame. The answer has
two parts.

1. For each fixed Möbius dilation \(D\), Poisson gives an exact shared dual
   integer \(n=qr+kD\) for all edge vertices \(k\). The transformed edge
   frame is therefore a genuine vector-valued dual packet.
2. Summing over \(D\) leaves a \(D\)-dependent multiplicative permutation of
   the dual nonzero residue coordinates. Multiplicative Fourier analysis
   diagonalizes these permutations, but returns exactly to the nonprincipal
   Dirichlet-character interface already present in V59. Arbitrary dual
   profiles can align after the permutations, so frame geometry alone cannot
   collapse them to one scalar packet or create a power saving.

The result is a precise obstruction to the proposed *frame-only* compiler. It
does not rule out a new profile-aware arithmetic theorem for the actual
Möbius packets.

## 0. Claim firewall

```
TPC209_MAXIMUM_CLAIM = EXACT_FIXED_DIVISOR_WHOLE_FRAME_POISSON_REINDEXING_PLUS_MULTIPLICATIVE_SPECTRAL_NORMAL_FORM_AND_SHARP_VECTOR_ALIGNMENT_OBSTRUCTION
TPC209_ROUTE_ADVANCE = YES
TPC209_STRUCTURAL_THRESHOLD_A = PASS
TPC209_SHARED_DUAL_PER_FIXED_DIVISOR = PROVED_EXACT
TPC209_WHOLE_FRAME_VECTOR_COVARIANCE = PROVED_EXACT
TPC209_MULTIPLICATIVE_CHARACTER_DIAGONALIZATION = PROVED_EXACT
TPC209_RETURN_TO_V59_CHARACTER_INTERFACE = PROVED_EXACT
TPC209_SCALAR_COMMON_DUAL_COLLAPSE = REFUTED_SCOPED
TPC209_FRAME_ONLY_POWER_SAVING = STOP_SCOPED
TPC209_SOURCE_VALID_KLOOSTERMAN_ATTACHMENT = OPEN
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_TPC_TRIGGER = true
```
\`TPC209_TPC_TRIGGER=true\` means that a real theorem package and a precise
bounded obstruction were obtained, so the numbered structural paper is
legitimate. It does **not** mean that Gate B or the twin-prime endpoint has
advanced arithmetically.

## 1. Frozen input and the exact question

TPC-208 writes the standard-zero-hole additive row, for a prime \(q\), as a
complete-graph frame on

\[
 G_q=\mathbb F_q^\times,
 \qquad N_q=q-1,
 \qquad P_q=I_{N_q}-N_q^{-1}{\bf1}{\bf1}^*.
\tag{1.1}
\]

For a sequence \(a\), its nonzero additive-frequency vector is

\[
 Y_q[a](k;v)=\sum_n a_n e(vn/H)e_q(-kn),
 \qquad k\in G_q.
\tag{1.2}
\]

Writing \(g_{k,l}=e_k-e_l\), the edge analysis form is

\[
 \mathcal E_q(Y,Z)
 :=\frac1{N_q}\sum_{\{k,l\}\subset G_q}
 (Y(k)-Y(l))\overline{(Z(k)-Z(l))}
 =\langle P_qY,P_qZ\rangle .
\tag{1.3}
\]

The equality follows from the complete-graph identity

\[
 \sum_{\{k,l\}}g_{k,l}g_{k,l}^*=N_qP_q.
\tag{1.4}
\]

The actual TPC scalar also contains the exact coefficient diagonal
subtraction, the outer \(q\), the prime shell, the kernel \(K_H\), four packet
signs, and physical block reassembly. They remain frozen. The present note
isolates only the proposed first transform of the additive frame; it never
silently replaces the physical remainder by a positive full-lattice energy.

The question is whether the factorization

\[
 t=Dm,
 \qquad \beta(t)=\sum_D c_D F_D(m)
\tag{1.5}
\]

can be Poisson-transformed in a way that leaves one common dual variable for
all \(D,k,l\), and then feeds a source-valid Kloosterman theorem without an
unpaid multiplicity.

## 2. One-component Poisson theorem

Let \(q>2\) be prime, let \(D\) be an integer with \((D,q)=1\), and let
\(F_D\) be a Schwartz function. Use

\[
 \widehat F_D(\xi)=\int_{\mathbb R}F_D(x)e(-x\xi)\,dx,
 \qquad e_q(x)=e(x/q).
\tag{2.1}
\]

Define the Poisson-ready additive component

\[
 Y_{q,D}(k)=\sum_{m\in\mathbb Z}F_D(m)e_q(-kDm),
 \qquad k\in G_q.
\tag{2.2}
\]

### Theorem 2.1 (shared dual integer at fixed dilation)

For every \(k\in G_q\),

\[
 \boxed{
 Y_{q,D}(k)
 =\sum_{r\in\mathbb Z}\widehat F_D\!\left(r+\frac{kD}{q}\right)
 =\sum_{\substack{n\in\mathbb Z\\n\equiv kD\;(q)}}
   \widehat F_D(n/q).}
\tag{2.3}
\]

For fixed \(D\), the map

\[
 (k,r)\longmapsto n=qr+kD
\tag{2.4}
\]

is a bijection from \(G_q\times\mathbb Z\) to
\(\{n\in\mathbb Z:q\nmid n\}\), with inverse

\[
 k\equiv nD^{-1}\pmod q,
 \qquad r=\frac{n-kD}{q}.
\tag{2.5}
\]

Define the dual residue packet

\[
 B_{q,D}(s)=
 \sum_{\substack{n\in\mathbb Z\\n\equiv s\;(q)}}
 \widehat F_D(n/q),
 \qquad s\in G_q,
\tag{2.6}
\]

and the multiplicative permutation

\[
 (U_D b)(k)=b(kD).
\tag{2.7}
\]

Then

\[
 \boxed{Y_{q,D}=U_DB_{q,D}.}
\tag{2.8}
\]

#### Proof

Poisson summation applied to \(x\mapsto F_D(x)e(-kDx/q)\) gives the first
equality in (2.3). Since \(D\) is invertible modulo \(q\), every integer
\(n\not\equiv0\pmod q\) has the unique residue representation
\(n=qr+kD\) with \(k\in G_q\). Reindexing gives the second equality and
(2.5)--(2.8). No edge, modulus, or absolute-value estimate is used.
\(\square\)

The theorem confirms a limited positive hypothesis: all edge vertices for a
fixed \(D\) use one dual integer lattice. It also identifies the first
failure mode: the dual packet is indexed by \(kD\), not by \(k\) itself.

## 3. Whole-frame covariance before any edge triangle

Let \(\mathcal D\) be a finite set of unit dilations and let
\(c_D,d_E\in\mathbb C\). Put

\[
 Y=\sum_{D\in\mathcal D}c_DU_DB_D,
 \qquad
 Z=\sum_{E\in\mathcal D}d_EU_EC_E.
\tag{3.1}
\]

### Proposition 3.1 (exact vector-valued whole-frame compiler)

The complete edge frame satisfies

\[
 \boxed{
 \mathcal E_q(Y,Z)
 =\sum_{D,E\in\mathcal D}c_D\overline{d_E}
 \langle P_qU_DB_D,P_qU_EC_E\rangle.}
\tag{3.2}
\]

Moreover \(U_DP_q=P_qU_D\), and therefore the cross term depends on the
relative multiplicative dilation \(D^{-1}E\):

\[
 \langle P_qU_DB_D,P_qU_EC_E\rangle
 =\langle P_qB_D,U_{D^{-1}E}P_qC_E\rangle,
\tag{3.3}
\]

up to the harmless choice of whether the inner product is linear in its first
or second argument.

#### Proof

Insert (3.1) into (1.3) and expand the finite sums. A multiplicative
permutation preserves \({\bf1}\), hence commutes with \(P_q\). The identity
\(U_D^*U_E=U_{D^{-1}E}\) gives (3.3). \(\square\)

Equation (3.2) is the exact whole-frame transform requested by TPC-208. It
does preserve the frame cancellation, but it is a vector-valued divisor
compiler. Removing \(D\ne E\) terms or taking an absolute value over \(D\)
would be an additional theorem, not a consequence of the transform.

## 4. Multiplicative spectral normal form

Let \(\widehat G_q\) be the multiplicative character group of \(G_q\), and
define the unitary multiplicative Fourier transform

\[
 (\mathcal M b)(\chi)=N_q^{-1/2}
 \sum_{s\in G_q}b(s)\overline{\chi(s)}.
\tag{4.1}
\]

For every \(D\in G_q\),

\[
 \mathcal M(U_Db)(\chi)=\chi(D)\mathcal M b(\chi).
\tag{4.2}
\]

The principal character coordinate is the constant vector, so \(P_q\) deletes
exactly \(\chi_0\).

### Theorem 4.1 (shared-character profile normal form)

For \(Y,Z\) in (3.1),

\[
 \boxed{
 \mathcal E_q(Y,Z)=
 \sum_{\chi\ne\chi_0}
 \left(\sum_Dc_D\chi(D)(\mathcal MB_D)(\chi)\right)
 \overline{\left(\sum_Ed_E\chi(E)(\mathcal MC_E)(\chi)\right)}.}
\tag{4.3}
\]

#### Proof

Apply the unitary transform \(\mathcal M\) to (3.2), use (4.2), and omit the
principal coordinate because \(P_q\) is the orthogonal projection onto the
nonprincipal character coordinates. Parseval gives (4.3). \(\square\)

This is the repaired shared-coordinate statement. One common character
\(\chi\) survives across the complete frame, but every divisor carries its own
profile \((\mathcal MB_{q,D})(\chi)\). Unless those profiles satisfy an
additional arithmetic relation, (4.3) is not a scalar multiplier
\(\sum_Dc_D\chi(D)\) times one common dual array.

## 5. Exact closure back to the V59 interface

For the physical additive vector (1.2), let \(\chi\ne\chi_0\) be a
nonprincipal character and define

\[
 \tau_q(\overline\chi)=
 \sum_{x\in G_q}\overline\chi(x)e_q(x).
\tag{5.1}
\]

### Proposition 5.1 (Gauss crosswalk)

\[
 \boxed{
 (\mathcal MY_q[a])(\chi)=
 \frac{\overline{\chi(-1)}\tau_q(\overline\chi)}{\sqrt{q-1}}
 \sum_{q\nmid n}a_ne(vn/H)\chi(n).}
\tag{5.2}
\]

#### Proof

Exchange the finite character sum and the sum over \(n\). For \(q\nmid n\),
the substitution \(x=-kn\) gives

\[
 \sum_{k\in G_q}\overline\chi(k)e_q(-kn)
 =\overline{\chi(-1)}\chi(n)\tau_q(\overline\chi).
\]

For \(q\mid n\), the inner sum is zero because \(\chi\) is nonprincipal.
Divide by \(\sqrt{q-1}\). \(\square\)

The right side of (5.2) is precisely a nonprincipal Dirichlet-character
transform of the original packet, up to the explicit Gauss factor and the
convention \(\chi\leftrightarrow\overline\chi\). Thus multiplicative
diagonalization of the additive edge frame is exactly a Gauss-factor
re-expression of the nonprincipal Dirichlet-character packets. It closes the
attempted route back to V59; it does not emit the fixed-modulus Kloosterman
arrays accepted by the later Blomer--Pascadi engine. This is an exact route
closure, not a claim that no other second transform could ever work.

## 6. Sharp obstruction to scalar common-packet collapse

The vector profile dependence in (4.3) cannot be removed by graph geometry.

### Theorem 6.1 (sharp alignment bound)

For weights \(c=(c_D)_{D\in\mathcal D}\), define

\[
 L_c:\bigoplus_{D\in\mathcal D}\mathbb C^{G_q}
 \longrightarrow\mathbb C^{G_q},
 \qquad
 L_c((B_D)_D)=P_q\sum_Dc_DU_DB_D.
\tag{6.1}
\]

Then

\[
 \boxed{\|L_c\|=\left(\sum_D|c_D|^2\right)^{1/2}.}
\tag{6.2}
\]

The bound is attained on the centered subspace. In particular, if all
profiles have comparable size, the complete frame supplies no additional
orthogonality between divisor components.

#### Proof

The adjoint is

\[
 L_c^*z=(\overline{c_D}U_D^*P_qz)_D.
\]

Consequently

\[
 L_cL_c^*z
 =\sum_D|c_D|^2U_DP_qU_D^*P_qz
 =\left(\sum_D|c_D|^2\right)P_qz.
\]

Hence (6.2). If \(z\in{\bf1}^\perp\) has unit norm, take

\[
 B_D=\overline{c_D}U_D^*z/\|c\|_2.
\]

The direct-sum input has unit norm and \(L_c(B)=\|c\|_2z\), proving
sharpness. \(\square\)

There is also a direct coherent fixture. Take
\(B_D=\operatorname{sgn}(c_D)U_D^*z\) for a fixed nonzero centered \(z\).
Then all output vectors align. For unit weights, the sum of individual frame
energies is \(|\mathcal D|\|z\|^2\), whereas the whole-frame energy is
\(|\mathcal D|^2\|z\|^2\). Thus the ratio is exactly \(|\mathcal D|\).

The fixture is an interface obstruction, not an asymptotic claim about the
actual \(\beta\). It proves that a frame-only argument cannot discard the
divisor cross terms or infer a power saving from the complete graph.


## 7. Common-profile resonance

If one *adds* the strong assumption \(B_D=B\) for every \(D\), then the
divisor sum is the convolution operator

\[
 M_c=\sum_Dc_DU_D.
\tag{7.1}
\]

The multiplicative characters diagonalize it:

\[
 M_c\chi=\left(\sum_Dc_D\chi(D)\right)\chi,
 \qquad
 \|P_qM_cP_q\|=\max_{\chi\ne\chi_0}
 \left|\sum_Dc_D\chi(D)\right|.
\tag{7.2}
\]

Even this repaired common-profile model has no automatic cancellation. For
\(q=5\), \(D=2,3\), and \(c_2=c_3=-1\), the quadratic character has
\(\chi(2)=\chi(3)=-1\), so its nonprincipal multiplier is \(2\), equal to the
\(\ell^1\) coefficient mass. This is an exact finite resonance, not an
asymptotic claim about the physical \(\beta\).

## 8. Finite certificate and numerical sanity check

The project certificate independently checks the exact matrix, permutation,
and dual-index identities for \(q=3,5,7,11,13\). It checks 1500 dual
reindex rows and 3016 permutation-matrix rows. The \(q=5\) alignment fixture
has energy ratio \(2\), and its quadratic multiplier equals its coefficient
\(\ell^1\) mass.

The separate Gaussian test in the project experiments applies the continuous
Poisson identity to three Schwartz functions and records errors below
\(10^{-12}\). It is a numerical sanity check only; the theorem is the exact
Schwartz Poisson identity in Section 2.

```
PYTHONDONTWRITEBYTECODE=1 python -B \
  papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/run_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B \
  papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B \
  papers/tpc-209-whole-frame-poisson-mobius-obstruction/experiments/independent_checker.py --check
```

The finite certificate is a QA artifact, not evidence for an asymptotic
power saving.

## 9. Source boundary and route decision

TPC-208 supplied the complete-graph frame but explicitly left the whole-frame
Poisson/Kloosterman compiler open. V59 already supplies the nonprincipal
character packet and exact \(q-2\) diagonal subtraction. Proposition 5.1
shows that multiplicative diagonalization of the new frame route is an exact
return to that interface.

The later Blomer--Pascadi theorem accepts an already-emitted fixed-modulus
bilinear Kloosterman cell. Equations (4.3) and (5.2) are upstream of that
input: they contain divisor-dependent dual profiles and no source theorem in
the current lock converts them, with the prime shell and signed diagonal
reassembly intact, into the accepted cell family.

Therefore the first fatal for this route is now precise:

```
NO_FRAME_ONLY_SCALAR_EMITTER:
POISSON_CREATES_ONE_SHARED_DUAL_LATTICE_PER_DILATION,
BUT_THE_COMPLETE_FRAME_RETAINS_DILATION_PERMUTATIONS;
CHARACTER_DIAGONALIZATION_RETURNS_TO_V59,
AND_ARBITRARY_PROFILES_HAVE_SHARP_COHERENT_ALIGNMENT.
```

The route is not globally closed. The smallest legitimate replacement is a
profile-aware theorem for the character expression (4.3), uniform in the
actual Möbius/hybrid packets, with the exact \(q-2\) subtraction, prime-only
shell, block kernel, packet signs, and physical normalization. That is the
TPC-210 candidate, not a free consequence of TPC-209.

## 10. Canonical registry

```
TPC209_MAXIMUM_CLAIM = EXACT_FIXED_DIVISOR_WHOLE_FRAME_POISSON_REINDEXING_PLUS_MULTIPLICATIVE_SPECTRAL_NORMAL_FORM_AND_SHARP_VECTOR_ALIGNMENT_OBSTRUCTION
TPC209_ROUTE_ADVANCE = YES
TPC209_STRUCTURAL_THRESHOLD_A = PASS
TPC209_SHARED_DUAL_PER_FIXED_DIVISOR = PROVED_EXACT
TPC209_WHOLE_FRAME_VECTOR_COVARIANCE = PROVED_EXACT
TPC209_MULTIPLICATIVE_CHARACTER_DIAGONALIZATION = PROVED_EXACT
TPC209_RETURN_TO_V59_CHARACTER_INTERFACE = PROVED_EXACT
TPC209_SCALAR_COMMON_DUAL_COLLAPSE = REFUTED_SCOPED
TPC209_FRAME_ONLY_POWER_SAVING = STOP_SCOPED
TPC209_SOURCE_VALID_KLOOSTERMAN_ATTACHMENT = OPEN
TPC209_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC209_ARITHMETIC_ADVANCE = NO
TPC209_GLOBAL_GATE_B_ADVANCE = NO
TPC209_FIXED_ATOM_CREDIT = 0
TPC209_L2 = NONE
TPC209_FIRST_FATAL = NO_FRAME_ONLY_SCALAR_EMITTER_DILATION_PERMUTATIONS_SURVIVE_AND_CHARACTER_DIAGONALIZATION_RETURNS_TO_V59
TPC209_ROUND2_CLUE = PROVE_OR_REFUTE_A_PROFILE_AWARE_NONPRINCIPAL_CHARACTER_BOUND_FOR_THE_ACTUAL_MOBIUS_POISSON_DUAL_PACKETS_BEFORE_ANY_PRIME_OR_BLOCK_TRIANGLE
TPC209_REUSABLE_STRUCTURE = WHOLE_FRAME_POISSON_VECTOR_COMPILER_PLUS_MULTIPLICATIVE_CHARACTER_PROFILE_NORMAL_FORM
TPC209_TPC_TRIGGER = true
```
