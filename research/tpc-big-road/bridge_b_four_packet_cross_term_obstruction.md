# Bridge B TPC-222: four-packet polarization and the PSD cross-term obstruction

更新时间：2026-08-22

TPC-222 isolates the four-packet signed interface left open by TPC-218 and TPC-221. It is
an exact Hilbert-space paper: it proves the polarization identity and the trace envelope,
then demonstrates that diagonal/trace information cannot identify a signed reassembly.
No prime-distribution estimate is claimed.

## Registry and claim firewall

~~~text
TPC222_MAXIMUM_CLAIM = EXACT_FOUR_POINT_POLARIZATION_AND_TRACE_OBSTRUCTION
TPC222_ROUTE_ADVANCE = YES
TPC222_STRUCTURAL_THRESHOLD_A = PASS
TPC222_PSD_PACKET_GRAM = PROVED_EXACT
TPC222_FOUR_POINT_POLARIZATION = PROVED_EXACT
TPC222_TRACE_RAYLEIGH_ENVELOPE = PROVED_EXACT
TPC222_SIGNED_CROSS_TERM_IDENTIFIABILITY = REFUTED_SCOPED
TPC222_FOUR_PACKET_SIGNED_REASSEMBLY = OPEN
TPC222_ARITHMETIC_CANCELLATION = NONE
TPC222_ARITHMETIC_ADVANCE = NO
TPC222_FIXED_ATOM_CREDIT = 0
TPC222_L2 = NONE
TPC222_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC222_FULL_GATE_B = OPEN
TPC222_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC222_TPC_TRIGGER = true
TPC222_NUMBERED_RELEASE = YES
TPC222_STATUS = PROVED_STRUCTURAL_L1
TPC222_ROUND2_CLUE = CONTROL_POLARIZED_LITERAL_PACKET_ENERGIES_WITH_SIGNED_CROSS_CORRELATION
~~~

## 1. Exact packet identities

Use the convention `inner(x,y)=sum_i conjugate(x_i)y_i`. For four packet vectors `V_j`,
define `G_(j,l)=inner(V_j,V_l)`. Then `G` is PSD and

~~~text
||sum_j c_j V_j||^2 = c^* G c.
~~~

For every pair `x,y`, expansion at the four fourth roots of unity gives

~~~text
inner(x,y) = 1/4 sum_(r=0)^3 i^(-r) ||x+i^r y||^2.       (2.1)
~~~

This is the exact four-point polarization compiler. It recovers a cross-term only if the
four phase-labelled energies are retained with their complex coefficients.

Since `G` is PSD, `lambda_max(G)<=tr(G)`, and therefore

~~~text
0 <= c^*G c <= tr(G)||c||_2^2.                            (2.2)
~~~

## 2. Exact signed non-identifiability fixture

Let `u=(1,0)`, and set
`V_j^+=u` while `V_j^-=(-1)^j u`. Both Gram matrices have diagonal `(1,1,1,1)` and
trace `4`. For `c=(1,1,1,1)`, however,

~~~text
||sum_j c_j V_j^+||^2 = 16,
||sum_j c_j V_j^-||^2 = 0.
~~~

Both matrices are rank-one PSD; the plus fixture saturates (2.2), while the minus fixture
has complete signed cancellation. Thus packet norms and trace alone cannot certify the
signed reassembly. The polarization residuals for both fixtures are exactly zero, so the
obstruction is not a failure of the identity; it is the absence of a theorem controlling the
phase-labelled inputs to that identity.

## 3. Route evaluation

~~~text
strongest_positive_result = exact four-point polarization and PSD trace envelope
strongest_obstruction = same diagonal/trace with signed energies 16 and 0
open_theorem = literal growing-scale polarized cross-correlation estimate
reusable_structure = phase-labelled four-energy compiler and PSD firewall
ROUND2_CLUE = CONTROL_POLARIZED_LITERAL_PACKET_ENERGIES_WITH_SIGNED_CROSS_CORRELATION
~~~

The maximum justified status is `PROVED_STRUCTURAL_L1`; arithmetic `L2`, fixed-atom credit,
strict `1/400`, and the twin-prime endpoint remain open.
