# TPC-293 proof package

## Theorem 1 — all-positive complete-graph benchmark

For the complete graph `K_m` with every edge sign `+1`,

```text
max_{a_i in {−1,+1}} #{i<j:a_i a_j=-1} = floor(m^2/4).
```

**Proof.** Let `r` vertices have label `+1`. An edge is favorable exactly
when its endpoints have different labels, so the favorable count is
`r(m-r)`. Since
`r(m-r)=m^2/4-(r-m/2)^2`, it is at most `floor(m^2/4)`. Choosing
`r=floor(m/2)` attains the bound. ∎

## Theorem 2 — signed frustration complement

For any loopless signed graph with `E` edges, if

```text
F = max_a #{(i,j) in E:a_i a_j sigma_ij=-1},
```

then the minimum number of unsatisfied edges is exactly `E-F`.

**Proof.** For any fixed labeling every edge is either favorable or
unfavorable, so its unsatisfied count is `E` minus its favorable count.
Minimizing the former over labelings is therefore the same as subtracting
the maximum of the latter from `E`. ∎

## Lemma 3 — switching invariance

For vertex signs `t_i`, define `sigma'_{ij}=t_i sigma_ij t_j`. Then
`F(sigma')=F(sigma)`.

**Proof.** Map a labeling `a` to `a'_i=t_i a_i`. For every edge,
`a'_i a'_j sigma'_{ij}=a_i a_j sigma_ij`. This is a bijection of
labelings preserving the favorable-edge indicator, hence preserves the
maximum. ∎

## Lemma 4 — triangle parity consistency

On a triangle with nonzero edge signs, all three equations
`a_i a_j sigma_ij=-1` are simultaneously solvable if and only if
`sigma_12 sigma_13 sigma_23=-1`.

**Proof.** Multiplication gives the necessary condition because each vertex
sign occurs twice. If the product is `-1`, set `a_1=1`,
`a_2=-sigma_12`, and `a_3=-sigma_13`; the last edge then also satisfies the
equation. ∎

## Finite certificate consequence

The exact-rational producer and the independent column-first replay agree on
all 18 rows. The certified finite census is

```text
edges = 1,380
max favorable = 744
minimum unsatisfied = 636
signed gain over all-positive benchmark = 3
all-positive rows = 17
signed-gain rows = 1
triangles = 5,727
sign-frustrated triangles = 5,718
```

The exceptional row is a finite sign observation. It does not promote the
unit-weight objective to the magnitude-weighted Gram quadratic form, and no
asymptotic or arithmetic claim follows from it.
