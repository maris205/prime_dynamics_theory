# Bridge B TPC-220: prime-AP collision crosswalk

更新时间：2026-08-22

TPC-220 takes the exact q-transverse target from TPC-219 and rewrites the literal
TPC-218 rows without changing their cutoff, profile, primitive support, or coefficient
source. It is an identity paper; no prime-distribution estimate is claimed.

## Registry and claim firewall

~~~text
TPC220_MAXIMUM_CLAIM = EXACT_PRIME_AP_AND_MULTIPLICATIVE_COLLISION_CROSSWALK
TPC220_ROUTE_ADVANCE = YES
TPC220_STRUCTURAL_THRESHOLD_A = PASS
TPC220_PRIME_AP_CROSSWALK = PROVED_EXACT
TPC220_MULTIPLICATIVE_COLLISION_GRAM = PROVED_EXACT
TPC220_DIAGONAL_REDUCTION = PROVED_EXACT
TPC220_ARITHMETIC_CANCELLATION = NONE
TPC220_ARITHMETIC_ADVANCE = NO
TPC220_FIXED_ATOM_CREDIT = 0
TPC220_L2 = NONE
TPC220_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC220_FULL_GATE_B = OPEN
TPC220_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC220_TPC_TRIGGER = true
TPC220_NUMBERED_RELEASE = YES
TPC220_STATUS = PROVED_STRUCTURAL_L1
TPC220_ROUND2_CLUE = QUANTIFY_THE_OFF_DIAGONAL_COLLISION_GRAPH_BEYOND_SCHUR
~~~

## 1. Literal rows and AP notation

Fix an active denominator `h`, a prime `q` with `(q,h)=1`, and write

~~~text
L_(h,q)=floor(hq/H),
w_(h,m,q)^j=psi_j(Hm/(hq)),
M_(h,q)^*= {m:0<|m|<=L_(h,q), (m,h)=1}.
~~~

For a primitive residue `a mod h`, the TPC row is

~~~text
B_(h,q)^j(a)=sum_(m in M_(h,q)^*) w_(h,m,q)^j
                  1_(m q^(-1)=a mod h).
~~~

For q weights `lambda_q`, define the exact weighted prime-AP packet

~~~text
Pi_(h,m)^j(r;lambda)
 = sum_(q in Q_x, q=r mod h, |m|<=L_(h,q))
       lambda_q w_(h,m,q)^j.
~~~

The range of `m` is finite and can be taken as `0<|m|<=floor(2hQ/H)`.

## 2. Exact prime-AP crosswalk

Since `a` and `q` are units modulo `h`,

~~~text
m q^(-1)=a (mod h)
  <=> m=a q (mod h)
  <=> q=a^(-1)m (mod h).
~~~

Thus, after swapping the finite `q,m` sums,

~~~text
sum_q lambda_q B_(h,q)^j(a)
 = sum_(m != 0) Pi_(h,m)^j(a^(-1)m;lambda).       (2.1)
~~~

Equation (2.1) is an exact weighted prime-AP representation of the literal shell row.
The profile weight and q-dependent cutoff remain inside `Pi`; no separability assumption
has been introduced.

## 3. Exact multiplicative collision Gram

Define the primitive row Gram

~~~text
Gamma_h^(j,l)(q,q')
 = sum_(a mod h, (a,h)=1)
      B_(h,q)^j(a) conjugate(B_(h,q')^l(a)).
~~~

Expanding both rows, a common primitive residue exists exactly when `m,m'` are units and

~~~text
m q^(-1)=m' (q')^(-1) (mod h)
  <=> m q'=m' q (mod h).
~~~

Consequently

~~~text
Gamma_h^(j,l)(q,q')
 = sum_(m in M_(h,q)^*) sum_(m' in M_(h,q')^*)
     w_(h,m,q)^j conjugate(w_(h,m',q')^l)
     1_(m q'=m' q mod h).                         (3.1)
~~~

For `q=q'`, if `2L_(h,q)<h`, the congruence forces `m=m'` because
`|m-m'|<=2L_(h,q)<h`. Hence

~~~text
Gamma_h^(j,j)(q,q)=sum_(m in M_(h,q)^*)|w_(h,m,q)^j|^2.  (3.2)
~~~

The off-diagonal entries in (3.1) are the exact collision graph left by TPC-219.

## 4. Certificate and route evaluation

The project certificate checks (2.1), (3.1), and (3.2) exactly for three denominators,
four primes, and constant and affine rational profiles. It also records nonzero
off-diagonal collisions. The finite computation is a consistency check only.

~~~text
strongest_positive_result = literal q reassembly is a weighted prime-AP operator
strongest_obstruction = off-diagonal Gram entries are multiplicative collisions
open_theorem = quantify the collision graph beyond Schur/absolute control
reusable_structure = primitive AP crosswalk plus diagonal/off-diagonal Gram split
ROUND2_CLUE = QUANTIFY_THE_OFF_DIAGONAL_COLLISION_GRAPH_BEYOND_SCHUR
~~~

The maximum justified status is `PROVED_STRUCTURAL_L1`; arithmetic `L2`, fixed-atom
credit, strict `1/400`, and the twin-prime endpoint remain open.
