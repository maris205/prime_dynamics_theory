# TPC-340 derivation package

For a finite vector `x` supported on `S`, TPC-339 gives

```text
||A x||^2 <= F(S)^2 ||x||^2,
F(S)^2 = ||A[:,S]||_F^2.                                  (1)
```

For a symmetric finite matrix define

```text
R = max_i sum_j |A(i,j)|.
```

Because `||A||_1=||A||_infty=R`, the standard induced-norm inequality gives

```text
||A||_2 <= sqrt(||A||_1 ||A||_infty) = R,
||A x||^2 <= R^2 ||x||^2.                                  (2)
```

Taking the smaller of the two valid right-hand sides yields the sign-free
hybrid envelope

```text
||A x||^2 <= min(F(supp(x))^2,R^2) ||x||^2.                 (3)
```

The active branch is a diagnostic: it does not change the proof of (3).
For nonzero `x`, the hybrid occupancy is the response gain divided by the
hybrid gain and is at most one.

The exact anchor uses the symmetric matrix with every entry in absolute value
one, `A=[[1,-1],[-1,1]]`, and `x=(1,1)`.  Its response energy is zero, source
norm is two, and `R^2=4`, explicitly satisfying (2).
