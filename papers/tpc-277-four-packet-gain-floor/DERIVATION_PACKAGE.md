# TPC-277 derivation package

## 1. Four-packet geometry

Let `V_0,...,V_3` be vectors in a real or complex Hilbert space.  Put

```text
D = sum_j ||V_j||^2,
S = V_0+V_1+V_2+V_3,
G = ||S||^2,
E = sum_{j<k} Re <V_j,V_k>.
```

Then `G=D+2E`.  Cauchy--Schwarz gives

```text
G <= (sum_j ||V_j||)^2 <= 4D.
```

When `E<=0`, `G<=D`.  For `G>0`, define

```text
r=D/G,  kappa=(D-G)/D=-2E/D.
```

The exact coordinate change is `r=(1-kappa)^(-1)`.

## 2. Sharpness and the missing asymptotic input

Four equal aligned packets attain `r=1/4`; four nonzero orthogonal packets
attain `r=1`.  Thus geometry alone cannot produce a positive exponent in a
bound `r>=b x^gamma`: an orthogonal family has `r=1` for every `x`.
Large gain requires `kappa` to approach one, equivalently `G/D` to approach
zero.  Merely proving `E<=0` supplies only the constant floor `r>=1`.

## 3. Exact source replay

For each declared row, the certificate constructs the actual beta source and
prime shell from TPC-268, accumulates the four packet outputs, applies the
three declared Haar contrasts to the output vectors, and computes `D,G` with
exact rational arithmetic.  Outward intervals at grid `10^15` are stored;
the exact pair `(D,G)` is represented by a SHA-256 replay digest.  The
independent checker recomputes the pair with the column-major accumulation
order.

## 4. Firewall

The eight rows establish neither a uniform lower bound nor a power law.  The
one-percent floor fails at the smallest-gain row, but this is only a finite
registered/extended obstruction.  No arithmetic cancellation, `L2` estimate,
full Gate-B payment, or twin-prime result is inferred.
