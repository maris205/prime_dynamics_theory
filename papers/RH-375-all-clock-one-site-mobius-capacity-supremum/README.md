# RH-375: All-clock one-site Möbius capacity supremum

RH-375 exactly optimizes the finite-clock class left open by RH-374.  For a
fixed finite clock `q`, let `g_r:{-1,0,1}->{-1,+1}` be a phase/current-input
factor whose output obeys the RH-366 distance-two rule for every possible
ternary input word.  The factor is allowed to be `q`-periodic without having
minimal period `q`.  Its limiting Möbius correlation exists, and

```text
F(q) = max_{I intersect (I+2)=empty} sum_{r in I} delta_(q,r),
```

where `delta_(q,r)` is the squarefree density in the progression `r mod q`.
Thus `F(q)` is an exact weighted cycle-MWIS value, not a numerical fit.
The self-loop clocks `q=1,2` have `F(q)=0`.  Zero-density phases and the
value `g_r(0)` can only add safety constraints and are deletable at an
optimum; either global correlation orientation realizes the MWIS value.

If `q|Q`, lifting a `q`-periodic factor to clock `Q` preserves its output
word and gives `F(q)<=F(Q)`.  For the RH-374 square clocks

```text
q_y = 4 prod_(i<=y) p_i^2,
B_y = (4 + 2 O_y/A_y)/pi^2,
```

there is a stronger special statement.  Whenever `q_y|Q` and `Q` has the
same prime support as `q_y`, writing `Q=R q_y` gives

```text
F(Q) = F(q_y) = B_y.
```

The proof is not a general cyclic-cover MWIS law.  Every positive phase has
weight `1/R` times its square-clock weight; the `4`-divisible zero phases
split the even support, and the `9`-divisible zero phases split the odd runs,
so the support MWIS cardinality is exactly multiplied by `R`.

For an arbitrary finite `q`, choose `y` containing every odd prime divisor
of `q` and put `Q=lcm(q,q_y)`.  Then the preceding two facts and RH-374's
strictly increasing Euler-product family imply

```text
sup_{q finite} F(q) = B_infinity,
F(q) < B_infinity for every finite q.
```

The supremum is therefore not attained by any finite clock.  This theorem is
only about universally safe one-site factors.  It does not include
memory-dependent observables, growing clocks `q(N)`, an infinite selector,
uniform-in-clock Davenport estimates, or adaptive-capacity convergence.
It does not construct an operator, trace, zero model, Hilbert--Pólya
realization, or proof of RH.  Route A is `GO`; Route B is `STOP_SCOPED`;
Gates A--E remain false/open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

The bounded scan through `q=256` and all finite enumeration rows are labeled
reproduction only.  The all-clock theorem is the cofinal divisibility proof,
not an extrapolation from that scan.
