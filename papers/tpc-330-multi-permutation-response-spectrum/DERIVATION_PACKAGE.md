# TPC-330 derivation package

## 1. Target and status

The target is a finite multi-permutation response spectrum for the literal
source-native signed-Gram diagnostic.  The matrix identities and bijection
claims are `PROVED_EXACT_FINITE`.  The source formula is
`PROVED_EXACT_FINITE_DECLARED_MODEL`.  The five-control spectrum is
`NUMERICALLY_CERTIFIED_FINITE`.  No growing arithmetic theorem is inferred.

## 2. Literal finite object

For the finite source interval
`I_(o,N)={o,...,o+N/2-1}`, define

```text
B_p(u,t) = 1_(u!=t) 1_(p does not divide u) 1_(p does not divide t)
            p H^(2s)/(H^2+(u-t)^2)^s
            (1_(p divides u-t)-1/(p-1)).
```

For one fixed shell-sign law `e`, put `C_e=sum_p e_p B_p`.  For a finite
source vector `v`,

```text
E_e(v)=||C_e v||_2^2,
D_e(v)=sum_t v_t^2 ||C_e e_t||_2^2,
O_e(v)=E_e(v)-D_e(v),
R_e(v)=E_e(v)/D_e(v).
```

The arithmetic vector is the finite V59 model

```text
beta_o^(2)(t)=Lambda(t+2)-b^(2)(t),
b^(2)(t)=2 C_2 1_(2 does not divide t)
          product_(p|t,p>2)(p-1)/(p-2).
```

## 3. Five-control orbit

Let `M=N/2` and define

```text
pi_0(i)=i,
pi_3,11(i)=(3i+11) mod M,
pi_5,17(i)=(5i+17) mod M,
pi_7,29(i)=(7i+29) mod M,
pi_rev(i)=M-1-i.
```

For `M=2048` or `4096`, each odd multiplier is coprime to `M`; reversal
is self-evidently bijective.  If `P_j` denotes the corresponding permutation
matrix, then

```text
P_j^T P_j=I,
||P_j v||_2=||v||_2,
multiset(P_j v)=multiset(v).
```

The response coordinate is

```text
R_(e,j)(v)=E_e(P_j v)/D_e(P_j v).
```

This five-coordinate vector is the finite placement-response spectrum.  It is
not a probability distribution over permutations.

## 4. Exact Gram derivation

Since `C_e v=sum_t v_t C_e e_t`, bilinearity gives

```text
E_e(v)=sum_(t,t') v_t v_t' <C_e e_t,C_e e_t'>.
```

The `t=t'` terms form `D_e(v)`; the remaining terms form `O_e(v)).
Therefore `E_e(v)=D_e(v)+O_e(v)` exactly.  If `D_e(v)>0`, the sign of
`O_e(v)` is the sign of `R_e(v)-1`.

For a placement control,

```text
E_e(P_j v)=v^T P_j^T C_e^T C_e P_j v.
```

Norm preservation alone does not force this quadratic form to be independent
of `j`.  Such independence would require a commutation or isotropy property
that is neither assumed nor observed.

## 5. Frozen finite spectrum

There are `32*5*4=640` response observations.  In negative/positive notation:

```text
identity      all 31/1   alt 25/7   mod4 32/0   half 32/0
affine 3,11   all  0/32  alt 20/12  mod4 27/5   half 31/1
affine 5,17   all  0/32  alt 30/2   mod4 32/0   half 28/4
affine 7,29   all  0/32  alt 21/11  mod4 32/0   half 29/3
reversal      all 31/1   alt 25/7   mod4 32/0   half 32/0.
```

For all-plus, the three affine controls are positive on all 32 rows.  Identity
and reversal have equal classifications on all 32 rows.  The five-control
signature is negative/positive/positive/positive/negative on 31 rows and
unanimously positive on one row.

Across all laws, identity and reversal have zero classification changes in
128 pairwise observations, although their ratios differ by as much as
`0.022723042898999735`.  Thus classification agreement is numerical and
finite, not an exact symmetry theorem.

## 6. Exact local anchor

On `[36001,36016]`, `Q=4`, `s=1`, with
`v_t=1_(t+2 prime)-1_(t odd)`, exact rational arithmetic gives

```text
E=306.7544239093389,
D=332.4445614235858,
O=-25.69013751424689,
E=D+O.
```

Reduced-fraction SHA-256 digests bind all three values.

## 7. Boundaries and next structure

The control menu is deterministic and finite.  It does not sample the
symmetric group, identify a limiting distribution, or prove a uniform source
estimate.  The result supports a position-sensitive obstruction and suggests
an exact next decomposition:

```text
response = finite control mean + centered placement deviation.
```

Whether the actual/source-aligned deviation obeys a reusable bound remains
`OPEN`.  Fixed-power credit is zero; full Gate B and the twin-prime endpoint
remain open.
