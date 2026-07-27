# TPC-124: Provenance-faithful physical reassembly

Paper title:

> *Provenance-Faithful Physical Reassembly of the TPC Hard Packet:
> Native-Leaf and Physical Residuals, Exact Block Cover, and Dual
> Certificates*

## Core result

Let `z` be the retained native-leaf vector supplied by a complete
TPC-123 archive. Let

```text
G : native leaves -> physical carriers,
C : block coefficients -> native leaves,
B = G C,
w = G z.
```

There are two different canonical residuals:

```text
r_leaf = (I - C C^dagger) z,
r_phys = (I - B B^dagger) w.
```

The exact decompositions are

```text
z = C C^dagger z + r_leaf,
w = B C^dagger z + G r_leaf
  = B B^dagger w + r_phys.
```

Native-leaf cover implies physical cover, but the converse can fail:
the grouping map can erase a nonzero provenance residual. Therefore a
zero physical residual is an H6-type fact, not by itself an H8
reconnection certificate.

More precisely, with `P_B = B B^dagger`,

```text
H = (I - P_B) G restricted to ker(C*),
r_phys = H r_leaf.
```

The minimum modulus of `H` on the full residual domain is the exact
criterion for whether physical residual control can be reversed to
native-leaf residual control. It includes zero singular directions;
the least positive singular value on the kernel complement is not
enough when `H` has a kernel. No growing lower bound for this value is
claimed.

The paper also proves separate dual tests for the two covers and the
exact Gram identity

```text
B* B = C* G* G C.
```

Determinant fibers and distinguished-zero-mode fibers must be joined
to the physical archive by separate explicit maps. They are not
identified by notation.

## Current verdict

The exact finite theorem and rational regression model pass. The
machine certificate explicitly computes the residual-transfer map on
the one-dimensional test domain, obtaining squared minimum moduli `1`
and `0` in the faithful and collapsed models. It labels these as a
finite coordinate-model regression only. The actual growing `G`, `C`,
`z` and `B` archives are not all present:

```text
PHYSICAL REASSEMBLY VERDICT = NOT_TESTABLE_FROM_CURRENT_ARTIFACTS
```

## Claim level

- Residual, duality and Gram identities: L0.
- Their typed attachment to the TPC-123/TPC-114/TPC-117 objects: L1.
- No growing cover theorem, residual `o(X)` theorem, endpoint
  exponent, fixed-`h0` L2 saving or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc124_reassembly_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-124-provenance-faithful-physical-reassembly.pdf`

SHA-256:

`1c8e06956d3481b0265bb489d21927487e9af959f16644cf12e31cffe9363006`
