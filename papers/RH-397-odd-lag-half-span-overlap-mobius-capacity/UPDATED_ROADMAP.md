# RH-397 updated roadmap

## Closed route

RH-397 closes a new overlap geometry for every fixed lag and phase clock:

1. RH-394 supplies the complete fixed three-shift terminal law at
   `(+h,0,-h)`; the fourth safety symbol is not analytic.
2. Positive projection reduces the table to a ternary relation at center
   value `+1`.
3. Two shared symbols make universal separation-`h` safety exactly the scalar
   flag constraint `t_r s_(r+h)=0`.
4. Every flag class saturates to one of four rectangles, and the
   collision-aware `M,U,V,W` formula gives its exact value.
5. Translation `V_r=U_(r+h)` and nonnegative edge filling telescope the
   objective to a weighted rising-set problem.
6. Every step-`h` independent set is realized, including empty/self-loop
   cases, giving the exact capacity at every fixed `h,q`.
7. For odd `h`, clock two captures all three-shift weight; literal repetition
   makes every declared even clock attain.
8. A local CRT construction produces adjacent positive weights at every odd
   clock, proving strictness and the exact iff-even attainment classification.

## New theorem edge

```text
fixed three-shift terminal law
          |
          v
two-symbol overlap flag collapse
          |
          v
four exact rectangles + MUVW translation
          |
          v
weighted step-h rising-set optimizer
          |
          v
odd-lag finite-clock maximum attained iff declared q is even.
```

The key qualitative change from RH-396 is finite-clock attainment: RH-396's
distance-`2h` safe class has a strict nonattained clock supremum, while the
new separation-`h` class attains its odd-lag maximum at every declared even
clock.  The classes are different and neither capacity is presented as a
strengthening of the other.

## Admissible next work

These are questions, not RH-397 conclusions:

- classify the maximum and exact maximizers of RH-396's fixed-lag Euler-run
  endpoint across all fixed lags;
- seek other fixed overlap relations whose flag geometry collapses to an
  exact weighted graph problem;
- investigate even-lag clock landscapes without extrapolating the odd-lag
  parity theorem;
- study causal rules under their own information constraint;
- revisit larger windows only when an analytic source pays every required
  correlation channel.

No next paper number follows merely from this list.  A successor requires a
fresh source lock, exact theorem contract, and independent proof audit.

## Permanent stops

Do not infer growing `h`, growing `q`, growing tables, a uniform rate,
ordinary Cesaro convergence, a prelimit maximum, causality, even-lag all-clock
classification, a four-shift or even-four law, generic graph capacity,
operator or trace identities, zeta-zero identification, RH, or any upgrade of
Gates A--E.
