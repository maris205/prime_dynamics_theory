# TPC-352 derivation package

Let `D_I=A_I-T_I` be the literal mask defect.  For the ordered shell
`p_0<...<p_(r-1)` define

```text
gamma_j = 1/p_j - (1/r) sum_k 1/p_k,
c_I(t)  = sum_j gamma_j 1_(p_j|t).
```

The coefficient identity is exact:

```text
sum_j gamma_j = sum_j 1/p_j - r(1/r)sum_k 1/p_k = 0.
```

Writing `h_(p_j,I)(t)=1_(p_j|t)`, multiply-divisible positions are retained
and

```text
c_I = sum_j gamma_j h_(p_j,I),
||D_I c_I||_2^2
  = sum_(j,k) gamma_j gamma_k
      <D_I h_(p_j,I),D_I h_(p_k,I)>.
```

For `c_I != 0`, inserting `c_I/||c_I||_2` into the induced Euclidean norm
gives

```text
||D_I||_(2->2) >= ||D_I c_I||_2 / ||c_I||_2.
```

The balanced parent uses a different fixed coefficient vector only for the
paired finite comparison.  Both vectors are evaluated on the same literal
matrix.  All claims about transfer, floor, baseline, and length behavior are
finite numerical observations, not limits in `M`, `Q`, or the origin.
