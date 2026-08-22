# Bridge B TPC-221: collision-graph Schur envelope and literal saturation

更新时间：2026-08-22

TPC-221 takes the exact multiplicative collision Gram from TPC-220 and supplies the first
reusable quantitative envelope for it. The result is finite-dimensional linear algebra on
the literal rows; it does not estimate primes in progressions and does not claim arithmetic
`L2` cancellation.

## Registry and claim firewall

~~~text
TPC221_MAXIMUM_CLAIM = EXACT_PSD_WEIGHTED_SCHUR_COLLISION_ENVELOPE_WITH_LITERAL_SATURATION
TPC221_ROUTE_ADVANCE = YES
TPC221_STRUCTURAL_THRESHOLD_A = PASS
TPC221_COLLISION_GRAM_PSD = PROVED_EXACT
TPC221_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_WEIGHTED_SCHUR_ENVELOPE = PROVED_EXACT
TPC221_LITERAL_SATURATION = PROVED_EXACT_FINITE
TPC221_ABSOLUTE_SCHUR_SUBP_SAVING = REFUTED_SCOPED
TPC221_ARITHMETIC_CANCELLATION = NONE
TPC221_ARITHMETIC_ADVANCE = NO
TPC221_FIXED_ATOM_CREDIT = 0
TPC221_L2 = NONE
TPC221_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC221_FULL_GATE_B = OPEN
TPC221_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC221_TPC_TRIGGER = true
TPC221_NUMBERED_RELEASE = YES
TPC221_STATUS = PROVED_STRUCTURAL_L1
TPC221_ROUND2_CLUE = SEEK_SIGNED_PHASE_DISPERSION_BEYOND_ABSOLUTE_COLLISION_DEGREES
~~~

## 1. Gram energy and the Schur envelope

Fix a modulus `h`, a packet coordinate, and a finite active prime set. Write `B_q` for the
vector of literal row values on primitive residues and define

~~~text
Gamma(q,q') = <B_q,B_q'>,
E(lambda) = sum_a |sum_q lambda_q B_q(a)|^2.
~~~

The Gram matrix is `A A^*`, hence positive semidefinite, and direct expansion gives

~~~text
E(lambda) = lambda^* Gamma lambda.
~~~

For positive weights `p_q`, the inequality
`2|lambda_q lambda_q'| <= t|lambda_q|^2+t^(-1)|lambda_q'|^2` with
`t=p_q'/p_q` yields

~~~text
E(lambda) <= rho_p ||lambda||_2^2,
rho_p = max_q p_q^(-1) sum_q' |Gamma(q,q')| p_q'.
~~~

The unweighted choice `p_q=1` is the standard absolute Schur radius. TPC-220's literal
collision formula supplies each entry of `Gamma`; this theorem only packages those entries
into an operator envelope.

## 2. Exact finite saturation

Take `h=5`, `H=500`, constant profile, and
`Q={101,151,181,191}`. Every q is prime, `q=1 (mod 5)`, and
`floor(hq/H)=1`. Thus the only atoms are `m=+-1`, and every row is the same vector
`e_1+e_4`. Consequently

~~~text
Gamma = 2 J_4,
max row sum = 8,
lambda=(1,1,1,1): E(lambda)=32,
sum_q Gamma(q,q)=8,
E(lambda)/sum_q Gamma(q,q)=4=P.
~~~

The top Rayleigh quotient equals the Schur radius. This is a literal finite obstruction to
deriving a sub-`P` shell estimate from absolute collision degrees alone. It is scoped: the
fixture does not assert that this alignment persists for the growing prime window.

## 3. Route evaluation

~~~text
strongest_positive_result = exact PSD and weighted-Schur collision envelope
strongest_obstruction = literal aligned rows saturate the P factor and Schur radius
open_theorem = signed/phase-sensitive dispersion for the growing off-diagonal graph
reusable_structure = collision-degree operator interface with adjustable Schur weights
ROUND2_CLUE = SEEK_SIGNED_PHASE_DISPERSION_BEYOND_ABSOLUTE_COLLISION_DEGREES
~~~

The maximum justified status is `PROVED_STRUCTURAL_L1`; arithmetic `L2`, fixed-atom credit,
strict `1/400`, and the twin-prime endpoint remain open.
