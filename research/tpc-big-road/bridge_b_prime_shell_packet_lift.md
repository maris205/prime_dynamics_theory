# Bridge B TPC-218: prime-shell Hilbert lift and the collapse barrier

更新时间：2026-08-22

本文件是 TPC-218 的 source-locked proof record。它只处理 TPC-217 之后的
结构问题：把 prime-shell label q 和 four-packet label j 保留在同一个
Hilbert-valued finite-window object 中，并精确计算重新合并 q 时支付的代价。
它没有证明 prime cancellation、Möbius cancellation、arithmetic L2 或孪生素数。

## Registry and claim firewall

~~~
TPC218_MAXIMUM_CLAIM = PRIME_LABEL_AND_FOUR_PACKET_PRESERVING_HILBERT_LIFT_WITH_EXACT_P_FACTOR_COLLAPSE_BARRIER
TPC218_ROUTE_ADVANCE = YES
TPC218_STRUCTURAL_THRESHOLD_A = PASS
TPC218_HILBERT_VALUED_LARGE_SIEVE = PROVED_STANDARD_TENSOR_LIFT
TPC218_PRIME_LABEL_PRESERVATION = PROVED_EXACT
TPC218_PACKET_MATRIX_BOUND = PROVED_EXACT
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE
TPC218_SPLIT_UNNORMALIZED_EXPONENT = PROVED_97_OVER_96
TPC218_SCALAR_COLLAPSE_RECOVERY = PROVED_X_11_OVER_32_LOG_FIVE
TPC218_Q_COLLAPSE_COST = PROVED_P_FACTOR
TPC218_PACKET_PROJECTION_BOUND = PROVED_TRACE_DOMINATION
TPC218_Q_ORTHOGONALITY = REFUTED_SCOPED
TPC218_PACKET_ALIGNMENT = REFUTED_SCOPED
TPC218_ARITHMETIC_CANCELLATION = NONE
TPC218_ARITHMETIC_ADVANCE = NO
TPC218_FIXED_ATOM_CREDIT = 0
TPC218_L2 = NONE
TPC218_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC218_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC218_FULL_GATE_B = OPEN
TPC218_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC218_TPC_TRIGGER = true
TPC218_NUMBERED_RELEASE = YES
TPC218_STATUS = PROVED_STRUCTURAL_L1
TPC218_ROUND2_CLUE = PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE
~~~

The word PROVED above refers to the displayed structural theorem and its
declared hypotheses. The finite fixtures are NUMERICALLY_CERTIFIED or
ALGEBRAIC_FINITE_ALIGNMENT; they are not asymptotic evidence.

## 1. Frozen source object

Retain the V46/V70 scales

~~~
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q_x={q prime: Q<q<=2Q},
D_x={d: Y0<d<=U, mu(d)^2=1},
c_d=mu(d)log(d)/d.
~~~

Let J>=1 be fixed and let the packet profiles satisfy
M=max_j ||psi_j||_infty < infinity. For q in Q_x, h<=U, and a residue
a mod h, define

~~~
B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h).
~~~

The definition is made for every residue a mod h; later frequency sums retain
only primitive a. Put

~~~
C_h=sum_(d in D_x,h|d)c_d,
K_(j,q)(n)=sum_(h<=U)sum_(a mod h,(a,h)=1)
             C_h B_(h,q)^(j)(a)e(na/h),
K_j(n)=sum_(q in Q_x)K_(j,q)(n),
K_vec(n)=(K_(j,q)(n))_(j,q).
~~~

The intended physical object is still the literal common-source kernel. The
new notation only declines to collapse two outer labels before applying the
finite-window estimate.

The exponent identities used below are

~~~
Q^2/H = x^(1/96),
Q^3/H = x^(11/32),
U^2/x = x^(-67/200),
UQ/H = x^(23/2400).
~~~

## 2. Fixed-q row estimate

For sufficiently large x, 4Q<H. If two nonzero atoms in one fixed-q row
have the same residue modulo h, then h divides their difference while

~~~
|m_1-m_2| <= 2 floor(hq/H) < h
~~~

because q<=2Q. Hence the atoms are injective. Consequently

~~~
sum_(a mod h,(a,h)=1)|B_(h,q)^(j)(a)|^2
 <= sum_(a mod h)|B_(h,q)^(j)(a)|^2
 <= 2 M^2 hq/H.                                      (2.1)
~~~

This is an unsigned row estimate. It uses neither prime distribution nor the
sign of mu.

## 3. Coefficient harmonic bound

If an emitter row is nonzero for at least one q, then
floor(hq/H)>=1, so h>=H/(2Q). Write d=hk in C_h. For an active h,

~~~
k <= U/h <= 2UQ/H = O(x^(23/2400)).
~~~

Therefore, without using any cancellation,

~~~
|C_h|
 <= (log U)/h sum_(k<=U/h)1/k
 << (log x)^2/h.                                      (3.1)
~~~

Summing over active h gives

~~~
sum_h h|C_h|^2
 << (log x)^4 sum_(H/(2Q)<=h<=U)1/h
 << (log x)^5.                                        (3.2)
~~~

The same estimate remains valid for the literal squarefree band because
discarding terms can only reduce the absolute majorant.

## 4. Hilbert-valued finite-window theorem

Let I be any consecutive interval of N integers. The standard additive
large sieve says that for frequencies separated modulo one by at least
delta,

