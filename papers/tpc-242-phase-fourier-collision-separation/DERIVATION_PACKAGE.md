# TPC-242 derivation package

## A. Convention-sensitive expansion

The inner product is conjugate-linear in its first slot. Hence

```text
<alpha u,v> = conjugate(alpha)<u,v>,
<u,alpha v> = alpha<u,v>.
```

With `c=<Y,X>` and `S=||X||^2+||Y||^2`, this fixes the expansion

```text
||X+i^jY||^2 = S+i^j conjugate(c)+i^(-j)c.
```

The orientation is not cosmetic. Multiplication by `i^(k j)` gives the mode
conditions

| contribution | surviving condition | selected mode |
|---|---:|---:|
| `S` | `k=0 mod 4` | `F_0` |
| `conjugate(c)` | `k+1=0 mod 4` | `F_3` |
| `c` | `k-1=0 mod 4` | `F_1` |

Thus the literal `i^j` transform selects `c=<Y,X>`. Changing either the
inner-product convention or the phase sign conjugates the answer.

## B. Common-offset projection

For `E'_j=E_j+A`,

```text
F'_k-F_k = (A/4) sum_(j=0)^3 i^(k j).
```

The increment is `A` at `k=0` and zero at every nontrivial character. In
particular, its `F_1` component is exactly zero. The word *common* means the
same additive scalar in all four labelled energies; an unsigned estimate on a
separate object has no such label structure.

## C. Sharp disk construction

The inequalities

```text
|<Y,X>|^2 <= ||X||^2||Y||^2
           <= ((||X||^2+||Y||^2)/2)^2
```

give the closed disk upper inclusion. For `S>0`, put `rho=|z|`,
`D=sqrt(S^2-4rho^2)`, `a=(S+D)/2`, and `b=(S-D)/2`. Then `a>0`,
`a+b=S`, and `ab=rho^2`. For any unit vector `e`, the one-dimensional witness

```text
X=sqrt(a)e,
Y=(conjugate(z)/sqrt(a))e
```

has squared norms `a,b` and selected coefficient `z`. This realizes every
point inside any nonzero complex Hilbert space, not merely the boundary. At
`S=0`, both vectors vanish.

Three diagnostic points at `S=2` are exact:

```text
z=0:       X=(1,0), Y=(0,1),
z=1/3+2i/3: X=(1,0), Y=(1/3-2i/3,2/3),
z=i:       X=(1,0), Y=(-i,0).
```

They are certificate illustrations only; the construction above proves the
continuum statement.

## D. Defect decomposition

For `a=||X||^2`, `b=||Y||^2`, and `c=<Y,X>`, insert and subtract `4ab`:

```text
(a+b)^2-4|c|^2
 = (a-b)^2+4(ab-|c|^2).
```

The first term measures energy imbalance. The second is four times the Gram
determinant and measures failure of collinearity. A strict deficit from the
boundary requires one of these two mechanisms.

## E. Typed route implication

The algebra has input type

```text
FOUR_PHASE_ENERGIES_FROM_ONE_COMMON_PAIR_(X,Y).
```

TPC-241 has output type

```text
UNSIGNED_STANDALONE_COMMON_PROFILE_NORM_FLOOR.
```

No repository theorem supplies the conversion from the latter to the former.
Therefore no TPC-241 numerical floor can be inserted into `F_0` or declared a
common offset. The valid conclusion is zero direct transfer, not physical
annihilation.
