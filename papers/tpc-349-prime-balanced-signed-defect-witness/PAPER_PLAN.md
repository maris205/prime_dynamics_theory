# TPC-349 paper plan

## Research question

TPC-348 showed that the literal divisibility-mask defect has deterministic
positive coordinate witnesses.  The next minimal question is whether a
prime-balanced signed combination of those hit coordinates exposes a stronger,
reusable lower-witness structure.

## Declared object

For the sorted shell `p_0 < ... < p_(r-1)`, use the zero-sum split

```text
beta_j = +1 for j < floor(r/2),
          0 for the possible middle prime,
         -1 for j >= r-floor(r/2).
```

Set `h_p(t)=1_(p divides t)`, `b_I=sum_j beta_j h_(p_j)`, and
`x_I=b_I/||b_I||_2` whenever `b_I` is nonzero.  The comparison baseline is the
TPC-348 best mask-hit coordinate column, computed only as a finite diagnostic.

## Claim targets

1. Prove the exact incidence and prime-Gram identities.
2. Prove the induced-norm lower bound `||D_I|| >= ||D_I b_I||/||b_I||`.
3. Audit the frozen 192-row panel, including an exact multi-hit anchor.
4. Test whether the signed witness uniformly improves the coordinate baseline;
   if not, record the obstruction and keep the arithmetic firewall closed.

## Validation plan

The producer locks TPC-348 code and certificate.  An independent checker rebuilds
the matrices in reverse shell order and checks every row.  A stress suite mutates
the balance rule, incidence support, census, range, anchor, and claim firewall.
Normal and optimized Python runs must agree; the PDF must compile cleanly.

## Expected decision

Promotion requires a theorem beyond finite linear algebra.  A finite positive
census can only support a `NUMERICALLY_CERTIFIED_FINITE` label.  The next route
question, conditional on this paper, is fresh/growing-panel replication of the
signed incidence Gram rather than an arithmetic conclusion.