~~~
sum_(n in I)|sum_l z_l e(n alpha_l)|^2
 <= (N-1+delta^(-1)) sum_l |z_l|^2.                    (4.1)
~~~

Distinct reduced fractions a/h with h<=U have circular separation at least
U^(-2). Apply (4.1) to each coordinate of the Hilbert vector

~~~
v_(h,a)=(C_h B_(h,q)^(j)(a))_(j,q).
~~~

Summing the scalar inequalities over (j,q) is exactly the tensor lift

~~~
sum_(n in I)||K_vec(n)||_2^2
 <= (N+U^2) sum_(h,a,j,q)|C_h B_(h,q)^(j)(a)|^2.       (4.2)
~~~

This is a standard Hilbert-space lift, not a new arithmetic theorem.

Use (2.1), sum_(q in Q_x)q<=2PQ, (3.2), and P=#Q_x<=2Q:

~~~
sum_(h,a,j,q)|C_h B_(h,q)^(j)(a)|^2
 <= (4 J M^2 P Q/H) sum_h h|C_h|^2
 << J M^2 (Q^2/H)(log x)^5.                           (4.3)
~~~

Combining (4.2)--(4.3) proves

~~~
N^(-1) sum_(n in I)||K_vec(n)||_2^2
 << J M^2 x^(1/96)(log x)^5,                            (4.4)
~~~

since U^2/N=x^(-67/200+o(1)). The unnormalized exponent is 97/96+o(1).

This proves the new TPC-218 structural edge:

~~~
TPC218_SPLIT_NORMALIZED_EXPONENT = PROVED_1_OVER_96_LOG_FIVE.
~~~

The prime labels and packet labels remain available to any later signed
reassembly; no Cauchy step has yet mixed the q coordinates.

## 5. Packet matrix and scalar recovery

Form the packet shell vector K_pkt(n)=(K_j(n))_j and its interval Gram matrix

~~~
G_I[j,l]=sum_(n in I) K_j(n) overline(K_l(n)).
~~~

It is positive semidefinite. Pointwise Cauchy in the prime label gives

~~~
sum_j |K_j(n)|^2
 <= P sum_(j,q)|K_(j,q)(n)|^2.                         (5.1)
~~~

Thus

~~~
tr(G_I)
 <= P sum_(n in I)||K_vec(n)||_2^2
 << (N+U^2) J M^2 (P Q^2/H)(log x)^5
 << (N+U^2) J M^2 (Q^3/H)(log x)^5.                    (5.2)
~~~

After normalization this is exactly the TPC-217 power x^(11/32) up to the
fixed packet factor and logarithms. For every unit vector omega in packet
space,

~~~
sum_(n in I)|<omega,K_pkt(n)>|^2
 = omega^*G_I omega
 <= tr(G_I).                                           (5.3)
~~~

The complex four-packet interface remains exact because

~~~
x overline(y) = (1/4) sum_(j=0)^3 i^j |x+i^j y|^2.    (5.4)
~~~

Equations (5.1)--(5.4) identify the legal reassembly interface. They do not
give a signed saving: tr(G_I) is an unsigned envelope.

## 6. Sharp scoped obstructions

### 6.1 Prime-label alignment

Take the finite structural fixture

~~~
d=5, H=500, q in {101,131,151,181}, psi(t)=1.
~~~

Each q is 1 mod 5, each cutoff is one, and every fixed-q row is exactly

~~~
B_(5,q) = e_1+e_4.
~~~

Therefore

~~~
||sum_q B_(5,q)||_2^2 = 32,
sum_q ||B_(5,q)||_2^2 = 8,
ratio = 4 = P.                                       (6.1)
~~~

This is a NUMERICALLY_CERTIFIED_FINITE_STRUCTURAL_ADVERSARY (in fact an
exact rational calculation). It refutes, in this scope, any attempt to remove
the P collapse cost using only the fixed-q row geometry. It is not an
asymptotic lower bound for the literal prime shell.

### 6.2 Packet alignment

Let v be any nonzero vector and set Z^(j)=omega_j v for a unit four-vector
omega. Then

~~~
sum_j ||Z^(j)||^2 = ||v||^2,
||sum_j overline(omega_j) Z^(j)||^2 = ||v||^2.         (6.2)
~~~

For omega=(1,i,-1,-i)/2, the projection-to-total ratio is exactly one. This
is an ALGEBRAIC_FINITE_ALIGNMENT, not a claim that an arbitrary literal
TPC packet realizes independent parallel vectors. It proves that Hilbert
packet geometry alone cannot manufacture four-packet cancellation.

## 7. Route evaluation

~~~
strongest_positive_result = prime labels and four packet labels survive an exact Hilbert-valued finite-window lift with split exponent 1/96, and the scalar recovery exposes exactly one P factor
strongest_obstruction = a finite q-aligned shell realizes the full P collapse ratio, while a parallel four-packet family has projection ratio one
open_theorem = prove signed prime-shell reassembly for the literal coefficient family while beating the exact P collapse and retaining the four-packet/zero/nonunit interfaces
reusable_structure = Hilbert-valued additive large sieve plus PSD packet Gram and exact four-point polarization
ROUND2_CLUE = PROVE_A_SIGNED_PRIME_SHELL_REASSEMBLY_BEYOND_THE_EXACT_P_COLLAPSE
~~~

The maximum justified conclusion is PROVED_STRUCTURAL_L1. There is no
arithmetic L2, no fixed-atom credit, and no strict 1/400 payment.
