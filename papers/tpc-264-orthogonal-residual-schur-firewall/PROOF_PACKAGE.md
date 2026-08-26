# TPC-264 proof package

Use the conjugate-linear-first-slot convention
`<r,s>=sum conjugate(r_j)s_j`.

## Theorem 1 — exact residual Schur feasible set

Let `P` be an orthogonal projection on a complex Hilbert space `H`, let
`w,g in H`, and write

```text
p=Pw, q=Pg, u=(I-P)w, v=(I-P)g,
a=||u||, b=||v||, c=<p,q>.
```

Condition on the projected vectors `p,q`, the residual norms `a,b`, and the
dimension `m=dim ker(P)`.

1. If `m>=2`, the possible values of `z=<u,v>` are exactly
   `{z in C: |z|<=ab}`.
2. If `m=1` and `ab>0`, the possible values are exactly
   `{z in C: |z|=ab}`.
3. If `m=0` or `ab=0`, the only possible value is `z=0`.

Consequently, the possible values of the full coupling `<w,g>` are obtained
by translating these sets by `c`.

### Proof

Because `P` is orthogonal, `p,u` and `q,v` lie in mutually orthogonal
subspaces.  Hence

```text
<w,g>=<p+u,q+v>=<p,q>+<u,v>=c+z.
```

The residual Gram matrix

```text
Gamma = [[a^2,z],[conjugate(z),b^2]]
```

is positive semidefinite.  Its determinant is nonnegative, giving
`|z|<=ab`.

Suppose `m>=2` and `a,b>0`.  Choose orthonormal `e_1,e_2` in `ker(P)`.  For
any `z` with `|z|<=ab`, set `r=|z|/(ab)` and choose `theta` so that
`z=ab r e^{i theta}`.  Define

```text
u=a e_1,
v=b(r e^{i theta}e_1 + sqrt(1-r^2)e_2).
```

Then `||u||=a`, `||v||=b`, and, under the stated convention,
`<u,v>=ab r e^{i theta}=z`.  Thus every point of the disk is realized.

If `m=1`, write `u=alpha e` and `v=beta e` in a unit vector `e`.  Fixed norms
give `|alpha|=a`, `|beta|=b`, so `|<u,v>|=|conjugate(alpha)beta|=ab`.
All phases are realized by varying `beta/alpha`.  If `m=0`, both residuals
vanish.  If `a=0` or `b=0`, Cauchy--Schwarz forces `z=0`.  Translation by `c`
finishes the full-coupling statement. `(square)`

## Theorem 2 — Schur firewall at the endpoint scale

Assume only the data of Theorem 1 and allow a structural family with
`a=b=x^(5/6)` and complement dimension at least two.  Then the feasible
residual set contains `z=x^(5/3)` and `z=-x^(5/3)`.  If additionally
`|c|=O(x^(5/3)/(log x)^M)` for every fixed `M`, the feasible full coupling
still contains a value of magnitude at least
`x^(5/3)-|c|`, and hence no bound `O(x^(5/3-delta))` follows from these data
for any fixed `delta>0`.

### Proof

Theorem 1 includes both endpoints of the disk.  Choose `z` with phase opposite
to `c` (or either endpoint if `c=0`); then `|c+z|>=x^(5/3)-|c|` by the reverse
triangle inequality.  Since `x^delta/(log x)^M` tends to infinity, this
quantity is not `O(x^(5/3-delta))`.  The scale family is synthetic and the
conclusion is a statement about non-identifiability under the declared data,
not a literal prime-shell construction. `(square)`

## Corollary — minimum missing theorem

On the actual V59 clock, TPC-263 supplies a logarithmically small center
`c=C_3`.  A sufficient next input for a fixed-power endpoint payment is either

```text
||(I-P_3)w|| ||(I-P_3)A_x beta|| << x^(5/3-delta), delta>1/400,
```

after all reassembly losses, or a direct signed estimate for the residual inner
product `<(I-P_3)w,(I-P_3)A_x beta>` with the same effective saving.  The
corollary is conditional; neither input is proved here.

## Scope firewall

```text
PROVED = exact projection split; Schur disk/circle/singleton classification;
         translated full-coupling feasible sets; endpoint implication under
         declared synthetic scale family
NUMERICALLY_CERTIFIED = rational and Gaussian finite witnesses; dimension-case
                        stress replay and mutation rejection
CONDITIONAL_THEOREM = residual norm or signed residual estimate would pay the
                      endpoint only under the displayed strict hypothesis
OPEN = actual V59 residual norm product, actual residual phase/cross-Gram,
       arithmetic L2, full Gate B, twin-prime theorem
REFUTED_SCOPED = dropping C_perp or inferring a fixed-power saving from P3 data
                 plus norm-only residual information
MODELING_CHOICE = synthetic x^(5/6) residual scale
```
