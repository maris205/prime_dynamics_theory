# Theorem ledger

## Proven statements

`PROVED` — Zero-hole frequency projection.  For prime `q`, with
`y=(A_hat(k))_(k!=0)` and `P=I-(q-1)^-1 11*`,

```text
V_0(a;v) = 1/q y* P y,
rank(P) = q-2.
```

The case `q=2` is the zero-dimensional variance after deleting residue zero.

`PROVED` — Complete-graph tight frame.  If
`Delta_(k,l)(n)=e_q(-kn)-e_q(-ln)`, then

```text
V_0(a;v)
 = 1/[q(q-1)] sum_{{k,l} in E(K_(q-1))}
     |sum_n a_n e(vn/H) Delta_(k,l)(n)|^2.
```

The edge count is `(q-1)(q-2)/2`, the rank is `q-2`, and the frame redundancy
is `(q-1)/2` for `q>2`.

`PROVED` — Edge mass and exact diagonal distribution:

```text
sum_e |Delta_e(n)|^2 = q(q-2) 1_(q does not divide n),

1/[q(q-1)] sum_e sum_n |a_n|^2 |Delta_e(n)|^2
 = (q-2)/(q-1) sum_(q does not divide n) |a_n|^2.
```

`PROVED` — Pure off-diagonal edge compiler.  After subtracting its own
coefficient diagonal, each edge cell is exactly a sum over `t!=u`, and

```text
q R_0(a;v) = 1/(q-1) sum_e E_e^circ[a](v).
```

`PROVED` — Edgewise four-packet polarization.  For
`a^(j)=beta+i^j w`, weights `i^j/4` recover the bilinear edge cell before any
absolute value or edge, block, or prime-modulus triangle inequality.

`PROVED` — Physical-kernel crosswalk.  The edge contraction is

```text
K_q(r,s) = 0          if rs=0,
           q(q-2)     if r=s!=0,
           -q         if r,s!=0 and r!=s.
```

Thus `K_q(r,s)/(q-1)` is exactly the original frozen V59 coefficient
`q(1_(r=s)-1/(q-1))` on unit residues.

`PROVED` — Oriented difference-fiber form.  With `l=k+d`,

```text
Delta_(k,k+d)(n)=e_q(-kn)(1-e_q(-dn)),
```

and the ordered `(d,k)` sum carries the exact factor `1/2` with
`d!=0`, `k!=0,-d`.

`PROVED`, scoped — Literal edge no-sparsification.  In any scalar-weighted
decomposition

```text
P = sum_(k<l) w_(k,l)(e_k-e_l)(e_k-e_l)*,
```

the `(k,l)` matrix entry forces `w_(k,l)=1/(q-1)` for every edge.  Hence no
strict subset works in this literal two-frequency class.  Dense bases,
higher-rank cells, and joint source theorems remain possible.

`REFUTED` — Separate absolute estimation of equal and off-equal additive
frequencies.  A row supported only at residue zero has `V_0=0`, while the two
pieces are `+(q-1)|L|^2/q` and `-(q-1)|L|^2/q`.

## Classification

```text
CLAIM_LEVEL=PROVED_STRUCTURAL_L1
V61_ROUTE_ADVANCE=YES
V61_STRUCTURAL_THRESHOLD_A=PASS
V61_FULL_GATE_B_STRICT_1_OVER_400=UNPAID
V61_ARITHMETIC_ADVANCE=NO
V61_FIXED_ATOM_CREDIT=0
V61_L2=NONE
V61_TPC_208_TRIGGER=true
```

## Strongest positive result

The complete nonzero-frequency projection, mandatory coefficient-diagonal
deletion, four-packet signs, and original physical residue kernel now occupy
one exact tight-frame representation.  No cancellation is deferred between
separately estimated frequency-diagonal and frequency-off-diagonal pieces.

## Strongest obstruction

The literal two-frequency representation is uniquely the full complete
graph.  Edgewise sparsification is impossible, so an arithmetic estimate must
retain or exploit collective frame geometry instead of paying one absolute
value per edge.

## Open theorem

Apply source-valid Möbius/Poisson or Voronoi transformations to the complete
oriented `(d,k)` frame of the literal V59 blocks, obtain legitimate
Kloosterman bilinear cells, and reassemble all block pairs, four-packet signs,
and prime moduli with a fixed saving greater than `1/400`.

## Reusable structure

```text
zero-hole projector
  = complete-graph Laplacian on nonzero additive frequencies
  + edgewise coefficient-diagonal deletion
  + oriented unit-annihilating difference fibers.
```

## ROUND2_CLUE

Apply the next transform to the whole `(d,k)` tight frame before any edge or
fiber triangle inequality.  Test whether Poisson summation creates a dual
variable shared across the frame; a shared variable is the narrowest plausible
mechanism for retaining the complete-graph cancellation through emission.
