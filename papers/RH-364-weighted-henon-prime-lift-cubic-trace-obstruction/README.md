# RH-364: Weighted Hénon prime lift and cubic trace obstruction

RH-364 is an independent trigger-5 theorem paper built from the exact local
hyperbolic survivor of

```text
H_6(x,y) = (1-6x^2-y,x).
```

The survivor is conjugate to the four-state subshift with adjacency matrix

```text
A = [[1,0,1,0],
     [1,0,0,0],
     [0,1,0,1],
     [0,1,0,0]].
```

Writing `phi=(1+sqrt(5))/2` and `kappa=773/224`, the paper proves:

- `tr(A^n)=Lucas_n+2 cos(n*pi/2)`, with primitive orbit counts
  `p_n=(1/n) sum_(d|n) mu(d) tr(A^(n/d))` and
  `p_n <= 4 phi^n/n`;
- the exact cone certificate gives every primitive survivor multiplier
  `L_o >= kappa^(n_o)`;
- for every real `beta>=0`, the weighted Euler zeta and determinant converge
  normally and are zero-free on

  ```text
  |z| < kappa^beta/phi,
  ```

  with an explicit all-order primitive-period tail bound;
- the flat/Euler correction is analytic and zero-free on the larger disk
  `|z|<kappa^2/phi`, but this does not continue either complete determinant
  beyond their common certified disk;
- the common-clock prime-copy operator

  ```text
  T_s = direct_sum_(ell prime) ell^(-s) A
  ```

  is in `S_q` exactly when `q Re(s)>1`.  Its ordinary Fredholm determinant is
  licensed on `Re(s)>1`, while genuine regularized `det_m` exists on
  `m Re(s)>1`;
- for the inverse determinant, the prime-power trace weights begin

  ```text
  (F_1,F_2,F_3) = (1,1,4).
  ```

  Thus primes and prime squares match von Mangoldt weights, but prime cubes
  have weight `4 log p`, with exact surplus `3 log p`;
- the natural positive-weight prime lift has a fractional non-meromorphic
  singularity at `s=1` for every real `beta>0`;
- the unique common scalar normalization fixes orders one and two but gives

  ```text
  Q_3 = 1 + 3 (L_*^3/L_3)^beta > 1,
  ```

  so it fails at cubes for every real `beta>=0`.

The normalized infinite product is source-certified near `s=1` only for

```text
0 <= beta < beta_0
beta_0 = log(2/phi)/log(L_*/kappa)
       = 0.290834898770...
```

For larger `beta`, the coefficient obstruction remains exact, but no
near-`s=1` analytic continuation is claimed.

## Route boundary

Route A is `GO`: the paper supplies a local all-order analytic theorem, exact
Schatten/Fredholm regions, a fractional-singularity theorem, and a strict
cubic trace obstruction.

Route B is `STOP_SCOPED`.  Copying the same survivor matrix over all prime
labels is an engineered functor, not a finite-field reduction, Hasse--Weil
factor, full `H_p` zeta, canonical global Hénon operator, or the physical
centered noisy determinant.  Even inside this functor, Gate D fails at prime
cubes.

Gates A--E remain false/open.  No Hilbert--Pólya operator, self-adjoint
generator, intrinsic `T log T` law, Riemann-zero identification,
completed-zeta divisor equality, or proof of RH is claimed.

## Reproduction

```bash
make result
make test
make pdf
make archive
```

Finite rows reproduce exact matrix, orbit-count, multiplier, radius, and
first-trace identities only.  The all-order conclusions are proved in the
manuscript; the reported finite-section root near `3.429` is explicitly not
certified.
