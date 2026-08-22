# Bridge B TPC-219: prime-shell longitudinal/transverse ledger

更新时间：2026-08-22

TPC-219 starts from the exact q-labelled packet object of TPC-218. It does not alter the
V46/V70 source coefficient, fixed `h0`, interval, packet profiles, or normalization. The
new theorem is an exact decomposition of the scalar q collapse.

## Registry and claim firewall

~~~text
TPC219_MAXIMUM_CLAIM = EXACT_LONGITUDINAL_TRANSVERSE_PRIME_SHELL_LEDGER
TPC219_ROUTE_ADVANCE = YES
TPC219_STRUCTURAL_THRESHOLD_A = PASS
TPC219_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC219_P_COLLAPSE_EQUIVALENCE = PROVED_EXACT
TPC219_ALIGNED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_BALANCED_ENDPOINT = PROVED_EXACT_FINITE
TPC219_ARITHMETIC_CANCELLATION = NONE
TPC219_ARITHMETIC_ADVANCE = NO
TPC219_FIXED_ATOM_CREDIT = 0
TPC219_L2 = NONE
TPC219_PRIME_SHELL_SIGNED_REASSEMBLY = OPEN
TPC219_FULL_GATE_B = OPEN
TPC219_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC219_TPC_TRIGGER = true
TPC219_NUMBERED_RELEASE = YES
TPC219_STATUS = PROVED_STRUCTURAL_L1
TPC219_ROUND2_CLUE = REEXPRESS_TRANSVERSE_ENERGY_AS_LITERAL_PRIME_AP_COLLISION_DATA
~~~

`PROVED` means exact finite Hilbert algebra under the displayed definitions. No finite
fixture is asymptotic arithmetic evidence.

## 1. Application object

Let `Q_x` be the prime shell from TPC-218, `P=#Q_x`, and let

~~~text
Z_q(n) = (K_(j,q)(n))_(0<=j<J) in C^J.
~~~

For an interval `I`, define

~~~text
Zbar(n) = P^(-1) sum_q Z_q(n),
R_q(n) = Z_q(n)-Zbar(n),
E_shell = sum_(n in I)||sum_q Z_q(n)||_2^2,
E_diag  = sum_(n in I)sum_q||Z_q(n)||_2^2,
E_perp  = sum_(n in I)sum_q||R_q(n)||_2^2.
~~~

The construction is exactly the packet-valued scalar recovery interface already present
in TPC-218.

## 2. Exact theorem

For each `n`, `sum_q R_q(n)=0`. Expanding `Z_q=Zbar+R_q` gives

~~~text
sum_q||Z_q||_2^2 = P||Zbar||_2^2 + sum_q||R_q||_2^2.       (2.1)
~~~

Since `sum_q Z_q=P Zbar`,

~~~text
||sum_q Z_q||_2^2
 = P^2||Zbar||_2^2
 = P sum_q||Z_q||_2^2 - P sum_q||R_q||_2^2.              (2.2)
~~~

Summing (2.2) over `I` proves

~~~text
E_shell = P(E_diag-E_perp).                              (2.3)
~~~

Equation (2.1) also gives `0<=E_perp<=E_diag`, hence

~~~text
0 <= E_shell <= P E_diag.                                (2.4)
~~~

For `0<=eta<=1`, rearranging (2.3) proves the exact equivalence

~~~text
E_shell <= eta P E_diag
    <=> E_perp >= (1-eta)E_diag.                          (2.5)
~~~

Thus a sub-`P` scalar recovery is precisely a lower bound on literal q-transverse energy.
No upper bound, Cauchy estimate, or unsigned trace estimate can supply (2.5) by itself.

## 3. Sharp finite endpoints

If every `Z_q=v`, then `R_q=0`, so `E_shell=P E_diag`. This saturates (2.4). If the
q-vectors sum to zero, then `Zbar=0`, `E_perp=E_diag`, and `E_shell=0`. The exact
rational certificate realizes both endpoints and checks (2.3) for a mixed family.

## 4. Route evaluation

~~~text
strongest_positive_result = exact P-collapse iff criterion via E_perp
strongest_obstruction = aligned q labels have zero transverse energy
open_theorem = prove a transverse lower bound for the literal prime shell
reusable_structure = constant-mode orthogonal projection and integrated Pythagorean ledger
ROUND2_CLUE = REEXPRESS_TRANSVERSE_ENERGY_AS_LITERAL_PRIME_AP_COLLISION_DATA
~~~

The maximum justified status is `PROVED_STRUCTURAL_L1`. There is no arithmetic `L2`,
fixed-atom credit, strict `1/400` payment, or twin-prime conclusion.
