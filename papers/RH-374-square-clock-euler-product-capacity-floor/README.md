# RH-374: Square-clock Euler-product capacity floor

RH-374 turns the single composite clock of RH-373 into a strictly increasing
family of fixed-clock certificates.  Let `p_1=3<p_2<...` be the odd primes,
`P_y=prod_{i<=y} p_i^2`, `q_y=4P_y`, and
`A_y=prod_{i<=y}(p_i^2-1)`.  For the universally safe one-site
phase/current-input selector class at the fixed clock `q_y`, the exact optimum
is

```text
B_y = (4 + 2 O_y/A_y)/pi^2,
```

where `O_y` is the number of odd-length positive runs in one period of the
odd-phase squarefree word.  With

```text
E_m^(y) = prod_{i<=y}(1-m/p_i^2),
```

the run identity is

```text
O_y = P_y * sum_{j in {1,3,5,7}}
      (E_j^(y) - 2E_(j+1)^(y) + E_(j+2)^(y)).
```

Adjoining an odd prime `p>=5` gives

```text
A' = (p^2-1)A,
O' = (p^2-1)O + L_even,
```

where `L_even` counts the one-sites lying in even-length old runs.  An exact
length-eight run persists by CRT, so `L_even>0` and `B_y` is strictly
increasing.  Consequently the Euler-product limit

```text
B_infinity = (4 + 2C)/pi^2,
C = sum_{j odd<=7}(e_j-2e_(j+1)+e_(j+2))/e_1,
e_m = prod_{p odd}(1-m/p^2),  e_9=0,
```

is another unconditional lower floor for the RH-366 capacity.  The quantifier
is fixed `y` before `N -> infinity`: one scalar `liminf K_N/N` dominates every
`B_y`, hence their supremum.  No growing clock, uniform-in-clock Davenport
estimate, or infinite selector is used.

Exact rows begin

| `y` | `q_y` | `A_y` | `O_y` | selected phases | `pi^2 B_y` |
|---:|---:|---:|---:|---:|---:|
| 1 | 36 | 8 | 0 | 16 | 4 |
| 2 | 900 | 192 | 8 | 392 | 49/12 |
| 3 | 44100 | 9216 | 544 | 18976 | 593/144 |

The `q=900` coefficient exceeds RH-373's `97/24` by exactly `1/24`.
The optimum claim is confined to fixed-`q_y` universally safe one-site
phase/current-input factors, equivalently the weighted phase MWIS.  It is not
an optimum over arbitrary memory transducers or all clocks, and it does not
prove convergence of the adaptive capacity.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```
